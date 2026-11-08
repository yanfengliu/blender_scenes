"""Build an editable sailor-uniform character and render its camera views headlessly."""
import argparse
import ctypes
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'outputs' / 'sailor_character'
PROGRESS = '[sailor-build] '


class WindowsJob:
    """Own Blender and all descendants, including children surviving its exit."""

    def __init__(self):
        from ctypes import wintypes

        class BasicLimits(ctypes.Structure):
            _fields_ = [
                ('PerProcessUserTimeLimit', ctypes.c_int64),
                ('PerJobUserTimeLimit', ctypes.c_int64),
                ('LimitFlags', wintypes.DWORD),
                ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t),
                ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t),
                ('PriorityClass', wintypes.DWORD),
                ('SchedulingClass', wintypes.DWORD),
            ]

        class IoCounters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in (
                'ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
                'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [
                ('BasicLimitInformation', BasicLimits),
                ('IoInfo', IoCounters),
                ('ProcessMemoryLimit', ctypes.c_size_t),
                ('JobMemoryLimit', ctypes.c_size_t),
                ('PeakProcessMemoryUsed', ctypes.c_size_t),
                ('PeakJobMemoryUsed', ctypes.c_size_t),
            ]

        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.api.CreateJobObjectW.restype = wintypes.HANDLE
        self.api.SetInformationJobObject.argtypes = [
            wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.api.SetInformationJobObject.restype = wintypes.BOOL
        self.api.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.api.AssignProcessToJobObject.restype = wintypes.BOOL
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api.CloseHandle.restype = wintypes.BOOL
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.BasicLimitInformation.LimitFlags = 0x2000  # KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(
                self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process):
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('must be a positive integer')
    return number


def camera_views(value):
    views = [view.strip() for view in value.split(',')]
    allowed = {'hero', 'portrait', 'back', 'profile'}
    if not views or any(view not in allowed for view in views):
        raise argparse.ArgumentTypeError(
            f'Invalid views {value!r}; choose comma-separated hero, portrait, back, or profile.')
    if len(views) != len(set(views)):
        raise argparse.ArgumentTypeError(f'Duplicate views in {value!r}; name each view once.')
    return views


def selected_views(args):
    if args.no_render:
        return []
    if args.views is not None:
        return args.views
    return ['hero'] if args.preview else ['hero', 'portrait', 'back']


def build_paths(args):
    def resolve(path):
        path = Path(path).expanduser()
        return (path if path.is_absolute() else ROOT / path).resolve()

    return resolve(args.scene), resolve(args.output_dir)


def blender_script(args):
    """Keep scene construction reusable and render orchestration in the runner."""
    scene_source, output = build_paths(args)
    views = selected_views(args)
    return f'''import bpy
from pathlib import Path

OUTPUT_DIR = {str(output)!r}
RENDER_SIZE = {args.size}
SAMPLES = {args.samples}
bpy.context.preferences.filepaths.save_version = 0
print({PROGRESS!r} + 'Constructing the character scene...', flush=True)
source = Path({str(scene_source)!r})
exec(compile(source.read_text(encoding='utf-8'), str(source), 'exec'), globals())
scene = bpy.context.scene
scene.cycles.samples = SAMPLES
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
dimensions = {{
    'hero': (max(1, int(RENDER_SIZE * .8)), RENDER_SIZE),
    'portrait': (min(RENDER_SIZE, 1200), min(RENDER_SIZE, 1200)),
    'back': (max(1, int(min(RENDER_SIZE, 1100) * .8)), min(RENDER_SIZE, 1100)),
    'profile': (min(RENDER_SIZE, 1200), min(RENDER_SIZE, 1200)),
}}
for view in {views!r}:
    camera = bpy.data.objects.get('Camera_' + view)
    if camera is None or camera.type != 'CAMERA':
        raise RuntimeError('Missing camera: Camera_' + view)
    scene.camera = camera
    scene.render.resolution_x, scene.render.resolution_y = dimensions[view]
    scene.render.filepath = str(Path(OUTPUT_DIR) / (view + '.png'))
    print({PROGRESS!r} + 'Rendering ' + view + '...', flush=True)
    bpy.ops.render.render(write_still=True)
    print({PROGRESS!r} + 'Saved ' + view + '.png', flush=True)
scene.camera = bpy.data.objects['Camera_hero']
scene.render.resolution_x, scene.render.resolution_y = dimensions['hero']
scene.render.filepath = str(Path(OUTPUT_DIR) / 'hero.png')
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(Path(OUTPUT_DIR) / 'sailor_character.blend'))
print({PROGRESS!r} + 'Saved the editable scene with the hero camera selected.', flush=True)
'''


def close_owned_process(process, job):
    if job is not None:
        # Closing the job also removes descendants after a successful Blender exit.
        job.close()
    if process is None:
        return
    if os.name != 'nt':
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        # Assignment failure can occur before the process joins our job.
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=subprocess.CREATE_NO_WINDOW, check=False)
    try:
        process.wait(timeout=15)
    except subprocess.TimeoutExpired:
        if os.name != 'nt':
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        process.wait(timeout=10)


def run(args):
    scene_source, output = build_paths(args)
    if not scene_source.is_file():
        raise FileNotFoundError(f'Scene source is missing: {scene_source}')
    output.mkdir(parents=True, exist_ok=True)
    expected = [output / 'sailor_character.blend']
    expected.extend(output / (view + '.png') for view in selected_views(args))
    before = {path: path.stat().st_mtime_ns if path.exists() else None for path in expected}
    process = None
    job = None
    scratch_path = None
    log_path = None
    succeeded = False
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py',
                                         prefix='build_', dir=output, delete=False) as scratch:
            scratch_path = Path(scratch.name)
            scratch.write(blender_script(args))
        log_path = scratch_path.with_suffix('.log')
        if os.name == 'nt':
            job = WindowsJob()
        command = [args.blender, '--background', '--factory-startup',
                   '--python-exit-code', '1', '--python', str(scratch_path)]
        with log_path.open('w', encoding='utf-8') as log:
            process = subprocess.Popen(
                command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                start_new_session=os.name != 'nt',
                env=dict(os.environ, PYTHONUNBUFFERED='1'))
            if job is not None:
                job.assign(process)
            print(f'Owned headless Blender PID {process.pid}. Log: {log_path}', flush=True)
            started = time.monotonic()
            last_report = started
            with log_path.open('r', encoding='utf-8', errors='replace') as reader:
                while True:
                    for line in reader:
                        if PROGRESS in line:
                            print(line[line.index(PROGRESS):].strip(), flush=True)
                    if process.poll() is not None:
                        # The writer is closed now, so collect its last progress lines.
                        for line in reader:
                            if PROGRESS in line:
                                print(line[line.index(PROGRESS):].strip(), flush=True)
                        break
                    now = time.monotonic()
                    if now - last_report >= 30:
                        print(f'Blender is working ({int(now - started)} seconds elapsed).', flush=True)
                        last_report = now
                    time.sleep(.5)
            if process.returncode:
                raise RuntimeError(f'Blender exited with code {process.returncode}; see {log_path}')
        for path in expected:
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f'Blender did not create the expected artifact: {path}')
            if path.stat().st_mtime_ns == before[path]:
                raise RuntimeError(f'Blender did not refresh the expected artifact: {path}')
        succeeded = True
        print(f'Finished: {output / "sailor_character.blend"}', flush=True)
    finally:
        close_owned_process(process, job)
        print('Owned Blender process and its descendants closed.', flush=True)
        if succeeded:
            for path in (scratch_path, log_path):
                if path is not None:
                    path.unlink(missing_ok=True)
        elif log_path is not None and log_path.exists():
            print(f'Failure evidence retained: {log_path}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--scene', type=Path, default=ROOT / 'scenes' / 'sailor_character.py',
                        help='Scene source path; relative paths resolve against the repository root.')
    parser.add_argument('--output-dir', type=Path, default=OUTPUT,
                        help='Output directory; relative paths resolve against the repository root.')
    parser.add_argument('--size', type=positive_int, default=1600,
                        help='Hero image height in pixels (width is 80%% of height).')
    parser.add_argument('--samples', type=positive_int, default=80)
    parser.add_argument('--preview', action='store_true', help='Render only hero.png unless --views is set.')
    parser.add_argument('--views', type=camera_views,
                        help='Render selected comma-separated views: hero,portrait,back,profile; overrides --preview.')
    parser.add_argument('--no-render', action='store_true', help='Build and save the editable scene only.')
    run(parser.parse_args())

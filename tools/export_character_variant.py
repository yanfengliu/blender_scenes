"""Export a separate complete unclothed adult body from an existing saved model.

Usage: python tools/export_character_variant.py --input saved.blend --output-dir NEW_FOLDER
The source is never saved. Full-body front/back/profile renders use the existing
lighting; this does not change anatomy, pose, face, hair or introduce a rig.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
BASE_SHA = '8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c'


def file_hash(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def export(args):
    import bmesh
    import bpy
    from mathutils import Vector
    sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
    from prepare_human_base import read_obj
    from natural_face import skin_regions
    from check_character_variant import (BODY, CLOTHING, require, body_snapshot, retained_snapshot,
                                          materials_snapshot, verify, negative_checks)
    require(args.output_dir != args.input.parent and not any((args.output_dir/name).exists()
            for name in ('unclothed.blend', 'front.png', 'back.png', 'profile.png', 'oblique.png', 'verification.json')),
            'Internal export also requires fresh artifact paths, separate from the source.')
    require(file_hash(args.base) == BASE_SHA, 'Canonical CC0 base.obj hash differs.')
    base = read_obj(args.base)
    selected = [i for i, group in enumerate(base['face_groups']) if group == 'body']
    canonical = {key: [base[key][i] for i in selected] for key in ('faces', 'face_uvs')}
    canonical['uvs'] = base['uvs']
    require(len(base['vertices']) == 19158 and len(canonical['faces']) == 13378, 'Unexpected base population.')
    bpy.ops.wm.open_mainfile(filepath=str(args.input), load_ui=False)
    body = bpy.data.objects[BODY]
    require(body.get('character_age', 0) >= 18, 'Expected explicitly adult character metadata.')
    require(len(body.data.vertices) == 19158, 'Saved body vertex identity differs.')
    before = body_snapshot(body)
    require(set(before['loops']).issubset(canonical['faces']), 'Saved topology is not canonical body topology.')
    require(set(body.data.uv_layers.keys()) == {'UVMap', 'ReferenceFaceProjection'} and
            set(body.data.color_attributes.keys()) == {'SkinToneGain', 'SkinResponse', 'ReferenceSkinBlend'},
            'New UV/color layers need an explicit restored-loop initialization contract.')
    clothing = bpy.data.collections[CLOTHING]
    removed = sorted(o.name for o in clothing.all_objects)
    retained = [o for o in bpy.context.scene.objects if o != body and o.name not in removed]
    retained_before = retained_snapshot(retained)
    materials = [m for m in bpy.data.materials]
    material_names = [m.name for m in materials]
    material_before = materials_snapshot(materials)
    vertex_values = {}
    for polygon in body.data.polygons:
        for li in polygon.loop_indices:
            vertex_values[body.data.loops[li].vertex_index] = (
                tuple(body.data.uv_layers['ReferenceFaceProjection'].data[li].uv),
                {a.name: tuple(a.data[li].color) for a in body.data.color_attributes})
    bm = bmesh.new()
    try:
        bm.from_mesh(body.data)
        bm.verts.ensure_lookup_table()
        uv = {name: bm.loops.layers.uv[name] for name in body.data.uv_layers.keys()}
        colors = {name: bm.loops.layers.float_color[name] for name in body.data.color_attributes.keys()}
        lip_center = (body.data.vertices[509].co.z+body.data.vertices[495].co.z)/2
        for face, uvface in zip(canonical['faces'], canonical['face_uvs']):
            if face in before['loops']:
                continue
            polygon = bm.faces.new([bm.verts[i] for i in face])
            polygon.smooth = True
            for loop, index in zip(polygon.loops, uvface):
                vertex = loop.vert.index
                gain, oil, lip, cheek = skin_regions(loop.vert.co, lip_center)
                projection, values = vertex_values.get(vertex, ((0, 0), {
                    'SkinToneGain': (*gain, 1), 'SkinResponse': (oil, lip, cheek, 1),
                    'ReferenceSkinBlend': (0, 0, 0, 1)}))
                loop[uv['UVMap']].uv = canonical['uvs'][index]
                loop[uv['ReferenceFaceProjection']].uv = projection
                for name, layer in colors.items():
                    loop[layer] = values[name]
        bm.to_mesh(body.data)
        # BMesh adds UV-selection flags and elides an all-false sharp_face layer.
        schema = {name for name, _, _ in before['attributes']}
        for attribute in list(body.data.attributes):
            if attribute.name not in schema:
                require(attribute.name.startswith('.uv_select_'), 'Unexpected BMesh attribute.')
                body.data.attributes.remove(attribute)
        if 'sharp_face' in schema and 'sharp_face' not in body.data.attributes:
            body.data.attributes.new('sharp_face', 'BOOLEAN', 'FACE')
        body.data.update()
    finally:
        bm.free()
    for name in removed:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    bpy.data.collections.remove(clothing)
    report = verify(body, canonical, before, list(bpy.context.scene.objects), removed)
    require(retained_snapshot(retained) == retained_before, 'Retained face/hair/studio data changed.')
    require(materials_snapshot(materials) == material_before, 'Material graphs changed.')
    report['negative_controls'] = negative_checks(body, canonical, before, list(bpy.context.scene.objects), removed)
    report.update(input=str(args.input), input_sha256=file_hash(args.input), canonical_base_sha256=BASE_SHA,
                  removed_objects=removed, retained_objects_exact=True, material_graphs_exact=True,
                  restored_attribute_policy='Existing loop values exact; new loops use vertex values where present, otherwise skin_regions. Unused reference projection/mask are zero only on newly exposed vertices.')
    scene = bpy.context.scene
    scene['Variant'] = 'Unclothed adult copy; complete canonical body faces; static original pose'
    scene['Geometry'] = 'Same saved adult anatomy, face and hair; restored body topology; clothing removed'
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    require(any(d.type == 'OPTIX' for d in prefs.devices), 'Inspection renders require the available OptiX GPU.')
    for device in prefs.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = args.samples
    scene.render.resolution_x, scene.render.resolution_y = int(args.size*.8), args.size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    cameras = {}
    rng = random.Random(20261107)
    positions = [('front', (0, -4.5, .85)), ('back', (0, 4.5, .85)), ('profile', (4.5, 0, .85)),
                 ('oblique', (rng.uniform(2.4, 3.2), rng.uniform(-4.0, -3.2), rng.uniform(1.0, 1.4)))]
    report['inspection_cameras'] = {'seed': 20261107, 'positions_m': dict(positions),
                                    'target_m': [0, 0, .85], 'ortho_scale_m': 1.90}
    for name, position in positions:
        data = bpy.data.cameras.new('Variant inspection / '+name)
        camera = bpy.data.objects.new(data.name, data)
        scene.collection.objects.link(camera)
        camera.location = position
        camera.rotation_euler = (Vector((0, 0, .85))-camera.location).to_track_quat('-Z', 'Y').to_euler()
        data.type, data.ortho_scale = 'ORTHO', 1.90
        scene.camera = camera
        scene.render.filepath = str(args.output_dir/(name+'.png'))
        print('Rendering full-body '+name, flush=True)
        bpy.ops.render.render(write_still=True)
        cameras[name] = camera
    scene.camera = cameras['front']
    scene.render.filepath = str(args.output_dir/'front.png')
    bpy.context.preferences.filepaths.save_version = 0
    target = args.output_dir/'unclothed.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    bpy.ops.wm.open_mainfile(filepath=str(target), load_ui=False)
    verify(bpy.data.objects[BODY], canonical, before, list(bpy.context.scene.objects), removed)
    require(retained_snapshot([bpy.data.objects[n] for n in retained_before]) == retained_before,
            'Saved retained face/hair/studio data differs.')
    require(materials_snapshot([bpy.data.materials[name] for name in material_names]) == material_before,
            'Saved material graphs differ.')
    report.update(saved_reopened_verified=True, samples=args.samples, resolution=[int(args.size*.8), args.size])
    (args.output_dir/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


def run(args, script=None, artifact_names=('unclothed.blend', 'front.png', 'back.png', 'profile.png', 'oblique.png')):
    from build_sailor_character import WindowsJob, close_owned_process
    if not args.input.is_file() or args.input.suffix.lower() != '.blend':
        raise ValueError('Input must be an existing saved .blend file.')
    if args.output_dir == args.input.parent or (args.output_dir.exists() and any(args.output_dir.iterdir())):
        raise ValueError('Use a fresh output folder; the source and existing variants are never overwritten.')
    source_hash = file_hash(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    log_path = args.output_dir/'export.log'
    job, process, succeeded = None, None, False
    try:
        job = WindowsJob() if os.name == 'nt' else None
        command = [args.blender, '--background', '--factory-startup', '--python-exit-code', '1',
                   '--python', str(Path(script or __file__).resolve()), '--', '--inside-blender',
                   '--input', str(args.input), '--output-dir', str(args.output_dir), '--base', str(args.base),
                   '--samples', str(args.samples), '--size', str(args.size)]
        with log_path.open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                                       start_new_session=os.name != 'nt')
            if job:
                job.assign(process)
            print(f'Owned headless Blender PID {process.pid}; log: {log_path}', flush=True)
            deadline = time.monotonic()+args.timeout
            while process.poll() is None:
                remaining = deadline-time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f'Export exceeded {args.timeout}s; inspect {log_path}')
                try:
                    process.wait(timeout=min(30, remaining))
                except subprocess.TimeoutExpired:
                    print('Blender is exporting and rendering the separate variant.', flush=True)
            if process.returncode:
                raise RuntimeError(f'Blender failed; inspect {log_path}')
        if file_hash(args.input) != source_hash:
            raise AssertionError('The dressed input file changed during export.')
        report = json.loads((args.output_dir/'verification.json').read_text(encoding='utf-8'))
        report['input_unchanged_sha256'] = source_hash
        report['artifacts'] = {name: file_hash(args.output_dir/name) for name in artifact_names}
        (args.output_dir/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        succeeded = True
    finally:
        close_owned_process(process, job)
        print('Owned Blender process and descendants closed.', flush=True)
        if file_hash(args.input) != source_hash:
            raise AssertionError('The dressed input file changed during export (including failure cleanup).')
        if succeeded:
            log_path.unlink(missing_ok=True)


if __name__ == '__main__':
    from build_sailor_character import positive_int
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--base', type=Path, default=ROOT/'.tools/human_reference_assets/base.obj')
    parser.add_argument('--blender', default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--samples', type=positive_int, default=128)
    parser.add_argument('--size', type=positive_int, default=1600)
    parser.add_argument('--timeout', type=positive_int, default=900, help='Maximum owned Blender runtime in seconds.')
    parser.add_argument('--inside-blender', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    args.input, args.output_dir, args.base = (p.expanduser().resolve() for p in (args.input, args.output_dir, args.base))
    export(args) if args.inside_blender else run(args)

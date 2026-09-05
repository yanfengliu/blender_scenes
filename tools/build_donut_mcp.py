"""Build the donut through the official Blender Lab MCP, then close both servers."""
import argparse
import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import socket
import subprocess
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


def checked_result(response):
    payload = response.structuredContent
    if payload is None:
        payload = json.loads(next(item.text for item in response.content if item.type == 'text'))
    if response.isError or payload.get('status') != 'ok':
        raise RuntimeError(f'Blender MCP rejected the request: {payload}')
    return payload.get('result')


async def run(args):
    output = ROOT / 'outputs/donut'
    output.mkdir(parents=True, exist_ok=True)
    cache = ROOT / '.tools/optix-cache'
    cache.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    command = [args.blender, '--background', '--factory-startup', '--online-mode',
               '--python', str(ROOT / 'tools/blender_bootstrap.py'), '--command',
               'blender_mcp', '--host', '127.0.0.1', '--port', str(port)]
    proc = None
    try:
        with (output / 'blender.log').open('w', encoding='utf-8') as log:
            proc = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                    env=dict(os.environ, OPTIX_CACHE_PATH=str(cache)), cwd=ROOT,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            print(f'Owned headless Blender PID {proc.pid}; port {port}', flush=True)
            for _ in range(100):
                if proc.poll() is not None:
                    raise RuntimeError(f'Blender exited: read {output / "blender.log"}')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=.2):
                        break
                except OSError:
                    await asyncio.sleep(.2)
            else:
                raise TimeoutError('Blender MCP did not start within 20 seconds')
            env = dict(os.environ, BLENDER_MCP_HOST='127.0.0.1', BLENDER_MCP_PORT=str(port))
            parameters = StdioServerParameters(command=str(ROOT / '.venv/Scripts/blender-mcp.exe'), env=env)
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=300)) as session:
                    await session.initialize()
                    catalog = await session.list_tools()
                    assert 'execute_blender_code' in [tool.name for tool in catalog.tools]
                    code = (ROOT / 'scenes/donut.py').read_text(encoding='utf-8')
                    prelude = f'OUTPUT_DIR = {str(output)!r}\nRENDER_SIZE = {args.size}\nSAMPLES = {args.samples}\n'
                    started = time.time()
                    response = await session.call_tool('execute_blender_code', {'code': prelude + code})
                    serialized = response.model_dump(mode='json')
                    (output / 'mcp_build.json').write_text(json.dumps(serialized, indent=2), encoding='utf-8')
                    print(json.dumps(serialized), flush=True)
                    built = checked_result(response)
                    blend = output / 'strawberry_donut.blend'
                    if Path(built['blend_file']) != blend or not blend.exists() or blend.stat().st_mtime < started:
                        raise RuntimeError('MCP build failed; see outputs/donut/mcp_build.json')
                    if not args.no_render:
                        for view in ['hero', 'overhead', 'detail']:
                            print(f'Rendering {view} through MCP...', flush=True)
                            render_code = f"""import bpy
from pathlib import Path
scene = bpy.context.scene
scene.camera = bpy.data.objects[{('Camera_' + view)!r}]
scene.render.resolution_x = {args.size if view == 'hero' else min(args.size, 900)}
scene.render.resolution_y = {int(args.size * .8) if view == 'hero' else min(args.size, 900)}
scene.render.filepath = {str(output / (view + '.png'))!r}
bpy.ops.render.render(write_still=True)
result = {{'view': {view!r}, 'path': scene.render.filepath}}
"""
                            started = time.time()
                            rendered = await session.call_tool('execute_blender_code', {'code': render_code})
                            (output / f'mcp_{view}.json').write_text(rendered.model_dump_json(indent=2), encoding='utf-8')
                            saved = checked_result(rendered)
                            png = output / f'{view}.png'
                            if Path(saved['path']) != png or not png.exists() or png.stat().st_mtime < started:
                                raise RuntimeError(f'MCP render failed for {view}')
                            print(f'Saved {view}.png', flush=True)
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=10)
        print('Owned Blender process closed; MCP stdio context closed.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--size', type=int, default=1500)
    parser.add_argument('--samples', type=int, default=96)
    parser.add_argument('--no-render', action='store_true')
    asyncio.run(run(parser.parse_args()))

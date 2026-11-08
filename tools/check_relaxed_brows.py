"""Check the visually accepted brows, including actual render-level geometry.

Run in owned background Blender with the saved character, or use -- --production
to execute the main scene's unchanged anatomy/eye prefix and final frame map.
The coordinate pin records an accepted visual result, not a claim of realism.
Projection and continuous separation checks reject folded or buried ribbons.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
from brow_uv_checks import projected_disks
from triangle_clearance import triangle_clearance, controls

BODY = 'Haru / anatomical adult skin'
ACCEPTED_COORDINATES = 'fdaf6f8106f99f88086eeafe9e6d5c798d9c19d774ec4aa709ef5e93d946db28'


def coordinate_hash(obj):
    return hashlib.sha256(b''.join(struct.pack('<3f', *v.co) for v in obj.data.vertices)).hexdigest()


def evaluated(obj):
    assert obj.matrix_world == Matrix.Identity(4)
    settings = [(m, m.levels) for m in obj.modifiers if m.type == 'SUBSURF']
    live = None
    try:
        for modifier, _ in settings:
            modifier.levels = modifier.render_levels
        bpy.context.view_layer.update()
        live = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = live.to_mesh()
        mesh.calc_loop_triangles()
        return {'points': [v.co.copy() for v in mesh.vertices],
                'faces': [tuple(p.vertices) for p in mesh.polygons],
                'triangles': [tuple(t.vertices) for t in mesh.loop_triangles]}
    finally:
        if live is not None:
            live.to_mesh_clear()
        for modifier, level in settings:
            modifier.levels = level
        bpy.context.view_layer.update()


def validate_brows(brows, body, *, visual_pin=True):
    if visual_pin:
        assert coordinate_hash(brows) == ACCEPTED_COORDINATES, 'Brows differ from the visually accepted shape.'
    surface = evaluated(brows)
    structure = projected_disks(surface)
    skin = evaluated(body)
    assert min(p.y for p in skin['points']) > -.5, 'Front-ray origin is not exterior.'
    tree = BVHTree.FromPolygons(skin['points'], skin['triangles'], all_triangles=True)
    offsets = []
    for point in surface['points']:
        hit, _, _, _ = tree.ray_cast(Vector((point.x, -.5, point.z)), Vector((0, 1, 0)))
        assert hit is not None, 'Brow point lacks forehead support.'
        offsets.append(hit.y-point.y)
    # Candidate 10's measured global standoff envelope, with the reviewed 50 um allowance.
    assert min(offsets) >= .0002078 and max(offsets) <= .0008784, 'Brow floats above or enters the forehead.'
    def query(center):
        stored = Vector(center)
        location, _, _, distance = tree.find_nearest(stored)
        assert location is not None
        return distance, math.dist(center, tuple(stored))
    proofs = [triangle_clearance([surface['points'][i] for i in t], query) for t in surface['triangles']]
    assert all(p['pass'] for p in proofs), 'Whole brow triangle is not certified clear of skin.'
    return {'status': 'pass', 'coordinates_sha256': coordinate_hash(brows), 'structure': structure,
            'front_offset_range_m': [min(offsets), max(offsets)], 'continuous_triangles': len(proofs),
            'clearance_controls': controls()}


def production_prefix():
    """Exercise the real call site without regenerating unrelated clothes/hair."""
    source = ROOT/'scenes/sailor_character_realistic.py'
    nodes = ast.parse(source.read_text(encoding='utf-8'), filename=str(source)).body
    boundaries = [i for i, n in enumerate(nodes) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'group' for t in n.targets)
                  and isinstance(n.value, ast.Subscript) and isinstance(n.value.slice, ast.Constant)
                  and n.value.slice.value == '04 Sailor clothing']
    assert len(boundaries) == 1
    finish = [n for n in nodes if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == 'upper_frame_diagnostics' for t in n.targets)]
    assert len(finish) == 1
    scope = {'__file__': str(source), 'OUTPUT_DIR': str(ROOT/'outputs/brow-source-check')}
    exec(compile(ast.Module(body=nodes[:boundaries[0]]+finish, type_ignores=[]), str(source), 'exec'), scope)


def negative_controls(brows, body):
    original = [v.co.copy() for v in brows.data.vertices]
    accepted = evaluated(brows)
    folded = {**accepted, 'points': [p.copy() for p in accepted['points']]}
    a, b, _ = folded['triangles'][0]
    folded['points'][a], folded['points'][b] = folded['points'][b], folded['points'][a]
    try:
        projected_disks(folded)
    except AssertionError:
        pass
    else:
        raise AssertionError('Folded-surface control was accepted.')
    rejected = []
    try:
        for name in ('inner_hook', 'buried', 'floating'):
            for vertex, point in zip(brows.data.vertices, original):
                vertex.co = point
                if name == 'inner_hook' and abs(point.x) < .025:
                    vertex.co.z -= .003
                elif name == 'buried':
                    vertex.co.y += .002
                elif name == 'floating':
                    vertex.co.y -= .002
            brows.data.update()
            bpy.context.view_layer.update()
            try:
                validate_brows(brows, body, visual_pin=name == 'inner_hook')
            except AssertionError:
                rejected.append(name)
            else:
                raise AssertionError(f'{name} negative was accepted.')
    finally:
        for vertex, point in zip(brows.data.vertices, original):
            vertex.co = point
        brows.data.update()
        bpy.context.view_layer.update()
    assert coordinate_hash(brows) == ACCEPTED_COORDINATES
    return ['folded_surface', *rejected]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.production:
        production_prefix()
    brows, body = bpy.data.objects['Eyebrows'], bpy.data.objects[BODY]
    result = validate_brows(brows, body)
    result['negative_controls'] = negative_controls(brows, body)
    result['production_prefix'] = args.production
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

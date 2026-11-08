"""Check saved garment isolation and actual smiled-body clearance; never save.

Blender --background --python-exit-code 1 --python tools/check_garment_isolation.py
  -- --baseline candidate4.blend --smile-reference candidate5.blend
  --candidate candidate6.blend --negative candidate5.blend --output receipt.json

Exact fingerprints cover both complete garment meshes, UVs, attributes, material
graphs, transforms and modifiers. Clearance covers all evaluated blouse/collar
inner, outer and rim triangles against canonical unculled anatomy reconstructed
from the candidate's actual saved coordinates, never neutral inputs or receipts.
Seven nearest-normal samples per triangle must retain the existing 0.2 mm gap,
with zero BVH overlap pairs. These are finite geometric checks, not a continuous
distance, self-collision, comfort or appearance proof.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import traceback

import bpy
from mathutils import Matrix
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_human_base import ASSETS, load_body

BODY = 'Haru / anatomical adult skin'
GARMENTS = ('Blouse / connected shoulders and short sleeves',
            'Sailor collar / continuous fitted fabric')
BASE_SHA = '8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c'
MINIMUM_GAP_M = .0002


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def file_hash(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def plain(value):
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    if isinstance(value, set):
        return sorted(value)
    return [plain(item) for item in value]


def properties(item):
    """All writable scalar/array RNA settings; pointers handled explicitly."""
    return {p.identifier: plain(getattr(item, p.identifier))
            for p in item.bl_rna.properties
            if not p.is_readonly and p.type in {'BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM'}}


def material_snapshot(material):
    require(material is not None and material.use_nodes, 'Garment material must use nodes.')
    require(material.animation_data is None and material.node_tree.animation_data is None,
            'Animated garment materials need a separate evaluation contract.')
    nodes = []
    allowed = {'OUTPUT_MATERIAL', 'BSDF_PRINCIPLED', 'TEX_NOISE', 'BUMP',
               'ATTRIBUTE', 'MATH', 'MIX_RGB'}
    for node in material.node_tree.nodes:
        require(node.type in allowed, f'Unsupported garment shader node {node.type}; expand snapshot coverage explicitly.')
        entry = {'type': node.bl_idname, 'settings': properties(node),
                 'inputs': [(s.identifier, plain(s.default_value))
                            for s in node.inputs if hasattr(s, 'default_value')]}
        for key in ('texture_mapping', 'color_mapping'):
            if hasattr(node, key):
                mapping = getattr(node, key)
                entry[key] = properties(mapping)
                if hasattr(mapping, 'color_ramp'):
                    entry[key]['ramp'] = {'settings': properties(mapping.color_ramp),
                                          'elements': [properties(e) for e in mapping.color_ramp.elements]}
        nodes.append(entry)
    links = [(l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier)
             for l in material.node_tree.links]
    return {'settings': properties(material), 'nodes': nodes, 'links': sorted(links)}


def modifier_snapshot(obj):
    require(obj.animation_data is None and not obj.constraints,
            f'{obj.name}: animated or constrained geometry is outside this check.')
    for modifier in obj.modifiers:
        require(modifier.type in {'SUBSURF', 'SOLIDIFY'}, 'Uncovered garment/body modifier type.')
    return [(m.type, properties(m)) for m in obj.modifiers]


def garment_snapshot(obj):
    mesh = obj.data
    require(obj.type == 'MESH' and mesh.shape_keys is None and mesh.animation_data is None and not mesh.has_custom_normals,
            'Garment snapshots require unkeyed meshes without custom split normals.')
    require(not obj.vertex_groups, 'Garment vertex-group weights need explicit snapshot coverage.')
    parts = {
        'vertices': [tuple(v.co) for v in mesh.vertices],
        'edges': [(tuple(e.vertices), e.use_seam, e.use_edge_sharp) for e in mesh.edges],
        'faces': [(tuple(p.vertices), p.material_index, p.use_smooth) for p in mesh.polygons],
        'loops': [(loop.vertex_index, loop.edge_index) for loop in mesh.loops],
        'attributes': [(a.name, a.domain, a.data_type, [properties(item) for item in a.data])
                       for a in mesh.attributes],
        'uv_layers': [(layer.name, layer.active_render, layer.active_clone,
                       [tuple(item.uv) for item in layer.data]) for layer in mesh.uv_layers],
        'active_layers': (mesh.uv_layers.active_index, mesh.attributes.active_index,
                          mesh.color_attributes.active_color_index, mesh.color_attributes.render_color_index),
        'materials': [(slot.link, material_snapshot(slot.material)) for slot in obj.material_slots],
        'transform': {key: plain(getattr(obj, key)) for key in
                      ('matrix_world', 'matrix_basis', 'matrix_parent_inverse')},
        'parent': obj.parent.name if obj.parent else None,
        'modifiers': modifier_snapshot(obj),
        'mesh_settings': properties(mesh),
    }
    result = {key: digest(value) for key, value in parts.items()}
    result['population'] = {'vertices': len(mesh.vertices), 'edges': len(mesh.edges),
                            'polygons': len(mesh.polygons), 'loops': len(mesh.loops),
                            'attributes': len(mesh.attributes), 'uv_layers': len(mesh.uv_layers)}
    return result


def body_snapshot(body):
    require(body.type == 'MESH' and body.data.shape_keys is None, 'Expected unkeyed saved body mesh.')
    require(body.data.animation_data is None and not body.vertex_groups,
            'Animated or weighted body mesh needs an explicit reconstruction contract.')
    require(not any(body.data.attributes.get(name) is not None for name in ('crease_edge', 'crease_vert')),
            'Body subdivision creases are outside the canonical reconstruction contract.')
    return {'coordinates': digest([tuple(v.co) for v in body.data.vertices]),
            'faces': digest([tuple(p.vertices) for p in body.data.polygons]),
            'vertices': len(body.data.vertices), 'polygons': len(body.data.polygons),
            'transform': digest(plain(body.matrix_world)), 'modifiers': digest(modifier_snapshot(body))}


def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    return {'garments': {name: garment_snapshot(bpy.data.objects[name]) for name in GARMENTS},
            'body': body_snapshot(bpy.data.objects[BODY])}


def differences(first, second):
    return {name: [key for key in first[name] if first[name][key] != second[name][key]]
            for name in GARMENTS if first[name] != second[name]}


def evaluated(obj):
    graph = bpy.context.evaluated_depsgraph_get()
    live = obj.evaluated_get(graph)
    mesh = live.to_mesh(preserve_all_data_layers=True, depsgraph=graph)
    try:
        mesh.calc_loop_triangles()
        return ([live.matrix_world @ v.co for v in mesh.vertices],
                [tuple(p.vertices) for p in mesh.polygons],
                [tuple(t.vertices) for t in mesh.loop_triangles])
    finally:
        live.to_mesh_clear()


def cycle(face):
    return min(face[i:]+face[:i] for i in range(len(face)))


def shell_layers(obj):
    """Prove both complete face layers and every boundary rim on a private copy."""
    copy = obj.copy()
    bpy.context.scene.collection.objects.link(copy)
    try:
        require(copy.modifiers and copy.modifiers[-1].type == 'SOLIDIFY', 'Expected final Solidify.')
        solid = copy.modifiers[-1]
        require(solid.show_viewport and solid.show_render and solid.use_rim, 'Complete active shell required.')
        require(all(m.show_viewport and m.show_render and
                    (m.type != 'SUBSURF' or m.levels == m.render_levels) for m in copy.modifiers),
                'Viewport/render modifier evaluation differs.')
        solid.show_viewport = False
        bpy.context.view_layer.update()
        base, faces, _ = evaluated(copy)
        solid.show_viewport = True
        bpy.context.view_layer.update()
        points, shell_faces, triangles = evaluated(copy)
        count = len(base)
        require(len(points) == 2*count, 'Solidify did not retain two complete vertex layers.')
        expected = Counter(cycle(face) for face in faces)
        edges = Counter(tuple(sorted(edge)) for f in faces for edge in zip(f, f[1:]+f[:1]))
        require(all(n in (1, 2) for n in edges.values()), 'Nonmanifold cloth base.')
        boundary = Counter({e: 1 for e, n in edges.items() if n == 1})
        oriented, rims = [Counter(), Counter()], Counter()
        for face in shell_faces:
            if all(i < count for i in face):
                oriented[0][cycle(face)] += 1
            elif all(i >= count for i in face):
                oriented[1][cycle(tuple(i-count for i in reversed(face)))] += 1
            else:
                edge = tuple(sorted({i % count for i in face}))
                require(len(face) == 4 and set(face) == {v+offset for v in edge for offset in (0, count)},
                        'Unrecognized rim correspondence.')
                rims[edge] += 1
        require(oriented == [expected, expected] and rims == boundary, 'Incomplete inner/outer/rim face coverage.')
        layers = {'outer': [], 'inner': [], 'rim': []}
        for triangle in triangles:
            key = 'outer' if all(i < count for i in triangle) else 'inner' if all(i >= count for i in triangle) else 'rim'
            layers[key].append(triangle)
        require(all(layers.values()), 'A complete clothing shell layer is empty.')
        return points, layers
    finally:
        bpy.data.objects.remove(copy, do_unlink=True)
        bpy.context.view_layer.update()


def measure(points, triangles, body_tree):
    overlap = BVHTree.FromPolygons(points, triangles, all_triangles=True).overlap(body_tree)
    minimum, worst = float('inf'), None
    for indices in triangles:
        a, b, c = (points[i] for i in indices)
        for point in (a, b, c, (a+b+c)/3, (a+b)/2, (b+c)/2, (c+a)/2):
            location, normal, face, _ = body_tree.find_nearest(point)
            require(location is not None, 'Full-body nearest query returned no surface.')
            gap = (point-location).dot(normal)
            if gap < minimum:
                minimum, worst = gap, {'point_m': tuple(point), 'body_triangle': face}
    return {'triangles': len(triangles), 'samples': 7*len(triangles),
            'overlap_pairs': len(overlap), 'minimum_signed_gap_m': minimum, 'worst': worst,
            'required_minimum_gap_m': MINIMUM_GAP_M, 'pass': minimum >= MINIMUM_GAP_M and not overlap}


def clearance(body, canonical):
    require(bpy.context.scene.unit_settings.scale_length == 1.0,
            'Garment clearance requires one Blender unit per metre.')
    body_snapshot(body)
    require(body.matrix_world == Matrix.Identity(4), 'Canonical-body reconstruction requires baked coordinates.')
    require(len(body.data.vertices) == len(canonical['vertices']) == 19158, 'Full saved source body population changed.')
    faces = canonical['faces']
    require(len(faces) == 13378, 'Canonical body face population changed.')
    visible = Counter(cycle(tuple(p.vertices)) for p in body.data.polygons)
    complete = Counter(cycle(face) for face in faces)
    require(not visible-complete and all(n == 1 for n in complete.values()), 'Visible skin is not a canonical subset.')
    edges = Counter(tuple(sorted(e)) for f in faces for e in zip(f, f[1:]+f[:1]))
    require(all(n == 2 for n in edges.values()), 'Canonical body must be closed and manifold.')
    require(len(body.modifiers) == 1 and body.modifiers[0].type == 'SUBSURF' and
            body.modifiers[0].levels == body.modifiers[0].render_levels == 2 and
            body.modifiers[0].show_viewport and body.modifiers[0].show_render, 'Expected active body Subsurf2.')
    data = bpy.data.meshes.new('Garment isolation temporary full body')
    full = None
    try:
        data.from_pydata([tuple(v.co) for v in body.data.vertices], [], faces)
        data.update()
        full = body.copy()
        full.data = data
        bpy.context.scene.collection.objects.link(full)
        bpy.context.view_layer.update()
        points, _, triangles = evaluated(full)
        require(len(triangles) == 13378*16*2, 'Canonical evaluated body triangle population changed.')
        volume = sum(points[a].dot(points[b].cross(points[c])) for a, b, c in triangles)/6
        require(volume > 0, 'Canonical body orientation is not outward.')
        tree = BVHTree.FromPolygons(points, triangles, all_triangles=True)
        garments = {}
        for name in GARMENTS:
            shell, layers = shell_layers(bpy.data.objects[name])
            garments[name] = {layer: measure(shell, tris, tree) for layer, tris in layers.items()}
        return {'pass': all(r['pass'] for rows in garments.values() for r in rows.values()),
                'actual_saved_coordinate_sha256': body_snapshot(body)['coordinates'],
                'source_vertices': len(body.data.vertices), 'canonical_faces': len(faces),
                'visible_faces': len(body.data.polygons), 'restored_hidden_faces': len(faces)-len(body.data.polygons),
                'evaluated_body_triangles': len(triangles), 'signed_body_volume_m3': volume, 'garments': garments}
    finally:
        if full is not None:
            bpy.data.objects.remove(full, do_unlink=True)
        bpy.data.meshes.remove(data)
        bpy.context.view_layer.update()


def penetration_control(body, canonical):
    """Bulge the actual saved chest through the frozen shirt, then restore it."""
    before = [v.co.copy() for v in body.data.vertices]
    changed = 0
    try:
        for vertex in body.data.vertices:
            if abs(vertex.co.x) < .12 and 1.13 < vertex.co.z < 1.27 and vertex.co.y < -.07:
                vertex.co.y -= .05
                changed += 1
        require(changed > 30, 'Actual-body penetration control has insufficient chest vertices.')
        body.data.update()
        bpy.context.view_layer.update()
        result = clearance(body, canonical)
        rows = result['garments'][GARMENTS[0]].values()
        require(not result['pass'] and any(r['minimum_signed_gap_m'] < -.001 for r in rows)
                and any(r['overlap_pairs'] for r in rows), 'Actual-body penetration control was not rejected.')
        return {'pass': True, 'mutated_saved_body_vertices': changed, 'measurement': result}
    finally:
        for vertex, point in zip(body.data.vertices, before):
            vertex.co = point
        body.data.update()
        bpy.context.view_layer.update()
        require(all(v.co == p for v, p in zip(body.data.vertices, before)), 'Negative control did not restore actual body.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('baseline', 'smile-reference', 'candidate', 'negative', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--assets', type=Path, default=ASSETS)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    paths = {key: getattr(args, key).resolve() for key in ('baseline', 'smile_reference', 'candidate', 'negative')}
    require(args.output.resolve() not in paths.values() and args.output.suffix.lower() == '.json',
            'Output must be a separate JSON receipt, never a saved scene input.')
    receipt = {'status': 'fail', 'bound': __doc__, 'paths': {k: str(p) for k, p in paths.items()}}
    hashes = {key: file_hash(path) for key, path in paths.items()}
    try:
        baseline, smile, negative, candidate = (capture(paths[key]) for key in
                                                ('baseline', 'smile_reference', 'negative', 'candidate'))
        drift = differences(baseline['garments'], candidate['garments'])
        negative_drift = differences(baseline['garments'], negative['garments'])
        receipt.update(garment_fingerprints={'baseline': baseline['garments'], 'candidate': candidate['garments']},
                       garment_drift=drift, historical_negative_drift=negative_drift,
                       body={'baseline': baseline['body'], 'smile_reference': smile['body'], 'candidate': candidate['body']})
        require(not drift, f'Candidate garments differ from accepted baseline: {drift}')
        require(all('vertices' in negative_drift.get(name, []) for name in GARMENTS),
                'Historical negative must expose actual coordinate drift in both garments.')
        require(candidate['body'] == smile['body'], 'Candidate actual body differs from retained smile reference.')
        require(candidate['body']['faces'] == baseline['body']['faces'], 'Candidate changed accepted visible body topology.')
        require(file_hash(args.assets/'base.obj') == BASE_SHA, 'Canonical body asset digest changed.')
        canonical = load_body(targets=(), assets=args.assets)
        body = bpy.data.objects[BODY]
        receipt['clearance'] = clearance(body, canonical)
        receipt['actual_body_penetration_control'] = penetration_control(body, canonical)
        require(body_snapshot(body) == candidate['body'] and
                {name: garment_snapshot(bpy.data.objects[name]) for name in GARMENTS} == candidate['garments'],
                'Verification changed actual saved source data in memory.')
        require(receipt['clearance']['pass'], 'Actual smiled-body clothing clearance failed.')
        receipt['status'] = 'pass'
    except Exception as error:
        receipt['error'] = str(error)
        traceback.print_exc()
    finally:
        receipt['saved_files_unchanged'] = all(file_hash(paths[k]) == h for k, h in hashes.items())
        receipt['file_sha256'] = hashes
        if not receipt['saved_files_unchanged']:
            receipt.update(status='fail', error='A saved input file changed during verification.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(receipt, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    require(receipt['status'] == 'pass', receipt.get('error', 'Garment isolation failed.'))
    print('GARMENT_ISOLATION: pass; actual saved data and negative controls.', flush=True)


if __name__ == '__main__':
    main()

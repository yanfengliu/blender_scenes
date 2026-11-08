"""Bounded saved-copy checks for the adult character's complete unclothed variant.

Imported by export_character_variant inside Blender. Comparisons use the saved
source's actual vertex identities, retained loops, materials and hair geometry.
"""
from collections import Counter
import hashlib
import json
import re

BODY = 'Haru / anatomical adult skin'
CLOTHING = '04 Sailor clothing'
WEAR = re.compile(r'blouse|collar|skirt|sock|shoe|loafer|neckerchief|barrette|accessor|ribbon', re.I)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def properties(item):
    def plain(value):
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return sorted(value) if isinstance(value, set) else [plain(v) for v in value]
    return {p.identifier: plain(getattr(item, p.identifier)) for p in item.bl_rna.properties
            if not p.is_readonly and p.type in {'BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM'}}


def body_snapshot(body):
    mesh = body.data
    require(not mesh.shape_keys and not mesh.has_custom_normals and not body.vertex_groups,
            'Keyed, custom-normal or weighted bodies require a separate export contract.')
    loops = {tuple(p.vertices): {
        'settings': (p.material_index, p.use_smooth),
        'uv': {a.name: [tuple(a.data[i].uv) for i in p.loop_indices] for a in mesh.uv_layers},
        'color': {a.name: [tuple(a.data[i].color) for i in p.loop_indices] for a in mesh.color_attributes}
    } for p in mesh.polygons}
    return {'coordinates': digest([tuple(v.co) for v in mesh.vertices]), 'loops': loops,
            'attributes': sorted((a.name, a.domain, a.data_type) for a in mesh.attributes),
            'materials': [m.name for m in mesh.materials],
            'modifiers': [(m.type, properties(m)) for m in body.modifiers],
            'matrix': [list(row) for row in body.matrix_world],
            'uv_active': [(a.name, a.active_render, a.active_clone) for a in mesh.uv_layers]}


def retained_snapshot(objects):
    """Retained objects and materials never get reconstructed by the exporter."""
    result = {}
    for obj in objects:
        data = obj.data
        shape = None
        if obj.type == 'MESH':
            shape = ([tuple(v.co) for v in data.vertices], [tuple(p.vertices) for p in data.polygons],
                     [(a.name, [properties(d) for d in a.data]) for a in data.attributes])
        elif obj.type == 'CURVE':
            shape = [(properties(s), [properties(p) for p in s.points],
                      [properties(p) for p in s.bezier_points]) for s in data.splines]
        result[obj.name] = digest((properties(obj), properties(data), shape,
                                   [(m.type, properties(m)) for m in obj.modifiers],
                                   [list(row) for row in obj.matrix_world]))
    return result


def materials_snapshot(materials):
    return digest([(m.name, properties(m),
                    [(n.name, properties(n), [(s.name, properties(s)) for s in n.inputs],
                      n.image.name if n.type == 'TEX_IMAGE' and n.image else None)
                     for n in m.node_tree.nodes] if m.use_nodes else [],
                    [(l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier)
                     for l in m.node_tree.links] if m.use_nodes else []) for m in materials])


def verify(body, canonical, before, objects, removed):
    actual = body_snapshot(body)
    require(Counter(tuple(p.vertices) for p in body.data.polygons) == Counter(canonical['faces']),
            'Body is culled or has noncanonical faces.')
    for key in ('coordinates', 'attributes', 'materials', 'modifiers', 'matrix', 'uv_active'):
        require(actual[key] == before[key], f'Body {key} changed.')
    require(all(actual['loops'].get(face) == row for face, row in before['loops'].items()),
            'An original visible face UV, color attribute or surface setting changed.')
    expected_uv = dict(zip(canonical['faces'], canonical['face_uvs']))
    uv = body.data.uv_layers['UVMap']
    for poly in body.data.polygons:
        for li, index in zip(poly.loop_indices, expected_uv[tuple(poly.vertices)]):
            require(all(abs(a-b) < 1e-7 for a, b in zip(uv.data[li].uv, canonical['uvs'][index])),
                    'A body loop lost its canonical photographic UV.')
    names = {o.name for o in objects}
    require(not names.intersection(removed) and not any(WEAR.search(name) for name in names),
            'Clothing, shoes, socks or an accessory remains.')
    return {'vertices': len(body.data.vertices), 'faces': len(body.data.polygons),
            'restored_faces': len(body.data.polygons)-len(before['loops']),
            'preserved_visible_faces': len(before['loops']), 'preserved_visible_loops': sum(map(len, before['loops'])),
            'coordinates_sha256': actual['coordinates'], 'all_canonical_faces_and_uvs': True,
            'visible_loop_uvs_and_colors_exact': True, 'modifiers_and_material_slots_exact': True,
            'attribute_schema_before': before['attributes'], 'attribute_schema_after': actual['attributes']}


def negative_checks(body, canonical, before, objects, removed):
    """Prove the checker rejects both historical failure classes, without saving."""
    from types import SimpleNamespace
    import bmesh
    import bpy
    original = body.data
    damaged = original.copy()
    outcomes = {}
    try:
        bm = bmesh.new()
        try:
            bm.from_mesh(damaged)
            bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm, geom=[bm.faces[-1]], context='FACES_ONLY')
            bm.to_mesh(damaged)
        finally:
            bm.free()
        body.data = damaged
        try:
            verify(body, canonical, before, objects, removed)
        except AssertionError as error:
            require('culled' in str(error), 'Culling negative failed for the wrong reason.')
            outcomes['culled_body'] = str(error)
        else:
            raise AssertionError('Culled-body negative control was accepted.')
    finally:
        body.data = original
        bpy.data.meshes.remove(damaged)
    for name, population in [('leftover_sock', [*objects, SimpleNamespace(name='Sock / negative control')])]:
        try:
            verify(body, canonical, before, population, removed)
        except AssertionError as error:
            outcomes[name] = str(error)
        else:
            raise AssertionError(f'Negative control was accepted: {name}')
    return outcomes

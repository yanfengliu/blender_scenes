"""Localized editable adult anatomy for the complete unclothed variant.

Coordinates are metres in the saved character's identity frame. The broad
chest response and small surface folds are separate fields on a continuous
skin mesh; no detached spheres, texture-plane patches or internal organs.
"""
import math
from collections import Counter
import hashlib
import struct


def smooth(a, b, value):
    t = max(0., min(1., (value-a)/(b-a)))
    return t*t*t*(10+t*(-15+6*t))


def disk(radius):
    return max(0., 1-radius*radius)**3


def fields(point):
    """Return displacement and areola/nipple/external-fold pigment weights."""
    x, y, z = point
    dx = dy = dz = areola = nipple = fold_tone = 0.
    side = -1. if x < 0 else 1.
    if 1.09 < z < 1.325 and abs(x) < .19 and y < -.06:
        # Add volume around existing tissue, fading before sternum, arm and rib.
        radius = math.hypot((abs(x)-.083)/.092, (z-1.196)/.098)
        volume = (1-smooth(.25, 1., radius))*smooth(.085, .125, -y)
        volume *= smooth(.005, .030, abs(x))
        dx += side*.014*volume
        dy -= .035*volume
        dz -= .008*volume
        # The original detailed nipple rings are centred on these actual rows.
        # Tangent projection follows their outward-facing orientation.
        tangent = .81*(abs(x)-.1000)+.58*(y+.1774)
        vertical = z-1.2035
        radial = math.hypot(tangent, vertical)
        front = smooth(.142, .160, -y)
        areola = (1-smooth(.008, .014, radial))*front
        nipple = disk(radial/.0042)*front
        relief = .00055*areola+.0030*nipple
        dx += side*.58*relief
        dy -= .81*relief
    if .755 < z < .852 and abs(x) < .044 and y < -.045:
        # Closed external vulvar form. Soft outer folds flank a shallow cleft;
        # smaller inner relief and hood merge into the same continuous surface.
        along = (z-.803)/.038
        envelope = disk(abs(along))
        lateral = disk(abs(x)/.040)
        front = smooth(.055, .085, -y)
        weight = envelope*lateral*front
        separation = .0045+.0075*max(0., 1-along*along)
        outer = math.exp(-((abs(x)-separation)/.0055)**2)
        inner = math.exp(-((abs(x)-.0042)/.0025)**2)
        cleft = math.exp(-(x/.0028)**2)
        hood = math.exp(-(x/.0040)**2-((z-.827)/.0070)**2)
        relief = weight*(.0042*outer+.0014*inner-.0034*cleft)+.0016*hood*front*lateral
        dy -= relief
        fold_tone = min(1., weight*(.58*inner+.82*cleft)+.18*hood*front*lateral)
    return (dx, dy, dz), (areola, nipple, fold_tone)


def in_detail_region(point):
    x, y, z = point
    return .748 < z < .860 and abs(x) < .050 and y < -.040


def _outside_face_state(mesh):
    """Cyclic corner identity includes geometry, existing UVs/colors and shading."""
    result = Counter()
    uvs = [mesh.uv_layers[name] for name in sorted(mesh.uv_layers.keys())]
    colors = [mesh.color_attributes[name] for name in sorted(mesh.color_attributes.keys())]
    for polygon in mesh.polygons:
        if any(in_detail_region(mesh.vertices[i].co) for i in polygon.vertices):
            continue
        corners = []
        for index in polygon.loop_indices:
            values = list(mesh.vertices[mesh.loops[index].vertex_index].co)
            for layer in uvs:
                values.extend(layer.data[index].uv)
            for layer in colors:
                values.extend(layer.data[index].color)
            corners.append(tuple(values))
        pivot = min(range(len(corners)), key=corners.__getitem__)
        values = [c for row in corners[pivot:]+corners[:pivot] for c in row]
        payload = struct.pack('<i?', polygon.material_index, polygon.use_smooth)
        payload += struct.pack('<'+str(len(values))+'f', *values)
        result[hashlib.sha256(payload).digest()] += 1
    return result


def apply_detail(body):
    """Bake the existing smooth surface, refine only pelvic sampling, sculpt."""
    import bmesh
    import bpy
    from mathutils import Matrix, Vector
    from check_anatomy_variant import geometry_metrics, accept_geometry

    if body.matrix_world != Matrix.Identity(4):
        raise ValueError('Anatomy detail requires the saved identity object frame.')
    if [(m.type, m.levels, m.render_levels) for m in body.modifiers] != [('SUBSURF', 2, 2)]:
        raise ValueError('Expected the original two-level smooth body surface.')
    bpy.context.view_layer.update()
    evaluated = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = bpy.data.meshes.new_from_object(evaluated, preserve_all_data_layers=True,
                                         depsgraph=bpy.context.evaluated_depsgraph_get())
    mesh.name = 'Haru / continuous detailed adult skin'
    evaluated_before = [tuple(v.co) for v in mesh.vertices]
    outside_before = _outside_face_state(mesh)
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        edges = [e for e in bm.edges if all(in_detail_region(v.co) for v in e.verts)]
        if len(edges) < 30:
            raise ValueError('Pelvic detail region did not cover the intended surface.')
        bmesh.ops.subdivide_edges(bm, edges=edges, cuts=2, use_grid_fill=True)
        bm.verts.index_update()
        bm.to_mesh(mesh)
    finally:
        bm.free()
    mesh.update()
    if Counter(evaluated_before)-Counter(tuple(v.co) for v in mesh.vertices):
        raise ValueError('Local refinement moved the original evaluated surface vertices.')
    if _outside_face_state(mesh) != outside_before:
        raise ValueError('Local refinement changed protected face topology, UVs, colors or shading.')
    before = [tuple(v.co) for v in mesh.vertices]
    faces = [tuple(p.vertices) for p in mesh.polygons]
    masks = []
    for vertex, point in zip(mesh.vertices, before):
        delta, pigment = fields(point)
        vertex.co = Vector(point)+Vector(delta)
        masks.append(pigment)
    mesh.update()
    report = geometry_metrics(before, [tuple(v.co) for v in mesh.vertices], faces)
    accept_geometry(report)
    layer = mesh.color_attributes.new(name='AdultAnatomyDetail', type='FLOAT_COLOR', domain='CORNER')
    for loop in mesh.loops:
        layer.data[loop.index].color = (*masks[loop.vertex_index], 1.)
    material = body.data.materials[0].copy()
    material.name = 'Skin / adult anatomy with localized pigmentation'
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    source = shader.inputs['Base Color'].links[0].from_socket
    attribute = nodes.new('ShaderNodeVertexColor')
    attribute.layer_name = 'AdultAnatomyDetail'
    separate = nodes.new('ShaderNodeSeparateColor')
    separate.mode = 'RGB'
    links.new(attribute.outputs['Color'], separate.inputs['Color'])
    for name, channel, color in [('Areola pigmentation', 'Red', (.72, .43, .40, 1)),
                                  ('Nipple pigmentation', 'Green', (.83, .66, .63, 1)),
                                  ('External fold pigmentation', 'Blue', (.80, .53, .50, 1))]:
        blend = nodes.new('ShaderNodeMixRGB')
        blend.name = name
        blend.blend_type = 'MULTIPLY'
        blend.inputs[2].default_value = color
        links.new(separate.outputs[channel], blend.inputs[0])
        links.new(source, blend.inputs[1])
        source = blend.outputs[0]
    links.new(source, shader.inputs['Base Color'])
    mesh.materials[0] = material
    body.modifiers.clear()
    body.data = mesh
    body['Anatomy variant'] = 'Localized chest volume, nipple and external vulvar relief; adult age 20'
    body['Anatomy source'] = 'scenes/anatomical_detail.py; source input retained separately'
    report.update(original_evaluated_vertices=len(evaluated_before), final_vertices=len(before),
                  local_subdivision_edges=len(edges), original_evaluated_vertices_preserved_before_sculpt=True,
                  protected_surface_faces_exact_before_sculpt=sum(outside_before.values()),
                  pigment_maxima=[max(p[i] for p in masks) for i in range(3)])
    return report, before, faces

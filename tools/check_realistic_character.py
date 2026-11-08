"""Check the currently loaded sailor-character scene without changing or saving it.

Bound: this checks source geometry, world transforms, selected shader connections,
FILE-image packing, camera presence, and the static-model contract. Additional
CHR-001 gates check source neck boundaries and active-depsgraph evaluated body
triangles in separately bounded front-face and ear regions against evaluated
mesh hair or unmodified POLY hair centerlines.
The latter omits curve radius and selects facial triangles by centroid. These
checks do not certify appearance, likeness, cuteness, skin realism, arbitrary
clothing clearance, or reference matching. CHR-001 still requires
native-resolution hero, portrait, profile, and back comparison against references.
The current eye contract checks two existing open corneal shells and their
registered inner tissue materials. Older single-material scenes use their
retained pre-layer checker; this gate does not certify optical realism.
The current smile contract freshly evaluates the saved body against pinned
neutral/proposed inputs, including the complete oral rails, affected surface,
exterior aperture and controls. Neutral truth is separately compared with the
frozen pre-smile saved body; this gate is not a likeness check.

Run with Blender --background <saved.blend> --python-exit-code 1 --python <this.py>.
"""
import json
import math
import hashlib
import struct
import sys
from pathlib import Path
from collections import Counter

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_reference_smile import verify_reference_smile

SMILE_INPUT_SHA256='c6c56c4e5d12884216403d5f604dff8290e864031ef6d9c9c6e36271027ea4df'


BODY_NAME = 'Haru / anatomical adult skin'
CAMERA_VIEWS = ('hero', 'portrait', 'profile', 'back')
CHARACTER_COLLECTIONS = (
    '01 Human anatomy', '02 Eyes and lashes', '03 Strand hair', '04 Sailor clothing',
)
BOUND = (
    'Loaded scene source geometry and transforms; stature uses face-used mesh '
    'vertices in the four character collections, excluding studio; linked skin/alpha materials, '
    'packed used FILE images, four cameras, and no armatures. CHR-001 additionally '
    'checks source neck boundaries and active-depsgraph evaluated body/mesh-hair '
    'triangles or unmodified POLY hair centerlines in named regions; curve radius '
    'is omitted. Does not certify visual realism, likeness, cuteness, arbitrary '
    'clothing clearance, or reference matching.'
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def upstream_nodes(socket):
    """Inspect connected nodes in the current flat material graph only."""
    pending = [link.from_node for link in socket.links]
    found = {}
    while pending:
        node = pending.pop()
        if node.as_pointer() in found:
            continue
        found[node.as_pointer()] = node
        pending.extend(link.from_node for inp in node.inputs for link in inp.links)
    return list(found.values())


def connected_principled(material):
    require(material is not None and material.use_nodes and material.node_tree,
            'An assigned material has no node shader; assign the intended node-based material.')
    outputs = [node for node in material.node_tree.nodes
               if node.type == 'OUTPUT_MATERIAL' and node.is_active_output]
    shaders = [node for output in outputs for node in upstream_nodes(output.inputs['Surface'])
               if node.type == 'BSDF_PRINCIPLED']
    require(len(shaders) == 1,
            f'Material {material.name!r} has {len(shaders)} active Principled shaders; '
            'connect its intended single Principled shader to the active material output.')
    return shaders[0]


def is_packed(image):
    return image.packed_file is not None or len(image.packed_files) > 0


def has_bounded_image_alpha(socket):
    """Accept direct image alpha or one attenuation multiply that preserves zero.

    Bound: one flat image link, optionally multiplied by an unlinked finite
    constant in (0, 1]. Other graphs require their own transparency proof.
    """
    if len(socket.links)!=1:
        return False
    source=socket.links[0].from_socket
    node=source.node
    if node.type=='TEX_IMAGE':
        return source.name=='Alpha' and node.image is not None
    if node.type!='MATH' or node.operation!='MULTIPLY':
        return False
    connected=[inp for inp in node.inputs[:2] if inp.is_linked]
    constants=[inp for inp in node.inputs[:2] if not inp.is_linked]
    if len(connected)!=1 or len(constants)!=1:
        return False
    factor=constants[0].default_value
    if not math.isfinite(factor) or not 0<factor<=1:
        return False
    if len(connected[0].links)!=1:
        return False
    image_output=connected[0].links[0].from_socket
    return image_output.node.type=='TEX_IMAGE' and image_output.name=='Alpha' and image_output.node.image is not None


def check_ocular_layers(eye):
    """Check actual face/UV witnesses independently of the scene assignment helper.

    Witnesses derive from pinned high-poly.obj SHA da2493215b708a344c33dc72f2a9a5b8fa985dcc5a70ad3b208995cf871da8e1.
    Complete source components/materials are covered; evaluated shell clearance
    and optical appearance have separate bounded checks and native review.
    """
    require(eye is not None and eye.type == 'MESH', 'Missing fitted Eyes mesh; restore the anatomical eye asset.')
    data = eye.data
    faces = [list(p.vertices) for p in data.polygons]
    require(len(data.vertices) == 1064 and len(faces) == 1020,
            'Eyes must retain all 1064 source vertices and 1020 quads; restore its pinned topology.')
    topology = hashlib.sha256(json.dumps(faces, separators=(',', ':')).encode()).hexdigest()
    require(topology == 'c50ec6c7f5dae37549b67d41054f115f0f8c08ac592e14616919885b3ab2720e',
            'Eyes face identities differ from the pinned complete asset; inspect the source topology.')
    uv = data.uv_layers.get('UVMap')
    require(uv is not None, 'Eyes UVMap is missing; restore the original eye texture coordinates.')
    uv_digest = hashlib.sha256(b''.join(struct.pack('<2f', *item.uv) for item in uv.data)).hexdigest()
    require(uv_digest == '8e13e7dd7fdfdc909f3ce78e852e05adae7daf8a054d360eb9db3056d29770fe',
            'Eyes corner UVs differ from the pinned float32 witness; restore their original identities.')
    # Union-find over every actual edge is independent of the builder's flood fill.
    parents = list(range(len(data.vertices)))
    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index
    for edge in data.edges:
        a, b = map(find, edge.vertices)
        parents[b] = a
    groups = {}
    for vertex in data.vertices:
        groups.setdefault(find(vertex.index), {'vertices': [], 'faces': []})['vertices'].append(vertex.index)
    for polygon in data.polygons:
        groups[find(polygon.vertices[0])]['faces'].append(polygon)
    census, shell_faces, tissue_faces = [], [], []
    for group in groups.values():
        polygons = group['faces']
        edges = Counter(tuple(sorted(edge)) for p in polygons for edge in p.edge_keys)
        row = (len(group['vertices']), len(polygons), sum(n == 1 for n in edges.values()))
        require(all(n in (1, 2) for n in edges.values()), 'Eyes have a nonmanifold component edge; restore the asset.')
        census.append(row)
        target = shell_faces if row == (256, 245, 20) else tissue_faces
        if target is shell_faces:
            require(all(.8794 <= uv.data[i].uv.x <= .9912 and .0109 <= uv.data[i].uv.y <= .1226
                        for p in polygons for i in p.loop_indices),
                    'Corneal component UV patch is unexpected; do not assign material by name alone.')
        target.extend(polygons)
    require(sorted(census) == sorted([(256, 245, 20), (276, 265, 20)]*2),
            f'Eyes component census {census} is incomplete; restore both open shell/tissue pairs.')
    require(len(data.materials) == 2 and len(shell_faces) == 490 and len(tissue_faces) == 530,
            'Eyes require two actual layers: 490 corneal faces and 530 tissue faces in distinct material slots.')
    shell_slots = {p.material_index for p in shell_faces}
    tissue_slots = {p.material_index for p in tissue_faces}
    require(len(shell_slots) == len(tissue_slots) == 1 and shell_slots != tissue_slots,
            'Eye material assignments cross the validated shell/tissue components; restore the full face populations.')
    outer = data.materials[next(iter(shell_slots))]
    inner = data.materials[next(iter(tissue_slots))]
    shell = connected_principled(outer)
    tissue = connected_principled(inner)
    def constant(node, key, expected):
        socket = node.inputs[key]
        actual = socket.default_value
        values = zip(actual, expected) if isinstance(expected, tuple) else [(actual, expected)]
        require(not socket.is_linked and all(abs(a-b) < 1e-6 for a, b in values),
                f'Eye {node.id_data.name}/{key} must be unlinked {expected}; restore the declared optical layer.')
    require({node.type for node in outer.node_tree.nodes} == {'BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'}
            and len(outer.node_tree.nodes) == 2 and len(outer.node_tree.links) == 1,
            'Corneal material must be the untextured single Principled interface; remove undeclared optical nodes.')
    for key, expected in [('Base Color', (1, 1, 1, 1)), ('Alpha', 1), ('Transmission Weight', 1),
                          ('IOR', 1.336), ('Roughness', .02), ('Specular IOR Level', .5), ('Coat Weight', 0)]:
        constant(shell, key, expected)
    constant(tissue, 'Specular IOR Level', 0)
    constant(tissue, 'Coat Weight', 0)
    alpha = tissue.inputs['Alpha']
    require(len(alpha.links) == 1 and alpha.links[0].from_node.type == 'TEX_IMAGE'
            and alpha.links[0].from_socket.name == 'Alpha',
            'Inner eye tissue must retain its direct original texture Alpha link.')
    image = alpha.links[0].from_node.image
    require(image is not None and image.packed_file is not None and
            hashlib.sha256(bytes(image.packed_file.data)).hexdigest() ==
            '4659691c7295ad6206c78b003e5fd0e5f91dcd53032fa914a229bb48cabe424b',
            'Inner eye tissue packed texture differs from the pinned brown-eye source.')
    nodes = inner.node_tree.nodes
    require(nodes.get('UV Map') is not None and nodes['UV Map'].uv_map == 'UVMap',
            'Inner eye registration must use its original UVMap.')
    for name, center in [('Vector Math', (.289061368554985, .2901778246762782, 0)),
                         ('Vector Math.001', (.7050885844462438, .7022999938386068, 0))]:
        require(nodes.get(name) is not None and nodes[name].type == 'VECT_MATH' and nodes[name].operation == 'DISTANCE',
                'Inner eye registered iris distance nodes are missing; restore the measured texture mask.')
        constant(nodes[name], 1, center)
    require(nodes.get('Math') is not None and nodes['Math'].operation == 'MINIMUM'
            and nodes.get('Map Range') is not None and nodes['Map Range'].interpolation_type == 'SMOOTHSTEP',
            'Inner eye limbal transition differs from the registered smooth mask.')
    for key, expected in [('From Min', 112/1024), ('From Max', 128/1024), ('To Min', 1), ('To Max', 0)]:
        constant(nodes['Map Range'], key, expected)
    brown = nodes.get('Natural brown iris, subdued red rim')
    require(brown is not None and brown.type == 'HUE_SAT', 'Inner eye brown correction node is missing.')
    constant(brown, 'Saturation', .62)
    constant(brown, 'Value', .72)
    links = {(l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier)
             for l in inner.node_tree.links}
    expected_links = {
        ('UV Map', 'UV', 'Image Texture', 'Vector'),
        ('UV Map', 'UV', 'Vector Math', 'Vector'), ('UV Map', 'UV', 'Vector Math.001', 'Vector'),
        ('Vector Math', 'Value', 'Math', 'Value'), ('Vector Math.001', 'Value', 'Math', 'Value_001'),
        ('Math', 'Value', 'Map Range', 'Value'),
        ('Image Texture', 'Color', brown.name, 'Color'), ('Map Range', 'Result', 'Mix (Legacy)', 'Fac'),
        ('Image Texture', 'Color', 'Mix (Legacy)', 'Color1'), (brown.name, 'Color', 'Mix (Legacy)', 'Color2'),
        ('Mix (Legacy)', 'Color', tissue.name, 'Base Color')}
    require(expected_links <= links, 'Inner eye color registration links changed; restore the complete original color path.')
    return {'source_component_census': sorted(census), 'corneal_faces': len(shell_faces),
            'inner_faces': len(tissue_faces), 'topology_witness_sha256': topology,
            'uv_witness_sha256': uv_digest,
            'bound': 'Complete source component/material/UV identity; open single-interface approximation, no optical or thickness certification.'}


def finite_coordinates(scene):
    checked = 0
    for obj in scene.objects:
        require(all(math.isfinite(value) for row in obj.matrix_world for value in row),
                f'Object {obj.name!r} has a nonfinite transform; rebuild its position, rotation, or scale.')
        if obj.type == 'MESH':
            coordinates = (vertex.co for vertex in obj.data.vertices)
        elif obj.type in {'CURVE', 'SURFACE'}:
            coordinates = (
                coordinate for spline in obj.data.splines
                for coordinate in (
                    [value for point in spline.bezier_points
                     for value in (point.co, point.handle_left, point.handle_right)]
                    if spline.type == 'BEZIER' else [point.co for point in spline.points]))
        elif obj.type == 'CURVES':
            coordinates = (point.position for point in obj.data.points)
        else:
            continue
        for index, coordinate in enumerate(coordinates):
            require(all(math.isfinite(value) for value in coordinate),
                    f'Object {obj.name!r} source coordinate {index} is nonfinite; '
                    'fix its geometry before saving the scene.')
            require(all(math.isfinite(value) for value in obj.matrix_world @ Vector(coordinate[:3])),
                    f'Object {obj.name!r} coordinate {index} becomes nonfinite in world space; '
                    'fix its coordinate or transform.')
            checked += 1
    return checked


def segment_enters_region(start, end, bounds):
    """Clip a segment against the supplied axis slabs, including crossing edges."""
    lower, upper = 0.0, 1.0
    for axis, minimum, maximum in bounds:
        delta = end[axis] - start[axis]
        if abs(delta) < 1e-15:
            if start[axis] < minimum or start[axis] > maximum:
                return False
            continue
        first, last = (minimum - start[axis]) / delta, (maximum - start[axis]) / delta
        lower, upper = max(lower, min(first, last)), min(upper, max(first, last))
        if lower > upper:
            return False
    return True


def check_neck_boundaries(scene, body, meters_per_unit, region_kind='neck'):
    """CHR-001: source skin cuts must lie outside the selected visible band.

    Neck: x +/- .09, z 1.335..1.43 m. Cuffs: x +/- .18, z .415..46 m.
    This source-edge test does not certify cloth fit or other body regions.
    """
    incidence = Counter()
    for polygon in body.data.polygons:
        vertices = tuple(polygon.vertices)
        for first, second in zip(vertices, vertices[1:] + vertices[:1]):
            incidence[tuple(sorted((first, second)))] += 1
    boundary = [edge for edge, count in incidence.items() if count == 1]
    require(region_kind in ('neck','sock cuffs'),f'Unknown skin-boundary region {region_kind!r}.')
    bounds = ((0, -.09, .09), (2, 1.335, 1.43)) if region_kind=='neck' else ((0,-.18,.18),(2,.415,.46))
    violations = []
    for edge in boundary:
        start, end = (body.matrix_world @ body.data.vertices[index].co * meters_per_unit
                      for index in edge)
        if segment_enters_region(start, end, bounds):
            violations.append(edge)
    require(not violations,
            f'CHR-001 skin: {len(violations)} source boundary edges enter the protected {region_kind} band '
            f'{bounds}; examples {violations[:5]}. '
            'Restore continuous visible skin and place the covered cut below the protected band.')
    return {'protected_boundary_edges': 0, 'total_source_boundary_edges': len(boundary),
            'bound': f'Source face edges; any segment entering {bounds}; all y.'}


def evaluated_triangles(obj, depsgraph, meters_per_unit):
    """Copy evaluated mesh triangles in world meters; release temporary mesh data."""
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        mesh.calc_loop_triangles()
        vertices = [evaluated.matrix_world @ vertex.co * meters_per_unit for vertex in mesh.vertices]
        require(all(math.isfinite(value) for vertex in vertices for value in vertex),
                f'Object {obj.name!r} evaluates to nonfinite geometry; fix its mesh or modifiers.')
        triangles = [tuple(triangle.vertices) for triangle in mesh.loop_triangles]
        return vertices, triangles
    finally:
        evaluated.to_mesh_clear()


def check_hair_face_clearance(scene, body, meters_per_unit, region_kind='front face'):
    """CHR-001: actual hair geometry must not cross the named body-surface region.

    Meshes use active-depsgraph evaluated triangles and BVH triangle overlap.
    Curves use transformed POLY centerline segments, omitting bevel/radius; curve
    modifiers and non-POLY splines are rejected rather than silently unchecked.
    All hair-collection objects are checked regardless of render visibility or
    material alpha. Body triangles are selected by centroid in the stated region.
    """
    require(region_kind in ('front face','ears'),f'Unknown hair-clearance region {region_kind!r}; use front face or ears.')
    bound=('Body triangle centroids: |x| < .07, y < -.070, z 1.445..1.54 m' if region_kind=='front face'
           else 'Body triangle centroids: |x| >= .060, y < .050, z 1.48..1.59 m')
    collection = scene.collection.children.get('03 Strand hair')
    require(collection is not None,
            'CHR-001 hair: missing 03 Strand hair collection; restore the actual hair geometry for checking.')
    objects = list(collection.all_objects)
    require(objects,
            'CHR-001 hair: the hair collection is empty; restore the intended hair before checking clearance.')
    depsgraph = bpy.context.evaluated_depsgraph_get()
    body_vertices, body_triangles = evaluated_triangles(body, depsgraph, meters_per_unit)
    protected = []
    for triangle in body_triangles:
        center = sum((body_vertices[index] for index in triangle), Vector()) / 3
        selected=(1.445 <= center.z <= 1.54 and center.y < -.070 and abs(center.x) < .07
                  if region_kind=='front face' else
                  1.48 <= center.z <= 1.59 and center.y < .050 and abs(center.x) >= .060)
        if selected:
            protected.append(triangle)
    require(protected,
            f'CHR-001 hair: no anatomical triangles enter the protected {region_kind} region; '
            'restore the expected face geometry and physical scale instead of skipping clearance.')
    face_tree = BVHTree.FromPolygons(body_vertices, protected, all_triangles=True)
    protected_ids = {index for triangle in protected for index in triangle}
    region = tuple((axis, min(body_vertices[index][axis] for index in protected_ids),
                    max(body_vertices[index][axis] for index in protected_ids)) for axis in range(3))
    collisions = []
    checked_mesh_triangles = checked_segments = candidate_segments = 0
    for obj in objects:
        if obj.type == 'MESH':
            vertices, triangles = evaluated_triangles(obj, depsgraph, meters_per_unit)
            checked_mesh_triangles += len(triangles)
            if triangles:
                hair_tree = BVHTree.FromPolygons(vertices, triangles, all_triangles=True)
                overlaps = hair_tree.overlap(face_tree)
                if overlaps:
                    collisions.append({'object': obj.name, 'kind': 'mesh', 'count': len(overlaps),
                                       'examples': [list(pair) for pair in overlaps[:5]]})
        elif obj.type == 'CURVE':
            require(not obj.modifiers and not obj.data.shape_keys,
                    f'CHR-001 hair: curve {obj.name!r} has modifiers or shape keys; '
                    'extend the clearance check to their evaluated centerlines before relying on it.')
            hit_examples = []
            hit_count = 0
            for spline_index, spline in enumerate(obj.data.splines):
                require(spline.type == 'POLY',
                        f'CHR-001 hair: {obj.name!r} spline {spline_index} is {spline.type}; '
                        'use POLY strands or add a bounded evaluated-spline check.')
                points = [obj.matrix_world @ Vector(point.co[:3]) * meters_per_unit for point in spline.points]
                pairs = list(zip(points, points[1:]))
                if spline.use_cyclic_u and len(points) > 1:
                    pairs.append((points[-1], points[0]))
                for segment_index, (start, end) in enumerate(pairs):
                    checked_segments += 1
                    if not segment_enters_region(start, end, region):
                        continue
                    candidate_segments += 1
                    direction = end - start
                    length = direction.length
                    if length < 1e-12:
                        continue
                    hit, normal, triangle_index, distance = face_tree.ray_cast(start, direction / length, length)
                    if hit is not None:
                        hit_count += 1
                        if len(hit_examples) < 5:
                            hit_examples.append([spline_index, segment_index, triangle_index])
            if hit_count:
                collisions.append({'object': obj.name, 'kind': 'poly_centerline',
                                   'count': hit_count, 'examples': hit_examples})
        else:
            require(False,
                    f'CHR-001 hair: unsupported object {obj.name!r} of type {obj.type}; '
                    'extend the geometry check for this representation before accepting clearance.')
    require(checked_mesh_triangles + checked_segments > 0,
            'CHR-001 hair: no triangles or strand segments were tested; restore actual hair geometry.')
    require(not collisions,
            f'CHR-001 hair: geometry intersects the protected {region_kind} surface: '
            f'{json.dumps(collisions, separators=(",", ":"))}. '
            'Refit or remove crossing geometry; shader alpha does not resolve this regression.')
    return {'region':region_kind,'intersections': 0, 'protected_body_triangles': len(protected),
            'checked_hair_mesh_triangles': checked_mesh_triangles,
            'checked_poly_segments': checked_segments, 'candidate_poly_segments': candidate_segments,
            'bound': bound+'; '
                     'active-depsgraph mesh triangles and unmodified POLY centerlines; curve radius omitted.'}


def check_geometry_regressions(scene, body, meters_per_unit):
    """Run both independent CHR-001 controls, preserving failures from each."""
    results, errors = {}, []
    for name, check in (('neck', check_neck_boundaries), ('hair_face', check_hair_face_clearance)):
        try:
            results[name] = check(scene, body, meters_per_unit)
        except AssertionError as error:
            errors.append(str(error))
    try:
        results['hair_ears']=check_hair_face_clearance(scene,body,meters_per_unit,'ears')
    except AssertionError as error:
        errors.append('Ear clearance: '+str(error))
    try:
        results['sock_cuffs']=check_neck_boundaries(scene,body,meters_per_unit,'sock cuffs')
    except AssertionError as error:
        errors.append('Sock cuffs: '+str(error))
    require(not errors, '\n'.join(errors))
    return results


def validate_scene():
    """Return a compact technical receipt, or raise an actionable AssertionError."""
    scene = bpy.context.scene
    body = scene.objects.get(BODY_NAME)
    require(body is not None and body.type == 'MESH',
            f'Missing anatomical mesh {BODY_NAME!r}; load the rebuilt 3D character scene.')
    mesh = body.data
    require(len(mesh.vertices) > 10000,
            f'Anatomical mesh has {len(mesh.vertices)} source vertices; '
            'restore the substantial anatomical base with more than 10000 source vertices.')
    used = sorted({index for polygon in mesh.polygons for index in polygon.vertices})
    require(len(used) > 1000,
            f'Only {len(used)} anatomical vertices belong to faces; restore the actual body surface.')
    for name in ('UVMap', 'ReferenceFaceProjection'):
        layer = mesh.uv_layers.get(name)
        require(layer is not None and len(layer.data) == len(mesh.loops) and len(layer.data) > 0,
                f'Anatomical mesh lacks complete {name!r} UV coordinates; rebuild its UV mapping.')
        require(all(math.isfinite(value) for item in layer.data for value in item.uv),
                f'UV layer {name!r} contains nonfinite values; rebuild its coordinates.')

    checked_coordinates = finite_coordinates(scene)
    meters_per_unit = scene.unit_settings.scale_length
    require(math.isfinite(meters_per_unit) and meters_per_unit > 0,
            'Scene unit scale is not positive and finite; set a valid meter scale.')
    points = [body.matrix_world @ mesh.vertices[index].co * meters_per_unit for index in used]
    minimum = [min(point[axis] for point in points) for axis in range(3)]
    maximum = [max(point[axis] for point in points) for axis in range(3)]
    extents = [maximum[axis] - minimum[axis] for axis in range(3)]
    center = sum(points, Vector()) / len(points)
    centered = [point - center for point in points]
    covariance = Matrix([[sum(p[a] * p[b] for p in centered) / len(centered)
                          for b in range(3)] for a in range(3)])
    diagonal_product = math.prod(covariance[a][a] for a in range(3))
    volume_ratio = covariance.determinant() / diagonal_product if diagonal_product > 0 else 0
    require(extents[0] > .20 and extents[1] > .10 and volume_ratio > .001,
            'The face-used body surface is too flat or thin to be the anatomical 3D base; '
            'restore volumetric body geometry instead of a projected image plane.')

    # Covered skin faces are intentionally absent. Measure stature from the
    # clothed character's face-used meshes, never loose anatomical helper verts
    # or the studio floor, while retaining the separate body surface checks.
    collections = [scene.collection.children.get(name) for name in CHARACTER_COLLECTIONS]
    missing = [name for name, collection in zip(CHARACTER_COLLECTIONS, collections) if collection is None]
    require(not missing,
            f'Missing character collections {missing}; restore the four named character collections '
            'so stature excludes studio geometry.')
    character_meshes = {obj.as_pointer(): obj for collection in collections
                        for obj in collection.all_objects if obj.type == 'MESH'}
    character_z = []
    for obj in character_meshes.values():
        face_used = {index for polygon in obj.data.polygons for index in polygon.vertices}
        character_z.extend((obj.matrix_world @ obj.data.vertices[index].co).z * meters_per_unit
                           for index in face_used)
    require(character_z,
            'The character collections contain no mesh faces; restore the clothed character geometry.')
    character_height = max(character_z) - min(character_z)
    require(1.60 <= character_height <= 1.70,
            f'Face-used clothed character height is {character_height:.4f} m; '
            'restore its intended 1.60–1.70 m physical stature, measured from feet through hair.')

    for view in CAMERA_VIEWS:
        camera = scene.objects.get('Camera_' + view)
        require(camera is not None and camera.type == 'CAMERA',
                f'Missing Camera_{view}; restore that camera before four-view inspection.')
    armatures = [obj.name for obj in scene.objects if obj.type == 'ARMATURE'
                 or any(modifier.type == 'ARMATURE' for modifier in obj.modifiers)]
    require(not armatures,
            f'The static scene contains armatures or armature modifiers on {armatures}; '
            'remove the unintended rig or explicitly revise the static-model contract.')

    skin_slots = [slot.material for slot in body.material_slots
                  if slot.material is not None and slot.material.name.startswith('Skin /')]
    require(len(skin_slots) == 1,
            'Anatomical mesh must use its single Skin / material; restore the photographed skin assignment.')
    skin = skin_slots[0]
    require(all(body.material_slots[polygon.material_index].material == skin for polygon in mesh.polygons),
            'Some anatomical faces do not use the skin material; restore their intended material indices.')
    shader = connected_principled(skin)
    scale_socket = shader.inputs.get('Subsurface Scale')
    require(scale_socket is not None and not scale_socket.is_linked,
            'Skin Subsurface Scale must be an explicit constant for this check; restore its meter-scale value.')
    subsurface_scale = scale_socket.default_value * meters_per_unit
    require(math.isfinite(subsurface_scale) and 0 < subsurface_scale < .01,
            f'Skin Subsurface Scale is {subsurface_scale:.6f} m; set it above zero and below 0.01 m.')
    color_nodes = upstream_nodes(shader.inputs['Base Color'])
    skin_images = []
    for node in color_nodes:
        if node.type != 'TEX_IMAGE' or node.image is None:
            continue
        image = node.image
        vector_input = node.inputs['Vector']
        uses_uv = (not vector_input.is_linked and any(
            layer.name == 'UVMap' and layer.active_render for layer in mesh.uv_layers)) or any(
                upstream.type == 'UVMAP' and upstream.uv_map == 'UVMap'
                for upstream in upstream_nodes(vector_input))
        if uses_uv and image.source == 'FILE' and image.size[0] >= 2048 and is_packed(image):
            skin_images.append(image)
    require(skin_images,
            'Skin Base Color lacks a connected packed UVMap image at least 2048 pixels wide; '
            'restore the photographic UV albedo texture and its color connection.')

    ocular_layers = check_ocular_layers(scene.objects.get('Eyes'))
    for object_name in ('Eyelashes', 'Eyebrows'):
        obj = scene.objects.get(object_name)
        require(obj is not None and len(obj.material_slots) > 0,
                f'Missing textured {object_name}; restore its fitted geometry and material.')
        for slot in obj.material_slots:
            surface = connected_principled(slot.material)
            require(has_bounded_image_alpha(surface.inputs['Alpha']),
                    f'Material {slot.material.name!r} lacks bounded image Alpha wired to Principled Alpha; '
                    'connect image Alpha directly, or through one multiply by a constant in (0, 1], to preserve transparent image borders.')

    used_file_images = [image for image in bpy.data.images if image.source == 'FILE' and image.users > 0]
    unpacked = [image.name for image in used_file_images if not is_packed(image)]
    require(not unpacked,
            f'Used image files are not packed: {unpacked}; pack those textures into the saved .blend.')
    geometry_regressions = check_geometry_regressions(scene, body, meters_per_unit)
    smile_gate = verify_reference_smile(body, {
        'portrait': scene.objects['Camera_portrait'].matrix_world.translation,
        'face_oblique': Vector((-.62,-1.05,1.55)),
    }, expected_contract_sha256=SMILE_INPUT_SHA256)
    return {
        'status': 'pass',
        'bound': BOUND,
        'source_vertices': len(mesh.vertices),
        'face_used_vertices': len(used),
        'body_surface_extent_m': {axis: round(value, 6) for axis, value in zip('xyz', extents)},
        'character_height_m': round(character_height, 6),
        'stature_meshes': len(character_meshes),
        'stature_face_used_vertices': len(character_z),
        'nonplanarity_ratio': round(volume_ratio, 6),
        'subsurface_scale_m': round(subsurface_scale, 6),
        'skin_uv_images': [{'name': image.name, 'width': image.size[0]} for image in skin_images],
        'packed_used_file_images': len(used_file_images),
        'checked_source_coordinates': checked_coordinates,
        'cameras': list(CAMERA_VIEWS),
        'geometry_regressions': geometry_regressions,
        'ocular_layers': ocular_layers,
        'reference_smile': smile_gate,
        'visual_acceptance': 'Not certified; CHR-001 requires four-view reference comparison.',
    }


if __name__ == '__main__':
    print(json.dumps(validate_scene(), separators=(',', ':')), flush=True)

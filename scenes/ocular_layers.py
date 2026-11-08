"""Separate the existing corneal shells from their concave iris/scleral tissue.

Harness: tools/build_sailor_character.py; the frozen ocular_layers diagnostic
validated this assignment in portrait and opposite-side oblique renders.
The asset has open shells, so this is one effective dielectric interface,
not a model of corneal thickness. It changes materials only.
"""
from collections import Counter
import hashlib
from pathlib import Path

from prepare_human_base import read_obj


ASSET_SHA256 = 'da2493215b708a344c33dc72f2a9a5b8fa985dcc5a70ad3b208995cf871da8e1'
TEXTURE_SHA256 = '4659691c7295ad6206c78b003e5fd0e5f91dcd53032fa914a229bb48cabe424b'
CORNEA_NAME = 'Eyes / existing corneal dielectric'


def validated_shell_faces(asset):
    """Identify both shells by complete connected topology and their UV patch."""
    faces = asset['faces']
    assert len(asset['vertices']) == 1064 and len(faces) == 1020, (
        'Eye asset population changed; use the pinned 1064-vertex, 1020-face asset.')
    adjacency = [set() for _ in asset['vertices']]
    for face in faces:
        assert len(face) == 4, 'Eye asset must retain its original quad topology.'
        for a, b in zip(face, face[1:]+face[:1]):
            adjacency[a].add(b)
            adjacency[b].add(a)
    remaining = set(range(len(adjacency)))
    census, shells = [], set()
    while remaining:
        first = min(remaining)
        remaining.remove(first)
        vertices, queue = {first}, [first]
        while queue:
            fresh = adjacency[queue.pop()] & remaining
            remaining.difference_update(fresh)
            vertices.update(fresh)
            queue.extend(fresh)
        indices = [i for i, face in enumerate(faces) if face[0] in vertices]
        assert all(set(faces[i]) <= vertices for i in indices), (
            'Eye component crosses its connected population; inspect asset topology.')
        edges = Counter(tuple(sorted((a, b))) for i in indices
                        for a, b in zip(faces[i], faces[i][1:]+faces[i][:1]))
        assert all(count in (1, 2) for count in edges.values()), (
            'Eye component has a nonmanifold edge; restore the pinned asset.')
        census.append((len(vertices), len(indices), sum(n == 1 for n in edges.values())))
        if len(vertices) == 256:
            assert all(.8794 <= asset['uvs'][j][0] <= .9912
                       and .0109 <= asset['uvs'][j][1] <= .1226
                       for i in indices for j in asset['face_uvs'][i]), (
                'Corneal component UV patch changed; do not classify tissue by index ranges.')
            shells.update(indices)
    assert census == [(256, 245, 20), (276, 265, 20)]*2 and len(shells) == 490, (
        f'Eye component census {census} differs from the two open shell/tissue pairs.')
    return shells


def assign_ocular_layers(eye, asset_path):
    """Keep the registered tissue graph; add the measured shell dielectric."""
    import bpy
    from mathutils import Vector

    asset_path = Path(asset_path)
    assert hashlib.sha256(asset_path.read_bytes()).hexdigest() == ASSET_SHA256, (
        f'Eye asset {asset_path} differs from its pinned source; verify before fitting.')
    asset = read_obj(asset_path)
    outer_faces = validated_shell_faces(asset)
    assert len(eye.data.vertices) == len(asset['vertices']), 'Fitted eye vertex identities changed.'
    assert [tuple(p.vertices) for p in eye.data.polygons] == asset['faces'], (
        'Fitted eye topology differs from the validated asset; material assignment stopped.')
    uv = eye.data.uv_layers['UVMap']
    for polygon, refs in zip(eye.data.polygons, asset['face_uvs']):
        for loop, ref in zip(polygon.loop_indices, refs):
            assert (uv.data[loop].uv-Vector(asset['uvs'][ref])).length < 1e-6, (
                'Fitted eye UVs differ from the validated asset; restore source UV identities.')
    assert len(eye.data.materials) == 1 and all(p.material_index == 0 for p in eye.data.polygons), (
        'Ocular layers require the original single tissue slot before assignment.')
    inner = eye.data.materials[0]
    shader = inner.node_tree.nodes['Principled BSDF']
    alpha = shader.inputs['Alpha']
    assert len(alpha.links) == 1 and alpha.links[0].from_socket.name == 'Alpha', (
        'The original eye image Alpha link changed; preserve the tissue color/alpha graph.')
    image = alpha.links[0].from_node.image
    assert image.packed_file and hashlib.sha256(bytes(image.packed_file.data)).hexdigest() == TEXTURE_SHA256, (
        'The packed brown-eye texture differs from the validated UV-alpha source.')
    for key, expected in [('Specular IOR Level', .5), ('Coat Weight', 0)]:
        assert not shader.inputs[key].is_linked and abs(shader.inputs[key].default_value-expected) < 1e-6, (
            f'Inner eye {key} changed before layer assignment; inspect the material input.')
        shader.inputs[key].default_value = 0
    outer = bpy.data.materials.new(CORNEA_NAME)
    outer.use_nodes = True
    shell_shader = outer.node_tree.nodes['Principled BSDF']
    for key, value in [('Base Color', (1, 1, 1, 1)), ('Alpha', 1),
                       ('Transmission Weight', 1), ('IOR', 1.336), ('Roughness', .02),
                       ('Specular IOR Level', .5), ('Coat Weight', 0)]:
        shell_shader.inputs[key].default_value = value
    eye.data.materials.append(outer)
    for i, polygon in enumerate(eye.data.polygons):
        polygon.material_index = int(i in outer_faces)
    return {'outer_faces': 490, 'inner_faces': 530,
            'bound': 'Existing open shells; one effective dielectric interface, no thickness claim.'}

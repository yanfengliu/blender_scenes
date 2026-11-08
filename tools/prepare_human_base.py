"""Read the local CC0 MakeHuman assets without Blender or MakeHuman imports.

The base retains original vertex indices so macro targets and MHCLO fittings
remain valid. Only faces in the ``body`` group are returned for the skin mesh;
the base's clothing, eyeball, joint and other helpers must not be rendered.
Assets and their SHA-256/source/license manifest live in ignored .tools/.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / '.tools' / 'human_reference_assets'
DEFAULT_TARGETS = (
    ('asian-female-young.target', 1.0),
    ('universal-female-young-averagemuscle-averageweight.target', 1.0),
)


def read_obj(path):
    """Return OBJ vertices, UVs, faces, UV face indices, and face group names."""
    vertices, uvs, faces, face_uvs, face_groups = [], [], [], [], []
    group = 'default'
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if not parts or parts[0].startswith('#'):
            continue
        if parts[0] == 'v':
            vertices.append([float(x) for x in parts[1:4]])
        elif parts[0] == 'vt':
            uvs.append(tuple(float(x) for x in parts[1:3]))
        elif parts[0] == 'g':
            group = parts[1]
        elif parts[0] == 'f':
            refs = [part.split('/') for part in parts[1:]]
            faces.append(tuple(int(ref[0]) - 1 for ref in refs))
            face_uvs.append(tuple(int(ref[1]) - 1 if len(ref) > 1 and ref[1] else -1 for ref in refs))
            face_groups.append(group)
    return dict(vertices=vertices, uvs=uvs, faces=faces, face_uvs=face_uvs, face_groups=face_groups)


def apply_target(vertices, path, weight=1.0):
    """Add sparse native-coordinate deltas; target indices are zero based."""
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if not parts or parts[0].startswith('#'):
            continue
        index = int(parts[0])
        if index < 0 or index >= len(vertices):
            raise ValueError(f'Target {path} refers to missing vertex {index}.')
        for axis in range(3):
            vertices[index][axis] += weight * float(parts[axis + 1])


def load_body(targets=DEFAULT_TARGETS, assets=ASSETS):
    """Return shaped native vertices and body-only faces, retaining helper groups.

    Native coordinates use decimeters, X left-right, Y up, Z forward. The young
    MakeHuman macro is its adult 25-year anchor, suitable as an adult anatomical
    starting point; it does not claim an exact inferred age or identity.
    """
    assets = Path(assets)
    data = read_obj(assets / 'base.obj')
    for name, weight in targets:
        apply_target(data['vertices'], assets / name, weight)
    groups = {}
    for face, name in zip(data['faces'], data['face_groups']):
        groups.setdefault(name, set()).update(face)
    data['groups'] = {name: sorted(indices) for name, indices in groups.items()}
    selected = [i for i, name in enumerate(data['face_groups']) if name == 'body']
    for key in ('faces', 'face_uvs', 'face_groups'):
        data[key] = [data[key][i] for i in selected]
    body_indices = data['groups']['body']
    data['ground_y'] = min(data['vertices'][i][1] for i in body_indices)
    return data


def fit_proxy(mhclo_path, human_vertices):
    """Load a mesh asset and fit its barycentric MHCLO anchors to shaped human.

    Supports explicit x/y/z_scale and the 1-index/9-field vertex forms used by
    the selected eyes, eyelashes, eyebrows, teeth and hair. Rejects shear
    mappings rather than producing a silently incorrect fit.
    """
    path = Path(mhclo_path)
    scales = [1.0, 1.0, 1.0]
    mappings, reading_vertices, obj_name = [], False, None
    for line in path.read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if not parts or parts[0].startswith('#'):
            continue
        token = parts[0]
        if token == 'obj_file':
            obj_name = parts[1]
        elif token in ('x_scale', 'y_scale', 'z_scale'):
            axis = 'xyz'.index(token[0])
            first, second = int(parts[1]), int(parts[2])
            scales[axis] = abs(human_vertices[first][axis] - human_vertices[second][axis]) / float(parts[3])
        elif 'shear' in token:
            raise ValueError(f'Unsupported shear fitting in {path}: {token}.')
        elif token == 'verts':
            reading_vertices = True
        elif token == 'material':
            # System hair places this header between ``verts`` and its rows.
            continue
        elif reading_vertices and token.lstrip('-').isdigit():
            if len(parts) == 1:
                mappings.append(list(human_vertices[int(token)]))
            elif len(parts) == 9:
                indices = [int(x) for x in parts[:3]]
                weights = [float(x) for x in parts[3:6]]
                offsets = [float(x) for x in parts[6:9]]
                mappings.append([
                    sum(human_vertices[indices[j]][axis] * weights[j] for j in range(3))
                    + offsets[axis] * scales[axis] for axis in range(3)
                ])
            else:
                raise ValueError(f'Unexpected vertex fitting row in {path}: {line}.')
        elif reading_vertices:
            reading_vertices = False
    if obj_name is None:
        raise ValueError(f'No obj_file declared in {path}.')
    data = read_obj(path.parent / obj_name)
    if len(mappings) != len(data['vertices']):
        raise ValueError(f'{path} fits {len(mappings)} vertices, but its OBJ contains {len(data["vertices"])}.')
    data['vertices'] = mappings
    return data


def to_blender(vertices, ground_y, scale=0.1):
    """Map native Y-up decimeters to Blender meters, facing Blender -Y."""
    return [(x * scale, -z * scale, (y - ground_y) * scale) for x, y, z in vertices]


def group_center(body, group_name):
    ids = body['groups'][group_name]
    return tuple(sum(body['vertices'][i][axis] for i in ids) / len(ids) for axis in range(3))


if __name__ == '__main__':
    import json
    body = load_body()
    eyes = fit_proxy(ASSETS / 'high-poly.mhclo', body['vertices'])
    points = [body['vertices'][i] for i in body['groups']['body']]
    print(json.dumps({
        'vertices_including_helpers': len(body['vertices']),
        'body_vertices': len(body['groups']['body']), 'body_faces': len(body['faces']),
        'uvs': len(body['uvs']), 'eye_vertices': len(eyes['vertices']),
        'native_body_bounds': [[min(p[a] for p in points), max(p[a] for p in points)] for a in range(3)],
        'ground_y': body['ground_y'],
        'landmarks': {name: group_center(body, name) for name in (
            'joint-head', 'joint-neck', 'joint-l-eye', 'joint-r-eye',
            'joint-l-shoulder', 'joint-r-shoulder', 'joint-l-elbow', 'joint-r-elbow',
            'joint-l-hand', 'joint-r-hand', 'joint-jaw')},
    }, indent=2))

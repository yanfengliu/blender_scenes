"""Connected cotton-blouse candidate extracted from the local CC0 human helper.

Harness: tools/build_sailor_character.py owns Blender and visual verification.
This candidate replaces the disconnected torso rings and dome sleeves. It uses
the already shaped MakeHuman helper-tights topology, including its underarms.
The caller owns the collar, pocket, skin coverage, pose, lights, and rendering.

Topology assertions cover this cropped garment before subdivision/solidify, at
the current approximately 1.65 m reference-body scale. They prove one component
and four clean openings, not cloth realism, body clearance, or reference likeness.
Inspect the front, profile, and back after fitting the complete outfit.
"""

from collections import Counter, defaultdict
import math


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _mul(a, scalar):
    return tuple(x * scalar for x in a)


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _unit(a):
    length = math.sqrt(_dot(a, a))
    return _mul(a, 1 / length) if length > 1e-12 else (0.0, 0.0, 0.0)


def _mean(points):
    points = list(points)
    return tuple(sum(p[a] for p in points) / len(points) for a in range(3))


def _smoothstep(low, high, value):
    t = max(0.0, min(1.0, (value - low) / (high - low)))
    return t * t * (3 - 2 * t)


def _topology(points, faces):
    """Check only the unthickened shirt: one component and four simple openings."""
    used = {i for face in faces for i in face}
    if used != set(range(len(points))):
        raise ValueError('Connected blouse contains loose or missing vertices; every vertex must belong to its shirt surface.')
    edges = Counter()
    directed = {}
    adjacency = defaultdict(set)
    for face in faces:
        if len(face) != 4 or len(set(face)) != 4:
            raise ValueError(f'Connected blouse face {face} is not a four-corner quad; preserve the helper shell and opening rows.')
        a, b, c = (points[i] for i in face[:3])
        area = _cross(_sub(b, a), _sub(c, a))
        if _dot(area, area) < 1e-20:
            raise ValueError(f'Connected blouse face {face} collapsed during fitting; its corners must enclose a nonzero area.')
        for a, b in zip(face, face[1:] + face[:1]):
            key = tuple(sorted((a, b)))
            edges[key] += 1
            directed[key] = (a, b)
            adjacency[a].add(b)
            adjacency[b].add(a)
    if any(count > 2 for count in edges.values()):
        raise ValueError('Connected blouse has an edge shared by more than two faces; opening support rows must not branch.')
    unseen = set(used)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for other in adjacency[stack.pop()] & unseen:
                unseen.remove(other)
                stack.append(other)
    if components != 1:
        raise ValueError(f'Connected blouse has {components} surface components; both sleeves and torso must form one connected shell.')
    boundary = [directed[key] for key, count in edges.items() if count == 1]
    boundary_adjacency = defaultdict(set)
    for a, b in boundary:
        boundary_adjacency[a].add(b)
        boundary_adjacency[b].add(a)
    if any(len(neighbors) != 2 for neighbors in boundary_adjacency.values()):
        raise ValueError('Connected blouse opening branches or ends; neckline, hem, and both cuffs must each be a simple closed loop.')
    unseen = set(boundary_adjacency)
    loops = []
    while unseen:
        first = min(unseen)
        loop, previous, current = [], None, first
        while current not in loop:
            loop.append(current)
            unseen.remove(current)
            following = sorted(boundary_adjacency[current] - {previous})
            previous, current = current, following[0]
        if current != first:
            raise ValueError('Connected blouse boundary returns into its interior; each opening must close at its first vertex.')
        loops.append(loop)
    if len(loops) != 4:
        raise ValueError(f'Connected blouse has {len(loops)} openings; expected exactly neckline, hem, and two cuffs before solidify.')
    return loops, boundary, adjacency


def _prepare_blouse(native_data, scale):
    """Prepare a single candidate using local data only; callable without Blender."""
    from prepare_human_base import ASSETS, group_center, read_obj, to_blender

    raw = read_obj(ASSETS / 'base.obj')
    original = to_blender(native_data['vertices'], native_data['ground_y'], scale)
    proportion_fit = 'body_proportions' in native_data
    crop_points = to_blender(native_data.get('proportions_baseline_vertices', native_data['vertices']),
                             native_data['ground_y'], scale)
    body_height = max(original[i][2] for i in native_data['groups']['body'])
    if not 1.62 <= body_height <= 1.68:
        raise ValueError(f'Connected blouse crop is bounded to a 1.65 m adult reference, but body height is {body_height:.4f} m; refit the crop planes for a different size.')
    helper_faces = [face for face, group in zip(raw['faces'], raw['face_groups'])
                    if group == 'helper-tights']
    bridge_samples = [original[i] for i in sorted({i for face in helper_faces for i in face})
                      if abs(original[i][0]) < .14 and 1.08 < original[i][2] < 1.31]

    def chest_bridge(z):
        # A continuous weighted front envelope spans the anatomical cleavage.
        # Weighting actual helper points avoids a fixed world-space chest plane.
        weights = [math.exp(-((p[2]-z)/.010)**2-p[1]/.004) for p in bridge_samples]
        total = sum(weights)
        if not total:
            raise ValueError(f'Cotton chest bridge has no shaped helper support near {z:.4f} m.')
        return sum(p[1]*w for p,w in zip(bridge_samples,weights))/total-.009
    selected = []
    for face in helper_faces:
        center = _mean(crop_points[i] for i in face)
        if 1.015 < center[2] < 1.388 and abs(center[0]) < .255:
            selected.append(face)
    if not selected:
        raise ValueError('Connected blouse crop found no helper-tights faces; supply the full shaped MakeHuman vertex set at the reference scale.')

    # Area-weighted normals come from the full helper, before cutting openings.
    normals = defaultdict(lambda: (0.0, 0.0, 0.0))
    for face in helper_faces:
        a, b, c = (original[i] for i in face[:3])
        normal = _cross(_sub(b, a), _sub(c, a))
        for index in face:
            normals[index] = _add(normals[index], normal)
    ids = sorted({i for face in selected for i in face})
    remap = {old: new for new, old in enumerate(ids)}
    faces = [tuple(remap[i] for i in face) for face in selected]
    points = []
    for index in ids:
        x, y, z = original[index]
        normal = _unit(normals[index])
        # Small normal clearance keeps the fitted shoulders and underarm shape.
        point = list(_add((x, y, z), _mul(normal, .009)))
        torso = (1 - _smoothstep(.135, .185, abs(x))) * (1 - _smoothstep(1.28, 1.36, z))
        waist = 1 - _smoothstep(1.10, 1.27, z)
        side_ease = .05 * abs(x) if proportion_fit else .014 * min(1, abs(x) / .12)
        point[0] += math.copysign(side_ease * torso * waist, x)
        front = torso * (1 - _smoothstep(-.09, -.045, y))
        # Let cotton hang past the waist and soften the central chest contour.
        if proportion_fit:
            # Follow the reshaped helper with cotton ease; the previous fixed
            # front plane/14 mm side inflation hid actual waist/bust changes.
            target_front = y - (.008 + .010 * waist)
            bridge = math.exp(-(abs(x)/.090)**4)*_smoothstep(1.14, 1.17, z)*(1-_smoothstep(1.235, 1.29, z))
            target_front += bridge*(min(target_front, chest_bridge(z))-target_front)
        else:
            target_front = -.173 - .010 * math.exp(-((z - 1.19) / .10) ** 2)
            target_front += .019 * min(1, abs(x) / .15) ** 2
        point[1] += front * .72 * (min(point[1], target_front) - point[1])
        # Millimetric, broad folds; avoid periodic ring ridges and large bulges.
        fold = .0012 * torso * math.sin(45 * x + .4) * math.sin(12 * (z - 1.015))
        point[1] += fold * min(1, abs(normal[1]))
        points.append(tuple(point))

    loops, boundary, adjacency = _topology(points, faces)
    names, regularized = {}, {}
    for loop in loops:
        center = _mean(points[i] for i in loop)
        if center[2] < 1.08:
            name = 'hem'
            for i in loop:
                x, y, _ = points[i]
                regularized[i] = (x, y, 1.015)
        elif center[2] > 1.33:
            name = 'neckline'
            for i in loop:
                x, y, _ = points[i]
                # Preserve the native opening in X/Y, with a clean shallow slope.
                regularized[i] = (x, y, 1.390 + .08 * (y + .02))
        else:
            side = 'l' if center[0] > 0 else 'r'
            name = side + '_cuff'
            shoulder = to_blender([group_center(native_data, 'joint-' + side + '-shoulder')],
                                  native_data['ground_y'], scale)[0]
            elbow = to_blender([group_center(native_data, 'joint-' + side + '-elbow')],
                               native_data['ground_y'], scale)[0]
            direction = _unit(_sub(elbow, shoulder))
            plane_center = _add(shoulder, _mul(_sub(elbow, shoulder), .58))
            for i in loop:
                regularized[i] = _sub(points[i], _mul(direction, _dot(_sub(points[i], plane_center), direction)))
        if name in names:
            raise ValueError(f'Connected blouse crop produced two {name} openings; the fixed crop no longer fits this body.')
        names[name] = loop
    if set(names) != {'hem', 'neckline', 'l_cuff', 'r_cuff'}:
        raise ValueError(f'Connected blouse openings are {sorted(names)}; expected one neckline, hem, and cuff per side.')

    # Add two connected support rows to every opening. Moving the old boundary
    # slightly inward gives subdivision room without rounded, balloon-like hems.
    boundary_ids = set(regularized)
    face_neighbors = defaultdict(set)
    for face in faces:
        for index in face:
            face_neighbors[index].update(face)
    inward = {}
    for index in sorted(boundary_ids):
        neighbors = adjacency[index] - boundary_ids
        if not neighbors:
            # A crop corner can have two boundary edges and only a diagonal
            # interior vertex in its adjoining quad. Use that real cloth vertex.
            neighbors = face_neighbors[index] - boundary_ids
        if not neighbors:
            raise ValueError(f'Connected blouse opening vertex {index} has no interior neighbor; support rows require a real adjoining cloth surface.')
        interior = _mean(points[i] for i in neighbors)
        inward[index] = _unit(_sub(interior, regularized[index]))
        points[index] = _add(regularized[index], _mul(inward[index], .006))
    current = {i: i for i in boundary_ids}
    for distance in (.0017, 0.0):
        new = {}
        for index in sorted(boundary_ids):
            new[index] = len(points)
            points.append(_add(regularized[index], _mul(inward[index], distance)))
        for a, b in boundary:
            faces.append((current[b], current[a], new[a], new[b]))
        current = new

    _topology(points, faces)
    return points, faces, {name: len(loop) for name, loop in names.items()}


def build_blouse(native_data, scale, collection, pose, material, body_object=None):
    """Return one editable posed shirt mesh; no collar, pocket, or body edits."""
    import bpy

    points, faces, openings = _prepare_blouse(native_data, scale)
    posed = [tuple(pose(point)) for point in points]
    loops,_,adjacency=_topology(posed, faces)
    if body_object is not None:
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
        bpy.context.view_layer.update()
        body_tree=BVHTree.FromObject(body_object,bpy.context.evaluated_depsgraph_get())
        neck=next(loop for loop in loops if _mean(posed[i] for i in loop)[2]>1.33)
        seen=set(neck);frontier=set(neck)
        for influence in (1.0,.9,.7,.3):
            for index in frontier:
                point=Vector(posed[index])
                location,normal,face_index,distance=body_tree.find_nearest(point)
                if location is None or distance>.06:
                    raise RuntimeError(f'Blouse neckline vertex {index} lacks anatomical support within 60 mm.')
                target=location+normal*.0035
                posed[index]=tuple(point.lerp(target,influence))
            following={other for index in frontier for other in adjacency[index]}-seen
            seen.update(following);frontier=following
    from cloth_finish import apply_blouse_drape
    posed=apply_blouse_drape(posed,faces)
    _topology(posed, faces)
    data = bpy.data.meshes.new('Connected helper blouse / cotton shell')
    data.from_pydata(posed, [], faces)
    data.update()
    data.materials.append(material)
    for polygon in data.polygons:
        polygon.use_smooth = True
    obj = bpy.data.objects.new('Blouse / connected shoulders and short sleeves', data)
    collection.objects.link(obj)
    obj['asset'] = 'MakeHuman CC0 base.obj helper-tights; pinned local provenance under .tools/human_reference_assets'
    obj['construction'] = 'One connected quad shell; clean neckline, hem and two cuffs; two supporting rows per opening'
    obj['topology_components_before_thickness'] = 1
    obj['boundary_loops_before_thickness'] = 4
    obj['opening_vertex_counts'] = str(openings)
    obj['verification_bound'] = 'Current 1.65 m static reference-body crop, before subdivision and solidify; visual clearance and likeness require rendered inspection'
    smooth = obj.modifiers.new('Smooth continuous cotton surface', 'SUBSURF')
    smooth.levels = 2
    smooth.render_levels = 2
    cloth = obj.modifiers.new('Cotton thickness / 1.3 mm', 'SOLIDIFY')
    cloth.thickness = .0013
    cloth.offset = 1
    cloth.use_even_offset = 'body_proportions' not in native_data
    if 'body_proportions' in native_data:
        if body_object is None:
            raise ValueError('Proportion fitting requires the complete unculled anatomical support object.')
        from fitted_body_clearance import fit_evaluated_blouse
        fit_report = fit_evaluated_blouse(obj,body_object)
        print({'full_body_fit_result':fit_report},flush=True)
    return obj

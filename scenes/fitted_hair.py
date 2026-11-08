"""Fine shoulder-length hair from the fitted CC0 long01 UV guide surfaces.

Harness: tools/build_sailor_character.py renders the fixed hero, portrait, profile
and rear views against character-reference.png. No source cards or scalp slabs
are rendered. Finite coordinates and the geometric face check do not establish
photographic realism; those four views still need visual inspection.

The clearance gate samples every long-strand vertex and segment midpoint between
jaw and brow heights. Frontal strands must stay 2 mm beyond the evaluated head
cross-section. Placement uses a 4 mm buffer. Fringe has a separate eye-line bound.
"""
import bisect
import math
import random
from collections import defaultdict
from pathlib import Path


def _lerp(a, b, t):
    return a + (b - a) * t


def _mix(a, b, t):
    return tuple(_lerp(a[i], b[i], t) for i in range(3))


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def _uv_islands(fitted):
    """Split at real UV seams; source long01 has 32 longitudinal islands."""
    parent = {}

    def find(key):
        parent.setdefault(key, key)
        root = key
        while parent[root] != root:
            root = parent[root]
        while parent[key] != key:
            after = parent[key]
            parent[key] = root
            key = after
        return root

    for face, uv in zip(fitted['faces'], fitted['face_uvs']):
        pairs = list(zip(face, uv))
        for a, b in zip(pairs, pairs[1:] + pairs[:1]):
            parent[find(a)] = find(b)
    islands = defaultdict(list)
    for index, (face, uv) in enumerate(zip(fitted['faces'], fitted['face_uvs'])):
        islands[find((face[0], uv[0]))].append(index)
    return sorted(islands.values(), key=lambda values: (-len(values), values[0]))


def _cross_sections(face_ids, fitted, points, levels=96):
    """Follow normalized position across descending V, including curved UV edges."""
    triangles = []
    for face_id in face_ids:
        face, uv = fitted['faces'][face_id], fitted['face_uvs'][face_id]
        for i in range(1, len(face) - 1):
            triangles.append(tuple((fitted['uvs'][uv[j]], points[face[j]]) for j in (0, i, i + 1)))
    low = min(uv[1] for tri in triangles for uv, point in tri)
    high = max(uv[1] for tri in triangles for uv, point in tri)
    sections = []
    for row in range(levels):
        v = _lerp(high, low, (row + 0.025) / levels)
        segments = []
        for tri in triangles:
            hits = []
            for (ua, pa), (ub, pb) in zip(tri, tri[1:] + tri[:1]):
                if (ua[1] <= v < ub[1]) or (ub[1] <= v < ua[1]):
                    t = (v - ua[1]) / (ub[1] - ua[1])
                    hits.append((_lerp(ua[0], ub[0], t), _mix(pa, pb, t)))
            if len(hits) == 2 and abs(hits[0][0] - hits[1][0]) > 1e-10:
                a, b = sorted(hits, key=lambda value: value[0])
                segments.append((a[0], b[0], a[1], b[1]))
        if segments:
            segments.sort(key=lambda segment: segment[0])
            sections.append((segments, [segment[0] for segment in segments],
                             segments[0][0], max(segment[1] for segment in segments)))
    if len(sections) < 12:
        raise ValueError(f'long01 UV island at face {face_ids[0]} produced only {len(sections)} cross-sections; at least 12 are needed for its root-to-tip flow.')
    return sections


def _section_point(section, fraction):
    segments, starts, low, high = section
    u = _lerp(low, high, fraction)
    index = max(0, min(len(segments) - 1, bisect.bisect_right(starts, u) - 1))
    a, b, pa, pb = segments[index]
    if u > b and index + 1 < len(segments):
        following = segments[index + 1]
        if following[0] - u < u - b:
            a, b, pa, pb = following
    return _mix(pa, pb, max(0.0, min(1.0, (u - a) / (b - a))))


def _make_guides(fitted, points):
    banks = []
    for index, face_ids in enumerate(_uv_islands(fitted)):
        sections = _cross_sections(face_ids, fitted, points)
        number = 96 if index < 2 else 12
        banks.append([[_section_point(section, (column + 0.15) / (number - 0.7))
                       for section in sections] for column in range(number)])
    if len(banks) < 4:
        raise ValueError(f'long01 supplied only {len(banks)} UV islands; its fitted scalp and longitudinal flow islands are required.')
    return banks


def _trim(points, end_z):
    result = []
    for point in points:
        if result and point[2] < end_z:
            prior = result[-1]
            if prior[2] > end_z:
                result.append(_mix(prior, point, (prior[2] - end_z) / (prior[2] - point[2])))
            break
        result.append(point)
    return result


def _resample(points, step=0.0065):
    lengths = [0.0]
    for a, b in zip(points, points[1:]):
        lengths.append(lengths[-1] + math.dist(a, b))
    if len(points) < 4 or lengths[-1] < 0.03:
        raise ValueError('A long01 guide is shorter than 30 mm or has fewer than four points; its UV root-to-tip path was not reconstructed.')
    count = max(24, min(44, math.ceil(lengths[-1] / step) + 1))
    result = []
    for i in range(count):
        distance = lengths[-1] * i / (count - 1)
        j = max(0, min(len(points) - 2, bisect.bisect_right(lengths, distance) - 1))
        span = lengths[j + 1] - lengths[j]
        result.append(_mix(points[j], points[j + 1], (distance - lengths[j]) / span if span else 0))
    return result


class _HeadSurface:
    """Evaluated anatomical BVH plus an explicit frontal cheek exclusion bound."""

    def __init__(self, bpy, native, scale, body_object):
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
        from prepare_human_base import group_center, to_blender
        self.Vector = Vector
        world = to_blender(native['vertices'], native['ground_y'], scale)
        body_points = [world[i] for i in native['groups']['body']]
        self.top = max(p[2] for p in body_points)
        joint = to_blender([group_center(native, 'joint-head')], native['ground_y'], scale)[0]
        eye = to_blender([group_center(native, 'joint-l-eye')], native['ground_y'], scale)[0]
        jaw = to_blender([group_center(native, 'joint-jaw')], native['ground_y'], scale)[0]
        self.cx, self.cy, self.eye = joint[0], joint[1], eye[2]
        self.brow, self.jaw = self.eye + 0.017, jaw[2] - 0.007
        self.centre = Vector((self.cx, self.cy, self.eye + 0.008))
        self.evaluated_body = body_object is not None
        if body_object is not None:
            bpy.context.view_layer.update()
            evaluated = body_object.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh = evaluated.to_mesh()
            try:
                vertices = [evaluated.matrix_world @ vertex.co for vertex in mesh.vertices]
                polygons = [tuple(polygon.vertices) for polygon in mesh.polygons]
                self.tree = BVHTree.FromPolygons(vertices, polygons)
            finally:
                evaluated.to_mesh_clear()
        else:
            self.tree = BVHTree.FromPolygons([Vector(p) for p in world], native['faces'])
        self.front_origin = min(p[1] for p in body_points if p[2] > self.jaw) - 0.15
        self.width_cache = {}
        self.envelope_cache = {}
        self.face_probes = self.skin_probes = 0
        self.minimum_clearance = math.inf

    def front(self, x, z):
        hit = self.tree.ray_cast(self.Vector((x, self.front_origin, z)),
                                 self.Vector((0, 1, 0)), 0.55)[0]
        return None if hit is None else hit.y

    def width(self, z, side):
        key = (round(z / 0.0005), side)
        if key not in self.width_cache:
            zz = key[0] * 0.0005
            hits = []
            for y_offset in (-0.052, -0.026, 0.0, 0.010):
                hit = self.tree.ray_cast(self.Vector((self.cx, self.cy + y_offset, zz)),
                                         self.Vector((side, 0, 0)), 0.18)[0]
                if hit is not None:
                    hits.append(abs(hit.x - self.cx))
            if not hits:
                raise ValueError(f'Head fitting found no facial cross-section at z={zz:.6f} m, side={side}; provide a complete anatomical body mesh.')
            self.width_cache[key] = max(hits)
        return self.width_cache[key]

    def fit(self, point, side, margin):
        p = self.Vector(point)
        if p.z >= self.jaw - 0.008:
            direction = p - self.centre
            length = direction.length
            if length > 1e-6:
                direction /= length
                hit, normal, index, distance = self.tree.ray_cast(self.centre, direction, 0.35)
                if hit is not None and length < distance + margin:
                    p = hit + direction * margin
        return self.fit_lateral(p, side, margin)

    def fit_lateral(self, point, side, margin):
        """Change X only, preserving the final polyline's Y/Z sampling bound."""
        p=self.Vector(point)
        if self.jaw - 0.012 <= p.z <= self.brow + 0.035 and p.y < self.cy + 0.040:
            # The guide is a polyline, so its entire segment must clear local
            # width peaks. Point-only fitting missed a peak between endpoints.
            # The 10 mm envelope exceeds the final 6.5 mm Y/Z interval bound.
            key=(round(p.z/.0005),side)
            if key not in self.envelope_cache:
                center_z=key[0]*.0005
                self.envelope_cache[key]=max(self.width(center_z+i*.0005,side) for i in range(-20,21))
            width = self.envelope_cache[key] + 0.004 + margin*.3
            # Finish the transition above the verified brow band; do not fade
            # the correction on an endpoint adjacent to a protected segment.
            weight = _smooth((self.brow + 0.035 - p.z) / 0.020)
            current = side * (p.x - self.cx)
            if current < width:
                p.x = self.cx + side * _lerp(current, width, weight)
        return tuple(p)

    def verify_long(self, points, side, strand_id):
        probes = list(points)
        probes.extend(_mix(a, b, 0.5) for a, b in zip(points, points[1:]))
        for p in probes:
            if not all(math.isfinite(value) for value in p):
                raise ValueError(f'long01 strand {strand_id} has non-finite coordinates {p}.')
            if self.jaw <= p[2] <= self.brow and p[1] < self.cy + 0.020:
                self.face_probes += 1
                clearance = side * (p[0] - self.cx) - self.width(p[2], side)
                self.minimum_clearance = min(self.minimum_clearance, clearance)
                if clearance < 0.002:
                    raise ValueError(f'long01 strand {strand_id} enters the frontal cheek zone at {tuple(round(v, 6) for v in p)}: clearance {clearance:.6f} m is below the required 0.002 m.')
                skin_y = self.front(p[0], p[2])
                self.skin_probes += 1
                if skin_y is not None and p[1] > skin_y - 0.00015:
                    raise ValueError(f'long01 strand {strand_id} intersects skin in the frontal cheek zone at {tuple(round(v, 6) for v in p)}; front skin is y={skin_y:.6f} m.')


def _long_points(bank, rng, head, strand_id, flyaway=False):
    location = rng.uniform(0.15, len(bank) - 1.15)
    index = min(len(bank) - 2, int(location))
    guide = [_mix(a, b, location - index) for a, b in zip(bank[index], bank[index + 1])]
    guide = guide[rng.randrange(0, 4):]
    end_z = head.top - rng.uniform(0.291, 0.309)
    guide = _trim(guide, end_z)
    side = -1 if sum(p[0] - head.cx for p in guide) < 0 else 1
    deformed = []
    for x, y, z in guide:
        t = _smooth((head.brow - z) / (head.brow - end_z))
        deformed.append((head.cx + (x - head.cx) * _lerp(1, 0.81, t),
                         head.cy + (y - head.cy) * _lerp(1, 0.88, t), z))
    points = _resample(deformed)
    phase = rng.uniform(0, math.tau)
    amplitude = rng.uniform(0.00010, 0.00055)
    layer = rng.uniform(0.0001, 0.0025)
    margin = rng.uniform(0.0012, 0.0020)
    if flyaway:
        amplitude += rng.uniform(0.0010, 0.0023)
    result = []
    for i, (x, y, z) in enumerate(points):
        t = i / (len(points) - 1)
        pulse = math.sin(math.pi * t)
        dx, dy = x - head.cx, y - head.cy
        radial = math.hypot(dx, dy)
        if radial > 0.001:
            x += layer * dx / radial
            y += layer * dy / radial
        x += amplitude * pulse * math.sin(phase + 5.2 * t)
        y += amplitude * pulse * 0.55 * math.sin(phase * 0.7 + 4.1 * t)
        result.append(head.fit((x, y, z), side, margin))
    # Radial fitting can alter Y/Z, and the initial guide has a point-count cap.
    # Bound the actual final segments after radial fitting, then move X only.
    bounded=[head.fit_lateral(result[0],side,margin)]
    for a,b in zip(result,result[1:]):
        divisions=max(1,math.ceil(max(abs(b[1]-a[1]),abs(b[2]-a[2]))/.006))
        for j in range(1,divisions+1):
            bounded.append(head.fit_lateral(_mix(a,b,j/divisions),side,margin))
    result=bounded
    if any(max(abs(b[1]-a[1]),abs(b[2]-a[2]))>.0065 for a,b in zip(result,result[1:])):
        raise ValueError(f'long01 strand {strand_id} exceeds the final 6.5 mm Y/Z segment bound.')
    head.verify_long(result, side, strand_id)
    return result


def _fringe_points(rng, head):
    """Continuous random placement avoids the former eight vertical stripes."""
    tip_x = head.cx + rng.uniform(-0.058, 0.058)
    side = -1 if tip_x < head.cx else 1
    root_x = head.cx + side * rng.uniform(0.003, 0.017)
    root_y = head.cy - rng.uniform(0.005, 0.025)
    root_z = head.top + rng.uniform(0.001, 0.0035)
    end_z = head.eye + rng.uniform(0.0045, 0.027)
    end_z += 0.008 * (abs(tip_x - head.cx) / 0.058) ** 2
    margin = rng.uniform(0.0010, 0.0022)
    phase = rng.uniform(0, math.tau)
    points, measured = [], []
    for i in range(36):
        t = i / 35
        x = _lerp(root_x, tip_x, _smooth(t)) + 0.00045 * math.sin(math.pi * t) * math.sin(phase + t * 4)
        z = _lerp(root_z, end_z, t ** 1.20)
        skin_y = head.front(x, z)
        measured.append(skin_y)
        points.append((x, root_y if skin_y is None else skin_y - margin, z))
    first = next((i for i, y in enumerate(measured) if y is not None), None)
    if first is None:
        raise ValueError('A fringe strand found no forehead surface; supply the anatomical head in body_object.')
    if first:
        for i in range(first):
            x, y, z = points[i]
            points[i] = (x, _lerp(root_y, points[first][1], i / first), z)
    old = points[:]
    for i in range(1, len(points) - 1):
        x, y, z = old[i]
        y = (old[i - 1][1] + 2 * y + old[i + 1][1]) / 4
        if measured[i] is not None:
            y = min(y, measured[i] - margin)
        points[i] = (x, y, z)
    if min(p[2] for p in points) < head.eye + 0.004:
        raise ValueError('Fringe tips fall below eye_z + 0.004 m; this fringe must stay above the eye line.')
    return points


def _materials(bpy):
    colors = ((0.0045, 0.0033, 0.0027), (0.0070, 0.0049, 0.0037),
              (0.0100, 0.0069, 0.0048), (0.0150, 0.0102, 0.0068))
    result = []
    for index, color in enumerate(colors):
        material = bpy.data.materials.new(f'Hair fine cylinder / dark brown {index + 1}')
        material.use_nodes = True
        material.diffuse_color = (*color, 1)
        shader = material.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Base Color'].default_value = (*color, 1)
        shader.inputs['Roughness'].default_value = 0.38 + index * 0.017
        shader.inputs['IOR'].default_value = 1.55
        shader.inputs['Specular IOR Level'].default_value = 0.30
        shader.inputs['Coat Weight'].default_value = 0.0
        # Real microscopic cylindrical normals replace sheet normals and baked
        # highlights. These are opaque filaments, not transparent hair cards.
        shader.inputs['Alpha'].default_value = 1.0
        result.append(material)
    return result


def _curve_group(bpy, name, collection, materials):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = data.render_resolution_u = 1
    data.bevel_depth = 0.000060
    data.bevel_resolution = 1
    data.use_fill_caps = False
    for material in materials:
        data.materials.append(material)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    obj['source_asset'] = 'MakeHuman system assets hair/long01: fitted MHCLO and OBJ'
    obj['source_license'] = 'CC0, September 2020; local source/license manifest in .tools/human_reference_assets'
    obj['construction'] = 'Fitted UV flow converted to opaque fine curves; source cards are not rendered'
    obj['seed'] = 9020526
    return obj


def _add_strand(data, points, rng, fringe=False):
    spline = data.splines.new('POLY')
    spline.points.add(len(points) - 1)
    spline.points.foreach_set('co', [value for point in points for value in (*point, 1.0)])
    shaft = rng.uniform(2 / 3, 1.10 if fringe else 4 / 3)
    radii = []
    for index in range(len(points)):
        t = index / (len(points) - 1)
        start, span = (0.56, 0.44) if fringe else (0.76, 0.24)
        tip = 1.0 - 0.96 * _smooth((t - start) / span)
        root = _lerp(0.85, 1.0, min(1.0, t / 0.10))
        radii.append(shaft * root * tip)
    spline.points.foreach_set('radius', radii)
    spline.material_index = rng.choices(range(4), (22, 43, 27, 8))[0]


def build_hair(native_data, scale, collection, body_object=None):
    """Return five editable curve objects; no hair card or scalp slab is created."""
    import bpy
    from prepare_human_base import ASSETS, fit_proxy, to_blender
    directory = Path(ASSETS) / 'hair' / 'long01'
    fitted = fit_proxy(directory / 'long01.mhclo', native_data['vertices'])
    points = to_blender(fitted['vertices'], native_data['ground_y'], scale)
    banks = _make_guides(fitted, points)
    head = _HeadSurface(bpy, native_data, scale, body_object)
    rng = random.Random(9020526)
    materials = _materials(bpy)
    objects, strand_id = [], 0
    specs = (('Hair / left fitted fine flow', 8250, [0], False),
             ('Hair / right fitted fine flow', 8250, [1], False),
             ('Hair / layered fitted fine flow', 5950, list(range(2, len(banks))), False),
             ('Hair / sparse wispy fringe', 1450, [], False),
             ('Hair / subtle flyaways', 100, list(range(len(banks))), True))
    low, high = [math.inf] * 3, [-math.inf] * 3
    for name, count, bank_ids, flyaway in specs:
        obj = _curve_group(bpy, name, collection, materials)
        fringe = not bank_ids
        for index in range(count):
            strand = (_fringe_points(rng, head) if fringe else
                      _long_points(banks[bank_ids[index % len(bank_ids)]], rng, head, strand_id, flyaway))
            if not all(math.isfinite(value) for point in strand for value in point):
                raise ValueError(f'Hair strand {strand_id} has a non-finite point; its UV guide or head fitting is invalid.')
            for point in strand:
                for axis in range(3):
                    low[axis], high[axis] = min(low[axis], point[axis]), max(high[axis], point[axis])
            _add_strand(obj.data, strand, rng, fringe)
            strand_id += 1
        obj['strand_count'] = count
        obj['evaluated_anatomical_fit'] = head.evaluated_body
        objects.append(obj)
    if head.face_probes == 0 or head.skin_probes == 0:
        raise ValueError('Hair face-clearance verification sampled no frontal cheek-zone segments; that is not a passing geometry check.')
    for obj in objects:
        obj['face_clearance_probes'] = head.face_probes
        obj['skin_surface_probes'] = head.skin_probes
        obj['minimum_measured_lateral_clearance_m'] = head.minimum_clearance
        obj['face_clearance_violations'] = 0
        obj['bounds_min_m'], obj['bounds_max_m'] = low, high
    print({'hair_strands': strand_id, 'guide_islands': len(banks),
           'bounds_min_m': low, 'bounds_max_m': high,
           'face_clearance_probes': head.face_probes, 'skin_surface_probes': head.skin_probes,
           'minimum_lateral_clearance_m': head.minimum_clearance,
           'source': 'CC0 MakeHuman long01 fitted UV flow rendered as fine opaque curves'})
    return objects


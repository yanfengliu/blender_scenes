"""A bounded corner and cheek response on the existing adult hm08 face.

Harness: the main's native-expression AST and prepare_human_base supply the
post-perioral mesh. This helper runs before body proportions and proxy fitting.
Bound: native body faces, a traced 38-quad oral strip and changed source triangle
fans. The historical paired source-vector diagnostic includes internal rails
and averaged-X interpolation; it is not an exterior aperture gate. Every build
must run tools.verify_reference_smile's live evaluated_exterior_aperture gate
after final body, pose and subdivision. Source checks do not establish evaluated
closure, surface intersections or likeness. Fixed native views remain required.
"""
import heapq
import math


CORNER_LIFT_M = .0010
SUPPORT_DISTANCE_M = .018


def _smooth(value):
    t = max(0., min(1., value))
    return t*t*t*(10. + t*(-15. + t*6.))


def _arch(parameter):
    # Spread curvature across the mouth. A delayed quintic rise changed opposing
    # interpolated rails by 87.6 um because their actual tessellation differs.
    # This C1 arch retains a flat central 10% and the configured corner lift.
    t = max(0., min(1., (parameter-.10)/.90))
    return t*t*(3.-2.*t)


def _normal(vertices, triangle):
    a, b, c = (vertices[i] for i in triangle)
    u = [b[k]-a[k] for k in range(3)]
    v = [c[k]-a[k] for k in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def trace_oral_strip(faces):
    """Follow opposite edges in real quads; preserve outer/inner rail identity.

    Starting outer/inner edge 520/537 is the inspected upper center. The first
    face goes toward 521. Adjacency then supplies every subsequent row, including
    the 16 corner-strip rows absent from the older 60-row MOUTH_CONTACT set.
    """
    edge_faces = {}
    for fi, face in enumerate(faces):
        for k, i in enumerate(face):
            edge_faces.setdefault(tuple(sorted((i, face[(k+1) % len(face)]))), []).append(fi)
    edge = (520, 537)
    first = edge
    previous = None
    sections, strip_faces = [], []
    for _ in range(64):
        options = [fi for fi in edge_faces.get(tuple(sorted(edge)), []) if fi != previous]
        if previous is None:
            options = [fi for fi in options if 521 in faces[fi]]
        if len(options) != 1:
            raise ValueError(f'Reference smile oral edge {edge} has {len(options)} continuations; restore the inspected hm08 quad strip.')
        fi = options[0]
        face = faces[fi]
        if len(face) != 4:
            raise ValueError(f'Reference smile oral face {fi} is not a quad; review the changed topology.')
        following = []
        for row in edge:
            k = face.index(row)
            neighbors = (face[k-1], face[(k+1) % 4])
            following.append(next(i for i in neighbors if i not in edge))
        sections.append(edge)
        strip_faces.append(fi)
        edge = tuple(following)
        previous = fi
        if edge == first:
            break
    if edge != first or len(sections) != 38 or len({i for pair in sections for i in pair}) != 76:
        raise ValueError('Reference smile requires the complete 38-quad, 76-row closed oral strip; inspect its topology before proceeding.')
    if (523, 540) not in sections:
        raise ValueError('Reference smile oral strip omitted lower center 523/540; restore the outer/inner rail correspondence.')
    return sections, strip_faces


def oral_parameterization(vertices, sections, scale):
    centers = [tuple((vertices[a][k]+vertices[b][k])*.5 for k in range(3)) for a, b in sections]
    lower = sections.index((523, 540))
    corners = [min(range(lower), key=lambda i: centers[i][0]),
               max(range(lower, len(sections)), key=lambda i: centers[i][0])]
    if corners != [12, 26] or lower != 19:
        raise ValueError(f'Reference smile corner/center order changed to {corners}/{lower}; inspect the actual oral strip.')
    widths = [abs(centers[i][0])*scale for i in corners]
    if any(not .022 < width < .027 for width in widths):
        raise ValueError(f'Reference smile needs the retained post-perioral half widths of 22-27 mm; received {widths} m.')
    paths = [
        {'side': -1, 'upper': list(range(0, corners[0]+1)), 'lower': list(range(lower, corners[0]-1, -1))},
        {'side': 1, 'upper': [0]+list(range(len(sections)-1, corners[1]-1, -1)), 'lower': list(range(lower, corners[1]+1))},
    ]
    # A shared lateral coordinate at each full strip cross-section is assigned
    # to BOTH outer and inner vertices. It is not a separate Gaussian per row.
    parameters = {}
    for path, width in zip(paths, widths):
        for rail_name in ('upper', 'lower'):
            indices = path[rail_name]
            values = [0. if i in (0, lower) else abs(centers[i][0])*scale/width for i in indices]
            if any(b <= a for a, b in zip(values, values[1:])):
                raise ValueError(f'Reference smile {path["side"]}/{rail_name} oral parameter is not monotone; inspect the folded or reordered input.')
            path[rail_name+'_t'] = values
            for i, value in zip(indices, values):
                parameters[i] = value
    return centers, paths, parameters, corners


def _rail_sample(path, rail_name, sections, t):
    values = path[rail_name+'_t']
    indices = path[rail_name]
    for k in range(len(values)-1):
        if values[k] <= t <= values[k+1]:
            weight = (t-values[k])/(values[k+1]-values[k])
            return {'sections': [indices[k], indices[k+1]],
                    'rows': [list(sections[indices[k]]), list(sections[indices[k+1]])],
                    'weight': weight}
    raise ValueError(f'Reference smile sample {t} lies outside the traced {rail_name} path.')


def paired_oral_samples(before, after, sections, paths, scale):
    """Export interpolation pairs, including all row knots and both corners.

    Opposing paths have different tessellation. Pair them at the SAME traced
    lateral parameter, independently interpolate both source rails, and measure
    their actual change. This bounds sampled source separation; it does not
    assert exact or continuous subdivision closure.
    """
    result = []
    for path in paths:
        samples = sorted(set(path['upper_t']+path['lower_t']+[i/256 for i in range(257)]))
        for t in samples:
            upper = _rail_sample(path, 'upper', sections, t)
            lower = _rail_sample(path, 'lower', sections, t)
            for depth in range(2):
                def point(vertices, sample):
                    a, b = (vertices[rows[depth]] for rows in sample['rows'])
                    return tuple(a[k]+sample['weight']*(b[k]-a[k]) for k in range(3))
                old_a, old_b = point(before, upper), point(before, lower)
                new_a, new_b = point(after, upper), point(after, lower)
                difference = [(new_a[k]-new_b[k])-(old_a[k]-old_b[k]) for k in range(3)]
                result.append({'side': path['side'], 't': t, 'depth': depth,
                               'upper': upper, 'lower': lower,
                               'before_gap_m': math.dist(old_a, old_b)*scale,
                               'after_gap_m': math.dist(new_a, new_b)*scale,
                               'separation_vector_change_m': math.sqrt(sum(v*v for v in difference))*scale})
    return result


def apply_reference_smile(native, scale=None):
    """Lift corners by 1.0 mm with a smooth adjacent cheek response.

    All X coordinates remain exact. Full oral cross-sections share a vertical
    value and keep depth exact. Central lip source rows remain exact. No existing
    helper is changed; this is a separate stage after the retained perioral edit.
    """
    from gentle_expression import MOUTH_CONTACT, EYE_CORNERS, EYE_PROXY_SCALE_ANCHORS
    from prepare_human_base import to_blender
    vertices = native['vertices']
    if len(vertices) != 19158 or any(not all(math.isfinite(c) for c in v) for v in vertices):
        raise ValueError('Reference smile requires 19,158 finite hm08 rows; restore native index correspondence and coordinates.')
    before = [tuple(v) for v in vertices]
    body = set(native['groups']['body'])
    height = max(before[i][1] for i in body)-native['ground_y']
    scale = 1.65/height if scale is None else scale
    if not math.isfinite(scale) or abs(height*scale-1.65) > 1e-6:
        raise ValueError('Reference smile requires the retained 1.65 m adult scale; preserve the body scale.')
    faces = native['faces']
    sections, strip_faces = trace_oral_strip(faces)
    centers, paths, parameters, corners = oral_parameterization(before, sections, scale)
    oral = {i for pair in sections for i in pair}
    if not set(MOUTH_CONTACT) <= oral or not oral <= body:
        raise ValueError('Reference smile traced strip lost a prior oral row or includes a helper; restore body topology.')
    world = to_blender(before, native['ground_y'], scale)
    adjacency = {i: set() for i in body}
    for face in faces:
        for k, i in enumerate(face):
            adjacency[i].update((face[k-1], face[(k+1) % len(face)]))
    distance = {i: 0. for i in oral}
    queue = [(0., i) for i in oral]
    heapq.heapify(queue)
    while queue:
        length, i = heapq.heappop(queue)
        if length != distance[i]:
            continue
        for j in adjacency[i]:
            value = length+math.dist(before[i], before[j])*scale
            if value < SUPPORT_DISTANCE_M and value < distance.get(j, math.inf):
                distance[j] = value
                heapq.heappush(queue, (value, j))
    pinned = set(EYE_PROXY_SCALE_ANCHORS)
    for pair in EYE_CORNERS.values():
        pinned.update(pair)
    for name, rows in native['groups'].items():
        if name != 'body':
            pinned.update(rows)
    after = [list(v) for v in before]
    half_width = sum(abs(centers[i][0])*scale for i in corners)*.5
    section_values = {i: CORNER_LIFT_M*_arch(t) for i, t in parameters.items()}
    for i, length in distance.items():
        x, y, z = world[i]
        # C2 physical-distance support and C2 spatial guards vanish before the
        # jaw, nose, lids and lateral outline. No abrupt face-ring pin is used.
        taper = 1.-_smooth(length/SUPPORT_DISTANCE_M)
        vertical = _smooth((z-1.463)/.006)*(1.-_smooth((z-1.508)/.010))
        front = 1.-_smooth((y+.126)/.016)
        corner = CORNER_LIFT_M*_arch(abs(x)/half_width)
        cheek = _smooth(length/.005)*_smooth((z-1.485)/.010)
        cheek *= _smooth((abs(x)-.018)/.010)*(1.-_smooth((abs(x)-.040)/.010))
        lift = (corner+.00065*cheek)*taper*vertical*front
        forward = .00035*cheek*taper*vertical*front
        if lift or forward:
            after[i][1] += lift/scale
            after[i][2] += forward/scale
    for section, rows in enumerate(sections):
        value = section_values[section]
        for i in rows:
            after[i] = [before[i][0], before[i][1]+value/scale, before[i][2]]
    changed = {i for i in range(len(before)) if tuple(after[i]) != before[i]}
    if changed & pinned or not changed <= set(distance):
        raise ValueError('Reference smile moved a protected helper/proxy row or left its 18 mm surface support; inspect the input anatomy.')
    for i in changed:
        x, y, z = world[i]
        if not (abs(x) < .049 and -.160 < y < -.108 and 1.463 < z < 1.518):
            raise ValueError(f'Reference smile row {i} moved outside its declared lower-face box at {world[i]}; restore the local support.')
    if not changed or max(math.dist(before[i], after[i])*scale for i in changed) > .001001:
        raise ValueError('Reference smile is absent or exceeds its 1.0 mm displacement allowance; inspect support and units.')
    for i in range(len(before)):
        if after[i][0] != before[i][0]:
            raise ValueError(f'Reference smile changed width at row {i}; retain all X coordinates.')
    for i in (520, 523, 537, 540, 466):
        if tuple(after[i]) != before[i]:
            raise ValueError(f'Reference smile changed central lip row {i}; retain the accepted central contour and contact.')
    area_ratio, normal_dot, affected = 1., 1., 0
    for face in faces:
        if not changed.intersection(face):
            continue
        for k in range(1, len(face)-1):
            triangle = (face[0], face[k], face[k+1])
            a, b = _normal(before, triangle), _normal(after, triangle)
            al, bl = math.sqrt(sum(v*v for v in a)), math.sqrt(sum(v*v for v in b))
            ratio = bl/al if al else 0.
            dot = sum(u*v for u, v in zip(a, b))/(al*bl) if al*bl else -1.
            if ratio <= .25 or dot <= 0.:
                raise ValueError(f'Reference smile folds or collapses source triangle {triangle}: area ratio {ratio}, normal dot {dot}; inspect its support gradient.')
            area_ratio, normal_dot = min(area_ratio, ratio), min(normal_dot, dot)
            affected += 1
    pairs = paired_oral_samples(before, after, sections, paths, scale)
    worst = max(p['separation_vector_change_m'] for p in pairs)
    # Retain the old red measurement honestly. Its internal/averaged-X vector
    # change does not measure exterior opening. The required live gate compares
    # actual exterior scalar and vertical gaps under the unchanged 50 um bound.
    source_diagnostic = {'name': 'historical_source_separation_vector',
        'maximum_change_m': worst, 'historical_bound_m': .00005,
        'historical_status': 'RED' if worst > .00005 else 'within historical bound',
        'scope': 'Source outer and internal rails at averaged cross-section X; not an evaluated exterior aperture claim.'}
    for i in changed:
        vertices[i][:] = after[i]
    return {'changed_rows': sorted(changed), 'oral_sections': [list(p) for p in sections],
            'oral_strip_faces': strip_faces, 'oral_paths': paths, 'paired_samples': pairs,
            'corner_sections': corners, 'section_parameters': parameters,
            'section_lifts_m': section_values, 'geodesic_distance_m': distance,
            'explicit_pinned_rows': sorted(pinned),
            'maximum_displacement_m': max(math.dist(before[i], after[i])*scale for i in changed),
            'maximum_paired_separation_change_m': worst,
            'source_vector_diagnostic': source_diagnostic,
            'required_evaluated_gate': 'evaluated_exterior_aperture',
            'native_before_changed': [[i, *before[i]] for i in sorted(changed)],
            'native_after_changed': [[i, *after[i]] for i in sorted(changed)],
            'affected_source_triangles': affected, 'minimum_area_ratio': area_ratio,
            'minimum_normal_dot': normal_dot,
            'bound': 'Source hm08 body only. Complete 38-quad/76-row oral strip; full cross-section depth and every native X exact. Changed source fans keep area ratio>.25 and positive orientation. Historical source-vector diagnostic is retained, including its RED result. REQUIRED live evaluated_exterior_aperture gate after body/pose/subdivision compares actual exterior scalar and vertical gap increases below50um, actual surface orientation and intersections, complete oral topology and numerical controls. This pure helper does not certify evaluated closure, proxies, masks or likeness.'}

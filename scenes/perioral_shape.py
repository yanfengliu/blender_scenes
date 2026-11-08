"""Bounded local lip reshaping with preserved native contact rows.

Harness: prepare_human_base and the current main's native-expression block
provide the inspected hm08 mesh for pure checks. Only the licensed upper-lip
target support and oral-rim adjacency may move. Source checks do not certify
evaluated lip contact, proxy fitting or likeness; native oblique/profile review
remains required before retaining an integrated candidate.
"""
import hashlib
import heapq
import math


UPPER_LIP_SHA256 = 'b124cbd9b9be318264f61a143da603b42e0357ed92b4b6afd1b31a83daaf8568'


def _smooth(value):
    t = max(0.0, min(1.0, value))
    return t*t*t*(t*(t*6.0-15.0)+10.0)


def _cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _triangle_normal(vertices, triangle):
    a, b, c = (vertices[i] for i in triangle)
    return _cross(tuple(b[j]-a[j] for j in range(3)),
                  tuple(c[j]-a[j] for j in range(3)))


def apply_perioral_shape(native, scale=None):
    """Retract the upper vermilion crest by 2 mm and widen contact by 8%.

    Native X is lateral, Y vertical and Z forward. The target is used only as
    anatomical support; no target volume is reapplied. Contact Y/Z and every
    vertex beyond the sparse support stay exact. Contact X uses one shared
    linear map for upper/lower rows, fading over 12 mm of actual face adjacency.
    """
    from gentle_expression import MOUTH_CONTACT, EYE_CORNERS, EYE_PROXY_SCALE_ANCHORS
    from prepare_human_base import ASSETS

    vertices = native['vertices']
    if len(vertices) != 19158:
        raise ValueError('Perioral shaping requires the inspected 19,158-vertex hm08 topology; restore native index correspondence.')
    before = [tuple(v) for v in vertices]
    if any(not all(math.isfinite(c) for c in point) for point in before):
        raise ValueError('Perioral shaping received nonfinite native coordinates; repair them before reshaping the lips.')
    body = set(native['groups']['body'])
    height = max(before[i][1] for i in body)-native['ground_y']
    scale = 1.65/height if scale is None else scale
    if not math.isfinite(scale) or abs(height*scale-1.65) > 1e-6:
        raise ValueError('Perioral shaping is bounded to the existing 1.65 m adult; preserve the current scale.')
    data = (ASSETS/'mouth-upperlip-volume-incr.target').read_bytes()
    if hashlib.sha256(data).hexdigest() != UPPER_LIP_SHA256:
        raise ValueError('The upper-lip target differs from the inspected CC0 hm08 asset; review its support before applying this helper.')
    target = {int(parts[0]):tuple(float(n) for n in parts[1:4])
              for line in data.decode('utf-8').splitlines()
              if (parts := line.split()) and parts[0].isdigit()}
    contact = set(MOUTH_CONTACT)
    if len(target) != 168 or len(contact) != 60 or not (set(target)|contact) <= body:
        raise ValueError('Perioral support must contain the inspected 168 target rows and 60 body oral-contact rows.')
    adjacency = {i:set() for i in body}
    for face in native['faces']:
        for i in face:
            adjacency[i].update(face)
    if not {521,537} <= adjacency[520] or not {534,557} <= adjacency[540]:
        raise ValueError('The oral-rim face adjacency no longer matches hm08; do not reshape unknown contact topology.')

    # Ring count is unsuitable for the very uneven hm08 mouth-corner spacing:
    # two adjacent dense rows previously received a displacement step large
    # enough to reverse their triangle. Use measured shortest paths over face
    # adjacency, originating only at the known oral rim, with a smooth taper.
    distance = {i:0.0 for i in contact}
    queue = [(0.0,i) for i in contact]
    heapq.heapify(queue)
    while queue:
        length,i = heapq.heappop(queue)
        if length != distance[i]:continue
        for other in adjacency[i]:
            candidate = length+math.dist(before[i],before[other])*scale
            if candidate < .012 and candidate < distance.get(other,math.inf):
                distance[other] = candidate
                heapq.heappush(queue,(candidate,other))
    after = [list(v) for v in before]
    width_rows = set()
    for i,length in distance.items():
        weight = 1.0-_smooth(length/.012)
        if weight:
            after[i][0] = before[i][0]*(1.0+.08*weight)
            width_rows.add(i)

    # The positive-forward target support identifies the actual upper vermilion.
    # Quintic taper gives zero derivative at its zero support and at the crest.
    # A second depth taper reaches zero at the central contact plane; oral rows
    # are also explicitly pinned, so no depth/height separation is introduced.
    contact_depth = before[520][2]
    crest_span = before[466][2]-contact_depth
    if not .006 < crest_span*scale < .009 or target[466][2] <= 0:
        raise ValueError('The current upper-lip crest is outside the inspected 6–9 mm forward-span range; reassess this deformation before applying it.')
    retracted = set()
    for i,delta in target.items():
        if i in contact or delta[2] <= 0:
            continue
        weight = _smooth(delta[2]/target[466][2])
        weight *= _smooth((before[i][2]-contact_depth)/crest_span)
        if weight:
            after[i][2] -= .002*weight/scale
            retracted.add(i)

    changed = {i for i,(a,b) in enumerate(zip(before,after)) if a != tuple(b)}
    allowed = set(target)|set(distance)
    pinned = set(range(len(vertices)))-allowed
    pinned.update(EYE_PROXY_SCALE_ANCHORS)
    for pair in EYE_CORNERS.values():pinned.update(pair)
    for name,indices in native['groups'].items():
        if name != 'body':pinned.update(indices)
    maximum = max((math.dist(before[i],after[i])*scale for i in changed),default=0.0)
    if not changed <= allowed or changed & pinned or maximum >= .003:
        raise ValueError(f'Perioral shaping changed a protected row or exceeded its <3 mm displacement bound; maximum {maximum:.7f} m.')
    if any(after[i][1:] != list(before[i][1:]) for i in contact):
        raise ValueError('Perioral shaping separated an oral-contact Y/Z coordinate; retain the original closed contact.')
    if any(not math.isfinite(c) for point in after for c in point):
        raise ValueError('Perioral shaping produced nonfinite coordinates; retain the unmodified native mesh.')

    triangle_count = 0
    minimum_area_ratio = 1.0
    minimum_normal_dot = 1.0
    for face in native['faces']:
        if not changed.intersection(face):continue
        for j in range(1,len(face)-1):
            triangle = (face[0],face[j],face[j+1])
            old = _triangle_normal(before,triangle)
            new = _triangle_normal(after,triangle)
            old_length = math.sqrt(sum(c*c for c in old))
            new_length = math.sqrt(sum(c*c for c in new))
            if old_length <= 1e-12:
                raise ValueError(f'Baseline perioral triangle {triangle} is collapsed; investigate before reshaping it.')
            ratio = new_length/old_length
            cosine = sum(a*b for a,b in zip(old,new))/(old_length*new_length) if new_length else -1.0
            if ratio < .25 or cosine <= 0:
                raise ValueError(f'Perioral triangle {triangle} collapses or flips after shaping; area ratio {ratio:.6f}, normal dot {cosine:.6f}.')
            minimum_area_ratio = min(minimum_area_ratio,ratio)
            minimum_normal_dot = min(minimum_normal_dot,cosine)
            triangle_count += 1
    for i in changed:vertices[i][:] = after[i]
    return {'changed_vertices':len(changed),'retracted_target_rows':len(retracted),
            'widened_rows':len(width_rows),'target_rows':len(target),'contact_rows':len(contact),
            'contact_width_ratio':1.08,'contact_yz_exact':True,
            'crest_forward_span_before_m':crest_span*scale,
            'crest_forward_span_after_m':(after[466][2]-after[520][2])*scale,
            'maximum_displacement_m':maximum,'affected_source_triangles':triangle_count,
            'minimum_source_triangle_area_ratio':minimum_area_ratio,
            'minimum_source_triangle_normal_dot':minimum_normal_dot,
            'unchanged_outside_support_vertices':len(pinned),
            'bound':'Native hm08 body triangle fans and sparse target/contact adjacency only. Contact Y/Z and all rows outside support are exact; common linear X mapping preserves paired contacts. Does not certify subdivided lip contact, self-intersections, photographic proportions or likeness; fixed native portrait/profile/oblique review is still required.'}

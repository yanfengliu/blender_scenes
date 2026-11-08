"""Staged, bounded additions to the current adult facial expression.

Harness: prepare_human_base and natural_face supply the same native mesh for
pure preflight. Call after natural_face.shape_expression, before proxy fitting.
These source-coordinate bounds do not certify evaluated eyelids or likeness;
the saved-scene four-camera and reference review remain required.
"""
import hashlib
import math
from collections import defaultdict


TARGET_HASHES = {
    'l-eye-height2-incr.target': '8521b63c1bf07af06194e96e14eb522dce43615ef1139b8117f104f5132fbc69',
    'r-eye-height2-incr.target': '35e1f070ab8a77dc103aab81c478f04136f6afec378a7003d8834e49ff02d916',
    'l-cheek-volume-incr.target': 'edb0bf9389aa7fd00f9d735603729b687b3899e9a6df0934ca14aa4d44574e27',
    'r-cheek-volume-incr.target': 'dfdde51eb34b3e2c70a4c0c9fe876339dd80ee6ec0fbb3f798e630af556f9695',
    'mouth-upperlip-volume-incr.target': 'b124cbd9b9be318264f61a143da603b42e0357ed92b4b6afd1b31a83daaf8568',
}

# Actual hm08 oral rim rows: central upper/lower contact is 520/523, with
# internal contact 537/540. The side rows join through the mouth corners.
# Their positive-X counterparts were checked against the native mirrored mesh,
# not inferred from a coordinate range on the already shaped face.
MOUTH_CONTACT = (
    446,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,
    531,532,533,534,535,536,537,538,539,540,3709,3730,5359,5360,7206,
    7261,7262,7263,7264,7265,7266,7267,7268,7269,7270,7271,7272,7273,
    7274,7275,7276,7277,7278,7279,7280,7281,7282,7283,10377,10398,11961,11962,
)
# Inner and outer eye-corner rows on the same native mesh.
EYE_CORNERS = {'l': (6847,6805), 'r': (63,21)}
# high-poly.mhclo uses these body vertices to scale its separate ocular helper.
EYE_PROXY_SCALE_ANCHORS = (5399,11998,962,5320,791,881)


def _smooth(low, high, value):
    t = max(0.0, min(1.0, (value-low)/(high-low)))
    return t*t*(3.0-2.0*t)


def _target(path, expected):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f'Gentle expression target {path.name} differs from the inspected hm08 asset; review its anatomy before using this bounded deformation.')
    return {int(parts[0]): tuple(float(n) for n in parts[1:4])
            for line in data.decode('utf-8').splitlines()
            if (parts := line.split()) and parts[0].isdigit()}


def apply_gentle_expression(native, scale=None):
    """Add a small upper-lid lift, upper-cheek response and central lip contour.

    All changes are vertical or forward. Upper lids are capped at 0.6 mm,
    cheeks at 0.7 mm up / 0.4 mm forward, and lip contour at 0.35 mm total.
    Mouth contact and two complete surrounding face rings remain unchanged.
    The existing adult macros and expression are inputs, not reapplied here.
    """
    from prepare_human_base import ASSETS, group_center

    vertices = native['vertices']
    if len(vertices) != 19158:
        raise ValueError(f'Gentle expression requires the inspected 19,158-vertex hm08 native mesh; received {len(vertices)} vertices.')
    before = [tuple(v) for v in vertices]
    if any(not all(math.isfinite(n) for n in v) for v in before):
        raise ValueError('Gentle expression received nonfinite native coordinates; repair the source geometry before applying expression.')
    body = set(native['groups']['body'])
    height = max(before[i][1] for i in body)-native['ground_y']
    scale = 1.65/height if scale is None else scale
    if not math.isfinite(scale) or not 1.64 <= height*scale <= 1.66:
        raise ValueError(f'Gentle expression is bounded to the current 1.65 m adult; supplied scale produces {height*scale:.6f} m.')
    adjacency = defaultdict(set)
    for face in native['faces']:
        for index in face:
            adjacency[index].update(face)
    protected = set(MOUTH_CONTACT)
    if not protected <= body or not {521,537} <= adjacency[520] or not {534,557} <= adjacency[540]:
        raise ValueError('Gentle expression oral-rim indices do not match the inspected hm08 face topology; preserve the original native index correspondence.')
    frontier = set(protected)
    for _ in range(2):
        frontier = {other for index in frontier for other in adjacency[index]}-protected
        protected.update(frontier)
    mouth_guard = set(protected)
    protected.update(EYE_PROXY_SCALE_ANCHORS)
    for pair in EYE_CORNERS.values():
        protected.update(pair)

    targets = {name: _target(ASSETS/name, digest) for name,digest in TARGET_HASHES.items()}
    deltas = [[0.0,0.0,0.0] for _ in vertices]
    regions = {'upper_lids': set(), 'upper_cheeks': set(), 'central_upper_lip': set()}
    lower_lids = set()
    for side in ('l','r'):
        eye = group_center(native, 'joint-'+side+'-eye')
        inner,outer = (before[i] for i in EYE_CORNERS[side])
        inner_x,outer_x = sorted((abs(inner[0]),abs(outer[0])))
        lid_target = targets[side+'-eye-height2-incr.target']
        # The negative lower-lid portion is never reapplied. Preserve its actual
        # socket rows as well as the positive target's unchanged eye corners.
        lower_lids.update(i for i,delta in lid_target.items()
                          if delta[1] <= 0 and before[i][1] >= eye[1]-.14)
        for index,delta in lid_target.items():
            if index not in body or index in protected or delta[1] <= 0:
                continue
            x,y,z = before[index]
            t = (abs(x)-inner_x)/(outer_x-inner_x)
            if not 0 < t < 1 or y <= eye[1]:
                continue
            taper = math.sin(math.pi*t)**2
            taper *= 1-_smooth(eye[1]+.08,eye[1]+.14,y)
            amount = .0006*min(1.0,delta[1]/.018)*taper
            if amount:
                deltas[index][1] += amount/scale
                regions['upper_lids'].add(index)
        # Existing cheek targets identify the cheek region only. Their lateral
        # volume deltas are not used: this is a small upward/forward response.
        for index in targets[side+'-cheek-volume-incr.target']:
            if index not in body or index in protected or index in lower_lids:
                continue
            x,y,z = before[index]
            below = eye[1]-y
            window = _smooth(.13,.18,below)*(1-_smooth(.34,.41,below))
            window *= _smooth(1.08,1.20,z)
            window *= 1-_smooth(.50,.58,abs(x))
            weight = window*math.exp(-((abs(x)-abs(eye[0])*1.30)/.15)**2-((below-.23)/.115)**2)
            if weight:
                deltas[index][1] += .0007*weight/scale
                deltas[index][2] += .0004*weight/scale
                regions['upper_cheeks'].add(index)

    lip_target = targets['mouth-upperlip-volume-incr.target']
    lip_center_y = before[466][1]  # Central upper vermilion crest, above contact.
    for index,delta in lip_target.items():
        if index not in body or index in protected:
            continue
        x,y,z = before[index]
        weight = (1-_smooth(.055,.115,abs(x)))*math.exp(-((y-lip_center_y)/.050)**2)
        length = math.hypot(delta[1],delta[2])
        if not length or not weight or z < before[520][2]+.015:
            continue
        amount = .00035*weight
        deltas[index][1] += amount*delta[1]/length/scale
        deltas[index][2] += amount*delta[2]/length/scale
        regions['central_upper_lip'].add(index)

    protected.update(lower_lids)
    changed = set().union(*regions.values())
    maximum = max(math.sqrt(sum(n*n for n in delta))*scale for delta in deltas)
    if maximum >= .0015 or any(any(deltas[i]) for i in protected):
        raise ValueError(f'Gentle expression exceeded its protected-point or <1.5 mm source displacement bound; measured maximum is {maximum:.7f} m.')
    for index in changed:
        vertices[index][1] += deltas[index][1]
        vertices[index][2] += deltas[index][2]
    return {
        'measurement_space': 'native source coordinates',
        'maximum_additional_displacement_m': maximum,
        'changed_vertices': len(changed),
        'mouth_contact_vertices': len(MOUTH_CONTACT),
        'mouth_with_two_face_rings_pinned': len(mouth_guard),
        'lower_lid_vertices_pinned': len(lower_lids),
        'region_counts': {name:len(ids) for name,ids in regions.items()},
        'region_maximum_displacement_m': {
            name:max((math.dist(before[i],vertices[i])*scale for i in ids),default=0.0)
            for name,ids in regions.items()},
        'bound': 'Current hm08 adult source coordinates only; mouth contact plus two face rings, lower socket rows, eye helpers and eye-proxy scales pinned. Evaluated subdivision, proxies, clearance, expression and reference likeness still require saved-scene review.',
    }

"""Bounded adult lower-cheek inset; source checks do not establish appearance."""
import math


def require(value, message):
    if not value:
        raise ValueError(message)


def apply_lower_cheek_inset(native):
    """Inset forward lower cheeks <=2.5 mm; retain chin, eyes and oral contact."""
    from gentle_expression import EYE_CORNERS, EYE_PROXY_SCALE_ANCHORS
    from reference_smile import trace_oral_strip
    from prepare_human_base import to_blender

    vertices = native['vertices']
    require(len(vertices) == 19158 and all(len(v) == 3 and all(math.isfinite(c) for c in v) for v in vertices),
            'Lower-cheek shaping requires the finite 19,158-row adult hm08 anatomy.')
    before = [tuple(v) for v in vertices]
    body = set(native['groups']['body'])
    require(body and body <= set(range(len(before))), 'Lower-cheek body indices are invalid.')
    height = max(before[i][1] for i in body)-native['ground_y']
    require(math.isfinite(height) and 14.9 < height < 15.0, 'Lower-cheek input left the inspected adult stature range.')
    scale = 1.65/height
    points = to_blender(before, native['ground_y'], scale)
    sections, _ = trace_oral_strip(native['faces'])
    oral = {i for pair in sections for i in pair}
    eyes = set(EYE_PROXY_SCALE_ANCHORS) | {i for pair in EYE_CORNERS.values() for i in pair}
    require(len(oral) == 76 and oral <= body and eyes <= body, 'Lower-cheek oral/ocular anatomy changed.')
    helpers = {i for name, rows in native['groups'].items() if name != 'body' for i in rows}

    def smooth(low, high, value):
        t = max(0., min(1., (value-low)/(high-low)))
        return t*t*t*(10.+t*(-15.+6.*t))

    def field(point):
        x, y, z = point
        return (.0025*smooth(.027, .050, abs(x))*smooth(1.43, 1.48, z)
                *(1.-smooth(1.50, 1.535, z))*smooth(.085, .105, -y))

    require(max(field(points[i]) for i in oral | eyes) == 0., 'Lower-cheek raw field reaches protected oral/ocular rows.')
    after = [list(v) for v in before]
    for i in body-helpers:
        after[i][0] -= math.copysign(field(points[i])/scale, before[i][0])
    changed = {i for i in range(len(before)) if tuple(after[i]) != before[i]}
    protected = (set(range(len(before)))-body) | helpers | oral | eyes
    protected |= {i for i in body if points[i][2] >= 1.535 or abs(points[i][0]) <= .027}
    require(changed and not changed & protected, 'Lower-cheek field is absent or moves protected anatomy.')
    maximum = max(math.dist(before[i], after[i])*scale for i in changed)
    require(maximum <= .002500000001 and all(tuple(after[i][1:]) == before[i][1:] for i in changed),
            'Lower-cheek field exceeds its 2.5 mm lateral-only bound.')
    require(all(all(math.isfinite(c) for c in v) for v in after), 'Lower-cheek field produced nonfinite coordinates.')
    for i in changed:
        vertices[i][:] = after[i]
    return {'changed_rows': len(changed), 'maximum_inset_m': maximum, 'oral_raw_field_zero': True,
            'bound': 'Source-only lower-cheek response; evaluated appearance and fit remain unverified.'}

"""Coherent upper-frame shaping in the final posed coordinate frame.

The existing native pose weights, fitting and joint landmarks keep their inputs.
Both finished skin and clothing use this same final mapping. It tapers
before the waist, hands and head, preserving the retained bust's forward shape.
This source map does not certify final clothing clearance or visual appeal.
"""
import math


SHOULDER_INSET_M = .022
SHOULDER_DROP_M = .004


def _smooth(low, high, value):
    t = max(0.0, min(1.0, (value-low)/(high-low)))
    return t*t*(3-2*t)


def upper_frame_point(point):
    """Narrow the shoulder/ribcage smoothly, with unchanged front projection."""
    x, y, z = point
    if not all(math.isfinite(v) for v in point):
        raise ValueError('Upper-frame shaping needs finite metre coordinates.')
    height = _smooth(1.10, 1.265, z)*(1-_smooth(1.36, 1.43, z))
    side = _smooth(.025, .165, abs(x))
    inset = SHOULDER_INSET_M*height*side
    slope = SHOULDER_DROP_M*side*_smooth(1.24, 1.30, z)*(1-_smooth(1.36, 1.43, z))
    return (x-math.copysign(inset, x), y, z-slope)


def finalize_upper_frame(objects):
    """Deform finished surfaces together, preserving the fitted collar outline.

    Fitting the helper again after narrowing changed the collar clipping contour
    into visible kinks. This final shared map retains the constructed topology,
    UVs, color bands and pose. Saved evaluated clearance still must be checked.
    """
    from mathutils import Vector
    report = {}
    for obj in objects:
        if obj.type not in {'MESH', 'CURVE'} or obj.data.users != 1:
            raise ValueError(f'Frame shaping needs unique mesh/curve data: {obj.name}')
        matrix, inverse = obj.matrix_world.copy(), obj.matrix_world.inverted()
        changed, maximum = 0, 0.0
        def mapped(co):
            nonlocal changed, maximum
            world = matrix @ co
            new = Vector(upper_frame_point(world))
            distance = (new-world).length
            if distance:
                changed += 1
                maximum = max(maximum, distance)
                return inverse @ new
            return co.copy()
        if obj.type == 'MESH':
            for vertex in obj.data.vertices:
                vertex.co = mapped(vertex.co)
            obj.data.update()
        else:
            for spline in obj.data.splines:
                if spline.type == 'BEZIER':
                    for point in spline.bezier_points:
                        co, left, right = (mapped(value) for value in (point.co, point.handle_left, point.handle_right))
                        point.co, point.handle_left, point.handle_right = co, left, right
                else:
                    for point in spline.points:
                        point.co = (*mapped(point.co.xyz), point.co.w)
        report[obj.name] = {'changed_controls': changed, 'maximum_displacement_m': maximum}
    return report

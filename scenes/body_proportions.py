"""Bounded proportion adjustment on the existing adult body and garment helper.

Harness: prepare_human_base reads the complete native topology; pure section
measurements below verify the deformation, not evaluated clothing clearance.
The head/neck, hands/feet, joint helpers, topology and UVs remain unchanged.
The saved unculled-body comparison and native views own fit/visual acceptance.
"""
from contextlib import contextmanager
import math


def _smooth(a, b, value):
    t = max(0.0, min(1.0, (value-a)/(b-a)))
    return t*t*(3-2*t)


def _window(value, low, first, last, high):
    return _smooth(low, first, value)*(1-_smooth(last, high, value))


def section_measurements(points, faces, heights=(.90, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20)):
    """Torso source-edge intersections, restricted to |x|<.18 m.

    These are width/depth sections, not circumferences or clothed silhouettes.
    The bound excludes arms at the chosen waist/hip levels; upper chest sections
    can contain arms and are deliberately not reported as chest circumference.
    """
    rows = []
    for z in heights:
        hits = []
        for face in faces:
            for a, b in zip(face, face[1:]+face[:1]):
                pa, pb = points[a], points[b]
                if (pa[2] <= z < pb[2]) or (pb[2] <= z < pa[2]):
                    t = (z-pa[2])/(pb[2]-pa[2])
                    point = tuple(pa[k]+t*(pb[k]-pa[k]) for k in range(3))
                    if abs(point[0]) < .18:
                        hits.append(point)
        if not hits:
            raise ValueError(f'Body section at {z:.3f} m has no source-edge intersections; measurement did not run.')
        rows.append({'height_m': z, 'width_m': max(p[0] for p in hits)-min(p[0] for p in hits),
                     'depth_m': max(p[1] for p in hits)-min(p[1] for p in hits),
                     'front_y_m': min(p[1] for p in hits), 'edge_samples': len(hits)})
    return rows


def apply_body_proportions(native):
    """Change body/helper shape in place before posing; retain native indices.

    Torso sections: waist -7%, hips -2.5%; upper-arm/thigh radial thickness -4.5%.
    Existing breast surfaces receive a broad <=18 mm forward field and <=3 mm
    lateral field per side. These caps describe displacement, not a cup size.
    """
    from prepare_human_base import group_center, to_blender

    before = [list(p) for p in native['vertices']]
    height = max(before[i][1] for i in native['groups']['body'])-native['ground_y']
    scale = 1.65/height
    points = to_blender(before, native['ground_y'], scale)
    joint_ids = {i for name, ids in native['groups'].items() if name.startswith('joint-') for i in ids}
    protected = {i for i, p in enumerate(points) if p[2] >= 1.30 or p[2] <= .45 or abs(p[0]) >= .36} | joint_ids

    def joint(side, name):
        return to_blender([group_center(native, f'joint-{side}-{name}')], native['ground_y'], scale)[0]

    limbs = []
    for side in ('l', 'r'):
        limbs.extend(((joint(side, 'shoulder'), joint(side, 'elbow'), .085, 'upper_arm'),
                      (joint(side, 'upper-leg'), joint(side, 'knee'), .135, 'thigh')))

    def shape(point):
        x, y, z = point
        # Torso taper fades before the arm field and leaves the shoulder intact.
        torso = 1-_smooth(.175, .225, abs(x))
        waist = .07*_window(z, .92, 1.035, 1.105, 1.20)
        hip = .025*_window(z, .79, .87, .92, .99)
        # Their overlap stays below .07; addition is smooth where windows cross.
        reduction = (waist+hip)*torso
        result = [x*(1-reduction), -.05+(y+.05)*(1-reduction), z]
        # Smooth radial contraction around fixed anatomical bone axes.
        for start, end, radius, kind in limbs:
            if x*start[0] <= 0:
                continue
            if kind == 'upper_arm' and abs(x) <= .175:
                continue
            axis = [end[k]-start[k] for k in range(3)]
            length2 = sum(v*v for v in axis)
            t = sum((point[k]-start[k])*axis[k] for k in range(3))/length2
            centre = [start[k]+t*axis[k] for k in range(3)]
            radial = [point[k]-centre[k] for k in range(3)]
            distance = math.sqrt(sum(v*v for v in radial))
            weight = _window(t, .02, .17, .80, 1.0)*(1-_smooth(radius*.8, radius, distance))
            if kind == 'upper_arm':
                weight *= _smooth(.175, .205, abs(x))
            for k in range(3):
                result[k] -= .045*weight*radial[k]
        # The two broad lobes displace existing tissue and its helper shell;
        # they never introduce separate spheres, a new seam or front texture.
        front = _smooth(.035, .075, -(y+.05))
        breast = 0.0
        for centre_x in (-.077, .077):
            radius2 = ((x-centre_x)/.078)**2+((z-1.205)/.087)**2
            breast += max(0.0, 1-radius2)**2
        breast = min(1.0, breast)*front*_window(z, 1.115, 1.15, 1.255, 1.295)
        result[1] -= .018*breast
        result[0] += math.copysign(.003*breast*_smooth(0, .025, abs(x)), x)
        # Fade the whole field before exact pinned boundaries. A point just
        # below the protected shoulder/outer-arm limits must not jump at them.
        fade = (1-_smooth(1.265, 1.30, z))*(1-_smooth(.33, .36, abs(x)))
        fade *= _smooth(.45, .48, z)
        result = [point[k]+fade*(result[k]-point[k]) for k in range(3)]
        return result, breast*fade

    after = []
    max_breast_forward = max_breast_lateral = 0.0
    for i, point in enumerate(points):
        if i in protected:
            after.append(point)
            continue
        result, breast = shape(point)
        after.append(tuple(result))
        max_breast_forward = max(max_breast_forward, .018*breast)
        max_breast_lateral = max(max_breast_lateral, .003*breast)
    # Preserve untouched native bytes exactly rather than round-tripping them.
    for i, (old, new) in enumerate(zip(points, after)):
        if old != new:
            native['vertices'][i] = [new[0]/scale, new[2]/scale+native['ground_y'], -new[1]/scale]
    assert all(native['vertices'][i] == before[i] for i in protected), 'Protected anatomy moved during proportion adjustment.'
    assert max_breast_forward <= .018000001 and max_breast_lateral <= .003000001
    assert all(math.isfinite(v) for p in native['vertices'] for v in p)
    assert max(native['vertices'][i][1] for i in native['groups']['body'])-native['ground_y'] == height
    # Garment cropping uses baseline face identities, so a narrowed sleeve does
    # not silently change which helper quads make its four opening loops.
    native['proportions_baseline_vertices'] = before
    native['body_proportions'] = {'waist_reduction': .07, 'hip_reduction': .025,
                                 'limb_radial_reduction': .045, 'bust_forward_cap_m': .018,
                                 'bust_lateral_cap_m': .003, 'skirt_hem_scale': .975}
    diagnostics = {'native_vertices': len(before), 'changed_vertices': sum(a != b for a, b in zip(before, native['vertices'])),
                   'protected_vertices': len(protected), 'protected_vertices_unchanged': True,
                   'stature_m': 1.65, 'maximum_breast_forward_field_m': max_breast_forward,
                   'maximum_breast_lateral_field_m': max_breast_lateral,
                   'before_sections': section_measurements(points, native['faces']),
                   'after_sections': section_measurements(after, native['faces']),
                   'bound': 'Pre-pose source geometry and complete native helpers; topology/UVs untouched. Source field caps and named torso sections do not prove final fitted garment clearance or visual acceptance.'}
    return diagnostics


@contextmanager
def full_body_support(native, posed):
    """Temporary unculled anatomical support with the skin's two-level surface.

    Its full canonical body faces include the torso hidden by visible-skin culls.
    It is deleted before saving/rendering and never substitutes an image plane.
    """
    import bpy
    data = bpy.data.meshes.new('Temporary unculled adult fit surface')
    obj = None
    try:
        data.from_pydata(posed, [], native['faces'])
        data.update()
        obj = bpy.data.objects.new(data.name, data)
        bpy.context.scene.collection.objects.link(obj)
        obj.hide_render = True
        modifier = obj.modifiers.new('Same anatomical subdivision as visible skin', 'SUBSURF')
        modifier.levels = modifier.render_levels = 2
        bpy.context.view_layer.update()
        yield obj
    finally:
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(data)

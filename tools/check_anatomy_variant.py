"""Actual continuous-surface checks for the requested adult anatomy changes."""
import math


def _normal(points, tri):
    a, b, c = [points[i] for i in tri]
    u = [b[k]-a[k] for k in range(3)]
    v = [c[k]-a[k] for k in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def geometry_metrics(before, after, faces):
    assert len(before) == len(after) and len(before) > 200000
    assert all(all(math.isfinite(c) for c in p) for p in after), 'Nonfinite anatomical surface.'
    changed = {i for i, (a, b) in enumerate(zip(before, after)) if a != b}
    chest = {i for i, (x, y, z) in enumerate(before) if 1.09 < z < 1.325 and abs(x) < .19 and y < -.06}
    pelvis = {i for i, (x, y, z) in enumerate(before) if .755 < z < .852 and abs(x) < .044 and y < -.045}
    outside = changed-chest-pelvis
    ratios, normal_dots = [], []
    for face in faces:
        if not changed.intersection(face):
            continue
        for k in range(1, len(face)-1):
            tri = (face[0], face[k], face[k+1])
            a, b = _normal(before, tri), _normal(after, tri)
            al, bl = math.sqrt(sum(c*c for c in a)), math.sqrt(sum(c*c for c in b))
            assert al > 1e-14 and bl > 1e-14, 'Collapsed anatomical triangle.'
            ratios.append(bl/al)
            normal_dots.append(sum(u*v for u, v in zip(a, b))/(al*bl))
    nipple = {}
    for side in (-1, 1):
        core, ring = [], []
        for i in chest:
            x, y, z = before[i]
            if side*x <= 0 or y >= -.160:
                continue
            radial = math.hypot(.81*(abs(x)-.1000)+.58*(y+.1774), z-1.2035)
            movement = .58*side*(after[i][0]-x)-.81*(after[i][1]-y)
            if radial < .0018:
                core.append(movement)
            elif .007 < radial < .011:
                ring.append(movement)
        assert core and ring, 'Nipple relief measurement missed its actual surface populations.'
        nipple[str(side)] = {'core_samples':len(core), 'ring_samples':len(ring),
                             'additional_relief_m':sum(core)/len(core)-sum(ring)/len(ring)}
    return {'changed_vertices':len(changed), 'outside_regions_changed':len(outside),
            'protected_vertices_exact':len(before)-len(chest|pelvis),
            'chest_vertices_changed':len(changed&chest), 'pelvis_vertices_changed':len(changed&pelvis),
            'maximum_displacement_m':max((math.dist(before[i],after[i]) for i in changed), default=0.),
            'maximum_chest_forward_m':max((before[i][1]-after[i][1] for i in chest), default=0.),
            'pelvis_outward_relief_m':max((before[i][1]-after[i][1] for i in pelvis), default=0.),
            'pelvis_inward_cleft_m':max((after[i][1]-before[i][1] for i in pelvis), default=0.),
            'nipple_relief':nipple, 'minimum_triangle_area_ratio':min(ratios,default=1.),
            'maximum_triangle_area_ratio':max(ratios,default=1.),
            'minimum_triangle_normal_dot':min(normal_dots,default=1.), 'checked_triangles':len(ratios)}


def accept_geometry(report):
    assert report['outside_regions_changed'] == 0, 'Anatomy edit moved protected face, limbs or torso.'
    assert 0.030 < report['maximum_chest_forward_m'] < .050, 'Chest volume response missing or excessive.'
    assert report['maximum_displacement_m'] < .050, 'Anatomy displacement exceeds its inspected bound.'
    assert report['chest_vertices_changed'] > 1000 and report['pelvis_vertices_changed'] > 300, 'Anatomy response is absent.'
    assert .0015 < report['pelvis_outward_relief_m'] < .007, 'External fold relief missing or excessive.'
    assert .001 < report['pelvis_inward_cleft_m'] < .005, 'External cleft missing or excessive.'
    assert all(row['additional_relief_m'] > .0008 for row in report['nipple_relief'].values()), 'Nipple relief is not more defined.'
    assert report['minimum_triangle_area_ratio'] > .20 and report['maximum_triangle_area_ratio'] < 5., 'Anatomy surface triangle changed excessively.'
    assert report['minimum_triangle_normal_dot'] > .35, 'Anatomy surface folded or reversed.'


def negative_checks(before, after, faces):
    results = {}
    for name, points in [('no_anatomy_change', before), ('remote_head_change', list(after))]:
        if name == 'remote_head_change':
            index = next(i for i, p in enumerate(before) if p[2] > 1.55)
            point = list(points[index]); point[0] += .001; points[index] = tuple(point)
        try:
            accept_geometry(geometry_metrics(before, points, faces))
        except AssertionError as error:
            results[name] = str(error)
        else:
            raise AssertionError('Anatomy negative control passed: '+name)
    return results


def local_surface_intersections(before, after, faces):
    """Actual triangle intersections, excluding pairs sharing a mesh vertex."""
    from mathutils.bvhtree import BVHTree
    report = {}
    for name, low, high in [('chest',1.07,1.34), ('pelvis',.72,.88)]:
        triangles = []
        for face in faces:
            if not any(low < before[i][2] < high and abs(before[i][0]) < .22 for i in face):
                continue
            triangles.extend((face[0],face[k],face[k+1]) for k in range(1,len(face)-1))
        collisions = []
        for points in (before, after):
            tree = BVHTree.FromPolygons(points, triangles, all_triangles=True)
            pairs = {tuple(sorted((a,b))) for a,b in tree.overlap(tree)
                     if a != b and not set(triangles[a]).intersection(triangles[b])}
            collisions.append(pairs)
        introduced = collisions[1]-collisions[0]
        retained_vertices = {i for a,b in collisions[1]&collisions[0] for t in (a,b) for i in triangles[t]}
        baseline_exact = all(before[i] == after[i] for i in retained_vertices)
        report[name] = {'triangles':len(triangles), 'baseline_pairs':len(collisions[0]),
                        'after_pairs':len(collisions[1]), 'introduced_pairs':len(introduced),
                        'surviving_baseline_collision_vertices_exact':baseline_exact}
        assert not introduced, 'Anatomy change introduced disjoint-triangle intersections in '+name
        assert baseline_exact, 'Anatomy change altered an already-intersecting surface in '+name
    return report

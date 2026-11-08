"""Bounded source-quad feedback from the actual thickened blouse to full skin.

Harness: body_proportions.full_body_support supplies unculled Subsurf2 anatomy.
The independent saved fit probe checks both actual shell layers afterward.
This solver requires verified FACE parent propagation and exact Solidify layers;
unknown correspondence fails. It never chooses controls by spatial proximity.
"""
from collections import Counter
import math


def _cycle(indices):
    indices = tuple(indices)
    return min(indices[i:]+indices[:i] for i in range(len(indices)))


def _evaluated_with_parents(obj, attribute):
    """Return the complete shell and its verified original-quad correspondence."""
    import bpy
    from mathutils import Vector
    source_count = len(obj.data.polygons)
    solid = [m for m in obj.modifiers if m.type == 'SOLIDIFY']
    assert len(solid) == 1 and solid[0] == obj.modifiers[-1]
    solid = solid[0]
    assert solid.show_viewport and abs(solid.offset-1) < 1e-8 and abs(solid.thickness-.0013) < 1e-8
    evaluated = None
    try:
        solid.show_viewport = False
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        evaluated = obj.evaluated_get(graph)
        mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=graph)
        points = [v.co.copy() for v in mesh.vertices]
        faces = [tuple(p.vertices) for p in mesh.polygons]
        propagated = mesh.attributes.get(attribute)
        assert propagated is not None and propagated.domain == 'FACE', 'Subsurf discarded the original-quad FACE attribute; no nearest-control fallback is allowed.'
        parents = [d.value for d in propagated.data]
        assert len(parents) == len(faces) and Counter(parents) == Counter({i:16 for i in range(source_count)}), 'Subsurf2 parent population is not exactly16 children per original quad.'
    finally:
        if evaluated is not None:
            evaluated.to_mesh_clear()
        solid.show_viewport = True
        bpy.context.view_layer.update()
    forward = {_cycle(face): i for i,face in enumerate(faces)}
    assert len(forward) == len(faces), 'Evaluated source face cycles are not unique.'
    edge_faces = {}
    for index, face in enumerate(faces):
        for edge in zip(face, face[1:]+face[:1]):
            edge_faces.setdefault(tuple(sorted(edge)), []).append(index)
    boundary = {edge:ids[0] for edge,ids in edge_faces.items() if len(ids) == 1}
    assert all(len(ids) in (1,2) for ids in edge_faces.values())
    evaluated = None
    try:
        graph = bpy.context.evaluated_depsgraph_get()
        evaluated = obj.evaluated_get(graph)
        mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=graph)
        mesh.calc_loop_triangles()
        shell_points = [v.co.copy() for v in mesh.vertices]
        count = len(points)
        assert len(shell_points) == 2*count, 'Solidify vertex population is not two complete layers.'
        matching = [offset for offset in (0,count) if max((shell_points[offset+i]-point).length for i,point in enumerate(points)) < 1e-6]
        assert len(matching) == 1, 'Solidify inner layer does not uniquely match every unshifted base coordinate.'
        inner = matching[0];outer = count-inner
        propagated = mesh.attributes.get(attribute)
        assert propagated is not None and len(propagated.data) == len(mesh.polygons)
        parent_faces = [];inner_seen = Counter();outer_seen = Counter();rim_seen = Counter()
        for polygon in mesh.polygons:
            ids = tuple(polygon.vertices)
            if all(outer <= i < outer+count for i in ids):
                child = forward.get(_cycle(tuple(i-outer for i in ids)))
                assert child is not None, 'An outer face has no exact forward source cycle.'
                outer_seen[child] += 1
                parent = parents[child]
                assert propagated.data[polygon.index].value == parent
            elif all(inner <= i < inner+count for i in ids):
                child = forward.get(_cycle(tuple(reversed(tuple(i-inner for i in ids)))))
                assert child is not None, 'An inner face has no exact reversed source cycle.'
                inner_seen[child] += 1
                parent = parents[child]
                assert propagated.data[polygon.index].value == parent
            else:
                mapped = tuple(sorted(set(i % count for i in ids)))
                assert len(ids) == 4 and mapped in boundary, 'Rim source correspondence is unknown.'
                assert set(ids) == {v+offset for v in mapped for offset in (inner,outer)}
                rim_seen[mapped] += 1
                # Rims inherit only the original quad adjacent to this exact
                # subdivided boundary edge, never an opposite spatial wall.
                parent = parents[boundary[mapped]]
            parent_faces.append(parent)
        expected = Counter({i:1 for i in range(len(faces))})
        assert inner_seen == expected and outer_seen == expected
        assert rim_seen == Counter({edge:1 for edge in boundary})
        triangles = [tuple(t.vertices) for t in mesh.loop_triangles]
        triangle_parents = [parent_faces[t.polygon_index] for t in mesh.loop_triangles]
        evidence = {'original_quads':source_count,'subsurf_quads':len(faces),'children_per_original_quad':16,
                    'inner_quads':sum(inner_seen.values()),'outer_quads':sum(outer_seen.values()),
                    'rim_quads':sum(rim_seen.values()),'whole_shell_triangles':len(triangles)}
        return shell_points, triangles, triangle_parents, evidence
    finally:
        if evaluated is not None:
            evaluated.to_mesh_clear()


def fit_evaluated_blouse(blouse, full_body):
    """Up to8 local source-quad corrections; <=20mm cumulative movement.

    Final success requires >=0.2mm signed sampled gap and zero shell/body BVH
    triangle overlaps, including both layers and rims. Samples include every
    triangle vertex, centroid and edge midpoint. This is not comfort or likeness.
    """
    import bpy
    from mathutils import Matrix, Vector
    from mathutils.bvhtree import BVHTree
    from fitted_blouse import _topology
    assert blouse.matrix_world == Matrix.Identity(4) and full_body.matrix_world == Matrix.Identity(4), 'This fit requires baked world-space mesh coordinates and identity object transforms.'
    before = [v.co.copy() for v in blouse.data.vertices]
    faces = [tuple(p.vertices) for p in blouse.data.polygons]
    loops,_,adjacency = _topology([tuple(p) for p in before],faces)
    neck = max(loops,key=lambda loop:sum(before[i].z for i in loop)/len(loop))
    pinned = set(neck);frontier = set(neck)
    for _ in range(2):
        frontier = {j for i in frontier for j in adjacency[i]}-pinned
        pinned.update(frontier)
    attribute = 'Temporary fit original quad'
    assert blouse.data.attributes.get(attribute) is None
    original_ids = blouse.data.attributes.new(attribute,'INT','FACE')
    for i,item in enumerate(original_ids.data):item.value = i
    history = []
    body_tree = BVHTree.FromObject(full_body,bpy.context.evaluated_depsgraph_get())
    try:
        for step in range(9):
            blouse.data.update();bpy.context.view_layer.update()
            points,triangles,parents,population = _evaluated_with_parents(blouse,attribute)
            shell_tree = BVHTree.FromPolygons(points,triangles,all_triangles=True)
            pairs = shell_tree.overlap(body_tree)
            touching = {pair[0] for pair in pairs}
            correction = {};minimum = math.inf;worst = None;sample_count = 0
            for index,(ia,ib,ic) in enumerate(triangles):
                a,b,c = points[ia],points[ib],points[ic]
                samples = (a,b,c,(a+b+c)/3,(a+b)/2,(b+c)/2,(c+a)/2)
                triangle_worst = None
                for point in samples:
                    location,normal,body_face,distance = body_tree.find_nearest(point)
                    assert location is not None
                    gap = (point-location).dot(normal);sample_count += 1
                    if gap < minimum:
                        minimum = gap;worst = {'point_m':list(point),'body_triangle':body_face,'signed_gap_m':gap,'source_quad':parents[index]}
                    if triangle_worst is None or gap < triangle_worst[0]:
                        triangle_worst = (gap,normal)
                gap,normal = triangle_worst
                if gap < .0002 or index in touching:
                    amount = max(.0015 if index in touching else 0.0,.002-gap)
                    vector = normal*amount;parent = parents[index]
                    if parent not in correction or vector.length > correction[parent].length:
                        correction[parent] = vector
            entry = {'step':step,'minimum_sampled_gap_m':minimum,'sample_count':sample_count,
                     'triangle_overlap_pairs':len(pairs),'overlapping_shell_triangles':len(touching),
                     'worst_sample':worst,'population':population}
            history.append(entry)
            print({'full_body_blouse_fit':entry},flush=True)
            if minimum >= .0002 and not pairs:
                assert all(blouse.data.vertices[i].co == before[i] for i in pinned)
                return {'status':'pass','history':history,'pinned_neckline_controls':len(pinned),
                        'maximum_source_correction_m':max((v.co-before[i]).length for i,v in enumerate(blouse.data.vertices)),
                        'bound':'Verified16-child original-quad correspondence, complete inner/outer/rim shell; no spatial control lookup. Source correction<=20mm; all7samples per actual triangle gap>=.2mm and zero shell/body overlap pairs. Independent saved fit/visual review required.'}
            if step == 8:
                raise RuntimeError(f'Full-body blouse fitting did not clear after8 corrections: gap {minimum:.6f}m, {len(pairs)} overlap pairs; worst {worst}. Preserve this evidence; do not cull skin or loosen the gate.')
            moves = [Vector() for _ in before];weights = [0 for _ in before]
            for parent,vector in correction.items():
                free = [i for i in faces[parent] if i not in pinned]
                if not free:
                    raise RuntimeError(f'Full-body fit needs to move pinned neckline quad {parent}; inspect the existing support fit.')
                for i in free:
                    moves[i] += vector*(4/len(free));weights[i] += 1
            for i,(move,weight) in enumerate(zip(moves,weights)):
                if not weight:continue
                candidate = blouse.data.vertices[i].co+move/weight
                if (candidate-before[i]).length > .020:
                    raise RuntimeError(f'Full-body blouse source control {i} needs more than20mm correction; inspect the fit geometry, not the limit.')
                blouse.data.vertices[i].co = candidate
    finally:
        blouse.data.attributes.remove(original_ids)
        blouse.data.update()

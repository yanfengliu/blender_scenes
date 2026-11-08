"""Topology-aware front-surface checks for the two UV-derived brow disks."""
import math
from collections import Counter,defaultdict


def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def intersect(a,b,c,d):
    if any(max(min(a[k],b[k]),min(c[k],d[k]))>min(max(a[k],b[k]),max(c[k],d[k])) for k in range(2)):return False
    return cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0


def projected_disks(surface):
    points=[(p[0],p[2]) for p in surface['points']];faces=surface['faces'];triangles=surface['triangles']
    assert all(all(math.isfinite(x) for x in p) for p in points)
    areas=[cross(*(points[i] for i in t)) for t in triangles]
    assert all(a>0 for a in areas),'Folded or degenerate front-projected brow triangle.'
    incidence=defaultdict(list);adjacency=defaultdict(set)
    for pi,face in enumerate(faces):
        for a,b in zip(face,face[1:]+face[:1]):
            incidence[tuple(sorted((a,b)))].append((a,b));adjacency[a].add(b);adjacency[b].add(a)
    assert all(len(v) in (1,2) for v in incidence.values())
    assert all(v[0]==v[1][::-1] for v in incidence.values() if len(v)==2),'Inconsistent edge winding.'
    remaining=set(adjacency);components=[]
    while remaining:
        visited={next(iter(remaining))};front=set(visited)
        while front:
            front={j for i in front for j in adjacency[i]}-visited;visited.update(front)
        remaining-=visited;components.append(visited)
    assert len(components)==2 and sum(map(len,components))==len(points)
    following={}
    for pairs in incidence.values():
        if len(pairs)==1:
            a,b=pairs[0];assert a not in following;following[a]=b
    assert set(following)==set(following.values())
    unseen=set(following);cycles=[]
    while unseen:
        first=next(iter(unseen));cycle=[];i=first
        while i not in cycle:
            cycle.append(i);unseen.remove(i);i=following[i]
        assert i==first;cycles.append(cycle)
    assert len(cycles)==2
    for component in components:
        edges=sum(a in component for a,b in incidence);polys=sum(face[0] in component for face in faces)
        assert len(component)-edges+polys==1
        assert sum(set(cycle)<=component for cycle in cycles)==1
    for cycle in cycles:
        edges=list(zip(cycle,cycle[1:]+cycle[:1]))
        for i,(a,b) in enumerate(edges):
            for c,d in edges[i+1:]:
                if {a,b}&{c,d}:continue
                assert not intersect(points[a],points[b],points[c],points[d]),'Front-projected boundary crosses itself.'
    assert max(points[i][0] for i in components[0])<min(points[i][0] for i in components[1]) or max(points[i][0] for i in components[1])<min(points[i][0] for i in components[0])
    return {'components':2,'disk_euler_characteristics':[1,1],'simple_boundary_lengths':[len(c) for c in cycles],
            'positive_projected_triangles':len(areas),'minimum_signed_double_area_m2':min(areas),'consistent_edge_winding':True}

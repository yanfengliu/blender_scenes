"""Conservative whole-triangle separation from an unsigned distance query."""
import math


def triangle_clearance(triangle,query,*,reserve=1e-7,max_depth=12,max_nodes=4095):
    """A query returns distance and its coordinate-quantization error in metres.

    Every triangle point lies within the maximum vertex radius about its
    centroid. Unsigned distance is 1-Lipschitz. This proves separation only;
    the caller must separately establish the exterior side.
    """
    assert len(triangle)==3 and all(len(p)==3 and all(math.isfinite(x) for x in p) for p in triangle)
    assert reserve>0 and max_depth>=0 and max_nodes>0
    queue=[(tuple(tuple(p) for p in triangle),0)];nodes=leaves=deepest=0;minimum=math.inf
    while queue:
        if nodes>=max_nodes:return {'pass':False,'reason':'node_budget','nodes':nodes,'leaves':leaves}
        (a,b,c),depth=queue.pop();nodes+=1;deepest=max(deepest,depth)
        center=tuple((a[k]+b[k]+c[k])/3 for k in range(3));radius=max(math.dist(p,center) for p in (a,b,c))
        distance,quantization=query(center)
        assert math.isfinite(distance) and distance>=0 and math.isfinite(quantization) and quantization>=0
        bound=distance-quantization-radius-reserve
        if bound>0:minimum=min(minimum,bound);leaves+=1;continue
        if depth>=max_depth:return {'pass':False,'reason':'depth_budget','nodes':nodes,'leaves':leaves,'center':center,'distance_m':distance,'radius_m':radius,'bound_m':bound}
        ab=tuple((x+y)*.5 for x,y in zip(a,b));bc=tuple((x+y)*.5 for x,y in zip(b,c));ca=tuple((x+y)*.5 for x,y in zip(c,a))
        queue.extend((((a,ab,ca),depth+1),((ab,b,bc),depth+1),((ca,bc,c),depth+1),((ab,bc,ca),depth+1)))
    return {'pass':True,'nodes':nodes,'leaves':leaves,'maximum_depth':deepest,'minimum_clearance_lower_m':minimum}


def controls():
    plane=lambda p:(abs(p[2]),0.)
    clear=((-0.002,0,.0004),(.002,0,.0004),(0,.002,.0004))
    assert triangle_clearance(clear,plane)['pass']
    assert not triangle_clearance(clear,plane,max_depth=0)['pass']
    assert not triangle_clearance(clear,plane,max_nodes=1)['pass']
    assert not triangle_clearance(((0,0,.001),(1,0,-.001),(0,1,.001)),plane)['pass']
    assert not triangle_clearance(((0,0,0),(1,0,.001),(0,1,.001)),plane)['pass']
    assert not triangle_clearance(((0,0,1e-8),(1e-6,0,1e-8),(0,1e-6,1e-8)),plane)['pass']
    # Unsigned clearance can accept an interior triangle: caller exterior checks
    # are mandatory, and this control deliberately preserves that limitation.
    assert triangle_clearance(tuple((x,y,-z) for x,y,z in clear),plane)['pass']
    assert not triangle_clearance(clear,lambda p:(abs(p[2]),.0005))['pass']
    return {'controls':8,'scope':'clear, unresolved depth/nodes, crossing, touching, near-reserve, interior limitation, query rounding'}

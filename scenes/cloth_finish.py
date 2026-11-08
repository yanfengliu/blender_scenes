"""Small cotton folds and sewn details for the existing connected blouse.

Harness: fitted_blouse._prepare_blouse and _topology expose pure source checks;
tools/build_sailor_character.py owns evaluated support and rendered inspection.
The drape keeps the mesh topology, opening support rows and collar neighborhood.
It is a bounded static deformation, not a cloth simulation.
"""
import heapq
import math
from collections import defaultdict


def _add(a,b):return tuple(x+y for x,y in zip(a,b))
def _sub(a,b):return tuple(x-y for x,y in zip(a,b))
def _mul(a,s):return tuple(x*s for x in a)
def _dot(a,b):return sum(x*y for x,y in zip(a,b))
def _cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def _unit(a):return _mul(a,1/max(1e-12,math.sqrt(_dot(a,a))))


def _smooth(low,high,value):
    t=max(0.0,min(1.0,(value-low)/(high-low)))
    return t*t*(3-2*t)


def _normals(points,faces):
    result=[(0.0,0.0,0.0) for _ in points]
    for face in faces:
        a,b,c=(points[i] for i in face[:3]);normal=_cross(_sub(b,a),_sub(c,a))
        for index in face:result[index]=_add(result[index],normal)
    return [_unit(normal) for normal in result]


def _protected(points,faces):
    from fitted_blouse import _topology
    from fitted_collar import _lower_bound,_inner_bound
    loops,_,edges=_topology(points,faces)
    face_neighbors=defaultdict(set)
    for face in faces:
        for index in face:face_neighbors[index].update(face)
    openings={index for loop in loops for index in loop};frontier=set(openings)
    # The boundary, its 1.7 mm support row and the original 6 mm support row.
    for _ in range(2):
        frontier={j for i in frontier for j in edges[i]}-openings;openings.update(frontier)
    collar={i for i,p in enumerate(points) if abs(p[0])<.170 and _lower_bound(p)-.015<p[2]<_inner_bound(p)+.020}
    frontier=set(collar)
    # Preserve complete source face neighborhoods around the actual clipping
    # fields, including the support used by the two-level blouse subdivision.
    for _ in range(2):
        frontier={j for i in frontier for j in face_neighbors[i]}-collar;collar.update(frontier)
    return openings,collar,edges


def apply_blouse_drape(points,faces):
    """Return posed points with deterministic outward folds capped at 2 mm.

    Call after the existing neckline fit and before creating the Blender mesh.
    Opening support rows and collar support neighborhoods remain exactly fixed.
    The cap and source topology do not certify evaluated body clearance.
    """
    from fitted_blouse import _topology
    before=[tuple(p) for p in points]
    if any(not all(math.isfinite(v) for v in p) for p in before):
        raise ValueError('Cotton drape needs finite posed blouse points before applying its 2 mm outward folds.')
    openings,collar,edges=_protected(before,faces);pinned=openings|collar
    distance=[float('inf') for _ in before];queue=[]
    for i in pinned:distance[i]=0.0;heapq.heappush(queue,(0.0,i))
    while queue:
        value,index=heapq.heappop(queue)
        if value!=distance[index]:continue
        for other in edges[index]:
            candidate=value+math.dist(before[index],before[other])
            if candidate<distance[other]:distance[other]=candidate;heapq.heappush(queue,(candidate,other))
    normals=_normals(before,faces);result=list(before);changed=[]
    for i,(x,y,z) in enumerate(before):
        if i in pinned:continue
        front=1-_smooth(-.070,-.025,y)
        lower=0.0
        for centre,slope,height,width,amount in ((-.091,-.22,1.087,.052,.0017),(.024,.16,1.085,.057,.0018),(.116,-.12,1.122,.039,.0013)):
            line=centre+slope*(z-height)
            lower+=amount*math.exp(-((x-line)/.0105)**2-((z-height)/width)**2)
        lateral=abs(x)
        underarm=.0018*math.exp(-((lateral-.198)/.037)**2-((z-(1.219-.48*(lateral-.18)))/.012)**2)
        underarm+=.0009*math.exp(-((lateral-.191)/.035)**2-((z-(1.194-.30*(lateral-.18)))/.014)**2)
        amount=min(.002,(front*lower+underarm)*_smooth(0,.022,distance[i]))
        if amount<1e-8:continue
        result[i]=_add(before[i],_mul(normals[i],amount));changed.append(i)
    _topology(result,faces)
    maximum=max((math.dist(a,b) for a,b in zip(before,result)),default=0.0)
    if maximum>.002000001 or any(result[i]!=before[i] for i in pinned):
        raise ValueError(f'Cotton drape exceeded its 2 mm or protected-support bound; maximum displacement is {maximum:.7f} m.')
    print({'cotton_drape':{'changed_vertices':len(changed),'opening_support_points_pinned':len(openings),
        'collar_support_points_pinned':len(collar),'maximum_outward_displacement_m':maximum,
        'bound':'Same source topology and exact opening/collar support neighborhoods; evaluated support and visual review remain required.'}})
    return result


def _mesh(name,vertices,faces,collection,material,thickness=.0007):
    import bpy
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
    for face in data.polygons:face.use_smooth=True
    obj=bpy.data.objects.new(name,data);collection.objects.link(obj);data.materials.append(material)
    if thickness:
        modifier=obj.modifiers.new('Folded cotton thickness','SOLIDIFY');modifier.thickness=thickness;modifier.offset=0
    return obj


def _stitch(name,points,collection,material,cyclic=False):
    import bpy
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=.00012;data.bevel_resolution=2
    spline=data.splines.new('POLY');spline.points.add(len(points)-1)
    spline.points.foreach_set('co',[v for p in points for v in (*p,1)])
    spline.use_cyclic_u=cyclic
    obj=bpy.data.objects.new(name,data);collection.objects.link(obj);data.materials.append(material)
    return obj


def _pocket_bounds(z):
    height=max(0,z-1.120);radius=.004
    inset=radius-math.sqrt(max(0,radius*radius-(radius-min(radius,height))**2))
    return .058+inset,.113-inset


def _pocket_gap(x,z):
    left,right=_pocket_bounds(z);u=max(0,min(1,(x-left)/(right-left)));v=max(0,min(1,(z-1.12)/.065))
    return .00065+.0014*math.sin(math.pi*u)**2*math.sin(math.pi*v)**2


def build_pocket_details(blouse,collection,ivory,seam):
    """Replace the old rectangular pocket with a shaped pocket and sewing cues.

    Return separate editable objects. Do not move blouse boundaries or rebuild
    its collar, sleeves or skirt. Every sampled detail uses evaluated support.
    """
    import bpy
    from mathutils import Vector
    from fitted_blouse import _topology
    bpy.context.view_layer.update()
    evaluated=blouse.evaluated_get(bpy.context.evaluated_depsgraph_get())
    transform=evaluated.matrix_world;inverse=transform.inverted()
    normal_transform=transform.to_3x3().inverted().transposed()
    def cast(origin,direction,gap,label):
        hit,point,normal,index=evaluated.ray_cast(inverse@Vector(origin),(inverse.to_3x3()@Vector(direction)).normalized())
        if not hit:raise ValueError(f'{label} has no evaluated blouse support at {tuple(round(v,5) for v in origin)} m; keep the sewn detail on the existing cotton shell.')
        return tuple(transform@point+(normal_transform@normal).normalized()*gap)
    def front(x,z,gap):return cast((x,-.5,z),(0,1,0),gap,'Pocket')
    objects=[];rows,columns=26,24;vertices=[]
    for i in range(rows+1):
        z=1.120+.065*i/rows;left,right=_pocket_bounds(z)
        for j in range(columns+1):
            x=left+(right-left)*j/columns;vertices.append(front(x,z,_pocket_gap(x,z)))
    faces=[(i*25+j,i*25+j+1,(i+1)*25+j+1,(i+1)*25+j) for i in range(rows) for j in range(columns)]
    objects.append(_mesh('Blouse / rounded sewn pocket with slight ease',vertices,faces,collection,ivory))
    vertices=[]
    for i in range(7):
        t=i/6;z=1.182+.003*t
        for j in range(columns+1):
            x=.058+.055*j/columns;vertices.append(front(x,z,.00115+.0006*math.sin(math.pi*t)))
    faces=[(i*25+j,i*25+j+1,(i+1)*25+j+1,(i+1)*25+j) for i in range(6) for j in range(columns)]
    objects.append(_mesh('Blouse / turned pocket top edge',vertices,faces,collection,ivory,.0004))
    path=[(.0595,1.1837-(1.1837-1.124)*j/28) for j in range(29)]
    path += [(.062+.0025*math.cos(math.pi+math.pi*.5*j/10),1.124+.0025*math.sin(math.pi+math.pi*.5*j/10)) for j in range(1,11)]
    path += [(.062+(.109-.062)*j/22,1.1215) for j in range(1,23)]
    path += [(.109+.0025*math.cos(1.5*math.pi+math.pi*.5*j/10),1.124+.0025*math.sin(1.5*math.pi+math.pi*.5*j/10)) for j in range(1,11)]
    path += [(.1115,1.124+(1.1837-1.124)*j/28) for j in range(1,29)]
    objects.append(_stitch('Blouse / pocket U perimeter stitching',[front(x,z,_pocket_gap(x,z)+.00047) for x,z in path],collection,seam))
    objects.append(_stitch('Blouse / pocket folded-edge stitch',[front(.0595+.052*j/30,1.183,.00115+.0006*math.sin(math.pi/3)+.00033) for j in range(31)],collection,seam))

    return objects

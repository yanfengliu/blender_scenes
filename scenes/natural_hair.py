"""An anatomical strand groom with continuous scalp-to-shoulder guide curves.

The body supplies the scalp and collision surface. No UV flow, hair cards,
ellipsoid shell, height-window X clamp, or photographed hair panels are used.
tools/check_realistic_character.py remains the independent intersection gate.
The fixed hero, portrait, profile and rear renders determine visual acceptance.
"""
import math
import random


def _mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def _unit(v):
    length = math.sqrt(sum(x * x for x in v))
    return tuple(x / length for x in v) if length > 1e-9 else (0.0, 0.0, 1.0)


def _bezier(a, b, c, d, t):
    u = 1 - t
    return tuple(u**3*a[i] + 3*u*u*t*b[i] + 3*u*t*t*c[i] + t**3*d[i] for i in range(3))


def _sample_curve(points, count=100):
    """Centripetal spacing is unnecessary for the already dense guide controls."""
    result = []
    for j in range(count):
        t = (len(points) - 1) * j / (count - 1)
        i = min(len(points) - 2, int(t))
        u = t - i
        a, b = points[max(0, i-1)], points[i]
        c, d = points[i+1], points[min(len(points)-1, i+2)]
        result.append(tuple(0.5*((2*b[k]) + (-a[k]+c[k])*u +
                                (2*a[k]-5*b[k]+4*c[k]-d[k])*u*u +
                                (-a[k]+3*b[k]-3*c[k]+d[k])*u*u*u) for k in range(3)))
    return result


class _Head:
    def __init__(self, bpy, native, scale, body_object):
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
        from prepare_human_base import group_center, to_blender
        self.Vector = Vector
        world = to_blender(native['vertices'], native['ground_y'], scale)
        joint, eye, jaw = [to_blender([group_center(native, name)], native['ground_y'], scale)[0]
                           for name in ('joint-head', 'joint-l-eye', 'joint-jaw')]
        self.cx, self.cy = joint[:2]
        self.eye, self.jaw = eye[2], jaw[2] - 0.007
        self.top = max(world[i][2] for i in native['groups']['body'])
        self.centre = Vector((self.cx, self.cy, self.eye + 0.012))
        if body_object is not None:
            bpy.context.view_layer.update()
            evaluated = body_object.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh = evaluated.to_mesh()
            try:
                verts = [evaluated.matrix_world @ v.co for v in mesh.vertices]
                polygons = [tuple(p.vertices) for p in mesh.polygons]
            finally:
                evaluated.to_mesh_clear()
        else:
            verts,polygons=[Vector(p) for p in world],native['faces']
        self.tree=BVHTree.FromPolygons(verts,polygons)
        protected=[]
        for polygon in polygons:
            c=sum((verts[i] for i in polygon),Vector())/len(polygon)
            if (1.44<c.z<1.60 and c.y<.06 and
                    (abs(c.x)>.05 or c.y<-.060)):
                protected.append(polygon)
        self.clearance_tree=BVHTree.FromPolygons(verts,protected)
        self.max_guide_lift = 0.0
        self.max_root_distance = 0.0
        self.measured_roots = 0
        self.corrected_strands=0
        self.max_strand_lift=0.0

    def scalp(self, direction, loft=0.005):
        direction = self.Vector(_unit(direction))
        # Outside-in selects the outer ear/head surface when a ray crosses both.
        hit = self.tree.ray_cast(self.centre + direction * 0.35, -direction, 0.35)[0]
        if hit is None:
            raise ValueError(f'Anatomical hair found no scalp along direction {tuple(direction)}; supply the complete body mesh.')
        return tuple(hit + direction * loft)

    def radial_skin(self, dx, dy, z):
        direction = self.Vector(_unit((dx, dy, 0)))
        origin = self.Vector((self.cx, self.cy, z)) + direction * 0.30
        hit = self.tree.ray_cast(origin, -direction, 0.30)[0]
        return None if hit is None else math.hypot(hit.x-self.cx, hit.y-self.cy)

    def column_radius(self, dx, dy):
        # The angular neighbourhood also protects interpolated child strands
        # beside a thin ear. No global width plane is imposed on the hairstyle.
        angle = math.atan2(dy, dx)
        radii = [self.radial_skin(math.cos(angle + da), math.sin(angle + da),
                                 self.jaw - 0.008 + i * 0.002)
                 for da in (-0.045, -0.0225, 0.0, 0.0225, 0.045)
                 for i in range(math.ceil((self.eye + 0.028 - self.jaw + 0.008) / 0.002) + 1)]
        radii = [r for r in radii if r is not None]
        if not radii:
            raise ValueError('Anatomical hair could not measure the local side-lock clearance column.')
        return max(radii) + 0.0055

    def front(self, x, z):
        hit = self.tree.ray_cast(self.Vector((x, -0.5, z)), self.Vector((0, 1, 0)), 0.7)[0]
        return None if hit is None else hit.y

    def anchor_root(self, point, dx, dy):
        """Place and measure a real follicle, rather than a floating guide root."""
        direction = (point[0]-self.centre.x+dx, point[1]-self.centre.y+dy,
                     point[2]-self.centre.z)
        root = self.scalp(direction, .00012)
        distance = self.tree.find_nearest(self.Vector(root))[3]
        if distance is None or distance > .0003:
            raise ValueError(f'Hair root at {root} is {distance} m from the anatomical scalp; required distance is at most 0.0003 m.')
        self.measured_roots += 1
        self.max_root_distance = max(self.max_root_distance, distance)
        return root

    def clear_whole_guide(self, guide):
        """A single smooth radial offset per guide, never a pointwise clipping field."""
        needed = 0.0
        for x, y, z in guide:
            if self.jaw - 0.015 <= z <= self.top:
                dx, dy = x-self.cx, y-self.cy
                radius = math.hypot(dx, dy)
                if radius > 0.003:
                    surface = self.radial_skin(dx, dy, z)
                    if surface is not None:
                        needed = max(needed, surface + 0.0025 - radius)
        if needed <= 0:
            return guide
        self.max_guide_lift = max(self.max_guide_lift, needed)
        result = []
        for x, y, z in guide:
            dx, dy = x-self.cx, y-self.cy
            radius = math.hypot(dx, dy)
            if radius > 0.003:
                x += needed * dx/radius
                y += needed * dy/radius
            result.append((x,y,z))
        return result

    def clear_interpolated_strand(self,points):
        """Fit the actual child, including segments, after guide interpolation.

        Two individually clear guides can straddle the narrow helix while their
        interpolation crosses it. Each affected child receives one broad radial
        lift over the measured crossing region, never point-by-point zigzags.
        """
        arc=[0.0]
        for a,b in zip(points,points[1:]):arc.append(arc[-1]+math.dist(a,b))
        changed=False
        def in_band(p):return 1.442<p[2]<1.598 and (abs(p[0])>.048 or p[1]<-.060)
        def hits(path):
            result=[]
            for i,(a,b) in enumerate(zip(path,path[1:])):
                if max(a[2],b[2])<1.442 or min(a[2],b[2])>1.598:continue
                a,b=self.Vector(a),self.Vector(b);delta=b-a;length=delta.length
                if length<1e-10:continue
                hit,normal,index,distance=self.clearance_tree.ray_cast(a,delta/length,length)
                if hit is not None:result.append((i,arc[i]+distance,tuple(hit)))
            return result
        for attempt in range(2):
            need=[]
            for i,(a,b) in enumerate(zip(points,points[1:])):
                for t in (0.0,.5):
                    p=_mix(a,b,t)
                    if not in_band(p):continue
                    dx,dy=p[0]-self.cx,p[1]-self.cy;r=math.hypot(dx,dy)
                    surface=self.radial_skin(dx,dy,p[2])
                    if surface is not None and surface+.0015>r:
                        need.append((arc[i]+t*(arc[i+1]-arc[i]),surface+.0015-r))
            crossing=hits(points)
            for i,s,p in crossing:
                r=math.hypot(p[0]-self.cx,p[1]-self.cy)
                surface=self.radial_skin(p[0]-self.cx,p[1]-self.cy,p[2])
                need.append((s,max(.0015,0 if surface is None else surface+.0015-r)))
            if not need:break
            centre=(min(s for s,d in need)+max(s for s,d in need))/2
            half_width=max(.035,(max(s for s,d in need)-min(s for s,d in need))/2+.020)
            def kernel(s):
                u=abs(s-centre)/half_width
                return (1-u*u)**2 if u<1 else 0.0
            amplitude=max(d/max(.10,kernel(s)) for s,d in need)+.00025
            if amplitude>.006:
                raise ValueError(f'Interpolated hair needs a {amplitude:.6f} m lift; the bounded 6 mm local repair is insufficient. Refit the guide corridor.')
            self.max_strand_lift=max(self.max_strand_lift,amplitude)
            changed=True;result=[]
            for i,(x,y,z) in enumerate(points):
                dx,dy=x-self.cx,y-self.cy;r=math.hypot(dx,dy)
                lift=amplitude*kernel(arc[i])
                if i==0:lift=0.0
                if r>.003:x+=dx/r*lift;y+=dy/r*lift
                result.append((x,y,z))
            points=result
        remaining=hits(points)
        if remaining:
            raise ValueError(f'Interpolated hair still crosses the anatomical face/ear surface at {remaining[:3]}; smooth local clearance did not resolve the child path.')
        if changed:self.corrected_strands+=1
        return points


def _transport_angle(parameter, amount):
    """An ordered temple sweep: expand one ear corridor, keep both seams shut.

    The smooth map is strictly increasing; unlike nearest-guide attraction it
    never collapses an interval into a lock or removes angular populations.
    """
    enter=_smooth((parameter+.45)/.25)
    leave=1-_smooth((parameter-.20)/(math.pi/2-.20))
    return parameter+.08*amount*enter*leave


def _ear_sweep(z,head):
    # A small one-way drift avoids the rejected shared outward/return S-bend.
    return _smooth((head.eye+.035-z)/.160)


def _scalp_arc(head, root_direction, end_direction, phase, count=40, parameter=0, side=1):
    """Follow the same anatomical crown surface for front and long hair."""
    dot = max(-1.0, min(1.0, sum(a*b for a,b in zip(root_direction, end_direction))))
    arc = math.acos(dot)
    scalp = []
    for j in range(count):
        t = j/(count-1)
        direction = tuple((math.sin((1-t)*arc)*root_direction[k] +
                           math.sin(t*arc)*end_direction[k])/math.sin(arc) for k in range(3))
        # A modest comb bend makes outer forehead strands sweep diagonally
        # before their eye-line tips. Roots/endpoints remain unchanged.
        front=1-_smooth((parameter+.70)/.50)
        bend=.15*front*max(0.0,math.cos(parameter))*math.sin(math.pi*t)**2
        horizontal=math.hypot(direction[0],direction[1])
        angle=math.atan2(direction[1],abs(direction[0]))+bend
        direction=(side*horizontal*math.cos(angle),horizontal*math.sin(angle),direction[2])
        # The child lock field supplies depth; guides no longer define a thick
        # outer blanket that every strand follows with almost the same tangent.
        loft = .0028 + .0016 * math.sin(math.pi*t)**2
        loft += .0007 * (1 + math.sin(phase*2.3 + 3.4*t)) * math.sin(math.pi*t)**2
        scalp.append(head.scalp(direction, loft))
    return scalp


def _guide(head, side, parameter):
    """One crown-rooted family from short frontal wisps to shoulder-length hair.

    Parameter is the actual azimuth: -pi/2 is forehead centre, +pi/2 rear.
    Length changes beyond the outer eye region, without a separate fringe
    beneath a fixed minimum-azimuth edge of the long hair.
    """
    phase = 3.2 * parameter + side * .71
    root_angle = .12 + .40 * parameter / (math.pi/2)
    root_direction = (0.0, math.sin(root_angle), math.cos(root_angle))
    ux, uy = side * math.cos(parameter), math.sin(parameter)
    long_weight = _smooth((parameter + .84)/.32)
    frontal = None
    if long_weight < 1.0:
        target_z = head.eye + .010 + .008 * math.sin(phase*2.2)**2
        # Solve against the actual forehead, including the strand's loft.
        # The lower bound remains above the eye line for every frontal guide.
        lo, hi = -.10, .38
        for _ in range(16):
            angle = (lo+hi)/2
            direction = (ux*math.cos(angle), uy*math.cos(angle), math.sin(angle))
            point = head.scalp(direction, .0038)
            if point[2] < target_z: lo = angle
            else: hi = angle
        elevation = (lo+hi)/2
        end_direction = (ux*math.cos(elevation), uy*math.cos(elevation), math.sin(elevation))
        frontal = _sample_curve(_scalp_arc(head,root_direction,end_direction,phase,55,parameter,side),110)
        if long_weight == 0.0:
            return head.clear_whole_guide(frontal)
    elevation = .30 + .065 * math.sin(phase)
    end_direction = (ux * math.cos(elevation), uy * math.cos(elevation), math.sin(elevation))
    scalp = _scalp_arc(head,root_direction,end_direction,phase,25,parameter,side)
    p = scalp[-1]
    dx,dy = p[0]-head.cx,p[1]-head.cy
    length = math.hypot(dx,dy)
    # Ordered anatomical stations replace the single maximum-radius column:
    # brow, rear of helix, cheek/jaw, then a modest inward shoulder-length tip.
    shoulder_z=head.top-.296+.004*math.sin(phase*1.7)
    stations=[p]
    levels=((min(p[2]-.008,head.eye+.018),.001),
            (head.eye-.015,.001),
            (head.jaw+.032,.001),
            (head.jaw-.014,.000),
            (shoulder_z+.022,-.005),
            (shoulder_z,-.012))
    for z,offset in levels:
        angle=_transport_angle(parameter,_ear_sweep(z,head))
        ux,uy=side*math.cos(angle),math.sin(angle)
        radius=length+offset
        # Local outermost-surface support includes the actual ear and a small
        # angular/height neighbourhood. Its radius is not carried to the tips.
        if z>head.jaw-.025:
            surfaces=[head.radial_skin(side*math.cos(angle+da),math.sin(angle+da),z+dz)
                      for da in (-.025,0,.025) for dz in (-.005,0,.005)]
            surfaces=[r for r in surfaces if r is not None]
            if surfaces: radius=max(radius,max(surfaces)+.0025)
        stations.append((head.cx+ux*radius,head.cy+uy*radius,z))
    tangents=[]
    for i,station in enumerate(stations):
        if i==0:
            direction=_unit(tuple(p[k]-scalp[-3][k] for k in range(3)))
            span=math.dist(stations[0],stations[1])
        elif i==len(stations)-1:
            direction=_unit(tuple(station[k]-stations[i-1][k] for k in range(3)))
            span=math.dist(station,stations[i-1])
        else:
            direction=_unit(tuple(stations[i+1][k]-stations[i-1][k] for k in range(3)))
            span=.5*(math.dist(station,stations[i-1])+math.dist(station,stations[i+1]))
        tangents.append(tuple(direction[k]*span for k in range(3)))
    controls=scalp[:]
    for i in range(len(stations)-1):
        a,b=stations[i:i+2]
        c1=tuple(a[k]+tangents[i][k]/3 for k in range(3))
        c2=tuple(b[k]-tangents[i+1][k]/3 for k in range(3))
        controls.extend(_bezier(a,c1,c2,b,j/10) for j in range(1,11))
    long_path = _sample_curve(controls,110)
    if frontal is not None:
        long_path = [_mix(a,b,long_weight) for a,b in zip(frontal,long_path)]
    return head.clear_whole_guide(long_path)


def _coverage(sample):
    """Invert a strictly positive continuous density, without guide attraction.

    Stratified samples cover the full angular domain. The frontal density is
    lighter but never zero; the side/rear density remains continuous and full.
    """
    def mass(x):
        u=max(0.0,min(1.0,(x-.16)/.19))
        return .28*x+.72*(.19*(u**3-.5*u**4)+max(0.0,x-.35))
    target=sample*mass(1.0);lo,hi=0.0,1.0
    for _ in range(24):
        mid=(lo+hi)/2
        if mass(mid)<target: lo=mid
        else: hi=mid
    return (lo+hi)/2


def _field_point(bank, guide, position):
    """Sample within neighbouring continuous guides, not one fixed column."""
    guide = max(0.0,min(len(bank)-1,guide))
    i = min(len(bank)-2,int(guide))
    j = min(len(bank[0])-2,int(position))
    t = position-j
    return _mix(_mix(bank[i][j],bank[i][j+1],t),
                _mix(bank[i+1][j],bank[i+1][j+1],t),guide-i)


def _child(bank, sample, rng, head, flyaway=False):
    fraction=_coverage(sample)
    f=fraction*(len(bank)-1)
    # Independent departures stay below 0.004 radians (about 0.4 mm at the
    # head), and vanish at the front/rear boundaries. No bin loses its density
    # to a shared attractor, which produced the rejected bars and scalp gaps.
    departure=rng.uniform(-.11,.11)*math.sin(math.pi*fraction)
    departure_mid=rng.uniform(-.07,.07)*math.sin(math.pi*fraction)
    # Roots occur throughout the upper scalp arc, not at one atlas extremum.
    start = rng.randrange(0,5+int(15*_smooth((fraction-.20)/.17)))
    phase = rng.uniform(0,math.tau)
    # Roots cover a surface. Independent depth keeps a dense inner population
    # while fewer strands cross the outer layer and break its sheen.
    outer = rng.random() < .32
    layer = rng.uniform(.0018,.0054) if outer else rng.uniform(.0001,.0018)
    wave = rng.uniform(0.00012,0.00055)
    if flyaway:
        layer += rng.uniform(0.0008,0.0020)
        wave += rng.uniform(0.0003,0.0007)
    fringe = _field_point(bank,f,len(bank[0])-1)[2] > head.eye+.004
    end_delta = (rng.uniform(-.0015,.006) if fringe else rng.uniform(-.006,.008))
    depth=rng.uniform(.0003,.0018)
    if not fringe and fraction < .48:
        end_delta += .004
    points=[]
    for i in range(64):
        t=i/63
        moving_guide=f+departure*_smooth((t-.10)/.80)+departure_mid*math.sin(math.pi*t)**2
        if fringe:
            moving_guide = min(moving_guide,(math.pi/2-.84)/math.pi*(len(bank)-1))
        position = start+(len(bank[0])-1-start)*t
        x,y,z = _field_point(bank,moving_guide,position)
        dx,dy=x-head.cx,y-head.cy
        radius=math.hypot(dx,dy)
        if radius>.003:
            lift = (layer+depth*_smooth(t/.45)) * _smooth(t/.16)
            x+=dx/radius*lift
            y+=dy/radius*lift
        pulse=math.sin(math.pi*t)
        x+=wave*pulse*math.sin(phase+4.5*t)
        y+=wave*.6*pulse*math.sin(phase*.7+5.2*t)
        z+=end_delta*_smooth((t-.72)/.28)
        points.append((x,y,z))
    # Attach the actual strand root to the evaluated scalp. The short smooth
    # lift reaches the lock field without an exposed disconnected root line.
    root = head.anchor_root(points[0],rng.uniform(-.0025,.0025),rng.uniform(-.002,.002))
    offset = tuple(root[a]-points[0][a] for a in range(3))
    for i in range(11):
        weight = 1-_smooth((i/63)/.15)
        points[i] = tuple(points[i][a]+offset[a]*weight for a in range(3))
    return head.clear_interpolated_strand(points), fringe


def build_hair(native_data, scale, collection, body_object=None):
    """Create 23,000 editable fine strands on smooth anatomical guide families."""
    import bpy
    # Only the material/filament writer is reused; no UV bank or old fitting field.
    from fitted_hair import _materials, _add_strand
    head=_Head(bpy,native_data,scale,body_object)
    banks=[]
    for side in (-1,1):
        banks.append([_guide(head,side,-math.pi/2+math.pi*i/95) for i in range(96)])
    rng=random.Random(9020537)
    mats=_materials(bpy)
    for i,mat in enumerate(mats):
        shader=next(node for node in mat.node_tree.nodes if node.type=='BSDF_PRINCIPLED')
        shader.inputs['Roughness'].default_value=(.38,.44,.49,.53)[i]
        shader.inputs['Specular IOR Level'].default_value=(.22,.25,.20,.18)[i]
    specs=(('Hair / continuous left crown fringe and fall',11425,0),
           ('Hair / continuous right crown fringe and fall',11425,1),
           ('Hair / subtle loose filaments',150,-1))
    objects=[]
    low=[math.inf]*3
    high=[-math.inf]*3
    for name,count,bank_id in specs:
        data=bpy.data.curves.new(name,'CURVE')
        data.dimensions='3D'
        data.resolution_u=data.render_resolution_u=1
        data.bevel_depth=.000060
        data.bevel_resolution=1
        data.use_fill_caps=False
        for mat in mats:data.materials.append(mat)
        obj=bpy.data.objects.new(name,data)
        collection.objects.link(obj)
        obj['construction']='Measured scalp roots; stratified continuous angular coverage; small independent child departures and depth'
        obj['source']='CC0 MakeHuman anatomical base and adult targets; no rendered external hair asset'
        obj['strand_count']=count
        obj['seed']=9020537
        for i in range(count):
            selected_id=rng.randrange(len(banks)) if bank_id==-1 else bank_id
            sample=rng.random() if bank_id==-1 else (i+rng.random())/count
            path,fringe=_child(banks[selected_id],sample,rng,head,bank_id==-1)
            if not all(math.isfinite(v)for p in path for v in p):
                raise ValueError(f'Natural hair {name}, strand {i} contains non-finite coordinates.')
            for p in path:
                for axis in range(3):
                    low[axis]=min(low[axis],p[axis]);high[axis]=max(high[axis],p[axis])
            _add_strand(data,path,rng,fringe)
        objects.append(obj)
    for obj in objects:
        obj['bounds_min_m']=low
        obj['bounds_max_m']=high
        obj['largest_whole_guide_clearance_offset_m']=head.max_guide_lift
        obj['measured_root_count']=head.measured_roots
        obj['maximum_measured_root_distance_m']=head.max_root_distance
        obj['interpolated_strands_corrected']=head.corrected_strands
        obj['maximum_local_strand_lift_m']=head.max_strand_lift
    print({'natural_hair_strands':23000,'guide_count':192,'bounds_min_m':low,
           'bounds_max_m':high,'largest_whole_guide_clearance_offset_m':head.max_guide_lift,
           'measured_root_count':head.measured_roots,'maximum_measured_root_distance_m':head.max_root_distance,
           'interpolated_strands_corrected':head.corrected_strands,'maximum_local_strand_lift_m':head.max_strand_lift,
           'verification':'Independent true-intersection test and four-view visual review are required.'})
    return objects

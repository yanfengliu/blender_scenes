"""Bounded adult pose and fitted accessories for the 1.65 m sailor character.

Harness: tools/build_sailor_character.py owns the saved-scene/four-view check.
Joint helper groups provide locations, never skin weights. Native topology,
torso, protected head/neck, socks, cameras and materials are not replaced here.
"""
import math


def _add(a,b): return tuple(a[i]+b[i] for i in range(3))
def _sub(a,b): return tuple(a[i]-b[i] for i in range(3))
def _mul(a,s): return tuple(x*s for x in a)
def _dot(a,b): return sum(x*y for x,y in zip(a,b))
def _unit(a): return _mul(a,1/max(1e-12,math.sqrt(_dot(a,a))))
def _cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def _mix(a,b,t): return _add(a,_mul(_sub(b,a),t))


def _smooth(a,b,x):
    t=max(0.0,min(1.0,(x-a)/(b-a)))
    return t*t*(3-2*t)


def _rotate(point,centre,axis,degrees):
    v=_sub(point,centre);axis=_unit(axis);angle=math.radians(degrees)
    c,s=math.cos(angle),math.sin(angle)
    return _add(centre,_add(_add(_mul(v,c),_mul(_cross(axis,v),s)),_mul(axis,_dot(axis,v)*(1-c))))


def _landmarks(native,scale,side):
    from prepare_human_base import group_center,to_blender
    names=['shoulder','elbow','hand','hand-2','hand-3','ankle','foot-1','foot-2']
    names += [f'finger-{f}-{j}' for f in range(1,6) for j in range(1,5)]
    return {name:to_blender([group_center(native,f'joint-{side}-{name}')],native['ground_y'],scale)[0]
            for name in names}


def make_relaxed_pose(native,scale,base_pose):
    """Wrap the existing pose; output has the same coordinate type as base_pose.

    Native X <= 0.17 m, head/neck and leg points retain the base mapping exactly.
    Shoulder adduction becomes 31 degrees; the forearm turns back 22 degrees.
    The old low-Z leg shift is undone only for identified native arm points.
    """
    limbs={1:_landmarks(native,scale,'l'),-1:_landmarks(native,scale,'r')}
    output_type=type(base_pose((0.0,0.0,0.0)))

    def relaxed(co):
        raw=tuple(co);side=1 if raw[0]>0 else -1;lm=limbs[side]
        weight=(_smooth(.17,.22,abs(raw[0]))*(1-_smooth(1.36,1.40,raw[2]))
                if .79<raw[2]<1.40 else 0.0)
        if weight==0.0: return base_pose(co)
        shaped=raw
        # Local finger capsules, rather than the eight-vertex joint helpers,
        # identify affected skin. No palm-wide displacement or torso weighting.
        if abs(raw[0])>.37 and raw[2]<1.06:
            candidates=[]
            for finger in range(1,6):
                a=lm[f'finger-{finger}-1'];b=lm[f'finger-{finger}-4']
                vector=_sub(b,a);t=max(0,min(1,_dot(_sub(raw,a),vector)/_dot(vector,vector)))
                distance=math.dist(raw,_mix(a,b,t))
                candidates.append((distance,finger,t))
            distance,finger,t=min(candidates)
            influence=(1-_smooth(.009,.020,distance))*_smooth(-.04,.22,t)
            if influence>0:
                palm_long=_sub(lm['finger-3-1'],lm['hand'])
                palm_width=_sub(lm['finger-5-1'],lm['finger-2-1'])
                normal=_mul(_unit(_cross(palm_width,palm_long)),side)
                direction=_unit(_sub(lm[f'finger-{finger}-4'],lm[f'finger-{finger}-1']))
                axis=_cross(direction,normal)
                bent=_rotate(raw,lm[f'finger-{finger}-1'],axis,3 if finger==1 else 4)
                distal=_smooth(.20,.62,t)
                bent=_mix(bent,_rotate(bent,lm[f'finger-{finger}-2'],axis,7),distal)
                shaped=_mix(raw,bent,influence)
        value=tuple(base_pose(shaped))
        shoulder=lm['shoulder']
        expected=_mix(shaped,_rotate(shaped,shoulder,(0,1,0),side*27),weight)
        if expected[2]<.86:
            # A hand remains a hand after adduction; the foot shift is not an
            # anatomical classification and must not move these fingertips.
            value=(value[0]+side*.065*(1-_smooth(.10,.86,expected[2])),value[1],value[2])
        value=_mix(value,_rotate(value,shoulder,(0,1,0),side*4),weight)
        elbow=_rotate(lm['elbow'],shoulder,(0,1,0),side*31)
        forearm=_sub(lm['hand'],lm['elbow'])
        along=_dot(_sub(raw,lm['elbow']),forearm)/_dot(forearm,forearm)
        forearm_weight=weight*_smooth(-.10,.30,along)
        value=_mix(value,_rotate(value,elbow,(1,0,0),22),forearm_weight)
        return output_type(value)

    relaxed.diagnostics={}
    for side,lm in limbs.items():
        points={name:tuple(relaxed(lm[name])) for name in ('shoulder','elbow','hand','finger-3-4')}
        points['elbow_to_wrist_forward_m']=points['elbow'][1]-points['hand'][1]
        relaxed.diagnostics[str(side)]=points
    print({'relaxed_pose_landmarks':relaxed.diagnostics})
    return relaxed


def _mesh(name,vertices,faces,collection,material,thickness=0,subdivision=0):
    import bpy
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);collection.objects.link(obj);data.materials.append(material)
    for face in data.polygons: face.use_smooth=True
    if subdivision:
        mod=obj.modifiers.new('Soft sewn surface','SUBSURF');mod.levels=mod.render_levels=subdivision
    if thickness:
        mod=obj.modifiers.new('Material thickness','SOLIDIFY');mod.thickness=thickness;mod.offset=0
    return obj


def _line(name,points,collection,material,radius=.00055,cyclic=False):
    import bpy
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=2
    data.bevel_depth=radius;data.bevel_resolution=2
    spline=data.splines.new('POLY');spline.points.add(len(points)-1)
    spline.points.foreach_set('co',[v for p in points for v in (*p,1)])
    spline.use_cyclic_u=cyclic
    obj=bpy.data.objects.new(name,data);collection.objects.link(obj);data.materials.append(material)
    return obj


def _foot_fit(native,scale,pose,side):
    from prepare_human_base import to_blender
    lm=_landmarks(native,scale,'l' if side>0 else 'r')
    ankle=tuple(pose(lm['ankle']));toe=tuple(pose(lm['foot-2']))
    forward=_unit((toe[0]-ankle[0],toe[1]-ankle[1],0))
    lateral=(-forward[1],forward[0],0)
    world=to_blender(native['vertices'],native['ground_y'],scale)
    points=[tuple(pose(world[i])) for i in native['groups']['body']
            if world[i][0]*side>0 and world[i][2]<.095]
    local=[(_dot(_sub(p,ankle),lateral),_dot(_sub(p,ankle),forward),p[2]) for p in points]
    lo=min(p[1] for p in local)-.006;hi=max(p[1] for p in local)+.008
    stations=[]
    for j in range(19):
        t=lo+(hi-lo)*j/18
        nearby=sorted(local,key=lambda p:abs(p[1]-t))[:max(20,len(local)//14)]
        left=min(p[0] for p in nearby)-.004;right=max(p[0] for p in nearby)+.004
        stations.append((t,left,right))
    # Smooth the measured envelope, then interpolate with continuous tangents.
    # Rounded end caps meet at one point; the old nonzero width at both tips
    # left a small straight edge and an abrupt corner in the shoe silhouette.
    for _ in range(2):
        stations=[stations[0]]+[(stations[i][0],
            *(.25*stations[i-1][k]+.5*stations[i][k]+.25*stations[i+1][k] for k in (1,2)))
            for i in range(1,18)]+[stations[-1]]
    ankle_points=[p for p in local if abs(p[2]-.075)<.016]
    opening_x=max(.027,(max(p[0] for p in ankle_points)-min(p[0] for p in ankle_points))*.5+.002)
    def at(t):
        f=max(0,min(18,(t-lo)/(hi-lo)*18));i=min(17,int(f));u=f-i
        bounds=[]
        for k in (1,2):
            p0,p1,p2,p3=(stations[j][k] for j in (max(0,i-1),i,i+1,min(18,i+2)))
            bounds.append(.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u))
        end=max(0,min(1,(t-lo)/.020,(hi-t)/.026))
        taper=math.sqrt(end*(2-end));centre=sum(bounds)/2;half=(bounds[1]-bounds[0])*.5*taper
        return centre-half,centre+half
    def point(x,t,z): return (ankle[0]+lateral[0]*x+forward[0]*t,ankle[1]+lateral[1]*x+forward[1]*t,z)
    def outline(a):
        t=(lo+hi)/2+(hi-lo)*.5*math.cos(a);left,right=at(t)
        return ((left+right)/2+(right-left)*.5*(1 if math.sin(a)>=0 else -1),t)
    def upper(a,q):
        x,t=outline(a)
        opening_t=.008+.048*math.cos(a);opening_side=opening_x*math.sin(a)
        x=x+(opening_side-x)*q;t=t+(opening_t-t)*q
        rim=.073+.004*(1-math.cos(a))*.5
        z=.017+(rim-.017)*math.sin(q*math.pi/2)**.90
        return point(x,t,z)
    return point,outline,upper,at,(lo,hi),local


def build_loafers(native,scale,pose,collection,materials):
    """Return foot-fitted open uppers, soles, heel blocks, apron and penny straps.

    materials requires {'leather': material, 'sole': material}. Sock geometry is
    neither edited nor rebuilt. The paired foot envelope supplies shoe length.
    """
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    objects=[];n=96
    for side in (-1,1):
        point,outline,upper,at,(lo,hi),foot=_foot_fit(native,scale,pose,side)
        name='Loafer / '+('left' if side>0 else 'right')
        def underside(t):
            if t>=.09:return .001
            return .001+.0095*(1-_smooth(.015,.09,t))+.0015*math.sin(math.pi*_smooth(.005,.08,t))**2
        vertices=[]
        for height_fraction in (0,.12,.88,1):
            for j in range(n):
                x,t=outline(math.tau*j/n);bottom=underside(t)
                vertices.append(point(x,t,bottom+height_fraction*(.017-bottom)))
        faces=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(3) for j in range(n)]
        # Longitudinal underside rows describe an actual arch. A single flat
        # bottom n-gon enclosed the heel and made the shoe a solid platform.
        centres={0:0,n//2:n//2}
        for j in range(1,n//2):
            _,t=outline(math.tau*j/n);left,right=at(t)
            centres[j]=len(vertices);vertices.append(point((left+right)/2,t,underside(t)))
        for j in range(n//2):
            for face in ((j,j+1,centres[j+1],centres[j]),
                         (centres[j],centres[j+1],(n-j-1)%n,(n-j)%n)):
                unique=tuple(dict.fromkeys(face))
                faces.append(tuple(reversed(unique)))
        sole=_mesh(name+' fitted welt and sole',vertices,faces,collection,materials['sole'])
        edge=sole.modifiers.new('Rounded sole edge','BEVEL');edge.width=.0016;edge.segments=3
        sole['forefoot_contact_z_m']=.001;sole['arch_underside_z_m']=underside(.035)
        objects.append(sole)
        rows=15
        vertices=[upper(math.tau*j/n,i/rows) for i in range(rows+1) for j in range(n)]
        faces=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(rows) for j in range(n)]
        ob=_mesh(name+' low toe box and open heel counter',vertices,faces,collection,materials['leather'],.0015,1)
        ob['measured_foot_length_m']=max(p[1] for p in foot)-min(p[1] for p in foot)
        ob['shoe_length_m']=hi-lo;objects.append(ob)
        objects.append(_line(name+' bound opening',[upper(math.tau*j/n,1) for j in range(n)],collection,materials['leather'],.0009,True))
        apron=[upper(-1.42+2.84*j/70,.22+.22*(abs(-1.42+2.84*j/70)/1.42)**1.3) for j in range(71)]
        apron=[(x,y,z+.0009) for x,y,z in apron]
        objects.append(_line(name+' sewn apron',apron,collection,materials['leather'],.00065))
        # Project a dense leather band along the evaluated upper's normals.
        # Vertex-only support on the old 24-point grid left broad face chords
        # below the curved shoe, exposing apparent detached rectangular ends.
        bpy.context.view_layer.update()
        tree=BVHTree.FromObject(ob,bpy.context.evaluated_depsgraph_get())
        centre_t=.082;left,right=at(centre_t);width=min(abs(left),abs(right))*.84
        def samples(knots):
            result=[]
            for a,b in zip(knots,knots[1:]):
                count=math.ceil((b-a)/.0014)
                result.extend(a+(b-a)*j/count for j in range(count))
            return result+[knots[-1]]
        xs=samples((-width,-.010,.010,width))
        ts=samples((centre_t-.010,centre_t-.002,centre_t+.002,centre_t+.010))
        strap=[]
        for t in ts:
            for x in xs:
                px,py,_=point(x,t,0)
                hit,normal,_,_=tree.ray_cast(Vector((px,py,.20)),Vector((0,0,-1)),.20)
                if hit is None: raise ValueError(f'{name} penny strap has no fitted upper support at {(x,t)}.')
                clearance=.00085+.00015*(1-_smooth(.70,1,abs(x)/width))
                strap.append(tuple(hit+normal*clearance))
        columns=len(xs);strap_faces=[];minimum_gap=float('inf')
        for i in range(len(ts)-1):
            for j in range(columns-1):
                if abs((xs[j]+xs[j+1])*.5)<.010 and abs((ts[i]+ts[i+1])*.5-centre_t)<.002:continue
                face=(i*columns+j,i*columns+j+1,(i+1)*columns+j+1,(i+1)*columns+j)
                # Face centres and edge midpoints must also clear the upper;
                # vertex contact alone cannot certify a curved leather strip.
                points=[Vector(strap[k]) for k in face]
                checks=[sum(points,Vector())/4]+[(points[k]+points[(k+1)%4])/2 for k in range(4)]
                for sample in checks:
                    hit,normal,_,_=tree.find_nearest(sample)
                    if hit is None:raise ValueError(f'{name} penny strap face has no nearby upper support.')
                    gap=(sample-hit).dot(normal);minimum_gap=min(minimum_gap,gap)
                    if gap<.00065:raise ValueError(f'{name} penny strap face clearance is {gap:.6f} m; dense leather faces must clear the upper by at least 0.000650 m before 1.2 mm thickness.')
                strap_faces.append(face)
        used=sorted({index for face in strap_faces for index in face})
        remap={index:new for new,index in enumerate(used)}
        strap=[strap[index] for index in used]
        strap_faces=[tuple(remap[index] for index in face) for face in strap_faces]
        band=_mesh(name+' slotted penny strap',strap,strap_faces,collection,materials['leather'],.0012)
        band['minimum_sampled_upper_clearance_m']=minimum_gap
        band['support_sample_count']=len(strap_faces)*5
        objects.append(band)
        # Fit the stacked heel inside the curved, asymmetric foot outline.
        # A centred rectangle protrudes beyond the narrowed rear sole.
        back=lo+.008;front=min(.009,back+.043)
        stations=[back+(front-back)*j/6 for j in range(7)]
        heel_outline=[]
        for edge,steps in ((0,stations),(1,list(reversed(stations)))):
            for t in steps:
                bounds=at(t);centre=sum(bounds)/2
                heel_outline.append((centre+(bounds[edge]-centre)*.90,t))
        count=len(heel_outline)
        heel=[point(x,t,z) for z in (.001,.012) for x,t in heel_outline]
        heel_faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]
        heel_faces.extend((j,(j+1)%count,(j+1)%count+count,j+count) for j in range(count))
        heel_object=_mesh(name+' low stacked heel',heel,heel_faces,collection,materials['sole'])
        edge=heel_object.modifiers.new('Rounded stacked heel edge','BEVEL');edge.width=.0018;edge.segments=3
        objects.append(heel_object)
    return objects


def build_neckerchief(blouse,collection,material):
    """Return a visibly wrapped knot and two unequal supported fabric tails."""
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update()
    evaluated=blouse.evaluated_get(bpy.context.evaluated_depsgraph_get())
    inv=evaluated.matrix_world.inverted()
    def support(x,z):
        origin=inv@Vector((x,-.5,z));direction=(inv.to_3x3()@Vector((0,1,0))).normalized()
        hit,co,normal,index=evaluated.ray_cast(origin,direction)
        if not hit: raise ValueError(f'Neckerchief has no blouse support at x={x:.4f}, z={z:.4f} m.')
        return (evaluated.matrix_world@co).y
    objects=[]
    # Folded scarf fabric emerges beneath each unchanged collar edge and
    # continues into the knot, rather than leaving an isolated red clip.
    for side in (-1,1):
        rows,columns=36,8;vertices=[]
        for i in range(rows+1):
            t=i/rows;x=side*(.136*(1-t)+.004*t)
            width=.0055+.005*math.sin(math.pi*t)
            centre_z=1.22+.774*abs(x)-.0075-.005*math.sin(math.pi*t)
            for j in range(columns+1):
                u=2*j/columns-1;z=centre_z+width*u
                fold=.002*(1-u*u)+.0012*math.sin(2.3*math.pi*t+u)*math.sin(math.pi*t)
                y=support(x,z)-(.002+.004*math.sin(math.pi*t))-fold
                vertices.append((x,y,z))
        faces=[(i*9+j,i*9+j+1,(i+1)*9+j+1,(i+1)*9+j) for i in range(rows) for j in range(columns)]
        objects.append(_mesh('Neckerchief / '+('left' if side<0 else 'right')+' folded collar entry',vertices,faces,collection,material,.0008,1))
    for side,length in ((-1,.127),(1,.145)):
        rows,columns=32,8;vertices=[]
        for i in range(rows+1):
            t=i/rows;cx=side*(.004+.025*t)+.003*math.sin(math.pi*t)
            width=.0045+.008*math.sin(math.pi*t*.92)
            for j in range(columns+1):
                u=2*j/columns-1;x=cx+u*width
                z=1.201+.010*(1-t)**3-length*t-.010*(u*side+.3)*t**4
                fold=.0022*(1-u*u)*math.sin(math.pi*t)+.0010*u*math.sin(2.8*t+side)
                y=support(x,z)-(.003+.012*(1-t)**3)-fold
                vertices.append((x,y,z))
        faces=[(i*9+j,i*9+j+1,(i+1)*9+j+1,(i+1)*9+j) for i in range(rows) for j in range(columns)]
        objects.append(_mesh('Neckerchief / '+('left' if side<0 else 'right')+' unequal folded tail',vertices,faces,collection,material,.0008,1))
    # An overlapping ribbon wraps around the narrow exits. Its open ends and
    # diagonal edges remain visible; there is no sphere beneath this knot.
    rows,columns=72,8;vertices=[]
    centre_y=support(0,1.215)-.011
    for i in range(rows+1):
        t=i/rows;a=-.78*math.pi+t*2.12*math.pi
        for j in range(columns+1):
            u=2*j/columns-1
            x=.0165*math.cos(a)*(1-.13*u*u)
            z=1.215+.014*u+.0017*math.cos(a)+.0013*math.sin(2*a)*(1-u*u)
            overlap=.0009*_smooth(.85,1,t)
            y=centre_y+.0095*math.sin(a)*(1-.12*u*u)-overlap-.0018*(1-u*u)
            y=min(y,support(x,z)-.002)
            vertices.append((x,y,z))
    faces=[(i*9+j,i*9+j+1,(i+1)*9+j+1,(i+1)*9+j) for i in range(rows) for j in range(columns)]
    objects.append(_mesh('Neckerchief / overlapping diagonal ribbon wrap',vertices,faces,collection,material,.0009,1))
    return objects

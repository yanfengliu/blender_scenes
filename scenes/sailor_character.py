"""Editable stylized adult (age 20) in a Japanese sailor-style outfit.

Run with tools/build_sailor_character.py. All geometry is generated locally;
the scene uses no external models, textures, or fonts.
"""
import bpy
import math
from pathlib import Path
from mathutils import Vector

TAU = math.tau
OUT = Path(globals().get('OUTPUT_DIR', str(Path.cwd() / 'outputs/sailor_character')))
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for old in list(bpy.data.materials):
    bpy.data.materials.remove(old)


def color(hexval):
    c = [int(hexval[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v < .04045 else ((v + .055) / 1.055) ** 2.4 for v in c) + (1,)


def material(name, hexval, rough=.45, metal=0, subsurface=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color(hexval)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = color(hexval)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    p.inputs['Subsurface Weight'].default_value = subsurface
    if subsurface:
        p.inputs['Subsurface Radius'].default_value = (1, .45, .25)
        p.inputs['Subsurface Scale'].default_value = .065
    return m


skin = material('Skin / warm porcelain', 'F2BEA2', .46, subsurface=.075)
earpink = material('Ear / soft warm shadow', 'DC9A87', .5)
blushmat = material('Cheeks / peach watercolor', 'EEA394', .55)
ivory = material('Blouse / warm ivory cotton', 'FAF3DD', .65)
navy = material('Uniform / midnight indigo twill', '26334D', .62)
navy_light = material('Uniform / raised pleat', '303F59', .6)
seam = material('Cotton / seam shadow', 'D9D2C1', .7)
stripe = material('Uniform / ivory braid', 'F6E9CD', .5)
red = material('Neckerchief / raspberry silk', 'B84255', .4)
redlight = material('Neckerchief / fold highlight', 'D26372', .4)
hair = material('Hair / dark chestnut', '432A2B', .41)
hairlight = material('Hair / chestnut ribbons', '613B34', .42)
hairglint = material('Hair / soft copper glints', '885344', .44)
outline = material('Face / soft espresso lines', '42262C', .48)
eye_white = material('Eyes / warm whites', 'FFF8EB', .27)
iris = material('Eyes / amber brown', '925128', .29)
irisgold = material('Eyes / honey fleck', 'D19A4C', .3)
pupil = material('Eyes / deep brown pupil', '241C26', .2)
shine = material('Eyes / catchlight', 'FFFFFF', .15)
lip = material('Lips / muted rose', 'BA686B', .5)
sock = material('Socks / ivory knit', 'EFE8D9', .72)
leather = material('Loafers / oxblood leather', '4C3039', .3)
sole = material('Loafers / dark rubber sole', '282732', .65)
gold = material('Hardware / brushed brass', 'D3AB66', .3, .65)
stage_mat = material('Stage / warm porcelain', 'F2D7C5', .6)
stage_edge = material('Stage / dusty rose rim', 'C4918C', .52)
floor_mat = material('Studio / pale sage', 'ACC3BB', .78)

# A very fine weave stays subtle at portrait distance.
for m in (ivory, navy, navy_light, sock):
    n, l = m.node_tree.nodes, m.node_tree.links
    tex = n.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = 170
    tex.inputs['Detail'].default_value = 2
    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .1
    bump.inputs['Distance'].default_value = .007
    l.new(tex.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], n.get('Principled BSDF').inputs['Normal'])

collections = {}
for title in ('01 Anatomy', '02 Face', '03 Hair', '04 Sailor outfit', '05 Shoes and socks', '06 Studio'):
    col = bpy.data.collections.new(title)
    bpy.context.scene.collection.children.link(col)
    collections[title] = col
group = collections['01 Anatomy']


def organize(obj):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    group.objects.link(obj)
    return obj


def mesh(name, verts, faces, mat, sub=0, smooth=True):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    group.objects.link(obj)
    data.materials.append(mat)
    for poly in data.polygons:
        poly.use_smooth = smooth
    if sub:
        mod = obj.modifiers.new('Soft sculpted surface', 'SUBSURF')
        mod.levels = sub
    return obj


def uv(name, loc, scale, mat, segments=40, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    ob = organize(bpy.context.object)
    ob.name = name
    ob.scale = scale
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def line(name, points, radius, mat, cyclic=False):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 16
    data.bevel_depth = radius
    data.bevel_resolution = 4
    spline = data.splines.new('BEZIER')
    spline.bezier_points.add(len(points) - 1)
    for p, co in zip(spline.bezier_points, points):
        p.co = co
        p.handle_left_type = p.handle_right_type = 'AUTO'
    spline.use_cyclic_u = cyclic
    ob = bpy.data.objects.new(name, data)
    group.objects.link(ob)
    data.materials.append(mat)
    return ob


def rings(name, profiles, mat, n=64, sub=2):
    # Profiles are (center_x, center_y, z, radius_x, radius_y).
    verts = [(cx + rx * math.cos(TAU * j / n), cy + ry * math.sin(TAU * j / n), z)
             for cx, cy, z, rx, ry in profiles for j in range(n)]
    faces = [(i*n+j, i*n+(j+1)%n, (i+1)*n+(j+1)%n, (i+1)*n+j)
             for i in range(len(profiles)-1) for j in range(n)]
    faces += [tuple(reversed(range(n))), tuple((len(profiles)-1)*n+j for j in range(n))]
    return mesh(name, verts, faces, mat, sub)


def tube(name, path, radii, mat, n=20, sub=2, depth=1):
    verts = []
    for i, (co, rad) in enumerate(zip(path, radii)):
        co = Vector(co)
        d = Vector(path[min(i+1, len(path)-1)]) - Vector(path[max(0, i-1)])
        d.normalize()
        side = d.cross(Vector((0, 1, 0))).normalized()
        other = d.cross(side).normalized()
        for j in range(n):
            a = TAU*j/n
            verts.append(co + side*rad*math.cos(a) + other*rad*depth*math.sin(a))
    faces = [(i*n+j, i*n+(j+1)%n, (i+1)*n+(j+1)%n, (i+1)*n+j)
             for i in range(len(path)-1) for j in range(n)]
    faces += [tuple(reversed(range(n))), tuple((len(path)-1)*n+j for j in range(n))]
    return mesh(name, verts, faces, mat, sub)


def panel(name, points, mat, thickness=.025, bevel=.012):
    ob = mesh(name, points, [tuple(range(len(points)))], mat)
    mod = ob.modifiers.new('Fabric thickness', 'SOLIDIFY')
    mod.thickness = thickness
    mod = ob.modifiers.new('Soft cloth edges', 'BEVEL')
    mod.width = bevel
    mod.segments = 3
    return ob


# Six-head fashion proportions and a relaxed contrapposto stance.
head_profile = [(0, 0, 5.52, .07, .12), (0, -.015, 5.59, .22, .24),
                (0, 0, 5.72, .37, .32), (0, 0, 5.91, .47, .398),
                (0, .012, 6.15, .52, .435), (0, .024, 6.38, .51, .43),
                (0, .035, 6.58, .42, .36), (0, .04, 6.74, .24, .23),
                (0, .04, 6.8, .025, .04)]
head = rings('Head / shaped cheeks and tapered jaw', head_profile, skin, 80, 2)
face_skin=skin.copy();face_skin.name='Skin / softly blended peach cheeks'
head.data.materials[0]=face_skin
nodes,links=face_skin.node_tree.nodes,face_skin.node_tree.links
coord=nodes.new('ShaderNodeTexCoord');sep=nodes.new('ShaderNodeSeparateXYZ')
links.new(coord.outputs['Object'],sep.inputs[0])


def math_node(operation,a,b=None):
    node=nodes.new('ShaderNodeMath');node.operation=operation
    if isinstance(a,(int,float)):node.inputs[0].default_value=a
    else:links.new(a,node.inputs[0])
    if b is not None:
        if isinstance(b,(int,float)):node.inputs[1].default_value=b
        else:links.new(b,node.inputs[1])
    return node.outputs[0]


dx=math_node('DIVIDE',math_node('SUBTRACT',math_node('ABSOLUTE',sep.outputs['X']),.343),.106)
dz=math_node('DIVIDE',math_node('SUBTRACT',sep.outputs['Z'],5.955),.065)
distance=math_node('SQRT',math_node('ADD',math_node('MULTIPLY',dx,dx),math_node('MULTIPLY',dz,dz)))
fade=nodes.new('ShaderNodeMapRange');fade.interpolation_type='SMOOTHSTEP'
fade.inputs['From Min'].default_value=0;fade.inputs['From Max'].default_value=1
fade.inputs['To Min'].default_value=.48;fade.inputs['To Max'].default_value=0
links.new(distance,fade.inputs['Value'])
mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=color('F2BEA2');mix.inputs[2].default_value=color('E18D82')
links.new(fade.outputs['Result'],mix.inputs[0]);links.new(mix.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])
head['character_age'] = 20
head['style'] = 'Original stylized adult character in Japanese sailor-style clothing'
rings('Neck', [(0, .025, 5.02, .20, .18), (0, .025, 5.15, .177, .167),
               (0, .025, 5.53, .16, .157), (0, .025, 5.66, .17, .165)], skin)
for side in (-1, 1):
    uv(('Left' if side < 0 else 'Right') + ' ear', (side*.496, .002, 6.0), (.095, .086, .145), skin)
    uv('Ear inner fold', (side*.54, -.063, 6.01), (.039, .022, .087), earpink)
    uv('Small pearl stud', (side*.54, -.085, 5.915), (.03, .025, .03), stripe)

# Legs continue under the skirt. The feet are on the top of the display plinth.
tube('Left leg / weight bearing', [(-.31,.03,3.7),(-.33,.015,3.4),(-.34,-.01,2.9),
     (-.34,-.07,2.4),(-.34,-.05,2.18),(-.35,.005,1.75),(-.35,.015,1.24),(-.35,.02,.59)],
     [.24,.257,.231,.171,.169,.189,.13,.092], skin)
tube('Right leg / relaxed',[(.3,.05,3.65),(.32,.035,3.35),(.39,-.09,2.89),
     (.44,-.18,2.44),(.44,-.17,2.25),(.50,-.01,1.73),(.55,.12,1.21),(.56,.13,.59)],
     [.25,.259,.23,.177,.172,.185,.13,.094],skin)

# A slim continuous arm silhouette avoids stacked primitive joints.
tube('Left arm', [(-.53,0,5.1),(-.7,0,4.91),(-.80,-.015,4.63),(-.86,-.06,4.43),
     (-.92,-.15,4.19),(-1.0,-.22,3.98),(-1.024,-.223,3.875)], [.18,.181,.151,.132,.11,.082,.079],skin)
tube('Right arm / friendly wave',[(.55,0,5.10),(.72,-.005,4.91),(.9,-.015,4.64),
     (1.035,-.04,4.53),(1.11,-.08,4.68),(1.26,-.12,5.02),(1.37,-.13,5.34),(1.383,-.13,5.435)],
     [.18,.18,.145,.139,.132,.106,.080,.078],skin)


def hand(name, wrist, axis, spread=1):
    # Five separate, tapering digits. Palm is smoothly overlapped with wrist.
    w, up = Vector(wrist), Vector(axis).normalized()
    across = Vector((up.z, 0, -up.x)).normalized()
    center = w + up*.14
    ob = uv(name + ' / palm', center, (.135,.068,.195), skin)
    ob.rotation_euler = up.to_track_quat('Z','Y').to_euler()
    lengths = [.27,.34,.315,.24]
    for j in range(4):
        offset = (j-1.5)*.067
        base = center+up*.11+across*offset
        lean = across*(j-1.5)*.045*spread
        bend=Vector((0,-.017*max(0,j-1),0))
        end = base+up*lengths[j]+lean+bend
        path = [base-up*.05, base, base+up*(lengths[j]*.5)+lean*.35,
                end-up*.035, end,end+up*.015]
        radius = [.037,.04,.035,.027,.020,.006]
        tube(name+f' / finger {j+1}', path, radius, skin, 12, 2, .85)
    base = center-across*.10-up*.05
    tube(name+' / thumb',[center-across*.025-up*.065,base,base-across*.072+up*.025,
         base-across*.145+up*.115,base-across*.15+up*.15],
         [.069,.061,.047,.036,.012],skin,12,2,.87)


hand('Left hand',(-1.0,-.22,3.985),(-.22,-.03,-1),.35)
hand('Right hand',(1.365,-.13,5.31),(.10,0,1),1)

# Weld the arm, wrist, palm, and digits into a single sculptable skin surface.
for side in ('Left','Right'):
    parts=[o for o in group.objects if o.name.startswith(side+' arm') or o.name.startswith(side+' hand')]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts:
        bpy.context.view_layer.objects.active=ob
        for modifier in list(ob.modifiers):
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        ob.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.object.join()
    arm=bpy.context.object
    arm.name=side+' arm and hand / seamless sculpt'
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    arm.data.remesh_voxel_size=.012
    bpy.ops.object.voxel_remesh()
    # Verify the full posed arm after remeshing: a floating digit can look valid
    # in silhouette while still being an entirely separate connected component.
    adjacency=[[] for _ in arm.data.vertices]
    for edge in arm.data.edges:
        a,b=edge.vertices;adjacency[a].append(b);adjacency[b].append(a)
    seen={0};pending=[0]
    while pending:
        for vertex in adjacency[pending.pop()]:
            if vertex not in seen:seen.add(vertex);pending.append(vertex)
    if len(seen)!=len(adjacency):
        raise RuntimeError(side+' arm has detached skin geometry; extend all digit roots inside the palm before remeshing')
    smooth=arm.modifiers.new('Soften wrist and finger webs','SMOOTH');smooth.factor=.55;smooth.iterations=4
    sub=arm.modifiers.new('Smooth skin finish','SUBSURF');sub.levels=1
    for poly in arm.data.polygons:poly.use_smooth=True

group = collections['02 Face']


def face_y(x,z):
    for lower, upper in zip(head_profile,head_profile[1:]):
        if lower[2] <= z <= upper[2]:
            t=(z-lower[2])/(upper[2]-lower[2])
            rx=lower[3]*(1-t)+upper[3]*t
            ry=lower[4]*(1-t)+upper[4]*t
            cy=lower[1]*(1-t)+upper[1]*t
            return cy-ry*math.sqrt(max(.05,1-(x/rx)**2))
    return -.3


def face_line(name, coords, radius, mat, offset=.021):
    return line(name,[(x,face_y(x,z)-offset,z) for x,z in coords],radius,mat)


def eye_patch(name,cx,cz,rx,rz,mat,offset=.024):
    verts=[(cx,face_y(cx,cz)-offset-.01,cz)]
    n=64
    for i in range(n):
        a=TAU*i/n
        x=cx+rx*math.cos(a)
        z=cz+rz*math.sin(a)*(.86 if math.sin(a)<0 else 1)
        verts.append((x,face_y(x,z)-offset,z))
    return mesh(name,verts,[(0,i+1,(i+1)%n+1) for i in range(n)],mat)


for s in (-1,1):
    cx=s*.222
    eye_patch('Eye / almond white',cx,6.135,.166,.106,eye_white)
    # Irises hug the curved face instead of sitting on top like googly eyes.
    eye_patch('Eye / iris dark limbal rim',cx+s*.004,6.132,.081,.100,outline,.04)
    eye_patch('Eye / amber iris',cx+s*.004,6.129,.066,.084,iris,.045)
    eye_patch('Eye / honey lower iris',cx+s*.004,6.103,.05,.048,irisgold,.049)
    eye_patch('Eye / pupil',cx+s*.004,6.145,.033,.062,pupil,.054)
    uv('Eye / large reflected softbox',(cx-.024,face_y(cx-.024,6.18)-.065,6.18),(.023,.009,.029),shine,24,16)
    uv('Eye / small reflected softbox',(cx+.032,face_y(cx+.032,6.107)-.061,6.107),(.010,.006,.013),shine,20,12)
    face_line('Upper eyelid',[(cx-.168,6.136),(cx-.113,6.218),(cx-.024,6.24),
              (cx+.088,6.224),(cx+.169,6.146)],.013,outline,.031)
    face_line('Lower eyelid',[(cx-.157,6.117),(cx-.08,6.057),(cx+.03,6.048),(cx+.145,6.097)],.0045,outline,.032)
    outer=cx+s*.161
    face_line('Outer eyelash',[(outer-s*.02,6.181),(outer+s*.038,6.196),(outer+s*.055,6.221)],.008,outline,.033)
    face_line('Eyebrow',[(cx-.131,6.32),(cx-.04,6.346),(cx+.064,6.342),(cx+.131,6.315)],.012,hair,.024)

uv('Nose / soft rounded tip',(0,-.405,5.987),(.052,.073,.067),skin)
face_line('Mouth / gentle smile',[(-.108,5.834),(-.065,5.804),(0,5.793),(.071,5.809),(.108,5.84)],.0075,outline,.018)
face_line('Lower lip / soft rose',[(-.048,5.778),(0,5.771),(.05,5.781)],.006,lip,.016)

group = collections['04 Sailor outfit']
rings('Blouse / tailored cotton body',[(0,.015,3.94,.366,.245),(0,.015,4.015,.381,.257),
     (0,.018,4.17,.388,.263),(0,.015,4.43,.43,.286),(0,0,4.72,.505,.31),
     (0,.008,4.97,.57,.278),(0,.015,5.075,.48,.223),(0,.02,5.18,.25,.158),
     (0,.02,5.20,.185,.152)],ivory,80,2)

for side in (-1,1):
    tube('Short sleeve',[(side*.49,0,5.015),(side*.59,0,5.015),(side*.70,-.002,4.89),
         (side*.79,-.01,4.73),(side*.823,-.014,4.65)],[.195,.233,.224,.207,.192],ivory,40,2,1.02)
    tube('Navy sleeve cuff',[(side*.765,-.008,4.775),(side*.785,-.01,4.735),
         (side*.823,-.014,4.65)],[.218,.216,.206],navy,40,0,1.02)
    tube('Sleeve cuff / ivory braid',[(side*.78,-.01,4.737),(side*.789,-.011,4.72)],
         [.222,.220],stripe,40,0,1.02)

# Square sailor cape: back panel, shoulder bridges, and the classic deep front V.
panel('Sailor collar / square back',[(-.58,.11,5.12),(-.56,.29,5.02),(-.48,.321,4.76),
      (.48,.321,4.76),(.56,.29,5.02),(.58,.11,5.12),(.2,.075,5.24),(-.2,.075,5.24)],navy)
for s in (-1,1):
    panel('Sailor collar / shoulder',[(s*.18,-.15,5.235),(s*.18,.10,5.24),
          (s*.57,.14,5.13),(s*.62,-.075,5.105),(s*.52,-.245,5.055)],navy)
    points=[(s*.18,-.159,5.235),(s*.52,-.245,5.055),(s*.59,-.188,5.08),
            (s*.43,-.292,4.895),(0,-.335,4.525),(s*.072,-.327,4.88)]
    panel('Sailor collar / front V',points,navy,.028,.012)
    line('Collar / outer ivory braid',[(s*.548,-.214,5.08),(s*.435,-.303,4.939),
         (s*.22,-.329,4.73),(0,-.357,4.562)],.009,stripe)
    line('Collar / inner ivory braid',[(s*.5,-.251,5.067),(s*.391,-.321,4.94),
         (s*.20,-.347,4.752),(0,-.364,4.61)],.0065,stripe)
for inset in (0,.041):
    line('Collar / squared back braid',[(-.51+inset,.324,5.005),(-.449+inset,.35,4.805+inset),
         (-.38+inset,.35,4.795+inset),(0,.35,4.795+inset),(.38-inset,.35,4.795+inset),
         (.449-inset,.35,4.805+inset),(.51-inset,.324,5.005)],.008 if not inset else .006,stripe)

# Neckerchief has folded fabric tails and a compact tied knot.
panel('Neckerchief / left folded tail',[(-.04,-.393,4.69),(-.205,-.387,4.58),
      (-.24,-.35,4.205),(-.12,-.385,4.26),(.02,-.418,4.55)],red,.037,.019)
panel('Neckerchief / right folded tail',[(.015,-.424,4.685),(.16,-.425,4.54),
      (.21,-.392,4.255),(.077,-.423,4.30),(-.044,-.444,4.57)],red,.034,.017)
uv('Neckerchief / silk knot',(0,-.415,4.66),(.093,.073,.095),red)
line('Neckerchief / fold left',[(-.037,-.442,4.61),(-.12,-.422,4.43),(-.173,-.379,4.265)],.005,redlight)
line('Neckerchief / fold right',[(.045,-.472,4.606),(.106,-.455,4.45),(.151,-.425,4.298)],.005,redlight)

# Eighteen modeled knife pleats, with a rounded cloth hem and interior thickness.
rings('Skirt / fitted waistband',[(0,.02,4.0,.371,.257),(0,.02,4.025,.381,.265),
      (0,.02,4.115,.383,.263),(0,.02,4.14,.366,.25)],navy,96,1)
uv('Waistband / tiny brass button',(-.31,-.164,4.09),(.019,.012,.019),gold,20,12)
N=18*8
pleat_levels=[(4.035,.38,.264,.003),(3.98,.408,.293,.013),(3.77,.51,.354,.03),
              (3.46,.63,.425,.048),(3.14,.71,.47,.062),(3.085,.72,.478,.062)]
verts=[]
pleat_shape=[0,.12,.20,.21,.2,.08,-.75,-.88]
for z,rx,ry,amount in pleat_levels:
    for j in range(N):
        a=TAU*j/N
        fold=amount*pleat_shape[j%8]
        verts.append(((rx+fold)*math.cos(a),.025+(ry+fold)*math.sin(a),z+.018*math.cos(a+.3)))
faces=[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j)
       for i in range(len(pleat_levels)-1) for j in range(N)]
skirt=mesh('Skirt / eighteen tailored knife pleats',verts,faces,navy,0,True)
skirt.data.materials.append(navy_light)
for p in skirt.data.polygons:
    if p.index%N%8 in (1,2):
        p.material_index=1
mod=skirt.modifiers.new('Real fabric thickness','SOLIDIFY');mod.thickness=.018
mod=skirt.modifiers.new('Softened pleat edges','BEVEL');mod.width=.012;mod.segments=3
for zband in (3.144,3.195):
    points=[]
    for j in range(N):
        a=TAU*j/N
        dz=zband-3.085
        fold=(.062-dz*.025)*pleat_shape[j%8]
        points.append(((.741-dz*.235+fold)*math.cos(a),.025+(.495-dz*.14+fold)*math.sin(a),zband+.018*math.cos(a+.3)))
    # POLY keeps trim on the pleat ridges rather than bridging across them.
    data=bpy.data.curves.new('Pleated hem braid','CURVE');data.dimensions='3D'
    data.bevel_depth=.006;data.bevel_resolution=3
    sp=data.splines.new('POLY');sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):p.co=(*co,1)
    sp.use_cyclic_u=True
    ob=bpy.data.objects.new('Skirt / double ivory hem braid',data);group.objects.link(ob);data.materials.append(stripe)

group=collections['05 Shoes and socks']
for name,x,y in [('Left',-.35,.02),('Right',.56,.13)]:
    if name=='Left':
        sock_path=[(-.35,.02,.51),(-.35,.02,.63),(-.35,.015,1.24),(-.35,.005,1.75),(-.347,-.014,1.94)]
    else:
        sock_path=[(.56,.13,.51),(.56,.13,.63),(.55,.12,1.21),(.50,-.01,1.73),(.476,-.076,1.94)]
    tube(name+' / knee sock',sock_path,[.115,.12,.148,.207,.204],sock,48,2)
    cuff=Vector(sock_path[-1]); below=Vector(sock_path[-2]); direction=(cuff-below).normalized()
    tube(name+' / folded sock cuff',[cuff-direction*.10,cuff-direction*.08,cuff,cuff+direction*.025],
         [.215,.218,.211,.205],sock,48,1)
    for j in range(24):
        a=TAU*j/24
        side=direction.cross(Vector((0,1,0))).normalized()
        other=direction.cross(side).normalized()
        radial=side*math.cos(a)+other*math.sin(a)
        line('Sock / cuff rib',[cuff-direction*.082+radial*.218,cuff+radial*.212],.0022,seam)
    uv(name+' loafer / sole',(x,y-.127,.277),(.192,.36,.076),sole)
    uv(name+' loafer / upper',(x,y-.145,.377),(.188,.345,.151),leather)
    uv(name+' loafer / heel',(x,y+.064,.29),(.157,.134,.098),sole)
    # The raised apron seam and penny strap make the shoes read as loafers.
    line(name+' loafer / apron seam',[(x-.126,y-.075,.478),(x-.142,y-.259,.446),
         (x-.095,y-.395,.416),(x,y-.434,.412),(x+.095,y-.395,.416),
         (x+.142,y-.259,.446),(x+.126,y-.075,.478)],.006,redlight)
    panel(name+' loafer / penny strap',[(x-.169,y-.095,.45),(x-.171,y-.17,.45),
          (x-.11,y-.185,.51),(x+.11,y-.185,.51),(x+.171,y-.17,.45),(x+.169,y-.095,.45),
          (x+.11,y-.105,.513),(x-.11,y-.105,.513)],leather,.02,.012)
    line(name+' loafer / penny slot',[(x-.032,y-.153,.524),(x+.032,y-.153,.524)],.008,sole)

group=collections['03 Hair']
# The cap is one closed-looking shell, with sculpted locks layered over it.
verts=[]
nt,np=112,30
for i in range(np+1):
    for j in range(nt):
        a=TAU*j/nt
        front=max(0,-math.sin(a))
        end=1.99-.78*front**.5
        p=.015+(end-.015)*i/np
        verts.append((.558*math.sin(p)*math.cos(a),.053+.487*math.sin(p)*math.sin(a),
                      6.153+.704*math.cos(p)))
faces=[(i*nt+j,i*nt+(j+1)%nt,(i+1)*nt+(j+1)%nt,(i+1)*nt+j)
       for i in range(np) for j in range(nt)]
cap=mesh('Hair / sculpted crown',verts,faces,hair,1)
mod=cap.modifiers.new('Hair shell thickness','SOLIDIFY');mod.thickness=.05


def hair_lock(name,path,widths,depths,mat=hair):
    # Broad elliptical sections produce solid locks with tapered, pointed tips.
    verts=[];n=14
    for i,(co,w,d) in enumerate(zip(path,widths,depths)):
        tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized()
        side=tangent.cross(Vector((0,1,0))).normalized()
        if side.length<.5:side=Vector((1,0,0))
        normal=side.cross(tangent).normalized()
        for j in range(n):
            a=TAU*j/n
            verts.append(Vector(co)+side*w*math.cos(a)+normal*d*math.sin(a))
    faces=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j)
           for i in range(len(path)-1) for j in range(n)]
    faces += [tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))]
    return mesh(name,verts,faces,mat,2)

# A continuous rear hair mass carries gentle flowing ridges and a scalloped edge.
back_levels=[(6.67,.30,.27,.003),(6.51,.435,.366,.003),(6.31,.527,.46,.004),
             (6.09,.574,.509,.005),(5.84,.592,.525,.007),(5.56,.603,.505,.011),
             (5.30,.621,.465,.014),(5.15,.601,.423,.014),(5.095,.571,.388,.01)]
verts=[];nn=129
for i,(z,rx,ry,amp) in enumerate(back_levels):
    for j in range(nn):
        a=-.065+(math.pi+.13)*j/(nn-1)
        flowing=a+.018*math.sin(i*.65+a*2)
        ridge=amp*math.cos(26*flowing)
        bottom=.035*math.cos(26*a) if i==len(back_levels)-1 else 0
        verts.append(((rx+ridge)*math.cos(a),.052+(ry+ridge)*math.sin(a),z+bottom))
faces=[(i*nn+j,i*nn+j+1,(i+1)*nn+j+1,(i+1)*nn+j)
       for i in range(len(back_levels)-1) for j in range(nn-1)]
rear=mesh('Hair / flowing shoulder length back',verts,faces,hair,2)
mod=rear.modifiers.new('Solid sculpted hair edge','SOLIDIFY');mod.thickness=.055
bpy.ops.object.select_all(action='DESELECT')
for ob in (cap,rear):
    bpy.context.view_layer.objects.active=ob
    for modifier in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
    ob.select_set(True)
bpy.context.view_layer.objects.active=cap
bpy.ops.object.join()
cap.name='Hair / seamless crown and back'
cap.data.remesh_voxel_size=.012
bpy.ops.object.voxel_remesh()
mod=cap.modifiers.new('Soften hair transitions','SMOOTH');mod.factor=.65;mod.iterations=8
mod=cap.modifiers.new('Polished hair surface','SUBSURF');mod.levels=1
for poly in cap.data.polygons:poly.use_smooth=True
for j in range(1,12):
    a=math.pi*j/12
    pts=[]
    for z,rx,ry,amp in back_levels[3:-1]:
        ridge=amp*math.cos(26*a)
        pts.append(((rx+ridge+.012)*math.cos(a),.052+(ry+ridge+.012)*math.sin(a),z))
    line('Hair / fine back strand',pts,.003,hairlight)

# Side locks frame the cheeks but keep the eyes fully visible.
for s in (-1,1):
    hair_lock('Hair / face framing lock',[(s*.37,-.20,6.65),(s*.51,-.27,6.37),
          (s*.531,-.272,6.03),(s*.532,-.258,5.71),(s*.578,-.205,5.36),(s*.51,-.235,5.16)],
          [.11,.13,.105,.095,.10,.006],[.055,.066,.05,.05,.05,.006])
    line('Hair / side lock copper sheen',[(s*.49,-.337,6.31),(s*.511,-.326,6.02),
         (s*.515,-.312,5.74),(s*.551,-.264,5.43)],.007,hairlight)

# Swept fringe: one coherent set of curved tapered locks, opening above the brows.
bangs=[
    ([(-.12,-.275,6.74),(-.32,-.412,6.59),(-.445,-.429,6.40),(-.46,-.405,6.255)], [.08,.14,.115,.003]),
    ([(-.07,-.34,6.76),(-.18,-.465,6.62),(-.275,-.482,6.45),(-.343,-.446,6.317)],[.09,.137,.10,.003]),
    ([(.0,-.34,6.76),(.012,-.48,6.64),(-.038,-.507,6.48),(-.114,-.487,6.348)],[.095,.143,.12,.003]),
    ([(.045,-.335,6.76),(.21,-.442,6.64),(.286,-.473,6.49),(.371,-.417,6.336)],[.084,.149,.126,.003]),
    ([(.14,-.272,6.74),(.365,-.361,6.61),(.479,-.356,6.42),(.485,-.33,6.268)],[.081,.139,.109,.003])]
for i,(p,w) in enumerate(bangs):
    hair_lock('Hair / swept fringe %d'%i,p,w,[.026,.036,.028,.003],hair if i%2 else hairlight)
    line('Hair / fringe highlight %d'%i,[(x,y-.033,z+.009) for x,y,z in p[1:3]],.0028,hairlight)

# A small red ribbon barrette adds an asymmetrical accent.
uv('Barrette / brass fastening',(.532,-.16,6.31),(.027,.125,.023),gold)
for s in (-1,1):
    ob=uv('Barrette / ribbon loop',(.557,-.148+s*.065,6.31+s*.043),(.031,.088,.056),red)
    ob.rotation_euler.x=-.55
uv('Barrette / ribbon knot',(.58,-.15,6.31),(.028,.039,.036),redlight)

# Shorten the exposed neck without changing the face's local shader coordinates.
for colname in ('02 Face','03 Hair'):
    for ob in collections[colname].objects:ob.location.z-=.065
for ob in collections['01 Anatomy'].objects:
    if ob==head or 'ear' in ob.name.lower() or 'pearl stud' in ob.name.lower():
        ob.location.z-=.065
    if ob.name=='Neck':
        for vert in ob.data.vertices:vert.co.z=5.2+(vert.co.z-5.2)*.86

group=collections['06 Studio']


def cylinder(name,loc,radius,depth,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=radius,depth=depth,location=loc)
    ob=organize(bpy.context.object);ob.name=name;ob.data.materials.append(mat)
    mod=ob.modifiers.new('Rounded display edge','BEVEL');mod.width=.06;mod.segments=5
    for p in ob.data.polygons:p.use_smooth=True
    mod=ob.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return ob


cylinder('Display / rose lower rim',(0,0,.065),1.51,.13,stage_edge)
cylinder('Display / porcelain plinth',(0,0,.144),1.5,.145,stage_mat)
bpy.ops.mesh.primitive_plane_add(size=200)
ob=organize(bpy.context.object);ob.name='Studio / seamless sage floor';ob.data.materials.append(floor_mat)


def aim(ob,target):
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()


def camera(name,loc,target,scale):
    data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);group.objects.link(ob)
    ob.location=loc;aim(ob,target);data.type='ORTHO';data.ortho_scale=scale;data.lens=65
    return ob


hero=camera('Camera_hero',(8,-24,11.0),(.20,0,3.55),7.8)
camera('Camera_portrait',(.8,-17,7.5),(-.1,-.02,5.96),2.3)
camera('Camera_back',(-8,20,10.0),(0,0,3.5),7.65)


def area(name,loc,target,energy,size,tint):
    data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size;data.color=tint
    ob=bpy.data.objects.new(name,data);group.objects.link(ob);ob.location=loc;aim(ob,target)


area('Light / large warm key',(-4.5,-7,10),(0,0,4),1000,5,(1,.85,.76))
area('Light / cool portrait fill',(5,-4,6),(0,0,4.5),650,4,(.79,.88,1))
area('Light / warm hair rim',(2,4,9),(0,0,4.5),1250,3.5,(1,.80,.64))
area('Light / gentle front eyelight',(-.3,-7,5.5),(0,0,5.8),90,2,(1,.95,.87))

scene=bpy.context.scene
scene['Character']='Haru / original stylized adult, age 20'
scene['Outfit']='Japanese sailor-style uniform: ivory blouse, navy collar and pleated skirt, raspberry neckerchief'
scene['Editing']='Editable meshes and curves grouped by anatomy, face, hair, clothing, and studio. Static posed model; no animation rig.'
scene.render.engine='CYCLES'
scene.cycles.samples=globals().get('SAMPLES',80)
scene.cycles.use_denoising=True
scene.cycles.adaptive_threshold=.025
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='OPTIX';prefs.get_devices()
    if any(d.type=='OPTIX' for d in prefs.devices):
        for d in prefs.devices:d.use=d.type=='OPTIX'
        scene.cycles.device='GPU'
except Exception:
    pass
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.62,.72,.8,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.32
scene.render.resolution_x=int(globals().get('RENDER_SIZE',1600)*.8)
scene.render.resolution_y=globals().get('RENDER_SIZE',1600)
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.camera=hero
scene.render.filepath=str(OUT/'hero.png')
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.245
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True);bpy.context.view_layer.objects.active=head
for screen in bpy.data.screens:
    for space_area in screen.areas:
        if space_area.type=='VIEW_3D':
            space_area.spaces.active.region_3d.view_perspective='CAMERA'
            space_area.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'sailor_character.blend'),compress=True)
print('SCENE_READY: '+str(OUT/'sailor_character.blend'),flush=True)

"""Reference-led adult sailor character, with anatomical CC0 human geometry.

Harness: tools/build_sailor_character.py renders the actual saved scene headlessly.
The generated references live alongside outputs; original toy-style work is retained.
"""
import bpy
import math
import random
import sys
import json
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1] if '__file__' in globals() and 'scenes' in Path(__file__).parts else Path.cwd()
# The build runner executes this file with its own globals.
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'scenes'))
from prepare_human_base import load_body,fit_proxy,to_blender,group_center,ASSETS,DEFAULT_TARGETS
from natural_hair import build_hair
from natural_face import build_skin,shape_expression,attach_skin_regions,fit_fuller_brows,soften_iris_color
from gentle_expression import apply_gentle_expression
from perioral_shape import apply_perioral_shape
from reference_smile import apply_reference_smile
from verify_reference_smile import bind_reference_smile,verify_reference_smile,SmileVerificationError
from ocular_layers import assign_ocular_layers
from body_proportions import apply_body_proportions,full_body_support
from relaxed_character_details import make_relaxed_pose,build_loafers,build_neckerchief

OUT=Path(globals().get('OUTPUT_DIR',ROOT/'outputs/sailor_character_proportions'))
OUT.mkdir(parents=True,exist_ok=True)
random.seed(83)
TAU=math.tau
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)


def srgb(hexval):
    values=[int(hexval[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in values)+(1,)


def material(name,tint,roughness=.5):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=srgb(tint)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=srgb(tint)
    p.inputs['Roughness'].default_value=roughness
    return m


def texture_material(name,path,roughness=.5,alpha=False):
    m=material(name,'FFFFFF',roughness)
    n,l=m.node_tree.nodes,m.node_tree.links;p=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True)
    tex.image.pack();l.new(tex.outputs['Color'],p.inputs['Base Color'])
    if alpha:l.new(tex.outputs['Alpha'],p.inputs['Alpha'])
    return m


skin=build_skin(ASSETS/'skins/young_asian_female/young_lightskinned_female_diffuse3.png')

ivory=material('Blouse / ivory woven cotton','E8E4DA',.76)
navy=material('Uniform / midnight navy wool twill','1D2635',.73)
trim=material('Collar / woven ivory braid','EAE7DC',.68)
red=material('Scarf / deep garnet fabric','8D2432',.64)
seam=material('Cotton seam thread','D3CEC1',.75)
sockmat=material('Socks / cotton knit','DAD6CB',.84)
shoe_mat=material('Loafers / dark brown calf leather','30221D',.37)
sole_mat=material('Loafers / rubber and stacked heel','191716',.66)
gold=material('Hardware / aged brass','B69B62',.38);gold.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.65
floor_mat=material('Studio / warm pale gray','B4AFA6',.78)
for m in (ivory,navy,trim,red,sockmat):
    n,l=m.node_tree.nodes,m.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Sheen Weight'].default_value=.10
    p.inputs['Specular IOR Level'].default_value=.15
    tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=1900;tex.inputs['Detail'].default_value=2
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.22;b.inputs['Distance'].default_value=.00015
    l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])

cols={}
for name in ('01 Human anatomy','02 Eyes and lashes','03 Strand hair','04 Sailor clothing','05 Studio'):
    col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col);cols[name]=col
group=cols['01 Human anatomy']


def mesh(name,verts,faces,mat,sub=0,uvs=None,face_uvs=None):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    ob=bpy.data.objects.new(name,data);group.objects.link(ob);data.materials.append(mat)
    for poly in data.polygons:poly.use_smooth=True
    if uvs is not None:
        layer=data.uv_layers.new(name='UVMap')
        for poly,uvface in zip(data.polygons,face_uvs):
            for loop_index,uvindex in zip(poly.loop_indices,uvface):layer.data[loop_index].uv=uvs[uvindex]
    if sub:
        mod=ob.modifiers.new('Smooth anatomical surface','SUBSURF');mod.levels=sub
    return ob


def line(name,points,radius,mat,cyclic=False):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=16
    data.bevel_depth=radius;data.bevel_resolution=3
    sp=data.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type=p.handle_right_type='AUTO'
    sp.use_cyclic_u=cyclic
    ob=bpy.data.objects.new(name,data);group.objects.link(ob);data.materials.append(mat)
    return ob


def rings(name,profiles,mat,n=96,sub=2,wrinkles=0):
    verts=[]
    for i,(cx,cy,z,rx,ry) in enumerate(profiles):
        for j in range(n):
            a=TAU*j/n
            fold=wrinkles*(math.sin(a*11+i*.7)+.4*math.sin(a*23-i*.6))
            verts.append((cx+(rx+fold)*math.cos(a),cy+(ry+fold)*math.sin(a),z+.3*fold))
    faces=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(profiles)-1) for j in range(n)]
    ob=mesh(name,verts,faces,mat,sub)
    sol=ob.modifiers.new('Real fabric thickness','SOLIDIFY');sol.thickness=.0013
    return ob


def tube(name,points,radii,mat,sub=2):
    verts=[];n=48
    for i,(co,r) in enumerate(zip(points,radii)):
        axis=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized()
        side=axis.cross(Vector((0,1,0))).normalized();normal=axis.cross(side).normalized()
        for j in range(n):
            a=TAU*j/n;wr=.0007*math.sin(13*a+i)
            verts.append(Vector(co)+(side*math.cos(a)+normal*math.sin(a))*(r+wr))
    faces=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(points)-1) for j in range(n)]
    ob=mesh(name,verts,faces,mat,sub)
    sol=ob.modifiers.new('Folded cloth thickness','SOLIDIFY');sol.thickness=.0016
    return ob


def panel(name,verts,mat,thickness=.0018):
    ob=mesh(name,verts,[tuple(range(len(verts)))],mat)
    sol=ob.modifiers.new('Fabric thickness','SOLIDIFY');sol.thickness=thickness
    bevel=ob.modifiers.new('Soft sewn edge','BEVEL');bevel.width=.0015;bevel.segments=3
    return ob


def uv(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,location=loc)
    ob=bpy.context.object;ob.name=name;ob.scale=scale
    for old in list(ob.users_collection):old.objects.unlink(ob)
    group.objects.link(ob);ob.data.materials.append(mat)
    for poly in ob.data.polygons:poly.use_smooth=True
    return ob


native=load_body(DEFAULT_TARGETS+(
    ('mouth-angles-up.target',.28),('l-cheek-volume-incr.target',.14),('r-cheek-volume-incr.target',.14),
    ('chin-width-decr.target',.10),('nose-scale-horiz-decr.target',.08),
    ('mouth-upperlip-volume-incr.target',.30),('l-eye-height2-incr.target',.035),('r-eye-height2-incr.target',.035)))
for v in native['vertices']:
    # Match the reference's shorter lower face while keeping a full adult skull.
    if 4.65<v[1]<5.8:
        weight=smoothweight=max(0,min(1,(v[1]-4.65)/.25))
        v[1]+=weight*(5.8-v[1])*.105
        v[0]*=1+.035*math.exp(-((v[1]-5.35)/.40)**2)
# A continuous local deformation coordinates the lips and cheek lift. It keeps
# original vertex indices, so the eyes/brows/lashes fit the same shaped anatomy.
mouth_y=shape_expression(native)
expression_diagnostics=apply_gentle_expression(native)
# Preserve the retained skin coordinates independently of the later anatomical
# edit. The body field and pose apply to both sets; culling keeps its own input.
skin_reference_native={**native,'vertices':[v[:] for v in native['vertices']]}
assert skin_reference_native['vertices'] is not native['vertices']
perioral_diagnostics=apply_perioral_shape(native)
# Garments fit the retained anatomical shape, independently of facial expression.
# A whole-body BVH can choose a different normal at an equal-distance triangle
# edge when distant face coordinates change. Preserve its pre-smile input rather
# than letting that traversal detail alter the neckline and derived collar.
garment_fit_native={**native,'vertices':[v[:] for v in native['vertices']]}
smile_diagnostics=apply_reference_smile(native)
proportion_diagnostics=apply_body_proportions(native)
apply_body_proportions(garment_fit_native)
apply_body_proportions(skin_reference_native)
assert len(skin_reference_native['vertices'])==len(native['vertices'])==19158
assert skin_reference_native['proportions_baseline_vertices'] is not native['proportions_baseline_vertices']
print({'perioral_shape':perioral_diagnostics},flush=True)
print({'body_proportions':proportion_diagnostics},flush=True)
height=max(native['vertices'][i][1] for i in native['groups']['body'])-native['ground_y']
assert max(garment_fit_native['vertices'][i][1] for i in native['groups']['body'])-garment_fit_native['ground_y']==height
assert all(native['vertices'][i]==garment_fit_native['vertices'][i]
    for name,indices in native['groups'].items() if name.startswith('joint-') for i in indices), 'Expression must preserve pose-driving joint helpers.'
SCALE=1.65/height
vertices=to_blender(native['vertices'],native['ground_y'],SCALE)


def landmark(name):return Vector(to_blender([group_center(native,name)],native['ground_y'],SCALE)[0])


def smoothstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)


def pose(co):
    co=Vector(co);s=1 if co.x>0 else -1
    shoulder=landmarks['shoulder'+str(s)]
    if co.z>.79 and co.z<1.40:
        # Torso and waist vertices stay in place; only the arm region rotates.
        # The earlier threshold narrowed the blouse hem by about 80 mm.
        weight=smoothstep(.17,.22,abs(co.x))*(1-smoothstep(1.36,1.4,co.z))
        rot=Matrix.Rotation(math.radians(s*27),3,'Y')
        co=co.lerp(shoulder+rot@(co-shoulder),weight)
    if co.z<.86:
        # Gentle leg adduction brings the feet together for the reference stance.
        shift=.065*(1-smoothstep(.10,.86,co.z))
        co.x-=s*shift
    return co


landmarks={'shoulder1':landmark('joint-l-shoulder'),'shoulder-1':landmark('joint-r-shoulder')}
pose=make_relaxed_pose(native,SCALE,pose)
posed=[pose(v) for v in vertices]
garment_fit_posed=[pose(v) for v in to_blender(garment_fit_native['vertices'],garment_fit_native['ground_y'],SCALE)]
skin_reference_posed=[pose(v) for v in to_blender(skin_reference_native['vertices'],native['ground_y'],SCALE)]
skin_cut_vertices=to_blender(skin_reference_native['proportions_baseline_vertices'],native['ground_y'],SCALE)
skin_cut_posed=[pose(v) for v in skin_cut_vertices]
visible_faces=[];visible_uvs=[]
for face,uvface in zip(native['faces'],native['face_uvs']):
    # Keep the exact retained10 visible face population. A narrower body must
    # not silently delete extra skin through the existing position-based cuts.
    center=sum((skin_cut_posed[i] for i in face),Vector())/len(face)
    unposed_center=sum((Vector(skin_cut_vertices[i]) for i in face),Vector())/len(face)
    # Only remove skin well inside opaque garments. The neck and shoulder skin
    # remain continuous beneath the neckline instead of ending at a guessed edge.
    covered_torso=.65<center.z<1.30 and abs(unposed_center.x)<.173
    covered_sleeve=1.205<center.z<1.30 and abs(unposed_center.x)>=.15
    # Keep continuous skin below the visible cuff; centre-based cuts can leave
    # boundary vertices several mm above their nominal height.
    covered_sock=center.z<.390
    if not (covered_torso or covered_sleeve or covered_sock):visible_faces.append(face);visible_uvs.append(uvface)
body=mesh('Haru / anatomical adult skin',posed,visible_faces,skin,2,native['uvs'],visible_uvs)
smile_input_sha=bind_reference_smile(body,smile_diagnostics,lambda co:pose(to_blender([co],native['ground_y'],SCALE)[0]))
assert smile_input_sha=='c6c56c4e5d12884216403d5f604dff8290e864031ef6d9c9c6e36271027ea4df', 'Reference smile input differs from the reviewed candidate4-neutral contract.'
body['character_age']=20;body['reference']='references/character-reference.png'
attach_skin_regions(body,skin_reference_posed)
# Keep the editable reference mapping for comparison, but do not mix its baked
# portrait lighting into skin albedo. The final material uses the continuous UV
# photograph and local skin-response attributes across the whole anatomical mesh.
anchors=[(4.80,509),(mouth_y,421),(native['vertices'][294][1],361),
         (group_center(native,'joint-l-eye')[1],282),(6.18,192)]
anchors.sort()


def projected_y(y):
    for (a,pa),(b,pb) in zip(anchors,anchors[1:]):
        if a<=y<=b:return pa+(pb-pa)*(y-a)/(b-a)
    return 509 if y<anchors[0][0] else 192


# The reference UV/unused blend mask also ride their original vertex identity.
# Use actual Blender source normals in the baseline coordinate frame, then remove
# this temporary data before constructing any dependent geometry or saving.
reference_skin_mesh=bpy.data.meshes.new('Temporary skin attribute reference')
try:
    reference_skin_mesh.from_pydata(skin_reference_posed,[],visible_faces)
    reference_skin_mesh.update()
    assert len(reference_skin_mesh.vertices)==len(body.data.vertices)
    assert len(reference_skin_mesh.loops)==len(body.data.loops)
    projection=body.data.uv_layers.new(name='ReferenceFaceProjection')
    weights=body.data.color_attributes.new(name='ReferenceSkinBlend',type='FLOAT_COLOR',domain='CORNER')
    for poly in body.data.polygons:
        for li in poly.loop_indices:
            index=body.data.loops[li].vertex_index
            local=reference_skin_mesh.vertices[index];v=local.co;raw=skin_reference_native['vertices'][index]
            px=609.8+246.5*raw[0];py=projected_y(raw[1])
            projection.data[li].uv=(px/1713,1-py/918)
            facing=smoothstep(.2,.7,-local.normal.y)
            face_region=smoothstep(1.441,1.46,v.z)*(1-smoothstep(1.551,1.566,v.z))
            sides=1-smoothstep(.052,.080,abs(v.x))
            eye_distance=min(math.sqrt(((v.x-s*.0305)/.018)**2+((v.z-1.542)/.008)**2) for s in (-1,1))
            avoid_eyes=smoothstep(1.0,1.5,eye_distance)
            weight=.56*facing*face_region*sides*avoid_eyes
            weights.data[li].color=(weight,weight,weight,1)
finally:
    bpy.data.meshes.remove(reference_skin_mesh)

group=cols['02 Eyes and lashes']
eye_mat=texture_material('Eyes / brown irises and moist sclera',ASSETS/'brown_eye.png',.27,True)
ep=eye_mat.node_tree.nodes.get('Principled BSDF');ep.inputs['Coat Weight'].default_value=0;ep.inputs['Coat Roughness'].default_value=.10
ep.inputs['Specular IOR Level'].default_value=.5;ep.inputs['IOR'].default_value=1.5
soften_iris_color(eye_mat)
lash_mat=texture_material('Eyelashes / natural fine alpha strands',ASSETS/'eyelashes/eyelashes02/eyelashes02.png',.55,True)
eyebrow_mat=texture_material('Eyebrows / fine natural brow hairs',ASSETS/'eyebrows/eyebrow007/eyebrow007.png',.7,True)
for name,path,mat,sub in [('Eyes',ASSETS/'high-poly.mhclo',eye_mat,2),
        ('Eyebrows',ASSETS/'eyebrows/eyebrow007/eyebrow007.mhclo',eyebrow_mat,1),
        ('Eyelashes',ASSETS/'eyelashes/eyelashes02/eyelashes02.mhclo',lash_mat,1)]:
    data=fit_proxy(path,native['vertices']);coords=to_blender(data['vertices'],native['ground_y'],SCALE)
    if name=='Eyebrows':coords=fit_fuller_brows(coords,body)
    ob=mesh(name,coords,data['faces'],mat,sub,data['uvs'],data['face_uvs'])
    if name=='Eyes':assign_ocular_layers(ob,ASSETS/'high-poly.obj')
    if name in ('Eyebrows','Eyelashes'):
        # Match the source alpha-hair materials: no cast shadow or specular.
        ob.visible_shadow=False
        mat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
        if name=='Eyelashes':
            # The reference has light individual lashes rather than dense fans.
            nodes,links=mat.node_tree.nodes,mat.node_tree.links
            shader=nodes.get('Principled BSDF')
            original=shader.inputs['Alpha'].links[0].from_socket
            density=nodes.new('ShaderNodeMath');density.operation='MULTIPLY';density.inputs[1].default_value=.42
            links.new(original,density.inputs[0]);links.new(density.outputs[0],shader.inputs['Alpha'])

group=cols['04 Sailor clothing']
# One connected helper-derived shirt includes shoulders and armholes.
from fitted_blouse import build_blouse
with full_body_support(garment_fit_native,garment_fit_posed) as fit_body:
    blouse=build_blouse(garment_fit_native,SCALE,cols['04 Sailor clothing'],pose,ivory,body_object=fit_body)
from fitted_collar import build_collar
build_collar(blouse,cols['04 Sailor clothing'],navy,trim)
from cloth_finish import build_pocket_details
build_pocket_details(blouse,cols['04 Sailor clothing'],ivory,seam)

build_neckerchief(blouse,cols['04 Sailor clothing'],red)

# Match the actual sewn blouse hem, including its flatter back and front.
from fitted_blouse import _topology
hem_points=[tuple(v.co) for v in blouse.data.vertices]
hem_loops,_,_=_topology(hem_points,[tuple(p.vertices) for p in blouse.data.polygons])
hem_ids=min(hem_loops,key=lambda loop:sum(hem_points[i][2] for i in loop)/len(loop))
hem_center=Vector((0,-.052,0))
hem_samples=sorted((math.atan2(hem_points[i][1]-hem_center.y,hem_points[i][0])%TAU,
    math.hypot(hem_points[i][0],hem_points[i][1]-hem_center.y)) for i in hem_ids)
hem_samples.append((hem_samples[0][0]+TAU,hem_samples[0][1]))

def waist_point(angle,offset=-.001):
    a=angle%TAU
    if a<hem_samples[0][0]:a+=TAU
    for (lo,rlo),(hi,rhi) in zip(hem_samples,hem_samples[1:]):
        if lo<=a<=hi:
            radius=rlo+(rhi-rlo)*(a-lo)/(hi-lo)+offset
            return Vector((radius*math.cos(angle),hem_center.y+radius*math.sin(angle),0))
    raise RuntimeError(f'Waist angle {angle} lacks a fitted hem segment.')

waist_n=96
waist_vertices=[tuple(waist_point(TAU*j/waist_n)+Vector((0,0,z))) for z in (.999,1.02) for j in range(waist_n)]
waist_faces=[(j,(j+1)%waist_n,waist_n+(j+1)%waist_n,waist_n+j) for j in range(waist_n)]
mesh('Skirt / waistband fitted beneath blouse hem',waist_vertices,waist_faces,navy,1)
N=20*8;shape=[0,.12,.16,.16,.16,.02,-.82,-.86]
rows=64
verts=[]
for i in range(rows+1):
    t=i/rows;z=1.014-(1.014-.650)*t
    flare=t+.12*t*(1-t);amp=.018*t*(2-t)
    for j in range(N):
        a=TAU*j/N;fold=amp*shape[j%8]
        hem=Vector((.237*.975*math.cos(a),-.044+.171*.975*math.sin(a),0))
        fitted=waist_point(a).lerp(hem,flare)+fold*Vector((math.cos(a),math.sin(a),0))
        verts.append((fitted.x,fitted.y,z+.003*math.cos(3*a)*t*t))
faces=[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j) for i in range(rows) for j in range(N)]
skirt=mesh('Skirt / twenty folded pleats',verts,faces,navy)
mod=skirt.modifiers.new('Wool fabric thickness','SOLIDIFY');mod.thickness=.0014
mod=skirt.modifiers.new('Softly pressed pleat edges','BEVEL');mod.width=.0017;mod.segments=3

# The socks follow actual calf topology instead of an independently guessed tube.
def clip_sock_polygon(points,height,keep_below):
    clipped=[]
    for a,b in zip(points,points[1:]+points[:1]):
        a_inside=a.z<=height if keep_below else a.z>=height
        b_inside=b.z<=height if keep_below else b.z>=height
        if a_inside:clipped.append(a)
        if a_inside!=b_inside:
            clipped.append(a.lerp(b,(height-a.z)/(b.z-a.z)))
    return clipped

# Face-centre selection left jagged vertices above the smooth ribbed top band.
sock_vertices=[];sock_faces=[];sock_indices={}
for face in native['faces']:
    points=[posed[i] for i in face]
    if max(p.z for p in points)<.073 or min(p.z for p in points)>.423:continue
    points=clip_sock_polygon(clip_sock_polygon(points,.073,False),.423,True)
    if len(points)<3:continue
    indices=[]
    for point in points:
        key=tuple(round(value,9) for value in point)
        if key not in sock_indices:
            sock_indices[key]=len(sock_vertices);sock_vertices.append(tuple(point))
        indices.append(sock_indices[key])
    if len(set(indices))>=3:sock_faces.append(indices)
sockob=mesh('Socks / anatomical calf fit',sock_vertices,sock_faces,sockmat,2)
sol=sockob.modifiers.new('Knit thickness','SOLIDIFY');sol.thickness=.002;sol.offset=1
for s in (-1,1):
    section=[v for i,v in enumerate(posed) if i in native['groups']['body'] and abs(v.z-.423)<.015 and v.x*s>0]
    xmin,xmax=min(v.x for v in section),max(v.x for v in section)
    ymin,ymax=min(v.y for v in section),max(v.y for v in section)
    cx,cy=(xmin+xmax)/2,(ymin+ymax)/2;rx=(xmax-xmin)/2+.003;ry=(ymax-ymin)/2+.003
    rings('Sock / ribbed top band',[(cx,cy,.410,rx,ry),(cx,cy,.427,rx,ry),
        (cx,cy,.435,rx-.001,ry-.001)],sockmat,64,1)
    for j in range(36):
        a=TAU*j/36
        line('Sock / knitted rib',[(cx+(rx+.0007)*math.cos(a),cy+(ry+.0007)*math.sin(a),.416),
            (cx+(rx+.0007)*math.cos(a),cy+(ry+.0007)*math.sin(a),.431)],.00027,seam)
build_loafers(native,SCALE,pose,cols['04 Sailor clothing'],{'leather':shoe_mat,'sole':sole_mat})

hair_objects=build_hair(native,SCALE,cols['03 Strand hair'],body_object=body)

group=cols['05 Studio']
# A round photographic sweep gives every inspection camera a seamless backdrop.
cyc_profile=[(.001,0),(5.5,0)]
for i in range(1,33):
    a=(math.pi/2)*i/32;cyc_profile.append((5.5+math.sin(a),1-math.cos(a)))
cyc_profile.append((6.5,8));sectors=192
cycverts=[(r*math.cos(TAU*j/sectors),r*math.sin(TAU*j/sectors),z) for r,z in cyc_profile for j in range(sectors)]
cycfaces=[(i*sectors+j,i*sectors+(j+1)%sectors,(i+1)*sectors+(j+1)%sectors,(i+1)*sectors+j)
    for i in range(len(cyc_profile)-1) for j in range(sectors)]
mesh('Studio / panoramic curved sweep',cycverts,cycfaces,floor_mat)


def aim(ob,target):ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()


def camera(name,loc,target,lens):
    data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);group.objects.link(ob)
    ob.location=loc;aim(ob,target);data.lens=lens;data.clip_start=.01
    return ob


hero=camera('Camera_hero',(.45,-4.5,1.5),(0,-.035,.86),80)
camera('Camera_portrait',(.045,-1.05,1.56),(0,-.035,1.508),82)
camera('Camera_back',(-.3,2.3,1.30),(0,-.02,.86),38)
camera('Camera_profile',(1.1,-.06,1.56),(0,-.035,1.51),82)


def light(name,loc,target,power,size,tint):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=tint
    ob=bpy.data.objects.new(name,data);group.objects.link(ob);ob.location=loc;aim(ob,target)


light('Softbox / neutral key',(-1.3,-1.8,2.55),(0,0,1.25),90,1.5,(1,.95,.90))
light('Softbox / gentle fill',(1.2,-1.1,1.75),(0,0,1.35),32,1.25,(.90,.95,1))
light('Softbox / broad hair separation',(.3,1.3,2.5),(0,0,1.4),65,1.1,(1,.94,.87))
scene=bpy.context.scene;scene.camera=hero
scene.render.engine='CYCLES';scene.cycles.samples=globals().get('SAMPLES',96)
scene.cycles.transparent_max_bounces=16
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.02
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    if any(d.type=='OPTIX' for d in prefs.devices):
        for d in prefs.devices:d.use=d.type=='OPTIX'
        scene.cycles.device='GPU'
except Exception:pass
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.68,.72,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.10
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene.render.resolution_x=int(globals().get('RENDER_SIZE',1600)*.8);scene.render.resolution_y=globals().get('RENDER_SIZE',1600)
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.filepath=str(OUT/'hero.png');scene.unit_settings.system='METRIC'
scene['Character']='Haru / reference-led adult Japanese woman, age 20'
scene['Reference']='references/character-reference.png and references/body-turnaround.png, generated with built-in ImageGen'
scene['Geometry']='Anatomical CC0 MakeHuman adult base with photographic UV skin; editable procedural sailor clothing and strand hair'
scene['Editing']='Static posed model; no animation rig. Textures packed in the blend file.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
try:
    smile_gate=verify_reference_smile(body,{'portrait':bpy.data.objects['Camera_portrait'].matrix_world.translation,
        'face_oblique':Vector((-.62,-1.05,1.55))},expected_contract_sha256=smile_input_sha)
except SmileVerificationError as error:
    (OUT/'reference-smile-gate.json').write_text(json.dumps(error.report,indent=2)+'\n',encoding='utf-8')
    raise
(OUT/'reference-smile-gate.json').write_text(json.dumps(smile_gate,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'sailor_character.blend'),compress=True)
print('SCENE_READY: '+str(OUT/'sailor_character.blend'),flush=True)

"""Two embedded brow ribbons from the asset's consistent UV disks."""
import hashlib
import math
from array import array


def smooth(a,b,x):
    t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)


def fit_uv_brows(obj,body):
    import bpy
    from mathutils import Matrix,Vector
    assert obj.matrix_world==body.matrix_world==Matrix.Identity(4)
    assert len(obj.data.vertices)==124 and len(obj.data.polygons)==96
    layer=obj.data.uv_layers.active;uv={}
    for polygon in obj.data.polygons:
        for vi,li in zip(polygon.vertices,polygon.loop_indices):
            point=tuple(layer.data[li].uv)
            assert vi not in uv or uv[vi]==point,'Brow vertex has an inconsistent UV seam.'
            uv[vi]=point
    assert len(uv)==124
    image=next(n.image for n in obj.active_material.node_tree.nodes if n.type=='TEX_IMAGE')
    assert [hashlib.sha256(p.packed_file.data).hexdigest() for p in image.packed_files]==['1827b24aaa1c928353027c5a86b8db59c1c22f06258b18faa2117d81f5ff9b05'], 'Unexpected eyebrow texture.'
    width,height=image.size;assert (width,height)==(512,512)
    pixels=array('f',[0.])*(width*height*4);image.pixels.foreach_get(pixels)
    result=[None]*124;profiles={};skin=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    for side in (-1,1):
        ids=[v.index for v in obj.data.vertices if v.co.x*side>0];assert len(ids)==62
        umin,umax=min(uv[i][0] for i in ids),max(uv[i][0] for i in ids)
        vmin,vmax=min(uv[i][1] for i in ids),max(uv[i][1] for i in ids)
        xmin,xmax=min(obj.data.vertices[i].co.x for i in ids),max(obj.data.vertices[i].co.x for i in ids)
        moments=[]
        for column in range(width):
            mass=weighted=0.
            for row in range(height):
                v=(row+.5)/height
                if vmin<=v<=vmax:
                    alpha=pixels[4*(row*width+column)+3];mass+=alpha;weighted+=alpha*v
            moments.append((mass,weighted))
        profiles[side]=[]
        for i in ids:
            u,v=uv[i];s=(u-umin)/(umax-umin);t=s if side>0 else 1-s
            weights=[math.exp(-.5*(((j+.5)/width-u)/.025)**2) for j in range(width)]
            denominator=sum(w*m[0] for w,m in zip(weights,moments));assert denominator>0
            center_v=sum(w*m[1] for w,m in zip(weights,moments))/denominator
            x=xmin+s*(xmax-xmin)
            center_z=1.5538+.0008*math.sin(math.pi*t)-.0016*smooth(.6,1.,t)
            z=center_z+.065*(v-center_v)
            hit,location,normal,face=skin.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)))
            assert hit,'New brow parameter point has no forehead support.'
            result[i]=(x,location.y-.00045,z)
            profiles[side].append({'row':i,'uv':[u,v],'anatomical_t':t,'alpha_center_v':center_v,'center_z':center_z,'point':result[i]})
    return result,profiles

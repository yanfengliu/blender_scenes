"""Sailor collar cut directly from the single evaluated blouse surface.

Every collar triangle is a clipped part of an existing garment triangle. The
actual blouse neck opening is retained. There is no projection, remeshing, or
subdivision after clipping. Opaque shader bands share the cloth geometry.
The inherited surface and normal offset do not certify appearance or likeness;
the integrated scene still requires front, profile, and back render inspection.
"""
import math
from collections import Counter


def _back_weight(y):
    t=max(0.0,min(1.0,(y+.075)/.05))
    return t*t*(3.0-2.0*t)


def _lower_bound(point):
    x,y,_=point
    back=_back_weight(y)
    return (1.220+.774*abs(x))*(1-back)+1.258*back


def _inner_bound(point):
    x,y,_=point
    # The front neck surface lies behind the chest. Keep its V straight until
    # the patch turns around the side of the neck, rather than blending early.
    t=max(0.0,min(1.0,(y+.020)/.040))
    back=t*t*(3.0-2.0*t)
    # On the back the real garment neckline supplies the boundary. The 1.6 m
    # limit is above this blouse, so it does not manufacture a neck cap.
    return (1.237+3.149*abs(x))*(1-back)+1.600*back


def _interpolate(a,b,t):
    return tuple(tuple(a[k][i]+t*(b[k][i]-a[k][i]) for i in range(3)) for k in range(2))


def _clip_polygon(polygon,field):
    """Clip on linearly sampled fields; interpolants stay on the source triangle."""
    if not polygon:return []
    result=[]
    previous=polygon[-1]
    previous_value=field(previous[0])
    for current in polygon:
        value=field(current[0])
        if (previous_value>=0)!=(value>=0):
            result.append(_interpolate(previous,current,previous_value/(previous_value-value)))
        if value>=0:result.append(current)
        previous,previous_value=current,value
    return result


def _outer_distance(point):
    x,y,z=point
    t=max(0.0,min(1.0,(y+.075)/.05))
    back=_back_weight(y)
    dz_dx=.774*(1-back)
    dz_dy=(1.258-(1.220+.774*abs(x)))*6*t*(1-t)/.05
    lower=(z-_lower_bound(point))/math.sqrt(1+dz_dx*dz_dx+dz_dy*dz_dy)
    return max(0.0,min(.155-abs(x),lower))


def _clipped_surface(triangles):
    """Return a welded clipped mesh and interpolated support normals."""
    points=[]
    normals=[]
    faces=[]
    lookup={}
    for triangle in triangles:
        # Splitting on the center plane makes both arms of the front V linear.
        polygons=[triangle]
        if min(v[0][0] for v in triangle)<0<max(v[0][0] for v in triangle):
            polygons=[_clip_polygon(triangle,lambda p:p[0]),
                      _clip_polygon(triangle,lambda p:-p[0])]
        for polygon in polygons:
            for field in (lambda p:p[0]+.155,lambda p:.155-p[0],
                          lambda p:p[2]-_lower_bound(p),
                          lambda p:_inner_bound(p)-p[2]):
                polygon=_clip_polygon(polygon,field)
                if len(polygon)<3:break
            if len(polygon)<3:continue
            indices=[]
            for point,normal in polygon:
                key=tuple(round(value,8) for value in point)
                if key not in lookup:
                    lookup[key]=len(points)
                    points.append(point)
                    length=math.sqrt(sum(value*value for value in normal))
                    if length<1e-8:raise RuntimeError('Clipped collar has a zero interpolated blouse normal.')
                    normals.append(tuple(value/length for value in normal))
                index=lookup[key]
                if not indices or index!=indices[-1]:indices.append(index)
            if len(indices)>1 and indices[0]==indices[-1]:indices.pop()
            for i in range(1,len(indices)-1):
                face=(indices[0],indices[i],indices[i+1])
                if len(set(face))==3:faces.append(face)
    if not faces:raise RuntimeError('Collar clipping retained no blouse triangles within the requested V and rear bounds.')
    used=set(index for face in faces for index in face)
    remap={old:new for new,old in enumerate(sorted(used))}
    return ([points[i] for i in sorted(used)],[normals[i] for i in sorted(used)],
            [tuple(remap[i] for i in face) for face in faces])


def _band_material(material,braid_material):
    """Two opaque 1.5 mm ivory bands, centered 3 and 6 mm from the outer edge."""
    result=material.copy()
    result.name='Collar / navy cloth with woven ivory edge bands'
    result.use_nodes=True
    nodes,links=result.node_tree.nodes,result.node_tree.links
    shader=next(node for node in nodes if node.type=='BSDF_PRINCIPLED')
    braid_shader=next((node for node in braid_material.node_tree.nodes if node.type=='BSDF_PRINCIPLED'),None)
    ivory=tuple(braid_shader.inputs['Base Color'].default_value) if braid_shader else tuple(braid_material.diffuse_color)
    attribute=nodes.new('ShaderNodeAttribute');attribute.attribute_name='Collar outer edge distance'
    masks=[]
    for inset in (.003,.006):
        delta=nodes.new('ShaderNodeMath');delta.operation='SUBTRACT';delta.inputs[1].default_value=inset
        links.new(attribute.outputs['Fac'],delta.inputs[0])
        absolute=nodes.new('ShaderNodeMath');absolute.operation='ABSOLUTE'
        links.new(delta.outputs[0],absolute.inputs[0])
        band=nodes.new('ShaderNodeMath');band.operation='LESS_THAN';band.inputs[1].default_value=.00075
        links.new(absolute.outputs[0],band.inputs[0]);masks.append(band)
    union=nodes.new('ShaderNodeMath');union.operation='MAXIMUM'
    for index,mask in enumerate(masks):links.new(mask.outputs[0],union.inputs[index])
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX'
    mix.inputs[1].default_value=shader.inputs['Base Color'].default_value
    mix.inputs[2].default_value=ivory
    for link in list(shader.inputs['Base Color'].links):
        links.new(link.from_socket,mix.inputs[1]);links.remove(link)
    links.new(union.outputs[0],mix.inputs[0]);links.new(mix.outputs[0],shader.inputs['Base Color'])
    return result


def build_collar(blouse,collection,material,braid_material):
    import bpy

    # Evaluate only the original outward surface: Solidify would duplicate it
    # into an inner shell. Restore every modifier flag even if extraction fails.
    solidifiers=[modifier for modifier in blouse.modifiers if modifier.type=='SOLIDIFY']
    visibility=[modifier.show_viewport for modifier in solidifiers]
    evaluated=None
    try:
        for modifier in solidifiers:modifier.show_viewport=False
        bpy.context.view_layer.update()
        evaluated=blouse.evaluated_get(bpy.context.evaluated_depsgraph_get())
        surface=evaluated.to_mesh();surface.calc_loop_triangles()
        transform=blouse.matrix_world
        normal_transform=transform.to_3x3().inverted().transposed()
        source=[(tuple(transform@vertex.co),tuple((normal_transform@vertex.normal).normalized()))
                for vertex in surface.vertices]
        triangles=[[source[index] for index in triangle.vertices] for triangle in surface.loop_triangles]
    finally:
        if evaluated is not None:evaluated.to_mesh_clear()
        for modifier,visible in zip(solidifiers,visibility):modifier.show_viewport=visible
        bpy.context.view_layer.update()

    support,normals,faces=_clipped_surface(triangles)
    # Blouse Solidify extends 1.3 mm outward. This leaves 1.0 mm between the
    # blouse outer surface and the 0.6 mm collar's inner surface at samples.
    offset=.0026
    points=[tuple(point[i]+offset*normal[i] for i in range(3)) for point,normal in zip(support,normals)]
    data=bpy.data.meshes.new('Collar mesh / clipped evaluated blouse triangles')
    data.from_pydata(points,[],faces);data.update()
    for polygon in data.polygons:polygon.use_smooth=True
    # Keep Solidify's rim normals separate from the supported outer fabric.
    # Candidate 7's smooth boundary tilted outward normals by 42 to 52 degrees.
    edge_uses=Counter(tuple(sorted(edge)) for face in faces
                      for edge in zip(face,face[1:]+face[:1]))
    for edge in data.edges:
        if edge_uses[tuple(sorted(edge.vertices))]==1:edge.use_edge_sharp=True
    data.update()
    distance=data.attributes.new(name='Collar outer edge distance',type='FLOAT',domain='POINT')
    for item,point in zip(distance.data,support):item.value=_outer_distance(point)
    obj=bpy.data.objects.new('Sailor collar / continuous fitted fabric',data)
    collection.objects.link(obj)
    data.materials.append(_band_material(material,braid_material))
    thickness=obj.modifiers.new('Woven collar thickness / 0.6 mm','SOLIDIFY')
    thickness.thickness=.0006;thickness.offset=0
    obj['fit']='Clipped directly from the evaluated single blouse surface; interpolated outward-normal offset; no projection or refinement.'
    obj['support_offset_m']=offset
    obj['source_triangle_count']=len(triangles)
    obj['retained_triangle_count']=len(faces)
    obj['verification_bound']='Inherited triangle support before normal offset; linear clipping samples the smooth front/back bounds. Integrated multi-view render inspection is required.'
    return obj

"""Local adult facial expression and continuous photographic skin shading.

This is an editable 3D surface treatment, not a projected portrait or a rendered
image correction. Geometry keeps the MakeHuman vertex indices and UV topology.
The expression and region functions are pure Python for bounded preflight checks;
Blender is imported only by the material builders. Visual likeness still needs
the four fixed-camera comparisons against the generated adult-20 reference.
"""
import math


def smoothstep(a, b, value):
    t = max(0.0, min(1.0, (value - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def shape_expression(native):
    """Coordinate a small closed smile through corners, cheeks and lip contact.

    Native X is lateral, Y vertical, Z forward. All deltas are continuous, local
    and below 2.5 mm at the scene's scale. The scalp, ears, neck, jaw outline and
    body pose stay unchanged. Proxy fits run after this change.
    """
    vertices = native['vertices']
    mouth_y = sum(vertices[i][1] for i in (520, 537, 540, 523)) / 4.0
    eye_y = sum(vertices[i][1] for i in native['groups']['joint-l-eye']) / len(native['groups']['joint-l-eye'])
    for v in vertices:
        x, y, z = v
        front = smoothstep(1.10, 1.24, z)
        if not front or not mouth_y - .15 < y < eye_y:
            continue
        corner = math.exp(-((abs(x) - .205) / .115) ** 2 - ((y - mouth_y - .018) / .11) ** 2) * front
        cheek = math.exp(-((abs(x) - .33) / .18) ** 2 - ((y - eye_y + .28) / .20) ** 2) * front
        # Close the lower contact edge across the smile, including its corners.
        # The previous center-only lift left two visible corner slits.
        contact_y = mouth_y + .018 * min((x / .20) ** 2, 1.0)
        contact = 0.0
        if y < contact_y:
            contact = .010 * math.exp(-(x / .24) ** 6 - ((y - contact_y) / .060) ** 2) * front
        v[0] += (.0045 if x >= 0 else -.0045) * corner
        v[1] += .012 * corner + .010 * cheek + contact
        v[2] += .006 * cheek - .001 * corner
    return mouth_y


def skin_regions(point, lip_center_z):
    """Return continuous RGB tone gain, oil, lip and cheek masks in meters."""
    x, y, z = point
    front = 1.0 - smoothstep(-.055, -.015, y)
    head = smoothstep(1.405, 1.485, z)
    # The source UV photograph is lighter on the forehead than the limbs, and
    # substantially darker around the knees. These are broad corrections, not
    # a whitening mask: the original mottling and anatomy remain in the albedo.
    lower_limb = smoothstep(.30, .43, z) * (1.0 - smoothstep(.57, .77, z))
    # Source medians in linear RGB: knee (.506,.238,.156), forearm
    # (.687,.418,.296). A scalar lift leaves the knee disproportionately red.
    # Per-channel partial normalization keeps local texture and some pigmentation.
    # The face red level stays at candidate 1's value; G/B are reduced modestly
    # because its rendered cheeks were 216/197/187 vs reference 220/177/164.
    tone_gain = (1.0 - .10 * head + .30 * lower_limb,
                 1.0 - .16 * head + .60 * lower_limb,
                 1.0 - .14 * head + .75 * lower_limb)
    nose = math.exp(-(x / .017) ** 2 - ((z - 1.515) / .031) ** 2)
    forehead = math.exp(-(x / .044) ** 4 - ((z - 1.577) / .025) ** 4)
    chin = math.exp(-(x / .024) ** 2 - ((z - 1.446) / .013) ** 2)
    oil = min(1.0, max(nose, .65 * forehead, .45 * chin) * front)
    lip = math.exp(-(x / .022) ** 6 - ((z - lip_center_z) / .0065) ** 4) * (1.0 - smoothstep(-.125, -.105, y))
    cheek = math.exp(-((abs(x) - .042) / .018) ** 2 - ((z - 1.507) / .017) ** 2) * front
    return tone_gain, oil, lip, cheek


def fit_fuller_brows(coords, body):
    """Flatten the sharp arch, thicken the existing hair texture, refit to skin.

    The source brow has a roughly 10 mm inner-to-outer rise. The new centerline
    removes 3.5 mm of that rise; only the local ribbon thickness is enlarged.
    Rays use body-local coordinates. The source scene keeps body and brows in
    the same identity frame, which is asserted instead of silently assumed.
    """
    import bpy
    from mathutils import Matrix, Vector
    if body.matrix_world != Matrix.Identity(4):
        raise ValueError('Fuller eyebrow fitting needs the anatomical body in the scene identity frame.')
    bpy.context.view_layer.update()
    evaluated = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    points = [Vector(co) for co in coords]
    result = []
    for point in points:
        neighbors = [(p, math.exp(-((abs(p.x) - abs(point.x)) / .0035) ** 2)) for p in points if p.x * point.x > 0]
        middle = sum(p.z * weight for p, weight in neighbors) / sum(weight for _, weight in neighbors)
        center_shift = .0012 * (1.0 - smoothstep(.015, .024, abs(point.x))) - .0035 * smoothstep(.016, .045, abs(point.x))
        z = middle + center_shift + 1.65 * (point.z - middle)
        hit, location, normal, face = evaluated.ray_cast(Vector((point.x, -.5, z)), Vector((0, 1, 0)))
        if not hit:
            raise ValueError(f'Eyebrow vertex at x={point.x:.5f}, z={z:.5f} has no forehead support; fix the brow fit.')
        result.append((point.x, location.y - .00045, z))
    return result


def build_skin(path):
    """Single UV albedo with independent color, oil and two-scale normal detail."""
    import bpy
    material = bpy.data.materials.new('Skin / continuous photographed albedo and local surface response')
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Subsurface Weight'].default_value = .085
    shader.inputs['Subsurface Radius'].default_value = (1.0, .42, .22)
    shader.inputs['Subsurface Scale'].default_value = .0012
    shader.inputs['IOR'].default_value = 1.46
    uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'
    photo = nodes.new('ShaderNodeTexImage'); photo.name = 'Original continuous CC0 skin photograph'
    photo.image = bpy.data.images.load(str(path), check_existing=True)
    photo.image.colorspace_settings.name = 'sRGB'; photo.image.pack()
    links.new(uv.outputs['UV'], photo.inputs['Vector'])
    tone = nodes.new('ShaderNodeHueSaturation'); tone.name = 'Whole-body photographic color'
    tone.inputs['Saturation'].default_value = 1.02; tone.inputs['Value'].default_value = .86
    links.new(photo.outputs['Color'], tone.inputs['Color'])
    gain = nodes.new('ShaderNodeVertexColor'); gain.layer_name = 'SkinToneGain'
    corrected = nodes.new('ShaderNodeMixRGB'); corrected.blend_type = 'MULTIPLY'; corrected.inputs[0].default_value = 1
    links.new(tone.outputs['Color'], corrected.inputs[1]); links.new(gain.outputs['Color'], corrected.inputs[2])
    response = nodes.new('ShaderNodeVertexColor'); response.layer_name = 'SkinResponse'
    separate = nodes.new('ShaderNodeSeparateColor'); separate.mode = 'RGB'
    links.new(response.outputs['Color'], separate.inputs['Color'])
    cheek_amount = nodes.new('ShaderNodeMath'); cheek_amount.operation = 'MULTIPLY'; cheek_amount.inputs[1].default_value = .12
    links.new(separate.outputs['Blue'], cheek_amount.inputs[0])
    flush = nodes.new('ShaderNodeMixRGB'); flush.blend_type = 'MULTIPLY'; flush.inputs[2].default_value = (1.035, .92, .93, 1)
    links.new(cheek_amount.outputs[0], flush.inputs[0]); links.new(corrected.outputs[0], flush.inputs[1])
    # Photographic lip color remains textured. Its anatomical mask previously
    # affected only roughness, leaving the lower lip almost the cheek color.
    lips = nodes.new('ShaderNodeMixRGB'); lips.name = 'Muted rose vermilion / preserve photographic detail'
    lips.blend_type = 'MULTIPLY'; lips.inputs[2].default_value = (.92, .76, .79, 1)
    links.new(separate.outputs['Green'], lips.inputs[0]); links.new(flush.outputs[0], lips.inputs[1])
    links.new(lips.outputs[0], shader.inputs['Base Color'])
    coord = nodes.new('ShaderNodeTexCoord')

    def noise(name, scale, detail):
        node = nodes.new('ShaderNodeTexNoise'); node.name = name
        node.inputs['Scale'].default_value = scale; node.inputs['Detail'].default_value = detail
        links.new(coord.outputs['Object'], node.inputs['Vector'])
        return node

    def remap(socket, low, high, name):
        node = nodes.new('ShaderNodeMapRange'); node.name = name
        node.inputs['From Min'].default_value = 0; node.inputs['From Max'].default_value = 1
        node.inputs['To Min'].default_value = low; node.inputs['To Max'].default_value = high
        links.new(socket, node.inputs['Value'])
        return node.outputs['Result']

    # Oil regions and centimeter-scale roughness are independent of pores. The
    # old graph drove bump and roughness with the same uniform high-frequency noise.
    oil_rough = remap(separate.outputs['Red'], .44, .32, 'Cheek-to-T-zone roughness')
    macro = noise('Broad uneven surface oils / 26 mm', 38, 2.5)
    modulation = remap(macro.outputs['Fac'], -.02, .02, 'Local roughness variation')
    add = nodes.new('ShaderNodeMath'); add.operation = 'ADD'
    links.new(oil_rough, add.inputs[0]); links.new(modulation, add.inputs[1])
    lip_rough = nodes.new('ShaderNodeMixRGB'); lip_rough.inputs[2].default_value = (.30, .30, .30, 1)
    links.new(separate.outputs['Green'], lip_rough.inputs[0]); links.new(add.outputs[0], lip_rough.inputs[1])
    links.new(lip_rough.outputs[0], shader.inputs['Roughness'])
    specular = remap(separate.outputs['Red'], .40, .40, 'Local specular oil response')
    links.new(specular, shader.inputs['Specular IOR Level'])
    pores = noise('Visible skin pores / 0.42 mm', 2400, 2.3)
    pore_bump = nodes.new('ShaderNodeBump'); pore_bump.name = 'Small pore relief'
    pore_bump.inputs['Strength'].default_value = .38; pore_bump.inputs['Distance'].default_value = .000045
    links.new(pores.outputs['Fac'], pore_bump.inputs['Height'])
    fine = noise('Fine epidermis / 0.13 mm', 7800, 1.3)
    fine_bump = nodes.new('ShaderNodeBump'); fine_bump.name = 'Fine epidermal relief'
    fine_bump.inputs['Strength'].default_value = .22; fine_bump.inputs['Distance'].default_value = .000012
    links.new(fine.outputs['Fac'], fine_bump.inputs['Height']); links.new(pore_bump.outputs['Normal'], fine_bump.inputs['Normal'])
    links.new(fine_bump.outputs['Normal'], shader.inputs['Normal'])
    return material


def attach_skin_regions(body, reference_coordinates=None):
    """Store masks on vertex identities, optionally before a local shape edit."""
    points = ([v.co for v in body.data.vertices] if reference_coordinates is None
              else reference_coordinates)
    if len(points) != len(body.data.vertices) or any(not math.isfinite(c) for p in points for c in p):
        raise ValueError('Skin-region reference coordinates must contain one finite point for every anatomical vertex.')
    gain = body.data.color_attributes.new(name='SkinToneGain', type='FLOAT_COLOR', domain='CORNER')
    response = body.data.color_attributes.new(name='SkinResponse', type='FLOAT_COLOR', domain='CORNER')
    lip_center = (points[509][2] + points[495][2]) / 2.0
    for loop in body.data.loops:
        g, oil, lip, cheek = skin_regions(points[loop.vertex_index], lip_center)
        gain.data[loop.index].color = (*g, 1)
        response.data[loop.index].color = (oil, lip, cheek, 1)


def soften_iris_color(material):
    """Register brown iris color and one wet-surface lobe to the texture limbus.

    The pinned 1024px brown_eye asset's 720-ray boundary census gives the two
    centers below, with a maximum 3.65px circular-fit residual. The 112–128px
    transition spans the dark rim. Color-filtered samples in the fitted-center
    135–165px ring stay unchanged; this is not independent whole-sclera
    segmentation. Native multi-view review remains necessary.
    """
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    image = next(n for n in nodes if n.type == 'TEX_IMAGE')
    uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'
    links.new(uv.outputs['UV'], image.inputs['Vector'])
    distances = []
    for center in ((.289061368554985, .2901778246762782, 0),
                   (.7050885844462438, .7022999938386068, 0)):
        distance = nodes.new('ShaderNodeVectorMath'); distance.operation = 'DISTANCE'; distance.inputs[1].default_value = center
        links.new(uv.outputs['UV'], distance.inputs[0]); distances.append(distance.outputs['Value'])
    nearest = nodes.new('ShaderNodeMath'); nearest.operation = 'MINIMUM'
    links.new(distances[0], nearest.inputs[0]); links.new(distances[1], nearest.inputs[1])
    mask = nodes.new('ShaderNodeMapRange'); mask.interpolation_type = 'SMOOTHSTEP'
    mask.inputs['From Min'].default_value = 112/1024; mask.inputs['From Max'].default_value = 128/1024
    mask.inputs['To Min'].default_value = 1; mask.inputs['To Max'].default_value = 0
    links.new(nearest.outputs[0], mask.inputs['Value'])
    brown = nodes.new('ShaderNodeHueSaturation'); brown.name = 'Natural brown iris, subdued red rim'
    brown.inputs['Saturation'].default_value = .62; brown.inputs['Value'].default_value = .92
    links.new(image.outputs['Color'], brown.inputs['Color'])
    mix = nodes.new('ShaderNodeMixRGB')
    links.new(mask.outputs['Result'], mix.inputs[0]); links.new(image.outputs['Color'], mix.inputs[1]); links.new(brown.outputs['Color'], mix.inputs[2])
    links.new(mix.outputs[0], shader.inputs['Base Color'])
    roughness = nodes.new('ShaderNodeMapRange'); roughness.name = 'Registered iris and sclera roughness'
    roughness.inputs['From Min'].default_value = 0; roughness.inputs['From Max'].default_value = 1
    roughness.inputs['To Min'].default_value = .27; roughness.inputs['To Max'].default_value = .10
    links.new(mask.outputs['Result'], roughness.inputs['Value'])
    links.new(roughness.outputs['Result'], shader.inputs['Roughness'])

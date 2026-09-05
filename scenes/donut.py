"""Procedural strawberry donut. Execute in a fresh Blender via Blender Lab MCP.

No downloaded models or textures. All geometry and materials remain editable.
"""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector
from mathutils.noise import noise_vector

random.seed(23)
TAU = math.tau
output = Path(globals().get('OUTPUT_DIR', str(Path.cwd() / 'outputs/donut')))
output.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)


def srgb(hex_color):
    values = [int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v < .04045 else ((v + .055) / 1.055) ** 2.4 for v in values) + (1,)


def material(name, color, roughness=.4):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = srgb(color)
    bsdf.inputs['Roughness'].default_value = roughness
    mat.diffuse_color = srgb(color)
    return mat, bsdf, mat.node_tree.nodes, mat.node_tree.links


def mesh_object(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for poly in mesh.polygons:
        poly.use_smooth = True
    return obj


def ramp(nodes, colors):
    node = nodes.new('ShaderNodeValToRGB')
    cr = node.color_ramp
    cr.elements.remove(cr.elements[1])
    for index, (position, color) in enumerate(colors):
        el = cr.elements[0] if index == 0 else cr.elements.new(position)
        el.position, el.color = position, srgb(color)
    return node


# Toasted crust, a pale proofing band, and fine open pores at two scales.
dough, p, n, l = material('Dough | golden fried crust and pale proof line', 'BC6A25', .54)
p.inputs['Subsurface Weight'].default_value = .035
p.inputs['Subsurface Radius'].default_value = (.18, .065, .025)
geo = n.new('ShaderNodeNewGeometry')
noise = n.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 3.9
noise.inputs['Detail'].default_value = 4
l.new(geo.outputs['Position'], noise.inputs['Vector'])
crust = ramp(n, [(.16, '70300E'), (.35, 'A84C13'), (.57, 'CF782C'), (.8, 'EAA24A')])
l.new(noise.outputs['Fac'], crust.inputs[0])
sep = n.new('ShaderNodeSeparateXYZ')
l.new(geo.outputs['Position'], sep.inputs[0])
subtract = n.new('ShaderNodeMath'); subtract.operation = 'SUBTRACT'; subtract.inputs[1].default_value = .55
l.new(sep.outputs['Z'], subtract.inputs[0])
absolute = n.new('ShaderNodeMath'); absolute.operation = 'ABSOLUTE'
l.new(subtract.outputs[0], absolute.inputs[0])
band = n.new('ShaderNodeMapRange')
band.inputs['From Min'].default_value = .022
band.inputs['From Max'].default_value = .145
band.inputs['To Min'].default_value = .72
band.inputs['To Max'].default_value = 0
l.new(absolute.outputs[0], band.inputs['Value'])
mix = n.new('ShaderNodeMixRGB')
l.new(band.outputs['Result'], mix.inputs[0]); l.new(crust.outputs['Color'], mix.inputs[1]); mix.inputs[2].default_value = srgb('EAB96D')
l.new(mix.outputs[0], p.inputs['Base Color'])
pores = n.new('ShaderNodeTexNoise'); pores.inputs['Scale'].default_value = 155; pores.inputs['Detail'].default_value = 3; pores.inputs['Roughness'].default_value = .8
l.new(geo.outputs['Position'], pores.inputs['Vector'])
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .58; bump.inputs['Distance'].default_value = .045
l.new(pores.outputs['Fac'], bump.inputs['Height'])
vor = n.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 65
l.new(geo.outputs['Position'], vor.inputs['Vector'])
pit = n.new('ShaderNodeValToRGB')
pit.color_ramp.elements[0].position = .1; pit.color_ramp.elements[1].position = .32
l.new(vor.outputs['Distance'], pit.inputs[0])
bump2 = n.new('ShaderNodeBump'); bump2.inputs['Strength'].default_value = .42; bump2.inputs['Distance'].default_value = .022
l.new(pit.outputs[0], bump2.inputs['Height']); l.new(bump.outputs[0], bump2.inputs['Normal']); l.new(bump2.outputs[0], p.inputs['Normal'])

icing, p, n, l = material('Glaze | strawberry fondant', 'DB6C89', .28)
p.inputs['Subsurface Weight'].default_value = .045
p.inputs['Subsurface Radius'].default_value = (.1, .035, .03)
p.inputs['Coat Weight'].default_value = .18
p.inputs['Coat Roughness'].default_value = .2
tex = n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 5; tex.inputs['Detail'].default_value = 3
color = ramp(n, [(.15, 'D36B88'), (.8, 'E1819B')]); l.new(tex.outputs['Fac'], color.inputs[0]); l.new(color.outputs[0], p.inputs['Base Color'])
micro = n.new('ShaderNodeTexNoise'); micro.inputs['Scale'].default_value = 190
ibump = n.new('ShaderNodeBump'); ibump.inputs['Strength'].default_value = .12; ibump.inputs['Distance'].default_value = .009
l.new(micro.outputs['Fac'], ibump.inputs['Height']); l.new(ibump.outputs[0], p.inputs['Normal'])


def surface(u, v, offset=0):
    major = 1.105 + .025 * math.sin(3 * u + .5) + .015 * math.sin(7 * u)
    minor = .554 * (1 + .055 * math.sin(4 * u + 1) + .026 * math.cos(9 * u))
    co = Vector(((major + minor * math.cos(v)) * math.cos(u), (major + minor * math.cos(v)) * math.sin(u), .603 + .447 * math.sin(v)))
    normal = Vector((math.cos(v) * math.cos(u), math.cos(v) * math.sin(u), math.sin(v)))
    wobble = noise_vector(co * 4.1)[0] * .018 + noise_vector(co * 19)[1] * .0035
    co += normal * (wobble + offset)
    co.z += .015 * math.sin(5 * u + .6) + .008 * math.cos(8 * u + v)
    co.z = max(co.z, .156 + .001 * math.sin(5 * u))
    return co


nu, nv = 256, 112
verts = [surface(TAU * i / nu, TAU * j / nv) for i in range(nu) for j in range(nv)]
faces = [(i * nv + j, ((i + 1) % nu) * nv + j, ((i + 1) % nu) * nv + (j + 1) % nv, i * nv + (j + 1) % nv) for i in range(nu) for j in range(nv)]
body = mesh_object('Donut | hand-shaped raised dough', verts, faces, dough)
sub = body.modifiers.new('Soft handmade surface', 'SUBSURF'); sub.levels = 1

drips = [(TAU * i / 11 + random.uniform(-.20, .20), random.uniform(.35, .95), random.uniform(.07, .145)) for i in range(11)]


def edge(u, inner=False):
    if inner:
        return math.pi - .2 + .12 * math.sin(6 * u) + .1 * math.sin(9 * u + 1)
    val = .48 + .075 * math.sin(5 * u) + .045 * math.cos(13 * u)
    for center, depth, width in drips:
        distance = (u - center + math.pi) % TAU - math.pi
        val -= depth * math.exp(-.5 * (distance / width) ** 2)
    return val


ni = 80
verts = []
for i in range(nu):
    u = TAU * i / nu
    outer, inner = edge(u), edge(u, True)
    for j in range(ni + 1):
        t = j / ni
        v = outer * (1 - t) + inner * t
        # A rounded thicker edge catches a narrow, realistic glaze highlight.
        lip = .011 * (math.exp(-t * 45) + math.exp(-(1 - t) * 45))
        verts.append(surface(u, v, .027 + lip))
faces = [(i * (ni + 1) + j, ((i + 1) % nu) * (ni + 1) + j, ((i + 1) % nu) * (ni + 1) + j + 1, i * (ni + 1) + j + 1) for i in range(nu) for j in range(ni)]
glaze = mesh_object('Icing | flowing strawberry glaze', verts, faces, icing)
solid = glaze.modifiers.new('Real glaze thickness', 'SOLIDIFY'); solid.thickness = .021; solid.offset = -.35
sub = glaze.modifiers.new('Rounded drip edges', 'SUBSURF'); sub.levels = 1

# Real capsule geometry, placed against the local icing tangent with varied spacing.
sprinkle_mats = [material('Sugar | ' + name, color, .3)[0] for name, color in [('vanilla', 'F8E7B2'), ('raspberry', 'C93555'), ('pistachio', '8DB889'), ('cocoa', '503026'), ('lemon', 'EFC965'), ('white', 'F9F3E6')]]
capsule_verts, capsule_faces = [], []
radius, length = .015, .1
profile = []
for j in range(7):
    a = -math.pi / 2 + j * math.pi / 12
    profile.append((-length / 2 + radius * math.sin(a), max(.0001, radius * math.cos(a))))
for j in range(7):
    a = j * math.pi / 12
    profile.append((length / 2 + radius * math.sin(a), max(.0001, radius * math.cos(a))))
for z, r in profile:
    for k in range(10): capsule_verts.append((r * math.cos(TAU * k / 10), r * math.sin(TAU * k / 10), z))
for j in range(len(profile) - 1):
    for k in range(10): capsule_faces.append((j * 10 + k, j * 10 + (k + 1) % 10, (j + 1) * 10 + (k + 1) % 10, (j + 1) * 10 + k))
meshes = []
for mat in sprinkle_mats:
    mesh = bpy.data.meshes.new(mat.name + ' capsule'); mesh.from_pydata(capsule_verts, [], capsule_faces); mesh.materials.append(mat)
    for poly in mesh.polygons: poly.use_smooth = True
    meshes.append(mesh)
sprinkles = bpy.data.collections.new('Sprinkles | individual sugar pieces'); bpy.context.scene.collection.children.link(sprinkles)
placed = []
for idx in range(205):
    for attempt in range(40):
        u = random.uniform(0, TAU); v = random.uniform(.34, math.pi - .42)
        pos = surface(u, v, .053)
        if all((pos - other).length > .095 for other in placed): break
    else: continue
    placed.append(pos)
    tu = (surface(u + .001, v) - surface(u - .001, v)).normalized()
    tv = (surface(u, v + .001) - surface(u, v - .001)).normalized()
    angle = random.uniform(0, TAU)
    direction = tu * math.cos(angle) + tv * math.sin(angle)
    obj = bpy.data.objects.new(f'Sprinkle {idx + 1:03}', random.choice(meshes)); sprinkles.objects.link(obj)
    obj.location = pos; obj.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    obj.scale = (random.uniform(.85, 1.2), random.uniform(.85, 1.2), random.uniform(.6, 1.3))


def lathe(name, profile, mat, center=(0, 0, 0), segments=192):
    verts = [(center[0] + r * math.cos(TAU * i / segments), center[1] + r * math.sin(TAU * i / segments), center[2] + z) for r, z in profile for i in range(segments)]
    faces = [(j * segments + i, j * segments + (i + 1) % segments, (j + 1) * segments + (i + 1) % segments, (j + 1) * segments + i) for j in range(len(profile) - 1) for i in range(segments)]
    return mesh_object(name, verts, faces, mat)


ceramic, p, n, l = material('Porcelain | warm ivory glaze', 'DDD9CA', .2)
p.inputs['Coat Weight'].default_value = .28
noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 220
bump = n.new('ShaderNodeBump'); bump.inputs['Distance'].default_value = .002; bump.inputs['Strength'].default_value = .12
l.new(noise.outputs['Fac'], bump.inputs['Height']); l.new(bump.outputs[0], p.inputs['Normal'])
plate = lathe('Plate | wheel-thrown porcelain', [(.001, .155), (1.65, .155), (1.81, .17), (1.96, .22), (2.16, .29), (2.29, .32), (2.33, .315), (2.35, .285), (2.33, .25), (2.13, .2), (1.88, .125), (1.35, .065), (1.28, .03), (1.19, .03), (1.16, .075), (.001, .105)], ceramic)
sub = plate.modifiers.new('Soft porcelain profile', 'SUBSURF'); sub.levels = 2

# Tiny crumbs make the otherwise clean still life feel handled.
bpy.context.view_layer.update()
plate_evaluated = plate.evaluated_get(bpy.context.evaluated_depsgraph_get())
for i in range(32):
    a = random.uniform(0, TAU); r = random.uniform(1.72, 2.1)
    x, y = r * math.cos(a), r * math.sin(a)
    size = random.uniform(.008, .024)
    hit, contact, _, _ = plate_evaluated.ray_cast(Vector((x, y, 2)), Vector((0, 0, -1)))
    if not hit:
        raise RuntimeError('Crumb ray did not hit the plate')
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=size, location=(x, y, contact.z + size * .59))
    crumb = bpy.context.object; crumb.name = 'Crumb'; crumb.scale = (1.4, 1, .7); crumb.data.materials.append(dough)

stone, p, n, l = material('Table | deep sage limestone', '58645C', .66)
tex = n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 4; tex.inputs['Detail'].default_value = 5
cr = ramp(n, [(.1, '424C47'), (.9, '768075')]); l.new(tex.outputs['Fac'], cr.inputs[0]); l.new(cr.outputs[0], p.inputs['Base Color'])
tex2 = n.new('ShaderNodeTexNoise'); tex2.inputs['Scale'].default_value = 140
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .2; bump.inputs['Distance'].default_value = .014
l.new(tex2.outputs['Fac'], bump.inputs['Height']); l.new(bump.outputs[0], p.inputs['Normal'])
bpy.ops.mesh.primitive_plane_add(size=200); bpy.context.object.name = 'Tabletop'; bpy.context.object.data.materials.append(stone)

linen, p, n, l = material('Linen | oatmeal weave', 'B8AB91', .88)
coordinates = n.new('ShaderNodeTexCoord')
warp = n.new('ShaderNodeTexWave'); warp.bands_direction = 'X'; warp.inputs['Scale'].default_value = 100; warp.inputs['Distortion'].default_value = .5
weft = n.new('ShaderNodeTexWave'); weft.bands_direction = 'Y'; weft.inputs['Scale'].default_value = 100; weft.inputs['Distortion'].default_value = .5
l.new(coordinates.outputs['Object'], warp.inputs['Vector']); l.new(coordinates.outputs['Object'], weft.inputs['Vector'])
weave = n.new('ShaderNodeMath'); weave.operation = 'MULTIPLY'; l.new(warp.outputs['Fac'], weave.inputs[0]); l.new(weft.outputs['Fac'], weave.inputs[1])
bump = n.new('ShaderNodeBump'); bump.inputs['Distance'].default_value = .008; bump.inputs['Strength'].default_value = .45
l.new(weave.outputs[0], bump.inputs['Height']); l.new(bump.outputs[0], p.inputs['Normal'])
verts = []
grid = 55
for i in range(grid):
    for j in range(grid):
        x = (i / (grid - 1) - .5) * 2.7; y = (j / (grid - 1) - .5) * 3.9
        z = .006 + .010 * math.sin(y * 6 + x * 1.8) ** 2 + .009 * math.sin(x * 9 + y * 2) ** 2
        verts.append((x, y, z))
faces = [(i * grid + j, (i + 1) * grid + j, (i + 1) * grid + j + 1, i * grid + j + 1) for i in range(grid - 1) for j in range(grid - 1)]
cloth = mesh_object('Linen | softly rumpled napkin', verts, faces, linen); cloth.location = (-2.35, 1.1, .002); cloth.rotation_euler.z = -.35
solid = cloth.modifiers.new('Woven cloth thickness', 'SOLIDIFY'); solid.thickness = .014
sub = cloth.modifiers.new('Soft folds', 'SUBSURF'); sub.levels = 1

cupmat, p, n, l = material('Cup | speckled charcoal ceramic', '36443F', .26)
cup = lathe('Cup | morning coffee', [(.001, .065), (.47, .065), (.53, .12), (.59, .9), (.57, 1.02), (.545, 1.03), (.52, 1.0), (.515, .9), (.46, .18), (.001, .18)], cupmat, (2.1, 3.5, 0))
sub = cup.modifiers.new('Pottery curves', 'SUBSURF'); sub.levels = 2
coffee = material('Coffee | dark roast', '271008', .16)[0]
lathe('Coffee surface', [(.001, .85), (.518, .85)], coffee, (2.1, 3.5, 0))
bpy.ops.mesh.primitive_torus_add(major_radius=.28, minor_radius=.072, major_segments=64, minor_segments=16, location=(2.69, 3.5, .6), rotation=(math.pi / 2, 0, 0))
handle = bpy.context.object; handle.name = 'Cup handle'; handle.data.materials.append(cupmat)
for poly in handle.data.polygons: poly.use_smooth = True


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def camera(name, location, target, lens, fstop):
    data = bpy.data.cameras.new(name); obj = bpy.data.objects.new(name, data); bpy.context.collection.objects.link(obj)
    obj.location = location; aim(obj, target); data.lens = lens
    data.dof.use_dof = True; data.dof.focus_distance = (Vector(target) - obj.location).length; data.dof.aperture_fstop = fstop
    return obj


hero = camera('Camera_hero', (5.5, -7.5, 6.0), (0, .1, .38), 60, 7.1)
camera('Camera_overhead', (.05, -.05, 9.6), (0, 0, .25), 56, 11)
camera('Camera_detail', (3.25, -4.7, 2.65), (.1, -.4, .66), 65, 10)


def area(name, location, target, power, size, color, shape='DISK', size_y=None):
    data = bpy.data.lights.new(name, 'AREA'); data.energy = power; data.shape = shape; data.size = size; data.color = color
    if size_y is not None: data.size_y = size_y
    obj = bpy.data.objects.new(name, data); bpy.context.collection.objects.link(obj); obj.location = location; aim(obj, target)


area('Key | broad window', (-3.5, -4.2, 6.4), (0, 0, .4), 700, 4.2, (1, .89, .77), 'RECTANGLE', 3.1)
area('Fill | white card', (3.5, -.5, 4), (0, 0, .5), 130, 3, (.84, .9, 1))
area('Rim | soft strip', (-1, 4.5, 5.5), (0, 0, .3), 350, 3, (1, .94, .85), 'RECTANGLE', 1.7)
scene = bpy.context.scene
scene.world.use_nodes = True; scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.38, .43, .5, 1); scene.world.node_tree.nodes['Background'].inputs[1].default_value = .22
scene.camera = hero
scene.render.engine = 'CYCLES'; scene.cycles.samples = globals().get('SAMPLES', 96); scene.cycles.use_denoising = True
scene.cycles.adaptive_threshold = .025
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    gpu = [d for d in prefs.devices if d.type == 'OPTIX']
    if gpu:
        for d in prefs.devices: d.use = d.type == 'OPTIX'
        scene.cycles.device = 'GPU'
except Exception:
    pass
scene.render.resolution_x = globals().get('RENDER_SIZE', 1500); scene.render.resolution_y = int(scene.render.resolution_x * .8); scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGB'; scene.render.image_settings.color_depth = '8'
scene.render.filepath = str(output / 'hero.png')
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.render.film_transparent = False
scene.unit_settings.system = 'METRIC'; scene.unit_settings.scale_length = .035
bpy.context.view_layer.objects.active = body
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True)
for screen in bpy.data.screens:
    for space_area in screen.areas:
        if space_area.type == 'VIEW_3D':
            space_area.spaces.active.region_3d.view_perspective = 'CAMERA'
            space_area.spaces.active.shading.type = 'MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(output / 'strawberry_donut.blend'), compress=True)
result = {'blend_file': str(output / 'strawberry_donut.blend'), 'objects': len(scene.objects), 'sprinkles': len(placed), 'engine': scene.render.engine, 'device': scene.cycles.device, 'resolution': [scene.render.resolution_x, scene.render.resolution_y], 'seed': 23}

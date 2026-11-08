"""Create the requested fuller, anatomically defined unclothed adult variant.

Input is the already complete unclothed saved scene. The source file and every
retained face/hair/studio object stay unchanged; this saves a new editable copy.
"""
import argparse
from array import array
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
from export_character_variant import file_hash, run, BASE_SHA


def mesh_fingerprint(body):
    """Bound saved verification without retaining millions of Python loop rows."""
    mesh = body.data
    def buffer(collection, property_name, width, kind='f'):
        data = array(kind, [0])*len(collection)*width
        collection.foreach_get(property_name, data)
        return hashlib.sha256(data.tobytes()).hexdigest()
    return {'vertices':len(mesh.vertices), 'faces':len(mesh.polygons),
            'coordinates':buffer(mesh.vertices, 'co', 3),
            'loop_vertices':buffer(mesh.loops, 'vertex_index', 1, 'i'),
            'polygon_starts':buffer(mesh.polygons, 'loop_start', 1, 'i'),
            'polygon_sizes':buffer(mesh.polygons, 'loop_total', 1, 'i'),
            'polygon_materials':buffer(mesh.polygons, 'material_index', 1, 'i'),
            'polygon_smooth':hashlib.sha256(bytes(int(p.use_smooth) for p in mesh.polygons)).hexdigest(),
            'uv':{a.name:buffer(a.data, 'uv', 2) for a in mesh.uv_layers},
            'colors':{a.name:buffer(a.data, 'color', 4) for a in mesh.color_attributes},
            'attributes':sorted((a.name,a.domain,a.data_type) for a in mesh.attributes),
            'uv_state':[(a.name,a.active_render,a.active_clone) for a in mesh.uv_layers],
            'uv_active_index':mesh.uv_layers.active_index,
            'color_active_index':mesh.color_attributes.active_color_index,
            'color_render_index':mesh.color_attributes.render_color_index,
            'materials':[m.name for m in mesh.materials],
            'material_slots':[(s.link,s.material.name if s.material else None) for s in body.material_slots],
            'modifiers':[m.type for m in body.modifiers],
            'matrix':[list(row) for row in body.matrix_world]}


def used_materials(scene):
    """Only live scene graphs survive Blender's normal orphan-ID cleanup."""
    materials = {s.material.name:s.material for obj in scene.objects
                 for s in obj.material_slots if s.material is not None}
    return [materials[name] for name in sorted(materials)]


def slot_state(objects):
    return {o.name:[(s.link,s.material.name if s.material else None) for s in o.material_slots] for o in objects}


def surface_negative_checks(body):
    """Actual copied-mesh negatives isolate smoothing and face assignment."""
    import bpy
    original = body.data
    copied = original.copy()
    result = {}
    try:
        body.data = copied
        original_smooth = copied.polygons[0].use_smooth
        expected = mesh_fingerprint(body)
        copied.polygons[0].use_smooth = not original_smooth
        assert mesh_fingerprint(body) != expected, 'Changed polygon smoothing was accepted.'
        result['polygon_smoothing_rejected'] = True
        copied.polygons[0].use_smooth = original_smooth
        copied.materials.append(copied.materials[0])
        expected = mesh_fingerprint(body)
        copied.polygons[0].material_index = 1
        assert mesh_fingerprint(body) != expected, 'Changed polygon material assignment was accepted.'
        result['polygon_material_assignment_rejected'] = True
    finally:
        body.data = original
        bpy.data.meshes.remove(copied)
    return result


def refine(args):
    import bpy
    from mathutils import Vector
    from anatomical_detail import apply_detail
    from check_anatomy_variant import negative_checks, geometry_metrics, accept_geometry, local_surface_intersections
    from check_character_variant import BODY, WEAR, retained_snapshot, materials_snapshot, require
    from prepare_human_base import read_obj
    require(file_hash(args.base) == BASE_SHA, 'Canonical body asset differs.')
    require(not any((args.output_dir/name).exists() for name in
                    ('unclothed.blend', 'front.png', 'back.png', 'profile.png', 'oblique.png', 'verification.json')),
            'Refinement requires fresh output artifacts.')
    source_hash = file_hash(args.input)
    bpy.ops.wm.open_mainfile(filepath=str(args.input), load_ui=False)
    body = bpy.data.objects[BODY]
    require(body.get('character_age', 0) >= 18, 'Expected explicitly adult anatomy.')
    require(len(body.material_slots) == 1 and body.material_slots[0].link == 'DATA',
            'Anatomy refinement requires the original single data-linked skin material.')
    base = read_obj(args.base)
    canonical = {tuple(f) for f, group in zip(base['faces'],base['face_groups']) if group == 'body'}
    require(len(body.data.vertices) == 19158 and len(body.data.polygons) == 13378 and
            {tuple(p.vertices) for p in body.data.polygons} == canonical,
            'Input must be the complete canonical unclothed body.')
    require(not any(WEAR.search(o.name) for o in bpy.context.scene.objects), 'Input still contains clothing.')
    retained = [o for o in bpy.context.scene.objects if o != body]
    before_retained = retained_snapshot(retained)
    before_slots = slot_state(retained)
    original_materials = used_materials(bpy.context.scene)
    before_materials = materials_snapshot(original_materials)
    report, before_points, faces = apply_detail(body)
    after_points = [tuple(v.co) for v in body.data.vertices]
    report['negative_controls'] = negative_checks(before_points, after_points, faces)
    report['actual_triangle_intersections'] = local_surface_intersections(before_points, after_points, faces)
    report['surface_negative_controls'] = surface_negative_checks(body)
    require(retained_snapshot(retained) == before_retained, 'Retained face/hair/studio objects changed.')
    require(slot_state(retained) == before_slots, 'Retained object material links changed.')
    require(materials_snapshot(original_materials) == before_materials, 'An original material graph changed.')
    require(all(x > .5 for x in report['pigment_maxima']), 'Localized anatomical pigmentation is absent.')
    expected_body = mesh_fingerprint(body)
    expected_materials = materials_snapshot(used_materials(bpy.context.scene))
    material_names = [m.name for m in used_materials(bpy.context.scene)]
    report['construction_body_fingerprint'] = expected_body
    (args.output_dir/'construction-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    scene = bpy.context.scene
    scene['Variant'] = 'Unclothed adult20; fuller chest and continuous external anatomical detail'
    scene['Editing'] = 'Static editable detailed skin mesh; no rig. Dressed and original unclothed inputs retained.'
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    require(any(d.type == 'OPTIX' for d in prefs.devices), 'OptiX GPU required for inspection.')
    for device in prefs.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'; scene.cycles.samples = args.samples
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    cameras = {}
    for name in ('front', 'back', 'profile', 'oblique'):
        camera = bpy.data.objects.get('Variant inspection / '+name)
        require(camera is not None and camera.type == 'CAMERA', 'Missing fixed variant camera '+name)
        cameras[name] = camera
    for name, position, target, scale in [
            ('torso_detail', (1.2, -4.5, 1.26), (0, -.05, 1.20), .53),
            ('pelvis_detail', (.25, -4.5, .81), (0, -.04, .815), .27)]:
        data = bpy.data.cameras.new('Anatomy inspection / '+name)
        camera = bpy.data.objects.new(data.name, data)
        scene.collection.objects.link(camera)
        camera.location = position
        camera.rotation_euler = (Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
        data.type = 'ORTHO'; data.ortho_scale = scale
        cameras[name] = camera
    for name, camera in cameras.items():
        scene.camera = camera
        if name.endswith('_detail'):
            scene.render.resolution_x = scene.render.resolution_y = min(args.size, 1200)
        else:
            scene.render.resolution_x, scene.render.resolution_y = int(args.size*.8), args.size
        scene.render.filepath = str(args.output_dir/(name+'.png'))
        print('Rendering anatomy '+name, flush=True)
        bpy.ops.render.render(write_still=True)
    scene.camera = cameras['front']
    scene.render.resolution_x, scene.render.resolution_y = int(args.size*.8), args.size
    scene.render.filepath = str(args.output_dir/'front.png')
    target = args.output_dir/'unclothed.blend'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    bpy.ops.wm.open_mainfile(filepath=str(target), load_ui=False)
    body = bpy.data.objects[BODY]
    require(mesh_fingerprint(body) == expected_body, 'Reopened detailed body geometry, UVs or masks differ.')
    require(retained_snapshot([bpy.data.objects[name] for name in before_retained]) == before_retained,
            'Saved face/hair/studio objects differ.')
    require(slot_state([bpy.data.objects[name] for name in before_slots]) == before_slots,
            'Saved retained object material links differ.')
    require(materials_snapshot([bpy.data.materials[name] for name in material_names]) == expected_materials,
            'Saved material graph differs.')
    accept_geometry(geometry_metrics(before_points, [tuple(v.co) for v in body.data.vertices], faces))
    require(file_hash(args.input) == source_hash, 'Original unclothed input changed.')
    report.update(status='pass', input=str(args.input), input_sha256=source_hash,
                  retained_face_hair_studio_exact=True, original_materials_exact=True,
                  saved_reopened_verified=True, body_fingerprint=expected_body,
                  source_sha256={str(p.relative_to(ROOT)):file_hash(p) for p in
                                 (ROOT/'scenes/anatomical_detail.py', Path(__file__), ROOT/'tools/check_anatomy_variant.py')},
                  scope='Continuous local chest/nipple/external vulvar surface and pigmentation. Static editable mesh; not internal anatomy, a rig, or full photographic likeness.')
    (args.output_dir/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    from build_sailor_character import positive_int
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--base', type=Path, default=ROOT/'.tools/human_reference_assets/base.obj')
    parser.add_argument('--blender', default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--samples', type=positive_int, default=128)
    parser.add_argument('--size', type=positive_int, default=1600)
    parser.add_argument('--timeout', type=positive_int, default=900)
    parser.add_argument('--inside-blender', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    args.input, args.output_dir, args.base = (p.expanduser().resolve() for p in (args.input,args.output_dir,args.base))
    if args.inside_blender:
        refine(args)
    else:
        run(args, script=__file__, artifact_names=('unclothed.blend','front.png','back.png','profile.png',
                                                 'oblique.png','torso_detail.png','pelvis_detail.png'))

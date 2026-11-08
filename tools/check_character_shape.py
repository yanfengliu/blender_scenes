"""Check the production upper-frame/eyelid response in unsaved anatomy.

Run in owned background Blender with -- --output <receipt.json>. The actual
main-scene anatomy AST is compared with controls omitting the frame map and
restoring the previous eye targets. This measures geometry, not attractiveness,
evaluated eyelid/globe fit, clothing clearance or final rendered silhouette.
"""
import argparse
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
from check_expression_fit import production_blocks
from upper_frame import upper_frame_point
from verify_reference_smile import bind_reference_smile, INPUT_PROPERTY
from check_realistic_character import SMILE_INPUT_SHA256


def anatomy(blocks, source, *, frame=True, eyes=True, smile=True):
    scope = {'__file__': str(source), 'ROOT': ROOT, 'print': lambda *a, **k: None}
    exec(blocks['imports'], scope)
    if not frame:
        scope['finalize_upper_frame'] = lambda objects: {}
    if not smile:
        scope['apply_reference_smile'] = lambda native: {'control': 'independent neutral construction'}
    load = scope['load_body']
    if not eyes:
        scope['load_body'] = lambda targets: load(tuple(
            (name, .035 if name in ('l-eye-height2-incr.target', 'r-eye-height2-incr.target') else weight)
            for name, weight in targets))
    exec(blocks['anatomy'], scope)
    data = bpy.data.meshes.new('Shape regression actual body')
    data.from_pydata(scope['posed'], [], scope['visible_faces'])
    body = bpy.data.objects.new(data.name, data)
    bpy.context.scene.collection.objects.link(body)
    clothes = bpy.data.collections.new('Shape regression clothes')
    scope.update(body=body, cols={'04 Sailor clothing': clothes})
    try:
        exec(blocks['finish'], scope)
        scope['posed'] = [v.co.copy() for v in data.vertices]
    finally:
        bpy.data.objects.remove(body, do_unlink=True)
        bpy.data.meshes.remove(data)
        bpy.data.collections.remove(clothes)
    return scope


def metrics(candidate, baseline):
    old, new = baseline['posed'], candidate['posed']
    body = baseline['native']['groups']['body']
    shoulder = [i for i in body if 1.29 <= old[i].z <= 1.365 and abs(old[i].x) > .055]
    assert len(shoulder) > 100, 'Shoulder measurement did not cover the anatomical shoulder rows.'
    width = lambda points: max(points[i].x for i in shoulder)-min(points[i].x for i in shoulder)
    lids = {}
    for side in ('l', 'r'):
        rows = [line.split() for line in (baseline['ASSETS']/f'{side}-eye-height2-incr.target').read_text().splitlines()
                if line and line[0].isdigit()]
        upper = [int(row[0]) for row in rows if float(row[2]) > .005 and int(row[0]) in body]
        lower = [int(row[0]) for row in rows if float(row[2]) < -.005 and int(row[0]) in body]
        assert len(upper) > 3 and len(lower) > 3, 'Named lid target must have both response populations.'
        lids[side] = {'upper_mean_lift_m': sum(new[i].z-old[i].z for i in upper)/len(upper),
                      'lower_mean_drop_m': sum(old[i].z-new[i].z for i in lower)/len(lower),
                      'upper_rows': len(upper), 'lower_rows': len(lower)}
    return {'shoulder_source_width_before_m': width(old), 'shoulder_source_width_after_m': width(new),
            'shoulder_width_ratio': width(new)/width(old), 'shoulder_rows': len(shoulder), 'lids': lids}


def accept(result):
    assert .84 <= result['shoulder_width_ratio'] <= .94, 'Upper-frame width has not been reduced by a bounded visible amount.'
    for lid in result['lids'].values():
        assert .00010 <= lid['upper_mean_lift_m'] <= .0010, 'Upper lids lack the bounded opening response.'
        assert .00010 <= lid['lower_mean_drop_m'] <= .0010, 'Lower lids lack the bounded opening response.'


def check_smile_input(candidate, neutral):
    """Independently reconstruct neutral geometry before accepting a new pin."""
    data = bpy.data.meshes.new('Shape regression smile binding')
    data.from_pydata(candidate['posed'], [], candidate['visible_faces'])
    body = bpy.data.objects.new(data.name, data)
    bpy.context.scene.collection.objects.link(body)
    try:
        transform = lambda p: candidate['pose'](candidate['to_blender']([p], candidate['native']['ground_y'], candidate['SCALE'])[0])
        digest = bind_reference_smile(body, candidate['smile_diagnostics'], transform)
        assert digest == SMILE_INPUT_SHA256, 'Refined-face smile inputs differ from the independently reviewed pin.'
        rows = json.loads(body[INPUT_PROPERTY])['coordinates']
        assert all(row['neutral'] == list(neutral['posed'][row['row']]) for row in rows), 'Bound neutral rows disagree with a separate production neutral construction.'
        assert all(row['proposed'] == list(candidate['posed'][row['row']]) for row in rows), 'Bound proposed rows disagree with the final anatomy.'
        assert candidate['visible_faces'] == neutral['visible_faces']
        return {'input_sha256': digest, 'independent_neutral_rows_exact': len(rows)}
    finally:
        bpy.data.objects.remove(body, do_unlink=True)
        bpy.data.meshes.remove(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    assert bpy.app.background, 'Use a dedicated background process.'
    source = ROOT/'scenes/sailor_character_realistic.py'
    blocks = production_blocks(source)
    baseline = anatomy(blocks, source, frame=False, eyes=False)
    candidate = anatomy(blocks, source)
    no_frame = anatomy(blocks, source, frame=False)
    no_eyes = anatomy(blocks, source, eyes=False)
    neutral = anatomy(blocks, source, smile=False)
    result = metrics(candidate, baseline)
    accept(result)
    controls = {}
    for name, control in [('previous_frame', no_frame), ('previous_eyes', no_eyes)]:
        try:
            accept(metrics(control, baseline))
        except AssertionError as error:
            controls[name] = str(error)
        else:
            raise AssertionError(f'{name} negative control was accepted.')
    mouth = baseline['smile_diagnostics']['changed_rows']
    assert all(candidate['posed'][i] == baseline['posed'][i] for i in mouth), 'This revision must preserve the existing smile contract.'
    assert candidate['visible_faces'] == baseline['visible_faces'], 'Frame shaping changed the retained skin face population.'
    protected = [i for i, p in enumerate(no_frame['posed']) if p.z <= 1.10 or p.z >= 1.43]
    assert all(candidate['posed'][i] == no_frame['posed'][i] for i in protected), 'Upper-frame mapping moved the waist, lower body or head.'
    assert all(a.y == b.y for a, b in zip(candidate['posed'], no_frame['posed'])), 'Frame mapping changed forward depth.'
    for value in (float('nan'), float('inf')):
        try:
            upper_frame_point((value, 0, 1.3))
        except ValueError:
            continue
        raise AssertionError('Nonfinite frame input accepted.')
    receipt = {'status': 'pass', 'bound': __doc__, 'metrics': result, 'controls_rejected': controls,
               'smile_rows_exact': len(mouth), 'protected_rows_exact': len(protected),
               'topology_preserved': True, 'frame_forward_depth_exact': True,
               'smile_input': check_smile_input(candidate, neutral)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()

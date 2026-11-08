"""Exercise production expression/garment isolation in four unsaved scenes.

Blender --background --python-exit-code 1 --python tools/check_expression_fit.py
  -- --output outputs/expression-fit.json

The maintained main scene's anatomy, material and clothing AST blocks run
unchanged. Neutral, actual smile and a <=0.7 mm remote forehead perturbation
must produce identical complete garment fingerprints. A <=2 mm front-chest
body/helper change before the garment reference snapshot must change fitting.
This checks dependency isolation, not saved-scene clearance or visual quality.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import traceback

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
from check_garment_isolation import GARMENTS, digest, differences, garment_snapshot, require


def production_blocks(source):
    nodes = ast.parse(source.read_text(encoding='utf-8'), filename=str(source)).body
    def assignment(node, name):
        return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
    def index(predicate, label):
        found = [i for i, node in enumerate(nodes) if predicate(node)]
        require(len(found) == 1, f'Production AST boundary {label!r} must occur exactly once; found {len(found)}.')
        return found[0]
    start = index(lambda n: assignment(n, 'native'), 'native assignment')
    stop = index(lambda n: assignment(n, 'body'), 'body assignment')
    cloth = index(lambda n: isinstance(n, ast.ImportFrom) and n.module == 'fitted_blouse'
                  and any(a.name == 'build_blouse' for a in n.names), 'build_blouse import')
    collar = index(lambda n: isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                   and isinstance(n.value.func, ast.Name) and n.value.func.id == 'build_collar', 'build_collar call')
    first_material = index(lambda n: assignment(n, 'ivory'), 'ivory material')
    last_material = index(lambda n: assignment(n, 'cols'), 'collection initialization')
    require(first_material < last_material < start < stop < cloth < collar, 'Production AST blocks changed order.')
    helpers = [n for n in nodes if isinstance(n, ast.FunctionDef) and n.name in ('srgb', 'material')]
    require(len(helpers) == 2, 'Production srgb/material helper definitions are missing or duplicated.')
    blocks = {'imports': [n for n in nodes[:start] if isinstance(n, (ast.Import, ast.ImportFrom))],
              'materials': helpers+nodes[first_material:last_material],
              'anatomy': nodes[start:stop], 'clothing': nodes[cloth:collar+1]}
    return {name: compile(ast.Module(body=items, type_ignores=[]), str(source), 'exec')
            for name, items in blocks.items()}


def perturb(native, scope, region):
    """Move actual native rows before posing; never change height or joint helpers."""
    joints = {i for name, ids in native['groups'].items() if name.startswith('joint-') for i in ids}
    body = set(native['groups']['body'])
    before = [tuple(v) for v in native['vertices']]
    height = max(before[i][1] for i in body)-native['ground_y']
    scale = 1.65/height
    points = scope['to_blender'](before, native['ground_y'], scale)
    allowed = body if region == 'forehead' else body | set(native['groups']['helper-tights'])
    changed = []
    for i in sorted(allowed-joints):
        x, y, z = points[i]
        center, radius, width, cap = (1.585, .025, .060, .0007) if region == 'forehead' else (1.215, .070, .145, .002)
        if abs(x) >= width or abs(z-center) >= radius or y >= -.04:
            continue
        movement = cap*(1-(x/width)**2)**2*(1-((z-center)/radius)**2)**2
        native['vertices'][i][2] += movement/scale
        changed.append(i)
    require(len(changed) > 5 and len(body.intersection(changed)) > 5, f'{region} control changed too few anatomical vertices.')
    require(all(tuple(native['vertices'][i]) == before[i] for i in joints), 'Control moved a pose-driving joint.')
    require(max(native['vertices'][i][1] for i in body)-native['ground_y'] == height, 'Control changed stature.')
    return {'region': region, 'changed_rows': len(changed), 'body_rows': len(body.intersection(changed)),
            'maximum_displacement_m': max(abs(native['vertices'][i][2]-before[i][2])*scale for i in changed)}


def run_case(name, source, blocks):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scope = {'__file__': str(source), 'ROOT': ROOT, 'print': lambda *a, **k: None}
    exec(blocks['imports'], scope)
    original_smile, original_perioral = scope['apply_reference_smile'], scope['apply_perioral_shape']
    controls = []
    def smile(native):
        result = {'control': 'neutral'} if name == 'neutral' else original_smile(native)
        if name == 'remote_face':
            controls.append(perturb(native, scope, 'forehead'))
        return result
    def perioral(native):
        result = original_perioral(native)
        if name == 'torso':
            controls.append(perturb(native, scope, 'chest'))
        return result
    scope.update(apply_reference_smile=smile, apply_perioral_shape=perioral)
    exec(blocks['materials'], scope)
    collection = bpy.data.collections.new('04 Sailor clothing')
    bpy.context.scene.collection.children.link(collection)
    scope['cols'] = {'04 Sailor clothing': collection}
    exec(blocks['anatomy'], scope)
    exec(blocks['clothing'], scope)
    bpy.context.view_layer.update()
    native = [tuple(v) for v in scope['native']['vertices']]
    posed = [tuple(v) for v in scope['posed']]
    require(len(native) == len(posed) == 19158, 'Actual body source population changed.')
    return {'garments': {n: garment_snapshot(bpy.data.objects[n]) for n in GARMENTS},
            'native': native, 'posed': posed, 'controls': controls, 'body_rows': scope['native']['groups']['body']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    require(bpy.app.background, 'Run this disposable-scene regression in a dedicated headless Blender process.')
    require(args.output.suffix.lower() == '.json', 'Output must be a JSON receipt.')
    source = ROOT/'scenes/sailor_character_realistic.py'
    receipt = {'status': 'fail', 'bound': __doc__, 'source': str(source),
               'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    try:
        blocks = production_blocks(source)
        cases = {name: run_case(name, source, blocks) for name in ('neutral', 'smile', 'remote_face', 'torso')}
        receipt['cases'] = {name: {'garments': value['garments'], 'controls': value['controls'],
                                  'native_sha256': digest(value['native']), 'posed_sha256': digest(value['posed'])}
                            for name, value in cases.items()}
        receipt['comparisons'] = {}
        for before, after in (('neutral', 'smile'), ('smile', 'remote_face'), ('smile', 'torso')):
            a, b = cases[before], cases[after]
            changes = {kind: [i for i in a['body_rows'] if a[kind][i] != b[kind][i]] for kind in ('native', 'posed')}
            drift = differences(a['garments'], b['garments'])
            receipt['comparisons'][before+' -> '+after] = {'changed_anatomical_rows': {k: len(v) for k, v in changes.items()},
                                                          'garment_differences': drift}
            require(all(changes.values()), f'{after}: actual native/posed anatomy did not change; vacuous control.')
            if after != 'torso':
                require(all(a['posed'][i][2] > 1.45 and b['posed'][i][2] > 1.45 for i in changes['posed']),
                        'Expression control changed anatomy outside the remote head region.')
                require(not drift, f'{after}: remote expression changed complete garment state: {drift}')
            else:
                require('vertices' in drift.get(GARMENTS[0], []), 'Relevant torso control failed to change actual blouse coordinates.')
        receipt['status'] = 'pass'
    except Exception as error:
        receipt.update(error=str(error), traceback=traceback.format_exc())
    finally:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        receipt['temporary_objects_cleaned'] = not bpy.data.objects
        require(receipt['temporary_objects_cleaned'], 'Temporary regression objects remain.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(receipt, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    require(receipt['status'] == 'pass', receipt.get('error', 'Expression-fit regression failed.'))
    print('EXPRESSION_FIT: pass; production AST, actual expression changes and responsive torso control.', flush=True)


if __name__ == '__main__':
    main()

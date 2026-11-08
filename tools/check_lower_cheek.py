"""Pure production-AST cheek regression; source geometry is not aesthetic proof."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
import check_lip_contour as lip
from prepare_human_base import to_blender
from perioral_shape import apply_perioral_shape
from reference_smile import apply_reference_smile, trace_oral_strip


def widths(native, scale):
    points = to_blender(native['vertices'], native['ground_y'], scale)
    result = {}
    for z in (1.44, 1.48, 1.50):
        hits = []
        for face in native['faces']:
            for i,j in zip(face, face[1:]+face[:1]):
                a,b = points[i],points[j]
                if (a[2] <= z < b[2]) or (b[2] <= z < a[2]):
                    t = (z-a[2])/(b[2]-a[2])
                    if a[1]+t*(b[1]-a[1]) < -.105:
                        hits.append(a[0]+t*(b[0]-a[0]))
        lip.require(len(hits) > 10, 'Forward-face section has too few source-edge samples.')
        result[z] = max(hits)-min(hits)
    return result


def accept_width(before, after):
    lip.require(abs(after[1.44]-before[1.44]) < 1e-10, 'Central chin section changed.')
    for z in (1.48,1.50):
        lip.require(.003 <= before[z]-after[z] <= .0052, 'Lower cheek lacks its bounded 3–5 mm width reduction.')


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    actual,_ = lip.production_input()
    original = lip.apply_lower_cheek_inset
    try:
        lip.apply_lower_cheek_inset = lambda native: {'control': 'no-op'}
        control,_ = lip.production_input()
    finally:
        lip.apply_lower_cheek_inset = original
    old,new = control['native'],actual['native']
    scale = 1.65/(max(old['vertices'][i][1] for i in old['groups']['body'])-old['ground_y'])
    before,after = widths(old,scale),widths(new,scale)
    accept_width(before,after)
    try:
        accept_width(before,before)
    except AssertionError:
        rejected = True
    else:
        rejected = False
    lip.require(rejected, 'No-op unexpectedly satisfies cheek-width acceptance.')
    a,b = old['vertices'],new['vertices'];changed = {i for i in range(len(a)) if a[i] != b[i]}
    ratios,dots,edges = [],[],set()
    for face in old['faces']:
        if not changed.intersection(face):continue
        for j in range(1,len(face)-1):
            tri = (face[0],face[j],face[j+1]);u,v = lip.normal(a,tri),lip.normal(b,tri)
            lu,lv = math.sqrt(sum(c*c for c in u)),math.sqrt(sum(c*c for c in v))
            lip.require(lu > 1e-12 and lv > 1e-12, 'Lower cheek contains a collapsed source fan.')
            ratios.append(lv/lu);dots.append(sum(x*y for x,y in zip(u,v))/(lu*lv))
            edges.update(tuple(sorted((i,k))) for i,k in zip(tri,tri[1:]+tri[:1]))
    gradient = max(math.dist([b[i][k]-a[i][k] for k in range(3)], [b[j][k]-a[j][k] for k in range(3)])/math.dist(a[i],a[j]) for i,j in edges)
    lip.require(min(ratios) >= .25 and min(dots) > 0 and gradient < .5, 'Lower-cheek source fan or continuity bound failed.')
    sections,_ = trace_oral_strip(old['faces']);oral = {i for pair in sections for i in pair}
    for native in (old,new):
        apply_perioral_shape(native);apply_reference_smile(native)
    lip.require(all(old['vertices'][i] == new['vertices'][i] for i in oral), 'Full lip chain changes protected oral XYZ.')
    lip.require('bpy' not in sys.modules, 'Pure lower-cheek regression imported Blender.')
    files = ('scenes/sailor_character_realistic.py','scenes/lower_cheek.py','scenes/natural_face.py',
             'scenes/gentle_expression.py','scenes/perioral_shape.py','scenes/reference_smile.py',
             'tools/prepare_human_base.py','tools/check_lower_cheek.py','tools/check_lip_contour.py')
    receipt = dict(status='pass',bound=__doc__,before_widths_m=before,after_widths_m=after,no_op_rejected=rejected,
                   changed_rows=len(changed),minimum_area_ratio=min(ratios),minimum_normal_dot=min(dots),
                   maximum_edge_gradient=gradient,whole_chain_oral_xyz_exact=len(oral),
                   source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__ == '__main__':main()

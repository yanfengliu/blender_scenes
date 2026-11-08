"""Check production lip contours on real native anatomy, without Blender.

Run .venv/Scripts/python.exe tools/check_lip_contour.py [--output receipt.json].
Source checks cover bounded geometry and reject the former thick-lip mechanism;
they do not establish attractiveness, evaluated closure or rendered appearance.
"""
import argparse
import ast
import copy
import hashlib
import heapq
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'scenes')]
from prepare_human_base import ASSETS, DEFAULT_TARGETS, load_body
from natural_face import shape_expression
from gentle_expression import apply_gentle_expression, MOUTH_CONTACT, EYE_CORNERS, EYE_PROXY_SCALE_ANCHORS
from perioral_shape import apply_perioral_shape
from lower_cheek import apply_lower_cheek_inset
from reference_smile import trace_oral_strip


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def production_input():
    source = ROOT/'scenes/sailor_character_realistic.py'
    nodes = ast.parse(source.read_text(encoding='utf-8'), filename=str(source)).body
    def boundary(name):
        found = [i for i,n in enumerate(nodes) if isinstance(n,ast.Assign)
                 and any(isinstance(t,ast.Name) and t.id == name for t in n.targets)]
        require(len(found) == 1, f'Expected one production {name} boundary.')
        return found[0]
    start, stop = boundary('native'), boundary('perioral_diagnostics')
    require(start < stop, 'Production native/perioral stages changed order.')
    scope = dict(math=math, load_body=load_body, DEFAULT_TARGETS=DEFAULT_TARGETS,
                 shape_expression=shape_expression, apply_gentle_expression=apply_gentle_expression,
                 apply_lower_cheek_inset=apply_lower_cheek_inset)
    exec(compile(ast.Module(body=nodes[start:stop], type_ignores=[]), str(source), 'exec'), scope)
    call = nodes[stop].value
    require(isinstance(call,ast.Call) and isinstance(call.func,ast.Name)
            and call.func.id == 'apply_perioral_shape', 'Production perioral call changed.')
    return scope, compile(ast.Module(body=[nodes[stop]],type_ignores=[]),str(source),'exec')


def former_contour_control():
    """Remove only the new upper vertical term and lower helper from actual code."""
    source = ROOT/'scenes/perioral_shape.py'
    tree = ast.parse(source.read_text(encoding='utf-8'), filename=str(source))
    counts = [0,0]
    class RemoveContour(ast.NodeTransformer):
        def visit_AugAssign(self,node):
            if ast.unparse(node.target) == 'after[i][1]' and ast.unparse(node.value) == '0.0012 * weight / scale':
                counts[0] += 1
                return None
            return self.generic_visit(node)
        def visit_Assign(self,node):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id == '_thin_lower_lip':
                counts[1] += 1
                node.value = ast.copy_location(ast.Dict(keys=[],values=[]),node.value)
            return self.generic_visit(node)
    tree=ast.fix_missing_locations(RemoveContour().visit(tree))
    require(counts == [1,1], f'Control must remove exactly the two contour mechanisms; found {counts}.')
    scope={'__name__':'lip_contour_control'}
    exec(compile(tree,str(source)+' [negative control]','exec'),scope)
    return scope['apply_perioral_shape']


def contour(vertices,scale):
    return {'upper_height_m':(vertices[466][1]-vertices[520][1])*scale,
            'lower_height_m':(vertices[523][1]-vertices[495][1])*scale,
            'lower_projection_m':(vertices[495][2]-vertices[523][2])*scale}


def accept_contour(metrics):
    require(.0058 <= metrics['upper_height_m'] <= .0065, 'Upper lip lacks the bounded height reduction.')
    require(.0063 <= metrics['lower_height_m'] <= .0070, 'Lower lip lacks the bounded height reduction.')
    require(.0019 <= metrics['lower_projection_m'] <= .0025, 'Lower lip lacks the bounded retraction.')


def normal(points,tri):
    a,b,c=(points[i] for i in tri)
    u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
    return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])


def verify_geometry(before,after,control,scale):
    old,new=before['vertices'],after['vertices']
    body=set(before['groups']['body'])
    sections,_=trace_oral_strip(before['faces']);oral={i for pair in sections for i in pair}
    require(len(oral)==76,'Complete oral strip population changed.')
    require(all(new[i][1:]==old[i][1:] for i in oral),'Full oral strip Y/Z changed.')
    require(all(new[i][0]==control['vertices'][i][0] for i in range(len(old))), 'Contour changes altered the retained width map.')
    require(all(new[i][0]==old[i][0]*1.02 for i in MOUTH_CONTACT),'Original 60-row contact width map changed.')
    protected=set(range(len(old)))-body
    for name,rows in before['groups'].items():
        if name!='body':protected.update(rows)
    protected.update(EYE_PROXY_SCALE_ANCHORS)
    for pair in EYE_CORNERS.values():protected.update(pair)
    require(all(new[i]==old[i] for i in protected),'Protected helper or ocular anchor moved.')
    adjacency={i:set() for i in body}
    for face in before['faces']:
        for i in face:adjacency[i].update(face)
    distance={i:0. for i in MOUTH_CONTACT};queue=[(0.,i) for i in MOUTH_CONTACT];heapq.heapify(queue)
    while queue:
        length,i=heapq.heappop(queue)
        if length!=distance[i]:continue
        for j in adjacency[i]:
            value=length+math.dist(old[i],old[j])*scale
            if value<.012 and value<distance.get(j,math.inf):
                distance[j]=value;heapq.heappush(queue,(value,j))
    target={int(p[0]) for line in (ASSETS/'mouth-upperlip-volume-incr.target').read_text().splitlines()
            if (p:=line.split()) and p[0].isdigit()}
    lower={i for i in body if abs(old[i][0]*scale)<.022 and .563<old[i][1]*scale<.582 and .140<old[i][2]*scale<.150}
    changed={i for i in range(len(old)) if new[i]!=old[i]}
    require(changed and changed <= target|set(distance)|lower,'Change escaped anatomical lip/adjacency support.')
    maximum=max(math.dist(old[i],new[i])*scale for i in changed)
    require(maximum<.003,'Combined perioral change exceeded 3 mm.')
    ratios,dots=[],[]
    for face in before['faces']:
        if not changed.intersection(face):continue
        for j in range(1,len(face)-1):
            tri=(face[0],face[j],face[j+1]);a,b=normal(old,tri),normal(new,tri)
            la,lb=math.sqrt(sum(c*c for c in a)),math.sqrt(sum(c*c for c in b))
            require(la>1e-12 and lb>1e-12,f'Collapsed source fan {tri}.')
            ratios.append(lb/la);dots.append(sum(x*y for x,y in zip(a,b))/(la*lb))
    require(min(ratios)>=.25 and min(dots)>0,'Combined lip shape collapses or reverses a source fan.')
    return dict(changed_rows=len(changed),full_oral_rows_yz_exact=len(oral),protected_rows_exact=len(protected),
                maximum_displacement_m=maximum,affected_triangles=len(ratios),
                minimum_area_ratio=min(ratios),minimum_normal_dot=min(dots))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    scope,stage=production_input();before=copy.deepcopy(scope['native'])
    scale=1.65/(max(before['vertices'][i][1] for i in before['groups']['body'])-before['ground_y'])
    control_scope={**scope,'native':copy.deepcopy(before),'apply_perioral_shape':former_contour_control()}
    exec(stage,control_scope)
    scope['apply_perioral_shape']=apply_perioral_shape;exec(stage,scope)
    actual=contour(scope['native']['vertices'],scale);control=contour(control_scope['native']['vertices'],scale)
    accept_contour(actual)
    try:accept_contour(control)
    except AssertionError:rejected=True
    else:rejected=False
    require(rejected,'Former lip mechanism passed the contour criterion; regression is ineffective.')
    geometry=verify_geometry(before,scope['native'],control_scope['native'],scale)
    require('bpy' not in sys.modules,'Pure regression imported Blender.')
    files=['scenes/sailor_character_realistic.py','scenes/perioral_shape.py','scenes/natural_face.py',
           'scenes/gentle_expression.py','scenes/lower_cheek.py','scenes/reference_smile.py','tools/prepare_human_base.py','tools/check_lip_contour.py']
    receipt=dict(status='pass',bound=__doc__,actual=actual,former_control=control,former_control_rejected=rejected,
                 geometry=geometry,source_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                 source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()

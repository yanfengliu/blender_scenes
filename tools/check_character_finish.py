"""Verify the actual saved finished body, clothing and strand coverage.

Run in owned Blender --background <scene.blend> --python-exit-code 1
--python tools/check_character_finish.py -- --output <receipt.json>.
Rebuild complete canonical body faces from the saved coordinates; test clothing
and nine ornaments, a real body-intrusion negative, and actual hair scanlines.
Finite geometry checks do not certify appearance; native six-view review remains
required. The saved scene must remain byte-identical throughout this check.
"""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'scenes')]
import prepare_human_base as base
base.ASSETS=ROOT/'.tools/human_reference_assets'
from check_realistic_character import validate_scene
from check_garment_isolation import clearance,penetration_control,evaluated,measure,GARMENTS,BASE_SHA,file_hash
from prepare_human_base import load_body
from body_proportions import full_body_support
from natural_hair import _Head
from hair_groom import fringe_coverage,crown_coverage,temple_coverage
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
assert bpy.app.background, 'Use an owned background process.'
blend=Path(bpy.data.filepath).resolve();before=hashlib.sha256(blend.read_bytes()).hexdigest()
assert args.output.suffix.lower()=='.json' and args.output.resolve()!=blend, 'Use a separate JSON receipt path.'
args.output.parent.mkdir(parents=True,exist_ok=True)
assert file_hash(base.ASSETS/'base.obj')==BASE_SHA, 'Canonical body asset digest changed.'
body=bpy.data.objects['Haru / anatomical adult skin'];canonical=load_body(targets=(),assets=base.ASSETS)
result={'blend_sha256':before,'status':'fail','canonical_base_sha256':BASE_SHA,
        'verification_source_sha256':file_hash(Path(__file__))}

ORNAMENTS={
 'Blouse / rounded sewn pocket with slight ease', 'Blouse / turned pocket top edge',
 'Blouse / pocket U perimeter stitching', 'Blouse / pocket folded-edge stitch',
 'Neckerchief / left folded collar entry', 'Neckerchief / right folded collar entry',
 'Neckerchief / left unequal folded tail', 'Neckerchief / right unequal folded tail',
 'Neckerchief / overlapping diagonal ribbon wrap'}

def checked_ornament(obj,tree):
 verts,_,tris=evaluated(obj)
 assert verts and tris, f'Ornament has no evaluated surface: {obj.name}'
 return measure(verts,tris,tree)

try:
 result['canonical']=validate_scene()
 result['clothing']=clearance(body,canonical)
 assert result['clothing']['pass'],'Saved evaluated clothing clearance failed'
 result['penetration_control']=penetration_control(body,canonical)
 actual_points=[v.co.copy() for v in body.data.vertices]
 with full_body_support(canonical,actual_points) as full:
  points,_,triangles=evaluated(full);tree=BVHTree.FromPolygons(points,triangles,all_triangles=True)
  objects={obj.name:obj for obj in bpy.data.collections['04 Sailor clothing'].all_objects
           if obj.name not in GARMENTS and obj.name.startswith(('Neckerchief /','Blouse /'))}
  assert set(objects)==ORNAMENTS, ('Unexpected ornament population',sorted(objects))
  data=bpy.data.meshes.new('Temporary empty ornament negative')
  empty=bpy.data.objects.new(data.name,data);bpy.context.scene.collection.objects.link(empty)
  try:
   try: checked_ornament(empty,tree)
   except AssertionError as error:
    assert 'no evaluated surface' in str(error), 'Empty control failed for an unrelated reason'
    result['empty_ornament_control_rejected']=True
   else: raise AssertionError('An empty evaluated ornament passed')
  finally:
   bpy.data.objects.remove(empty,do_unlink=True);bpy.data.meshes.remove(data)
  ornaments={name:checked_ornament(obj,tree) for name,obj in objects.items()}
  result['ornaments']=ornaments
  assert all(row['pass'] for row in ornaments.values()),'Saved evaluated ornament clearance failed'
 native={**canonical,'vertices':[[p.x,p.z,-p.y] for p in actual_points],'ground_y':0}
 head=_Head(bpy,native,1.,body)
 hair=list(bpy.data.collections['03 Strand hair'].all_objects)
 result['fringe']=fringe_coverage(hair,head.eye,head.cy)
 result['crown']=crown_coverage(hair,head)
 result['temples']=temple_coverage(hair,head)
 assert result['fringe']['pass'] and result['crown']['pass'] and result['temples']['pass'],'Actual saved hair guard failed'
 result['status']='pass'
except Exception as error:
 result['error']=str(error)
 raise
finally:
 assert hashlib.sha256(blend.read_bytes()).hexdigest()==before
 result['saved_scene_unchanged']=True
 args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 print(json.dumps({'status':result['status'],'report':str(args.output)}),flush=True)

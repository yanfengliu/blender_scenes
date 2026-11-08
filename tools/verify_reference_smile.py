"""Live evaluated exterior-aperture gate for the retained 1.5 mm smile.

Harness: the verified CC limit stencil and actual triangle narrow phase from
candidate2; complete CC2 oral descendants and surface populations from V3;
strict translation ownership and terminal rounding controls reviewed separately.
Bound: 76 anchors, all rail knots plus257 samples per half/depth, changed-source
descendants + neighbors + complete corner patches + prior oral region. Scalar
and vertical exterior increases <50um; central scalar increases <50um. Shared
triangle vertices, ten inner classification ties, ambiguous rail alternatives,
and separate hair/cloth occlusion remain explicit omissions. No realism claim.

Saved body property reference_smile_input contains coordinate/topology INPUTS,
never a pass flag. The caller pins its digest and independently checks neutral
truth against the accepted pre-smile body. Every verification evaluates live
geometry and controls; a saved receipt never substitutes for this call.
"""
from collections import Counter, defaultdict, deque
import copy
import hashlib
import heapq
import json
import math
import struct
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from mathutils.geometry import intersect_ray_tri

INPUT_PROPERTY='reference_smile_input'
ATTRIBUTE='reference_smile_temporary_source_face'
ERROR_M=1e-6
APERTURE_INCREASE_M=.00005
ORDINARY_INTERVAL_M=1e-10
EXPECTED_RECORDS=1318


def _json(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))


def _digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _topology(faces):
    return _digest(_json(faces))


def bind_reference_smile(body,report,transform_native_point):
    """Bind factual neutral/proposed inputs after body, pose and CC2 creation.

    The proposed-coordinate comparison explicitly rejects any later body field
    affecting these facial rows. Caller must independently compare neutral
    coordinates with the accepted pre-smile body before candidate acceptance.
    """
    require(INPUT_PROPERTY not in body,'Reference smile input is already bound; inspect its provenance instead of replacing it.')
    require(report.get('required_evaluated_gate')=='evaluated_exterior_aperture','Reference smile source report lacks its required live gate.')
    rows=report['changed_rows']
    require(rows==sorted(set(rows)) and len(rows)==522,'Reference smile needs the frozen522 changed native rows.')
    before=report['native_before_changed'];after=report['native_after_changed']
    require([r[0] for r in before]==rows==[r[0] for r in after],'Reference smile neutral/proposed row identities differ.')
    require(len(body.data.vertices)==19158 and body.matrix_world==Matrix.Identity(4),'Reference smile requires retained19158-row body and identity object transform.')
    records=[]
    for old,new in zip(before,after):
        i=old[0];neutral=Vector(transform_native_point(old[1:]));proposed=Vector(transform_native_point(new[1:]))
        require(body.data.vertices[i].co==proposed,f'Reference smile final row{i} differs from the exact posed proposal; a body field or later edit changed it.')
        records.append({'row':i,'neutral':list(neutral),'proposed':list(proposed)})
    contract={'schema':1,'gate':'evaluated_exterior_aperture','vertex_count':19158,
        'coordinate_frame':'final posed body local coordinates; identity object matrix',
        'topology_sha256':_topology([list(p.vertices) for p in body.data.polygons]),
        'changed_rows':rows,'coordinates':records,'oral_sections':report['oral_sections'],
        'oral_paths':report['oral_paths'],'corner_sections':report['corner_sections'],
        'historical_source_vector_diagnostic':report['source_vector_diagnostic']}
    encoded=_json(contract)
    body[INPUT_PROPERTY]=encoded
    return _digest(encoded)


class SmileVerificationError(ValueError):
    def __init__(self,message,report):
        super().__init__('Reference smile live evaluated gate failed: '+message)
        self.report=report


def catmull_clark_limit(vertices, faces, contact):
    """Predict all76 source-vertex limit positions for actual use_limit_surface.

    The former finite-two-step predictor failed on446 by27.848um. The observed
    saved modifier enables limit evaluation; its quad limit stencil matched
    actual446 within0.239um. Every row must still pass the unchanged1um bound.
    """
    neighbors={i:set() for i in contact};opposite={i:[] for i in contact}
    for face in faces:
        for k,i in enumerate(face):
            if i not in neighbors:continue
            assert len(face)==4, 'Contact limit stencil requires the inspected all-quad neighborhood.'
            neighbors[i].update((face[k-1],face[(k+1)%4]))
            opposite[i].append(vertices[face[(k+2)%4]])
    result={}
    for i in contact:
        n=len(opposite[i]);assert n==len(neighbors[i]) and n>=3
        result[i]=(vertices[i]*(n*n)+sum((vertices[j] for j in neighbors[i]),Vector())*4+
                   sum(opposite[i],Vector()))/(n*(n+5))
    return result


def normal(points,triangle):
    a,b,c=(points[i] for i in triangle)
    return (b-a).cross(c-a)


def intersections(points,triangles):
    # BVH supplies candidates only. Disjoint-index pairs receive segment/triangle
    # narrow phase; coplanar pairs use2D edges/containment. Shared-vertex pairs
    # are excluded as topological neighbors, not certified collision-free.
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True,epsilon=0)
    hits=set();candidates=0;coplanar=0;eps=1e-9
    def crosses(a,b):
        nonlocal coplanar
        pa=[points[i] for i in a];pb=[points[i] for i in b]
        na=(pa[1]-pa[0]).cross(pa[2]-pa[0]);nb=(pb[1]-pb[0]).cross(pb[2]-pb[0])
        if na.length==0 or nb.length==0:raise AssertionError('Collapsed evaluated triangle cannot be a valid intersection input.')
        na.normalize();nb.normalize()
        if abs(abs(na.dot(nb))-1)<1e-7 and max(abs((p-pa[0]).dot(na)) for p in pb)<eps:
            coplanar+=1;axis=max(range(3),key=lambda k:abs(na[k]));axes=[k for k in range(3) if k!=axis]
            a2=[(p[axes[0]],p[axes[1]]) for p in pa];b2=[(p[axes[0]],p[axes[1]]) for p in pb]
            def orient(x,y,z):return (y[0]-x[0])*(z[1]-x[1])-(y[1]-x[1])*(z[0]-x[0])
            def inside(p,tri):
                signs=[orient(tri[j],tri[(j+1)%3],p) for j in range(3)]
                return min(signs)>=-1e-18 or max(signs)<=1e-18
            if inside(a2[0],b2) or inside(b2[0],a2):return True
            return any(orient(a2[i],a2[(i+1)%3],b2[j])*orient(a2[i],a2[(i+1)%3],b2[(j+1)%3])<0 and
                       orient(b2[j],b2[(j+1)%3],a2[i])*orient(b2[j],b2[(j+1)%3],a2[(i+1)%3])<0
                       for i in range(3) for j in range(3))
        for edges,surface in [(pa,pb),(pb,pa)]:
            for i,a0 in enumerate(edges):
                direction=edges[(i+1)%3]-a0;length=direction.length
                if not length:continue
                hit=intersect_ray_tri(*surface,direction/length,a0,True)
                if hit is not None and -eps<=(hit-a0).dot(direction/length)<=length+eps:return True
        return False
    for a,b in tree.overlap(tree):
        if a>=b or set(triangles[a])&set(triangles[b]):continue
        candidates+=1
        if crosses(triangles[a],triangles[b]):
            hits.add(tuple(sorted((tuple(sorted(triangles[a])),tuple(sorted(triangles[b]))))))
    return hits,{'triangles':len(triangles),'narrow_phase_pairs':candidates,'coplanar_pairs':coplanar,'confirmed_pairs':len(hits)}

def edges_of(faces):
    edges = defaultdict(list)
    for fi, face in enumerate(faces):
        for k, a in enumerate(face):
            edges[tuple(sorted((a, face[(k+1) % len(face)])))].append(fi)
    return dict(edges)


def source_regions(faces, sections, paths):
    edges = edges_of(faces)
    inner_loop = {tuple(sorted((sections[i][1], sections[(i+1) % len(sections)][1]))) for i in range(len(sections))}
    strip = {fi for edge in edges for fi in edges[edge] if set(faces[fi]) <= {v for pair in sections for v in pair}}
    strip = {fi for fi in strip if any(tuple(sorted(pair)) in edges and fi in edges[tuple(sorted(pair))] for pair in sections)}
    adjacency = defaultdict(set)
    for edge, rows in edges.items():
        if edge in inner_loop:
            continue
        for fi in rows:
            adjacency[fi].update(set(rows)-{fi})
    inner_seeds = {fi for edge in inner_loop for fi in edges[edge] if fi not in strip}
    assert inner_seeds and len(strip) == 38
    inside = set(inner_seeds)
    queue = deque(inside)
    while queue:
        for other in adjacency[queue.popleft()]-inside:
            inside.add(other); queue.append(other)
    assert inside.isdisjoint(strip) and 20 < len(inside) < 2000, 'Inner loop did not isolate a bounded mouth cavity.'
    seeds = {'upper': set(), 'lower': set()}
    for path in paths:
        for name in seeds:
            for a, b in zip(path[name], path[name][1:]):
                edge = tuple(sorted((sections[a][1], sections[b][1])))
                seeds[name].update(fi for fi in edges[edge] if fi in inside)
    distances = {}
    for name in seeds:
        distance = {i: 0 for i in seeds[name]}; queue = deque(distance)
        while queue:
            i = queue.popleft()
            for j in adjacency[i] & inside:
                if j not in distance:
                    distance[j] = distance[i]+1; queue.append(j)
        assert set(distance) == inside
        distances[name] = distance
    upper = {i for i in inside if distances['upper'][i] < distances['lower'][i]}
    lower = {i for i in inside if distances['lower'][i] < distances['upper'][i]}
    ties = inside-upper-lower
    return {'strip': strip, 'inside': inside, 'inner_upper': upper,
            'inner_lower': lower, 'inner_ties': ties, 'edges': edges}


def trace_descendant_edges(source_faces, evaluated_faces, owners, anchor_indices, paths, sections):
    original_edges = edges_of(source_faces)
    fine_edges = edges_of(evaluated_faces)
    seams = defaultdict(list)
    for edge, adjacent in fine_edges.items():
        owner_pair = tuple(sorted({owners[i] for i in adjacent}))
        if len(owner_pair) == 2:
            seams[owner_pair].append(edge)
    cache = {}
    for path in paths:
        for name in ('upper', 'lower'):
            for depth in (0, 1):
                rows = [sections[i][depth] for i in path[name]]
                for a, b in zip(rows, rows[1:]):
                    key = tuple(sorted((a, b)))
                    if key in cache:
                        continue
                    pair = tuple(sorted(original_edges[key]))
                    assert len(pair) == 2
                    adjacency = defaultdict(set)
                    for x, y in seams[pair]:
                        adjacency[x].add(y); adjacency[y].add(x)
                    first, last = anchor_indices[a], anchor_indices[b]
                    assert len(adjacency[first]) == len(adjacency[last]) == 1
                    chain = [first]
                    while chain[-1] != last:
                        options = adjacency[chain[-1]]-set(chain)
                        assert len(options) == 1, 'Evaluated source-edge descendant is ambiguous.'
                        chain.append(options.pop())
                        assert len(chain) <= 5
                    assert len(chain) == 5 and len(adjacency) == 5, 'CC2 source edge needs four actual descendants.'
                    cache[key] = chain if a < b else list(reversed(chain))
    result = []
    for path in paths:
        item = {'side': path['side']}
        for name in ('upper', 'lower'):
            for depth in (0, 1):
                rows = [sections[i][depth] for i in path[name]]
                chain = []
                for a, b in zip(rows, rows[1:]):
                    piece = cache[tuple(sorted((a, b)))]
                    if a > b:
                        piece = list(reversed(piece))
                    chain.extend(piece if not chain else piece[1:])
                item[name+str(depth)] = chain
        result.append(item)
    return result, cache


def line_hits(points, chain, x):
    hits = []
    for k, (a, b) in enumerate(zip(chain, chain[1:])):
        pa, pb = points[a], points[b]
        if x < min(pa.x, pb.x)-1e-10 or x > max(pa.x, pb.x)+1e-10:
            continue
        if abs(pb.x-pa.x) < 1e-12:
            if abs(x-pa.x) < 1e-10:
                hits.append({'segment': k, 'rows': [a,b], 'weight': None, 'point': list(pa), 'vertical_segment': True})
            continue
        t = min(1., max(0., (x-pa.x)/(pb.x-pa.x)))
        point = pa.lerp(pb, t)
        if not any((point-Vector(old['point'])).length < 1e-10 for old in hits):
            hits.append({'segment': k, 'rows': [a,b], 'weight': t, 'point': list(point), 'vertical_segment': False})
    return hits


def common_x_gaps(points, paths, x_grids=None):
    records, grids = [], {}
    for path in paths:
        for depth in (0, 1):
            upper, lower = path['upper'+str(depth)], path['lower'+str(depth)]
            low = max(min(points[i].x for i in upper), min(points[i].x for i in lower))
            high = min(max(points[i].x for i in upper), max(points[i].x for i in lower))
            key = str(path['side'])+':'+str(depth)
            xs = (x_grids[key] if x_grids is not None else sorted(set(
                [points[i].x for i in upper+lower if low <= points[i].x <= high]
                +[low+(high-low)*i/256 for i in range(257)])))
            grids[key] = xs
            terminal = points[upper[-1]].x
            for x in xs:
                u, l = line_hits(points, upper, x), line_hits(points, lower, x)
                record = {'side':path['side'], 'depth':depth, 'x_m':x,
                          'terminal_corner':abs(x-terminal)<1e-10,
                          'near_corner':abs(x-terminal)<.002 and abs(x-terminal)>=1e-10,
                          'upper_branches':u, 'lower_branches':l, 'pairs':[]}
                for a in u:
                    for b in l:
                        delta = Vector(a['point'])-Vector(b['point'])
                        record['pairs'].append({'upper_segment':a['segment'], 'lower_segment':b['segment'],
                            'signed_vertical_m':delta.z, 'signed_depth_m':delta.y, 'distance_m':delta.length})
                record['ambiguous'] = len(u)!=1 or len(l)!=1 or any(h['vertical_segment'] for h in u+l)
                records.append(record)
    return records, grids


def compare_gaps(old, new):
    assert len(old) == len(new)
    rows = []
    for a, b in zip(old, new):
        assert (a['side'],a['depth'],a['x_m']) == (b['side'],b['depth'],b['x_m'])
        assert len(a['pairs']) == len(b['pairs']), 'Common-X branch population changed.'
        for p, q in zip(a['pairs'], b['pairs']):
            assert (p['upper_segment'],p['lower_segment']) == (q['upper_segment'],q['lower_segment'])
            rows.append({'side':a['side'],'depth':a['depth'],'x_m':a['x_m'],
                'ambiguous':a['ambiguous'] or b['ambiguous'], 'terminal_corner':a['terminal_corner'],
                'near_corner':a['near_corner'], 'before':p, 'after':q,
                'vertical_change_m':q['signed_vertical_m']-p['signed_vertical_m'],
                'depth_change_m':q['signed_depth_m']-p['signed_depth_m'],
                'distance_change_m':q['distance_m']-p['distance_m']})
    return rows


def segment_distance(a, b, c, d):
    u, v, w = b-a, d-c, a-c
    aa, bb, cc, dd, ee = u.dot(u), u.dot(v), v.dot(v), u.dot(w), v.dot(w)
    denominator = aa*cc-bb*bb
    if aa<1e-25:return (a-(c+max(0.,min(1.,ee/cc))*v)).length if cc else w.length
    if cc<1e-25:return (a+max(0.,min(1.,-dd/aa))*u-c).length
    s = max(0.,min(1.,(bb*ee-cc*dd)/denominator)) if denominator>1e-25 else 0.
    t = (bb*s+ee)/cc
    if t<0.:t=0.;s=max(0.,min(1.,-dd/aa))
    elif t>1.:t=1.;s=max(0.,min(1.,(bb-dd)/aa))
    return (w+s*u-t*v).length


def point_triangle_distance(p, a, b, c):
    ab, ac, ap = b-a, c-a, p-a
    d1,d2=ab.dot(ap),ac.dot(ap)
    if d1<=0 and d2<=0:return ap.length
    bp=p-b;d3,d4=ab.dot(bp),ac.dot(bp)
    if d3>=0 and d4<=d3:return bp.length
    vc=d1*d4-d3*d2
    if vc<=0 and d1>=0 and d3<=0:return (p-(a+ab*d1/(d1-d3))).length
    cp=p-c;d5,d6=ab.dot(cp),ac.dot(cp)
    if d6>=0 and d5<=d6:return cp.length
    vb=d5*d2-d1*d6
    if vb<=0 and d2>=0 and d6<=0:return (p-(a+ac*d2/(d2-d6))).length
    va=d3*d6-d5*d4
    if va<=0 and d4-d3>=0 and d5-d6>=0:return (p-(b+(c-b)*(d4-d3)/((d4-d3)+(d5-d6)))).length
    total=va+vb+vc
    assert abs(total)>1e-30
    return (p-(a+ab*(vb/total)+ac*(vc/total))).length


def minimum_surface_distance(points, upper, lower):
    """Exact triangle-feature distance over selected tessellations, via AABB pruning.

    Each surviving pair checks six vertex/triangle and nine edge/edge distances.
    Intersections are checked separately. Shared-vertex pairs are omitted and
    counted because terminal connections are not opposing internal clearance.
    """
    def node(triangles):
        ids={i for t in triangles for i in t}
        low=tuple(min(points[i][k] for i in ids) for k in range(3))
        high=tuple(max(points[i][k] for i in ids) for k in range(3))
        if len(triangles)<=6:return (low,high,triangles,None)
        axis=max(range(3),key=lambda k:high[k]-low[k])
        ordered=sorted(triangles,key=lambda t:sum(points[i][axis] for i in t))
        middle=len(ordered)//2
        return (low,high,None,(node(ordered[:middle]),node(ordered[middle:])))
    def bound(a,b):return math.sqrt(sum(max(0.,a[0][k]-b[1][k],b[0][k]-a[1][k])**2 for k in range(3)))
    a,b=node(upper),node(lower);queue=[];serial=0
    heapq.heappush(queue,(bound(a,b),serial,a,b))
    best=math.inf;tested=omitted=0;example=None
    while queue:
        distance,_,a,b=heapq.heappop(queue)
        if distance>best:continue
        if a[2] is not None and b[2] is not None:
            for ta in a[2]:
                for tb in b[2]:
                    if set(ta)&set(tb):omitted+=1;continue
                    pa,pb=[points[i] for i in ta],[points[i] for i in tb]
                    value=min([point_triangle_distance(p,*pb) for p in pa]+[point_triangle_distance(p,*pa) for p in pb]+
                              [segment_distance(pa[i],pa[(i+1)%3],pb[j],pb[(j+1)%3]) for i in range(3) for j in range(3)])
                    tested+=1
                    if value<best:best=value;example=[ta,tb]
        else:
            children=([(child,b) for child in a[3]] if a[3] is not None else [(a,child) for child in b[3]])
            for ca,cb in children:
                value=bound(ca,cb)
                if value<=best:
                    serial+=1;heapq.heappush(queue,(value,serial,ca,cb))
    return {'minimum_m':best,'example':example,'triangle_pairs_tested':tested,'shared_vertex_pairs_omitted':omitted}

def mapped(point, shift):
    return tuple(point[k]-shift[k] for k in range(3))


def point_segment_distance(point, a, b):
    edge = tuple(b[k]-a[k] for k in range(3))
    length = sum(v*v for v in edge)
    t = max(0., min(1., sum((point[k]-a[k])*edge[k] for k in range(3))/length)) if length else 0.
    return math.dist(point, tuple(a[k]+t*edge[k] for k in range(3)))


def translated_branch_evidence(before, after, points, shift):
    """Account for every raw branch and pair, never truncate with zip.

    Only the same segment, or adjacent segments meeting at the same actual
    vertex within the existing error bound, can correspond. A many-to-one knot
    duplicate stays in the evidence and all resulting pair errors are checked.
    """
    result = {'rows': [], 'failures': [], 'maximum_gap_error_m': 0.,
              'raw_population_changes': 0, 'raw_identity_changes': 0}
    if len(before) != len(after):
        result['failures'].append('Translated record population differs.')
    for index in range(max(len(before), len(after))):
        if index >= len(before) or index >= len(after):
            result['rows'].append({'index': index, 'before': before[index] if index < len(before) else None,
                                   'translated': after[index] if index < len(after) else None, 'unmatched_record': True})
            continue
        a, b = before[index], after[index]
        row = {'index': index, 'side': a['side'], 'depth': a['depth'], 'x_m': a['x_m'],
               'translated_x_m': b['x_m'], 'rails': {}, 'pair_errors': [], 'failures': []}
        if (a['side'], a['depth']) != (b['side'], b['depth']) or abs(a['x_m']+shift[0]-b['x_m']) > ERROR_M:
            row['failures'].append('Translated sample identity changed.')
        population_changed = len(a['pairs']) != len(b['pairs'])
        identities_changed = False
        matches = {}
        for name in ('upper', 'lower'):
            old, new = a[name+'_branches'], b[name+'_branches']
            identities_changed |= [h['rows'] for h in old] != [h['rows'] for h in new]
            correspondence = []
            for oi, u in enumerate(old):
                for ni, v in enumerate(new):
                    point = mapped(v['point'], shift)
                    error = math.dist(u['point'], point)
                    shared = sorted(set(u['rows']) & set(v['rows']))
                    same = u['segment'] == v['segment'] and u['rows'] == v['rows']
                    knot = [i for i in shared if abs(u['segment']-v['segment']) == 1
                            and math.dist(u['point'], points[i]) <= ERROR_M and math.dist(point, points[i]) <= ERROR_M]
                    if error <= ERROR_M and (same or knot):
                        correspondence.append({'before_branch': oi, 'translated_branch': ni,
                            'reason': 'same_segment' if same else 'adjacent_segments_at_shared_vertex',
                            'shared_vertex_rows': knot, 'mapped_hit_error_m': error})
            missing_old = sorted(set(range(len(old)))-{m['before_branch'] for m in correspondence})
            missing_new = sorted(set(range(len(new)))-{m['translated_branch'] for m in correspondence})
            row['rails'][name] = {'before': old, 'translated': new, 'matches': correspondence,
                                  'unmatched_before': missing_old, 'unmatched_translated': missing_new}
            if missing_old or missing_new:
                row['failures'].append('Unmatched '+name+' branches.')
            matches[name] = correspondence
        # Cartesian pair coverage is explicit, including duplicate knot branches.
        old_pair_ids = {(p['upper_segment'], p['lower_segment']) for p in a['pairs']}
        new_pair_ids = {(p['upper_segment'], p['lower_segment']) for p in b['pairs']}
        covered_old, covered_new = set(), set()
        for u in matches['upper']:
            for l in matches['lower']:
                old_id = (a['upper_branches'][u['before_branch']]['segment'], a['lower_branches'][l['before_branch']]['segment'])
                new_id = (b['upper_branches'][u['translated_branch']]['segment'], b['lower_branches'][l['translated_branch']]['segment'])
                p = next(p for p in a['pairs'] if (p['upper_segment'], p['lower_segment']) == old_id)
                q = next(p for p in b['pairs'] if (p['upper_segment'], p['lower_segment']) == new_id)
                errors = {k: abs(p[k]-q[k]) for k in ('signed_vertical_m', 'signed_depth_m', 'distance_m')}
                row['pair_errors'].append({'before_segments': old_id, 'translated_segments': new_id, 'absolute_errors_m': errors})
                result['maximum_gap_error_m'] = max(result['maximum_gap_error_m'], *errors.values())
                covered_old.add(old_id); covered_new.add(new_id)
        row['unmatched_before_pairs'] = sorted(old_pair_ids-covered_old)
        row['unmatched_translated_pairs'] = sorted(new_pair_ids-covered_new)
        if row['unmatched_before_pairs'] or row['unmatched_translated_pairs']:
            row['failures'].append('Unmatched Cartesian branch pairs.')
        row.update(raw_population_changed=population_changed, raw_identities_changed=identities_changed)
        result['raw_population_changes'] += population_changed
        result['raw_identity_changes'] += identities_changed
        result['failures'].extend('Row '+str(index)+': '+failure for failure in row['failures'])
        result['rows'].append(row)
    return result


def shared_boundary_equivalence(row, points):
    """Only same-class hits on one shared actual triangle edge may switch owner."""
    a, b = row['before'], row['translated']
    common = sorted(set(a['triangle_vertices'] or []) & set(b['triangle_vertices'] or []))
    distances = None
    if len(common) == 2 and a['hit_point'] is not None and row['translated_hit_mapped_back'] is not None:
        edge = [points[i] for i in common]
        distances = [point_segment_distance(a['hit_point'], *edge), point_segment_distance(row['translated_hit_mapped_back'], *edge)]
    accepted = (a['kind'] == b['kind'] and row['source_face_only_changed']
        and row['source_face_relationship'] == 'edge_neighbors'
        and len(common) == 2 and row['mapped_back_hit_distance_m'] <= ERROR_M
        and row['both_hits_within_existing_1um_triangle_boundary_bound']
        and distances is not None and max(distances) <= ERROR_M)
    return {'equivalent': bool(accepted), 'shared_actual_edge': common,
            'mapped_hits_distance_to_shared_edge_m': distances, 'existing_bound_m': ERROR_M}


def ray_transitions(old, new):
    if len(old) != len(new):
        return {'failure': 'Ray population differs.', 'before_count': len(old), 'after_count': len(new)}
    gains = [i for i in range(len(old)) if old[i]['kind'] != 'internal_cavity' and new[i]['kind'] == 'internal_cavity']
    losses = [i for i in range(len(old)) if old[i]['kind'] == 'internal_cavity' and new[i]['kind'] != 'internal_cavity']
    return {'gains': gains, 'losses': losses,
            'before_cavity': sum(h['kind'] == 'internal_cavity' for h in old),
            'after_cavity': sum(h['kind'] == 'internal_cavity' for h in new), 'population': len(old)}


def corresponding_seam_rays(targets, rays, state):
    indexed = {}
    failures = []
    for label in ('before', state):
        index = {}
        for hit in rays[label]:
            target = targets[hit['target']]
            if target['state'] != label:
                continue
            key = (hit['camera'], target['side'], target['x_m'], target['fraction'])
            if key in index:
                failures.append('Duplicate corresponding seam target: '+str(key))
            index[key] = (hit, target)
        indexed[label] = index
    a, b = indexed['before'], indexed[state]
    unmatched_before, unmatched_after = sorted(a.keys()-b.keys()), sorted(b.keys()-a.keys())
    keys = sorted(a.keys() & b.keys())
    result = ray_transitions([a[k][0] for k in keys], [b[k][0] for k in keys])
    result.update(failures=failures, unmatched_before=unmatched_before, unmatched_after=unmatched_after,
                  correspondence='camera, side, actual world X, aperture fraction; targets move with each seam')
    for name in ('gains', 'losses'):
        result[name+'_details'] = [{'identity': keys[i], 'before': a[keys[i]][0], 'after': b[keys[i]][0],
            'before_target': a[keys[i]][1], 'after_target': b[keys[i]][1],
            'target_motion_m': math.dist(a[keys[i]][1]['point'], b[keys[i]][1]['point'])} for i in result[name]]
    return result

def f32(value):
    return struct.unpack('<f',struct.pack('<f',value))[0]


def rounding_cell(value):
    """IEEE binary32 nearest-even interval, derived from adjacent values."""
    rounded=f32(value)
    bits=struct.unpack('<I',struct.pack('<f',rounded))[0]
    lower_bits,upper_bits=(bits+1,bits-1) if rounded<0 else (bits-1,bits+1)
    lower=struct.unpack('<f',struct.pack('<I',lower_bits))[0]
    upper=struct.unpack('<f',struct.pack('<I',upper_bits))[0]
    return {'rounded':rounded,'lower_midpoint':(lower+rounded)/2,
        'upper_midpoint':(rounded+upper)/2,'tie_included':bits%2==0,
        'half_ulp_below':(rounded-lower)/2,'half_ulp_above':(upper-rounded)/2}


def require(condition,message):
    if not condition:
        raise ValueError(message)


def in_cell(query,cell):
    lo,hi=cell['lower_midpoint'],cell['upper_midpoint']
    return lo<query<hi or (cell['tie_included'] and query in (lo,hi))


def check_records(data):
    for label in ('before','translated'):
        rows=data[label]
        require(len(rows)==EXPECTED_RECORDS,'Missing or extra '+label+' record.')
        identities=[(r['side'],r['depth'],r['x_m']) for r in rows]
        require(len(set(identities))==len(identities),'Duplicate '+label+' record.')
    for index in range(EXPECTED_RECORDS):
        a,b=data['before'][index],data['translated'][index]
        require((a['side'],a['depth'])==(b['side'],b['depth']),'Changed side/depth record identity.')
        require(b['x_m']==a['x_m']+data['shift_m'][0],'Translated query does not equal recorded query plus recorded shift.')


def terminal_witness(record,translated,rail,branch,paths,points,shift):
    path=next(p for p in paths if p['side']==record['side'])
    chain=path[rail+str(record['depth'])]
    vertex=chain[-1]
    require(record['terminal_corner'] and branch['weight']==1.,'Missing branch is not an exact baseline terminal knot.')
    require(branch['segment']==len(chain)-2 and branch['rows']==chain[-2:], 'Wrong terminal segment or vertex provenance.')
    require(path['upper'+str(record['depth'])][-1]==path['lower'+str(record['depth'])][-1]==vertex,'Opposing paths do not share the proven terminal vertex.')
    require(vertex in points and tuple(branch['point'])==points[vertex], 'Terminal point lacks independent retained endpoint coordinates.')
    require(record['x_m']==points[vertex][0], 'Near query lacks exact baseline terminal query provenance.')
    endpoint=[f32(points[vertex][k]+shift[k]) for k in range(3)]
    witness={'side':record['side'],'depth':record['depth'],'rail':rail,
        'segment':branch['segment'],'segment_vertices':branch['rows'],'terminal_vertex':vertex,
        'baseline_weight':branch['weight'],'baseline_query_x_m':record['x_m'],
        'baseline_actual_endpoint_m':list(points[vertex]),'shift_m':list(shift),
        'recorded_translated_query_x_m':translated['x_m'],
        'calculated_float32_endpoint_m':endpoint,
        'kind':'calculated analytical terminal completion; not returned by V3 line_hits'}
    validate_endpoint(witness)
    return witness


def validate_endpoint(witness):
    base=witness['baseline_actual_endpoint_m'];shift=witness['shift_m']
    expected=[f32(base[k]+shift[k]) for k in range(3)]
    endpoint=witness['calculated_float32_endpoint_m']
    cell=rounding_cell(base[0]+shift[0])
    query=witness['recorded_translated_query_x_m']
    require(in_cell(query,cell),'Query lies outside the derived binary32 rounding interval.')
    require(query==witness['baseline_query_x_m']+shift[0], 'Translated query differs from recorded query plus shift.')
    mapped=tuple(endpoint[k]-shift[k] for k in range(3))
    mapped_error=math.dist(mapped,base)
    require(mapped_error<=ERROR_M,'Calculated endpoint mapped-point error exceeds unchanged 1 um bound.')
    require(endpoint==expected,'Calculated endpoint does not equal componentwise binary32 addition.')
    witness.update(rounding_cell_x_m=cell,
        query_minus_calculated_endpoint_x_m=query-endpoint[0],
        mapped_back_endpoint_m=list(mapped),mapped_point_error_m=mapped_error,
        ordinary_interval_tolerance_m=ORDINARY_INTERVAL_M,
        operation='Frozen V3 translated_points=[p+shift for p in baseline points]; componentwise binary32 rounded addition. Python grid uses binary64 query+shift.')


def measured_pair(upper,lower):
    delta=[upper[k]-lower[k] for k in range(3)]
    return {'signed_vertical_m':delta[2],'signed_depth_m':delta[1],
        'distance_m':math.sqrt(sum(v*v for v in delta))}


def check_pair_error(before,after):
    errors={k:abs(after[k]-before[k]) for k in ('signed_vertical_m','signed_depth_m','distance_m')}
    require(max(errors.values())<ERROR_M,'Completed pair error exceeds unchanged 1 um bound.')
    return errors


def controls(data,paths,points,result):
    records=[]
    def rejected(name,call,reason):
        try:call()
        except ValueError as error:
            require(reason in str(error),name+' failed for an unintended reason: '+str(error))
            records.append({'control':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('Negative control was accepted: '+name)
    witness=result['witnesses'][0]
    outside=copy.deepcopy(witness);outside['recorded_translated_query_x_m']=witness['rounding_cell_x_m']['upper_midpoint']+witness['rounding_cell_x_m']['half_ulp_above']
    rejected('query_outside_derived_interval',lambda:validate_endpoint(outside),'outside the derived')
    row=data['before'][0];translated=data['translated'][0];branch=row['upper_branches'][0]
    near=copy.deepcopy(row);near['x_m']+=1e-12
    rejected('near_query_without_exact_terminal',lambda:terminal_witness(near,translated,'upper',branch,paths,points,data['shift_m']),'exact baseline terminal query')
    wrong=copy.deepcopy(branch);wrong['rows'][-1]=527
    rejected('wrong_vertex',lambda:terminal_witness(row,translated,'upper',wrong,paths,points,data['shift_m']),'Wrong terminal segment or vertex')
    wrong_segment=copy.deepcopy(branch);wrong_segment['segment']-=1
    rejected('wrong_segment',lambda:terminal_witness(row,translated,'upper',wrong_segment,paths,points,data['shift_m']),'Wrong terminal segment or vertex')
    nonterminal=copy.deepcopy(row);nonterminal['terminal_corner']=False
    rejected('nonterminal_missing_branch',lambda:terminal_witness(nonterminal,translated,'upper',branch,paths,points,data['shift_m']),'not an exact baseline terminal')
    endpoint=copy.deepcopy(witness);endpoint['calculated_float32_endpoint_m'][2]+=2e-6
    rejected('endpoint_error_over_1um',lambda:validate_endpoint(endpoint),'endpoint mapped-point error')
    pair=result['pair_completions'][0];changed=copy.deepcopy(pair['calculated_pair']);changed['signed_vertical_m']+=2e-6
    rejected('pair_error_over_1um',lambda:check_pair_error(pair['before_pair'],changed),'pair error exceeds')
    missing=copy.deepcopy(data);missing['translated'].pop()
    rejected('missing_record',lambda:check_records(missing),'Missing or extra')
    duplicate=copy.deepcopy(data);duplicate['translated'][1]=copy.deepcopy(duplicate['translated'][0])
    rejected('duplicate_record',lambda:check_records(duplicate),'Duplicate translated record')
    return records


def complete_translation(data,paths,points):
    check_records(data)
    raw=translated_branch_evidence(data['before'],data['translated'],points,data['shift_m'])
    completed=copy.deepcopy(data['translated']);witnesses=[];pairs=[]
    for row in raw['rows']:
        i=row['index'];before=data['before'][i];after=completed[i]
        for rail in ('upper','lower'):
            evidence=row['rails'][rail]
            require(not evidence['unmatched_translated'],'Unexpected translated branch has no baseline provenance.')
            for missing in evidence['unmatched_before']:
                original=before[rail+'_branches'][missing]
                witness=terminal_witness(before,after,rail,original,paths,points,data['shift_m'])
                witness.update(record_index=i,before_branch_index=missing)
                branch=copy.deepcopy(original);branch.update(point=witness['calculated_float32_endpoint_m'],analytical_completion=True)
                after[rail+'_branches'].append(branch);witnesses.append(witness)
        for upper in after['upper_branches']:
            for lower in after['lower_branches']:
                if not (upper.get('analytical_completion') or lower.get('analytical_completion')):continue
                pair=measured_pair(upper['point'],lower['point'])
                pair.update(upper_segment=upper['segment'],lower_segment=lower['segment'],analytical_completion=True)
                old=[p for p in before['pairs'] if (p['upper_segment'],p['lower_segment'])==(pair['upper_segment'],pair['lower_segment'])]
                require(len(old)==1,'Calculated terminal pair lacks exact baseline segment provenance.')
                error=check_pair_error(old[0],pair);after['pairs'].append(pair)
                pairs.append({'record_index':i,'before_pair':old[0],'calculated_pair':pair,'absolute_errors_m':error})
    matched=translated_branch_evidence(data['before'],completed,points,data['shift_m'])
    require(not matched['failures'],'Live translated geometry has unmatched nonterminal branches or pairs.')
    require(matched['maximum_gap_error_m']<ERROR_M,'Live complete translation gap error exceeds1um.')
    census={'records':len(data['before']),'baseline_pairs':sum(len(r['pairs']) for r in data['before']),
        'raw_returned_pairs':sum(len(r['pairs']) for r in data['translated']),
        'calculated_pairs':len(pairs),'calculated_branches':len(witnesses),
        'accounted_pairs':sum(len(r['pairs']) for r in completed)}
    require(census['baseline_pairs']==census['accounted_pairs'],'Translation pair census is incomplete.')
    result={'census':census,'witnesses':witnesses,'pair_completions':pairs,
        'maximum_complete_gap_error_m':matched['maximum_gap_error_m'],
        'raw_population_changes':[r for r in raw['rows'] if r['raw_population_changed']],
        'raw_identity_changes':raw['raw_identity_changes']}
    result['negative_controls']=controls(data,paths,points,result)
    return result

def aperture_targets(records_by_state):
    targets=[]
    for label,records in records_by_state:
        for record in records:
            if record['depth'] or record['ambiguous'] or record['terminal_corner']:continue
            a=Vector(record['upper_branches'][0]['point']);b=Vector(record['lower_branches'][0]['point'])
            for fraction in (.2,.5,.8):
                targets.append({'state':label,'side':record['side'],'x_m':record['x_m'],
                    'near_corner':record['near_corner'],'fraction':fraction,'point':list(a.lerp(b,fraction))})
    assert targets and any(row['near_corner'] for row in targets)
    return targets


def body_first_hits(state,targets,origins,regions,translation=None):
    shift=Vector((0,0,0)) if translation is None else translation
    points=state['points'] if translation is None else [p+shift for p in state['points']]
    tree=BVHTree.FromPolygons(points,state['triangles'],all_triangles=True,epsilon=0)
    results=[]
    for name,origin in origins.items():
        start=origin+shift
        for row,target in enumerate(targets):
            point=Vector(target['point'])+shift;direction=(point-start).normalized()
            location,normal,index,distance=tree.ray_cast(start,direction,3.)
            if index is None:kind='no_body_hit';owner=None
            else:
                owner=state['owners'][state['triangle_polygons'][index]]
                kind='internal_cavity' if owner in regions['inside'] else ('oral_strip' if owner in regions['strip'] else 'exterior_skin')
            boundary=None
            if index is not None:
                vertices=[points[i] for i in state['triangles'][index]]
                distances=[]
                for a,b in zip(vertices,vertices[1:]+vertices[:1]):
                    direction=b-a
                    t=max(0.,min(1.,(location-a).dot(direction)/direction.length_squared)) if direction.length_squared else 0.
                    distances.append((location-(a+direction*t)).length)
                boundary=min(distances)
            results.append({'camera':name,'target':row,'kind':kind,'source_face':owner,
                'distance_m':distance,'hit_point':list(location) if location is not None else None,
                'actual_triangle_index':index,
                'triangle_vertices':state['triangles'][index] if index is not None else None,
                'evaluated_polygon':state['triangle_polygons'][index] if index is not None else None,
                'minimum_actual_triangle_boundary_distance_m':boundary,
                'boundary_within_existing_1um_bound':boundary<=1e-6 if boundary is not None else None})
    return results


class _Run:
    def __init__(self,body,expected_contract_sha256):
        self.body=body;self.original=body.data;self.work=None
        require(INPUT_PROPERTY in body,'Missing reference_smile_input; the live gate cannot be omitted.')
        encoded=body[INPUT_PROPERTY]
        require(isinstance(encoded,str) and _digest(encoded)==expected_contract_sha256,'Changed reference_smile_input digest; supply the pinned build input.')
        self.contract=json.loads(encoded);c=self.contract
        require(c['schema']==1 and c['gate']=='evaluated_exterior_aperture','Unknown reference smile input contract.')
        self.source_faces=[tuple(p.vertices) for p in self.original.polygons]
        self.proposed=[v.co.copy() for v in self.original.vertices]
        require(len(self.proposed)==c['vertex_count']==19158,'Changed reference smile source population.')
        require(_topology(self.source_faces)==c['topology_sha256'],'Changed reference smile source topology.')
        require(body.matrix_world==Matrix.Identity(4),'Reference smile final object transform changed.')
        mods=list(body.modifiers)
        require(len(mods)==1 and mods[0].type=='SUBSURF' and mods[0].levels==mods[0].render_levels==2 and mods[0].subdivision_type=='CATMULL_CLARK' and mods[0].use_limit_surface,'Reference smile requires the retained final CC2 limit-surface modifier.')
        require(not self.original.shape_keys and not any(a.name in {'crease_vert','crease_edge',ATTRIBUTE} for a in self.original.attributes),'Reference smile topology/shape-key/crease contract changed.')
        self.changed_rows=c['changed_rows'];self.sections=[tuple(p) for p in c['oral_sections']]
        self.paths=c['oral_paths'];self.corner_sections=c['corner_sections']
        self.contact=tuple(i for pair in self.sections for i in pair)
        require(len(self.contact)==len(set(self.contact))==76 and len(self.sections)==38,'Reference smile complete oral strip is missing.')
        require(self.changed_rows==sorted(set(self.changed_rows)) and len(self.changed_rows)==522,'Reference smile changed-row contract differs from the approved field.')
        require([r['row'] for r in c['coordinates']]==self.changed_rows,'Missing/duplicate reference smile coordinate input.')
        self.neutral=[p.copy() for p in self.proposed]
        for row in c['coordinates']:
            i=row['row'];before=Vector(row['neutral']);after=Vector(row['proposed'])
            require(all(math.isfinite(v) for v in (*before,*after)) and self.proposed[i]==after,f'Reference smile final coordinate agreement failed at row{i}.')
            require(before.x==after.x,f'Reference smile input changes width at row{i}.')
            self.neutral[i]=before
        self.report={'gate':'evaluated_exterior_aperture','input_sha256':expected_contract_sha256,
            'historical_source_vector_diagnostic':c['historical_source_vector_diagnostic'],'failures':[]}

    def raw_evaluated(self):
        bpy.context.view_layer.update()
        evaluated=self.body.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh=evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            points=[v.co.copy() for v in mesh.vertices]
            faces=[tuple(p.vertices) for p in mesh.polygons]
            triangles=[tuple(t.vertices) for t in mesh.loop_triangles]
            polygon_ids=[t.polygon_index for t in mesh.loop_triangles]
            owners=[v.value for v in mesh.attributes[ATTRIBUTE].data] if ATTRIBUTE in mesh.attributes else None
            return {'points':points,'faces':faces,'triangles':triangles,'triangle_polygons':polygon_ids,'owners':owners}
        finally:evaluated.to_mesh_clear()


    def capture(self):
        state=self.raw_evaluated()
        owners=state['owners']
        assert owners is not None and len(owners)==len(state['faces'])
        counts=Counter(owners)
        assert set(counts)==set(range(len(self.source_faces)))
        assert all(counts[i]==len(face)*4 for i,face in enumerate(self.source_faces)), 'Face-domain provenance did not propagate to every level2 descendant.'
        prediction=catmull_clark_limit([v.co.copy() for v in self.work.vertices],self.source_faces,self.contact)
        tree=KDTree(len(state['points']))
        for i,p in enumerate(state['points']):tree.insert(p,i)
        tree.balance();mapping={};errors=[]
        for i in self.contact:
            co,index,error=tree.find(prediction[i])
            assert error<1e-6,f'Full oral anchor {i} failed the unchanged 1 um CC correspondence: {error} m.'
            mapping[i]=index;errors.append(error)
        assert len(set(mapping.values()))==76
        paths,seams=trace_descendant_edges(self.source_faces,state['faces'],owners,mapping,self.paths,self.sections)
        state.update(anchor_indices=mapping,anchor_error_m=max(errors),paths=paths,
            descendant_source_edges=len(seams),descendant_edge_count=sum(len(v)-1 for v in seams.values()))
        return state


    def set_points(self,points):
        self.work.vertices.foreach_set('co',[v for p in points for v in p])
        self.work.update();bpy.context.view_layer.update()


    def compare_structure(self,old,new,regions):
        assert old['faces']==new['faces'] and old['owners']==new['owners']
        assert old['anchor_indices']==new['anchor_indices'] and old['paths']==new['paths']
        assert all(a.x==b.x for a,b in zip(old['points'],new['points'])), 'A descendant X changed; rebuild a union-X grid before measuring.'
        changed={i for i,(a,b) in enumerate(zip(old['points'],new['points'])) if a!=b}
        source_changed=set(self.changed_rows)
        affected_source={fi for fi,face in enumerate(self.source_faces) if source_changed.intersection(face)}
        relevant=set(affected_source)
        source_edges=regions['edges']
        for adjacent in source_edges.values():
            if affected_source.intersection(adjacent):relevant.update(adjacent)
        corner_rows={i for corner in self.corner_sections for i in self.sections[corner]}
        corner_faces={fi for fi,face in enumerate(self.source_faces) if corner_rows.intersection(face)}
        corner_patch=set(corner_faces)
        for adjacent in source_edges.values():
            if corner_faces.intersection(adjacent):corner_patch.update(adjacent)
        relevant.update(corner_patch)
        previous_triangles={i for i,t in enumerate(old['triangles']) if (
            abs(sum(old['points'][j].x for j in t)/3)<.045 and
            sum(old['points'][j].y for j in t)/3<-.105 and
            1.455<sum(old['points'][j].z for j in t)/3<1.505)}
        population_polygons={pi for pi,owner in enumerate(old['owners']) if owner in relevant}
        population_polygons.update(old['triangle_polygons'][i] for i in previous_triangles)
        lookups=[{tuple(sorted(t)):pi for t,pi in zip(state['triangles'],state['triangle_polygons'])} for state in (old,new)]
        affected=0;area=dot=1.
        # Cover the union of both ACTUAL tessellations. Changed quad diagonals use
        # stable evaluated face provenance for collision comparison below.
        for t in set(old['triangles'])|set(new['triangles']):
            if not changed.intersection(t):continue
            key=tuple(sorted(t));pi=lookups[1].get(key,lookups[0].get(key))
            assert pi in population_polygons, 'Changed evaluated descendant lies outside complete support/neighbor/old-region union.'
            a,b=normal(old['points'],t),normal(new['points'],t)
            assert a.length>0 and b.length>0
            ratio=b.length/a.length;cosine=a.normalized().dot(b.normalized())
            assert ratio>.25 and cosine>0,f'Evaluated triangle {t} folds/collapses: {ratio}/{cosine}.'
            area=min(area,ratio);dot=min(dot,cosine);affected+=1
        assert affected>1000 and len(population_polygons)>500
        populations=[[t for t,pi in zip(state['triangles'],state['triangle_polygons']) if pi in population_polygons] for state in (old,new)]
        before_hits,before_stats=intersections(old['points'],populations[0])
        after_hits,after_stats=intersections(new['points'],populations[1])
        stable=lambda hits,lookup:{tuple(sorted((lookup[a],lookup[b]))) for a,b in hits}
        new_hits=stable(after_hits,lookups[1])-stable(before_hits,lookups[0])
        internal=[];internal_stable=[]
        for number,(label,state) in enumerate([('before',old),('proposal',new)]):
            inner_upper=[t for t,pi in zip(state['triangles'],state['triangle_polygons']) if state['owners'][pi] in regions['inner_upper']]
            inner_lower=[t for t,pi in zip(state['triangles'],state['triangle_polygons']) if state['owners'][pi] in regions['inner_lower']]
            assert inner_upper and inner_lower
            upper_ids={tuple(sorted(t)) for t in inner_upper};lower_ids={tuple(sorted(t)) for t in inner_lower}
            hits,stats=intersections(state['points'],inner_upper+inner_lower)
            crossed=[pair for pair in hits if ((pair[0] in upper_ids and pair[1] in lower_ids) or (pair[1] in upper_ids and pair[0] in lower_ids))]
            distance=minimum_surface_distance(state['points'],inner_upper,inner_lower)
            distance['intersection_adjusted_minimum_m']=0. if crossed else distance['minimum_m']
            internal_stable.append(stable(crossed,lookups[number]))
            internal.append({'state':label,'upper_triangles':len(inner_upper),'lower_triangles':len(inner_lower),
                'cross_upper_lower_intersections':len(crossed),'crossed_pair_examples':crossed[:10],
                'narrow_phase':stats,'minimum_feature_distance':distance,
                'omitted_source_tie_faces':sorted(regions['inner_ties'])})
        central=[]
        for pair in [(520,523),(537,540)]:
            a=(old['points'][old['anchor_indices'][pair[0]]]-old['points'][old['anchor_indices'][pair[1]]]).length
            b=(new['points'][new['anchor_indices'][pair[0]]]-new['points'][new['anchor_indices'][pair[1]]]).length
            central.append({'rows':pair,'before_gap_m':a,'after_gap_m':b,'increase_m':b-a})
            if b-a>=.00005:self.report['failures'].append('Legacy central evaluated scalar gap exceeds unchanged 50 um increase: '+str(pair))
        if new_hits:self.report['failures'].append('New nonadjacent evaluated intersections in complete population: '+str(len(new_hits)))
        new_internal=internal_stable[1]-internal_stable[0]
        if new_internal:
            self.report['failures'].append('New opposing inner-cavity surface intersections.')
        return {'changed_evaluated_vertices':len(changed),'affected_evaluated_triangles':affected,
            'minimum_area_ratio':area,'minimum_normal_dot':dot,'affected_source_faces':len(affected_source),
            'support_plus_neighbor_source_faces':len(relevant),'old_region_triangles':len(previous_triangles),
            'complete_corner_source_faces':len(corner_patch),'union_evaluated_polygons':len(population_polygons),
            'union_triangles_before_after':[len(p) for p in populations],
            'actual_tessellation_changed':old['triangles']!=new['triangles'],
            'intersection_pair_identity':'Actual tessellation narrow phase in each state; stable evaluated polygon-pair provenance compares new crossings across possible diagonal changes.',
            'before_intersections':before_stats,'after_intersections':after_stats,
            'new_intersections':len(new_hits),'new_pair_examples':list(new_hits)[:10],
            'inner_surfaces':internal,'new_internal_polygon_pairs':list(new_internal),'legacy_central_pairs':central,
            'shared_vertex_pairs':'Excluded by the preserved narrow phase; not certified collision-free.'}

    def run(self,origins):
        try:
            require(set(origins)=={'portrait','face_oblique'},'Reference smile needs portrait and opposite oblique camera origins.')
            origins={name:Vector(value) for name,value in origins.items()}
            untouched=self.raw_evaluated()
            self.work=self.original.copy();self.body.data=self.work
            attribute=self.work.attributes.new(ATTRIBUTE,'INT','FACE')
            attribute.data.foreach_set('value',list(range(len(self.source_faces))))
            instrumented=self.raw_evaluated()
            require(untouched['points']==instrumented['points'] and untouched['faces']==instrumented['faces'],'Source-face provenance altered evaluated geometry.')
            self.set_points(self.neutral);baseline=self.capture()
            require(baseline==self.capture(),'Unchanged live evaluation control failed.')
            regions=source_regions(self.source_faces,self.sections,self.paths)
            self.set_points(self.proposed);proposal=self.capture()
            require(all(a.x==b.x for a,b in zip(baseline['points'],proposal['points'])),'A proposal descendant X changed; retained common-X grid is invalid.')
            base_gaps,grids=common_x_gaps(baseline['points'],baseline['paths'])
            new_gaps,_=common_x_gaps(proposal['points'],proposal['paths'],grids)
            comparison=compare_gaps(base_gaps,new_gaps)
            structure=self.compare_structure(baseline,proposal,regions)
            self.report.update(structure=structure,oral_anchors=76,
                maximum_anchor_error_m=max(baseline['anchor_error_m'],proposal['anchor_error_m']),
                oral_descendant_edges=baseline['descendant_edge_count'])
            crossed=[Vector(p) for p in [(0,0,0),(1,0,0),(0,1,0),(.2,.2,-.1),(.2,.2,.1),(.8,.2,0)]]
            require(len(intersections(crossed,[(0,1,2),(3,4,5)])[0])==1,'Triangle crossing control failed to reject an intersection.')
            require(not intersections(crossed[:3]+[p+Vector((0,0,2)) for p in crossed[3:]],[(0,1,2),(3,4,5)])[0],'Separated triangle control reports an intersection.')
            distance_control=[Vector(p) for p in [(0,0,0),(.01,0,0),(0,.01,0),(0,0,.002),(.01,0,.002),(0,.01,.002)]]
            require(abs(minimum_surface_distance(distance_control,[(0,1,2)],[(3,4,5)])['minimum_m']-.002)<1e-8,'Known2mm internal-distance control failed.')
            shift=Vector((.001,.002,.003))
            shifted_gaps,_=common_x_gaps([p+shift for p in baseline['points']],baseline['paths'],
                {key:[x+shift.x for x in xs] for key,xs in grids.items()})
            data={'before':base_gaps,'translated':shifted_gaps,'shift_m':list(shift)}
            live_path_points={i:tuple(baseline['points'][i]) for path in baseline['paths'] for name,chain in path.items() if name!='side' for i in chain}
            translation=complete_translation(data,baseline['paths'],live_path_points)
            self.report['translation']=translation
            # Positive opening control is the preserved3mm upper strip field.
            control=[p.copy() for p in self.neutral]
            upper={i for path in self.paths for section in path['upper'] for i in self.sections[section]}
            lower={i for path in self.paths for section in path['lower'] for i in self.sections[section]}
            distances={i:0 for i in upper-lower};front=set(distances);adjacency=defaultdict(set)
            for face in self.source_faces:
                for i in face:adjacency[i].update(face)
            for depth in (1,2):
                front={j for i in front for j in adjacency[i]}-set(distances)-lower
                distances.update({i:depth for i in front})
            for i,depth in distances.items():
                control[i].z+=.003*max(0.,1.-(abs(self.neutral[i].x)/.0242)**2)*(1.-depth/3.)
            self.set_points(control);opening=self.capture()
            require(opening['faces']==baseline['faces'] and opening['owners']==baseline['owners'] and opening['paths']==baseline['paths'],'Opening control changed actual topology.')
            require(all(a.x==b.x for a,b in zip(baseline['points'],opening['points'])),'Opening control changed X; common-X grid is invalid.')
            opening_gaps,_=common_x_gaps(opening['points'],opening['paths'],grids)
            opening_changes=compare_gaps(base_gaps,opening_gaps)
            positive=max(r['vertical_change_m'] for r in opening_changes if r['depth']==0 and not r['terminal_corner'] and not r['ambiguous'])
            targets=aperture_targets([('before',base_gaps),('proposal',new_gaps),('opening_control',opening_gaps)])
            rays={name:body_first_hits(state,targets,origins,regions) for name,state in [('before',baseline),('proposal',proposal),('opening_control',opening)]}
            shifted_rays=body_first_hits(baseline,targets,origins,regions,shift)
            require(len(rays['before'])==len(shifted_rays),'Translation changed ray population.')
            neighbors=defaultdict(set)
            for adjacent in regions['edges'].values():
                for fi in adjacent:neighbors[fi].update(set(adjacent)-{fi})
            mismatches=[]
            for index in range(len(shifted_rays)):
                a,b=rays['before'][index],shifted_rays[index]
                require((a['camera'],a['target'])==(b['camera'],b['target']),'Translation changed camera/target identity.')
                semantic=a['kind']!=b['kind'];face_only=not semantic and a['source_face']!=b['source_face']
                if not (semantic or face_only):continue
                back=Vector(b['hit_point'])-shift if b['hit_point'] is not None else None
                old,new=a['source_face'],b['source_face']
                row={'ray_index':index,'semantic_kind_changed':semantic,'source_face_only_changed':face_only,
                    'before':a,'translated':b,'translated_hit_mapped_back':list(back) if back is not None else None,
                    'mapped_back_hit_distance_m':(back-Vector(a['hit_point'])).length if back is not None and a['hit_point'] is not None else None,
                    'source_face_relationship':'edge_neighbors' if old is not None and new in neighbors[old] else 'other',
                    'both_hits_within_existing_1um_triangle_boundary_bound':a['boundary_within_existing_1um_bound'] and b['boundary_within_existing_1um_bound']}
                row['ownership_equivalence']=shared_boundary_equivalence(row,baseline['points']);mismatches.append(row)
            fixed={name:ray_transitions(rays['before'],rays[name]) for name in ('proposal','opening_control')}
            corresponding={name:corresponding_seam_rays(targets,rays,name) for name in ('proposal','opening_control')}
            exterior=[r for r in comparison if r['depth']==0 and not r['terminal_corner'] and not r['ambiguous']]
            aperture_failures=[r for r in exterior if r['distance_change_m']>=APERTURE_INCREASE_M or r['vertical_change_m']>=APERTURE_INCREASE_M]
            self.report.update(exterior_aperture={'bound_m':APERTURE_INCREASE_M,'samples':len(exterior),
                'maximum_scalar_increase_m':max(r['distance_change_m'] for r in exterior),
                'maximum_vertical_increase_m':max(r['vertical_change_m'] for r in exterior),
                'maximum_absolute_depth_change_m':max(abs(r['depth_change_m']) for r in exterior),
                'near_corner_samples':sum(r['near_corner'] for r in exterior),'failures':aperture_failures,
                'ambiguous_records':[r for r in base_gaps if r['ambiguous']],
                'terminal_records':[r for r in base_gaps if r['terminal_corner']]},
                translation_ray_mismatches=mismatches,opening_vertical_increase_m=positive,
                fixed_ray_transitions=fixed,corresponding_seam_transitions=corresponding,
                ray_bound='Body-first-hit only. Both fixed and seam-following occupancy gains/losses can reflect a moved existing seam; actual exterior gaps determine bounded enlargement. Hair/cloth occlusion omitted.')
            require(all(r['ownership_equivalence']['equivalent'] for r in mismatches),'Translation changed semantic class or failed strict shared actual-edge ownership equivalence.')
            for name,result in corresponding.items():
                require(not result['failures'] and not result['unmatched_before'] and not result['unmatched_after'],'Corresponding seam ray population differs: '+name)
            require(positive>.001,'Opening control fails to show >1mm opening in the same unambiguous exterior population.')
            require(fixed['opening_control']['gains'] and corresponding['opening_control']['gains'],'Opening control fails to expose cavity in both ray measurements.')
            require(not aperture_failures,'Actual exterior scalar/vertical gap increase reaches the50um bound.')
            require(not self.report['failures'],'Actual surface/central gate failed: '+str(self.report['failures']))
            self.report['status']='pass; live evaluated geometry and controls, within stated bounds'
            return self.report
        except Exception as error:
            self.report.update(status='fail',error=str(error))
            raise SmileVerificationError(str(error),self.report) from error
        finally:
            self.body.data=self.original
            if self.work is not None:bpy.data.meshes.remove(self.work)
            bpy.context.view_layer.update()
            require([v.co for v in self.original.vertices]==self.proposed,'Reference smile gate failed to preserve the actual source mesh.')
            require(ATTRIBUTE not in self.original.attributes,'Reference smile temporary provenance leaked into actual mesh.')


def verify_reference_smile(body,camera_origins,*,expected_contract_sha256):
    """Measure live final geometry; the input digest is not a pass receipt.

    Call again after reopening a saved blend. The caller must pin the input
    digest and independently verify neutral coordinates against the accepted
    pre-smile body. SmileVerificationError.report retains measured counterevidence.
    """
    return _Run(body,expected_contract_sha256).run(camera_origins)

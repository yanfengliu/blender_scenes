"""Continuous grooming controls and a bounded front-fringe coverage instrument.

The scanlines measure actual opaque filament intervals in a frontal orthographic
projection, not photographic density, oblique coverage or aesthetic acceptance.
"""
import math


def smooth(value):
    t = max(0.0, min(1.0, value))
    return t*t*(3-2*t)


def coverage_fraction(sample):
    """Front density is 0.82 of the rear; preserve every angular interval."""
    def mass(x):
        u = max(0.0, min(1.0, (x-.16)/.19))
        return .82*x+.18*(.19*(u**3-.5*u**4)+max(0.0, x-.35))
    target = sample*mass(1.0)
    low, high = 0.0, 1.0
    for _ in range(24):
        middle = (low+high)/2
        if mass(middle) < target: low = middle
        else: high = middle
    return (low+high)/2


# Unequal combed groups: azimuth, brow-tip height, lateral flow offset (radians).
# The same rounded transitions shape the tips and their neighboring filaments.
# No repeated-frequency peak field is used: candidate8 rendered it as cut teeth.
_FRINGE_LOCKS = {
    -1: ((-math.pi/2,.009,0.), (-1.31,.007,.050), (-1.02,.014,-.012),
         (-.78,.010,0.), (-.62,.010,0.)),
    1: ((-math.pi/2,.009,0.), (-1.23,.014,.060), (-.94,.0065,-.010),
        (-.62,.010,0.)),
}

# Broad side/back regions: azimuth, scalp exit elevation, vertical flow offset,
# tip-length offset. Neighboring sectors turn at unequal heights without a row
# of identical ear-height bends or a shared periodic lower edge.
_FALL_GROUPS = {
    -1: ((-.84,.55,.008,.002), (-.31,.62,.014,-.005), (.27,.48,-.010,.007),
         (.88,.58,.005,-.006), (math.pi/2,.53,-.006,.004)),
    1: ((-.84,.56,.005,.003), (-.18,.49,-.012,-.004), (.52,.61,.010,.008),
        (1.08,.51,-.004,-.006), (math.pi/2,.53,-.006,.004)),
}


def _group_values(groups, parameter):
    if parameter <= groups[0][0]: return groups[0][1:]
    for first, last in zip(groups, groups[1:]):
        if parameter <= last[0]:
            weight = smooth((parameter-first[0])/(last[0]-first[0]))
            return tuple(a+(b-a)*weight for a,b in zip(first[1:],last[1:]))
    return groups[-1][1:]


def comb_fraction(fraction, progress, side):
    """Ordered, unequal lock flow; no guide attraction or empty intervals.

    The largest control slope gives a derivative above 0.63. The offset
    vanishes at both domain boundaries and at the scalp root.
    """
    parameter = fraction*math.pi-math.pi/2
    _, flow = _group_values(_FRINGE_LOCKS[side], parameter)
    return fraction+flow/math.pi*smooth((progress-.12)/.65)


def fringe_tip_height(parameter, side):
    """Few broad unequal brow-length groups, with feathering in child lengths."""
    return _group_values(_FRINGE_LOCKS[side], parameter)[0]


def fall_shape(parameter, side):
    return _group_values(_FALL_GROUPS[side], parameter)


def strand_radius(progress, shaft, fringe):
    # Retain a visible shaft to the brows; taper only the physical free tip.
    start, span = (.84, .16) if fringe else (.90, .10)
    tip = 1-.96*smooth((progress-start)/span)
    root = .85+.15*min(1.0, progress/.10)
    return shaft*root*tip


def add_strand(data, points, rng, fringe=False):
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    spline.points.foreach_set('co', [v for point in points for v in (*point, 1.0)])
    shaft = rng.uniform(.85, 1.25) if fringe else rng.uniform(2/3, 4/3)
    spline.points.foreach_set('radius', [strand_radius(i/(len(points)-1), shaft, fringe)
                                         for i in range(len(points))])
    spline.material_index = rng.choices(range(4), (26, 43, 25, 6))[0]


def fringe_coverage(objects, eye_height, centre_y, half_width=.050):
    """Measure actual curve coordinates and radii, never saved pass metadata.

    Three frontal scanlines 20/35/50 mm above the eye joint cover the central
    100 mm of forehead. Conservative radius intervals omit projected cylinder
    obliquity, illumination, depth ordering and antialiasing. Long side locks
    outside that window cannot satisfy the fringe check.
    """
    levels = [eye_height+offset for offset in (.020, .035, .050)]
    intervals = [[] for _ in levels]
    retention, ends = [], []
    for obj in objects:
        if obj.type != 'CURVE' or obj.data.dimensions != '3D' or obj.modifiers:
            raise ValueError('Fringe coverage requires unmodified three-dimensional filament curves.')
        if any(abs(value-1) > 1e-8 for value in obj.scale):
            raise ValueError('Fringe coverage requires unit object scale.')
        for material in obj.data.materials:
            shaders = [n for n in material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'] if material.use_nodes else []
            if len(shaders) != 1 or shaders[0].inputs['Alpha'].is_linked or shaders[0].inputs['Alpha'].default_value != 1:
                raise ValueError('Fringe coverage requires the opaque single-Principled filament material.')
        for spline in obj.data.splines:
            if spline.type != 'POLY': raise ValueError('Fringe coverage requires actual POLY filament points.')
            points = [(obj.matrix_world @ p.co.xyz, obj.data.bevel_depth*p.radius) for p in spline.points]
            if points[-1][0].z > eye_height+.004 and abs(points[-1][0].x) < half_width+.010:
                widest = max(radius for _, radius in points)
                if widest <= 0: raise ValueError('A fringe strand has no physical shaft radius.')
                retention.append(points[round(.8*(len(points)-1))][1]/widest)
                ends.append(points[-1][0].z-eye_height)
            for (a, ra), (b, rb) in zip(points, points[1:]):
                for level, hits in zip(levels, intervals):
                    if not (min(a.z, b.z) <= level < max(a.z, b.z)): continue
                    t = (level-a.z)/(b.z-a.z)
                    x, y = a.x+t*(b.x-a.x), a.y+t*(b.y-a.y)
                    radius = ra+t*(rb-ra)
                    if y < centre_y-.04 and abs(x) < half_width+radius:
                        hits.append((max(-half_width, x-radius), min(half_width, x+radius)))
    rows = []
    for level, hits in zip(levels, intervals):
        covered = 0.0
        cursor = -half_width
        largest_gap = 0.0
        for left, right in sorted(hits):
            largest_gap = max(largest_gap, left-cursor)
            if right > cursor:
                covered += right-max(left, cursor)
                cursor = right
        largest_gap = max(largest_gap, half_width-cursor)
        rows.append({'height_m': level, 'strand_intersections': len(hits),
                     'covered_fraction': covered/(2*half_width), 'largest_gap_m': largest_gap})
    failures = []
    if any(row['covered_fraction'] < .65 for row in rows):
        failures.append('A central-forehead scanline has less than 65% opaque filament interval coverage.')
    if any(row['largest_gap_m'] >= .008 for row in rows):
        failures.append('A central-forehead scanline has an uncovered interval of 8 mm or more.')
    if not retention or min(retention) < .85:
        failures.append('Fringe shaft radius at 80% length falls below 85% of its maximum, producing early fade.')
    return {'scanlines': rows, 'window_half_width_m': half_width,
            'fringe_strands': len(retention), 'minimum_shaft_retention_at80pct': min(retention) if retention else 0,
            'tip_height_above_eye_range_m': [min(ends), max(ends)] if ends else [],
            'pass': not failures, 'failures': failures, 'bound': fringe_coverage.__doc__}


def crown_scanlines(objects,head):
    levels=[head.top-offset for offset in (.012,.022,.035)]
    hits=[[] for _ in levels];half=.008
    for obj in objects:
        for spline in obj.data.splines:
            points=[(obj.matrix_world@p.co.xyz,obj.data.bevel_depth*p.radius) for p in spline.points]
            for (a,ra),(b,rb) in zip(points,points[1:]):
                for z,intervals in zip(levels,hits):
                    if not min(a.z,b.z)<=z<max(a.z,b.z):continue
                    t=(z-a.z)/(b.z-a.z);x=a.x+t*(b.x-a.x);y=a.y+t*(b.y-a.y);r=ra+t*(rb-ra)
                    if abs(x)>half+r:continue
                    skin=head.front(x,z)
                    if skin is not None and y<skin:intervals.append((max(-half,x-r),min(half,x+r)))
    rows=[]
    for z,intervals in zip(levels,hits):
        cursor=-half;covered=0.;largest=0.
        for a,b in sorted(intervals):
            largest=max(largest,a-cursor)
            if b>cursor:covered+=b-max(a,cursor);cursor=b
        rows.append({'height_m':z,'coverage':covered/(2*half),'largest_gap_m':max(largest,half-cursor)})
    return rows


def crown_coverage(objects, head):
    """Reject a straight exposed crown cleft in a bounded frontal projection.

    Actual foreground strands in the central 16 mm window, at 12/22/35 mm
    below the anatomical top. A gap must remain below 2 mm. Only the front
    of the actual scalp contributes, so rear strands cannot conceal a cleft.
    Three finite slices do not prove continuous scalp coverage or appearance.
    """
    rows = crown_scanlines(objects, head)
    return {'pass': all(row['largest_gap_m'] < .002 for row in rows),
            'scanlines': rows, 'maximum_allowed_gap_m': .002,
            'window_half_width_m': .008, 'bound': crown_coverage.__doc__}


def temple_scanlines(objects,head):
    """Six finite angular projections of the actual upper-temple filaments."""
    low,high=-1.10,-.45
    rows=[]
    for side in (-1,1):
        for height in (head.eye+.035,head.eye+.055,head.eye+.075):
            intervals=[]
            for obj in objects:
                for spline in obj.data.splines:
                    for a,b in zip(spline.points,spline.points[1:]):
                        if not min(a.co.z,b.co.z)<=height<max(a.co.z,b.co.z):continue
                        t=(height-a.co.z)/(b.co.z-a.co.z)
                        x=a.co.x+t*(b.co.x-a.co.x)-head.cx
                        y=a.co.y+t*(b.co.y-a.co.y)-head.cy
                        if side*x<=0:continue
                        azimuth=math.atan2(y,abs(x));radius=math.hypot(x,y)
                        if not low-.01<azimuth<high+.01:continue
                        skin=head.radial_skin(x,y,height)
                        if skin is None or radius<skin:continue
                        width=math.asin(min(1,obj.data.bevel_depth*(a.radius+t*(b.radius-a.radius))/radius))
                        intervals.append((max(low,azimuth-width),min(high,azimuth+width)))
            cursor=low;largest=covered=0.
            for a,b in sorted(intervals):
                if b<a:continue
                largest=max(largest,a-cursor)
                if b>cursor:covered+=b-max(a,cursor);cursor=b
            rows.append({'side':side,'height_m':height,'coverage':covered/(high-low),
                         'largest_gap_radians':max(largest,high-cursor),
                         'window_radians':[low,high]})
    return {'rows':rows,'bound':'Actual filament angular intervals outside actual scalp at six upper-temple slices; angular gaps are not rendered projected gaps or aesthetic acceptance.'}


def temple_coverage(objects,head):
    """Reject an empty fringe-to-side sector; this cannot certify appearance.

    At 35/55/75 mm above the eye joint on both sides, an uncovered angle must
    stay below .02 radians (2 mm arc at a 100 mm radius). Only strands outside
    the actual scalp contribute. The instrument requires world-space POLY data.
    """
    for obj in objects:
        if obj.type!='CURVE' or obj.modifiers or obj.data.dimensions!='3D':
            raise ValueError('Temple coverage requires unmodified 3D filament curves.')
        if any(abs(obj.matrix_world[i][j]-(i==j))>1e-8 for i in range(4) for j in range(4)):
            raise ValueError('Temple coverage requires identity world transforms.')
        if any(s.type!='POLY' for s in obj.data.splines):
            raise ValueError('Temple coverage requires actual POLY filament points.')
        for material in obj.data.materials:
            shaders=[n for n in material.node_tree.nodes if n.type=='BSDF_PRINCIPLED'] if material.use_nodes else []
            if len(shaders)!=1 or shaders[0].inputs['Alpha'].is_linked or shaders[0].inputs['Alpha'].default_value!=1:
                raise ValueError('Temple coverage requires opaque single-Principled filament materials.')
    result=temple_scanlines(objects,head)
    result['pass']=all(row['largest_gap_radians']<.02 for row in result['rows'])
    result['maximum_allowed_gap_radians']=.02
    return result

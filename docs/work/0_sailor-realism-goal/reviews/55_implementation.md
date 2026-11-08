# Review 55: implementation

## Target

Candidate-29 actual sharp final capture and unchanged terminal-region feasibility.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Pure recorded-geometry analysis; root owns native acceptance.

## Reports

Complete authored report, SHA-256 `9268d85226ed965e18c23c76084c0e8f0f0bb45df7cda069f25d899311100301`.

# Candidate29 terminal-corner diagnosis — 2026-11-08

Independent pure-data decision: the unchanged adaptive lower-shape guard correctly rejects a single 80.15578614112698-degree corner created by the terminal center-capture branch. The original terminal goal is valid; this failure does not justify projecting it, increasing the turn limit or skipping a strand. A shorter straight chord into the unchanged terminal ball is geometrically possible in the recorded local state, subject to native endpoint and retained postguard verification. No repair source or candidate30 full attempt is approved by this diagnosis. Reviewer launched no Blender/GPU process and changed no source.

## Exact evidence and stage

`candidate29-source/first-strand-failure.json` SHA256 is `19d47cad4393d40c3e65ca9ec690a5346bd271df824e408792b3a98bd380a07b`; `candidate29-source/result.json` SHA256 is `f3537078c7fea844b63fe85b5664f1264c8924ef42f64ef1bbe53bdac88d922b`. All 37 recorded source/input bindings independently rehash without mismatch. The core is `815ead7941b2951da64425f52d53fbd797d9d293bda274f99e290dd64a3c2fa3`, fullbuilder `0be6573f8b3dc7aec0d39c7b5bcc4931017792c298493f8085e8162f15350431`, manifest `7846aa52bd94a2d960119717455b9651346521d7578912e1a4959b3e35cb3778`, and accepted27 input blend `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`.

Failure is left strand6524 after exactly 6,524 completed paths, sample0.5710982437740446, fraction0.5907848179340363, parameter0.28520891707905527, layer0.002176466227383065 m and swirl−0.08611744645962098. The root is `[-0.03733697533607483,-0.03508177772164345,1.6391156911849976]`. Root reports this as an integrated failure; the receipt's elapsed time is 140.0653553 seconds. Input, production source and bound source immutability flags are true. There is no saved-scene receipt or provisional blend.

Unlike candidate28's march exhaustion, this march returns completed terminal arrival, emits the actual POLY path/radii, and fails `adaptive_shape(stored, lower.high)` before the final emitted whole-path physical, lower guide/shaft and brow checks execute for this strand. The head postguard and root attachment call precede this failure in the unchanged builder. Construction certificates do not imply that the unexecuted final checks passed.

## Actual float32 witness

I independently recomputed all 202 interior turns and all 203 segment lengths. There are 204 recorded points, all exactly representable as stored float32; 204 actual radii and 203 certificates are present. Actual radius range is 0.001728215620966768..0.043205390077134375 mm. Arclength is 0.2670683215972632 m, consistent with recorded 0.2670683215972631 m and below the 0.5 m budget; 203 steps are below 900. Release length is 0.060699650933870225 m. The only turn at or above 75 degrees is vertex202; every other turn is at most 8.835711411728152 degrees.

The offending three points are:

| Index | Stored world point, metres |
| --- | --- |
| 201 | `[-0.05818377807736397,-0.036438409239053726,1.3967623710632324]` |
| 202 | `[-0.05811774730682373,-0.03657644987106323,1.3966398239135742]` |
| 203 | `[-0.056236591190099716,-0.03621404618024826,1.3967207670211792]` |

The incoming segment is 0.19604357330213972 mm; the outgoing segment is 1.9174557510600442 mm. Their angle is **80.15578614112698 degrees**. The outgoing certificate explicitly names `certified_terminal_chord_capture` and fresh goal proof. Its complete-body clearance bound is 5.004344597412551 mm against a 5 mm requirement, only 4.344597412551 micrometres of excess. Its construction reserve is 85.86439292474585 mm. The branch certifies physical clearance, construction clearance and remaining travel, then appends the center without an incoming-tangent predicate. The final shape instrument detects that omitted acceptance condition.

The selected center is the original tip rounded to float32, with physical hard reserve0.2540549370765692 mm and terminal radius0.2537549370765692 mm; both ear reserves are large and `all_hard_goal_pass=True`. Scalp goal is also unchanged. The ordinary released-step 0.1-distance cap remains effective before capture. The special final chord is intentionally outside that ordinary-step rule and was already governed by its own physical/travel proof; this failure is its missing turn condition, not an ordinary integration-step overrun or float32 duplicate.

The near-goal sequence explains why this capture fails at the first physically certified opportunity:

| Start vertex | Center distance, mm | Incoming-to-center angle | Conservative body bound, mm |
| --- | ---: | ---: | ---: |
| 198 | 2.102445125 | 65.275162179° | 4.917706147 |
| 199 | 2.059911477 | 67.467825111° | 4.941959330 |
| 200 | 1.988526739 | 72.480027421° | 4.978893980 |
| 201 | 1.960511783 | 75.024061652° | 4.991447118 |
| 202 | 1.917455751 | 80.155786141° | 5.004344597 |

At points200/201 the center is within 2 mm but the conservative chord proof still falls below 5 mm. At point202 that proof first passes while the tangent corner exceeds75 degrees. Merely clipping along the same center ray does not substantially change its direction and cannot by itself cure this corner.

## Bounded geometric counterevidence

The unchanged terminal ball subtends a 7.604798087528132-degree ray half-angle at point202. Its center direction is 80.15578614112698 degrees from the incoming tangent. Therefore it contains candidate rays below75 degrees; center-capture failure does not prove terminal-region infeasibility or require a curved connector.

For a concrete diagnostic witness only, I rotated the incoming unit direction 74 degrees toward the goal direction in their common plane, intersected that ray with the unchanged sphere, chose the midpoint between near entry and closest approach, and rounded the endpoint to float32. The result is `[-0.05629703402519226,-0.036379024386405945,1.3965905904769897]`. Recomputed stored properties are:

| Property | Value |
| --- | ---: |
| Turn from actual incoming segment | 73.99907736981969° |
| Actual chord length | 1.8320473812593707 mm |
| Distance to unchanged terminal center | 0.21867116288651453 mm |
| Unchanged terminal radius | 0.2537549370765692 mm |
| Conservative body bound from recorded fresh start | 5.089752967213224 mm |
| Conservative ear construction reserve from same start | 85.94980129454652 mm |
| Total arclength with this one replacement chord | 0.2669829132274624 m |

This uses the existing conservative 0.08 mm construction radius and recorded fresh-start physical query, not a reduced actual shaft radius. It supplies a pure-data existence witness for a potentially admissible terminal chord. It is **not** an accepted repaired path: this reviewer has not freshly queried its native endpoint, rerun complete physical/guide/shaft/brow/head checks, recalculated emitted arclength radii or run the root diagnostic. The 74-degree choice is a diagnostic witness, not a proposed production parameter or a request to tune the limit. A general repair must select and prove candidates under the unchanged75-degree condition after float32 storage and must fail closed when none works.

Root and author received the exact witness and the distinction between local feasibility and native acceptance. Retain this candidate29 failure unchanged. One integrated attempt remains under root's accounting; concrete frozen source review and the prior12 cases plus exact failed6524 bounded native validation are required before considering candidate30. No clearance, length, angle, valid-goal-preservation or complete-population waiver is supported by this evidence.


## Findings and disposition

Root agrees that the final center capture causes the only excessive turn. An analytic intersection between the permitted heading cone and the unchanged arrival sphere is a simpler proposed correction than adding another path segment. An arbitrary 74-degree angle is not adopted; the general feasible interval determines the arrival direction. Native thirteen-path and complete-population verification remain required.

## Verification

The exact failed specification, all stored points, radii, certificates and terminal plan remain under `outputs/character-round3-20261108/candidate29-source`. The quoted feasible chord is a diagnostic witness, not a saved or visually accepted groom.

## Round outcome

Nine integrated attempts used; one remains, number 30.

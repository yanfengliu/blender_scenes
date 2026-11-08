# Review 51: implementation

## Target

Actual candidate-28 failed strand, ear contact replay and bounded native terminal measurements.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native diagnostic execution and acceptance.

## Reports

Complete authored report, SHA-256 `f69dc090045cb2259484006b89aa1dddd7e527bb88cce2c421cc1b8e55a6335e`.

# Candidate28 failure: independent bounded causal diagnosis

Candidate28 failed at zero-based left strand 2391, after 2,391 complete strands. The failed construction exhausted 900 steps, producing 901 recorded float32 construction points and 0.452725502628 m of arclength; it did not reach the 0.5 m travel limit. The path failed inside `march`, before curve emission, radius sampling and brow verification for this strand. The empty actual-radii field therefore does not describe an emitted hair object or a brow collision. No scene was accepted by this diagnosis.

The primary causal evidence is active conflict between terminal approach and the ear construction contact rule, not the previous free-space integration orbit. Independent one-step replay using only the reconstructed left-ear contact, the requested float32 tip, recorded incoming heading and recorded physical allowance reproduces all 17 construction steps 110 through 126 (points 111 through 127) bit-for-bit, including every recorded heading-correction angle. Thus body/clothing contact steering is not needed to explain that initial near-goal turn-away. The authored 0.1-distance cap is active, but shrinking steps does not remove the competing directional constraint.

## Exact evidence and scope

- `candidate28-source/first-strand-failure.json`: SHA-256 `6ba1c5ed469ea3651b0b1db796e0ceb6bb60b7e3f1219277556b2d3f623673e3`.
- Growth core: `91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78`.
- Ear wrapper: `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2`.
- Support envelope: `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2`.
- Native construction inputs retained in `ear-hull-root-probe/hull-construction-result.json`: `0f8784badef18eb9d1f27c34352d165f28f9931187523a1b84b2dca828f2b9b4`.

Both halfspace fields were rebuilt in ordinary Python from their archived 7,849 native input coordinates. Input and plane-geometry hashes match the actual failed result: left input `8d677edd05dbed3530bef7103747113abcdfc031b0fb8c8de321533cf30a2f23`, geometry `656186fbb4e3bf2aa99d651f3851349cb41e2aef200936a8033998807af5f0fc`; right input `6cb421ed5160bf0748602a0206a435cdc89d460a27a3978721438864be4372a6`, geometry `5ce066e094f45e1abe16a688792fb165d79a32f8b9d6ac8e9e273952e881f042`. No Blender/GPU job or new growth attempt was launched; source remained unchanged. Only this diagnosis report was written. Findings were sent to root and the author independently of the author's own diagnosis.

## Recorded geometry

The failed sample is 0.20932803620952234, parameter -0.8142604491264853, left side. Its fringe-to-long blend is only 0.018369059294, but it is classified as long. Requested scalp and tip goals are about 3.715030705 mm apart, with a 6 mm scalp release sphere. The only recorded goal event is `scalp_release` on segment 89. Point 90 is 5.692258052 mm from the original scalp goal. These measurements identify a near-fringe transition-family case, not one of the earlier broadly separated terminal fixtures.

Requested float32 tip is (-0.06354701519012451, -0.11369895190000534, 1.5488559007644653). At that point the left support-envelope field is 1.170069649 mm. Its required construction centerline floor is 1.5 mm margin + 0.08 mm construction shaft radius + 0.0003 mm numerical reserve = 1.5803 mm. The requested center itself therefore fails that construction floor by 0.410230351 mm. This statement concerns the construction field only; it is not a measured Euclidean body-distance violation.

The original scalp goal has field 1.845142099 mm, below the wrapper's preparation threshold of 1.5 + 0.08 + layer 2.393145251 + reserve 0.0006 = 3.973745251 mm, so the source's preparation branch must consider a projected scalp target. Its exact selected point is not retained in this failure. Terminal selection uses the primary physical query and preserves physically valid original goals, while scalp preparation uses the ear construction envelope. That difference is a relevant endpoint/steering contract interaction; it must not be replaced by an unsupported assertion that every physical goal must move.

## Exact near-goal contact replay

At point 121, the requested goal distance is 1.924400805 mm and the left field is 3.084379046 mm. The unit goal direction has dot product -0.994756078 with the active ear-plane normal, while the contact cap allows only a dot product at least -0.001359682. The ear contact therefore removes nearly all motion toward the requested center and applies an 8.765644703-degree heading correction. The independent replay matches that correction and the next float32 point exactly.

Across points 110..126, independent ear-only corrections and next points match all 17 recorded steps exactly. The normal is the same active plane, index 369, with components approximately (-0.912982493, -0.399607052, 0.082323580). Tail fields approach 3.0803 mm: the 1.5803 mm hard construction floor plus the unchanged 1.5 mm steering anticipation buffer. The last 100 steps still have nonzero heading corrections, approximately 2.46..9.81 degrees. This is not a no-contact recurrence.

Ordinary step lengths in the tail are roughly 0.1 or 0.05 times current goal distance. The 0.1 cap is doing what it says; bounded float32 retries halve nominal cap-sized steps when the stored chord would slightly exceed the cap. More steps at the same contact contour cannot be assumed to resolve the incompatible approach. The strict 900-step failure is correctly retained.

The direct-center shortcut also correctly refuses the relevant move. At point 121 its conservative construction reserve is F(start) - distance_to_center - shaft_radius - numerical_reserve - margin = -0.420321759 mm. It cannot certify a chord to a center already below the hard construction floor. Removing that check would replace a recorded failure with an unsupported success and is not justified.

## Missing terminal-region measurement

The recorded path's closest vertex to the requested float32 tip is point 121 at 1.924400805 mm. The closest point on the entire recorded polyline is inside segment 120 at t=0.654579101512, distance 1.924113836 mm. It therefore enters a 2 mm sphere around the requested tip, but no terminal event is recorded. The selected terminal radius is NOT present in the failure receipt: `terminal_plan`, `completion` and `grown_length_m` are null because `march` raised before returning its result, and its failure helper attaches only points/certificates/call count. The selected sphere must not be assumed to have the maximum 2 mm radius.

At the observed steering contour, the requested center's active-plane offset is about 1.910230351 mm inward. This makes the actual selected sphere radius and the possible certified first-entry point decisive. A safe terminal region could intersect the hard-feasible exterior while its center is uncertifiable; alternatively the region could be incompatible with the current constraints. The present record does not establish either global conclusion. The independent replay strongly supports the requested center as the steering target in the inspected interval, but a native terminal-plan measurement is still required to bind its exact selected point/radius and physical reserve.

The author informed this reviewer that root requested a bounded native query of the terminal plan, original goal, points 110..126 and straight center-versus-sphere-entry proofs. That is the appropriate next evidence before repair: fresh body/clothing distances, exact unchanged terminal radius, complete construction fields and a proof for any proposed arrival segment. No repair implementation or new full attempt was approved by this diagnosis.

## Disposition

The observed cap/halfspace interaction is causally established for the near-goal turn-away by exact replay. The failed sample exposes a mismatch between a physically selected terminal region, ear-envelope steering clearance and center-only direct capture; the precise terminal-region feasibility remains pending its omitted measurements. Preserve the failed source/receipt and make future failure diagnostics retain selected terminal/scalp plans so the same uncertainty does not recur.

Do not relax the 900-step count, 0.5 m travel limit, 75-degree shape ceiling, physical margins, root limits or any postguard to consume this failure. Do not equate surface-clearance certificates for construction prefixes with a completed emitted groom. Two integrated attempts remain under root's accounting, and any next full build must follow bounded measured evidence and independent review of a concrete repair. This report is diagnostic only.

## Native terminal-region measurements, 2026-11-08

This appendix resolves the omitted-plan uncertainty above without changing or discarding the original failure evidence. I independently read the frozen probe and actual receipt, recomputed the closest point on all 900 recorded segments, and rehashed all 35 source/input bindings with zero mismatches. The probe performs native measurements only: no path growth, scene save or rendering. Root reports its owned PID 54712 exited zero and was closed after 12.3966 seconds; the receipt's internal measurement duration is 9.7108657 seconds. This reviewer launched no Blender process.

The probe `terminal-region-root-probe/probe_terminal_region.py` has SHA256 `c0efdad2e101cf4662328a0c33cf29a6ea47fd8268faef7fbbee3f003847349d`; `terminal-region-root-probe/terminal-region-result.json` has SHA256 `91f778a1f395df1da8ba787f211358e134ca0a53b76aeda6f9a3829cdf3db63c`. The receipt binds the failed candidate28 source manifest `f819a02033b0110f1fd8ac60bc5a9cf9b3d20534bceb47a5fc6a0e347d594775`, core `91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78`, original failure `6ba1c5ed469ea3651b0b1db796e0ceb6bb60b7e3f1219277556b2d3f623673e3`, and accepted candidate27 input blend `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`. Its status is `actual_terminal_region_diagnosis`, with `input_unchanged`, `source_unchanged` and the object-name inventory check all true. The inventory flag alone is not a scene-geometry fingerprint.

The selected terminal point is exactly the original requested goal rounded to float32: `[-0.06354701519012451, -0.11369895190000534, 1.5488559007644653]`. Its nearest physical support is body at 1.984282862395048 mm; clothing is 173.168182373047 mm away. The original planner labels the goal physically valid and selects radius **1.8936828623950482 mm**, exactly `physical_distance - 0.010 mm body margin - 0.080 mm shaft radius - 0.0006 mm numerical reserves`. That radius was not 2 mm. The independent full-polyline minimum remains segment120, t=0.6545791015118751, at 1.924113836412135 mm; the actual recorded path therefore misses the selected ball by **0.03043097401708673 mm**. There was no missed continuous event for this selected sphere.

At that same float32 center, the left ear construction field is 1.1700696485674451 mm and its retained hard reserve is **−0.4102303514325549 mm**; its working steering reserve is −1.9102303514325549 mm. The original goal was admitted using physical clearance without checking the construction reserve. This directly confirms the inconsistent goal eligibility. These numbers remain supporting-plane lower-bound construction measurements; they are not a body-intersection finding or an exact Euclidean ear distance. The native scalp plan separately projects its obstructed goal by 2.2822278508127327 mm, to `[-0.0654941126704216, -0.11541727930307388, 1.5525509119033813]`. Root attachment is 0.11940262629650533 mm, within the unchanged 0.3 mm bound.

The 23 inspected checkpoints are 0, 89, 90, 100, 110 through 126, 850 and 900. Every center chord fails the complete physical-plus-ear proof. Sphere-entry chord measurements give the following counterevidence against treating center replacement with first sphere entry as an already validated repair:

| Checkpoints | Measured first-entry chord result | Retained disqualifier |
| --- | --- | --- |
| 0, 89, 90, 100 | Fail physical/ear chord proof | Unsafe chord |
| 110–117 | Pass physical/ear chord proof, travel and strict ball entry; turns 56.08655429–74.02219621 degrees | Current point is outside unchanged 2 mm capture range; point117 is 2.002096078 mm away |
| 118–125 | Pass physical/ear chord proof, travel and strict ball entry; current point is within 2 mm | Turns 76.78970779–102.16798678 degrees exceed retained 75-degree guard |
| 126, 850, 900 | Pass physical/ear chord proof, travel and strict ball entry | Outside 2 mm capture range and turns above 75 degrees |

There are **zero eligible witnesses among these 23 sampled checkpoints**, and consequently no completed prefix was sent through the probe's conditional whole-prefix shape, physical, old-head and brow checks. A physically and construction-safe sphere-entry chord by itself is not a completed compliant prefix. The probe does not enumerate every possible chord or establish global infeasibility; it must not be represented as proving that no admissible terminal route exists.

Updated disposition: the native evidence confirms a terminal-planning defect, while the existing 0.1-distance step cap and failure guards behaved as designed. The physically valid but construction-invalid center is an unsuitable preserved goal for this construction system. Review a concrete repair that derives terminal eligibility and conservative ball radius from every applicable physical and construction reserve, uses the existing invalid-goal projection only when eligibility fails, and preserves already valid goals. Keep the 900-step, 0.5 m, 75-degree, capture, root, clearance and final postguard limits unchanged. Frozen source review and actual bounded reruns of the prior 11 cases plus this exact failed specification remain prerequisites for considering another full attempt. This measurement pass is not a repaired-path result, full-groom pass or aesthetic acceptance.


## Findings and disposition

Root confirms the endpoint planner accepted a physically valid center that violated mandatory ear-construction clearance. The actual path missed its selected terminal sphere by about 0.030431 mm; no eligible capture was demonstrated among the sampled checkpoints. This is an endpoint-validity defect, not permission to increase path budgets or waive clearance. The proposed repair includes every mandatory support in goal eligibility and terminal-radius calculation; bounded old-case and failed-case verification must precede another full attempt.

## Verification

Root-owned native PID 54712 exited 0 and closed after 12.3966 seconds. All 23 checkpoints, exact terminal plan and source/input bindings are retained under `outputs/character-round3-20261108/terminal-region-root-probe`.

## Round outcome

Eight integrated attempts used, two remain, next 29. No new integrated trial was consumed by this read-only diagnostic.

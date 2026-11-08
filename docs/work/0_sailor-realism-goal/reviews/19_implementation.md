# Review 19: implementation

## Target

Evidence-only shared-field hair instrument based on 49da8f215db2a0d501b23f8d44b5891daacc3c8a. Initial and repaired source bytes, controls, failure receipts and diagnosis are retained in outputs/character-round2-20261107/hair-attempt17-evidence; archive-manifest.json SHA256 567bb41fd359d7634c812516c2edee10b49f172836aa5aa5d8e0d865dcc51f10 binds all 94 files. Exact target hashes are in the authored report. No production source was changed.

## Reviewers and coverage

Astra xhigh independently inspected source, repair diffs and hashes. Root owned execution and accepted or rejected its actual result. No reviewer-run Blender or native appearance review is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows; its original SHA256 is b26fde4c500e1849c6eb188c12101068462ad4b38ae22a912a0ff20e79887656.

# Shared-field instrument: independent source preflight

Reviewer: Independent Codex reviewer, Astra xhigh.

Scope: Evidence-only hair instrument before its one full-groom run. Base `49da8f2` in `outputs/.worktrees/character-naturalness-round2`, with production scene/runtime source unchanged. This is a source-readiness review, not a Blender execution, full-groom acceptance or native visual judgment. No source, plan or Blender process was modified or launched by the reviewer.

## Initial exact target

Paths are relative to the worktree's `outputs/round2-hair-search/`. These four hashes were independently recomputed before review.

| File | SHA-256 |
|---|---|
| `shared_field.py` | `ed40fce850ef8deeafd8526dff416623fc7135edebd7f3bab506c6ae006faecd` |
| `shared-field/groom-source.py` | `d86665075b80352d5ff1ce659a1abbb4143d151aa8dbf4861861b8bdf3e0d78f` |
| `probe_shared_field.py` | `971cbf9d8440043d1897c4153d8bf1013692b18539c4d8f57e526a173eabeafc` |
| `run_shared_field.py` | `2a48eafd7f066bde53dfe5b4d4ff4637e8be06f323e618a4234aac1fa49b7256` |

The instrument reuses the reviewed `global_route_core.py` (`a986d8d147ebaecc7ca2599e7c942becbeb7c0d2eaaf4308874fa697aa5fcc8a`), `complete_lower.py` (`0af6595c670e5140ab3505c1443a9e36d3e2f8e2a7696c3854f9d0c9831aa1d6`) and preserved upper source (`eb937b5fcc01c3cbec5a4dd924548896e5037bbabeeb99462219b045ef792a9f`). I read the full new solver, probe and runner and compared the full groom delta to the preserved upper source. The canonical-body reconstruction and strand-radius/field interpolation dependencies were inspected where needed. There is no independent runtime result in this preflight.

## Initial disposition

Do not launch this exact initial source as the final one-run instrument yet. The continuous distance method and complete support construction are sound in principle, but the surrounding success contract has the actionable gaps below. Root accepted the three initial coverage findings and required repairs before execution; root independently identified the missing launcher timeout. Initial source must remain recoverable when repaired source is substituted.

1. **SF1: support equivalence is informational, not enforced.** `probe_shared_field.py:44-48` records body/clothing hash equality between candidate 11 and candidate 10, then proceeds regardless of either result. This cannot substantiate the claim that support equivalence was checked as a prerequisite. Assert both equalities before building the groom, or explicitly abandon the equivalence claim and obtain a disposition on the changed support. Because the new distance checks use candidate 10's own geometry, the omission does not itself prove a candidate 10 collision; it is a fail-closed provenance/transfer defect.

2. **SF2: the initial 1.5 mm child assertion is a centerline margin.** `shared_field.py:241-271` only receives point coordinates, and `probe_shared_field.py:63-65` discards the actual stored spline radii. A 1.5 mm centerline clearance can leave approximately 1.42 mm at the shaft surface for an 0.08 mm strand radius. Root requires actual strand-surface clearance, so pass conservative radius bounds during construction and use the stored bevel depth, point radii and object transform for the actual-curve check. The distance lower bound must subtract a valid maximum radius over each tested subsegment; point-radius sampling alone is not a continuous surface-margin certificate. Guide margin remains a separate 5 mm guide-centerline requirement.

3. **SF3: child smoothness omits potentially changed entry joints.** `truncate()` sets `first=max(starts[0],46)` at `shared_field.py:228`, then asks `path_metrics` to enforce the turn limit only from that index onward. Moving child interpolation can enter the changed lower guide field before point 46. The field-entry joint or a changed joint before truncation can therefore escape the intended turn check. Check turns and collapsed segments over the actual modified lower region, including its entering joint, and repeat that check on the actual stored float32 curves. A distance pass does not rule out a kink.

4. **SF4: the launcher has no wall deadline.** `run_shared_field.py:14-15` polls indefinitely. Its `finally` Job cleanup is appropriate once the loop exits, but a stalled process never reaches it. Root requires a 900-second wall deadline, an explicit timeout receipt and the same finally cleanup of the owned process tree. This is a resource-bound repair, not a change to the geometric acceptance thresholds.

5. **SF5: immutability flags do not affect success.** `probe_shared_field.py:101-103` only records whether candidate 10, candidate 11 and production hair bytes remained unchanged. They can be false while `status` remains `geometry_pass_pending_appearance` and the process exits zero. Failed final immutability checks must change the outcome and fail the run after its diagnostic receipt is preserved. Source hashes should also describe the exact executed/reviewed files rather than silently transferring acceptance to edits made during the attempt.

Small real controls are warranted before spending the full run: reject a historical failed lower path through the new verifier, exercise radius-dependent clearance where the centerline alone would pass, and reject an entry kink before point 46. These controls should target the actual new verifier and smoothness code, not a duplicate implementation. They do not require a second full groom.

## Mechanism and remaining limits

The earlier clothing-support boundary limitation is addressed in this source. `LowerField.__init__` retains every evaluated clothing face without an overall-band prefilter. It records original modifier enable/subdivision settings, evaluates render-enabled modifiers at render subdivision levels, and restores the temporary changes in `finally`. The complete canonical body is separately reconstructed at subdivision level two. The same full body/clothing BVHs feed both the actual-segment checks and support constraints. This is a meaningful source correction to the conditional padded-domain claim in review 18; runtime support hashes/counts still need to be inspected after execution.

The neighboring guide cell uses one support normal and a common 6 mm construction half-plane for both guide edges. Variable cubic sections are split at knot boundaries before Bezier control constraints are generated; fixed prefix corners must meet the same cell plane. The emitted guide corners are then checked explicitly, so the actual bilinear guide cell stays in that shared half-plane by convexity. This avoids inferring a shared safe corridor from two unrelated safe guides. The preferred transverse field transports adjacent displacements, but spacing is still an objective rather than a hard minimum-spacing proof. It must not be described as demonstrated physical separation or natural density without post-fit evidence and pixels.

The adaptive distance certificate is mathematically appropriate for a fixed evaluated triangle surface. Euclidean distance to a set is 1-Lipschitz, so midpoint distance minus half the subsegment length is a lower bound for every point on that subsegment. `verify()` accepts only a lower bound above the required margin plus a numerical cushion; otherwise it subdivides or fails at its depth limit. It also checks exact segment rays, rejects inside-body midpoint samples, and fails on empty nearest queries. Clipping includes entering and exiting boundary segments. This is substantially stronger than fixed endpoint/midpoint distance samples. SF2 concerns the omitted strand radius, not the validity of that centerline lower bound.

The source preserves the requested population of 11,425 strands per side plus 150 loose strands, with 64 stored points per strand, and checks those actual counts after construction. It reapplies the independent fringe, crown, temple and face/ear guards and root/lift limits. The final loop reads stored Blender coordinates, which addresses float32 conversion before distance checking. Those are useful fail-closed design choices. Full population success, independent lower-check success, stable transverse spacing and native visual improvement remain unexecuted claims.

The new endpoint treatment truncates along the lower polyline instead of displacing tips downward outside a certified height cell. It retains the original random draws and upper points, but maps them to a different lower length/cut distribution. That is within the explicit length freedom accepted in review 18 and must remain disclosed in the outcome. Reconnecting resampled truncation points can cut across original polyline corners; the final actual-segment distance verifier is therefore necessary even if the original path passed.

## Verification and next decision

Performed by reviewer: full static inspection of the new instrument, source hash computation, groom-delta inspection and targeted dependency reads. Not performed: Blender launch, full-guide optimization, complete child generation, runtime negative controls, saved-scene verification, rendering or native image review. The worker's earlier syntax/basis/QP smoke report is not a substitute for the pending full run and was not independently executed here.

Source readiness is withheld for the initial hashes above pending the accepted repairs. A subsequent section will bind and assess repaired bytes if supplied. The one full-groom attempt must still be treated as evidence whose outcome can fail; no geometry or appearance pass is pre-authorized by this review.

## Repaired-source preflight: ready for the bounded attempt

The author preserved all four initial files byte-for-byte in `shared-field/readiness-v1/`; I recomputed their hashes and matched the initial target above. I then inspected the complete repair diffs and independently recomputed the new hashes:

| Repaired file | SHA-256 |
|---|---|
| `shared_field.py` | `0990c0a221b7bdc82ba2b150dcabd76fb478affc49efecf1ee12d067a63900c7` |
| `probe_shared_field.py` | `5abd6e7b8c7899027843b49e645d89450eb2dcd53e8f08b45b78dc088b80c318` |
| `run_shared_field.py` | `5b19413a8af68405913f7da832e3e0a4f56ea2df34e45c5b5a141587a5cf65f1` |
| Unchanged `shared-field/groom-source.py` | `d86665075b80352d5ff1ce659a1abbb4143d151aa8dbf4861861b8bdf3e0d78f` |

SF1 is repaired in source: either support hash mismatch now raises before the new groom is constructed. SF5 is also repaired: the final input, candidate-11, production and listed evidence-source hashes are compared, any mismatch forces failed status, and the process raises after writing its diagnostic receipt when no earlier exception already provides failure. This certifies the listed immutable inputs; it is not a claim that every external Python dependency is independently hashed by this probe.

SF2 is repaired for the actual generated curves. Construction uses the worst supported 0.080 mm shaft radius. The actual-curve loop extracts bevel depth and stored point radii, with the current generated objects' transform scale; those objects are created unparented with identity transforms. Each segment uses the maximum of its endpoint radii, a conservative bound for the linearly varying POLY shaft including a clipped subsegment. The nearest-distance threshold adds this radius, and the Lipschitz lower bound subtracts it. Thus the asserted child quantity is now at least 1.5 mm of physical surface clearance rather than a mislabeled centerline distance. A future generalization to sheared transforms would need an operator-norm radius bound or an explicit transform restriction; no shear is introduced by this reviewed groom.

SF3 is repaired in source: `check_child_shape` finds the first segment entering the lower region, checks its segment lengths and subsequent lengths, and measures turns starting at the entering joint rather than truncation index 46. It is called by the common verifier both during construction and for the final stored float32 curves. The author reports a lightweight read-only check accepting the measured smooth child and rejecting the new entry kink at point 45; I did not rerun that smoke check. The actual stored-POLY control remains in the pending Blender attempt.

SF4 is repaired in source: the owned runner records a 900-second deadline, detects an overrun while waiting, sets timeout metadata and raises through the same `finally` process/Job cleanup. No timeout or cleanup execution is claimed by this static review.

The three new controls are appropriately causal. They round-trip through real temporary Blender POLY storage and remove their objects and curve datablocks in `finally`. The historical path must be rejected by complete-support crossing/clearance/inside checks. A real clear segment first passes with zero radius, then receives an enlarged stored radius and must fail specifically on physical clearance. The synthetic entry kink must lie before point 46 and fail specifically on the turn check. Expected errors are checked rather than swallowing arbitrary exceptions. Metrics are restored after successful controls so their deliberate failures do not contaminate the population's reported extrema. Their runtime results remain pending.

No blocking source defect remains for this one evidence-only attempt. This is readiness to execute these exact repaired bytes, not F21 closure, a successful full field, acceptable guide spacing, or appearance acceptance. Inspect the actual control results, support equivalence, complete emitted-child margins, counts, independent guards, immutable hashes and owned-process completion before attributing runtime success. The shared-corridor constraints remain conservative: a cell can contain fixed short-guide corners above the band, so a fixed-prefix infeasibility would reject this certificate without proving that no natural route exists. No relaxation or alternative attempt is pre-approved here.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F22 | SF1: support equivalence was only recorded. | Accepted and repaired before execution. | Both complete geometry hashes are asserted. |
| F23 | SF2: child margin omitted shaft radius. | Accepted and repaired before execution. | Stored endpoint radii bound physical shaft clearance. |
| F24 | SF3: early changed entry joints escaped smoothness checks. | Accepted and repaired before execution. | Actual lower entry and float32 curves are checked. |
| F25 | SF4: owned runner lacked a deadline. | Accepted and repaired before execution. | 900-second deadline and finally cleanup. |
| F26 | SF5: immutability flags did not invalidate success. | Accepted and repaired before execution. | Hash mismatch forces failure. |
| F21 | Actual complete guide/child margins remain unproved. | Open: no children were generated. | Next source proposal must retain 5 mm guide and 1.5 mm physical child clearance. |
| F12 | Hair naturalness remains unresolved. | Open: this attempt never reached renderable full geometry. | A passing complete groom still requires native appearance review. |

## Verification

The reviewed attempt 17 ran once under owned PID 18636, exited 1 after 20.00 seconds and closed. Complete candidate-10/11 body and clothing hashes matched. All three stored-POLY negative controls rejected as expected. Construction then failed at fixed cell left guides 26/27, positions 97-98, before guide solving or child generation. A separate owned read-only diagnosis found a continuous 8.585844 mm body clearance bound for that clipped fixed cell; its best projected plane yields 5.877665 mm. This diagnoses an overconservative construction certificate, not a failure of the actual required 5 mm physical guide margin. No retry or appearance acceptance occurred in this round.

## Round outcome

The repaired instrument was ready for one bounded execution; its actual outcome was construction failure. The five instrument findings were repaired and checked, but neither F21 nor F12 is closed. A future attempt requires a new exact-source review and consumes the remaining integrated-attempt budget.

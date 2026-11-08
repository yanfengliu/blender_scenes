# Review 23: implementation

## Target

Read-only causal attribution of the rejected attempt 18, based on 882e4f4d609669add52785cb39b424644d8f4deb. Exact scripts, matrices, receipts and authored note are retained in outputs/character-round2-20261107/hair-attempt18-diagnosis, archive-manifest.json SHA256 6fcb08733da546a705d57ce9b31d5596c623aaeac64dd529a975afb7bd61a15f. Executed attempt 18 remains separately immutable. No production change or new repair candidate is part of this review.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 5bd376b30b78f770cb2295e94cb34a0ce8afea9ebae355af4b2faadfc6782e62.

# Independent review: attempt 18 equality attribution

Reviewer: Independent Codex reviewer, Astra xhigh. This is a read-only causal review of the failed guide-27 solve, not another groom attempt or approval of a new solver. No Blender application, GPU process, render or source modification was performed.

## Exact target and independent checks

Reviewed `equality_attribution.py`, SHA-256 `a10779714c82285c564eaff4b28cc3b826d4375c70f6fe19f0704569afe7935a`; `attribution.json`, SHA-256 `b4534f19bba33860d93d86cf7ed41026b810d45d9a7d1dbde461e0b460c3e162`; and `equality-only-path.json`, SHA-256 `a69c34fe0c5e38b1bb01821dc3948ba0a2a91613f5e78d6a8cdf0e803d1f6dc7`, all in `outputs/round2-hair-search/attempt18-diagnosis/` in the isolated worktree.

The attribution binds attempt-18 `shared_field.py` (`1a46fb86694f392070ba6cf55f7e45b1c2df5b35b2f281c531e6b1cb1a8736b2`), `global_route_core.py` (`a986d8d147ebaecc7ca2599e7c942becbeb7c0d2eaaf4308874fa697aa5fcc8a`), failed `result.json` (`a151d9198f65263f8e9f87c00f9e550c5a718f3815c12eeb282c9cb923de3858`) and actual `original-guides.json` (`29e050ba6d410d3cfb5cb284a3ffcf381db916950082869cf28c4e9202dbff18`). I compared the algebra with the reviewed production path through the attempt-18 objective and equality construction.

I reran the attribution offline using bundled Python with NumPy, compiling the source after omitting its final two file writes and print. The independently recomputed report equals the retained JSON exactly. I additionally solved the full equality-constrained KKT system, independently of the script's null-space solution: its controls agree within `1.911e-14` m, and the equality residual is `4.562e-15`. This was a short Python calculation, not a Blender application run, and did not overwrite the worker's evidence.

## Causal conclusion

The bound is sound for the exact current objective, join conditions and norm-preserving preferred-field construction. With the original target and the identical fixed position/tangent/second-derivative conditions, the equality-only path adds only 0.340141 mm of length, has a 0.971342-degree join turn and reaches 59.014478 mm maximum lower absolute X. The large excursion is therefore not an inevitable consequence of preserving this incoming two-jet under the existing smoothness objective.

The transported-target bound also correctly covers the actual unknown preferred target. For the active group 27 through 95, integrating rotated neighboring differences and recentering their mean expresses each target as the original group mean plus a weighted sum of rotated differences. Each rotation preserves its difference's norm. Applying the triangle inequality to `R(delta)-delta` gives the stated `sum(2*abs(coefficient)*norm(delta))` displacement bound. Linear interpolation preserves the interpolated bound. The equality-constrained optimizer is affine in its target, so absolute response weights validly propagate those target bounds to each emitted tail station.

Even across every rotation admitted by that construction, the largest sampled curve deviation from the original-target equality solution is at most 7.786437 mm. The tighter stationwise bound gives a minimum possible equality-only lower X of -62.585135 mm. The observed constrained solution reaches -437.578091 mm. At that observed station, adding the inequality stage therefore changes X by at least 374.992956 mm relative to the equality-only optimizer with the same actual preferred target. This is a causal lower bound on the inequality stage's contribution to the extreme point; it is not a claim that exactly that amount of arc length or turn angle has been independently decomposed.

These are float64 numerical calculations of an analytic sufficient bound, not interval-arithmetic certification. The independently checked linear solve residuals are negligible relative to the approximately 375 mm separation. The result applies to the pinned group, objective, source coordinates and norm-preserving field. It should not be extended automatically to a future mechanism that changes those assumptions.

## What this supports next

The evidence supports inspecting the hard constraint mechanism rather than sweeping preferred-field rotations, curvature weights or join parameters. It does not yet prove that the proportional residual allocation itself is defective, that the projected support is the culprit, or that the QP implementation solved the intended row correctly. The failed receipt did not retain the actual target, successful control coefficients or active inequality provenance before the later shape rejection.

The authorized one-time exact QP capture is the appropriate next discriminator. Reconstruct the active row's original joint clipped-cell or span inequality, its fixed contribution and actual free weights; compare the final solution with both that joint inequality and the allocated per-guide inequality. A severe individually allocated bound despite a feasible joint cell would support a distinct coupled-constraint mechanism. A faithfully active but overly conservative projected support would instead support changing the geometric representation. A row-construction or solve discrepancy would call for a bounded correctness repair. This review does not choose among those mechanisms before the captured evidence exists.

No parameter loop, attempt-19 implementation or additional groom run is approved here. Attempt 18 remains rejected; its physical margins and shape rejection stay unchanged. The useful new conclusion is that the current equality conditions and allowed preferred-field rotations cannot account for the observed extreme, so the next investigation should be confined to the inequality stage and its provenance.

## Subsequent exact capture and bounded attempt-19 design judgment

I inspected the later authorized capture source and receipts, preserving the earlier stage-level conclusion above. Exact targets: `capture_first_qp.py` SHA-256 `1ce13f2c0ee4d1263045ff153114934973df44d7d96925fa6e9726f97779959d`; `first-qp.json` `4f1eef941ce5e04e773153facb6475f2e3722e543af7871a5b04bc4221bb40ec`; `capture-result.json` `2331fcf3f105a6f8ae25740ac6ca7a200df32c4cb96a279e0da3c39c5b88e4df`; `capture-process.json` `c9aa52aacc157139d53c6da0f25fda6d329d0d388c1737aa4e9f7df88b534746`. I independently recomputed those hashes. The capture intercepts the existing first solve, calls the original solver with its actual arguments and reconstructs every row's classification back to the captured `G/h`, asserting correspondence before stopping without children or saving.

The decisive row is row 7: mixed cell guides 26/27, samples 99-100, clipped vertex weights `[0,0,1,0]`. Its own free weight and total free weight are both one, with zero fixed contribution. It is therefore a direct constraint on guide 27's first free sample, not proportional-allocation amplification and not a Bezier-control inequality. The fallback radial plane has support `0.11643337361423642` m and requires `0.12143437361423642` m. The equality-only actual-target solution falls short by 6.185263 mm at a point immediately after the fixed join. The support witness lies at Z=1.480268 m, while the controlled point is at Z=1.469035 m. This is a conservative projected-support demand, not a measured collision at that point.

The capture's single-active reconstruction matches its solved coefficients within `5.552e-17` m. I independently solved a KKT system containing the original equalities plus that one active row; its coefficients agree with the captured solution within `9.015e-13` m, with equality residual `1.499e-14` and maximum inequality violation `5.371e-15`. The captured support vertex's projection also reproduces the support exactly. This makes a solver-misattribution explanation implausible at the scale of the observed excursion and identifies the direct hard plane as the operative demand.

The same capture runs the unchanged complete-body/clothing guide verifier on the original guide 27 and reports a pass at a minimum certified clearance of 8.907881 mm against the 5 mm requirement. The run confirms unchanged bound input/source and closes its owned process with exit zero in 15.006 seconds. These are root/worker-run geometric measurements, not my own Blender execution. The capture checks the original guide; the proposed next source must additionally check its float32 form rather than claiming that coverage from this receipt.

Prescreening original guides and preserving those already certified safe is a justified distinct next mechanism. Attempt 18 chose a model from its height/drop criteria even for this safe guide, removing its fixed status and subjecting its near-join sample to the fallback radial plane. Keeping such a guide fixed avoids unnecessary optimization and gives subsequent clipped cells its actual fixed geometry for separator selection. This is supported by causal evidence and does not require changing the physical margins, objective or curvature weight.

The design approval is conditional and limited to preparing source. A passing prescreen must use the unchanged complete 5 mm verifier on both the original and float32 guide and preserve the original guide coordinates exactly. Failure to certify is not always proof of a physical collision: expected crossing/clearance/nonconvergence outcomes must be distinguished from malformed support, nonfinite inputs and programming errors, which should abort rather than be silently classified as fit candidates. Record each decision and its witness separately from final population metrics.

All clipped cells must still be certified; individually safe guides can interpolate through an unsafe region. No fixed-cell skip, child-count reduction or bypass of actual 23,000-strand/radius/upper checks is justified. A mixed-cell incompatibility after freezing a guide must remain a recorded failure, not cause an unreviewed release or threshold relaxation. The precise revised source and its prescreen controls need a fresh preflight before the next single run. This note approves neither attempt-19 execution nor full-groom geometry or appearance.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F32 | A conservative projected plane needlessly deforms an already-safe short guide. | Accepted: exact active-row/KKT evidence and actual original-guide clearance establish the mechanism. | Prepare preservation of guides that pass complete original and float32 checks; keep mixed cells and all actual children checked. |
| F21 | Complete actual guide/child proof remains open. | This diagnosis does not construct the full groom. | Fresh exact-source preflight before any attempt 19 run. |
| F12 | Hair appearance remains unresolved. | No new scene or render. | Native review remains necessary after any passing full groom. |

## Verification

Reviewer independently reproduced the entire offline attribution and checked an independent KKT solve. The exact read-only capture reproduces the failed controls and identifies direct row 7 with weight one, no fixed contribution and no residual-split amplification. Unchanged guide 27 passes the actual 5 mm segment certificate at 8.907881 mm minimum bound. The owned capture PID 39904 exited 0 and closed after 15.006 seconds; no hair replacement, children, save or render. All sources and input remain unchanged.

## Round outcome

Prescreen-and-preserve is supported for bounded source preparation. It is not a new geometry or visual pass and does not authorize a full run before fresh source review. No curvature, target-weight or margin sweep is supported.

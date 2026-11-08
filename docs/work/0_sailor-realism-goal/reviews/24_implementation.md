# Review 24: implementation

## Target

Attempt 19 prescreen-and-preserve implementation based on 0032b5963128707ad23044b18000efc4fdfe828c. Exact source and all actual outcome files remain in outputs/character-round2-20261107/hair-attempt19-evidence; archive-manifest.json SHA256 ffb08b6e612a74fd54dec41fc9b3f7eacbc10711f89165d6d1891245adef5e33. The nine-source target and renderer19 adaptation are bound in the authored report. No production changes.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 fc616df1f34f08d905db6408314e50dd033a929a866dd5d2c90c3932966c07ef.

# Attempt 19: independent source preflight

Reviewer: Independent Codex reviewer, Astra xhigh. Base `0032b5963128707ad23044b18000efc4fdfe828c`; production runtime remains dc67-equivalent. Scope is the narrow guide-prescreen dispatch, retained geometry/save contracts and the renderer's attempt-number adaptation. No Blender application, source edit or additional agent was used by this reviewer.

## Exact source

The target is `outputs/.worktrees/character-naturalness-round2/outputs/round2-hair-search/attempt19/`. I independently matched all nine files in `preflight-sha256.json`, SHA-256 `ba8252955b30c66a8977528271a630a885df45d10849db86303aadda506e04a0`, and parsed their syntax. The changed files are:

| File | SHA-256 |
|---|---|
| `shared_field.py` | `8875092f31e64e5eded50cf665457450a254251b947144113aa24a8ae32ce0ea` |
| `probe.py` | `ac85ca65bd89a02ba54f33dc08bed4e8d2cc490622c23a730d237ac7c6a5c946` |
| `run.py` | `7089aa709a9470dd24b90f0db10a05bc88ff8c283603da13e01ebc7c94a09990` |
| `prescreen_controls.py` | `ef1a42359358e6ae419598314e70c01a4b095c628b3ed6b06d1dba6a88d192a6` |

The groom, clipping/cell certificate, QP, lower checker and mathematical controls are byte-identical to the reviewed attempt-18 versions, bound by the same nine-file manifest. The new preflight description hashes to `97d9d8d3c8b00a292fde0b006187c77b09e364709a8f24f227363025032567b2`; the stored synthetic prescreen-control receipt is `7931b8cd950578d01d3c0c3b7f12fa6cf89f480ca8d49a2f2df20c322875622b`; the unchanged mathematical-control receipt is `7bded22faddfee4d4f0b9cd1ea3e52e973b7c6c76180250bd4af5aa5b92e9965`.

Primary `outputs/character-round2-20261107/render_candidate19.py` hashes to `b32d1f21ad0965a0ab2242379055db79e60324f8072a512f1ca7ed60a386de30`. Its complete diff from the reviewed final renderer 18 contains only the source directory, output directory and temporary-camera name changes. The common fingerprint helper and renderer gates are unchanged. No runtime result or provisional scene existed when the source inspection finished.

## Decision

Ready for one bounded attempt using these exact sources. No blocking defect was found in the narrow delta. This is source readiness, not a complete physical-clearance, saved-scene or appearance pass. Attempt 18's rejection remains intact, and no automatic retry or threshold relaxation is approved.

The change follows the captured cause rather than tuning parameters. The previous solve unnecessarily modeled an original guide that already satisfied the complete physical clearance requirement, then forced it against a conservative fallback plane. The new dispatch certifies original guides first and retains passing guides as fixed geometry. It does not change the objective, curvature weight, 5.001 mm construction target, 6 mm vertical padding or actual 5 mm/1.5 mm physical requirements.

## Prescreen and error handling

All 192 source guides are prescreened before model construction. Each must have finite 110-by-3 coordinates. The same complete-body/clothing verifier runs once on original float64 coordinates and once on the float32 roundtrip. Both representations are checked even after an expected failure in the first phase. A guide is preserved only if both pass; otherwise only the explicitly typed physical failure or distance noncertification can make it a fitting candidate.

`PhysicalClearanceFailure` covers an actual ray crossing, signed inside-body result or measured distance violation. `DistanceNoncertification` separately identifies exhaustion of the unchanged depth-14 proof. The latter is correctly distinguished from a demonstrated collision. Invalid coordinates, malformed/nonfinite or empty support queries, collapsed lower segments and unexpected exceptions remain ordinary errors and propagate out of the attempt. A guide requiring repair with no permitted tail/drop now fails explicitly instead of becoming an unverified fixed guide. This is fail-closed dispatch rather than a broad exception catch that silently fixes failed guides.

Each phase uses fresh scratch metrics and restores both the original metric object and `last_checked_path` in `finally`. Its own counters, bounds and any failure witness remain in the phase ledger. Thus expected prescreen failures do not contaminate the final successful population's counters or extrema. Partial ledgers are retained on an instrument failure. Empty lower domains are labeled explicitly; a pass over such a domain is not presented as a finite measured clearance there.

Certified guides become the existing `model=None` fixed expressions. Their output bytes and canonical coordinate hashes must match the original, and both original/float32 verification run again in the final guide loop. The `preserved_exact` result is set after those checks, not merely inferred from the prescreen decision. Preserving guides changes which remaining active guides form contiguous preferred-field groups, as the preflight acknowledges; the transport formula and its weights are unchanged.

No cell is skipped because a guide passed its own test. All original mixed/fixed clipped-cell certificates, fixed-ball exterior check, final clipped-vertex replay and knot-split span replay remain. Individual guide clearance still cannot establish interpolation clearance. A fixed-cell or mixed-cell incompatibility must remain a failure. The final actual child population, shaft radii, lower-entry shape checks, independent lower checker and upper/root guards are unchanged and mandatory.

## Controls, save and renderer

The new controls exercise the actual prescreen/verifier methods with clearly labeled synthetic supports. They cover physical crossing/inside/distance outcomes, proof nonconvergence, each expected failure in either representation, explicit empty domains, metric/last-path restoration, malformed support and coordinates, collapsed paths and unexpected exceptions. The phase-dispatch tests confirm that both calls occur and that the second receives the actual float32 roundtrip. These tests are meaningful for the new dispatch class, but they are not evidence of clearance against the real candidate-10 anatomy. Root reports independently rerunning both control families without writing artifacts; I inspected their source and retained results but did not run their numerical tests in this review.

The probe runs these controls in the eventual owned process and retains all historical actual stored-curve controls. It still requires candidate-10/candidate-11 complete evaluated support equality, all 23,000 paths with 64 stored points, actual physical checks and source/input immutability. The only save-schema changes are candidate-19 names and additive prescreen reporting. The shared render fingerprint still occurs after actual stored verification and independent guards, immediately before the authorized provisional save, with its required helper/snapshot source bindings. Existing-output refusal, failed-save cleanup and `geometry_pass_pending_appearance` status remain unchanged.

The launcher changes only its purpose label; it retains the 900-second deadline, hidden owned process, WindowsJob cleanup and no retry. Renderer 19 retains the reviewed fresh-output guard, non-hair/benchmark comparisons, mandatory fingerprint dependency membership, reopened coordinate/radius/render-state equivalence and six fixed/held-out views. It cannot establish a successful saved candidate until the producer actually supplies a matching passed receipt and scene. There is no new renderer implementation behavior requiring a broader re-review in the observed three-line adaptation.

## Verification and limits

Performed independently: full narrow-diff and new-control source review, all manifest hashes, AST syntax, renderer diff and hash verification. Not performed: Blender launch, actual guide prescreen, full field solve, complete child generation, provisional save/reopen, rendering or native image inspection. The new prescreen adds up to 384 actual guide checks; runtime remains unmeasured here.

The source is ready for the one proposed ninth attempt. F21's full-population physical proof and the user's hair appearance goal remain unresolved. A successful guide prescreen must not be reported as a successful groom, and any later failure must retain its exact witness. Further source changes or another run require their own bounded disposition.

## Subsequent root-run outcome: fixed cell remains uncertified

Root executed the one authorized attempt after the source-readiness decision. I read its `result.json`, SHA-256 `468ea0d5785e156007a3fb07c1ab7bd780213a9826146af83b4e1b54efff66ed`; `process.json`, SHA-256 `cc46a7c0cab0bfff112d5682e16b6f3260795badcb5de085cf87287340b52a1c`; and `prescreen-guides.json`, SHA-256 `f2522c6539539c6e79211718cb10d2e80584c903a8b043f6d0f7af4b225096eb`. These are attributed runtime records, not a Blender run performed by the reviewer.

All 192 guide prescreens completed: 60 guides passed both representations and 132 were eligible for repair through measured physical failures. Across the 384 phase records there are 120 passes and 264 physical failures, with no instrument-error or noncertification outcome. Guide 26's lower domain is empty and is labeled accordingly. Guide 27 certifies 8.907881 mm in each representation. The final `preserved_exact` flags have not been finalized: the attempt stops before the final guide loop, so selection for preservation is not a completed all-field proof.

The actual failure is wholly fixed cell guides 26/27, samples 100-101, during shared-corridor construction. The best existing vertex-anchored containing-ball body lower bound is 4.334556 mm, below the unchanged 5.001 mm construction requirement. Its tested vertices are approximately 9.823 to 12.661 mm from the body, but those point distances do not prove that the whole cell meets the required margin. No actual crossing is established by this failure; the interior remains uncertified under that single-ball construction.

All historical controls and complete support equivalence passed, and all input/source/production immutability flags are true. Prescreen metrics stayed isolated: final guide/child path, ray and distance-query counts remain zero. No QP, child population, saved-scene success record or native render followed. I checked that `candidate19-provisional.blend` is absent. The owned process receipt records exit 1, a closed process/job, no timeout and 20.009 seconds elapsed.

Attempt 19 is therefore rejected as a complete construction result. Source readiness above remains its historical preflight decision, not a geometry pass. Root reports that nine of ten second-round attempts are now used and one remains. No retry or new source execution is authorized by this report.

## Initial adaptive-certificate design assessment

Root subsequently requested only a read-only design judgment on a bounded adaptive fixed-cell certificate. The proposed farthest-pair split is valid in real arithmetic. For `P=conv(V)`, select vertices `a,b` and `m=(a+b)/2`; replace `a` by `m` for one child hull and `b` by `m` for the other. For any parent convex combination with weights `lambda_a <= lambda_b`, rewrite `lambda_a*a + lambda_b*b` as `2*lambda_a*m + (lambda_b-lambda_a)*b`, placing the point in the child without `a`. Reverse the roles for the opposite inequality. Both children lie within the parent, and together they cover it. Choosing the farthest pair is a refinement strategy; it is not needed for this coverage identity and does not by itself guarantee a certificate within a finite budget.

This can tighten a sufficient containing-ball bound without lowering the margin or changing the actual cell. Every leaf must retain the exterior-side condition and satisfy distance to each complete BVH minus a genuine containing radius at the same 5.001 mm target. A node/depth limit must fail if any region remains queued or uncertified. Duplicate or degenerate vertices must be handled without losing parent coverage. The radius should be computed relative to the actual queried anchor, with conservative allowance for its float32 conversion and numerical subdivision error; a mathematical midpoint identity should not be silently treated as an exact floating-point coverage guarantee.

The certificate remains fixed-core-only and cannot replace actual guide, offset, child-shaft or stored-curve checks. A useful bounded diagnostic should include this failed cell, an interior-crossing cell whose endpoints/vertices alone look clear, and forced budget exhaustion, in addition to the existing inside-body negative. Those controls distinguish whole-cell coverage from a sampled or prematurely stopped traversal.

The proposed adaptive proof is justified for a bounded diagnostic. No attempt-20 source, full-groom run or appearance approval is given here; exact implementation, leaf coverage, numerical bounds and failure behavior still require review. No such diagnostic was executed by this reviewer.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F32 | Already-safe guides were needlessly fitted. | Source dispatch correction is supported; actual prescreen identifies 60 safe guides. | Final preservation output never completes, so no full repair acceptance. |
| F21 | Complete actual guide/child proof remains open. | Fixed-cell certificate fails before QPs and children. | Bounded adaptive proof investigation; physical limits unchanged. |
| F12 | Hair naturalness remains unresolved. | No saved scene or render. | One substantive attempt remains, subject to fresh source review. |

## Verification

Root independently reran pure mathematical and prescreen controls; reviewer verified exact hashes, source differences and renderer target adaptation. The one run classifies all 192 guides: 60 dual-pass and 132 physical failures, with zero instrument errors/noncertification. It stops at fixed cell 26/27, points 100-101, whose best vertex-anchored ball bound is 4.334556 mm versus 5.001 mm required. No actual crossing is established by this failure. All final guide/child counters remain zero and final preservation flags are unfinished. Complete support equivalence, actual controls and source/input immutability pass. PID 6576 exits 1 and closes after 20.009 seconds; no QP, children, saved_scene entry or provisional file.

## Round outcome

Exact-source readiness enabled one execution; runtime failed at a conservative whole-cell certificate. Nine of ten substantive attempts are used. The mathematically sound adaptive split is permitted for bounded diagnostic investigation only, with complete coverage, exterior/rounding safeguards and failure on exhausted budgets. No final full run is authorized by this record.

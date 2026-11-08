# Review 22: implementation

## Target

Attempt 18 shared-field correction based on 882e4f4d609669add52785cb39b424644d8f4deb. All 20 executed source/evidence files and authored review remain in outputs/character-round2-20261107/hair-attempt18-evidence, archive-manifest.json SHA256 d3cce8d1624598ba463c888230de4d3c055ccc97a91500696c99f00c67beb539. Initial exact target and unchanged dependencies are listed in the authored report; shared root-owned fingerprint dependencies remain in their separately retained paths.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 da2d10ffac7b0e3d46e6aca0e2782ff7e6ef5a93d2d89ad9efbe96333734fec0.

# Attempt 18: independent source preflight

Reviewer: Independent Codex reviewer, Astra xhigh. Base `882e4f4d609669add52785cb39b424644d8f4deb`; intervening commits are documentation, with production runtime still based on `dc67d1c`. Scope is the exact evidence-only clipped-cell instrument and authorized provisional-save workflow before one bounded run. No production source was changed, Blender launched or new image inspected by this reviewer.

## Exact target and coverage

The target is `outputs/.worktrees/character-naturalness-round2/outputs/round2-hair-search/attempt18/` under the primary checkout. I independently matched every source in `preflight-sha256.json`, whose SHA-256 is `8eb094e2132f9f77e1ea10a7f61552d99cd268f41f74a0951fbfe146a6b4acd0`, and parsed all eight Python sources for syntax. Full source files are retained in this fresh attempt directory; attempt 17 and its original failure evidence remain separate.

| Source | SHA-256 |
|---|---|
| `shared_field.py` | `1a46fb86694f392070ba6cf55f7e45b1c2df5b35b2f281c531e6b1cb1a8736b2` |
| `cell_certificate.py` | `af5417d2aac6f1010dc4bf2cfe07540df24686034d2da1adfc5d9f2c1d31d024` |
| `probe.py` | `a74d025c823f99e1578f9b22d6e053559f265d2c8e902280c1d7a026168681e0` |
| `run.py` | `4f4022b10b6db7d154a3441300969c7bd8567066578bffbf0fb0109937f3d4d4` |
| `mathematical_controls.py` | `7c59b4d3c90687bb5c32a16b6e3c3d9d332b338311f208ff1cde273e0780aaca` |
| Unchanged `groom-source.py` | `d86665075b80352d5ff1ce659a1abbb4143d151aa8dbf4861861b8bdf3e0d78f` |
| Unchanged `global_route_core.py` | `a986d8d147ebaecc7ca2599e7c942becbeb7c0d2eaaf4308874fa697aa5fcc8a` |
| Unchanged `complete_lower.py` | `0af6595c670e5140ab3505c1443a9e36d3e2f8e2a7696c3854f9d0c9831aa1d6` |

The preflight description hashes to `93e6efb5549d5c0e7a42d1c418cf13cf5d6fb708c9585b0a6ac3aa9799819705`; the retained pure mathematical-control result hashes to `7bded22faddfee4d4f0b9cd1ea3e52e973b7c6c76180250bd4af5aa5b92e9965`. The shared primary `outputs/character-round2-20261107/hair_render_fingerprint.py` remains `cc63b9b80f4e819d8a96c87417a1576729b5dddd4e9a0a69b7dadf9846d60dbf`. Its renderer-side contract was reviewed separately at renderer SHA-256 `813cae1b22aaf0fab3d006d417ee5975163af1e1c1e5adabea299a7a8eafa65f`.

I read the complete new cell mathematics, shared-field integration, probe, launcher and mathematical controls, and checked the unchanged groom/physical-verifier contract against the prior review. At the end of the source inspection there was neither a provisional scene nor a runtime result receipt in this attempt directory. Root independently reports rerunning all five pure mathematical controls with bundled Blender Python; that is a root-run result, not my own solver or Blender execution.

## Decision

Ready for one bounded attempt using these exact sources. I found no blocking source defect in the reviewed scope. This grants readiness to run, not a complete-groom, F21 physical-clearance or appearance pass. The actual run may legitimately fail under its unchanged physical checks or conservative construction constraints. There is no approval for an automatic retry or a threshold/normal sweep.

The change is justified by attempt 17's diagnosed fixed cell: a whole-cell 3D containing-ball bound establishes at least 8.585844 mm body clearance and 97.900023 mm clothing clearance, while its best padded horizontal projected separator reaches only 5.877665 mm. A 6 mm projected construction target therefore rejected this safe fixed cell for a conservative representation reason. Replacing that target with 5.001 mm while retaining actual 5 mm guide and 1.5 mm shaft-surface checks is an explicit construction correction, not a physical acceptance relaxation. The 6 mm vertical obstacle padding remains unchanged.

## Mathematical and integration assessment

`clipped_weights()` correctly includes in-band corners and intersections of all six original tetrahedron edges with both parallel height planes. All resulting weights are nonnegative, sum to one, and retain their exact height-domain interpretation. This is a convex-hull bound for the four-corner emitted cell, so it covers its bilinear field even when the four corners are not coplanar. Redundant vertices in planar or line degeneracies are harmless. Fixed final Z coordinates are essential; the post-solve replay explicitly checks them rather than relying on the original heights implicitly.

`separator()` distinguishes empty, overlapping and separated projected hulls and handles point/segment fixed subsets. For separated convex hulls, its closest vertex-edge pair produces an oriented supporting direction, and the code verifies that the resulting support gap agrees with the computed Euclidean hull separation. The projected obstacle hull is built from the complete padded face population. When no fixed clipped vertex exists, the anatomical route direction remains the stated conservative choice. A variable cell with an incompatible fixed subset fails; it does not silently substitute the fixed-cell exemption.

The per-guide residual split is sufficient. For a clipped inequality `sum(C_g x_g) + F >= b + T`, each free guide receives `(alpha_g / sum(alpha)) * (b + T - F)`, where `alpha_g` is its actual positive convex corner weight. Summing those guide inequalities recovers the original joint inequality. Zero free weight is treated separately as a fixed condition, and tiny positive weights are retained rather than discarded. This can exclude some feasible joint solutions; it is not claimed to be a complete coupled optimizer. That conservatism can cause a future failure without proving physical impossibility.

The source does not stop at the decomposition's arithmetic assertion or each QP's solver status. After all independent guide solves, it reconstructs the actual four corners, applies the original clipped weights and recomputes every original horizontal inequality. It also reconstructs each knot-split Bezier control set from the solved coefficients and checks the span inequalities. Splitting at spline knots preserves the single-cubic convex-hull argument; clipping each span's parameter interval by its fixed height keeps that certificate within its stated domain. These replays close the gap between separately allocated constraints and the actual joint field.

The 3D ball fallback is restricted to wholly fixed clipped expressions. Its anchor must satisfy the existing outward body-normal side convention before unsigned surface distance is used. A containing-ball radius then bounds every point in the fixed convex hull; distance minus that radius supplies the continuous surface-clearance lower bound. The final replay requires the supposedly fixed coordinates to remain exact and recomputes the proof on the same complete BVHs. It is explicitly labeled fixed-core-only. It does not certify radial layers, waves, child interpolation or all possible offsets. The actual child verifier remains mandatory for those generated paths.

Complete canonical body and all render-evaluated clothing faces remain in the support. There is no overall clothing-band prefilter. Render-enabled modifier settings and render subdivision levels are recorded and restored. Candidate-10/candidate-11 complete evaluated support hashes must still match before proceeding. This retains the earlier support-completeness and transfer repairs.

The actual physical checks are not replaced by the 5.001 mm construction number. Every guide is checked against both surfaces before and after float32 rounding; the measured coordinate rounding plus QP tolerance must fit within the explicit construction reserve. Every child is checked during generation and again from its actual stored Blender points. Stored shaft radii enter the continuous Lipschitz lower bound through a conservative maximum endpoint radius. Segment rays, inside-body rejection, boundary clipping, whole lower-entry turn/collapse checks and depth-limit failure remain in place. The required population is still 11,425 strands on each side plus 150 loose strands, with 64 points per strand. Original fringe/crown/temple, face/ear and root/lift guards, plus the independent corrected lower checker, remain required.

The unchanged preferred transverse field does not establish a hard minimum inter-guide or inter-strand spacing. A geometry pass can still produce concentrated or unnatural hair. Finite turn limits likewise do not certify pleasing curvature. Native fixed and held-out views remain the acceptance evidence for the user's hair complaint; no source result should be described as aesthetic improvement.

## Controls, save binding and ownership

The pure controls cover clipping both height planes and all six edges, the exact historical mixed cell and saved obstacle hull, two/single/zero/tiny free-weight residual cases, fixed contributions and degenerate projected hulls. They exercise the original joint inequality directly rather than merely checking the helper's reported status. Their stored pass result and root's independent rerun support the source math, but neither substitutes for the actual Blender population.

The forthcoming actual run retains the historical bad-guide, enlarged stored-radius and pre-index-46 entry-kink controls. It adds the real fixed-cell positive and an inside-head bad-cell control that first proves unsigned distance alone would exceed the target, then requires exterior-side rejection. Temporary control curves are removed in `finally`; metrics are restored after successful controls. Candidate acceptance still requires the controls and all subsequent population checks to succeed.

The previously pending renderer producer condition is satisfied in this source. After the actual stored-strand physical loop, independent upper/root/lower checks and scene-contract assertion, the probe computes the shared render fingerprint immediately before the provisional save. No intervening operation changes hair geometry or material state. Both the fingerprint helper and `check_character_variant.py` are included explicitly in the immutable source map; the helper's expected SHA-256 is also asserted. The receipt binds the ordered object names, coordinate hash, full supported render-state hash and saved scene path/SHA-256. The separately reviewed renderer requires those dependency entries and compares the fingerprint after reopening. Successful reopening remains a future runtime result.

Saving is conditional on complete geometry success and refuses an existing target. It writes only the authorized `candidate18-provisional.blend` in this attempt directory, with status `geometry_pass_pending_appearance`. The normal exception/immutability-failure path removes an attempt-owned provisional file if a save had begun, preserving any pre-existing file rejected before ownership. A forced external termination can bypass Python cleanup; root must inspect the owned-process result and any interrupted output rather than treating file existence alone as a pass. The renderer also requires the successful bound result receipt, so an incomplete file is not an accepted artifact.

The runner retains the 900-second wall deadline, hidden owned headless process, WindowsJob and finally cleanup. There is no automatic retry. Final input, candidate-11, production and listed evidence-source hashes must remain unchanged; immutability failure invalidates the status and process outcome. The docstring's inherited word “unsaved” is stale, but the executable save gate, receipt scope and preflight explicitly describe the authorized provisional save; this wording is not a readiness blocker.

## Outcome and limits

Independent verification performed here: complete static review of the new source and save contract, all eight manifest hashes, AST syntax, shared-helper hash, and review of the retained pure-control evidence. No Blender, full-guide solve, complete child generation, save/reopen, timeout-control execution or native render inspection was performed by this reviewer.

The exact source is ready for the single bounded run. F21 is not closed by this source review: the actual complete stored population must demonstrate the required margins. Hair appearance remains unresolved until the resulting candidate, if any, is inspected in all six native views. Any runtime failure must retain its witness and be judged on its actual scope; it does not authorize reducing physical requirements or declaring an attractive groom impossible.

## Subsequent root-run outcome: rejected before population or save

After the exact-source readiness decision, root executed the one authorized attempt. I then read its actual `result.json`, SHA-256 `a151d9198f65263f8e9f87c00f9e550c5a718f3815c12eeb282c9cb923de3858`, and `process.json`, SHA-256 `46a4e68053f3f306ee8809d92ccd9e56222d1ef7539b3e9770202e23b378026d`. This is a separately attributed runtime outcome, not a retrospective claim that the source review or complete population passed.

The run failed the retained guide turn/collapse gate on left-bank guide 27, join index 98. The measured join turn is 79.041627 degrees, above the unchanged 75-degree rejection threshold; the solved curve also adds 504.091347 mm of arc length and reaches 437.578091 mm in absolute lateral extent. The QP had one active constraint and small equality residual, illustrating why satisfying its algebra alone cannot establish a usable guide. The physical/shape checks appropriately stopped the attempt.

All five actual controls produced their expected outcomes, complete candidate-10/candidate-11 support hashes matched, and input/production/evidence-source immutability flags are true. The failure occurs before any new child population or saved scene: checked child paths are zero, no `stored_curves` or `saved_scene` success record exists, and I verified that `candidate18-provisional.blend` is absent. The owned process receipt records exit 1, no timeout, a closed process/job and 30.006 seconds elapsed. No native candidate-18 image or appearance acceptance follows from this run.

Attempt 18 is therefore a rejected construction result, with F21's complete-population proof and the user's hair appearance goal still unresolved. The source-readiness judgment above remains its historical preflight decision; it is not an authorization to rerun or relax the failing shape threshold. Root reports that eight of the ten second-round attempts are now used, with two remaining. No further diagnostic or solver revision was performed by this reviewer.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F21 | Complete actual guide and child margins remain unproved. | Open: source preserves the limits, but runtime fails before children. | No geometry acceptance; preserve actual failed solve. |
| F12 | Hair naturalness remains unresolved. | Open: no usable groom or native render was produced. | Diagnose the excessive guide excursion before a further bounded attempt. |
| F30 | Saved curve rendering state needs the actual physical-stage binding. | Source producer condition is satisfied. | Fingerprint is after stored physical checks and guards, immediately before provisional save, with both dependencies required. Runtime save was never reached. |

## Verification

Reviewer checked all eight manifest hashes and syntax. Root separately reran the five pure mathematical controls using Blender bundled Python; all pass. The single actual run reproduced full support equivalence and all five actual controls, then rejected guide 27 at 79.041627 degrees, 504.091347 mm extra length and 437.578091 mm lateral extent. PID 33176 exited 1 and closed at 30.006 seconds; source/input/production hashes remain unchanged. No child, saved_scene entry or provisional blend exists.

## Round outcome

Exact-source readiness enabled one run; it did not pre-approve success. Runtime construction failed. Eight of ten substantive attempts are used and two remain; no retry, parameter change, production integration or native visual acceptance follows automatically.

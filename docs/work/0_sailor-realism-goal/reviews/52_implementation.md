# Review 52: implementation

## Target

Endpoint eligibility and radius repair, exact twelve-path native replay.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native execution, acceptance and delivery.

## Reports

Complete authored report, SHA-256 `e155071470989a721fbd7d2af3f6bf4717840596e90a1cc5471954f6fcd93d0a`.

# Independent terminal-plan v3 review — 2026-11-08

Decision: no blocker in the frozen terminal-eligibility/radius repair or its bounded runner. The root-owned actual diagnostic passes all 12 requested cases, including the exact failed candidate28 strand2391. This permits preparing and reviewing a complete integration bundle; it is not a full-population, saved-scene, rendered or aesthetic acceptance. I read source and retained evidence, ran pure controls without writing their receipts or bytecode, and wrote only this report. I launched no Blender/GPU job and did not read another reviewer's report.

## Exact scope and bindings

| Artifact in `surface-terminal-plan-v3` | SHA256 |
| --- | --- |
| `surface_groom_core.py` | `815ead7941b2951da64425f52d53fbd797d9d293bda274f99e290dd64a3c2fa3` |
| `run_bounded_terminal_plan.py` | `c782a1a0a65d9c5ddea153027a45c8d2d0ce7631f8e69f2fa623d37e461ddff3` |
| `source-manifest.json` | `2fdf05b24592ebccb6a1d1ca4c4447ade0d3d69e6bc36d863e9e559c32820847` |
| `outer_ear_support.py` | `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2` |
| `support_envelope.py` | `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2` |
| `check_terminal_plan.py` | `761223d5d84fadd6979367c15b7627b4c7f8740aba86648d0262ce122b269a42` |
| `check_capture_budget.py` | `c84bd909ddc0af657d49978dc2cfdc5f104d2396dd498eaa5fb95cd02dfdf375` |

All six local and 38 external manifest entries match their current bytes. The actual root-staged core, runner and two construction helpers are byte-identical to this frozen source. I independently regenerated the unified core diff against candidate28 core `91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78`; it exactly matches `core-diff.patch`. The only behavioral change is in terminal planning. March changes attach diagnostic metadata around the same planning and failure paths; event clipping, physical proofs, contact steering, float32 step limits and capture-budget code are unchanged.

## Repair assessment

Each candidate point is rounded to float32 before querying complete physical support and every construction contact. Physical reserve subtracts its required margin, 0.08 mm shaft radius and 0.0003 mm numerical reserve. Each construction reserve separately subtracts its own hard margin, shaft radius and numerical reserve. Eligibility requires physical exterior, correct side, finite physical reserve greater than 0.0006 mm, and every construction reserve finite and greater than 0.0006 mm. An invalid candidate cannot be selected even if Python's minimum operation encounters a NaN before/after another value: the separate finite checks control eligibility.

The selected radius is `min(2 mm, max(0, minimum_hard_reserve - 0.0003 mm))`, using the minimum physical/construction reserve. Construction contacts are not replaced by Euclidean body distances: the support-envelope field remains its documented conservative 1-Lipschitz lower bound. The fixed actual wrapper supplies both ear contacts. All-constraint-valid original goals skip projection entirely, including valid goals with less than the optional 1.5 mm steering buffer. Only invalid originals invoke the existing outer radial projection; every projected point is rounded and freshly checked, with the same side/exterior/reserve requirements. Neither the projection algorithm nor its clearance targets changed. No first-approach completion or tolerance inflation was added.

The radius remains a planning/capture bound, not a substitute for complete segment verification. The physical required-margin function can vary with height; the retained integration/event proof checks the maximum required margin at the actual segment endpoints, and the native/final instruments still check every actual segment. The review does not infer that an arbitrary unverified path inside a terminal ball is safe.

The exact native candidate28 snapshot is decisive counterevidence: the old planner preserves a physical-only radius of 1.8936828623950482 mm around a center with −0.4102303514325549 mm hard ear reserve. The new planner rejects that original. It does not enlarge the old region or waive the failed contour; it constructs and rechecks an eligible projected goal using the pre-existing invalid-goal route.

## Pure checks and retained limits

I reran all ten authored terminal-planning/source controls in memory: physical-valid/construction-invalid projection; the reverse case; thin valid original preservation; a second construction contact determining the minimum; physical reserve determining the minimum; physical-only backward compatibility and 2 mm cap; fresh rejection of an invalid projected point; exact native2391 rejection; exhausted-march plans/travel attachment; and unchanged unrelated helpers/900-step default. All pass. The five capture-budget cases also pass their expected outcomes, including reproducing the original overrun, rejecting insufficient budget and one-ULP-short capture, and preserving exact/ample-budget capture. I independently tested nine non-finite cases: NaN, positive infinity and negative infinity in the physical reserve, first construction contact and second construction contact. All reject rather than select an invalid goal.

The native runner uses the same 0.5 m long / 0.3 m short budgets and default 900-step maximum. It requires actual terminal-ball arrival, the retained lowest fringe scanline, complete-body root attachment, every-path physical proof, lower 5 mm guide and 1.5 mm shaft checks, adaptive nondegeneracy and unchanged lower 75-degree turn guard, unchanged head/radial postguard, and whole-path brow shaft clearance. Missing body root support, an ambiguous body support, non-finite distance, interior root or distance outside 0..0.3 mm throws before `root_attachment_pass=True`. The query is wired as separate actual physical geometry plus construction support, not a construction substitute for actual geometry. The old first-11 case sequence/seeds and exact failed2391 specification are bound; failures are recorded individually and the final assertion requires all 12 rows to pass.

## Actual bounded result

`terminal-plan-v3-root-probe/bounded-terminal-plan.json` has SHA256 `c56fcfc57590514e063f4ba11f559c1c5fc117909e54f15be0fdefe33e8ac0c5`. It reports `bounded_pass`, 12/12 geometry passes, internal elapsed time 9.3966511 seconds, unchanged input/failure/source bindings, and unchanged scene object-name inventory. All 45 recorded source/input bindings independently rehash without mismatch. Input is accepted candidate27 blend `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`; complete evaluated body/clothing hashes are asserted by the runner. The object-name inventory flag alone is not a geometry fingerprint, and no scene was saved or rendered by this diagnostic.

I compared the first 11 cases to the prior accepted `ear-terminal-root-probe/bounded-ear-steering.json`: every specification and every recorded point is exactly equal, not merely approximately close. The original valid ear and thin-terminal cases retain their original goals. The thin goal still has 0.4010976189613348 mm radius and ends at its center. These are useful direct regression checks; the new required construction-radius accounting did not change those actual paths.

For exact candidate28 strand2391, the original center is now explicitly recorded as physical-valid/construction-invalid. The existing projection moves it 3.0598383706614204 mm to `[-0.06564163416624069, -0.11592946201562881, 1.5488559007644653]`. Fresh physical hard reserve is 4.748776660573483 mm and minimum construction hard reserve is 2.393447674220717 mm, yielding a 2 mm terminal radius. The path finishes in 111 points / 110 segments with actual arclength 0.12462347619600112 m; its endpoint distance is 1.999869532827333 mm, strictly inside that measured sphere. Its root distance is 0.11940262629650533 mm. This is a completed bounded path with the retained guards, unlike the earlier measurement-only chord witnesses.

Across all 12 cases I recomputed every recorded arclength, checked 2..901 point counts, the unchanged travel budgets and strict arrival radii for all long paths. Maximum arclength is 0.3488376809306132 m, maximum root distance is 0.11993543012067676 mm, and maximum lower turn is 53.124580743917804 degrees. The brow receipt accounts for all 12 paths and all 2,347 segments against the accepted evaluated brow surface SHA256 `4c857cd5efda96be78410718f85c7a406f485a860597a7cfc1601eff956d0a4b` (1,642 vertices / 3,072 triangles). All 2,347 pass the expanded-AABB separation proof; none exercises the recursive capsule branch in this particular bounded sample. The final full population still needs that guard with actual emitted radii.

## Diagnostic coverage and integration followups

The core now attaches exact terminal/scalp plans and accumulated length/release state to failures raised through `march.fail`, including the reproduced exhausted-step case. Terminal-plan exhaustion with no eligible candidate retains its rejected candidates and adds the scalp plan when propagated through `march`. The bounded runner reads exception plans and length before falling back to returned results. This addresses the missing-plan diagnosis that obstructed candidate28 analysis.

This is not universal metadata coverage: exceptions thrown directly by external projection/query code before those handlers may lack a terminal plan or travel state, and the bounded row writer does not serialize the exception's `released` or `release_length_m` fields. These remain diagnostic limitations, not paths that can falsely succeed. Most importantly, unchanged candidate28 `build_surface_groom.py` still writes `result.get('terminal_plan')` and `result.get('length_m')`; simply swapping in the new core would discard the new exception metadata again on a full march failure. Root and author were informed before full integration. The candidate29 fullbundle must explicitly wire exception plans/state into its first-failure writer, bind this 12-case evidence and the active source files, and undergo its own exact review.

No source/actual bounded blocker remains in this v3 scope. Full 23,000-strand construction, every emitted float32 point/radius, coverage, final face/ear/brow gates, save/reopen fingerprints, unchanged nonhair candidate27 state and six native render receipts remain unperformed by this review. No integrated attempt or visual acceptance is implied.


## Findings and disposition

Accept the bounded repair and its exact native result. Previous eleven paths are unchanged; the formerly failing path now finishes within every retained limit. A complete candidate still requires full-population and native visual gates.

## Verification

Exact sources, native receipts and original failure evidence are retained under `outputs/character-round3-20261108`. Reviewed unclothed delivery files are also retained under `outputs/unclothed-variant/relaxed-brows`.

## Round outcome

Nine integrated attempts used, one remains, next 30. Brows are accepted in both delivered variants; whole face and hair realism remains open.

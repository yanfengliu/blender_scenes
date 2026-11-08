# Review 20: implementation

## Target

Buccal diagnostic prerequisite based on 49da8f215db2a0d501b23f8d44b5891daacc3c8a. Exact source, expected field, failed screens, corrected actual-fit measurements and subsequent unsaved render are retained in outputs/character-round2-20261107/face-form-attempt16-evidence; archive-manifest.json SHA256 bd1b5a5825485085c1f7f15b596756c738a143c3fa9b37857998cd4185702159 binds all 33 files. Individual target hashes are in the authored report.

## Reviewers and coverage

Astra xhigh independently read source and diffs, verified hashes, reproduced scalar field values, and checked recorded populations and inequalities. No reviewer-run Blender or pixel review occurred in this prerequisite review. Root and the diagnostic author subsequently inspected the three native views.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows; its original SHA256 is 895ce8ba20b2dea98c3833be99245eb015d5a74a25df60ad2b1f69642aa4a5b7.

# Independent review: buccal diagnostic ocular instrument

Reviewer: Independent Codex reviewer, Astra xhigh. Scope: whether actual evaluated ocular evidence justifies replacing the conservative bounding-box pre-render screen for one unsaved native portrait, face-oblique and profile comparison. This is not production integration, smile-contract rebinding or appearance acceptance. No Blender process or render was launched by this reviewer; no source was edited.

## Exact reviewed target

The worktree is `outputs/.worktrees/character-naturalness-round2/`; paths below are relative to its `outputs/face-form-diagnostic/`. I recomputed every artifact hash listed by `corrected-fit-outcome.json` and found no mismatch.

| Input or evidence | SHA-256 |
|---|---|
| `probe.py` | `4769a66781f8537a262d827004b0ea27d618ffb05fcbfa49b13329d29cf4700e` |
| `deltas.json` | `3b17327f61cff9f29066eecb569f0c18cc87460d4a41135807ce12c0cb9c3020` |
| `expected-points.json` | `660812876e0873354d1cb3fc01d7cbed05ef2297273cdc6454cb5b05e4a083aa` |
| `measure_actual_fit_corrected.py` | `634e3f2a594a617b48ddcb6e5d15217ad1e5517888c2a33a6ec987b8fc6b5b6f` |
| `actual-fit-measurement-corrected.json` | `befd771c3f01941ae5f53155ea0815155fa4da0065737db0fda09ac08d62a6f0` |
| `ocular-screen-witnesses-corrected.json` | `755116b7a9f189b527483d69adaa770aa151177af38243dc2dca582dafea1c51` |
| `corrected-fit-outcome.json` | `20e734a40746ac45f2621996c7247349f287e5d4779cdcefe9e41366f7a85ec8` |
| `evaluated-change.json` | `c68e803a3b875ab486bb765543563e86b4a902d9aba2b300a95833a5e6c7da12` |
| Original halted `render_diagnostic.py` | `a0edc4853031e5ea54ed0e0331571562c6e203dc55f72d68dc7c7fb61dd36d08` |

The `3b17327f...` hash identifies the field data, not `probe.py`; the request's initial label was corrected by root and is not repeated here. The unchanged comparison functions come directly from primary-checkout `outputs/sailor_character_realism_goal/candidate-12/source/tools/check_orbital_fit.py`, SHA-256 `0940ae31ff6fbf1d11075165a1c5f118bc416d2e6ee2fbd40a473940b2a7ae24`, independently verified. The measured input is frozen candidate 10, blend SHA-256 `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`, asserted at entry and exit by the executed measurement.

Current production anatomy source SHA-256 is `5e086f3131fbef21a545bf115a2a2ad37ea481ba3801fd615c1f785c781afb9e`, matching the probe and corrected receipt. The unchanged oral evaluator is `tools/verify_reference_smile.py`, SHA-256 `235cf8e41c676394abe80c5bd6c157ca44962ae398766708395a4b3b48cc5df4`; the evaluated-mesh utility is `tools/check_garment_isolation.py`, SHA-256 `e14f1262c69464c32ee5f34983d2047a27015de7bc5eb0cea4d4b207e6f0e2fd`. I recomputed these source hashes.

## Decision and reasons

Approve replacing the overly broad zero-movement bounding-box screen with the exact actual-surface measurement as the prerequisite for one unsaved native diagnostic triplet of this field. This is a correction to a diagnostic screen, not permission to relax the existing 50 micrometre evaluated-fit limits. It does not establish that the face is more appealing or that the proposal is ready to enter production.

The original screen selects every evaluated body point within the evaluated eye object's axis-aligned box expanded by 3 mm and rejects any nonzero movement there. A point in such a box need not be close to the finite corneal surface. Its largest changed witness, row 80010, moves 0.640258 mm but remains 11.147578 mm from the actual corneal shell after the edit, with positive signed-normal clearance. This is concrete evidence that movement inside that box is not equivalent to an ocular-contact failure. The original halted run and its receipt must remain intact; they correctly record the result of the original conservative rule.

The replacement keeps the relevant previously reviewed measurement rather than inventing a more favorable threshold or smaller population. It hash-pins and AST-extracts `rendered`, `snapshot`, `tree`, `signed_distance`, `compare` and `accept` directly from the frozen checker, without editing those function bodies. The global tolerance remains exactly 0.00005 m. Evaluated subdivision uses render levels, and the corneal shell population is checked rather than inferred from a proxy. The exact candidate receipt contains 15,680 corneal triangles and preserves evaluated Eyes and Eyelashes exactly.

The fixed baseline-selected ocular population remains 9,514 evaluated body rows, and the fallback additionally includes all 9,173 evaluated body rows actually changed by the field; these populations can overlap. The original 964 baseline-selected lash roots are retained. The candidate's maximum added eye penetration is 4.386216 micrometres, including the all-changed-row fallback; maximum added lash separation is 25.404056 micrometres; added lash penetration is zero. I independently checked these recorded quantities against the unchanged four acceptance inequalities. No-op comparisons report zero for all four regressions.

The worst actual eye regression is at row 22115, on a triangle without an open-shell boundary edge: signed-normal distance changes from approximately -0.476895 to -0.481281 mm. Keeping this existing negative value visible matters. The check bounds additional sampled regression; it does not assert that every baseline sample has positive clearance. The complete receipt also contains far-surface and open-shell context, rather than interpreting every signed projection as solid-object penetration.

The first attempted inward control was ineffective for this new field. It moved the buccal field's own weighted rows farther posteriorly and produced only 17.577564 micrometres of added eye regression, so its expected rejection did not occur. That first result is correctly retained as inconclusive in `actual-fit-outcome.json` (`c79caceed9b26df95ce8a7cf405095da3c3cdf2f22e0b816e251d277006b7550`) and `actual-fit-measurement.json` (`b8b06526d57209d2792ae704fcaa689bea7487d629ab8c4cb6acd30ffed0c53c`). It must not be rewritten as a pass.

The corrected control changes the deliberately defective mesh, not the candidate or its acceptance rule. It selects 264 actual source contact-neighborhood rows within 2 mm of the corneal shell, excludes nearest triangles touching an open boundary, and moves them 3 mm opposite the actual outward shell normal. The evaluated eye regression becomes 2.970466 mm and is rejected by the unchanged eye limit. Its recorded worst witness is also away from an open-shell boundary. Separately moving the actual lash object 3 mm yields 2.958953 mm of added root separation and is rejected by the unchanged lash limit. I inspected the original-to-corrected script diff: the candidate comparison and acceptance functions are unchanged; the edits replace the unsuccessful inward-control construction and preserve separate output filenames. This is a justified repair of a noncausal negative control.

The oral evidence also supports a diagnostic render without granting a smile pass. The unchanged live oral evaluator reports all 304 evaluated oral-path vertices unmoved, all 658 unambiguous exterior aperture samples unchanged, and zero change across all 1,322 recorded aperture comparisons. I independently recomputed those counts and zero-change checks from the retained receipt. The source proposal changes 340 rows, with an exact maximum 3.5 mm posterior displacement; evaluating the two scalar field functions against all 340 stored expected points reproduces `deltas.json` exactly, with zero numerical mismatch.

There are still 44 overlaps with the frozen 516-row smile-coordinate contract. Exact oral rails do not make those coordinate records current. The old property/hash remains unchanged during this experiment and is restored with the body; no new pin or full smile-verification result is authorized. Any later integration requires independent neutral/proposed reconstruction, a deliberately reviewed binding update and the full existing safeguards. Source fan-area/orientation observations and the finite ocular measurements also do not constitute a continuous self-intersection proof or a facial anatomy assessment.

## Execution conditions and limits

The replacement renderer must bind the exact field, expected-point input, corrected measurement, baseline and checker hashes, require `measured_pass` plus the successful negative/no-op controls and unchanged 50 micrometre limits, and retain the live oral comparison. The measurement script intentionally records `measured_fail` without necessarily making candidate rejection itself a process error; exit zero alone is not an adequate render precondition. This approval concerns the reviewed data and evidence, not an arbitrary future renderer edit or a changed amplitude/support sweep.

Keep the render unsaved and diagnostic, restore the original body/property/cameras, preserve the source blend and both earlier failed-screen/control records, and inspect all three resulting native views before making an appearance claim. The existing halted renderer already restores the body/cameras and checks input immutability in `finally`; its actual replacement must preserve those behaviors. Owned-process cleanup and the GPU slot remain root's responsibility. No production pin, scene save or integration follows automatically from a favorable triplet.

Coverage is finite evaluated vertex/root nearest-normal sampling against an open finite shell. There is no continuous swept-surface guarantee, full lash shaft certificate, full self-intersection proof or visual acceptance in this review. The exact measurement receipt reports restored body coordinates, unchanged original contract and unchanged saved blend. Its owned process record reports exit zero, 7.263 seconds and a closed process tree; these are worker-run results read from the bound artifacts, not reviewer-run Blender tests.

Independent work performed: source and diff inspection, exact hash checks, offline scalar-field reproduction, receipt/population and inequality checks, and witness interpretation. No Blender, render or native image inspection occurred in this instrument-review round. The bounded decision is to permit the single diagnostic triplet under the conditions above; full face appearance and production integration remain unapproved.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F27 | The eye bounding box rejected distant cheek movement without actual contact regression. | Accepted as an overconservative diagnostic screen. | Replaced only for one unsaved diagnostic by exact hash-bound actual-shell evidence; unchanged 50 micrometre bounds and real negative/no-op controls. |
| F28 | The original field-weighted inward control did not exercise ocular contact. | Accepted as an inconclusive instrument result, preserved. | Actual contact-neighborhood control rejected at 2.970466 mm; candidate checks unchanged. |
| F13 | Face naturalness remains unresolved. | Open: the diagnostic did not materially improve naturalness. | No production face integration or parameter sweep. |

## Verification

The corrected actual-fit receipt reports 4.386 micrometres added eye regression, 25.404 micrometres added lash separation and zero added lash penetration; unchanged limits, successful no-op and both meaningful negative controls were verified. Exact oral geometry remains unchanged, but 44 source rows overlap the old frozen coordinate property and no production rebind is granted. Root dispatched the one hash-bound unsaved triplet as attempt 16, PID 20716, 20.013 seconds, exit 0 with closed process tree. Root and the author reject the native portrait/oblique/profile result: the small cheek change does not materially improve naturalness and can accentuate the muzzle.

## Round outcome

The one diagnostic render was permitted under actual-surface safeguards. Its appearance was rejected, and no source blend, production face or smile binding was changed. Both the original failed screen and ineffective negative control remain recoverable.

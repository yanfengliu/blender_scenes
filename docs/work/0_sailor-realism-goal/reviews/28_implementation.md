# Review 28: implementation

## Target

Frozen saved-scene face diagnostic probe_saved_candidate10.py SHA2569b7dc28d5cf16c9af7a300ddc0435819a42dee621091909af8a8298fbd4bbf37 and saved-probe-inputs.json SHA2569d46d50c24148983302d43c91056e1c32c60efabf1cb58977a8e15e09033cd5e. Exact source, inputs and actual receipt are retained in outputs/character-round3-20261108/face-evaluated-probe.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source, supplied evidence and native reference views. Root owns Blender execution and acceptance. This review did not run Blender or render a new appearance candidate.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 b3be0803a849bde19c157c866835a30a9cff52a732faa94b50264dffef5ff645.

# Independent review of the first round-3 evaluated face instrument

Reviewed 2026-11-08. This is a separate authored follow-up to `face-source.md`; that original report is preserved. I reviewed the frozen runner, its inputs and reused functions, and the root-produced measurement. I did not run Blender, create a render, edit production code, install dependencies, or rely on another reviewer's conclusions. Pure read-only Python controls are described below.

## Decision

Do not accept this runner's fixed-world-X comparison as the replacement physical aperture instrument, and do not render this face candidate yet. Its fail-closed outcome is appropriate, but the reported 838.584 micrometre maximum does not establish an actual mouth-opening regression. The new instrument confounds lateral transport with opening, including at common-domain samples. It also cannot pass its own unchanged actual-mouth population because known terminal alternatives remain unsupported. Separately, the evaluated structure check stopped before completing its safety measurement.

The cumulative pre-smile baseline handling resolves the main baseline issue from FACE-SRC-1 for this exact frozen candidate-10 input: the original retained contract is restored and used, and the complete old/new source union is 642 rows. The finite eye/lash comparison is coherently reused and passes its unchanged bounds on the actual supplied result. These positive parts do not turn the unresolved mouth/structure outcome into a pass.

## Reviewed identity

The worktree remains `C:/Users/38909/Documents/github/blender_scenes/outputs/.worktrees/character-naturalness-round2`, at the source/design revision identified in `face-source.md`. All paths below are relative to the primary checkout. SHA256 values bind the reviewed bytes.

| Artifact | SHA256 |
| --- | --- |
| `outputs/character-round3-20261108/face-form/probe_saved_candidate10.py` and its execution copy under `face-evaluated-probe/` | `9b7dc28d5cf16c9af7a300ddc0435819a42dee621091909af8a8298fbd4bbf37` |
| `outputs/character-round3-20261108/face-form/saved-probe-inputs.json` | `9d46d50c24148983302d43c91056e1c32c60efabf1cb58977a8e15e09033cd5e` |
| `outputs/character-round3-20261108/face-evaluated-probe/saved-candidate10-measurement.json` | `79111baf3ecb7a13e3f646517694f5bf233cb67fd2d3b4dc982bd6bcabdf6ea2` |
| `outputs/character-round3-20261108/face-form/coupled_probe.py` | `827aea5b9a5d783808394ade0e2c48a266a8a440cfe4e03aa4579e09a4e85b65` |
| `outputs/character-round3-20261108/face-form/coupled-probe.json` | `374ac27e71e3bf82fda6d9e1a5be1fdc80df14646d208df9dbd8d385393e3ea4` |
| `outputs/sailor_character_realism_goal/candidate-12/source/tools/check_orbital_fit.py` | `0940ae31ff6fbf1d11075165a1c5f118bc416d2e6ee2fbd40a473940b2a7ae24` |
| `outputs/character-round2-20261107/face-form-attempt16-evidence/measure_actual_fit_corrected.py` | `634e3f2a594a617b48ddcb6e5d15217ad1e5517888c2a33a6ec987b8fc6b5b6f` |
| `outputs/.worktrees/character-naturalness-round2/tools/verify_reference_smile.py` | `235cf8e41c676394abe80c5bd6c157ca44962ae398766708395a4b3b48cc5df4` |
| `outputs/.worktrees/character-naturalness-round2/tools/check_garment_isolation.py` | `e14f1262c69464c32ee5f34983d2047a27015de7bc5eb0cea4d4b207e6f0e2fd` |

The runner checks the immutable blend against `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`, and its measured original mouth contract is `52d36d7c9db5b4750807bb97dec4c0270f7cc4b3aa2296407b36c00194a9ab2e`. I inspected these assertions and the recorded successful checks; I did not independently open the blend.

## Findings

### FACE-INST-1 â€” Fixed-world-X comparison rejects gap-preserving lateral transport

Priority: P1, blocks using this instrument for aperture acceptance or declaring a physical failure from its large positive numbers. `probe_saved_candidate10.py:49-70` samples both states at identical world X. `:57-58` additionally assigns zero aperture outside either state's half-rail domain. Both choices can compare different material sections of the mouth rather than the same opening after it moves. The original fixed-X instrument relied on all-X-exact geometry; replacing that precondition requires an explicit transport/correspondence contract, not merely a larger X-grid.

I executed the exact frozen `union_aperture` function and the exact existing `line_hits` function in pure Python with a small three-coordinate vector implementation. This tests their algebra only, without substituting a different aperture algorithm. The synthetic rails are two mirrored halves with shared central upper/lower points `(0,0,+/-0.0002)`, paired points at `(|x|=.020,z=+/-0.0003)` and `(|x|=.0228,z=+/-0.00045)`, and a common closed corner at `(|x|=.023,z=0)`. Y is zero. Each half's upper/lower chains are centre, first pair, second pair, corner; the same chains are supplied at both depths. Central anchor identities map to the shared central pair. This yields more than 500 exterior samples and no ambiguities.

| Control | Corresponding upper/lower gaps | Reported max scalar/vertical increase | Max common-domain scalar increase | Failures |
| --- | --- | --- | --- | --- |
| Exact no-op | Exact | 0 / 0 micrometres | 0 micrometres | 0 |
| Rigid translation of every point by +1 mm in X | Exact | 900 / 900 micrometres | 814.285714 micrometres | 82, including 57 in the common domain |
| Shared X-width transport `x *= 1.009`, unchanged Y/Z | Exact | 900 / 900 micrometres | 899.447827 micrometres | 16, including 10 in the common domain |

The first control passes, and both gap-preserving transports fail. Rigid translation leaves every geometric distance unchanged. For the width control, each corresponding upper/lower pair still has the same X and exact same separation vector as before. The large rejection is therefore an instrument effect on these valid counterexamples. Removing only outside-domain-zero samples does not solve it. This remains decisive despite using Python arithmetic rather than Blender float32 because the discrepancies are hundreds of micrometres, not rounding-scale errors.

The actual receipt has the same correspondence risk. It reports 17 exterior outside-zero samples, all failing. Excluding them leaves 1,299 common-domain exterior samples and 98 primary failures, with maxima 612.726719 micrometres scalar and 517.725945 micrometres vertical. The worst primary common sample at X=-22.83645048737526 mm pairs old upper/lower segments 47/25 with new segments 44/23. Its old measured distance is 251.940588 micrometres and new distance 864.667307 micrometres. That is a real fixed-world-X cross-section difference; it is not, by itself, a demonstrated increase between corresponding parts of the opening. The incremental comparison has 90 common-domain failures and a 612.952199 micrometre maximum, so the cumulative baseline is not the reason for this particular large number.

Required disposition: preserve this raw result as counterevidence against this instrument's acceptance semantics. Define and independently review correspondence for variable-X rails using actual traced geometry, including corner branch ownership, rather than choosing a remapping solely because it lowers the score. Require exact no-op, rigid transport, known gap-preserving width transport, actual opening, and asymmetric upper/lower separation controls under the unchanged physical bounds. Retain fixed-world-X measurements as a separate occupancy/section diagnostic if useful. Do not drop the 50 micrometre bound, subtract these numbers heuristically, or claim the current face is safe on the basis of this finding.

### FACE-INST-2 â€” The actual no-op is unsupported at terminal branch alternatives

Priority: P1 before acceptance. The blanket ambiguity rule at `probe_saved_candidate10.py:60-68,83` is fail-closed, which is preferable to omitting a difficult corner and reporting a pass. However the actual `mouth_no_op` has four ambiguous records, no physical increases and `sampled_bound_pass=false`. The runner only asserts zero maxima at `:145`, so its successful no-op assertion does not demonstrate that the acceptance instrument accepts unchanged valid geometry.

These are not unexplained numeric noise: at the left exterior terminal X=-22.838199511170387 mm, the upper rail has one branch, while the lower rail contains both an earlier crossing on segment 26 and the shared terminal endpoint on segment 27. The upper/terminal branch meets at the same endpoint; the other lower branch is distinct. Analogous left/right and inner-depth records account for the four no-op alternatives. The proposal has eight ambiguous old/new records because the terminal X positions move.

Required disposition: preserve complete alternatives and explicitly resolve their anatomical/topological meaning, or continue to classify the instrument as unsupported. Extend the retained original terminal ownership/rounding controls to the chosen variable-X correspondence. Do not merely remove ambiguous records or change `sampled_bound_pass` to ignore them. A positive acceptance instrument must demonstrate its no-op success on this actual population and reject real opening in the same supported population.

### FACE-INST-3 â€” Evaluated structure coverage is incomplete for the wider cheek field

Priority: P1, independent of FACE-INST-1 and FACE-INST-2. The runner removes only the old all-X assertion and reuses `compare_structure` at `probe_saved_candidate10.py:161-174`. The actual execution raises `Changed evaluated descendant lies outside complete support/neighbor/old-region union.` at `verify_reference_smile.py:830`. Consequently the complete area/orientation loop, nonadjacent intersection comparisons and inner-cavity checks did not finish. An empty `mouth_structure_failures` list after this exception is not a structural pass; the runner correctly keeps `raw_measured_bounds_pass=false`.

The old population includes descendants of directly affected source faces plus one source-edge neighbor ring, corner patches and an old bounded oral region (`verify_reference_smile.py:804-822`). That population was built for the earlier mouth deformation. The new lateral cheek field can influence additional CC2 limit-surface descendants. The exception establishes a missing population in this exact case, though the receipt does not retain the offending triangle/owner needed to identify the entire missing support.

Required disposition: record the first and complete missing descendant population with actual source/evaluated provenance, then form a complete influence population, including all required collision opponents. Confirm outside-support coordinates remain exact. Keep the coverage assertion and all physical orientation/intersection requirements. Do not enlarge the old coordinate box blindly or suppress the assertion. The retained intersection function excludes shared-vertex pairs and uses stable polygon-pair identities; those inherited limits must remain explicit, and the changed skin's intersections with the complete groom require their own measurement.

## Positive checks and their limits

Input reconstruction is coherent. I independently regenerated the pure source input in memory and verified all 512 expected-before coordinates, all 512 requested-after coordinates and deltas, all 1,269 source guard coordinates, and both eye centres exactly against `saved-probe-inputs.json`. The runner's root-produced measurement reports zero stored-vector mismatch for all 512 and all 1,269 checks. The delta is applied once at `probe_saved_candidate10.py:124`; all other source rows remain exact at `:138`.

The primary neutral is taken from the already frozen candidate-10 contract before the old reference smile, at `:109-122`, and the original/new support union is supplied at `:129`. It is not reset to the post-smile source. Its contract provenance was independently reconstructed when candidate 10 was accepted as the saved benchmark, as recorded in the reviewed project design; this runner relies on that immutable artifact and validated contract rather than performing another no-smile production build. If that historical provenance is no longer trusted, it must be rebuilt before acceptance. It is not repaired by hashing the current property anew.

The six eye/lash functions are compiled verbatim from the pinned candidate-12 checker at `:96-102`. The checker uses actual complete corneal-shell triangles, the retained lower-orbit population and all newly changed evaluated body vertices for its conservative fallback. It compares neutral-selected lash roots with actual body surfaces. In the measured run, 9,514 fixed body samples, 964 lash-root samples and 11,964 changed evaluated fallback rows give zero added eye penetration, zero added lash penetration, and 25.404056 micrometres added signed-normal lash separation, below the original 50 micrometre maximum. Eye and lash evaluated coordinates are exact before/after. No-op regressions are zero.

The inward-eye negative produces 2,970.465855 micrometres added penetration; the translated-lash negative produces 2,958.952863 micrometres added separation. Both are actual evaluated negative meshes and are detected. This supports the bounded finite eye/lash result, not a continuous tissue-contact or all-face intersection guarantee. The open-shell nearest-normal metric can have boundary/projection effects; this runner retains its conservative fallback and reports the worst context rather than removing inconvenient rows. In this result no fallback relaxation is needed.

The reused ocular `rendered` function selects triangles using the frozen eye material slot and asserts more than 10,000 shell triangles; it relies on the pinned saved artifact's already verified shell/material identity. The unpinned import of `check_garment_isolation.evaluated` is included in this review's hash table, but should be retained/pinned with any reusable instrument because the recorded runner hashes alone do not capture that dependency.

The runner restores the original body mesh and saved mouth property in a `finally` block, removes its temporary mesh and copied negative-control objects, checks object/mesh/material identity sets, and verifies the blend hash. The actual receipt reports all cleanup checks true. It never saves or renders. The receipt status explicitly says measured/review-required, so exit code zero is not an approval signal. The retained intersection/distance and rigid-translation numerical controls from the old `_Run.run` are not all executed by this runner; exact reused code alone does not constitute a fresh run of those controls.

## Face-only appearance scope clarification

An isolated face comparison may keep candidate 10's complete hair unchanged while retaining the inherited lower-hair failure as an openly rejected condition. This is consistent with the purpose of comparing independent facial mechanisms and with earlier face-only experiments. It does not waive the 5 mm guide / 1.5 mm emitted-shaft requirements or close F21. Those remain mandatory for new-hair/full-groom acceptance and any claim that the complete character satisfies the round-3 safety benchmark.

For such a face-only experiment, independently verify the complete actual hair geometry remains identical and measure the entire groom against the changed skin for introduced face/ear/groom intersections, preserving old failures rather than reclassifying them. The present runner does not implement either complete-hair identity or hair/skin intersection checking. They are separate prerequisites before rendering, along with a supported mouth instrument and completed evaluated structure checks. Candidate-10 hair must not be regenerated from a changed source path and assumed identical.

This clarification narrows the face-experiment scheduling condition stated broadly in the earlier source report. It does not change final acceptance, the physical margins, or the status of inherited failed evidence.

## What remains

The current result permits retaining a measured source/ocular experiment and the instrument counterexamples. It does not permit claiming an actual mouth failure, an actual mouth pass, complete surface safety, or an appearance improvement. A revised instrument needs independent review of its exact code and controls, then root-owned evaluation. No amplitude or shape retuning is justified solely to make the rejected fixed-world-X measurement smaller.

Only this authored report was written by this follow-up review. Its pure Python commands terminated, with no Blender or GUI subprocess and no task-owned service remaining. The report preserves the first runner/receipt hashes and leaves all production, failure and benchmark artifacts untouched.

## Findings and disposition

Rejected as an aperture acceptance instrument: fixed-world-X comparison confounds lateral transport, an actual no-op has terminal branch alternatives, and the original evaluated structure population is incomplete for the cheek field. No shape failure or visual success is inferred from that instrument.

Preserve original pre-smile neutral and all642changedrows; replace only disproved measurement assumptions through independently reviewed transport-invariant correspondence and complete evaluated influence coverage. No render yet.

## Verification

Root's actual diagnostic matches all 512 proposed baseline rows and 1,269 ocular/proxy guard rows exactly. It uses the original saved pre-smile contract and 642 cumulative changed rows. Actual eye penetration increase is zero and lash separation increase is 25.404 micrometres, within the unchanged 50 micrometre bound; real mouth, eye and lash negatives are detected. The aperture result and structure assertion remain unaccepted for the reasons above. PID 27064 closes after 15.639 seconds; original scene data, contract, input file and temporary data blocks are restored or cleaned. No saved candidate or render is produced.

## Round outcome

Rejected as an aperture acceptance instrument: fixed-world-X comparison confounds lateral transport, an actual no-op has terminal branch alternatives, and the original evaluated structure population is incomplete for the cheek field. No shape failure or visual success is inferred from that instrument. Round 3 remains zero of ten integrated attempts used. All evidence is diagnostic; no production change is accepted by this record.

# Review 27: design

## Target

Coordinated facial-form source proposal and exact receipt on runtime dc67 and docs base52454616a756d1bf41a4bb35d4b9b9a4ec0233ae. Frozen source and original receipts remain in outputs/character-round3-20261108/face-form; exact copied actual probe inputs remain in face-evaluated-probe.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source, supplied evidence and native reference views. Root owns Blender execution and acceptance. This review did not run Blender or render a new appearance candidate.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 8d65528a45c14079677612423d0543adc0e237e5f48146bed5c4e50ded697bda.

# Independent review of the round-3 facial surface proposal

Reviewed 2026-11-08 by the independent Codex source/design reviewer. This report concerns only the exact source proposal and coordinate receipt listed below. No other reviewer's conclusions were read. No Blender evaluation, build, render, installation, network operation, production edit, or GUI was performed. A later geometry runner was not available for this review and is not approved by it.

## Decision

The exact mechanism and coordinate evidence are coherent enough for a root-owned, fail-closed evaluated-safety probe. They are not sufficient to authorize an appearance render by themselves. One native appearance experiment is reasonable only after the actual final geometry passes the unchanged physical bounds with the correct cumulative neutral baseline, and the instrument handling the newly variable mouth width is reviewed. Existing intervention row counts and hashes are provenance for their old fields, not user appearance requirements.

The principal issue is baseline ownership: the supplied 512-row receipt is incremental relative to the already smiling current rest surface. The protected mouth requirement belongs to the independently reconstructed pre-smile neutral. Treating the receipt's `native_before_changed` as the complete neutral would silently give the new deformation another 50 micrometres of allowance. This matters on these exact bytes: the source paired scalar-gap increase is 20.686663 micrometres incrementally, but 56.334935 micrometres cumulatively against the pre-reference-smile neutral. Neither source result proves an evaluated pass or failure.

## Exact reviewed inputs

Repository/worktree: `C:/Users/38909/Documents/github/blender_scenes/outputs/.worktrees/character-naturalness-round2`. HEAD was `52454616a756d1bf41a4bb35d4b9b9a4ec0233ae`; the latest runtime revision was `dc67d1c786e7a67b8107d98ce4c72980173bc62e`. `scenes/` and `tools/` have no differences between the proposal's recorded `0032b5963128707ad23044b18000efc4fdfe828c` base and reviewed HEAD. A later concurrent change to `docs/work/0_sailor-realism-goal/plan.md` was observed and left untouched; it was not relied on.

All SHA256 values are lowercase. Paths in the following table are relative to the primary checkout unless prefixed with `worktree/`.

| Input | SHA256 |
| --- | --- |
| `outputs/character-round3-20261108/face-form/proposal.md` | `e4372f8affdf552e929dea4050fee87ef63ce3320940fe6b8127eb2a81fd4978` |
| `outputs/character-round3-20261108/face-form/coupled_probe.py` | `827aea5b9a5d783808394ade0e2c48a266a8a440cfe4e03aa4579e09a4e85b65` |
| `outputs/character-round3-20261108/face-form/coupled-probe.json` | `374ac27e71e3bf82fda6d9e1a5be1fdc80df14646d208df9dbd8d385393e3ea4` |
| `outputs/character-round3-20261108/face-form/probe.py` | `8b860b8a592e9e80301e76483c0fed80b18b271ebd93c79a56ba074ba3c90153` |
| Reconstructed full native input, compact JSON encoding used by receipt | `03566b35f3e500032e0b28047419b8918a9f3dac3cdced613b14227522295f17` |
| `worktree/docs/work/0_sailor-realism-goal/design.md` | `340cb06ff01a9d7a7f5defeda0ab0a47b0920047e727fceffd74f7cbb71d31a9` |
| `worktree/scenes/sailor_character_realistic.py` | `5e086f3131fbef21a545bf115a2a2ad37ea481ba3801fd615c1f785c781afb9e` |
| `worktree/tools/prepare_human_base.py` | `c4c3526d9ed9c719cdfa7c3c18ef5f25278ea894d9746a879d3874dbf0779b9e` |
| `worktree/tools/verify_reference_smile.py` | `235cf8e41c676394abe80c5bd6c157ca44962ae398766708395a4b3b48cc5df4` |
| `worktree/scenes/body_proportions.py` | `c6f899328bb1ae97ca1dfdfc1ff59869980de2ef06ec3f178787e866959feaa3` |
| `worktree/scenes/relaxed_character_details.py` | `94abd29d8ff0f601d5b3e9bd83d064ef52cf52266f17cf82756da26dcff17a8a` |
| `outputs/sailor_character_proportions/references/character-reference.png` | `ea71fef894f068da0736a177ce4619ef176d0719581033cab8781b63f18e1139` |
| `outputs/sailor_character_realism_goal/candidate-10/portrait.png` | `8a312efd5f083cf04d3daddd9c18f893584b58faac8bdb8c13029ee6dfe65a09` |
| `outputs/sailor_character_realism_goal/candidate-10/profile.png` | `4c33b1807012a4284bcaea04863f3f77c6a4a0967bf457fa1a5b75939aa46046` |
| `outputs/sailor_character_realism_goal/candidate-10/face_oblique.png` | `48d051b2c71898d58a1e11249bba83de0bb1565468f6dd95113991c7fa9a4a9b` |

The candidate-10 blend identity `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41` is the frozen benchmark specified by the reviewed design and proposal; this review did not reopen or independently rehash that blend. The four inspected PNG hashes above were independently checked.

## Findings and required dispositions

### FACE-SRC-1 â€” Preserve the pre-smile neutral through the new cumulative field

Priority: P1, integration blocker if omitted; not a claim of evaluated failure. `face-form/coupled_probe.py:20-30` takes the current source after the production smile, and `:131-144` measures and exports only the added solve relative to that surface. Production applies the existing smile at `scenes/sailor_character_realistic.py:177`; `tools/verify_reference_smile.py:12-15` and `:50-55` explicitly require the accepted pre-smile neutral. The proposal's instruction to use the exact receipt arrays at `face-form/proposal.md:39` must therefore mean the added displacement applied once, not a replacement for cumulative neutral provenance.

Independent source replay finds 386 rows common to the old 516-row smile and new 512-row field. The complete cumulative before/after support has 642 rows. Using the true pre-smile source as neutral yields maximum paired scalar increase 56.33493525215709 micrometres and vector change 57.473002107100285 micrometres; the incremental figures are 20.686663272550827 and 21.12749576244002. Source rails use shared traced parameters and include internal depth, so these are a reason to evaluate, not the exterior aperture verdict.

Required disposition: independently reconstruct the complete no-reference-smile body through the same remaining pipeline; preserve its coordinates for all 642 cumulative changed rows, verify all other rows exact, and compare the final proposed stored/evaluated coordinates against that neutral. Keep the incremental measurement as a separate diagnostic. Do not reset the aperture allowance to the post-smile rest surface. Any replacement neutral must have an explicit physical justification and independent review rather than a convenient new hash.

### FACE-SRC-2 â€” The old mouth verifier is not a drop-in instrument for variable width

Priority: P1 before appearance rendering; not an objection to changing an implementation convention. The new oral rule changes X as well as height/depth at `face-form/coupled_probe.py:97-101`. The existing binder insists on 516 rows at `tools/verify_reference_smile.py:60`; the live verifier repeats that count at `:747` and requires every changed row's X to remain exact at `:753`. These checks will reject the new mechanism for an expected implementation reason. Suppressing them without checking downstream correspondence would not prove the retained physical requirement.

Required disposition: review the exact adapter or replacement instrument, including actual CC2 tracing, upper/lower and corner identity, complete changed-surface population, matching lateral domains under variable X, ambiguous/missing branches, and the same scalar/vertical strict less-than-50-micrometre criteria. It must fail or explicitly withhold a pass on unsupported cases, retain no-op and actual opening negative controls, and preserve source/float32/evaluated coordinate provenance. The current original gate's unchanged physical checks at `:954-972` are the reference requirement. This report approves no unseen runner, no bypass, and no automatic acceptance from a new source hash.

## Independently checked support and mathematics

Two pure-Python executions used Blender's already installed Python executable solely for existing NumPy. In-memory AST execution omitted the census/receipt output statements; no evidence files were overwritten, no subprocesses were launched by those scripts, and `bpy` was absent. The full native input digest and both complete control/coupled result dictionaries reproduced exactly, including every before/after changed coordinate. Both commands exited normally. The second execution independently recomputed source fans from world coordinates rather than reading the receipt's aggregate metrics.

The inverse-edge weights are positive and symmetric. The implemented energy is the unnormalised discrete squared Laplacian `||L d||^2`, with K = L-transpose L and fixed displacement constraints (`coupled_probe.py:68-76`, `:94-115`). The linear solve is coherent; measured residual is approximately 4.16e-17. This is a displacement fairing model, not nonlinear tissue elasticity, preservation of volume, or a maximum-principle interpolation. The proposal's validity text makes those limits explicit.

The nominal support includes components of 516, 10, 9 and 1 rows. All 512 actually changed rows and all 18 handle rows lie in the 516-row main component; the smaller islands are exact no-ops. Thus the operative deformation is connected, although the entire support mask is not literally one connected patch. This does not block the exact probe.

World-coordinate recomputation over all 1,208 affected source fan triangles gives minimum area ratio 0.77173219706974, minimum normal dot 0.9364753348339446, and maximum edge displacement gradient 0.2962458139500039, matching the receipt within arithmetic rounding. All changed coordinates are finite, and no helper/nonbody row changes. Maximum displacement is 1.8213762067902444 mm, at row 11929, with world delta approximately (+0.317407, -0.803687, +1.603356) mm. This exceeds the largest handle displacement because a biharmonic field can overshoot; the reported global 2.5 mm diagnostic bound covers this exact solve, not all future choices.

The extra four oral rings correct the support-clipping mechanism described in the retained failure. Freezing two edge layers at `coupled_probe.py:62-66` discourages a boundary ridge but is not a theorem of geometric tangent/curvature continuity. Positive source fan orientation and edge gradients do not establish nonintersection or smooth-looking final CC2 curvature. Actual evaluated geometry and profile/oblique pixels remain necessary. The source script records `source_guards_pass` at `:142`; exit code zero alone is not a safety pass.

## Pipeline and dependency coverage

Native-to-world conversion is coherent: `prepare_human_base.py:130-132` maps `(x,y,z)` to `(scale*x,-scale*z,scale*(y-ground))`; the proposed inverse displacement at `coupled_probe.py:117-119` maps world `(dx,dy,dz)` to native `(dx/scale,dz/scale,-dy/scale)`. Superior/anterior/lateral signs in the proposal agree with this mapping. Changed rows occupy world z=1.4612804216423902..1.5295993299813642 m. The subsequent body-proportion protection at `body_proportions.py:61` and the head-excluding pose at `sailor_character_realistic.py:200-213` / `relaxed_character_details.py:48-52` leave this region unchanged. The 1.65 m height scale therefore remains stable for this exact field.

The MHCLO parser's support includes every barycentric row and explicit scale endpoint used by production `fit_proxy` (`coupled_probe.py:38-57`; `prepare_human_base.py:95-115`). Independent calls to the actual production fitter before/after the received coordinates returned zero changed fitted vertices for the 1,064-vertex eye, 250-vertex eyelash and 124-vertex eyebrow assets. This is stronger than a source-mask claim for these exact asset mappings. It still does not prove that a newly shaped evaluated body preserves signed clearance to unchanged proxies. The final brow helper also depends on evaluated body fitting (`sailor_character_realistic.py:293-294`), and complete corneal shells/lashes plus affected body descendants must be checked in the actual probe.

The full native-to-world float32 round-trip error is at most approximately 0.060589 micrometres in this source replay. The runner must still use actual Blender-stored coordinates and modifier evaluation, not this estimate. Original garment fitting snapshots are captured before the smile (`sailor_character_realistic.py:169-180`), and the face proposal belongs after the current smile, without mutating those snapshots. That gives a coherent garment-isolation route; it is not proof of garment or groom clearance. Full hair support can depend on the body surface even when joints are exact, so complete emitted geometry remains a separate check.

## Cumulative shape and visual interpretation

I inspected the 1713 x 918 reference and three native 1200 x 1200 candidate-10 facial views. The candidate has a broad smooth cheek surface beside a more explicitly curved mouth, while the reference has a subtler linked mouth/cheek response. A connected three-dimensional cheek experiment is a defensible hypothesis. The reference also differs in skin response, camera and lighting; neither those images nor the handle vectors prove that adding lift will improve appeal.

This solve adds to existing edits. Of its 512 changed rows, 473 already participate in natural_expression, 40 in gentle_expression, 128 in lower_cheek, 352 in perioral, and 386 in reference_smile. The source census showing zero reference_smile motion in the midcheek box does not mean that region is unshaped: natural_expression and gentle_expression already affect it. Cumulative lift, cheek fullness and mouth stretch are the practical appearance risks.

The proposal correctly discloses that malar handles land about 13 mm lateral to the requested centre and mouth-side handles about 7 mm below their requested height (`proposal.md:23`). This exact experiment primarily tests lateral-cheek and mouth-side coordination, not an established central malar or under-eye solution. Inspect for lateral pillow-like swelling, nasolabial ridges/hollows, more protrusive lips/profile, exaggerated corner stretch and a younger-looking face. Do not call an unchanged or merely smoother-looking face successful. If this placement fails visually, another amplitude sweep would not resolve the stated anatomical-placement question.

## Conditions for proceeding

1. Freeze and match the exact source/asset/receipt inputs, then apply the received native field once to the full reconstructed current body at the intended post-smile stage. A mismatch is a stop, not an opportunity to transplant by row number blindly.
2. Resolve FACE-SRC-1 with independently verified cumulative neutral/proposed coordinates and FACE-SRC-2 with review of the exact runner. Keep the actual strict 50 micrometre mouth and eye/lash bounds; source gaps and frozen support masks are not replacements.
3. On actual Blender-stored final geometry, check all affected source and CC2 surfaces, complete corneal/lash geometry, protected body and independent garment coordinates, and the complete groom/physical clearance requirements from the round-3 design. No sampled-only groom result or unchanged metadata can stand in for that population.
4. If all required physical gates and instrument controls pass, one unchanged six-view native 128-sample OptiX appearance experiment is justified. Root and independent native-view judgment must decide whether it materially improves the adult face. Keep the candidate-10 benchmark immutable and report any remaining face/hair gap.

## Review limits and resource disposition

No appearance candidate was generated. No actual evaluated aperture, eye/lash distance, self-intersection, body/garment clearance, or emitted groom test was run. The original verifier and source pipeline were inspected, but this was not a complete audit of every existing safety instrument. The retained failure files were acknowledged from the proposal; their replay was not independently executed. The repository's requested `docs/learning/lessons.md` is absent in this worktree; relevant `docs/learning/gate-proofs.md` evidence was read instead.

Only this authored report was written. All pure-Python commands terminated; this review created no browser, server, Blender, GPU or GUI process and has no task-owned process left running. Production source, retained proposal/receipt bytes, benchmark renders and concurrent work were untouched.

## Findings and disposition

Source hypothesis is coherent for an evaluated diagnostic. Cumulative neutral and variable-X aperture instrumentation must be verified before any render. Actual probe subsequently confirms exact input coordinates and ocular limits, but the new aperture instrument is not accepted.

FACE-SRC-1 and FACE-SRC-2 remain explicit conditions; review28 preserves the instrument findings.

## Verification

Root's actual diagnostic matches all 512 proposed baseline rows and 1,269 ocular/proxy guard rows exactly. It uses the original saved pre-smile contract and 642 cumulative changed rows. Actual eye penetration increase is zero and lash separation increase is 25.404 micrometres, within the unchanged 50 micrometre bound; real mouth, eye and lash negatives are detected. The aperture result and structure assertion remain unaccepted for the reasons above. PID 27064 closes after 15.639 seconds; original scene data, contract, input file and temporary data blocks are restored or cleaned. No saved candidate or render is produced.

## Round outcome

Source hypothesis is coherent for an evaluated diagnostic. Cumulative neutral and variable-X aperture instrumentation must be verified before any render. Actual probe subsequently confirms exact input coordinates and ocular limits, but the new aperture instrument is not accepted. Round 3 remains zero of ten integrated attempts used. All evidence is diagnostic; no production change is accepted by this record.

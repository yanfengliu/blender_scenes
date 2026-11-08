# Review 6: implementation

## Target

Repository: blender_scenes. Base revision: ade40140278b6bd7fd060ccac3dfb0692cb43748. This round records the independent design and source review of the candidate 5 garment drift, the bounded source repair, and the first saved-garment checker before its two review fixes. It does not grant final visual, runtime or Git-delivery acceptance.

The adopted candidate 5 main source is retained at outputs/candidate5-recovery-20261107/baseline/scenes/sailor_character_realistic.py, SHA256 596ad5820ad8e372d221a2ccc5d26754fe23c05e591cf488964a638f0f74694f. The inspected dependencies include fitted_blouse.py (74d97092ae59cb4683d61aaf13f8be3c6917a5f1063c6dda0423e4f6139ef26c), body_proportions.py (2edad88b5a38e36b97e87e87db1ecf4cb32a8c5f0699982cf9b6c5dcbc451743), reference_smile.py (62fa4f32c9cae2fae087194b52a294c6eacede1c49f910fbd207d6246a307362), and fitted_body_clearance.py (df6d3bbed4abd633dbbcb67111d2e36ff761d39356294c3e9bb3ba82e8a0f8c5). The frozen candidate 5 source and recovery baseline retain these inputs.

The repaired main source has SHA256 9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b. Its exact bytes are retained in outputs/candidate5-recovery-20261107/review-targets/scenes/sailor_character_realistic.py and outputs/sailor_character_realism_goal/candidate-6/source/scenes/sailor_character_realistic.py. The initially reviewed checker has SHA256 e37d11528fd81ed1ce28963bc8cdf2ddb66c0ed51f829b46fbb2131f7293cc38 and is retained as outputs/candidate5-recovery-20261107/review-targets/checker-before-review-fixes.py. The latter was recovered and its digest independently checked before writing this record; later fixed bytes do not replace this original review target.

The retained final implementation patch is outputs/candidate5-recovery-20261107/review-targets/implementation.patch, SHA256 7acf07e3b55be1e2897fe7cb4cd225cc54b244e82c0adbd991ef454be370f5c6. The same directory's manifest.json has SHA256 948e58bb7147d22e4cd46c3eb36368f58cebd04a56b80916a1e79a397f4bc39f and identifies the final main and both maintained checkers. It supplies the later repair target, while the separate original-checker file preserves the earlier findings.

## Reviewers and coverage

The independent garment design reviewer read the exact scene orchestration, blouse preparation and fitting, body proportions, collar derivation, pose, expression helper, existing saved-fit probe, preservation checker and diagnostic evidence. This was read-only investigation and source review: the reviewer did not launch Blender, render, browse, delegate or edit implementation. Root owned implementation and causal/runtime checks. The garment regression worker implemented the maintained saved checker. The following reports preserve the reviewer's substantive conclusions at their original stages, including the originally pending and failed evidence.

## Reports

### Independent garment design reviewer

**Initial design and causal-evidence report.** Recommend a separate garment fitting anatomy snapshot, captured after perioral shaping and before apply_reference_smile. In the adopted sailor_character_realistic.py at lines 168-169, copy the native vertex rows after apply_perioral_shape. Apply the same proportions and pose to that independent copy, then pass it to garment preparation and full_body_support. Keep the current smiled anatomy for visible skin, proxies, smile binding and final validation.

Do not reuse skin_reference_native. Its capture at line 166 precedes the retained perioral deformation, so it is not candidate 4's anatomical input. The snapshot must receive its own proportions_baseline_vertices; body_proportions.py at lines 56 and 134 already creates independent rows when apply_body_proportions is called separately. Sharing unchanged topology and groups is reasonable; sharing mutable vertex rows is not. Use the same pose only with assertions that scale and pose-driving joint coordinates remain identical.

Keep the current fitting algorithm. fitted_blouse.py at line 260 constructs a whole-body BVH; lines 266-270 use a returned face normal to displace neckline controls. A distant expression change can therefore expose tie-selection sensitivity even when nearby support coordinates are unchanged. Deterministic tie-breaking would choose a new policy, without guaranteeing candidate 4's exact choices. Moving the smile after garment construction would disturb more of the established build order and expression consumers.

The saved diagnosis reports three changed blouse rows, maximum displacement 0.184754 mm, followed by 618 changed collar rows and 437 changed collar-distance attributes. This propagation matches fitted_collar.py at line 145: the collar derives from the evaluated blouse and its normals. The existing preservation failure should remain authoritative until a new saved candidate passes.

The v2 probe is well targeted: it checks complete neutral-body reproduction, identical prepared and posed garment inputs, unchanged local support faces, witness-query predictions, and an exact full blouse/collar reconstruction. At the time of this initial report, no neutral-clothing-support-v2.json receipt existed. The existing neutral-clothing-support.json recorded the earlier .edge_verts / INT32_2D instrument failure. Thus the v2 script supported the proposed experiment, not a successful causal conclusion. This historical qualification is retained rather than rewritten using later success.

Recommended regression and acceptance checks:

- Whole-class isolation: exercise neutral, current smile and an additional bounded remote-face perturbation through the production fitting path. Require exact fitted blouse and derived collar geometry, attributes, modifiers, materials and settings. Include a relevant torso or pose change as a positive control so the check cannot pass by freezing all garment inputs.
- Saved-scene preservation: retain the strict comparison to frozen candidate 4, allowing only the factual smile contract and its specified body-coordinate changes. Require restored garments to equal candidate 4 and final smile coordinates and contract to equal candidate 5. Do not exclude collar attributes or introduce a numerical garment tolerance.
- Actual-body fit: validate against canonical unculled faces reconstructed from the final saved smiled body's 19,158 coordinates, with matching Subsurf2. Check complete inner/outer/rim triangle overlaps and signed samples, retaining the existing 0.2 mm build clearance requirement and sign/intrusion controls.
- No repair during acceptance: fit_evaluated_blouse mutates controls at fitted_body_clearance.py lines 168-180. Calling it against the actual smiled body as a check can silently change the garments again. Use a read-only measurement path or explicitly prohibit corrections and prove coordinates unchanged.
- Visual acceptance: inspect the new saved result at full resolution in hero, portrait, profile, back and oblique views. Exact preservation plus fit measurements does not itself certify collar appearance or the retained smile.

check_realistic_character.py alone is insufficient for complete garment clearance: its geometry checks at lines 418-435 cover neck boundaries, hair, ears and sock cuffs, not complete blouse/body clearance. This initial report was read-only design/code review; no tests or visual acceptance were performed.

**Exact repaired-main source report.** No blocking code findings in sailor_character_realistic.py, SHA256 9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b. Lines 168-176 capture independent vertex rows at the correct post-perioral, pre-smile boundary and apply proportions separately. Lines 183-185 verify equal height and every pose-driving joint helper, supporting reuse of the existing pose. Line 216 computes the separate posed fitting anatomy. Lines 309-310 consistently route both blouse preparation and anatomical support through that reference. Visible skin, proxies, skin-reference data and factual smile binding retain their existing inputs and ordering.

At that review stage, the new causal receipt supported the diagnosis: all three query witnesses reproduced the saved candidate 4/5 differences despite unchanged local support coordinates. It reported exact rebuilt blouse state; the collar differed only in captured dimensions. Updating the dependency graph before measurement was appropriate, and retaining the dimensions comparison preserved the check. This was source approval for the bounded change, not runtime acceptance. The refreshed causal receipt, saved-scene preservation, read-only actual-body clearance, regression controls and visual review remained outstanding at that stage.

**Original saved-checker report.** Found two false-pass risks in check_garment_isolation.py, SHA256 e37d11528fd81ed1ce28963bc8cdf2ddb66c0ed51f829b46fbb2131f7293cc38:

- F9 / GI-R1, P2: subdivision creases are omitted. body_snapshot at lines 130-135 ignores body attributes, while clearance at lines 244-250 reconstructs an attribute-free mesh. Changed crease_edge or crease_vert data could alter the actual Subsurf2 body without changing the fingerprint or measured reconstruction. For this bounded scene, reject crease attributes; otherwise verify and map them onto complete topology.
- F10 / GI-R2, P2: metre scale is unverified. measure at lines 212-225 treats raw coordinates as metres. Require scene.unit_settings.scale_length == 1 before enforcing the 0.2 mm physical gap.

The remaining design is sound for the frozen scene. Procedural material graphs use a restrictive supported-node list. Garment fingerprints cover source geometry, UVs, attributes, materials, transforms and modifiers. Face-cycle and rim counters prove complete shell coverage; labels agree with the known positive-thickness baseline. Candidate 5 must expose coordinate drift in both garments. The actual-body intrusion control requires both negative gaps and overlaps, then restores every source coordinate exactly.

Minor hardening suggestion, not a blocking finding: reject empty attribute-value snapshots so an unsupported future RNA value cannot silently hash as an empty object.

By the end of the original checker review, the refreshed causal receipt reported exact blouse and collar reconstruction, including dimensions. The reviewer ran no Blender processes or tests and made no implementation edits. The two checker findings remained pending fixes and re-review.

## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F8 | Remote expression changes the whole-body BVH's tied normal choice and consequently unrelated garment geometry. | Root accepted the separate post-perioral, pre-smile anatomy boundary; the reviewer found no blocking issue in the exact implementation. Runtime and visual acceptance were still separate. | Main SHA256 9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b; saved and production regression plus integration review in round 7. |
| F9 | GI-R1: actual-body reconstruction omits subdivision crease attributes. | Root accepted the finding and chose a bounded fail-closed contract instead of topology mapping. The original finding remains retained above. | Reject body crease attributes and other unsupported body geometry state; exact fix reviewed in round 7. |
| F10 | GI-R2: raw coordinates are labelled metres without verifying scene unit scale. | Root accepted the finding and chose the existing fixed-metre contract. The original finding remains retained above. | Require scale_length == 1 before clearance; exact fix reviewed in round 7. |

These root dispositions were supplied by the integration owner and are attributed here; they do not replace the independently authored reports. F0-F7 and their earlier rounds remain historical records.

## Verification

The reviewer read source and retained JSON receipts, compared the repaired main against the adopted candidate 5 source, and checked exact file digests. No reviewer-run runtime test, Blender process or visual review belongs to this implementation round. The final causal receipt at outputs/candidate5-recovery-20261107/neutral-clothing-support-v2.json confirms all three original query witnesses, unchanged queried support coordinates, exact neutral-supported blouse and collar reconstruction, the unchanged smiled skin, restored loaded state and unchanged saved inputs. Earlier instrument failure and stale-dimensions failure remain historical evidence, not successful checks.

The preserved original checker digest, final three-file manifest and implementation patch were independently rechecked while writing this record. Later integration results and fixes are recorded in the next round rather than retroactively replacing this round's qualifications.

## Round outcome

The separate garment-reference mechanism and exact repaired main are accepted at source level. The original checker requires F9 and F10 to be fixed before its physical-clearance report can support acceptance. Whole-scene preservation, actual-body verification, nonvacuous production controls and native visual inspection remain the required integration evidence. Full photographic likeness and Git delivery are not accepted by this round.

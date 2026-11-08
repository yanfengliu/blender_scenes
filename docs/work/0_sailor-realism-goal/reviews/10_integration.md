# Review 10: integration

## Target

Candidate 9, based on `2e95c6b0a1655ca2e6c4f067348bcdbbdaa231c1`. Its exact 27-file source is retained under primary-checkout `outputs/sailor_character_realism_goal/candidate-9/source/`, with `source-manifest.json` SHA-256 `87a9e784ab628135e7685d937baa7309f42bb7588fc952c46cc97cdb4e47cbd6`. I recomputed all 27 hashes and matched that manifest. Later live worktree changes are outside this rendered target.

| Key candidate 9 source | SHA-256 |
|---|---|
| `scenes/sailor_character_realistic.py` | `2de68d224f73406bcef88a43e628a1bdd0ac4e64f145dd4b6b2949228f7afebe` |
| `scenes/perioral_shape.py` | `ebaa220c50afd6a32cc691a054ab21338a80300910b72924cde39fdb169c026a` |
| `scenes/natural_face.py` | `a740665defcb771dc141b41bc41817ad1616e61752cdb9a34c6121e52f5bf611` |
| `scenes/natural_hair.py` | `bfdccc3dc53122726cdef40c2afa3e6064cfc128a0065da2f3e52dafea012027` |
| `scenes/hair_groom.py` | `7692e2d304da5409dd681684cb8d0a59e3c4e24bb9bbe7be5a5736458ce55e74` |
| `tools/check_expression_fit.py` | `9cd803f49aa0202fcbd85852694e7d5527bd0f16736517b1064b57f82cf3bd92` |
| `tools/check_realistic_character.py` | `1a0e8b99b78b5c61f6a53a24f57a49806d9281bd3396ab5f4bcaa44f1ce3196c` |

I separately reviewed the maintained pure-Python verification source `tools/check_lip_contour.py` in the isolated worktree, SHA-256 `d842612089683b968a157d5397ce9f2d5751e3fe95a89dc4cae9182b049b8cba`. It is not one of the 27 candidate 9 render inputs. The read receipt `outputs/search-shape/maintained-lip-regression-final.json` pins that exact checker and the candidate 9 source hashes. Root owns preserving the supplemental checker/evidence and binding reviewed code to a recoverable delivered revision before cleanup.

| Candidate 9 artifact | SHA-256 |
|---|---|
| `hero.png` | `8eeaea6c766803ad13deca3bc518cef614e5f8cf22e0ea2e394a116482c98868` |
| `portrait.png` | `7977a3322592cdd44e81fe18546eb163c3f2fd0102c1242bfb2c788e61f23081` |
| `profile.png` | `51014d119727eb971b7dadd702695d766e9bf76d6cb8d461b277e16e170de7cf` |
| `back.png` | `920fa992403a559233b7808b18aafb8996213eb07113002eb93fc10d9c08edd2` |
| `face_oblique.png` | `3b9cbea14f8812868f906fe78376cfbfedb90634a5eedf9e9e7651cb90cbe54a` |
| `torso_random.png` | `0d5cd2db24af632dc4aca331f3febd4c7c0f7d952670f980b9905cbffb332f47` |
| `sailor_character.blend` | `8d29b5511d52ee8fdef5de254bde57a356f207b8755ebb27fe1aa0b95cca59d1` |

The comparison references remain the frozen adult-20 character and body turnaround recorded with their exact hashes in round 8. Candidate 8 is the immediately preceding rendered control, recorded in round 9. I read the fixed benchmark and disqualifiers in this work unit's `design.md` before judging candidate 9.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I inspected the frozen candidate 9 changes against candidate 8, the supplemental maintained lip regression, the independent branch report and runnable lower-lip probe, and the input/geometry receipts described below. I inspected hero, portrait, profile, back, opposite oblique and seeded torso at native resolution through `view_image` with original detail, then hashed all six renders and the saved blend. I ran no Blender process, build, runtime regression or independent source probe, and changed only this authored report. Root owns runtime gates, rendering, process cleanup and final status.

## Reports

### Independent Codex reviewer

I reject candidate 9 as the completed response to the user's three appearance objections. The upper-body width objection is materially addressed: the shoulder silhouette is narrower and the fuller-bust/slim-waist intent is retained in the hero and seeded torso. The face remains insufficiently natural and appealing against the adult reference. Hair coverage is improved relative to candidate 6, but the groom remains visibly artificial and the opposite oblique exposes a long scalp wedge between the fringe and side lock. The latter is a decisive remaining defect, not an issue hidden by passing frontal coverage numbers.

The frontal fringe no longer has candidate 8's equal repeated triangular teeth. That is a bounded improvement. In the portrait and hero, however, it returns toward a dense, nearly horizontal curtain. The temples form conspicuous outward bulges, and the profile shows a strong horizontal ridge or band near ear height, a thin exposed side separation, and sparse windows among the lower ends. The oblique makes the separation unambiguous: a long straight skin-colored wedge runs from the upper scalp down to the outer forehead between two dense hair populations. This differs from the reference's small, softly interleaved gaps and natural transitions. F12 therefore remains open, including the user's sparse/balding concern at that oblique seam.

The hair source replaces the repeated-frequency tip field with explicit unequal smooth groups shared by tip height and lateral flow. `_group_values` gives continuous interpolation between the declared ordered groups; the small flow offsets preserve ordering for these controls. The fall groups vary scalp exit elevation and side transitions without increasing strand count or adding a flat cap. This is a reasonable mechanism change, but it does not earn acceptance: the actual profile still has a strong band and the oblique has a scalp gap. The frontal crown guard measures only a central 16 mm window at three heights. The fringe guard measures three frontal scanlines and shaft retention. Those guards accurately describe their limited coverage and do not test this off-center oblique transition. Their thresholds were not weakened; their pass cannot rebut the rendered F12 finding.

The lip geometry changes are bounded and reviewable. The upper crest uses the existing sparse anatomical target and depth taper for a further 1.2 mm downward component while retaining the 2 mm retraction. The new lower field lifts by at most 0.8 mm and retracts by at most 0.4 mm. It derives a contact envelope from the complete traced lower rail, restricts the field to a small front lower-vermilion box, protects the complete 76-row oral strip and non-body/helper groups, and requires the raw field to be zero on the oral rows before explicit pinning. It keeps all X coordinates unchanged, checks source triangle orientation/area, and rejects excessive adjacent displacement gradients. These properties are more meaningful than merely retaining a list of pinned vertices while applying a nonzero field across the boundary.

The maintained `check_lip_contour.py` is nonvacuous within its declared source-geometry scope. It executes the production pre-perioral AST and actual perioral call. Its former-mechanism control removes exactly the new upper vertical term and lower helper from the current source, requiring exactly one match for each transformation. The actual contour must satisfy bounded upper/lower heights and lower projection; the former control must fail. It independently recomputes the full oral Y/Z invariant, the retained X-width map, protected helper/ocular rows, allowed anatomical support, combined displacement and affected triangle fans. Its receipt binds the checked production inputs and checker hashes, and it asserts that Blender was not imported. I found no blocking defect in this verifier.

The independent branch's frozen-8 comparison and the maintained check use different baselines. The branch probe reconstructs the former candidate 8 chain and checks all 76 complete oral coordinates before and after the reference smile, then compares combined changed fans against that chain. The maintained check compares the complete current perioral stage against its pre-perioral input, so its 0.576954 minimum fan area ratio is not interchangeable with the design note's approximately 0.6484 comparison against candidate 8. I read the branch harness and report, but did not rerun them or personally obtain a separate raw 0.6484 receipt. The maintained receipt supplies directly read production evidence with its own clearly stated baseline.

The revised smile input is explicitly pinned to `f5ca919d4a0c29a83f15ecaa4ebac925bc04bd1df5552c514148445e2033a914` in both the main and canonical checker. I read the independent construction code and receipt comparing all 514 neutral/proposed changed-row coordinates with separate production anatomy. The 514-row population and live 50 micrometre evaluated mouth-aperture contract remain unchanged from candidate 8. This is a new anatomical input pin, not a relaxed aperture limit. The upper-frame source and the final shared body/clothing deformation are byte-identical to candidate 8; the new collar regression from candidate 7 has not visibly returned.

F13 remains open despite the valid lip mechanism. The lips look somewhat quieter, but the face still reads as smooth and mannequin-like in the portrait and oblique, with prominent pale lip contours and broad, comparatively flat lower-cheek planes. The reference has softer transitions and more coherent facial form/surface detail. The material change reduces the rose multiplier and restores some specular response; the rendered result does not establish the requested natural appeal. Further eye enlargement or skull shortening would not address the dominant remaining relationship between cheek planes, lip contours and rigid hair framing. The adult age/skull intent remains intact, and the current eyes are not a reason to pursue a more juvenile face.

F14 is fixed in the frozen source: `check_expression_fit.production_blocks` now explicitly requires `collar < finish`, so the harness cannot silently reorder an earlier final stage past garment construction. The production-stage and remote-expression control mechanisms otherwise retain the reviewed behavior.

F15 is a minor diagnostic clarity issue. `apply_perioral_shape` computes its top-level `changed_vertices`, fan counts and upper-stage support diagnostics before calling `_thin_lower_lip`; the new lower-stage report is nested separately. Those top-level fields should not be presented as aggregate statistics for the whole now-combined function. The maintained verifier correctly computes the combined result: 445 changed rows and 984 affected triangles, rather than the earlier stage's 442/980 figures. This does not invalidate the geometry checks or cause the rendered appearance failure, but explicit stage labels or aggregate metrics would prevent later status reports from understating the changed population.

## Findings and disposition

Earlier authored reports remain retained. These are this reviewer's observed dispositions for candidate 9; root owns subsequent fixes and delivery status.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F11 | Candidate 7's collar/stripe step regression. | Does not visibly recur in candidate 9 canonical or held-out views; frame mechanism unchanged from 8. | Final retained scene still needs actual evaluated garment/accessory checks. |
| F12 | Hair has unnatural fringe/side flow and exposed scalp gaps. | Equal scallops reduced; dense curtain, temple bulges, profile band and long oblique scalp wedge remain. Final appearance rejected. | Address the actual fringe-to-side transition and inspect all six views; central scanline passes are insufficient. |
| F13 | Face does not meet the requested soft natural adult appeal. | Bounded lip change is valid but rendered improvement remains insufficient. | Keep adult proportions; judge any final form/surface adjustment by native reference comparison. |
| F14 | Production AST ordering omits the final-stage relation. | Fixed in frozen candidate 9 by `collar < finish`. | No further action for this finding. |
| F15 | Top-level perioral diagnostics remain upper-stage figures after the lower stage is added. | Minor reporting issue; maintained verifier provides true combined evidence. | Label stage-specific values or add explicit aggregate metrics; do not report 442/980 as the combined count. |

## Verification

Reviewer content checks: all 27 frozen source hashes matched the manifest; the supplemental checker hash matched its receipt; all six native images were inspected and hashed; the saved blend was hashed. No runtime check was run by this reviewer. Image judgment is based on the actual candidate 9 pixels, not inferred from source metrics.

I read `candidate9-input-preflight.json` under primary `outputs/character-naturalness-20261107/`: 514 independently constructed neutral rows and 514 proposed rows match the new pin; source shoulder ratio remains 0.89763 and upper/lower lid responses remain about 0.962/0.708 mm. I read candidate 9 `reference-smile-gate.json` top-level status, pin and failure count: `pass; live evaluated geometry and controls, within stated bounds`, the `f5ca919d...` pin above, and zero listed failures. I did not audit every large witness array or rerun the gate.

I read isolated `outputs/search-shape/maintained-lip-regression-final.json`: PASS; former contour rejected; upper/lower source heights 6.104034/6.659788 mm and lower projection 2.206724 mm; 445 combined changed rows; all 76 oral Y/Z rows and 5,788 protected rows exact; maximum combined displacement 2.332381 mm; 984 affected source triangles; minimum fan area ratio 0.576954 and normal dot 0.855480. These source checks do not prove subdivided lip closure, surface appearance or likeness. The separately read live smile receipt addresses its own evaluated aperture bounds.

Root retains ownership of complete saved-scene body/garment/accessory verification and any remaining gates. This review does not assert unobserved candidate 9 saved-clearance results, a new runtime test run, or completion of the user's appearance goal.

## Round outcome

Candidate 9 is rejected as the finished appearance result. Of the user's three objections, the narrower upper body is materially addressed, while natural hair and facial appeal remain unresolved. F14 is fixed; F15 is a minor diagnostic issue rather than an acceptance blocker. The ninth integrated candidate has been inspected in all six supplied views. Only candidate 10 remains within the stated budget, and this report does not authorize further attempts or pre-accept a later result.

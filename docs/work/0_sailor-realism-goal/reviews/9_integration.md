# Review 9: integration

## Target

Candidate 8, based on `2e95c6b0a1655ca2e6c4f067348bcdbbdaa231c1`, with exact source retained under primary-checkout `outputs/sailor_character_realism_goal/candidate-8/source/`. The 27-file `source-manifest.json` has SHA-256 `76a3a1d102987f97bd0d400707d2ce6e4bf1a5545aeb2ca055597e2180382a85`; I recomputed and matched all 27 hashes. This is the frozen built input, not later live worktree edits. Root owns preserving the source patch and binding the final reviewed implementation to a recoverable commit.

| Key reviewed source | SHA-256 |
|---|---|
| `scenes/sailor_character_realistic.py` | `f753723a2ac95174e549cd450856fcb2a812549af0de0ad6d8913a3eb00f1ae3` |
| `scenes/upper_frame.py` | `605255433687d05ec556c5dc1a9c8a61b494add54f5bfc6af0ad2935d5bdb945` |
| `scenes/natural_hair.py` | `41393913089633384e706e3b52299ba614a90b8d7765b155c8348e6bb3af41cf` |
| `scenes/hair_groom.py` | `0afe1e7a62e1be7c91d62cb5010449d642becdd878a3cb8cf3228d8f6f2c56b3` |
| `scenes/perioral_shape.py` | `247598ac592f3ededd41b8c21cfe67b1124ef0e2b3f3d6e0d3860eba00a8e188` |
| `scenes/reference_smile.py` | `7b9fd9be113ec09feaff0a5d7d20ca71c54ce68a3554c91ee12e2410eb868b96` |
| `tools/check_character_shape.py` | `7c2a0f61db34606340ae1ff44898a3a339d76713eb194b33e5c49e0559e314f2` |
| `tools/check_expression_fit.py` | `3c0fb304f31a874ed5aa275a55a8e604287d7a2ba077a3fb00624fb808f12dca` |
| `tools/check_realistic_character.py` | `e0fdc352214a108ec2f37a05b5da97f60d3734452ec339229a2f38a658c9d5a6` |
| `tools/verify_reference_smile.py` | `eb4a0cede5ddb3f8ee87b061bfe8f41cbccca52628f0af25c2480fe29ae3351a` |

| Candidate 8 artifact | SHA-256 |
|---|---|
| `hero.png` | `cddadbd691976e9d9e2144a142f0d7e5531117d25f8c41de12df01d41f4bcea9` |
| `portrait.png` | `f72e5c6355ce40e951cc58ccefa2b55843d18d1e6fe050a3ae528809d2255803` |
| `profile.png` | `1e8df138752a8be9a7be5184604927668b55cb330cea7c3d33ee6f90faab55b2` |
| `back.png` | `969af932f3d62a6645f21bc8ba782063f3f83904a21b7d9324e9f3d748722a4b` |
| `sailor_character.blend` | `4d41c0cb821a366ee838a279b08c5460bfd5be63a396d3667eab34d6a0485f72` |

The visual comparisons are the exact candidate 7 images and original adult reference images recorded in round 8, plus candidate 6 reviewed earlier in this continuation. This report preserves both the source review and the subsequent four-view judgment in one actual integration round.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the frozen candidate 8 changes against frozen candidate 7, including final upper-frame deformation, facial targets, perioral and smile bounds, revised input pin, production AST regressions, signed scalp-guide flow, fringe tip field and crown coverage check. I inspected all four candidate 8 images through `view_image` at original detail and checked their hashes. I read the completed source-shape and smile receipts described below. I did not launch Blender, build a candidate, run runtime checks, edit scene source or inspect a candidate 8 oblique/random view. This report is reviewer-authored; root owns subsequent dispositions and overall delivery status.

## Reports

### Independent Codex reviewer

I found no blocking code defect in the frozen candidate 8 changes, but I reject this candidate as the finished appearance result. It improves candidate 7: the obvious crown cleft disappears, the pronounced collar shoulder steps are substantially smoothed, and the eyes are visibly more open. The narrower shoulders and fuller-bust/slim-waist direction remain. The remaining hair edge and facial appearance still fail the user's request.

The final upper-frame stage is a coherent response to F11. The main now constructs the body, blouse, collar and clothing details using the existing pose and fitting inputs, then calls `finalize_upper_frame([body, *clothing.all_objects])` at line 399. The function transforms mesh controls and curve controls/handles in world coordinates, rejects shared geometry data, and returns unchanged controls without a needless coordinate round trip. This applies the same smooth map to already constructed surfaces instead of asking the collar builder to reconstruct its boundary from the narrowed helper. Forward depth and the protected waist/head regions remain unchanged by the field. The narrowed silhouette is retained in the hero view. In the portrait and profile the conspicuous extra corner from candidate 7 is removed; the collar still has its intentional change from the shoulder edge into the front V. I consider the specific visible F11 regression repaired in these views, subject to root's final evaluated garment and accessory support checks.

A shared source-control map is not proof of preserved evaluated clearance. Subdivision evaluates after the mesh edit, solidify follows changed normals, and curve cross-sections are not themselves transformed point by point. The source docstring accurately leaves clearance and appearance unproved. Final acceptance still needs the actual complete body against the final inner/outer garment shells and rims, plus the retained pocket and ornament support checks. The expression regression exercises the final stage for its blouse/collar fingerprints, but deliberately does not build all clothing details or claim those support checks.

The face revision is deliberate rather than an unreviewed change of a frozen smile contract. The main uses eye-height targets 0.60, nose horizontal reduction 0.30 and upper-lip volume 0.18. Perioral contact widening is reduced from 8% to 2%; the corner lift is reduced from 1.5 to 1.0 mm, with the source displacement cap tightened accordingly. The existing 6–9 mm pre-retraction crest guard remains. Because the anatomy changes, the current smile has 514 changed rows instead of 522. Both bind and verification checks now require 514; the main and canonical checker pin `006ab241260745ff5a88cc3b37bfdb82d3a6c6d00ff753a4c49fedc45159e105`. The old candidate's source and contract remain recoverable in its frozen evidence.

`check_character_shape.check_smile_input` independently executes the production anatomy with the smile disabled, then compares every bound neutral coordinate with that separate construction and every proposed coordinate with the final mapped body. It also requires the new digest to equal the explicit pin. This is a meaningful consistency check instead of accepting an arbitrary new count. The changed rows are above the final frame field, so using the retained pose for their binding is consistent with the actual final coordinates. The live aperture, surface orientation/intersection and negative-control logic is unchanged apart from the expected row count; the 50 micrometre evaluated aperture limit has not been relaxed. The character's adult age and skull/height intent remain retained.

The production shape regression now constructs a temporary mesh and executes the actual final-stage AST before reading its coordinates. Its no-frame and old-eye controls remain nonvacuous. The expression regression likewise compares final mapped body coordinates and complete blouse/collar fingerprints, preserving the remote-face and relevant-torso controls. F14 is a minor test robustness gap: `production_blocks` discovers the final-stage node at line 43, but line 44's order assertion stops at `collar` and does not require `collar < finish`. The current production source has the correct order. Adding that relation when next editing the test would prevent a future misplaced final stage from being silently reordered by the harness. This is not a current scene defect or a reason to rebuild otherwise identical candidate 8 pixels.

The hair code removes the independent outward root offset and rotates the signed scalp direction rather than reflecting each half away from the midline. Both central populations therefore share a scalp corridor. The new crown check samples actual foreground strand intervals in a central 16 mm window at three levels and requires every measured gap below 2 mm. Its claim explicitly excludes continuous scalp coverage and aesthetic acceptance. The existing fringe check supplies the current curve/material/scale prerequisites before crown checking. The tip field and comb field use coordinated phases, and the ordered comb avoids collapsing entire intervals onto one guide. I found no new code blocker in those bounded mechanics.

F12 remains open as an appearance problem. The portrait confirms that the exposed central crown cleft is gone, and the back no longer shows the earlier skin-colored split. However, the new fringe has several repeated deep scallops or triangular teeth along its lower edge. That periodic pattern reads as a deliberately cut graphic shape rather than soft irregular locks. It is visible even at hero scale. The profile remains a near-solid straight curtain with an ear-height change of flow and sparse windows among the lower ends. The 12 mm coherent tip-height variation is consistent with the visible scallops; actual rendered review is the evidence for the finding. Further work should soften that repeated pattern and improve side flow while retaining coverage, rather than raising strand count or reopening a broad transparent forehead.

F13 also remains open. The more open eyes are an improvement and do not appear childlike, but the face still reads as smooth and mannequin-like, with prominent pale lip contours and limited visible cheek participation. The profile continues to show a projecting lip outline. The requested soft natural facial appeal is not established by the increased eyelid measurements or revised smile pin. I would not keep enlarging the eyes as the next response: the remaining form, surface and hair-framing relationship is more significant. The adult reference remains the visual target, not a numeric facial proportion or an exaggerated youthful style.

## Findings and disposition

Earlier findings and authored reports remain unchanged. The following are this reviewer's observed dispositions for candidate 8, with final integration status owned by root.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F11 | Candidate 7's added shoulder turns kink the collar and stripes. | Specific pronounced step visually repaired in candidate 8 portrait/profile; no general garment-clearance claim follows. | Root verifies final evaluated shell and accessory support. |
| F12 | Hair lacks natural fringe/crown/side flow. | Crown cleft repaired; repeated scalloped fringe and stiff side curtain remain. Final appearance rejected. | Retain coverage, soften periodic tip pattern and side flow; inspect actual native views. |
| F13 | Facial changes are insufficient for the requested natural adult appearance. | Eyes improve; overall face still not accepted. | Refine remaining facial form/surface relationships without repeated eye enlargement or another additive smile layer. |
| F14 | Production AST order assertion omits `collar < finish`. | Minor test robustness observation; current source order is correct, so not a current build blocker. | Add the relation with the next test edit; preserve existing negative controls. |

## Verification

I verified all 27 frozen source hashes and hashed the saved blend and four images. All four images were inspected at native resolution. I compared the frozen code changes and did not run tests or Blender. No oblique/random view was inspected for this candidate; fixed views already establish rejection.

I read root's `outputs/character-naturalness-20261107/shape-preflight8.json`: PASS, shoulder-source ratio 0.89763 across 162 rows, upper/lower mean lid responses about 0.962/0.708 mm per side, both old-frame and old-eye controls rejected, 514 smile rows exact, 16,540 protected rows exact, face population and forward depth preserved, and 514 independently reconstructed neutral rows matching the new pin. I also read `candidate8-input-preflight.json` and its independent-neutral construction code. These are source-anatomy checks, not ocular fit or appearance acceptance.

I read candidate 8 `reference-smile-gate.json` top-level status and input: `pass; live evaluated geometry and controls, within stated bounds`, with the revised `006ab241260745ff5a88cc3b37bfdb82d3a6c6d00ff753a4c49fedc45159e105` pin. I did not audit every large witness array or rerun it. Root reported the crown guard rejected candidate 7 as a negative control; this report does not claim that as reviewer-run runtime coverage. The source review approves the test mechanism within its stated bound.

## Round outcome

Candidate 8 makes visible progress but is rejected as the finished appearance result. F11's specific visible step and F12's crown cleft improve; F12's remaining hair shape and F13's facial appearance remain unresolved. No blocking code defect was identified in the exact frozen implementation; F14 is a minor guard observation. This round does not accept final realism or delivery and does not cover later candidates.

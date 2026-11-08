# Review 14: integration

## Target

Closure of round 12's final-export and held-out-view coverage for the separate unclothed candidate 10 variant. Base remains `1ef6de511a0214234b676277dbb1f27c20b47a63`. The final exporter/checker/tests are unchanged from the reviewed `outputs/character-round2-20261107/review12-oblique-source/` snapshot. Its manifest SHA-256 is `1271a08b7d194217778f5259f18ad18d26db97bbbd0452ad55bf88108e3a6fe4`; I recomputed all three retained hashes and confirmed the live worktree tools still match.

| Final source | SHA-256 |
|---|---|
| `tools/export_character_variant.py` | `e55d2caf908f3b3d830901f230c8aa1c34217faf9e27c472a184b72fb37b4c83` |
| `tools/check_character_variant.py` | `512264e4724b73ed5042f4b0ecf5beb27d55fedaaa3cd395b7062b663f21b72b` |
| `tools/test_character_variant_runner.py` | `51b6579318095b79423d2f1990ca2c5a7173bac3a86a8751cc49ce23f273b789` |

The actual final-run artifacts are retained under primary-checkout `outputs/unclothed-variant/candidate-10-reviewed/`. They are separate from the earlier three-view export and from the dressed input. I independently hashed every artifact below and matched every digest listed in the verification receipt.

| Final artifact | SHA-256 |
|---|---|
| `unclothed.blend` | `ac2dc384ed3095beb6b909f305577cb6168cdfb0b349ce60dfb8cc5dc5d50e5f` |
| `front.png` | `9c2813df6901b9a3383b7830f234335b72f086be42bc86a5037c8c8013b14da1` |
| `back.png` | `6e50c0fdde65f1b1a1c2fb4b9e670092ff92b0c952958709e085cce45cedee88` |
| `profile.png` | `4c247bb4488ed80173b13fd0ad9fcc6500e59a00f131f07e1925343a345b51da` |
| `oblique.png` | `91ddd0989329c80cad911a59d3f6cb12b2bb0f228a01c407f7405bed197051c1` |
| `verification.json` | `b845616751b5b53930a61df700e2beafcbf503ce99bfebc8010e729afcee79ef` |

The dressed input is still `outputs/sailor_character_realism_goal/candidate-10/sailor_character.blend`, SHA-256 `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. I recomputed its current hash and matched both the initial and final input hashes in the new receipt. This review does not apply to candidate 11's rejected hair or any developing candidate 12 source.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the complete final verification receipt, verified source/artifact hashes and inspected all four final-run images through `view_image` at original detail, each 1280 by 1600 pixels. This includes the new seeded oblique, rather than transferring approval from round 12's older three images. The exact unchanged source and tests retain round 12's substantive implementation review; I did not repeat those tests or claim a new full code audit. I did not launch Blender, render or inspect the blend interactively. Root ran the final exporter and reports its owned process/job closed. I edited only this reviewer-owned report.

## Reports

### Independent Codex reviewer

Accept this exact saved artifact as the requested separate, complete unclothed copy of candidate 10 within the preserved static-character contract. Front, back and profile show a continuous anatomical body with hands and feet intact and no visible clothes, socks, footwear or accessories. The added elevated oblique exposes the shoulder-to-arm, chest-to-torso and waist-to-hip transitions from a different direction. Those regions remain continuous, with no obvious holes, detached patches or abrupt restored-skin seams visible at native resolution. The same adult face, hair, proportions and static pose remain recognizable across all four views.

This is acceptance of the variant task, not an endorsement of the broader appearance goal. Candidate 10's smooth facial rendering, helmet-like hair mass and comparatively rigid locks remain. The export neither introduces the rejected orbital experiment nor adopts candidate 11's shelf/bulge regression. It restores canonical body faces and removes separate clothing while preserving the existing character source coordinates. Keeping the dressed input intact and saving this copy separately is the appropriate outcome for the user's request.

The final receipt supports the visual result with the previously reviewed checks. All 19,158 source coordinates retain digest `439bab992ea56dc92bc636f246ecf5ae7fb9e87892536af1863c31bb4f316b95`. The body has all 13,378 canonical faces, including 4,198 restored faces; 9,180 original visible faces and 36,720 original visible loops are preserved. Before/after attribute schemas match, canonical photographic UVs pass, original visible UV/color values and face surface settings remain exact, and supported modifier/material-slot comparisons pass. The receipt lists 100 removed objects and reports retained-object/material-graph comparisons and successful checks after reopening the saved variant.

The unchanged negative controls retain their actual scope from round 12: the missing-face control alters a copied Blender mesh and must be rejected; the leftover-sock control tests the name-based population predicate. Both are rejected in this final run. They do not prove arbitrary future Blender-state preservation, and the snapshot limits documented in round 12 remain applicable. This final integration does not broaden those claims to animation, rigging, unsupported custom attributes or universal byte-level equality of all Blender data.

The seeded oblique closes the missing held-out native-view coverage identified in round 12. Its recorded seed is 20261107, camera position approximately `(2.851683, -3.695758, 1.323093)` metres, target `(0, 0, 0.85)` metres and orthographic scale 1.90 metres. All four renders use 128 samples at 1280 by 1600. The original three inspection directions remain, so the additional view supplements them rather than replacing a failed view.

## Findings and disposition

No new material finding. The two outstanding variant integration checks from round 12 are now satisfied for these exact artifact hashes. Root retains responsibility for Git delivery and current work-unit status.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| — | Round 12 lacked a final-code export artifact. | Root completed the export with the unchanged reviewed final tools; the new receipt and all artifact/input hashes were independently checked. | Closed for `candidate-10-reviewed`. |
| — | Round 12 lacked a held-out native view. | All four final views, including the seeded oblique, were inspected at original detail and show the complete unclothed copy. | Closed for this exact variant. |
| F12 / F13 | Prior hair and face appearance limitations. | Still unresolved; accepting the separate variant does not change the earlier appearance verdict. | Remain with the separately scoped appearance work. |

## Verification

I verified the retained source manifest, the three unchanged live tool hashes, every final image/blend digest, the verification-receipt digest and the dressed input's unchanged digest. I read the final receipt's topology, coordinate, original-loop, schema, material/retained-object, negative-control, reopened-save and camera fields. All relevant positive booleans are true, both negative controls report the intended rejection, and before/after schema lists are equal. I actually inspected every final render, not just their existence or exit status.

Root reports the final exporter used an owned headless Blender process and closed its process/job after completion. I did not independently execute or observe that process lifecycle; the final receipt itself does not contain process-cleanup telemetry. No task-owned Blender, GUI, browser or server was created by this reviewer. The three launcher tests had already passed independently in round 12; they were not rerun here because the tested source is unchanged. This report asserts local artifact acceptance, not that repository gates or Git delivery have independently been rechecked in this round.

## Round outcome

The requested candidate 10 unclothed variant is accepted as a separate complete static copy with the dressed input preserved. Round 12's final-code execution and seeded-oblique review gaps are closed for the exact hashes above. The broader face/hair naturalness goal remains unresolved, and no acceptance transfers to a later character or exporter revision without checking the affected result.

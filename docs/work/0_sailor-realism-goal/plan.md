# Reference-led sailor character realism

Status: active
Owner: root (integration, acceptance and delivery)
Created: 2026-09-05
Updated: 2026-11-07

## Problem and outcome

The owner rejected the artificial face, broad upper body and sparse hair. Candidate 10 narrows the frame and restores hair coverage, but its mannequin-like face and helmet silhouette remain rejected. The previous ten-attempt round is closed; its complete plan and delivery are recoverable at commit 1ef6de511a0214234b676277dbb1f27c20b47a63 and authored review rounds 8 through 11.

The owner's new instruction, "Then keep making progress", authorizes a fresh round of up to ten integrated candidates under the existing local rule. Global numbering continues at 11. The owner also requests a complete unclothed version and an explanation of clothing separation. Neither request authorizes pretending that the static character is rigged.

## Scope

Retain the adult age-20 anatomy, accepted narrowed frame and bust/waist intent, camera/lighting benchmark, separate garment fitting and strict live mouth bounds. Investigate coordinated lower-orbit/cheek movement and hair paths around the actual ears. Root owns integration and delivery; round2_face_search and round2_hair_search own bounded local mechanisms, unclothed_variant owns the saved-copy exporter, and garment_design_review supplies independent review.

Clothing, shoes and socks are separate objects, but covered body faces were omitted from the dressed build. The unclothed workflow restores complete canonical topology using unchanged saved coordinates and skin attributes, removes garment objects, and saves another artifact without modifying the dressed input. It does not maintain a second anatomical source. Both versions remain static, without an armature or bone-driven skinning.

## Approach

The fixed benchmark and disqualifiers were recorded in design.md before fresh independent searches. The selected orbital response couples a small lower-lid lift with upper-cheek support after the smile and both preserved reference copies. Pure production checks preserve all oral anchors, eyeball and eyelash proxy coordinates, skin/garment references and source continuity. Evaluated eye/lash fit and rendered appearance remain separate requirements.

Actual hair attribution measured a 23.39 mm broad clearance correction caused by early free fall across the ear. The new route follows the anatomical side surface below the ear before falling, with unequal lower locks. Its unsaved complete groom preserves all existing guards and reduces upper-temple extent by about 6-8 mm per side. Maximum correction rises to 34.58 mm farther back; native profile/back/oblique review must determine whether this only moves the bulge.

## Acceptance criteria

- Natural, appealing adult facial expression and full organic hair without a helmet silhouette, rigid lower curtain or scalp seams, judged in native canonical four, fixed opposite oblique and seeded torso views.
- Retain coherent clothing fit, the accepted upper-frame changes and the strict mouth/eye/skin geometry requirements. Test numbers do not establish attractiveness.
- Complete unclothed body with preserved coordinates and visible skin attributes, no garments or accessories, source input unchanged, and native fixed plus seeded-oblique inspection.
- Independent exact-source review, required repository gates, secret/size checks, merged main and pushed delivery, and cleanup of owned processes and worktree.

## Implementation steps

- Completed: fresh face/hair diagnoses and bounded proposals; current orbital production source checks and full unsaved hair guards pass.
- Completed: candidate-10 unclothed copy, with 4,198 restored faces, unchanged 19,158 coordinates and all 36,720 original visible UV/color loops, saved-file reopening and front/back/profile review. The final launcher adds bounded timeout, failure-path input checks and a seeded oblique view; final selected export will exercise that exact source.
- Completed: candidate 11 and all six native views; rejected for hair silhouette despite passing technical checks. The orbital proposal was excluded after its evaluated fit failure. One of ten integrated attempts is used.
- Completed: final candidate-10 unclothed export, four native views, independent review 14 and required repository gates. Its source and documentation are ready for the separate delivery milestone.
- Active: a distinct hair-path correction for candidate 12 and an actual-shell face proposal; these are not accepted or included in the variant milestone.

## Outcome

Appearance proposals remain local and uncommitted on codex/character-naturalness-round2 in outputs/.worktrees/character-naturalness-round2. Primary checkout changes from other work remain untouched. Evidence is intentionally retained under outputs/character-round2-20261107, worker evidence folders, outputs/unclothed-variant and the immutable numbered candidate folders. CHR-001 and the remaining face/hair portion of CHR-004 remain open.


## Current round results

Candidate 11 used one of ten new integrated attempts. It passed the saved technical checks, but root and independent six-view review rejected ear-height shelves, an abrupt lower waist and a ballooned rear silhouette. Candidate 10 remains the usable dressed draft. The attempted orbital field was excluded before integration: evaluated witnesses showed corneal penetration increasing from 104 to 249 micrometres and a lower-lash root changing from 99 micrometres clearance to 401 micrometres embedding. All failed source bytes and measurements remain recoverable in outputs/character-round2-20261107/rejected-orbital-source and the preserved worker evidence. Neither failure is relabeled a successful appearance repair.

The final reviewed variant tools produced outputs/unclothed-variant/candidate-10-reviewed with the complete saved body, unchanged input and all four native inspection views. Its saved blend SHA256 is ac2dc384ed3095beb6b909f305577cb6168cdfb0b349ce60dfb8cc5dc5d50e5f. Further appearance work uses a distinct hair-path correction and actual-shell face investigation; no unverified revision replaces the usable draft.

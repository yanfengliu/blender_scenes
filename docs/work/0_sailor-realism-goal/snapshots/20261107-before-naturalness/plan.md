# Reference-led sailor character realism

Status: active
Owner: root (implementation, integration and acceptance)
Created: 2026-09-05
Updated: 2026-11-07

## Problem and outcome

The adult sailor character still differs visibly from the frozen reference. The current requested continuation is narrower: resolve candidate 5's unintended garment changes, finish its visual review, and reconcile the status notes while preserving the accepted body proportions and smile.

## Scope

Candidate 6 retains candidate 5's actual smiling body and restores candidate 4's exact blouse and collar. Body proportions, hair, pose, materials, canonical cameras and lighting stay fixed. Earlier candidates and their evidence remain preserved. The unimported regional-hair and surface-growth experiments remain outside this delivery. Root owns implementation and integration; garment_design_review supplies independent source and visual review; garment_regression supplies the two maintained regression tools.

## Approach

A face-only edit changed which equal-distance triangle normal the whole-body BVH returned at three neckline controls. Local support geometry did not move, but the derived collar inherited the changed blouse. Capture separate garment anatomy after the retained perioral edit and before the smile, apply the same proportions and pose, and use that anatomy for garment preparation and fitting. Validate final clearance against the actual saved smiling body with canonical hidden skin faces restored. Changing the BVH tie policy would not guarantee the previously accepted garment geometry.

## Acceptance criteria

- Exact saved garments equal candidate 4; actual saved body and factual smile contract equal candidate 5; all other captured scene inputs remain unchanged within the stated capture bounds.
- The actual smiling body's complete evaluated surface has no triangle overlaps with either garment's inner, outer or rim; sampled signed gaps remain at least 0.2 mm.
- Historical candidate 5 fails garment isolation; an in-memory body intrusion fails clearance and is restored. Neutral, smile and extra remote-face cases produce identical garments through the production construction path, while a torso change still changes fitting.
- Root and independent native-resolution review accept the local increment in hero, portrait, profile, back, fixed opposite oblique and an additional seeded torso view. Passing this repair does not close full reference likeness.
- Required repository gates pass before Git delivery. Retain source and authored records in Git, with generated scenes/renders and raw evidence ignored.

## Implementation steps

- Completed: reproduce all three saved neckline query witnesses; rebuild the exact accepted blouse and collar using neutral support.
- Completed: build candidate 6 once at the fixed settings, preserving the existing five candidates.
- Completed: saved whole-scene isolation, canonical reopened checker, actual-body garment clearance, historical and intrusion controls, and four-case production expression regression.
- Completed: root and independent review of six native images and the exact scene/checker revisions; see reviews/6_implementation.md and reviews/7_integration.md.
- Completed: reviewed character source and status notes merged to main and pushed as f65ba3ee3bdf8e3ad44e1663642e67dbc2ce639c. The inherited fleet blocker has been repaired separately; its complete suite now passes 563/563 without skips, and all 35 repositories have current canon.

## Outcome

Six of ten integrated attempts are used. Candidate 5 is preserved as the garment-drift negative control; candidate 6 is the accepted local repair at outputs/sailor_character_realism_goal/candidate-6/sailor_character.blend (SHA256 8a3fa2c0d8df7025cc08a7d946df1822c4d43bf8230396e93838f3e31bf2abd2). The saved blouse and collar exactly match candidate 4, while the body exactly retains candidate 5. All 114 captured nonbody objects and all captured material, attribute, image, camera and lighting data preserve candidate 4. Across 585,900 finite surface samples the minimum blouse gap is 0.574623 mm and collar gap is 3.356572 mm; every shell partition has zero body-overlap pairs. The 381-vertex intrusion and historical candidate 5 are rejected. Smile and 112-row forehead controls leave garments exact; the torso control affecting 345 body rows changes fitting. Root and independent six-view review accept this local result. CHR-003 is repaired; CHR-001 and overall photographic likeness remain open because the skin, hair and cloth still differ substantially from the reference. Four integrated attempts remain in this round; none was consumed by unsaved checks. The initial normal-access fleet run passed 548/557 and exposed nine inherited failures. The owner approved a one-time delivery exception, but the underlying fleet repair was completed first: six new cleanup regressions were added, all 563 tests now pass without skips, both dependency audits report zero vulnerabilities, and canon sync is current across 35 repositories. Windows fixture cleanup and the two missing census entries were fixed without weakening assertions or changing production work-document safety behavior (fleet work unit 32). No exception is needed for this delivery. The work-document structure check passes one unit. The required official Blender Lab MCP donut gate also passes, with all three native renders inspected. The reviewed repair is merged to main and pushed as f65ba3ee3bdf8e3ad44e1663642e67dbc2ce639c; its exact source/checker hashes remain those in review rounds 6 and 7. Fleet repair 70d5679ca22560d7222a391485877c9f376d0f6d is also merged and pushed. GitHub Actions returned zero runs for both exact revisions. Unrelated pre-existing donut/chili and experimental hair files remain untouched and uncommitted in the primary checkout. The September status remains recoverable in snapshots/20261107-before-candidate6/plan.md.

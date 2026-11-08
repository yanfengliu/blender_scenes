# Review 7: integration

## Target

Repository: blender_scenes. Base revision: ade40140278b6bd7fd060ccac3dfb0692cb43748. The reviewed local result is outputs/sailor_character_realism_goal/candidate-6/sailor_character.blend, SHA256 8a3fa2c0d8df7025cc08a7d946df1822c4d43bf8230396e93838f3e31bf2abd2. Frozen candidate 4 is b9cb210243c7e05b9eae904e20f344eb683ed1f2e3dca3a3a77b88fc5da43837; candidate 5 is 1eebe0bbaaafd2c13fd06daac29e97e365bbc51271c4cd3ddb83241000c430fa.

Exact source targets are sailor_character_realistic.py (9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b), check_garment_isolation.py (b9deb8d792c2a82561a5805d2b2a7b0b77d4566aa22037afa3082acfeddbd4e1), and check_expression_fit.py (b0393a810fa0617e8775e2b222104c34c78b38c6341f16429c7ebf30b32091dd). Their bytes are retained under outputs/candidate5-recovery-20261107/review-targets/scenes/ and tools/. That directory's manifest.json has SHA256 948e58bb7147d22e4cd46c3eb36368f58cebd04a56b80916a1e79a397f4bc39f; implementation.patch is 7acf07e3b55be1e2897fe7cb4cd225cc54b244e82c0adbd991ef454be370f5c6. These ignored inputs remain deliberately retained while code cannot be committed.

The inspected image targets and their native dimensions are listed in the authored report below. The two frozen references are outputs/sailor_character_proportions/references/character-reference.png (ea71fef894f068da0736a177ce4619ef176d0719581033cab8781b63f18e1139) and body-turnaround.png (28b8220d0f56cac0dae249755becf6f63474c8ed749dc001ac4bef1dfec20680). The reviewer checked these digests against outputs/sailor_character_realism_goal/baseline-manifest.json.

## Reviewers and coverage

The independent garment design reviewer verified the two exact checker fixes, reviewed the production expression regression, inspected all six candidate 6 images at original resolution, all five corresponding candidate 4 and candidate 5 images, and both frozen references. The reviewer read completed runtime receipts and independently hashed the reviewed artifacts; the reviewer did not launch Blender or rerun the runtime gates. Root performed the builds and gate runs, inspected all six new images and accepted the local increment. The garment regression worker implemented the maintained checkers. No reviewer or root acceptance in this record closes overall photographic likeness.

Only these two reviewer-owned review records were written by the independent reviewer after the read-only work. Implementation, other documentation, Git operations and runtime process ownership remained with root.

## Reports

### Independent garment design reviewer

**Final source-fix and visual report.** I accept candidate 6 for the local garment-isolation repair and preservation of the candidate 5 smile. No blocking finding remains in this bounded review. Overall photographic realism and reference likeness remain unaccepted.

Reviewed scene: 8a3fa2c0d8df7025cc08a7d946df1822c4d43bf8230396e93838f3e31bf2abd2. Reviewed scene source: 9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b.

The two checker findings are closed in check_garment_isolation.py, SHA256 b9deb8d792c2a82561a5805d2b2a7b0b77d4566aa22037afa3082acfeddbd4e1. F9 / GI-R1: lines 132-135 reject mesh animation, vertex groups and subdivision crease attributes; line 235 applies that contract before reconstruction. F10 / GI-R2: lines 233-234 require one Blender unit per metre before evaluating the physical clearance threshold.

I inspected all six new PNGs with view_image(detail="original"), all five corresponding candidate 4 and candidate 5 views, and both reference images. The reference hashes match baseline-manifest.json. The hero and torso views show continuous blouse coverage through the chest, sleeves and waist, with the collar bands following the retained shoulder shape. The profile and back show no newly visible neckline break, collar displacement or garment opening. The portrait and opposite oblique preserve candidate 5's subtle mouth-corner lift without a newly visible central opening or lip fold. The small nape exposure and stiff, smooth garment treatment are also present in earlier candidates; I found no new visual regression attributable to this repair. Visual inspection alone cannot resolve the original submillimetre drift; the exact saved comparisons establish its removal.

The inspected candidate 6 image targets are:

| Image | Native resolution | SHA256 |
|---|---|---|
| hero.png | 1280 x 1600 | b035a1620b882eeb8af677afef35f3e4d4609c8193b7f01a3db2ac51716ff5a9 |
| portrait.png | 1200 x 1200 | 717a5c5b686e396a275788bce107cba41d93656346d9a11f4fe9c919927520d9 |
| profile.png | 1200 x 1200 | 3745ca142f44ee5e52f48e5583decba73364808e5c741a60be402029088e9ed5 |
| back.png | 880 x 1100 | 8b1f819fb1566fec626991e02886e5ec207d36c3685279fd11153bf26042ed9a |
| face_oblique.png | 1200 x 1200 | 222a9a1abd3a0cfac34c08465a73333060f589aefc7e2c1b63803216bb64f65a |
| torso_random.png | 1200 x 1400 | b56511385695019fcd64b64e6e040c86c0f60d328cfef81ab81ee95f824c3f65 |

These files are under outputs/sailor_character_realism_goal/candidate-6. The oblique and random-view receipts bind their images to the same saved scene and report removal of temporary cameras without changing the scene file.

I read the completed runtime receipts rather than relying on the coordinator's summary:

- Saved preservation passes: all 114 captured nonbody objects, material graphs, packed images, original attributes, body topology/UVs and other captured scene inputs match candidate 4. Only the pinned smile coordinate changes and factual smile input remain.
- Garment isolation passes: both garment fingerprints match candidate 4; the actual body fingerprint matches candidate 5. Canonical reconstruction restores 4,198 hidden faces and evaluates 428,096 body triangles.
- Clearance passes: every inner, outer and rim partition has zero body-overlap pairs. The minimum sampled blouse gap is 0.574623 mm; the minimum collar gap is 3.356572 mm, both above 0.2 mm.
- Controls pass: historical candidate 5 exposes garment coordinate drift. A 381-vertex chest intrusion produces negative gaps and overlaps, is rejected and is restored.
- Canonical smile and standalone checks pass: the live aperture receipt reports maximum scalar increase 3.7272 micrometres, vertical increase 8.8215 micrometres and zero depth change under the retained 50 micrometre bound.

Evidence hashes: garment-isolation.json is 6d8068f749306e6f7b8cc730e91d66f46068039102e11500ba107b46cabba342; smile-preservation.json is 41033f2c2a5aeedafee3d77a9763d00df33503d741f09e9f5c377eef9f369c61.

The remaining realism gap is visible against the references: hair forms a uniform straight curtain, facial rendering remains smooth and synthetic, and the blouse lacks the reference's loose fabric folds and construction detail. Those are inherited limitations outside this repair. Sampled clearance and triangle-overlap checks do not prove continuous clearance, self-collision freedom or cloth comfort.

At the time this source-fix and visual report was delivered, I had launched no Blender or GUI process, run no tests and changed no files. Repository gates and Git delivery remained outside this review's scope. Writing the subsequently authorized review records does not change that runtime-coverage statement.

**Production expression regression source report.** No blocking findings in check_expression_fit.py, SHA256 b0393a810fa0617e8775e2b222104c34c78b38c6341f16429c7ebf30b32091dd. The comparisons are nonvacuous: neutral/smile/forehead cases must change actual native and posed anatomy above 1.45 m while preserving complete garment fingerprints. The torso control runs before the production garment-reference capture, affects body and helper coordinates, and must change blouse vertices. Each case resets its disposable scene. The selected production blocks omit scene saving and rendering, and final cleanup resets Blender again. The test appropriately covers dependency isolation; saved clearance and visual acceptance remain separate. This initial regression report was static review only; I did not run the regression.

**Later expression-receipt verification.** I subsequently read outputs/sailor_character_realism_goal/candidate-6/expression-fit.json, SHA256 96ae77af735546defb2b1caf4dcf98f5738e1416f436686d7093f25d8ac9107c. Its status is pass and its source SHA256 matches the reviewed main. Neutral to smile changes 522 native and 504 posed anatomical rows with no garment difference. Smile to remote_face changes 112 native and 112 posed rows with no garment difference; the recorded forehead displacement is 0.689844 mm. The torso control perturbs 486 body/helper rows, including 345 anatomical body rows, with a 1.997520 mm maximum injected displacement; both native and posed body comparisons change 345 rows and both garments' vertex fingerprints change. The receipt records that temporary objects were cleaned. This confirms meaningful runtime controls without changing the earlier static report into a claim that the reviewer ran them.

**Documentation content observations.** The current plan, README, CHR-003 entry and dated devlog correctly separate the accepted local repair from open CHR-001 and overall likeness. Their exact-saved geometry, 585,900 sample total, minimum gaps, six native views and six-of-ten integrated-attempt claims agree with the inspected evidence. The reviewer flagged garbled multiplication/arrows in an unrelated README section and an ambiguous "345-row torso control" phrase. After root's edits, the reviewer checked that the README encoding defects were absent and the plan qualified the torso control as affecting 345 body rows. The final plan and detailed devlog state the 548/557 fleet result, nine unrelated failures, passed donut gate and blocked code delivery without claiming a commit or push. These were minor content corrections, not new scene or runtime changes.

## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F8 | Remote expression changed unrelated garment geometry through tied BVH normal selection. | Resolved for this local increment. The reviewer accepts the separate reference mechanism; exact saved fingerprints, nonvacuous production controls, actual-body checks and six-view inspection pass. Root independently accepts the local result. | Main 9ec3cbc64ed7a2504536f5c5c7f41d56e1ae24ad2927386be3d2d5f9081d527b and candidate 6 scene 8a3fa2c0d8df7025cc08a7d946df1822c4d43bf8230396e93838f3e31bf2abd2. |
| F9 | GI-R1: body subdivision creases were absent from reconstruction coverage. | Resolved. Root added fail-closed guards; the reviewer checked the exact guards and their call before clearance. | Fixed checker b9deb8d792c2a82561a5805d2b2a7b0b77d4566aa22037afa3082acfeddbd4e1, lines 132-135 and 235. |
| F10 | GI-R2: physical units were assumed without checking scene scale. | Resolved. Root added the fixed-metre requirement; the reviewer checked it precedes measurement. | Same fixed checker, lines 233-234. |

The original F9/F10 findings and reasons remain in round 6, with their original exact checker bytes retained separately. F0-F7 remain unchanged history. The optional empty-attribute-snapshot hardening remains a nonblocking suggestion; it is not claimed as implemented.

## Verification

The independent reviewer read and hashed completed candidate 6 receipts for the canonical reopened checks, strict saved preservation, garment isolation, actual-body intrusion and production expression regression. The reviewer inspected the six native images and the frozen comparisons directly. Runtime checks were performed by root or its assigned runner, not by this reviewer.

The six measured shell partitions contain 585,900 samples in total. All partitions have zero body-overlap pairs. Historical candidate 5 fails both garments' vertex comparisons. The intrusion control records negative gaps and overlaps, then exact source restoration and unchanged saved files. These checks remain bounded to the declared finite samples, triangle populations and supported source state.

Root reported the repository gate status on 2026-11-07: sync-canon check exited 0 with warnings about uncensused platsim and typewriter; the unsandboxed fleet npm test passed 548 of 557 tests, with nine failures in census and unrelated Windows work-document shell/path tests. These are not reported as Blender-source failures, but the repository rule still blocks a code commit while required gates fail. Root reported that the official donut MCP build/render gate passed, its hero/overhead/detail images were inspected at native resolution, and its owned process tree was closed. The independent reviewer did not run or visually inspect that donut gate and attributes those results to root.

No code commit, merge or push is claimed by this round. Any owner exception to the failed repository gate is a separate decision after the full reviewable payload is prepared; this review does not supply that exception.

## Round outcome

The exact local garment-isolation repair, retained smile, fixed saved checker and production regression are accepted within their stated scope. No material F8-F10 finding remains open. Root and independent native six-view review accept this increment, while CHR-001 and full photographic likeness remain open. Required fleet failures block code delivery under the repository rule, so product source remains recoverable in the isolated worktree and retained targets rather than being described as merged or pushed. The plan remains the current work-status record; this round preserves the authored review and evidence at acceptance time.

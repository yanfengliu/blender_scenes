# Review 15: integration

## Target

Exact candidate 12, the second integrated appearance attempt in the newly authorized round, built from base `1300d0e625d0f02d97a9bbf22cc62b749e13b3b4`. This is the actual-cornea-following orbital experiment with candidate 10 hair retained. The developing lower-hair repair is excluded. Frozen inputs are under primary-checkout `outputs/sailor_character_realism_goal/candidate-12/source/`; their 37-file manifest SHA-256 is `e4bd5af679549da97e2785c098f1db1a69336198885130bab7787201d4da6d11`. I independently verified every retained file's hash and byte length against that manifest. Candidate 12's hair source matches candidate 10 after newline and final-whitespace normalization; it is not candidate 11's rejected replacement.

| Reviewed source | SHA-256 |
|---|---|
| `scenes/sailor_character_realistic.py` | `fd13fd0770d793b3be87066938e826972347422448f8dd8335866d85e502e604` |
| `scenes/orbital_expression.py` | `c6732a20b772b2642123e40890563a1bfbb1b68299dcf35451353b41516b4c5f` |
| `tools/check_orbital_expression.py` | `53e5bc0ff0166eb69025ae348555fd54711fdcc1b7622447cae5c63cdd92fc28` |
| `tools/check_orbital_fit.py` | `0940ae31ff6fbf1d11075165a1c5f118bc416d2e6ee2fbd40a473940b2a7ae24` |

Final artifacts are retained beside the source folder. I independently verified all nine entries in `artifact-manifest.json`, SHA-256 `476cfa59e856d18e9c348a3ef16f9e854b3904180547b3067a4aded51bcc3200`.

| Final artifact | SHA-256 |
|---|---|
| `sailor_character.blend` | `1ded6a0cc3ef367d72483b0c37b05c422a07dfc25375533a6a429153f8dd76ae` |
| `hero.png` | `7c4056f27c152c35dde88ea6c91be73cc9e5fbca5d3cad98518da771260a09e4` |
| `portrait.png` | `2825b47f99c6c5cd93bc8cb1c7003c618f4b2f8f7c2be7b4b52e937e9625a756` |
| `profile.png` | `fb218a3fc2fb912235565d667826f8b25a37a4e8172bad4a285c9e3008300d45` |
| `back.png` | `75b519f46abd8a6c8e9d74174d270d8d3a5bbbdb45e12e39128ab33bdeeee302` |
| `face_oblique.png` | `80a8f48c47e5515bb53675f4323d05dbd1776a8c9dc023253920824ff1e1f872` |
| `torso_random.png` | `98136a22c0799908b4d1e0fa72378920557ae176e2c6d96a1e6abc24b858d9e7` |
| `saved-verification.json` | `416d48256ca38dff9d74e79cb2a942a3e2fdb0f5c4f1d2b2268f2302cd2d7333` |
| `saved-orbital-fit.json` | `2aab0406f028bf3b13a8b8ed6162aa03020adb09fc1c2553775110f4d07e6f5d` |

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the complete frozen orbital helper and both maintained orbital checkers, the main integration and relevant unchanged production extraction/proportion/frame dependencies. Hash verification of the other frozen files is revision binding, not a claim to have newly audited every line. I inspected all six candidate 12 images at original detail, then all six corresponding candidate 10 images and the original adult character reference. Native dimensions are 1280 by 1600 for hero, 1200 by 1200 for portrait/profile/opposite oblique, 880 by 1100 for back and 1200 by 1400 for seeded torso. I read the maintained production preflight receipts and the final saved orbital receipt, and selectively inspected the much larger saved finish receipt's relevant results and limits.

I did not launch Blender, render, run these runtime gates or inspect the blend interactively. Runtime results below are read from root/worker-run retained receipts. Root reports the supplementary-view/saved-check process completed and closed. I created no browser, GUI, Blender or GPU process and edited only this reviewer-owned report. This review does not extend the separate unclothed variant acceptance from round 14 to a new variant export.

## Reports

### Independent Codex reviewer

Candidate 12 is NOT ACCEPTED as a material aesthetic improvement or as completion of the appearance goal. Its bounded orbital mechanism and evaluated regression checks are technically acceptable for this exact static experiment. Those are separate judgments. The rendered change is too subtle to establish a clearly more natural, appealing adult expression relative to candidate 10.

In the native portrait, the lower lids and upper cheeks change slightly, but the face still reads as broad, softly blurred cheek planes surrounding a small, comparatively isolated mouth smile and glossy dark eyes. The eye/cheek response does not create a clear improvement in the connected expression seen in the adult reference. Hero and seeded torso retain essentially the same facial impression at their intended viewing scales. The opposite oblique confirms this rather than revealing a convincing improvement hidden in the frontal view. I see no obvious new lid tear, conspicuous lash detachment or distorted eye surface in these inspected renders; that observation is not a claim of continuous geometric clearance.

The adult identity, prior narrower upper frame, fuller bust/slim-waist direction and clothing silhouette remain recognizable. Candidate 12 does not introduce the earlier collar shoulder kink. These preserved results should not be reported as new gains from the orbital change. The head still has a broad rounded hair cap, a blunt dense fringe, nearly straight side curtains and an abrupt lower silhouette. Profile exposes a conspicuous bare neck/shoulder cutout within the lower hair outline; back shows the corresponding exposed patches. These are inherited problems in the retained hair, not repairs made by this candidate. Compared with the reference's irregular groups, visible ear transition and soft tapered ends, the hair continues to dominate the unnatural impression.

The source correction addresses the actual cause of F18 more carefully than the rejected joint-circle proposal. `orbital_expression.py:14-45` evaluates the complete fitted eye proxy with Blender subdivision before filtering the marked corneal triangles; filtering first would change the boundary surface. Temporary object, mesh and marker material are removed in a `finally` path, with existing datablock identity sets checked afterward. The production helper contains no unused pure subdivision replica or module-global ID cache. The explicit response object carries the shell, sections and transport shared by body and lashes.

`orbital_expression.py:87-111` retains the bounded 0.45 mm requested lift and 0.8 mm cheek support, queries a fixed-X shell section and moves outward when necessary to preserve at least the original signed section gap. The interpretation is a source-space gap floor, not exact three-dimensional contact. Outside the open section domain it retains the provisional motion and records affected body rows. The code's unchanged-X field, protected oral/ocular anchors, helper exclusion, regional bounds, finite coordinates and exact eye-proxy refit checks are appropriate for this fixed adult anatomy. The left-side canthal definition mirrored through absolute X and the hard-coded stature/support bounds also make this a deliberately specific model helper, not a general expression solver for arbitrary heads.

The main applies the response after the reference smile and before body proportions (`sailor_character_realistic.py:177-183`). The existing garment/skin snapshots precede the response. Lash transport now occurs after actual mesh creation, using Blender-stored vertex coordinates (`sailor_character_realistic.py:299-304`), so it preserves the passed prototype's float32 ordering. The earlier proposed pre-mesh order was not silently treated as equivalent. Relevant unchanged code supports this coordinate frame: `body_proportions.py:61` protects head rows above 1.30 m, and `upper_frame.py:25-28` fades its final deformation to zero by 1.43 m. The orbital region lies above both boundaries. `check_expression_fit.py:27-51` still extracts the actual ordered production anatomy and final-frame statements, avoiding a separately maintained miniature anatomy implementation.

The maintained source gate is meaningful rather than a comparison of two no-ops. It executes production AST, extracts the actual post-mesh lash branch and requires that branch to contain the transport call. It compares against a production no-orbit control, checks source triangle area/orientation and edge displacement gradients, rejects absent motion, checks exact protected references and eye geometry, and exercises normal and intentional-exception temporary-shell cleanup. Its optional historical equivalence mode verifies the pinned passed-0.45 prototype before use and compares every native row plus body, eye and lash source coordinates/topology. Root ran that mode in the separate maintained preflight. The candidate's routine source receipt says equivalence was not requested; that field is accurate and must not be presented as a second equivalence run.

The maintained evaluated gate independently builds production no-orbit and no-smile cases. It checks render-level subdivision, exact evaluated eye geometry, fixed baseline-selected lower-orbit body samples and baseline-selected lash roots. Saved mode verifies saved source geometry, topology, transform and supported subdivision settings before measuring the actual saved objects. It propagates the recorded fallback controls through subdivision to identify their evaluated influence. Actual inward-displaced body and translated-lash copies must fail the same measurements. The saved file hash is checked unchanged afterward. These checks cover the previously demonstrated source-versus-evaluated defect class and the float32 integration risk without relaxing the 50 micrometre limits.

The evaluated metrics remain finite nearest-normal differential measurements. The open shell, baseline signed distances, nearest-face choices and selected root population do not establish an absolutely penetration-free eye/lash assembly or continuous clearance between samples. The saved lash separation result leaves only about 3.60 micrometres below the current bound; changed geometry or evaluation settings require rerunning the real saved gate. Existing low-hair body/clothing contacts are outside this orbital gate and outside the fringe/crown/temple projection checks in the saved finish tool. A green finish receipt cannot close that separate lower-hair problem.

## Findings and disposition

| ID | Finding | Independent disposition |
|---|---|---|
| F18 | Earlier orbital proposal passed source checks while worsening evaluated eye/lash fit. | Resolved for this exact bounded candidate 12 implementation: actual fitted-shell evaluation, shared post-mesh lash transport, production equivalence and the unchanged saved 50 micrometre gates pass. This is not aesthetic acceptance or absolute-clearance certification. |
| F13 | Face remains insufficiently natural and appealing. | Open. All six native views fail to establish material improvement over candidate 10; the small orbital response does not close the expression gap. |
| F12 | Hair remains visibly artificial. | Open. Candidate 10 hair is retained, including the rounded cap, blunt fringe, rigid lower curtain and exposed neck/shoulder outline. The unintegrated lower-hair proposal is outside this review. |

No new material implementation defect was found in the frozen orbital helper, main integration or maintained orbital checks. Root separately reports rejection of candidate 12 as a material aesthetic improvement, consistent with this independent visual disposition. No broader approval of current evolving source is implied.

## Verification

The retained actual-production receipts are in the isolated worktree's `outputs/round2-face-search/`: `maintained-source-preflight.json`, SHA-256 `1cc07a9fc1ae5537277a19d54ea463e4921e4290ed857f261ab48be391273b98`; `maintained-fit-preflight.json`, SHA-256 `b222b68a271ac53b48977d8f11336bd7635b912ca9a20663b5ba8aee3d4be279`; and `maintained-gate-sources.json`, SHA-256 `b162ae445f332effb23f3ca1365d893bf3b8e52762c1eac6bf2472940e24eae4`. Their main/helper/checker hashes match the frozen reviewed inputs. The historical proposal is pinned to SHA-256 `85c8d714162fb5e071d4db388ae3914b02fa4d4eebaa29d3b78e73446c4debc6`. The older `shell-route/source-equivalence.json` uses a diagnostic shell and explicitly records `actual_evaluator: false`; I did not substitute it for the actual maintained equivalence receipt.

The actual source gate records 248 changed native rows, 17,583 protected rows exact, all 76 oral rows exact, maximum movement 0.917623 mm, 624 affected source fan triangles, minimum area ratio 0.971464, minimum normal dot 0.966002 and maximum edge gradient 0.241596. The no-op control rejects. Actual historical equivalence covers all 19,158 native rows and all source vertices of body/eyes/lashes: 19,158/1,064/250. Both cleanup identity-set checks pass. The routine candidate source receipt, `check_orbital_expression.json`, SHA-256 `01d8cf95f95bcb8c8dc962455d87f0f2f4cf1717862834dd06fccf4345e27048`, reproduces the source invariants without the optional historical comparison.

The final saved orbital receipt passes on the exact blend listed above: 9,514 lower-orbit/cheek evaluated samples, 964 baseline-selected lash roots, maximum additional eye penetration 29.680190 micrometres, lash separation 46.395217 micrometres and lash penetration 2.074709 micrometres, each below 50 micrometres. These saved lash values differ slightly from the unsaved preflight's 46.426903/2.141148 micrometres; the saved values are the final artifact result. All 834 evaluated rows influenced by the fallback source controls have zero additional eye penetration. Shell identity is within 0.357749 micrometres across 7,922 active shell vertices. The real inward-body and separated-lash controls produce approximately 1.316713 mm and 2.958953 mm regressions and are rejected. All 516 independently reconstructed neutral/proposed smile rows retain input pin `52d36d7c9db5b4750807bb97dec4c0270f7cc4b3aa2296407b36c00194a9ab2e`.

The saved finish receipt uses the previously reviewed checker SHA-256 `2fb43449929926946fe9ed07adab66feed428b5dec15470803c4189259773fef` and canonical base SHA-256 `8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c`. It reports canonical checks passing, complete 13,378-face support reconstructed from the actual 19,158 source coordinates, garment shells above the unchanged 0.2 mm requirement with zero overlap pairs, rejection of the real intrusion and empty-ornament controls, all nine named ornaments checked, and passing fringe/crown/temple coverage. Its own visual-acceptance field correctly says appearance is not certified. I read the pertinent summaries and bounds, not every large per-sample record. The shape and four-case expression receipts also report pass; their SHA-256 values are `13ab75bd5fc2e3354889eb27d195e0c20ce7780dabf006e4c7440af52e29264c` and `ea6c0dcf72d914565a600aeb757b43f9814ac604480c3689fdd5e15f3d82790e` respectively.

Both held-out images were inspected as new candidate 12 outputs. The torso receipt retains seed 20261107, reports the temporary camera removed and matches the final blend/image hashes. Native viewing and hash checks were performed by this reviewer; all Blender build/gate executions were performed by root or the face worker. No fresh fleet or donut run is claimed by this review.

## Round outcome

The exact candidate 12 orbital implementation clears this bounded source and evaluated-fit review. Candidate 12 remains NOT ACCEPTED as a material aesthetic improvement and does not meet the overall appearance goal. F12/F13 remain open; source safety and saved gate success do not lower the visual benchmark. Retain this experiment and its failed predecessors as evidence while root chooses the next distinct mechanism within the authorized round.

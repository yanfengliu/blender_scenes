# Review 8: integration

## Target

Candidate 7, based on `2e95c6b0a1655ca2e6c4f067348bcdbbdaa231c1`. The exact built source is retained under `outputs/sailor_character_realism_goal/candidate-7/source/` in the primary blender_scenes checkout. Its 27-file `source-manifest.json` has SHA-256 `8944c75879da60401e38409ece6cb2b36ad93ee8ff0590e50274d23ef51ee36f`; I recomputed all 27 source hashes and matched the manifest. This review does not cover the subsequently evolving candidate 8 source in the worktree.

| Main reviewed source | SHA-256 |
|---|---|
| `scenes/sailor_character_realistic.py` | `deba0b45873c9a18e18c7d149ae86296951a7a6e0b3d3a21744fe92e51887b07` |
| `scenes/upper_frame.py` | `6efd70510146fc83bd6bebe1d5c286851a46fa7172cf70cbc41e019568feea20` |
| `scenes/natural_face.py` | `c3c0749643f764e86f1af37e9566815f6caddd3f4675897ea6c552fb05d85803` |
| `scenes/natural_hair.py` | `7cd7c70f47ba295f9403cd8b13c0e92e191de62e33e8de86d125091082c7c164` |
| `scenes/hair_groom.py` | `bdd4dbc84d31d711101c5abce094f9929dce42b88afc8517c9ac2666f3543b0f` |
| `tools/check_character_shape.py` | `9c3394121af3d56ebbd03f8b093f20737db247149bf46682c1970ce9a5d38a66` |
| `tools/check_realistic_character.py` | `2fe77e55e4df78287f8726e068e5b2755e5323a8d23d3c229f90234d8d903ce7` |

| Candidate 7 artifact | SHA-256 |
|---|---|
| `hero.png` | `10cd55f90e2c9258ce0b57e5e939180b212fd06c8897e508669ea630b737b2f6` |
| `portrait.png` | `b29b5f603c38c18c27c87be030171368d4dd428f9f43d9a774e3a9828a259bd8` |
| `profile.png` | `f220d69805edd5628feebf88eaeb2e510863429a298a2376f3ceaf15707331bd` |
| `back.png` | `f66c87a3b74afcab9a6045af8be35442a5dbd9410c266573d75b22c08ad71c6b` |
| `sailor_character.blend` | `6f1ed4735801f25c492ca78aa1fa4f87cd1fb6c7c396c16111e5c5e27ecf8bde` |

Comparison inputs are candidate 6's native hero, portrait and profile images and the original adult reference images under `outputs/sailor_character_proportions/references/`: `character-reference.png`, SHA-256 `ea71fef894f068da0736a177ce4619ef176d0719581033cab8781b63f18e1139`, and `body-turnaround.png`, SHA-256 `28b8220d0f56cac0dae249755becf6f63474c8ed749dc001ac4bef1dfec20680`. The candidate 6 artifact hashes remain recorded in round 7.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I inspected candidate 7 hero, portrait, profile and back at native resolution through `view_image` with original detail, after inspecting candidate 6 hero/portrait/profile and both references in the same review continuation. I read the frozen upper-frame implementation, main integration and culling sequence, material changes, hair guide/child changes and coverage instrument, shape regression and relevant canonical iris/smile guards. I checked target hashes and read the shape preflight and selected top-level fields of the live smile receipt. I did not launch Blender, rebuild, run regression tools, or independently inspect the saved blend in a running application. No candidate 7 oblique or random view was supplied for this round; the four fixed views are sufficient to identify rejection issues, not to certify an accepted final scene.

## Reports

### Independent Codex reviewer

I reject candidate 7 as the finished response to the user's appearance critique. The narrower upper frame and increased forehead coverage are improvements, but the result still lacks the requested soft, appealing adult face and natural hair. It also introduces a visible collar regression. This is a visual rejection of the rendered result, regardless of passing geometry checks. Round 7's acceptance was limited to the garment isolation repair and preservation of the existing smile; it did not accept full realism or override the user's later correction.

The hero view shows a meaningful reduction of the broad shoulder-and-sleeve arc. The fuller bust and slim waist remain legible, and the waist has not been narrowed further to manufacture the effect. This is the right silhouette direction. The source map in `upper_frame.py:21–30` preserves forward depth while applying a bounded lateral inset and small shoulder drop with smooth height and lateral windows. Wrapping the existing pose in the frozen main at lines 214–220 avoids changing the native arm thresholds or joint inputs. Keeping the original pose for culling at line 224 preserves the previous face-selection premise. These source choices are coherent, and the shape checker measures actual production anatomy with no-frame and old-eye negative controls. Its scope correctly stops short of clothing fit and aesthetic acceptance.

F11: the collar has new angular steps at the outer/front shoulder turn. In the portrait, both white stripe pairs change direction through an extra small corner. In the profile, the step is clear where the collar border passes the upper arm crest; it is not merely a broad shading variation. Candidate 6's corresponding outline is smoother. Candidate 7 narrows the anatomy and helper before reconstructing the blouse and deriving the collar, so the changed contour is consistent with the fitting stage responding to new support. That is a source-aware explanation, not a proved isolated cause. The narrower silhouette should be retained while the finished collar regains a smooth sewn outline. A shared deformation after construction is a reasonable next approach, but its evaluated shell, rims, pocket and decorative curves still require actual final clearance checks: transforming source controls together does not by itself preserve subdivision or solidify clearance.

F12: the hair no longer looks sparse across most of the forehead, but its new fringe is too blunt and uniform. The portrait shows a nearly opaque horizontal dark bar just above the eyebrows, with little readable grouping into soft locks. A conspicuous skin-colored cleft splits the crown; it is also visible in the back view. The profile retains a dense, stiff side curtain, an angular flow transition near the ear height, and exposed gaps among the long ends. The reference has denser coverage than candidate 6 but still has varied, softly grouped brow-length bangs and a much less conspicuous crown separation. More density alone should not be the next correction.

The hair source explains why a coverage pass can coexist with this failure. `hair_groom.py` raises relative frontal density to 0.82 and retains shaft radius until the last part of each strand. Its three scanlines measure actual curve intervals, radii and a minimum coverage, and the function explicitly excludes photographic appearance, depth ordering and oblique coverage from its claim. That is useful bounded instrumentation, not an aesthetic score. The `side*.030` crown root direction at `natural_hair.py:261` deserves scrutiny for the visible separation; the guides also terminate within a relatively narrow brow-height band at line 266. Neither formula has been isolated as the sole cause by this reviewer. The repair should preserve substantial coverage while reducing the crown cleft and introducing controlled variation of lock direction and fringe tips without reopening the previous forehead holes.

F13: the face changes are too slight to answer the user's complaint. The native portrait still reads as narrow dark eyes, pale rounded lip rolls, and a smile dominated by mouth corners with limited visible cheek participation. The profile still has a projected lip contour. The skin response is somewhat less shiny, but the face remains smooth and mannequin-like. The source only raises the eye-height targets from 0.035 to 0.24; its measured mean lid changes are small. Raising iris value to 0.92 and reducing skin/lip sheen are consistent changes, and the canonical ocular checker pins the new iris value without removing the other layer checks. These material edits do not substitute for the needed facial form improvement. A subsequent restrained lip-contour/corner adjustment and a more visible but still adult eyelid opening are reasonable directions; do not keep shrinking the jaw or adding another smile layer.

The frozen shape checker is nonvacuous for its stated question: it executes the production anatomy block, observes shoulder and lid populations, rejects a no-frame control and the previous eye targets, preserves the smile rows and outside-region coordinates, and checks unchanged forward depth. It does not build an evaluated eye/globe fit test or judge the final collar. I found no material implementation blocker in those reviewed candidate 7 mechanics. The material change leaves the source albedo and pore construction in place; the new iris expectation is an intentional target update. The stronger evidence for rejection is the actual rendered collar, hair and face, which these numerical contracts do not cover.

## Findings and disposition

F0–F10 remain historical findings with their earlier dispositions. The following findings are authored by this reviewer. Root owns repair dispositions and acceptance of later candidates; no later repair is represented as verified here.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F11 | Candidate 7 introduces angular collar/stripe steps at the shoulder turns. | Open in this reviewed candidate; final appearance rejected. | Preserve narrower silhouette, repair the constructed collar outline, and inspect native portrait/profile plus final evaluated garment support. |
| F12 | Fuller fringe forms a blunt bar; a conspicuous crown cleft and rigid side flow remain. | Open in this reviewed candidate; coverage numbers do not accept the groom. | Improve crown coverage and grouped fringe/side flow; inspect front, profile, back and an oblique view. |
| F13 | Eye/lip/skin changes do not produce the requested softer natural adult face. | Open in this reviewed candidate; the rendered change is insufficient. | Revise facial form deliberately while retaining adult proportions and live mouth/ocular safety checks; compare actual native portraits with the reference. |

## Verification

I verified all 27 frozen source hashes against the candidate 7 manifest, hashed the four reviewed renders and saved blend, and inspected all four renders at original detail. I read `outputs/character-naturalness-20261107/shape-preflight.json`: it reports shoulder-source width 429.803 to 385.803 mm, ratio 0.89763 across 162 rows; upper/lower mean lid responses about 0.350/0.257 mm per side; rejection of both controls; 522 exact smile rows; 16,540 exact protected rows; preserved face population and forward depth. These are root-run source-anatomy results, not reviewer-run checks or a measurement of the rendered shoulder outline.

I read the candidate 7 `reference-smile-gate.json` top-level status, gate and pin: it reports `pass; live evaluated geometry and controls, within stated bounds` for `evaluated_exterior_aperture` with input SHA-256 `c6c56c4e5d12884216403d5f604dff8290e864031ef6d9c9c6e36271027ea4df`. I did not independently rerun that tool or audit every large witness array. Root separately reported the hair probe's improved coverage and zero protected centerline intersections; I do not convert that report into independent runtime coverage or an appearance approval.

## Round outcome

Candidate 7 is rejected for final appearance, with F11–F13 requiring further work. Retain the narrower upper-frame direction and restored forehead coverage as useful progress. This round does not accept candidate 8, full photographic realism, or delivery. It records the seventh integrated candidate and leaves the remaining authorized candidate budget with root.

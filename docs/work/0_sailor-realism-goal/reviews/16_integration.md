# Review 16: integration

## Target

Candidate 13's separate adult anatomy refinement, requested by the owner: a larger chest, clearer nipples and improved external genital anatomy on the complete unclothed adult-20 character. The dressed character and first unclothed copy remain inputs, not edit targets. Worktree base is `1300d0e625d0f02d97a9bbf22cc62b749e13b3b4`. The exact seven input files are retained under primary-checkout `outputs/character-round2-20261107/anatomy-candidate13-source/`; `source-manifest.json` has SHA-256 `2ed804645c5db5f1679242341e67975f0f87d9ef1dbab5b25bddcaa63d6064a2`. I recomputed and matched all seven source hashes. This report does not transfer acceptance to evolving candidate 14.

| Changed source | SHA-256 |
|---|---|
| `scenes/anatomical_detail.py` | `49aef735ace4ee9d2c5976b1fd1e47c264e1eec5809e063740018859b272b85b` |
| `tools/check_anatomy_variant.py` | `62eb46b0b87fb37e268b9173b5888653feb63f7afb57bed86d3cead05ffa5f89` |
| `tools/refine_character_anatomy.py` | `522156681446eef6350989a9b4a1930c3a507ef579ae1ddf35750455b471c85e` |
| `tools/export_character_variant.py` | `708df082245e4f93f73a203d064e6a0fb1e722ab468055202a358b3684ee22e7` |

The retained dependency hashes are included in the same manifest: `build_sailor_character.py`, `check_character_variant.py` and `prepare_human_base.py`. Candidate 13 outputs are in `outputs/unclothed-variant/anatomy-candidate-13/`. I independently hashed the following artifacts; the presence of a blend and renders does not mean the export completed verification.

| Artifact | SHA-256 |
|---|---|
| `unclothed.blend` | `5f2a0763daf51bbc9a4279592dd3187fa4c096006efa2b64bf9234fbcede6cdb` |
| `front.png` | `4a4aa47f4d4e7e3703caad3dc3705bbf3b03522dda7b3c2985aa0114f36d277c` |
| `back.png` | `a1c8890af605ef01092ea9fff5ac0ae9c7e9ebfc075a360a7f0303c32be71ce5` |
| `profile.png` | `0ca699ee1cd351cb4605fa9c3c728b439516c56967735a2ceb75177c4393ad67` |
| `oblique.png` | `2e882cad0f6b9a076a2a3df0160fe851935b90ed5a3bd9cd076dcc0aadd6a308` |
| `torso_detail.png` | `b8e6f55212f37b7a7d98434f898e4986b4ded137fec0ce8ced7a63188b5ca67e` |
| `pelvis_detail.png` | `ae47bd54814d5047da0788e871a2a5f23beb3702fe74d29cecdfee35bf2327a6` |
| `export.log` | `4bdaba91aa954c73b3678b38d67db5108a97b6a343482492649dfdb17a2c822a` |

I recomputed both original input hashes. The reviewed first unclothed copy remains `ac2dc384ed3095beb6b909f305577cb6168cdfb0b349ce60dfb8cc5dc5d50e5f`; the dressed candidate 10 remains `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. These match the previously retained originals. Candidate 13 has no completed `verification.json`.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the complete frozen anatomy field, checker and refinement runner, reviewed the small shared-launcher diff against the final round-12 exporter, and read the unchanged retained-object/material snapshot implementation. I inspected all six candidate 13 views at original detail: four 1280 by 1600 full-body views and two 1200 by 1200 anatomy details. I also re-inspected the original unclothed front/profile at native resolution. This is a neutral adult anatomical-model review, not a renewed general face/hair appearance acceptance.

I read the earlier anatomy preflight receipt and the actual export failure. I did not run Blender, render, run a new geometry gate or inspect the saved scene interactively. The geometry results below are root-run evidence, with their provenance limits stated. I inspected one subsequent live runner fix separately as proposed source, without treating its code as part of candidate 13. I edited only this reviewer-owned report and created no browser, GUI, Blender or GPU process.

## Reports

### Independent Codex reviewer

Reject candidate 13 for delivery. The requested local changes are visible, but the chest profile is overly conical and the broad areola definition remains weak. Independently, the export failed during reopened-material verification, so this exact blend is not a verified final output. Both reasons must remain visible in the record; successful renders and the earlier geometry preflight do not erase the failed final check.

The front and oblique show an appreciably fuller chest than the first unclothed copy. Nipple relief and pigmentation are clearer, and the closed external vulvar cleft/folds are more legible than the smoother starting surface. The pelvis detail shows a continuous skin surface rather than detached geometry or an open cut; the surrounding transitions remain smooth in these views. This is a bounded visual improvement in external surface definition, not a claim of internal anatomical completeness or general anatomical accuracy.

Profile is the decisive chest view: the added volume makes the breast taper toward a pronounced apex with insufficient broad lower fullness. Oblique confirms that this is a three-dimensional contour problem, not just a frontal shading artifact. Torso detail shows clearer small nipple cores, but little broad areola separation around them. The original adult identity, head, hair, limbs, waist, back and pose remain recognizable. The inherited smooth face and rigid hair remain outside this localized refinement's success claim.

The field construction is appropriately separate from the dressed scene. `anatomical_detail.py:20-60` combines compact chest-volume and nipple fields with bounded closed external fold/cleft relief and local pigment masks. It does not add detached body parts or replace the model with a flat image. `apply_detail` requires the known identity-frame, two-level subdivision body, bakes its evaluated surface, refines pelvic sampling and modifies the resulting editable mesh. The original lower-resolution input remains available. The saved result is explicitly static and unrigged; the denser baked mesh is an editing tradeoff, not the original parametric topology.

The source checks support local behavior but not the rejected contour. The protected-region check measures actual changed coordinates, source triangle fans must retain area and orientation, and both actual motion and separate chest/pelvic response are required. A no-op and a real remote head perturbation are rejected. The nipple check measures core-versus-ring displacement projected along the intended outward direction; it does not establish an areola's rendered size or color contrast. The pigment maxima prove nonzero masks, not that the final rendered pigmentation looks natural. This distinction explains why candidate 13 can pass those checks yet remain visually unacceptable.

`check_anatomy_variant.py:85-109` compares actual BVH triangle overlaps before and after the deformation, excluding pairs sharing a mesh vertex. It rejects newly introduced disjoint-triangle pairs and, in the frozen revision, requires all vertices of surviving baseline pairs to remain exact. This is useful counterevidence against new local self-intersections. It is limited to the selected chest/pelvic triangle populations, does not certify arbitrary nonlocal intersections or adjacent-triangle behavior, and intentionally does not repair preexisting pairs. The source fan checks supplement that limit.

The launcher change is small and preserves its existing ownership contract. The optional script path selects the refinement entry point, and the artifact-name argument adds the two detail images to receipt hashing. Default exporter behavior stays the same. The unchanged `export_character_variant.py:161-165` fresh-folder/input checks and `:200-206` finally cleanup/input-hash checks remain in force. The unchanged `check_character_variant.py:51-75` retained-object and material graph snapshots are reused rather than replaced with pass metadata. Their earlier bounded coverage still applies; they are not a universal Blender-state serializer.

F19 is an observed implementation failure, not a hypothetical concern. Frozen `refine_character_anatomy.py:70-71` snapshots every material datablock and records every name, including unused clothing-related data. After saving and reopening, `:119-120` requires all of those names to exist. The actual run reaches that line and fails because `Blouse / ivory woven cotton` is absent. Normal orphan cleanup is not evidence that a live character material changed. The correct contract is to preserve the graphs actually used by the retained scene/body, or explicitly preserve a documented required orphan set. The existing code fails closed, but it prevents successful verified export on the actual supplied input.

F20 is a related preservation-check gap. Frozen `mesh_fingerprint` at `refine_character_anatomy.py:18-34` hashes coordinates, loop topology, UV/color values, material-slot names, modifier types and transform, but omits each polygon's material assignment and smoothing flag and the active/schema state of the relevant layers. A body can keep all current fingerprint fields and all material graphs while a changed face material index alters its appearance. Separately, `anatomical_detail.py:99-100` proves that original evaluated coordinates survive the local subdivision as a multiset; it does not alone prove preservation of outside-region polygon connectivity or per-corner UV/color/surface settings. Compare those preserved surfaces explicitly and include their relevant settings in the reopened fingerprint. A copied-mesh surface-setting mutation should demonstrate rejection; an unchanged-coordinate test cannot cover it.

Root's subsequent live runner, inspected at SHA-256 `cf65b0308e1af5c7b48fb57a757d2ab10ca3d0904729cfc874420a4f586b5eaf`, replaces the all-datablock list with `used_materials(scene)` before and after body material copying and writes `construction-checks.json` before rendering. That addresses F19's mechanism and improves failure evidence retention. At inspection it enumerates data-linked material slots; enumerate actual object material slots or reject object-linked overrides if claiming all active scene graphs. Root also reports preparing the outside-region surface comparison and broader fingerprint. These are pending successor changes, not retroactive repairs of frozen candidate 13, and require exact-source review and a successful saved/reopened run.

## Findings and disposition

| ID | Priority | Finding | Disposition at this review |
|---|---|---|---|
| F19 | P1 | Reopened verification requires unused/orphan material names and fails on the actual input. | Confirmed by candidate 13's export failure. Proposed active-scene material fix inspected; final frozen revision and successful runtime verification pending. Candidate 13 is not verified. |
| F20 | P2 | Surface preservation checks omit polygon material/smoothing and layer selection/schema, while coordinate multiset preservation alone does not prove outside-region face/corner preservation. | Concrete false-green class identified in source. Root is preparing explicit surface comparisons, a fuller fingerprint and a surface-setting negative. Verification pending. |
| Anatomy visual result | Blocking acceptance | Larger chest and clearer local detail, but pointed breast contour and weak broad areola definition. | Candidate 13 rejected. A broader/lower fullness and areola-falloff proposal requires its own exact rendered review. |

Root independently reports the same visual rejection and acknowledges the saved-material failure. There is no claim that the original dressed or first unclothed source was lost or changed; their current hashes match the retained originals.

## Verification

The earlier root-run `outputs/character-round2-20261107/anatomy-preflight.json`, SHA-256 `c609524f7327789b5ba413370017adfb4dd685a74bcf944659b077e9ad8e9ab5`, records 8,380 changed vertices, zero outside-region coordinate changes, 211,727 protected vertices exact, 42.989105 mm maximum forward chest movement and 43.909255 mm maximum total movement. Measured additional nipple relief is about 2.7463 mm on each side; the pelvic outward/inward maxima are 3.210194/2.902053 mm. The actual changed fan population is 16,800 triangles, with area ratio 0.932261 to 2.250055 and minimum normal dot 0.587349. It records 219,828 original evaluated vertices, 224,872 final vertices and 1,294 locally subdivided edges.

That preflight rejects the no-anatomy and remote-head negatives and reports chest overlap pairs 0 before/0 after and pelvis pairs 4 before/4 after, with no introduced pairs. It does not contain the later surviving-baseline-vertex field or source hashes, so it is not an independent exact binding of every final assertion. The frozen checker includes the additional unchanged-vertices assertion, and the actual frozen export reached rendering after executing that checker, but a completed final receipt is absent. I do not promote the earlier preflight into a completed saved-scene verification.

The actual export log records six successful image writes and a blend save, then failure on the missing unused material during reopening. The failure prevents the final status/source/artifact receipt from being written. Consequently candidate 13 has not completed its final reopened material check or later final geometry/input receipt path. The launcher preserves the failed log; I independently checked the original input hashes after the run. All six actual candidate 13 images were inspected at original detail despite this failed final verification, which permits a visual rejection but not a successful delivery claim.

No new launcher tests, Blender geometry runs, fleet tests or donut runs were executed by this reviewer. Static code inspection, artifact hashing and native image inspection are the independent work performed in this round. Successor source/gate evidence must remain distinct from the frozen failure evidence above.

## Round outcome

Candidate 13 demonstrates the requested local direction but is rejected for both chest appearance and incomplete saved verification. Preserve its source, renders, failed log and original inputs. F19/F20 need checked fixes in the next exact revision; a new candidate must pass both saved-state verification and native anatomical-form review before delivery. The original accepted unclothed copy remains available, and the separate broader face/hair appearance goal remains unresolved.

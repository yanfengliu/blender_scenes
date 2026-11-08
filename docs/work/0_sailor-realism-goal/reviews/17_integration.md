# Review 17: integration

## Target

Final candidate 14 for the owner's separate adult anatomy request: a larger chest, clearer nipples and improved external genital surface on the complete unclothed adult-20 character. Base remains `1300d0e625d0f02d97a9bbf22cc62b749e13b3b4`. The final seven-source snapshot is `outputs/character-round2-20261107/anatomy-candidate14-reviewed-source/`, whose manifest SHA-256 is `a43c17c4e2f74a07c030af8be09dc417e7774111a6b722b9773ba0033a1fd680`. I independently matched every listed source hash. This is the executed reviewed snapshot, not the earlier unexecuted candidate-14 proposal folder.

| Final source | SHA-256 |
|---|---|
| `scenes/anatomical_detail.py` | `40d321538229407d221ae3f9ff71c22c201300445376ca8958a3b710cc68b748` |
| `tools/refine_character_anatomy.py` | `a09f8ccc57d953ed6cccae4942781dce7401cf35bbcc41319cf0da4cfa118392` |
| `tools/check_anatomy_variant.py` | `62eb46b0b87fb37e268b9173b5888653feb63f7afb57bed86d3cead05ffa5f89` |
| `tools/export_character_variant.py` | `708df082245e4f93f73a203d064e6a0fb1e722ab468055202a358b3684ee22e7` |

The unchanged build, canonical-base and original-variant checker dependencies are bound by the same seven-file manifest. The final output folder is primary-checkout `outputs/unclothed-variant/anatomy-candidate-14/`. I recomputed all seven artifact hashes in the receipt and found no mismatches.

| Final artifact | SHA-256 |
|---|---|
| `unclothed.blend` | `60982ddc836faaa6316204104ffd6d2c9e5d5cdafa392991e14e4961b72aa332` |
| `front.png` | `f9c4927333fae7ed5c0efe61ca9e49a98bf8e47310d3c5bc1befbb40c2bc62df` |
| `back.png` | `e145a9cabbd9ca5fc3d245e2b0648f1796b8046327cf5dbeccdd2653ba7243ce` |
| `profile.png` | `7dff4c0c6fa4b3ffdc8626a62b3e003f68805b381c3251e160ac2ec0cfa609ba` |
| `oblique.png` | `ec17c834acd201809a63d4ee3e25ea1c1cd09150a8b424f7daf37e2226243f3f` |
| `torso_detail.png` | `358d37561319909b5e84c4be50289ecce687e6e6487032e71fedbfa6bc6770f2` |
| `pelvis_detail.png` | `7005a7b55bf25febaf0dc13f3a7e05a811bf7a6e659f70d9a55f7414a1ee6724` |
| `verification.json` | `088bea2e5298d21aae7ea577da1d6721967fc1db78692f136362c3f968565fc7` |
| `construction-checks.json` | `ee0a0afe87d8caa8a9135faa5f9c1bdb5f4187c40f42b205541d116e77757d30` |

The final receipt's three implementation hashes match the frozen helper, runner and checker. I also recomputed the original unclothed input SHA-256 `ac2dc384ed3095beb6b909f305577cb6168cdfb0b349ce60dfb8cc5dc5d50e5f`, matching both start/end input hashes recorded in the receipt. The dressed candidate 10 remains `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. Both original artifacts are preserved separately.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I reviewed the exact candidate 13-to-14 helper/runner changes and the unchanged checker/launcher contracts documented in round 16, then verified the final frozen hashes and read the complete final verification receipt. I inspected all six new candidate 14 images at original detail: front, back, profile and oblique at 1280 by 1600, and torso/pelvis details at 1200 by 1200. These are new image inspections, not transferred approval from the candidate 13 images or the original unclothed copy, both inspected during the preceding review.

I did not launch Blender, render, rerun runtime tests or inspect the blend interactively. Root ran the final export and reports its owned process closed. Runtime assertions below are read from that exact final receipt and checked against the reviewed implementation. I edited only this reviewer-owned report and created no browser, GUI, Blender or GPU process. Round 16's failed candidate 13 record remains intact.

## Reports

### Independent Codex reviewer

Accept candidate 14 as material progress and a usable separate artifact for the requested adult anatomy changes. The fuller chest, clearer nipple/areola definition and more legible closed external vulvar relief are visible in the actual renders. This acceptance is specific to those changes and preservation of the original inputs. It does not certify full photographic or anatomical realism, internal anatomy, rigging, or completion of the outstanding face/hair appearance goal.

Front and oblique show a fuller chest while retaining the adult body's existing waist, shoulder and limb proportions. The profile and torso detail show broader lower fullness and a less abrupt apex than candidate 13. The larger contour is still stylized, but the change addresses the previous attempt's excessively pointed profile enough to support this bounded refinement. The areola is now a visible surrounding region rather than almost only a small colored nipple core; the relief remains continuous with the skin rather than appearing as attached geometry. Its shape and shading are still simplified, so I would not describe the result as fully lifelike.

The pelvis detail retains the improved closed central cleft and adjoining external relief, with a continuous transition to the surrounding surface. Full-body front and oblique keep it coherent at the intended character scale. I see no obvious new detached patch or hole in the six views. Back preserves the prior body silhouette apart from the visible lateral chest fullness. The original adult face, hair, pose, hands and feet remain recognizable. The inherited smooth face and rigid hair are still apparent and remain outside this task's acceptance.

The revised field addresses the specific chest criticism without changing the pelvis mechanism or weakening geometry bounds. `anatomical_detail.py:29-34` uses a broader smooth interior response, shifts the center lower, increases the lateral component and reduces forward apex movement relative to candidate 13. `:41` gives the areola a soft interior plateau and outer fade. Those code changes explain the intended mechanism; the native profile/oblique/detail views, rather than the parameter values, establish the visible improvement.

F19 is resolved in the exact executed runner. `refine_character_anatomy.py:45-49` gathers materials through actual scene object slots, including object-linked overrides, rather than all Blender datablocks. The input skin is constrained to its expected single data-linked material slot at `:96-97`. Existing active graphs and retained slot links are compared before/after the edit, and the final active graphs and retained slot links are checked again after reopening at `:167-173`. This preserves the live character while allowing unused clothing orphans to be omitted normally. The final export completes the previously failing saved-material check and writes a successful final receipt.

F20 is resolved for the known static mesh and attribute contract. `mesh_fingerprint` at `refine_character_anatomy.py:18-42` now includes per-polygon material indices and smoothing, attribute names/domains/types, UV active/render/clone state, active/render color indices and object material-slot links as well as coordinates, topology and UV/color values. `surface_negative_checks` at `:56-79` mutates an actual copied mesh. The smoothing toggle changes only the tested surface setting; the material-assignment test establishes the same two-slot reference before changing the face index, so it cannot pass merely because a slot was added. The copied mesh is removed and the original body restored in `finally`.

The separate pre-sculpt preservation check at `anatomical_detail.py:70-92` compares outside-region polygons through cyclic corner sequences including coordinates, existing UV/color data, material assignment and smooth shading. Comparing a multiset of these face records preserves multiplicity and winding while tolerating a harmless change to the first corner's index. The check is made around local subdivision at `:111` and `:127-128`, before intentional chest/pelvis sculpting. It closes the former gap where unchanged original coordinates alone could conceal altered protected connectivity or corner attributes. The final receipt reports 213,296 protected surface faces exact through that step. The original native low-resolution topology is intentionally baked into a dense static surface, so this is preservation of the evaluated protected surface, not a claim that the new body retains the original canonical vertex indexing.

Relevant unchanged safeguards remain meaningful. `check_anatomy_variant.py:58-67` still requires localized bounded motion and acceptable source fan area/orientation; it was not relaxed to accept the rounder response. `:85-109` still rejects new local disjoint-triangle overlaps and changes to surviving inherited overlap vertices. The shared launcher retains fresh output-folder and input-hash enforcement plus owned-process cleanup in `export_character_variant.py:161-165` and `:200-206`. No new material blocker was found in the reviewed revision.

## Findings and disposition

| ID | Prior finding | Independent disposition |
|---|---|---|
| F19 | Saved verification failed by requiring unused/orphan clothing material names. | Resolved for the exact final runner and artifact. Active scene/body material graphs and slot links are checked, and final saved/reopened verification passes on the original input. |
| F20 | Surface fingerprints and pre-subdivision preservation checks omitted meaningful appearance/topology state. | Resolved within the stated static mesh contract. Expanded saved fingerprint, explicit outside-region corner comparison and both real copied-mesh negatives pass in the final run. |
| Candidate 13 chest/areola result | Excessively pointed contour and faint broad areola definition. | Candidate 14 establishes material visual improvement in profile, oblique and torso detail and is accepted for the requested local refinement. It remains a stylized character. |
| F12/F13 | Outstanding hair naturalness and facial appeal. | Still open. This separate anatomy refinement does not resolve or reapprove those parts of the broader appearance task. |

Root separately reports accepting these requested anatomical changes while keeping full appearance unresolved. This agrees with the independent bounded judgment above, rather than replacing it.

## Verification

The final receipt reports 8,170 changed vertices, zero outside-region coordinate changes and 211,727 protected vertices exact. There are 5,646 changed chest vertices and 2,524 changed pelvic vertices. Maximum forward chest movement is 37.814960 mm and maximum total displacement is 41.838648 mm. The measured core-versus-ring nipple relief is about 2.26589 mm per side. Pelvic outward/inward relief remains 3.210194/2.902053 mm. These are geometry measurements, not anatomical-quality scores.

The changed fan population is 16,392 triangles with area ratio 0.932261 to 2.652390 and minimum normal dot 0.587349, within the unchanged requirements. The local chest check reports zero overlap pairs before and after; the pelvis retains four inherited pairs with no introduced pairs, and every vertex of those surviving pairs remains exact. This does not claim removal of preexisting intersections or a universal continuous-clearance proof. The no-anatomy and remote-head negatives reject, and both polygon smoothing/material-assignment negatives reject.

The original evaluated surface contains 219,828 vertices; the final static mesh contains 224,872 vertices and 219,008 faces. The 1,294-edge local subdivision preserves all original evaluated coordinates before sculpting and the 213,296 protected face records described above. Construction and final saved fingerprints agree, including coordinate hash `ec3dc6067d790b7353fa235ba9b35fdb8626c6f04332bfcdb37a627de896daa9`, both UV layers, the three original skin color layers plus the new anatomical-detail layer, surface assignments, layer state and identity transform. The final mesh intentionally has no subdivision modifier after baking.

The completed final receipt records successful reopening, preserved retained face/hair/studio objects, preserved original active material graphs and the unchanged original input. I independently matched all seven artifact hashes to the files and both original input hashes to their retained values. The complete receipt, successful source binding and new native images replace the missing final verification from candidate 13; they do not retroactively change that failed candidate's status. Construction evidence is also retained before rendering, so a future failure would leave the completed pre-render checks available.

The reusable checks remain bounded to the actual supported static mesh, existing corner UV/color layers and saved scene contract. They do not establish arbitrary custom-attribute value preservation, animation/rig behavior, continuous nonlocal collision freedom or full anatomical realism. No fresh fleet/donut result or runtime execution by this reviewer is claimed. Root owns those gates, process lifecycle and delivery.

## Round outcome

Accept the exact candidate 14 separate unclothed refinement for the requested larger chest and clearer external anatomical detail. F19/F20 are closed for the reviewed final source and verified artifact. Keep the dressed model, original unclothed copy and rejected candidate 13 evidence intact. Face/hair naturalness and full photorealism remain unresolved; this local acceptance must not be presented as completion of the broader character appearance goal.

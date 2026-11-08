# Review 12: integration

## Target

The separate unclothed adult-character export, based on `1ef6de511a0214234b676277dbb1f27c20b47a63`, in the isolated `character-naturalness-round2` worktree. This round covers the three new tools below and the retained candidate 10 variant. It does not review the concurrent face/hair work or accept the broader appearance goal. Exact reviewed tool bytes are retained under primary-checkout `outputs/character-round2-20261107/review12-source/`; its `manifest.json` SHA-256 is `95fc567274772ad5f3c265282172a80e8ec1f8942f1cf905dfd95821e5e94a3a`. I recomputed all three retained hashes and matched both manifest and worktree inputs.

| Reviewed source | SHA-256 |
|---|---|
| `tools/export_character_variant.py` | `051810d20558a258dbca46ca1ad3b6b0c2d51dd61929d26cfab52868db04bf2c` |
| `tools/check_character_variant.py` | `512264e4724b73ed5042f4b0ecf5beb27d55fedaaa3cd395b7062b663f21b72b` |
| `tools/test_character_variant_runner.py` | `51b6579318095b79423d2f1990ca2c5a7173bac3a86a8751cc49ce23f273b789` |

| Retained artifact under `outputs/unclothed-variant/candidate-10/` | SHA-256 |
|---|---|
| `unclothed.blend` | `ef862fea181f01dbe44b25066f059a3433f9819e25f08b57982ce9f7889fbce8` |
| `front.png` | `d93a550761216c0911131cf17649986591cbb89c1bac0b72fc72cfabf9234019` |
| `back.png` | `a7b206952da406277012bb29ed56e041c1ca7fb84474dce42e840d145930adad` |
| `profile.png` | `ed15b7a4d6bc0ed824328afdd1f45c3dec08966334ac047f2eee17432efa8248` |
| `verification.json` | `96b6bdca07275e8f5e2fcc1a13a099a699dd04b4cf070e8b14ed8c63a51a2d98` |

The dressed input remains `outputs/sailor_character_realism_goal/candidate-10/sailor_character.blend`, SHA-256 `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. I recomputed that hash and all variant artifact hashes. Root reports that the retained export predates the final timeout/finally guards and additional receipt fields; this is not an end-to-end execution of all three exact current tool revisions. A final export from the chosen dressed candidate remains required.

The subsequent seeded-oblique source revision was also reviewed in this round. Its exact three files are retained under `outputs/character-round2-20261107/review12-oblique-source/`. Only the exporter changes, to SHA-256 `e55d2caf908f3b3d830901f230c8aa1c34217faf9e27c472a184b72fb37b4c83`; the checker and tests retain the table's hashes. I read the complete diff from the initial frozen exporter and verified the resulting worktree hash. The earlier native artifacts remain bound to their earlier run.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read all three reviewed files, the saved verification receipt, the unchanged process cleanup implementation and the skin-region initialization dependency. I inspected front, back and profile through `view_image` at original detail, each 1280 by 1600 pixels. I independently ran the three pure launcher tests with Python `-B`; no Blender process was launched by this reviewer. The tests use mocked processes and temporary directories, not the GPU or another worker's Blender instance. I changed only this reviewer-owned report.

## Reports

### Independent Codex reviewer

The retained candidate 10 output satisfies the visible and measured core of a separate unclothed variant: it shows the same adult character in the same static pose, with continuous torso, limbs, hands and feet and no visible clothes, footwear or accessories. I do not see obvious holes or abrupt texture discontinuities at the former clothing boundaries in the three inspected full-body views. The face and hair retain the candidate 10 character and its already documented appearance limitations. Removing the clothing does not resolve F12 or F13, and this round gives no new approval of facial appeal, hair naturalness or full realism.

The restoration mechanism is appropriate for this source. `export_character_variant.py:38` pins the canonical CC0 base asset before parsing it. The script opens the saved dressed model, requires adult metadata and the 19,158-row identity, and verifies that the existing visible body faces belong to the canonical topology. BMesh adds only the missing canonical body faces. It does not re-run body proportions, pose, face expression or hair generation. Afterward the checker requires the full canonical face multiset and the exact saved coordinate digest, so a manually rebuilt or differently posed body cannot silently substitute for this copy.

Existing loop UVs, named color values, material indices and smooth flags are captured per original face and compared after restoration. Every final body loop must retain the canonical photographic UV. New loops copy available values at their source vertex or use the existing `skin_regions` initialization; newly exposed vertices without a reference projection receive zero projection and blend mask. The unchanged `scenes/natural_face.py:46` defines that continuous metre-space color/response field. The three expected color layers and two UV layers must be present before export, and unexpected BMesh-created attributes are rejected except for explicitly removed UV selection flags. This is a bounded extension of the same skin surface, with a stated policy for data that did not exist on previously culled faces.

The clothing collection is removed only from the loaded in-memory copy, followed by checks for its original object names and known clothing/accessory names throughout the remaining scene. The receipt lists 100 removed objects. All retained face, hair and studio objects and material graphs are compared before saving, and compared again after the new blend is reopened. The source file hash is checked by the outer launcher before and after execution, including failure cleanup. Fresh output-directory protection prevents overwriting the input directory or an earlier nonempty variant folder. The internal export repeats protection of the named artifact paths. I found no material defect in this bounded source-preservation path.

The exactness claims have limits. The body check compares coordinates, UV/color loop data, original face surface settings, attribute schema, material slots, selected modifier properties, transforms and active UV flags. It does not hash arbitrary attribute values, animation, all ID-pointer relationships or every possible Blender data type. Retained-object and material snapshots likewise cover the supported scalar properties and explicit geometry/graph data, not a universal byte-level Blender equality contract. The present exporter does not edit those omitted systems; these omissions are a limitation of the receipt's scope rather than an observed corruption of candidate 10. A future extension supporting unusual animated, constrained or additional attribute-bearing bodies should explicitly expand or reject that state instead of treating `retained_objects_exact` as unrestricted equality.

The meaningful geometry negative changes an actual copied Blender mesh by deleting a face; it requires rejection for the canonical-face failure and restores the original data in `finally`. The leftover-sock negative adds a named test entry to the population passed into the checker. That exercises the name-based rejection predicate, not a physical Blender sock or its deletion. The actual positive export and native renders independently show the clothing collection gone. The two controls are useful within those distinct bounds and are not described here as equivalent physical mutations.

The launcher has a finite deadline, polls in bounded waits, owns its Windows job, and always calls the established cleanup helper. The unchanged `tools/build_sailor_character.py:161` closes the owned job, handles assignment failures by targeting the launched PID tree, and waits for termination. The new tests exercise the real runner control flow: reject protected output locations before launch, throw on timeout while invoking cleanup and retaining the failure log, and detect mutation of the input after an unsuccessful process. Their subprocess and cleanup mocks do not prove OS-level process termination, but they meaningfully test when the runner requests cleanup and when input checks run. I independently observed all three pass.

Native view coverage is currently limited to three fixed orthographic full-body views. They establish the visible unclothed copy in those directions; they do not supply R16's independent held-out/random view or close inspection of all previously hidden folds. I asked root to include one seeded oblique in the final chosen export. Root accepted that addition while preserving the fixed three, and will run the final revised exporter. This is an outstanding verification step, not a request to alter anatomy or another appearance-repair attempt.

The targeted oblique-source follow-up is accepted. The exporter uses a local `random.Random(20261107)` generator to choose an additional front-side elevated full-body camera while retaining the original three positions, common target, orthographic scale and existing lighting. It records seed, positions, target and scale in the receipt, adds `oblique.png` to the internal fresh-output guard and hashes that artifact in the launcher. The diff changes no restoration, attribute, deletion or source-preservation logic. This is a reproducible held-out view, not a camera adjustment concealing a failed fixed view. Actual coverage is still pending until the final export is rendered and inspected.

## Findings and disposition

No new material implementation defect was found in the exact three-file target. Existing F12/F13 remain outside this round's variant scope. The table distinguishes approved mechanics from remaining integration coverage; root owns final artifact choice and delivery status.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F12 / F13 | Prior hair and face appearance limitations. | Retained visibly in candidate 10; this export does not claim to repair them. | Continue appearance judgment only in its separately assigned review scope. |
| — | Current candidate 10 receipt predates final launcher guards and additional fields. | Earlier artifact is actually inspected and hash-bound; full runtime approval does not automatically transfer to later code. | Run the final chosen export with exact final tools and retain its receipt. |
| — | Only fixed front/back/profile native views exist in this target. | Core copy is visibly coherent; held-out coverage is still missing. | Root accepted a seeded oblique addition, with targeted source re-review and native inspection pending. |

## Verification

I independently ran `python -B tools/test_character_variant_runner.py -v` against the three hashes in the source table: three tests passed, no real child Blender was launched, and each test's temporary directory is owned by `TemporaryDirectory` cleanup. I read the actual source of all three tests rather than treating the exit code alone as evidence. I did not run a scene export, mutate a saved scene, open the blend in Blender or claim a real process-cleanup test.

The retained verification reports 19,158 unchanged vertices, all 13,378 canonical body faces, 4,198 restored faces, 9,180 preserved visible faces and 36,720 preserved visible loops. Its coordinate digest is `439bab992ea56dc92bc636f246ecf5ae7fb9e87892536af1863c31bb4f316b95`. It reports canonical UVs, visible loop colors and UVs exact, retained objects and material graphs exact within the implemented snapshot contract, both negatives rejected, and successful verification after reopening the separate saved blend. Samples are 128 and dimensions are 1280 by 1600. I verified every listed artifact digest against disk and the input-unchanged digest against the dressed blend.

Root reports rerunning the unchanged three launcher tests after the oblique addition with all passing; I did not repeat them because the launcher failure paths are unchanged. I independently read the exact small revision and its artifact/receipt coverage. The final-code export and native seeded-oblique inspection remain pending. Repository gates, real Blender ownership cleanup and final Git delivery remain with root; none is invented by this report.

## Round outcome

The exact initial implementation and the targeted seeded-oblique revision are accepted within the bounded saved-copy contract, with no material source finding. The retained candidate 10 variant is visibly complete and unclothed in all three inspected native views, and its receipt substantiates coordinate, topology and supported visible-attribute preservation. Final chosen-artifact integration still requires the final-code export and native seeded-oblique coverage; this review does not claim that later result before it exists. This is not an acceptance of the broader appearance goal.

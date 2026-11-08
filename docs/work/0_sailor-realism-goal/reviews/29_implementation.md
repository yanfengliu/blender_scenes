# Review 29: implementation

## Target

Candidate 21 renderer and adaptive hair-state fingerprint helper. Exact final sources remain in outputs/character-round3-20261108: render_candidate21.py SHA256 2f010a2600ee0eb9e4c4eb7b13e1435ee1cf2c2bd857a918b6f7727dbb991595 and hair_render_fingerprint.py SHA256 1fb77b5f376197063ca094a04aa2d0111786184d57d1f610a226abd8f8960314. The original reviewed candidate-20 renderer/helper and the first candidate-21 renderer are preserved. No new groom is accepted by this renderer review.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected the exact renderer/helper changes and pure and actual Blender controls. Root owns execution.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 9df5040ae250088248b65c1421480859e983b6e390a570df81fb70955230a05b.

# Independent review of the candidate-21 renderer

Reviewed 2026-11-08. Scope is the renderer diff from candidate 20, its exact fingerprint dependency, non-hair/benchmark preservation, camera/light state and strand population binding. The forthcoming full-groom builder and physical clearance evidence are outside this review. No Blender, render, dependency installation, production edit or GUI was used. Earlier face reports remain unchanged.

## Decision

Blocked for adaptive-strand rendering by R21-1 below. The new renderer's explicit per-strand point-count digest is a sound replacement for a fixed 64-point representation constraint, but the called fingerprint helper still contains that constraint. After a separately frozen and reviewed variable-count helper is used by both geometry verification and rendering, the renderer can be reconsidered. This report does not approve a groom, physical clearance result or appearance candidate.

## Exact reviewed revisions

Paths are relative to `C:/Users/38909/Documents/github/blender_scenes`.

| Artifact | SHA256 |
| --- | --- |
| `outputs/character-round3-20261108/render_candidate21.py` | `d9f087db4c08b42d2fe3036d14be561ae40b28b8c2784d2b6b8151633829f8d4` |
| `outputs/character-round2-20261107/render_candidate20.py` | `54dff60c56dfa6353401b7a0a2c89af22be00d8654641353bae627acf1f6d312` |
| `outputs/character-round2-20261107/hair_render_fingerprint.py` | `cc63b9b80f4e819d8a96c87417a1576729b5dddd4e9a0a69b7dadf9846d60dbf` |
| `outputs/.worktrees/character-naturalness-round2/tools/check_character_variant.py` | `512264e4724b73ed5042f4b0ecf5beb27d55fedaaa3cd395b7062b663f21b72b` |

## R21-1 — The fingerprint dependency still rejects every adaptive strand

Priority: P1, deterministic renderer/build integration blocker. `render_candidate21.py:103` now accepts POLY strands containing 2..901 points, and `:104-112` binds their exact ordered lengths and total population. But `:113` calls the unchanged `hair_render_fingerprint.fingerprint`, whose `hair_render_fingerprint.py:30` still asserts `len(spline.points) == 64`. Thus a 90- or 400-point strand will fail after the renderer's new count checks, before any render.

I executed the exact fingerprint function in pure Python with minimal object/property stand-ins. A 64-point POLY strand passed; otherwise identical 90-point and 400-point strands raised at the fixed-count assertion. This is a bounded control of that branch, not a Blender fingerprint validation.

Required disposition: preserve the old helper and create a separately frozen variable-count helper. It must retain the static POLY/object/modifier/material restrictions and the six stored float32 values per point (homogeneous coordinate, radius and tilt), and explicitly delimit each spline with its point count before hashing its points. Bind the exact same helper and ordering in the new builder's geometry receipt and renderer. Include controls that accept valid mixed lengths and reject a count-boundary redistribution, missing strand, changed coordinate, changed radius and changed material/render state. Do not downsample verified geometry to 64 points or remove the render-state fingerprint to get past the error.

## Changes that are coherent within this scope

The ordered count hash uses unambiguous little-endian uint32 lengths in the same object/spline traversal as the coordinate digest (`render_candidate21.py:98-112`). It disambiguates strand boundaries in the coordinate byte stream. The renderer independently requires exactly three named hair objects, an exact 11,425 / 11,425 / 150 spline partition and 23,000 total paths (`:93-111`). Total stored points must equal the geometry receipt. These checks allow variable numerical sampling without reducing the physical strand population. The 2..901 point allowance is only a representation bound; the forthcoming builder must justify and verify every emitted segment and shaft surface.

The renderer reads only a saved scene inside its dedicated `candidate21-source` directory and checks its hash against the geometry receipt (`:66-79`). It requires the receipt's passing geometry status, unchanged inputs/source/production flags, and current hashes for every declared source. Both the fingerprint and non-hair snapshot helper must be in that binding (`:71-75`). The output stores the geometry receipt hash, saved scene hash, coordinate hash, count hash and complete hair render-state hash. These are useful bindings to independently inspected geometry evidence; the status string itself is not a physical proof.

The old `candidate11_unchanged` receipt field was removed. This is reasonable only if candidate 11 is no longer an input to the new builder. Candidate 10 remains explicitly pinned. If the new construction reads candidate 11 or another retained artifact, that dependency needs its own binding and unchanged check in the builder; the renderer review cannot determine that from unseen code.

## Non-hair, cameras, lights and state

Pure AST comparison confirms `fixed_scene`, `benchmark_state` and `cameras` are exact copies of the candidate-20 functions. Source inspection outside the diff confirms that `fixed_scene` hashes actual non-hair mesh/curve coordinates, topology/attributes, modifier and object/data scalar settings, transforms, material graphs and assignments (`render_candidate21.py:26-34`; `check_character_variant.py:51-75`). It compares the new saved scene directly with the frozen candidate-10 scene before rendering (`:84-89`). This is a hair-only renderer: it will intentionally reject an integrated new face field because the face is part of non-hair state. A combined face/hair candidate would need a separately reviewed baseline contract.

The benchmark comparison preserves the existing world, light graphs, color settings and all compared render/Cycles scalar settings except controlled output dimensions/path and compute-device choice (`render_candidate21.py:36-53`). The four canonical camera settings/transforms must match the retained oblique receipt (`:90-91`), and the six-view dimensions and extra camera construction are unchanged from candidate 20 (`:144-175`). The renderer still requires Cycles, 128 samples and an available OptiX device (`:116-127`). Only the temporary camera names change to candidate 21. I found no newly introduced camera, lighting, sample-count or non-hair-state relaxation in this diff.

The imported snapshot helpers retain their prior scope limitations: material images are identified by name rather than independently hashed pixel payload, and scalar property snapshots are not a general serialization of arbitrary Blender state. The frozen saved-scene hash and independently reviewed builder remain part of the trust boundary. This review does not elevate those inherited helpers into complete scene equivalence proofs.

## Output preservation and cleanup

The renderer refuses pre-existing planned PNGs or a render receipt before starting and rechecks each PNG before writing (`:82-83,180`). Partial outputs remain evidence rather than being overwritten on rerun. It restores the active camera, dimensions, resolution percentage and filepath, removes both temporary cameras and their data, compares canonical cameras, and checks all saved input hashes in `finally` (`:189-199`). The new point-count code creates no process or Blender datablock resources.

As before, the launcher must own and terminate the background Blender process on success/failure. The renderer changes process-local Cycles device preferences and image-output settings without saving user preferences or a blend; process teardown is therefore part of its lifecycle. The exact supplied script does not independently launch or terminate that process. No process was launched by this review.

## Review limits and next check

No actual adaptive curve population or new geometry receipt existed in the reviewed scope, so its point-count ordering, total and helper hash agreement are not verified in Blender. No rendered pixels were inspected for candidate 21. A corrected helper and caller must receive a bounded re-review, followed by root-owned verification that the exact geometry-accepted scene is the one rendered. The full-groom physical gates remain mandatory and were not reviewed or approved here.

Only this authored report was written. Pure Python controls terminated normally and left no task-owned browser, Blender, GUI or server process.

## Corrected revision re-review, 2026-11-08

The initial finding and disposition above are retained for their exact reviewed revision. The old renderer is now preserved as `outputs/character-round3-20261108/render_candidate21_pre_review.py`, still SHA256 `d9f087db4c08b42d2fe3036d14be561ae40b28b8c2784d2b6b8151633829f8d4`. The earlier round-2 helper is unchanged. This section supersedes the initial renderer blocker only for the new exact revisions below.

| Corrected artifact | SHA256 |
| --- | --- |
| `outputs/character-round3-20261108/render_candidate21.py` | `2f010a2600ee0eb9e4c4eb7b13e1435ee1cf2c2bd857a918b6f7727dbb991595` |
| `outputs/character-round3-20261108/hair_render_fingerprint.py` | `1fb77b5f376197063ca094a04aa2d0111786184d57d1f610a226abd8f8960314` |
| `outputs/character-round3-20261108/check_fingerprint.py` | `4240dd9424e37c755e120ed3f2ad905203b391a01250d8fa28b09e21b9823435` |
| `outputs/character-round3-20261108/fingerprint-controls.json` | `f494ab6ed4823c4736561a6638efcccabeb930aee7be9c5801218b5a2f5281d1` |

I independently checked both corrected code hashes and their complete diffs. The renderer changes only the fingerprint import path to its new round-3 helper. The new helper changes only the per-spline count assertion to 2..901 and inserts `struct.pack('<I', len(spline.points))` before that spline's property record and all six-float point records (`hair_render_fingerprint.py:30-36`). All static-object, modifier, constraint, parent, animation, material, curve, transform, homogeneous-weight, radius and tilt coverage is retained. The explicit count prevents moving a boundary within an identical flattened point stream from preserving its fingerprint.

I read the root-authored pure-control script and its bound result. The seven passing cases correctly exercise deterministic exact clones; redistribution from lengths [2,3] to [3,2] with identical flattened points; changed coordinate, radius and tilt; and rejection of 1 and 902 points. The controls stub the existing object/material snapshot functions and make that limitation explicit. They prove the new hash framing and point-value sensitivity, not actual Blender property enumeration or full material-state equivalence. The unchanged property/material snapshot implementation was inspected in this review; no new regression is apparent there.

Disposition: R21-1 is resolved for renderer `2f010a...` plus helper `1fb77b...`. I found no remaining blocker in this bounded renderer/helper source diff. The exact same new helper must be bound in the builder receipt, the saved actual scene must pass the renderer's population/count/coordinate/state comparisons, and the full-groom physical evidence must be reviewed separately before rendering. A native adaptive-curve smoke was announced by root but was not yet available for inspection when this disposition was written; no native or full-scene success is claimed here.

## Native adaptive-curve smoke addendum, 2026-11-08

The previously pending native smoke is now available. I inspected its script, exact hashes, JSON result, process receipt and log. `outputs/character-round3-20261108/native_fingerprint_probe.py` has SHA256 `00e6a37828e146e01701fbe1f930cc5e4c815bfcaa80ba8d274dfcd221677c8b`; `native-fingerprint-result.json` has SHA256 `d993da2225ca449f8646a17312cbfa158ff8b98f19f480659aae5d1e560d070b`. The recorded helper and non-hair snapshot dependency hashes match the corrected revisions reviewed above. Root's owned Blender 5.2 process exited zero, with its process tree closed, after approximately 1.811 seconds.

This script uses actual Blender POLY curves and the real property-snapshot helper, without stubs. The two splines contain 90 and 180 points. The fingerprint is deterministic; changing and restoring radius, tilt and coordinates changes and recovers the exact fingerprint; redistributing the same flattened 270 points into 91 and 179 points changes the fingerprint; restoring 90/180 recovers it. The object/curve/material identity sets are restored and source hashes remain unchanged. No render or saved scene is produced. These five recorded controls resolve the bounded native variable-count execution gap.

One harness limitation remains explicit: `native_fingerprint_probe.py:36` writes `status: pass` in `finally`, even if an earlier assertion raises. A future run must therefore require exit code zero and the complete expected control list, not just that status field. This inspected run satisfies both, so the limitation does not invalidate its positive result. The full 23,000-strand scene, nonempty material graphs, physical clearance checks and actual renderer remain outside this small smoke's coverage. Full-groom acceptance is still not approved by this renderer review.

## Findings and disposition

R21-1 is resolved: the new helper explicitly binds each adaptive spline's point count and every stored coordinate, homogeneous weight, radius and tilt. The renderer retains exact 23,000-strand population, nonhair and material identity, unchanged native cameras/lighting/render benchmark, immutable source and saved-state bindings, and fresh-output protection. This replaces an old fixed-64 construction assertion; actual physical segment checks remain mandatory in the builder.

## Verification

Seven pure controls pass. The actual Blender smoke uses two splines with 90/180 points, checks deterministic repeat, coordinate/radius/tilt mutation and restoration, and redistributes the same 270 flattened points into 91/179 to prove path-boundary sensitivity. All five native controls pass, temporary data is removed, sources are unchanged, and PID 54056 exits zero and closes after 1.811 seconds. The small smoke writes a pass-labelled receipt in finally, so its successful exit and complete control list are explicitly required; no generic failure-report correctness is claimed.

## Round outcome

Renderer source and native adaptive fingerprint behavior are ready for a separately approved, fully verified groom. The full builder, physical population and six rendered views remain unproven. No integrated appearance attempt is consumed by this isolated fingerprint smoke.

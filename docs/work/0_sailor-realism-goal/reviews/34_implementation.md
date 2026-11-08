# Review 34: implementation

## Target

Frozen candidate22 face builder, complete state/capsule helper, six-view renderer and the actual failed build.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns every Blender execution.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 d988cca8e9456b98e9eaf03f0337b14729fc6e64792147c2119e876b8f8d520f.

# Independent review of the candidate-22 face-only driver

Reviewed 2026-11-08 after the author froze the build, helper, renderer and manifest. Scope: exact evidence binding, complete baseline-hair retention, changed-skin/shaft intersection checking, canonical scene retention, saved-scene replay and six native views. No Blender, GPU, render or scene build was run by this reviewer. Only this authored report was written; prior face and renderer reports remain unchanged.

## Decision

No blocking source defect was found in the exact frozen revision. It is suitable for a root-owned geometry build. The new capsule check is a conservative real-arithmetic test against the complete final changed-skin polygon population and includes strand radius; it fails closed on unresolved segments. The build replays the exact previously measured float32 positions and preserves the complete retained hair and scene state. The renderer independently reloads baseline and saved candidate and verifies those bindings before any image.

This is not a pre-existing runtime pass. Rendering remains conditional on a successful actual complete capsule/face/ear check, exact saved/reopened coordinates and retained state, unchanged source hashes, and root inspection of the build result. The inherited F21 lower-hair defect remains open. Neither final full-groom acceptance nor appearance improvement is approved by this source review.

Subsequent actual execution failed before the geometry edit on the state serializer defect documented in the runtime addendum below. The source-review conclusion above is retained as the pre-execution judgment; the current candidate-22 decision is failed and rendering is disallowed.

## Exact frozen inputs

Files are in `C:/Users/38909/Documents/github/blender_scenes/outputs/character-round3-20261108/face-candidate22-source-draft`. Copying the exact files to the sibling `candidate22-source` folder is supported: local manifest keys are relative filenames and the driver resolves them against its actual folder. External pins remain absolute and unchanged.

| File | SHA256 |
| --- | --- |
| `build_face_candidate22.py` | `ce17604fdd73d94603cd26f25000bfa36b5dd510282b042d57db6ff17cca92b5` |
| `face_candidate22_helpers.py` | `2e3f1ea8fd28704623ad34838ca98490bc84280af102cfa1344ca5d4835633c7` |
| `render_face_candidate22.py` | `2ed5905bd267dfee43b07fbf0ee6e42b85223fde0661cc5b27769e33f8964e7c` |
| `source-manifest.json` | `494e20d3735b2882a0a78df32b58c7add3dd07c115bc57734d00f0eadf88cf2e` |
| `test_capsule_bound.py` | `b824f4be8e5f1ddc49c5a067befd0cc09dedd298d4cae88543a558d84a118d1d` |
| `source-checks.json` | `f91507f8db4c69a4e8eb56d4234e4f845359a20cc2a6ca8127e0d098b605b7c1` |

I independently rehashed all five local source entries and all 24 external manifest entries; every hash matched. This includes the frozen candidate-10 blend and six benchmark PNGs, fixed/seeded camera receipts, accepted topology-runner receipt and code, material instrument, saved coordinate inputs, independent topology review, new hair fingerprint and its native smoke evidence, and the actually imported state/face-clearance helpers. The inspected worktree HEAD is docs-only revision `02cff2e1f5e84340d8c335cbbc8f65a5f4e64533`; latest runtime source revision remains `dc67d1c786e7a67b8107d98ce4c72980173bc62e`. The manifest's `runtime_base_revision` label names the earlier docs commit `dcee6ed...`; actual file hashes, not that descriptive label, establish the reviewed runtime identity.

## Evidence, coordinates and saved-state binding

`build_face_candidate22.py:29-48` checks the accepted topology measurement, its strict 50 micrometre primary scalar/vertical upper bounds, complete material-domain/terminal coverage, finished structure checks, ocular result, actual negative controls, process exit and cleanup, and every measurement dependency hash. The manifest independently pins the exact accepted measurement `c9f2ed...` and runner `2115bb...`, so a newly written file containing a convenient pass flag cannot substitute for them.

The build opens the immutable candidate-10 blend and checks its original mouth property digest and all 516 original proposed coordinates (`:60-71`). It applies the 512 input deltas once and requires each resulting stored coordinate to equal the accepted measurement's `stored_after` vector (`:74-80`). Every other source coordinate and all ocular guard rows remain exact. This verifies the actual float32 result, not just equality of high-level parameters.

The old `reference_smile_input` remains unchanged as historical provenance. A separate factual binding stores hashes of baseline/current/original-neutral coordinates, the complete 642-row cumulative neutral/candidate-10/proposed triples, accepted measurement/instrument/review identities and source dependencies (`:87-103`). It is explicitly labeled an input binding rather than a saved pass flag. Existing code must not reinterpret the unchanged historical mouth property as a current proposed-coordinate contract; the new renderer deliberately uses the separate binding and accepted geometry evidence.

Before saving, the build checks all source hashes again. It writes only a new `provisional.blend`, then reopens those exact bytes and checks body coordinates, old/new properties, fixed state and hair state (`:109-118`). Existing output files cause a stop, and a failed build writes a failed result and raises rather than returning a passing exit. The baseline blend and all bound sources are checked unchanged in `finally`.

The renderer repeats the critical comparisons independently after reloading both baseline and candidate (`render_face_candidate22.py:36-57`): complete original and final source coordinate digests, exact 512 stored positions, every other source row, original-neutral digest, all 642 coordinate triples, complete hair state, retained scene state and factual binding. Its own exact source hash must appear in the build dependency map. It therefore does not rely only on build booleans or custom saved metadata.

## Complete changed-skin/shaft test

The change detector compares actual evaluated before/after coordinates and requires unchanged evaluated polygon topology. It includes every final polygon incident to any changed vertex and every triangle of those polygons, using actual polygon ownership (`face_candidate22_helpers.py:116-122` in this frozen file). This is broader than a face-centroid region or changed-vertex-only collision sample. Unchanged hair and unchanged skin polygons cannot acquire a new geometric surface intersection relative to the baseline merely because another polygon changes; the complete changed polygon population is the necessary additional surface set.

All three retained hair objects and all 23,000 splines are included regardless of opacity. The helper requires identity transforms, static unmodified POLY strands, noncyclic splines, 3D ROUND bevels, no external bevel/taper, no extrude/offset, finite stored endpoints and nonnegative endpoint radii. Every segment uses the maximum endpoint radius multiplied by bevel depth. Under this frozen round POLY representation, that capsule conservatively encloses the connected shaft geometry; it is not a centreline-only check or a substitution of fewer segments.

The broad phase rejects a segment only when the complete endpoint/radius-expanded AABB is separated from the entire changed-patch AABB on at least one axis. It therefore handles crossing segments whose endpoints are both outside and segments whose centreline misses while their radius enters. Every remaining segment is checked by `capsule_clearance` (`:89-107`).

For a subsegment midpoint c, half length h and shaft radius r, unsigned distance to a fixed triangle surface is 1-Lipschitz. Consequently `distance(c, surface) - h - r` is a lower bound on separation of the entire capsule from the surface. The implementation further subtracts the query's float32 quantization distance and a 0.1 micrometre numerical reserve. Positive lower bounds certify that subsegment. Otherwise the segment is bisected; depth/node exhaustion returns uncertified, never pass. The proof does not depend on nearest-normal sign on an open surface patch.

The traversal permits a passing result only when there are no failures and all 23,000 paths were processed. Early termination after eight failures cannot produce a pass. The final record separates AABB-proven and adaptive-ball-certified segments and retains failing endpoint/radius witnesses. A positive actual result should also be checked for a complete segment count and accounting consistent with the exact retained hair population.

This is a conservative real-arithmetic enclosure with explicit finite-precision reserve, not a formal interval proof for Blender BVH arithmetic. The pure tests do not validate native BVH numerical error or every Blender bevel representation; the static representation checks and the previously reviewed actual hair fingerprint are material prerequisites. Root must inspect the actual runtime result rather than treating these source inequalities as an already established clearance.

The builder additionally runs the unchanged native front-face and ear centreline checks. Those retain their documented centroid/radius limitations; the new capsule check supplies radius-aware coverage for every changed skin polygon. Passing this face-only combination does not certify unchanged lower skin, garments or the original lower-groom 1.5 mm margin, and the output explicitly preserves that limitation.

## Retained scene, hair and six views

The reviewed `hair_state` hashes every stored spline point, homogeneous weight, radius, tilt, per-spline length, object/data settings, static transforms and material/render state using the corrected fingerprint `1fb77b...`, plus hair custom properties and exact object population. It compares directly with the loaded frozen baseline, before saving, after reopening and in the renderer. No hair is regenerated from current scene source or inferred unchanged from strand count alone.

The new fixed-state digest excludes only body positions and the one factual binding. It retains body topology/UV/color/attribute schema/modifier state, other object geometry and attributes, parents/constraints, material assignments and polygon smoothing, custom properties, shader graphs and ramps, packed FILE-image payload hashes, world/light graphs, camera objects, collections, render/Cycles/color/image settings and scene frame. The code is a bounded serializer for this known static scene, not a general complete serialization of arbitrary Blender extensions. I found no change path in these drivers that bypasses its preserved-state comparisons.

The renderer checks original native PNG dimensions for all six views, retains the four canonical camera objects, reconstructs the fixed oblique from its frozen receipt and the torso camera from the same seed 20261107 and saved position/target/lens (`render_face_candidate22.py:28-31,76-90`). Native dimensions remain hero 1280x1600, portrait/profile/oblique 1200x1200, back 880x1100 and torso 1200x1400. It requires Cycles, 128 samples, PNG RGBA 8-bit and the frozen view/look/exposure/denoise settings, and fails if OptiX is unavailable. The geometry and light state comparisons occur before GPU device selection or temporary cameras are created.

The renderer preserves partial output and refuses existing planned images or a receipt. Its `finally` restores the original active camera, dimensions, percentage, filepath and device, removes temporary cameras and their data, then rechecks retained state, complete hair, body coordinates, factual properties and every saved/source hash. Any cleanup or immutability failure is recorded as failure. The root launcher remains responsible for closing the owned background Blender process; neither driver leaves a server or visible application open.

## Verification performed and execution boundary

I independently replayed the exact pure capsule/AABB controls in memory, omitting the test's file-writing statements. The long clear segment required adaptive subdivision and passed; centreline crossing, radius-only intersection, touching, and node-budget exhaustion were all rejected. The four AABB controls correctly distinguish separated capsules from crossing endpoints, radius intrusion and touching. All five Python files compile. `bpy` was not imported, no evidence receipt was rewritten, and no subprocess was launched by these controls.

The author-added state fields and final AABB helper were re-read after freeze, and the final hashes above match the complete manifest. No native API execution, candidate save, actual capsule BVH result or candidate-22 image has been inspected in this source-review task. Root may run the exact frozen geometry build. Rendering is appropriate only after inspecting a successful actual build result and reopened state for this same revision; any failure remains a failure requiring bounded diagnosis, not relaxed margins or omitted paths.

One face-only visual experiment is the intended downstream scope. The appearance decision still requires the six actual native images and independent comparison with the original adult reference and immutable candidate 10. Inherited F21 remains open, and the full-groom requirements remain mandatory for any later complete-character acceptance.

## Actual execution addendum: candidate 22 failed before geometry editing

The root-owned attempt used the exact reviewed build SHA `ce17604fdd73d94603cd26f25000bfa36b5dd510282b042d57db6ff17cca92b5`. I inspected `candidate22-source/build-result.json` SHA `78188871e4e6cb22aef537e0fd4d40c69e7c1225cf15d93852df3bd63b04de95` and `build_face_candidate22.process.json` SHA `1b447c5930fa108c101f76be263340c9d228c8d09c8f6699914ea6e110511123`. They record status `failed`, exit code 1, PID 41900 closed after 12.241567 seconds, `rendered: false`, and unchanged baseline and source files. I independently rehashed all 30 entries recorded by the build, including the manifest and baseline blend; every entry still matches. The output directory contains no `provisional.blend`.

**P1 — The retained-state digest cannot serialize the actual body loop map.** At `face_candidate22_helpers.py:40`, `body_snapshot(body)` is retained with only `coordinates` removed, then included in JSON `digest` at line 61. The pinned `tools/check_character_variant.py:38-43` returns `loops` keyed by polygon vertex tuples. Its `digest` at line 22 uses `json.dumps`, which rejects tuple dictionary keys. This raises `TypeError: keys must be str, int, float, bool or None, not tuple` during the first `fixed_state()` call (`build_face_candidate22.py:72`). The coordinate edit starts at lines 74-77 and was never reached. No capsule check, saved-scene reopen, or render occurred; none has a native candidate-22 pass.

The initial static review missed this imported return-type incompatibility. Compilation and capsule arithmetic controls do not exercise the native state serializer. Preserve the failed candidate and repair the serializer in a separately bound revision by canonicalizing the complete tuple-keyed loop map to deterministically ordered `(vertices, attributes)` records. Keep all polygon settings, UV values and color values, and avoid dropping the map or stringifying ambiguous keys. Before another full build, execute a bounded native baseline preflight covering digest stability, a no-op, representative retained-state mutations with restoration, and save/reopen equivalence. Review the exact changed source and preflight evidence separately. The repair is not approved merely because it is proposed, and this addendum provides no candidate-24 or appearance approval.


## Findings and disposition

Accepted the runtime tuple-key serialization finding. Preserved original source/result and prepared a separate candidate24 instrument-only correction; no face coordinate delta changed.

## Verification

Nine pure controls pass, but actual build22 fails in initial fixed_state before face edits because body_snapshot loops use tuple keys. Root process41900 exits1 and closes after12.242seconds; baseline and all bound sources remain exact.

## Round outcome

Candidate22 rejected before geometry editing, save or render. Native state-control preflight and independent fix review are required before the next build.

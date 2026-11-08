# Review 21: implementation

## Target

Read-only saved-scene six-view renderer based on 882e4f4d609669add52785cb39b424644d8f4deb. Initial, intermediate and final source plus shared fingerprint helper and native smoke remain deliberately retained in outputs/character-round2-20261107. Initial renderer is render_candidate18_pre_review.py; intermediate revisions are render_candidate18_reviewed_v2.py and render_candidate18_reviewed_v3.py; final is render_candidate18.py. Exact source, wrapper, helper and benchmark hashes appear in the report. No production source changes.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 2bb09d549180d7ee1309462281f7f8c27d557577a7f40f7d2803cf5c98304faa.

# Candidate 18 renderer: independent source review

Reviewer: Independent Codex reviewer, Astra xhigh. This review concerns the unexecuted evidence renderer and its launch wrapper, not the pending attempt-18 solver, geometry result or appearance. No Blender was launched and no implementation source or plan was edited by the reviewer.

## Initial exact source

Primary-checkout `outputs/character-round2-20261107/render_candidate18.py`, SHA-256 `a9831df4d79c1ead5ef0e6528382dca1c549947b56bc616f74411d3de754cc42`; wrapper `run_blender.py`, SHA-256 `3d3585b5976edcb5c537fdbdd28eff1cad54e8f95870d34c72af583148893fb5`. I independently hashed both and read their complete source. I also read the imported snapshot functions in the isolated worktree's `tools/check_character_variant.py`, the stronger existing garment/anatomy fingerprint helpers for comparison, and frozen candidate-10 oblique/random-view receipts.

The imported variant-checker SHA-256 is `512264e4724b73ed5042f4b0ecf5beb27d55fedaaa3cd395b7062b663f21b72b`. The candidate-10 `oblique-receipt.json` and `random-view-receipt.json` hashes are respectively `d57ae3f1d17d2c77efed49e90b13fe0d62a51111a36d11367a41a95b36af0f0c` and `80112958139b961074b9a52e64830e2e1527ae38c93cac23bd9f88a86c5f7259`.

The intended source is `outputs/.worktrees/character-naturalness-round2/outputs/round2-hair-search/attempt18/result.json` and its eventual provisional saved scene. Neither a successful attempt-18 receipt nor a rendered candidate is available in this review. The expected baseline is candidate 10, SHA-256 `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`.

## Initial disposition: repair before execution

R1. **Non-hair and benchmark equality are incomplete.** `fixed_scene()` combines retained object fingerprints with a set of material graphs. The imported `retained_snapshot()` omits object material-slot linkage/identity, while the material set can remain identical when two objects exchange existing materials. Object-linked overrides can also be absent from the material collection gathered through `obj.data.materials`. Explicit per-object slot link/material bindings and per-polygon material/smooth state are needed for the claimed unchanged non-hair appearance. World and compositor state are not objects in that comparison. The small set of exposure/look/denoising assertions also omits other rendering controls, including gamma, sampling behavior and possible compositor changes. Capture and compare the actual baseline/provisional world, compositor, color, render and Cycles settings, excluding only explicitly named runtime output/device controls. Unsupported render-affecting state should fail closed or have a narrower stated contract. Root accepted this finding before execution.

R2. **The saved hair is bound only by coordinates and counts.** The current loop hashes actual world coordinates and checks 23,000 POLY strands with 64 points each. It does not bind point radii, bevel depth, taper/render settings, modifiers or per-spline material assignments to the geometry stage. A saved shaft can widen after the clearance check and still satisfy the renderer's coordinate hash. Require an emitted-hair fingerprint recorded at the successful physical-check stage and compare it after reopening, covering actual shaft radii and the curve/object settings that affect the rendered shape, plus material-slot and per-spline assignments. Reject unsupported deformation rather than assuming the source-created state survived saving. The eventual saved-scene hash binds a file, but does not by itself establish that its width and render state match the state that passed clearance.

R3. **The output guard can overwrite earlier evidence.** PNG existence is checked one view at a time inside `try`; `finally` writes `render-receipt.json` unconditionally. An existing image can therefore reject the run while the new finalizer overwrites an earlier receipt. An occupied later view can also be discovered only after several new renders. Check all six planned image paths and the receipt path before rendering or entering a finalizer that writes the new receipt. Preserve prior output on rejection. Once a fresh run owns those paths, retain partial results and a clearly failed or incomplete receipt if rendering fails.

The frozen supplementary camera definitions should also be bound explicitly. The oblique path uses the recorded location, Euler angles, lens, sensor width/fit and shift; check the realized matrix and optical settings after update. The torso path reproduces seed 20261107 and checks its location, but currently leaves target/lens/sensor/shift/resolution partly implicit or unchecked against the benchmark. Set and record the full intended target and camera configuration so the claim of the same seeded view is reviewable. This is part of R1's benchmark correction, not permission to choose a more favorable view.

## Sound parts and ownership

The renderer requires `geometry_pass_pending_appearance`, all four existing immutability flags, current source hashes and the provisional saved file's receipt hash before opening it. It confines the saved file to the intended attempt directory and pins the baseline blend. These are useful prerequisites; their successful execution and the final worker schema remain pending.

The canonical camera snapshot is compared to the recorded candidate-10 camera values. Rendering retains the canonical four view dimensions and adds the existing fixed oblique and seeded torso views. It requires Cycles with 128 samples and an available OptiX device, and selects only OptiX devices. This preserves the intended GPU workflow instead of silently falling back to CPU. No blend-save or user-preference-save command is present.

Temporary cameras are owned by this render and removed with their camera datablocks in `finally`; the script restores its original camera/resolution/path and verifies canonical camera and saved-input hashes. Pre-render assertion failures are contained by the separate owned headless process. `run_blender.py` creates a WindowsJob, uses a hidden process, waits with a configurable default 900-second timeout, and closes the owned process/job in `finally`, including exception/timeout paths. I found no task-specific process-ownership blocker in that wrapper. Runtime process closure must still be inspected; this source review did not launch it.

## Verification and next decision

Performed: exact source hashes, complete static renderer/wrapper read, imported snapshot inspection and comparison against the actual frozen supplementary camera receipts. Not performed: Blender execution, successful provisional-scene reopening, output freshness control, physical clearance, saved-radius equivalence, rendering or native visual review.

Readiness is withheld for the initial renderer hash pending the coordinated R1-R3 repair. Root has accepted the findings and is preserving this initial source before editing. Repaired exact-source disposition can be appended without erasing these findings. Even a later source-readiness approval will not constitute attempt-18 geometry or appearance acceptance.

## Repaired renderer: conditional source readiness

Final renderer SHA-256 `813cae1b22aaf0fab3d006d417ee5975163af1e1c1e5adabea299a7a8eafa65f` and shared `hair_render_fingerprint.py` SHA-256 `cc63b9b80f4e819d8a96c87417a1576729b5dddd4e9a0a69b7dadf9846d60dbf` were independently recomputed and reviewed. The initial renderer remains byte-exact as `render_candidate18_pre_review.py`. Intermediate hashes `4eaa0acf600d57528266c1ab35c73ba85d1d15f0ad1aaee7c4f00e81ea5b5d7f` and `19a1eb5c191bfb2b22498b7fd4bfab48f7e8adad6bd5e544b8baa2ac6b6eda2e` remain as `render_candidate18_reviewed_v2.py` and `render_candidate18_reviewed_v3.py`; I checked those retained bytes too.

R1's reported gaps are addressed for the supported static scene. The final material population comes from actual object slots, including object-linked overrides; slot link/material identity and per-polygon material/smooth settings are compared explicitly. Baseline/provisional render, Cycles, color-management, image-format, world and light-node snapshots are compared. Only the named output dimensions/path and GPU device selection are excluded from the corresponding scalar comparisons. Any nonempty compositor graph is rejected rather than accepted through an incomplete graph comparison. The torso target/lens are checked against its receipt and sensor/shift settings are explicit. Supplementary camera matrices and full scalar camera settings are recorded with each rendered view. The existing snapshot functions still define a bounded static RNA/node-input contract; this is not a new claim of generic coverage for arbitrary animation, shader-group internals or external image-content changes.

R2 is addressed on the renderer side. The shared helper fingerprints each supported object/curve's scalar state and transform, actual slot bindings/material snapshots, spline properties, and every stored homogeneous coordinate, radius and tilt in order. It rejects modifiers, constraints, parenting, animation, shape keys, bevel objects, taper objects and non-round bevel mode. This makes the geometry contract deliberately narrower than arbitrary Blender curves. The renderer compares that reopened fingerprint to `stored_curves.render_state_sha256` as well as checking the existing coordinate hash and exact population. It now explicitly requires normalized-path source bindings for both the shared helper and `check_character_variant.py`, so a receipt cannot silently omit those dependencies from the version check.

The remaining R2 dependency is the producer: the worker must compute this same fingerprint immediately after verifying the actual stored physical strands and before saving, record both required source hashes, and bind the resulting saved scene. That placement and the successful receipt are not yet available for this renderer review. They must be checked in the separate attempt-18 source/runtime review. Absence of the expected fingerprint currently fails the renderer rather than bypassing the comparison.

R3 is addressed: all six image destinations and the receipt destination are rejected if already occupied before scene comparison, rendering or entry into the receipt-writing finalizer. Per-view checks remain as additional protection. A fresh owned run can retain its partial receipt if rendering later fails, and the existing finally cleanup of temporary cameras and owned-process wrapper remain in place.

Root ran a read-only baseline helper smoke on the intermediate `4eaa0acf...` renderer. I read `renderer18-preflight.json`, SHA-256 `7b498bc897b6a23e48221259fe46bf5a7c735810466d298617de49d64cf3c544`, and its process receipt, SHA-256 `b18aee7a084877e99a14c6e72ad0081a54c30ba6ec320f034ddf3625bfcff543`. They record successful snapshots of 112 non-hair objects, benchmark state and baseline hair, unchanged candidate-10 input, exit zero and closed owned process in 9.937 seconds. This establishes native API compatibility for that intermediate helper smoke. It does not execute the final active-slot population correction or mandatory-dependency guard, open a saved attempt-18 scene, prove unchanged saved radius state or render an image. I did not run Blender.

Conditional source readiness is granted for the final renderer/helper hashes above. No material blocker remains in the reviewed renderer scope. The producer's fingerprint placement, successful exact geometry receipt, reopened-scene checks, owned runtime cleanup and all six native images remain pending. R1-R3's initial authored findings are preserved above; this disposition does not convert them or the helper smoke into a full candidate acceptance.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F29 | R1: nonhair assignments and world/render benchmark were incompletely bound. | Accepted and repaired in source. | Actual object slots and used materials, polygon assignment/shading, world/light/color/render state are checked; unsupported compositor graphs reject. |
| F30 | R2: coordinate-only proof omitted hair radius/render-state changes. | Accepted and repaired in source. | Shared fingerprint binds actual curve/spline/point/radius/material state, with explicit dependency entries and producer placement. |
| F31 | R3: stale outputs could be partially overwritten. | Accepted and repaired in source. | All six PNGs and receipt are checked before any output. |

## Verification

Root ran one read-only native baseline smoke against intermediate renderer 4eaa0acf600d57528266c1ab35c73ba85d1d15f0ad1aaee7c4f00e81ea5b5d7f: 112 nonhair objects and current benchmark/fingerprint helpers pass; input unchanged, owned PID 31116 closed after 9.937 seconds. Two subsequent small source repairs were independently inspected. Final renderer 813cae1b22aaf0fab3d006d417ee5975163af1e1c1e5adabea299a7a8eafa65f was not executed on attempt 18 because that groom failed before saving. No new visual result is attributed to this instrument.

## Round outcome

Final source is conditionally ready for the exact successful saved groom and its complete producer proof. Attempt 18 failed, so no render followed. Any future candidate uses a separately bound target and fresh outputs; this record is not appearance acceptance.

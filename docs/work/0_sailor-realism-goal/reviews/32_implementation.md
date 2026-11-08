# Review 32: implementation

## Target

Frozen complete direct-surface candidate21 groom and its actual stored-geometry and receipt contracts.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native Blender execution.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 54f4dab2b8fb1ec551754ea64825d993cef78bc914921afd98933b5ee8a223cd.

# Candidate21 full groom: independent bounded source review

Decision: no blocking implementation finding for the root-owned, single full candidate21 experiment. The reviewed source may be run once under the root's process/deadline controls. This is not a full-population geometry pass, appearance acceptance, or permission to substitute the 18 diagnostic paths for 23,000 generated strands. No Blender, GPU job, browser, CLI reviewer, or subagent was launched by this reviewer; source was read only. Only this report was written.

## Exact reviewed target

Root revision supplied: `dcee6ed29c3f4e7085ab8e675144ce63fa4ce886`. The operative target is the preserved frozen byte set under `outputs/character-round3-20261108/candidate21-source/`, with SHA-256 independently recomputed during this review:

- `surface_groom_core.py`: `44469cc3c1b727972e7241ee4b53f126e7f3a3de4b3ef485f7850f480ad8add6`.
- `build_surface_groom.py`: `87910f655b40530d47500f3ad473cf1b95dfaf699db33dd481e5a6a155f255ba`.
- `run_full_surface_groom.py`: `5043f0b891e186b8c93dd8329108d2eb0ba25960dd31c50349408a2af2dae29b`.
- Renderer `outputs/character-round3-20261108/render_candidate21.py`: `2f010a2600ee0eb9e4c4eb7b13e1435ee1cf2c2bd857a918b6f7727dbb991595`.
- Fingerprint helper `outputs/character-round3-20261108/hair_render_fingerprint.py`: `1fb77b5f376197063ca094a04aa2d0111786184d57d1f610a226abd8f8960314`.
- Imported WORK `tools/check_realistic_character.py`: `0aa9f7294a034dcad295164b547fcb999c24e5ce371dd4b4572a667c0a2c9133`.
- Imported WORK `tools/check_character_variant.py`: `512264e4724b73ed5042f4b0ecf5beb27d55fedaaa3cd395b7062b663f21b72b`.

The review read AGENTS.md, repository retention policy, fleet coordinator and review-pin runbooks, imported head/coverage/lower/face/ear checks, the author handoff and seven controls, and raw v1/v2/v3/goal probe evidence. No other reviewer report was read. `docs/learning/lessons.md` is absent in both the primary checkout and named worktree.

## Guard assessment

1. Complete population and fail-first behavior are explicit. `build_surface_groom.py:127-181` constructs the exact three populations 11,425/11,425/150, advances the completed count only after all per-strand checks, preserves the first failure and re-raises it, and rejects any final count mismatch. A failed path is never skipped or replaced. The per-strand exception path retains its specification, rounded coordinates and available certificate. `run_full_surface_groom.py:83-106` can save only after build returns, retained-scene comparisons and stored population checks pass; exceptions produce failed status, and final source/input checks can only downgrade status.

2. Actual emitted geometry is checked. `build_surface_groom.py:151-164` emits POLY coordinates and radii, reads the stored float32 coordinates/radii back, requires exact coordinate equality, measures every root against the anatomical head (maximum 0.3 mm), and verifies every segment. `verify_entire_stored` at lines 97-106 uses fresh nearest distances to the minimum of complete body and clothing and subtracts actual edge length, maximum actual endpoint radius and a numerical reserve. Along a straight edge the height ramp is monotonic, so its maximum endpoint requirement bounds the whole edge. The lower verifier separately receives 5 mm guide margin and 1.5 mm physical shaft margin with actual emitted radii.

3. Complete support is preserved. Imported `shared_field.py:70-117` restores all canonical body faces, evaluates render-enabled modifiers at render subdivision levels, and retains every mesh/curve clothing object and polygon without a height prefilter. The driver asserts the established body/clothing geometry hashes. Imported `shared_field.py:456-508` rejects malformed paths/radii, performs exact lower-band segment rays against both support BVHs, tests inside-body status, and recursively certifies distance bounds or raises. This is not an endpoint-only physical check.

4. The adaptive edge change is bounded and explicit. Only the private lower instance's `check_child_shape` is replaced, and it is restored in `finally` (`build_surface_groom.py:120-124,195`). The replacement rejects nonfinite or <=1e-9 m actual edges and retains the 75-degree entering/lower-joint turn ceiling. Physical distance/radius verification is still run for each stored segment; there is no resampling or dropping of short segments. The former 0.25 mm minimum was a point-spacing instrument, not a surface-clearance proof. Replacing it is reasonable for this experiment, but a successful full run still must expose actual minimum lengths and short-edge counts. Recomputed shape checks on the raw 18 v3 paths found all nondegenerate, maximum lower turn 33.7678558137 degrees, and zero lower edges under 0.25 mm; those 18 paths therefore do not themselves demonstrate the new short-lower-edge branch. The separate 40 micrometre positive control and duplicate/90-degree negative controls cover that branch at source level.

5. Local repair and coverage do not silently rescue invalid construction. `build_surface_groom.py:146-147` rejects any nonzero old head repair; imported `natural_hair.py:165-222` itself raises for excessive repair or remaining face/ear crossings. Fringe, crown and temple scans inspect actual stored curves and each returned pass field is enforced at `build_surface_groom.py:185-189`. Their finite projections are explicitly limited geometric coverage measurements.

6. Face and ear calls really fail on violations. `build_surface_groom.py:191-192` assigns the result of each check without swallowing exceptions. Imported WORK `check_realistic_character.py:323-415` rejects missing collection/geometry/region, unsupported curve forms, and any collision using `require(not collisions)` at lines 407-410; `require` raises AssertionError at lines 56-58. Thus no additional caller-side pass test is missing. These two checks measure POLY centerline crossings; the separate full-support actual-radius proof supplies shaft clearance.

7. Render binding is adequate for these static unmodified POLY objects. The helper rejects parents, modifiers, constraints, animation, shape keys and external bevel/taper objects. It binds writable scalar/array object, curve and spline RNA settings, matrices, slots/material graph snapshots, counts and every stored point's four coordinates, radius and tilt. The renderer checks saved-blend bytes, source bindings, population, all coordinate/count digests and the full render-state fingerprint before rendering. Radius-only or other captured render-state changes therefore cannot reuse the geometry receipt. These are static-curve bindings, not a general serializer of arbitrary Blender pointer graphs.

8. Nonhair and benchmark protection is checked twice. The build compares nonhair objects, data, transforms, materials and scene settings before saving. The renderer independently loads the canonical candidate10 and provisional file and compares fixed objects/material assignments, camera state and render/color/world/light settings before rendering. The renderer deliberately controls output dimensions/location and GPU selection, uses six native views, and leaves output status pending visual review. No aesthetic inference follows from any of these hashes.

## Nonblocking observations and limits

- FG21-M1: imported `hair_groom.py:122-125` labels its fringe retention check as 80% length but samples 80% of point indices. The new radius construction uses actual arclength (`build_surface_groom.py:48-53`), so that legacy receipt label is no longer an exact arclength measurement for adaptive paths. It can conservatively reject an otherwise good taper if points cluster near the tip, or describe a different location. Current construction explicitly prescribes the maintained arclength taper, and all actual radii are physically checked, so this is not a launch blocker. Do not cite that particular receipt field as a fresh proof of radius at exactly 80% arclength.
- FG21-M2: source/input immutability is evaluated in the driver's `finally` after saving (`run_full_surface_groom.py:98-105`). A concurrent mutation can leave a provisional file on disk with a failed receipt. The renderer correctly refuses it; file existence alone must never count as a candidate pass. Likewise, process failure or missing receipt is a failure, not an invitation to use an older artifact.
- The original seven pure controls were independently rerun against the frozen builder/core with bytecode writing disabled and the control script's output-write tail omitted. All seven passed, including expected failures. AST parsing passed for the frozen three sources, renderer and fingerprint helper. No actual mesh/BVH query was rerun here because the assignment reserves Blender to root.
- Raw v1 evidence contains the stalled physical advance at path 13; v2 reports length-complete long paths rather than validated arrivals. V3 replaces those long completions with seven measured terminal-ball arrivals and three explicitly named first-feasible approaches, alongside eight short scalp arrivals. The reviewed core raises on travel/step exhaustion; it never treats them as success. First feasible approach is still a distinct endpoint choice, not proof of reaching the requested tip. It can affect visual length and must remain visible in the full completion ledger and six-view review.
- Full 23,000-strand geometry, runtime/memory cost, saved candidate21 and rendered appearance were not available during review and are not approved by this report. Independent source permission here is only to perform the bounded experiment. Parent owns the only Blender job and its cleanup; this reviewer created no process requiring cleanup.


## Findings and disposition

Accepted source for one bounded experiment. Root then ran the full population: candidate21 stopped at strand526, before save or render, because a short fringe path exhausted travel without reaching its terminal ball. The source review is not reclassified as a runtime pass; failed raw evidence is retained. Both nonblocking observations remain explicit.

## Verification

Seven pure source controls passed independently. Root full candidate21 failed at strand526 after15.140seconds; process tree closed, source/input hashes unchanged and no blend/render produced.

## Round outcome

Source review permitted the experiment; runtime candidate21 rejected. One of ten round3 attempts consumed, with first failure and all source retained.

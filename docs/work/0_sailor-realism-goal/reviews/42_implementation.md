# Review 42: implementation

## Target

Supporting-halfspace ear construction with unchanged physical hair requirements.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual Blender execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 3310c5bc6fc8d6f158309cf0dfae0d65b09ddf54614d981e662e57130b120641.

# Halfspace ear construction: independent source review

Decision: no blocking source finding for the root-owned eleven-path actual diagnostic using the exact frozen sources below. This is source and pure-control approval for a diagnostic only. The earlier terminal loop and 79.234-degree thin-goal turn remain unresolved until actual route evidence says otherwise; neither may be waived. There is no full candidate, full-population geometry pass or appearance acceptance in this report.

## Exact target and scope

All entries in `surface-ear-halfspace/manifest.json` were independently checked against disk. Relevant SHA-256 values are:

- `support_envelope.py`: `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2`.
- `outer_ear_support.py`: `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2`.
- `surface_groom_core.py`: `051e6f2d00c1b0cdff3cbd621384cfa38ea9c8f07e9747acdca14d9a26c27422`.
- `run_bounded_ear_steering.py`: `ffbcb997fc540f8b1fe8a495ae430ab8df0be9bee70b6db14ca0451fee4fd638`.
- `check_support_envelope.py`: `c3d80fe15db52325b5df7754989befbdee629b63b81d21e9646f5de50f01f7a7`.
- Retained controls `halfspace-controls.json`: `ff8a22827404ddd7960f8b4b3f6ce2ddd5487385598ba7a6cfba869b9fa75543`.
- Root's actual hull-construction diagnosis: `ear-hull-root-probe/hull-construction-result.json`, `0f8784badef18eb9d1f27c34352d165f28f9931187523a1b84b2dca828f2b9b4`.
- Preserved v1 route failure: `ear-route-probe/bounded-ear-steering.json`, `573ee8c048fcc5aa638b47c9f55c71748b04250fe52c8c1767b1f72ba074fe2e`.

The source was read only. Only this review report was written. The reviewer ran ordinary Python controls with bytecode output disabled and the author's report-writing tail omitted. No Blender/GPU process, renderer, browser, subagent or package installation was launched. Prior v1 reports and failures were preserved.

## Why the representation changes

The raw native construction diagnosis establishes more than the previous face-normal hypothesis. Both original triangle constructions fail exact self-convexity and all-input containment on the original 7,849-point sets; maximum face-plane violations are 1.444987077 mm on the left and 1.401993660 mm on the right. Re-centering and uniform normalization still fail on the original coordinates, while the mesh remains closed with Euler characteristic 2. Thus changing only the method for querying normal signs would not establish that the underlying triangle construction is a valid enclosing convex surface. That earlier hypothesis is superseded by direct invalid-topology/containment evidence, not accepted as a sufficient repair.

The new helper does not use BMesh hull topology. It constructs the intersection of 642 fixed supporting halfspaces. Each offset is the maximum dot product over every selected input coordinate plus an outward numerical reserve. It then independently verifies every input against every stored plane using exact integer representations of the binary floats. Selected polygons are contained as well because each polygon's points are convex combinations of its contained vertices. The fixed direction set is precommitted; the reviewed source has no direction-density or amplitude search.

## Mathematical and implementation assessment

1. The exact proof is appropriate. `exact_containment` converts input points, center, normal components and offsets to exact integer ratios, checks every plane against every input, and checks each normal's squared norm is at most one. The inequality's integer numerator and denominator correctly represent the stored offset minus the exact normal dot product. A failed inequality or oversized normal raises. The source does not rely solely on the floating calculation that chose the offsets.

2. The distance claim is correctly limited. For the intersection K of these halfspaces, f(p)=max_i(n_i dot (p-c)-h_i) is 1-Lipschitz when every normal norm is at most one. For any y in K, each positive plane violation is at most the distance from p to y, so f(p) is a lower bound on exterior distance to K. It is generally smaller than Euclidean nearest distance near corners. The source and receipts explicitly use this lower-bound interpretation. Requiring f(p)-segment_length-radius-reserve to exceed the construction margin is therefore conservative for the entire segment. Physical mesh clearance remains a separate calculation.

3. Floating evaluation is conservative for the documented domain. Coordinates are restricted to absolute values at most 10 m, stored normals have norm at most one, and contact evaluation subtracts 1e-10 m. That reserve comfortably exceeds ordinary binary64 rounding for three products, their additions, offset subtraction and coordinate centering in this bounded domain. The exact mathematical field is 1-Lipschitz; floating samples can differ at rounding scale, which the reserve protects rather than claiming exact equality of computed differences. The accelerated NumPy branch performs the same binary64 matrix-vector expression. It was inspected but not executed in this reviewer environment because its ordinary Python environment lacks NumPy; the root's actual Blender run is still required for that branch.

4. Ray projection uses the halfspaces themselves. `ray_interval` intersects the nonnegative ray with every linear inequality and includes an outward roundoff allowance. It does not infer inside/outside status from a triangle normal. The resulting radial candidate is not treated as a physical-distance certificate: `_project` rechecks the original body/clothing query and all construction contacts before returning its stored goal. A projection failure remains a failure.

5. Separation from the actual body is preserved. `OuterEarQuery.__call__` still delegates to the original physical query. It reconstructs complete evaluated body coordinates, checks the established body geometry hash, and selects all polygons overlapping the canonical ear bounds. Construction records bind input coordinates, plane geometry, representation, lower-bound semantics and exact all-input proof. The runner passes the separate `physical_query` into whole-path actual-shaft verification and retains lower guide/shaft, 75-degree shape and old radial postguard checks. No halfspace distance substitutes for Euclidean body/clothing distance.

6. EAR-1 is fixed in the inherited core. Independent diff inspection shows that its final-chord shortcut now requires `length_done+step<=length`, using the actual stored float32 chord length. Rerunning the previous plane counterexample with a 0.0005 m budget now raises the travel-limit failure rather than returning a 0.0012083 m success. This report does not claim that the separately known sharp final joint is fixed; the 75-degree guard remains enforced.

7. The eleven-case harness is unchanged in scope. Relative to the original ear-route runner, changes add the envelope module to source binding and require successful all-input proofs with 7,849 source vertices. It retains the same original ear/fringe cases, six held-out ear cases, valid thin goal and two invalid rear goals. Every failed row still makes `bounded_failed`, and final assertions require exactly eleven rows, passing overall status and source/input immutability. It creates no full groom, saves no scene and performs no rendering.

## Independent controls

The complete author control program was rerun in memory against the frozen sources in approximately 3.54 seconds. Both native 7,849-point inputs passed every one of the 642 exact planes, with exact minimum outward reserves of 9.999999301044947e-11 m and 9.999999466426413e-11 m. Resulting plane-geometry hashes matched the retained controls: left `656186fbb4e3bf2aa99d651f3851349cb41e2aef200936a8033998807af5f0fc`, right `5ce066e094f45e1abe16a688792fb165d79a32f8b9d6ac8e9e273952e881f042`.

The 300 analytic cube-pair checks passed the distance-lower-bound and Lipschitz comparisons. The corner example explicitly gives a 0.172420744279 m bound versus true cube distance 0.173205080757 m. Analytic ray intersection and miss controls passed. The three archived false-exhaustion tails now have positive fields with differences no greater than their approximately 2 mm steps; this demonstrates those exact discontinuities are absent in the replacement field, not that new trajectories finish.

Two additional reviewer negative controls passed: moving one cube support offset inward by 1 mm caused the exact proof to raise, and replacing a normal with a norm greater than one also caused it to raise even with a generous containing offset. The original EAR-1 travel-budget counterexample was rejected. AST parsing passed for all five Python files.

## Limits and required next evidence

No new actual route was run by this reviewer. The eleven-path native diagnostic must still be run and inspected, including the NumPy query branch, construction records, original-goal preservation, physical support margins, unchanged radial postguard and shape limits. The raw v1 loop and 79.234-degree final joint are pending defects; source containment does not resolve either one.

Minor inherited harness limitation: the runner reports the core's root distance but does not itself assert the full builder's explicit 0.3 mm root-attachment threshold. The root coordinates come from the unchanged precommitted specifications, and the complete builder retains its measured-root check; nevertheless, inspect each bounded receipt's root measurement before citing root attachment as a measured diagnostic pass. Likewise, the runner's source list does not include imported `hair_groom.py`, which supplies specification functions; preserve/compare its established candidate10 hash when interpreting source binding. These do not block this read-only diagnostic, but the eventual full integration must retain the complete dependency list and explicit root guard.

A passing diagnostic would permit further full-builder integration review, not a 23,000-strand or appearance claim. The new helper must be explicitly wired for construction, while actual radii and body/clothing proofs, full population, coverage, face/ear, unchanged materials/nonhair/benchmark, save guards and renderer fingerprints remain mandatory. No full candidate is approved here.

## Findings and disposition

The root-owned actual eleven-path diagnostic improves to10/11 passing, with the previous false-inside jumps absent. The left0.50 route still orbits its terminal:2mm integration steps and persistent heading inertia miss the2mm target ball despite more than22mm physical support clearance. Terminal tolerance, travel budget, root, shape and physical margins remain unchanged; no full-groom trial is authorized by these results.

## Verification

Exact source, process ownership receipts and raw actual witnesses are retained in outputs/character-round3-20261108. Root findings are separate from the authored report. No runtime source is accepted by this record.

## Round outcome

Six integrated attempts are used and four remain. Current investigations remain bounded diagnostics; next full candidate number is27.

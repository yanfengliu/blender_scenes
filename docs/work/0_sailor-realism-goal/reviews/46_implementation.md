# Review 46: implementation

## Target

Distinct UV-derived brow construction, actual injectivity and candidate27 driver.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual execution and visual acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 f552eb2ed13c56b0e7997a5b8dddd755d50f0119f56ed010676bdac66d91b4d9.

# UV-based brow construction review

2026-11-08. **No blocking finding in the exact construction and actual geometry evidence. Proceed to the full retained-state, hair/eye, saved-scene, and native-view gates.** This accepts the bounded construction for that next verification step; it does not accept candidate 27 or its appearance. The previous candidate-25/26 field remains rejected for promotion on an alpha-padding exemption, and its failures remain retained.

I read `uv_brows.py`, the unsaved probe, actual captured geometry/result, the triangle certifier, and the added `brow_uv_checks.py`. I independently checked the actual projected mesh with exact integer predicates and ran the pure checker and eight certifier controls. No Blender, GPU renderer, browser, or GUI was launched. The report is the only file written for this review, and no reviewer-owned background process remains.

## Exact inputs

All paths in this table are under `outputs/character-round3-20261108/`. I recomputed each listed file hash and verified all source hashes recorded in the geometry result plus its actual-surface hash.

| Input | SHA-256 |
|---|---|
| `brow-parameterization/uv_brows.py` | `e5c0f1208d19bc856b950d285d208d9bcdc3d146f31fe03837c6b80e7624178b` |
| `brow-parameterization/probe.py` | `ded8afd16bb119a43646f402cfe1f9c7f0cb1269ce129ce149cfdb7818e431c2` |
| `brow-parameterization/geometry-result.json` | `7d39782716709a747e169eb44f3ea73563a21bfdd42caf50e2f548710e9e1249` |
| `brow-parameterization/actual-surface.json` | `88c6e2353a244e1c0379c6e53c45231bc1e210a9577c59b4be60360ea6f9d9c0` |
| `brow-parameterization/brow_uv_checks.py` | `495f3ec0de82524c11f31c6a9b947ff81c09bc88759ec2d6fd2ae0606a7f95fa` |
| `brow-surface-probe/triangle_clearance.py` | `e0bb92aa2f30025c1a997c76e076a0fe47def24116cdd526e4483d8c5f0744db` |
| Render-level evaluator in `candidate26-source/build_brows.py` | `e5ce5a4a5b5f74958fa127c660e54783a7ae58dfcb9472369b8c25ec8d71ed3b` |

The process receipt records exit 0, PID 36704 closed, and 4.3706453 seconds. The result is an unsaved diagnostic, not a final candidate build. The root must bind the full build to the same construction, packed texture, and frozen source/evaluated coordinates; later geometry changes need renewed checks.

## Construction and scope

`uv_brows.py:15-21` requires a consistent UV coordinate for each of the original 124 control vertices across the 96 polygons. It retains the topology and reads the existing texture. At lines 26-47, each 62-vertex component is reconstructed from its UV disk: physical x is linear in U across the original control-coordinate x bounds; V retains positive scale 0.065 m per UV unit after subtracting a smoothed alpha-weighted center. Anatomical direction is correctly reversed on the negative-x disk. The center curve has an inner height of 1.5538 m, a soft 0.8 mm arch, and an outer 1.6 mm descent. Lines 48-50 refit y to the existing evaluated forehead with the 0.45 mm control-point offset.

The alpha centroid reads Blender's existing packed image pixels; it does not edit the image, UVs, material, body, or other objects. The Gaussian smoothing scale is 0.025 U. Since that centroid depends on the texture, the full build must pin the already-inspected packed PNG hash `1827b24aaa1c928353027c5a86b8db59c1c22f06258b18faa2117d81f5ff9b05`, as the root plans. This mechanism reconstructs the full brow ribbon; it must not be described as preserving the previous outer brow positions or old ribbon width exactly.

The analytical mapping alone would not prove injectivity after subdivision. This review therefore evaluates the actual 1642-vertex, 3072-triangle surface, not only the formula or its control points.

## Independent projected-surface proof

Every captured x and z coordinate is exactly representable on an integer grid with scale 2^30. I converted to that common grid and used integer orientation/intersection predicates, eliminating a floating-point tolerance from the boundary and triangle-orientation decisions. Results:

- All 3072 actual triangles have strictly positive projected signed double area. The minimum is exactly 1.7618706493749414e−9 m² for the captured coordinates.
- There are two connected components. Each has 821 vertices, 2356 triangulated edges, 1536 triangles, and Euler characteristic 1.
- Each component has one 104-edge boundary loop. No nonadjacent boundary edges cross or touch. There are no duplicate projected vertex positions.
- All shared edge windings are opposite; there are no nonmanifold edges. Every vertex link is a single cycle or boundary path, so no hidden vertex pinch is present.
- For each component, the sum of oriented triangle areas equals its boundary area exactly. Positive triangle orientation, a simple boundary, and the verified disk topology establish a one-to-one piecewise-linear XZ disk, rather than a merely positive local-area test.
- The disks occupy disjoint x intervals: approximately `[0.011320742, 0.052081574]` m and `[−0.052088335, −0.011319396]` m. Their projected areas are 88.875055 and 88.678431 mm² respectively. They cannot overlap each other.

Thus the actual surface has no projected folding or internal double coverage, including adjacent facets that the older nonadjacent-only BVH filter skipped. This also prevents a three-dimensional self-crossing in this exact mesh: an intersection would require coincident projected coordinates from distinct surface points. The independent result agrees with the probe's zero nonadjacent BVH intersections. The inherited texture-bearing intersections have been removed, not waived.

`brow_uv_checks.py:14-56` is appropriate for the actual Blender tessellations and fixed topology used here: it checks positive triangle orientation, coherent polygon edge incidence/winding, two components, disk Euler values, one simple boundary per component, and separated x domains. I ran it on the actual new surface; it passes. I also ran it against the retained actual baseline; it rejects the folded projection with the expected assertion. The function assumes its triangle list is the actual tessellation of its polygon list, supplied by the evaluated-mesh capture; it should not be advertised as a complete validator for arbitrary unrelated or malformed face/triangle arrays. My additional exact vertex-link and duplicate-position checks above apply to this pinned actual artifact.

## Body separation and remaining checks

The probe tests every one of the 3072 actual brow triangles against the full evaluated body of 293760 triangles, using the previously reviewed unsigned-distance lower bound, four-way subdivision, query-rounding subtraction, positive reserve, and fail-closed budgets. It reports zero separation failures over 45692 nodes. I reran all eight pure controls successfully: clear separation, exhausted depth/nodes, crossing, touching, near-reserve rejection, the intentional unsigned-interior limitation, and query rounding. The certifier proves separation only; the separately checked exterior side is necessary.

All actual brow vertices have positive front-ray offsets. The body's measured front extent is behind the ray origin y = −0.5 m, and the captured brow minimum y is −0.1428964 m, also beyond that origin. These facts supply the exterior-side witness; positive unsigned distance is not being mistaken for proof against an entirely embedded triangle.

The new vertex standoff range is 0.208765–0.464529 mm versus baseline 0.257805–0.828370 mm. It satisfies the documented absolute-envelope criterion; the lower endpoint has only approximately 0.960 micrometres of margin above `baseline_min − 50 micrometres`. Keep the exact check and rerun it on the final scene rather than relying on rounded numbers or broadening the tolerance. Whole-surface body separation independently passes despite this narrow envelope margin.

The full hair-shaft and eye-clearance checks, exact retained state, saved-copy reopening, source/texture bindings, and six native benchmark renders remain outstanding for the full candidate. The probe restores the original brow coordinates and confirms the baseline file is unchanged, but it does not replace those full-build gates. Native inspection must determine whether the expression is relaxed, whether the new thickness and tails look natural, and whether the change creates a worried or surprised expression. Geometry progress does not yet establish visible success or full-character completion; inherited lower-hair F21 remains outside this review.

## Candidate 27 driver addendum — 2026-11-08

**No blocking code finding in the exact candidate-27 driver delta.** I read the full `brow-candidate27-draft/build_brows.py` and the renderer delta against candidate 26, then recomputed every local and external manifest hash. The initial reviewed manifest SHA-256 is `79431631fbac98653fa8f8055a2ac51127450ef1cb1032bc910a9e22201c24b2`; the build script is `41887a14a11bda58d9d34458d2f2d841a79e7dfe8341a2da3f65ac1e519965d4`, and the renderer is `c6cd180865cec35cc139e6c9fdc454b6e0b977e14d7e99feceba71da5cfdfd8f`. The construction, projected-disk checker, and triangle certifier are exact copies of the versions bound above.

The driver at lines 97-103 asserts the actual body/brow modifier settings and exact packed texture hash. Lines 106-110 require every stored proposed coordinate and every evaluated point, polygon, and actual triangle to match the independently certified evidence. This binds the exact-integer projected-disk findings above to the full build rather than assuming a new fit is equivalent. Lines 59-81 retain exact ordered polygon topology, projected-disk validation, zero actual nonadjacent self-crossing, and continuous full-body separation. Lines 115-119 enforce positive front offsets, the documented absolute envelope, and the separate whole-surface certificate. The new gate is explicitly described in the report payload; it is not silently substituted for an eye/lash requirement.

Lines 120-132 still run the complete stored hair-shaft clearance check, evaluated eye intersection check, exact retained-state/body-coordinate checks, saved-copy reopening, and final source/baseline hash checks. The renderer's only delta from the already-reviewed six-view driver is the candidate/output/temporary-camera labels. There is no change to benchmark cameras, render settings, cleanup, or native sizes. Successful build/render completion and native appearance remain unobserved at this source review.

One nonblocking factual metadata issue was reported to the root: the initial manifest's `controls` text still describes the rejected local inner-lift field and exact unchanged outer controls. It should describe the actual projected-disk check, folded-baseline negative control, and eight triangle-certificate controls. The code and report scope already describe the new full-ribbon reconstruction correctly. A metadata-only correction does not require another code review, but its final manifest hash must be recorded below before treating this record as the final source binding.

The root corrected that metadata before launch. I reread the corrected manifest and recomputed its SHA-256: **`4e243d5ac51f770f141e14c1f40717f114a3d7840589d885e129e2e30c2d613f` is the final reviewed candidate-27 manifest.** All five Python hashes remain identical to the reviewed values, and every external dependency hash still matches. The corrected controls description matches the UV-disk construction and physical checks. The stale earlier manifest is recorded only as review history. Final source disposition remains no blocking finding; runtime and native appearance must still be verified.

## Findings and disposition

Root accepts this exact source for the bounded native trial. Candidate27 subsequently builds, certifies all3072 brow triangles clear of actual skin, clears all23000 retained hair paths and eyes, and reopens the saved blend with all other state exact. Appearance is still pending the six native views. The previous folded inner-lift design remains rejected.

## Verification

Exact native receipts, source and inputs remain under outputs/character-round3-20261108. Root observations after the report are explicitly separate.

## Round outcome

Seven integrated attempts used, three remain, next28. No round3 appearance accepted yet.

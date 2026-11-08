# Review 45: implementation

## Target

Actual corneal/lash fit of the eye-opening reversal.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual execution and visual acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 d1843ffaaff3f2149f075c831b7a669b0a3eb7564d8f9d313c7d122ae6903ead.

# Independent actual-result addendum: eye-opening reversal rejected

Reviewed 2026-11-08. This is the actual-result addendum to `eye-opening-source.md`, `eye-opening-instrument.md` and `eye-texspace-instrument.md`; those source reviews and both earlier failed metadata runs remain preserved. I inspected the retained native receipts and independently recomputed selected geometry queries using read-only Python/NumPy. I did not run Blender, a GPU job, a build, save or render, and wrote only this report.

## Decision

Reject the authored-opening reversal as-is. The exact proposal causes real additional lid/cornea penetration and fails both unchanged lash bounds. A direct new skin-edge/corneal-triangle intersection independently corroborates the nearest-distance evidence. The additional conservative brow-separation check also fails. The metadata repair is validated by actual graphs and controls; the result is not another unexplained metadata stop.

No full candidate or render is justified for this revision. Passing mouth, structural and retained-hair checks does not offset the ocular failures. The source-gradient continuity concern remains unresolved; it does not need to be waived or resolved favorably to reject a proposal that already fails the fixed physical bounds. This review proposes no amplitude sweep, hidden proxy transport, eyeball alteration or relaxed threshold.

## Exact run and evidence

Files are under `C:/Users/38909/Documents/github/blender_scenes/outputs/character-round3-20261108/eye-root-probe-v3`.

| File | SHA256 |
| --- | --- |
| `measurement.json` | `877234c123b2a03b6b89c06b3cc104a0ae0557290065a112dcc670134c048f1a` |
| `noncoordinate-comparison.json` | `b3da67939f534ae09d25b691efbf6a29d1f0b6f66f4d55de49d4697b73dc37d0` |
| `actual-evaluated-data.json` | `fc2f24457d4ba53248e063c08291695e34e006335d10211ec346dc549899ba48` |
| `run_probe.process.json` | `83656767ff90c842eb67085426b5afd2b9cb7bd1b62a7e6726628cde13847482` |

The owned wrapper binds reviewed runner `c8d93ce9f12d67afecad841738c30cbcec0418e2a87e2d89aae73ff650b6dfac` and manifest `3a98e6e1e08ee1956be02bf3d050a214dcff586ce4f0d46eec6e17c3855ee517`. PID 44736 exited 0 and its tree closed after 125.140237 seconds. The diagnostic successfully completed its measurements but recorded `status: measured_fail` and `measured_checks_pass: false`; process exit 0 is not geometry acceptance. All 53 input hashes independently still match.

The recorded actual coordinate/surface artifact is byte-identical to v2's artifact, confirming that v3 changed the metadata instrument rather than the proposal geometry. The baseline blend remains `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. All original coordinates, historical mouth contract, complete scene state and temporary datablock populations were restored, and source/blend hashes remained unchanged. There was no save or render.

## Actual metadata issue closed

The live before/after graph snapshots are identical. Both meshes have the active render layer `UVMap`, DATA-linked material slots and one flat packed Image Texture with an unlinked Vector input. The brow graph contains only Image Texture, Principled and Material Output nodes. The lash graph adds the existing scalar Math node on the alpha path. I inspected the actual links: there is no link to either Image Texture Vector input, no TexCoord/Generated/Object node, no procedural texture and no group path. These image inputs use the active UV map under the documented [Blender Image Texture behavior](https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/image.html?highlight=image+texture).

The packed brow image hash is `1827b24aaa1c928353027c5a86b8db59c1c22f06258b18faa2117d81f5ff9b05`; the packed lash image hash is `6375eb8934d86d49eb2a37589e179614fb557dd92a772ced11e269ad6d72d79d`. Both remain exact. The six previously observed automatic texture-space scalars pass the exact geometry-derived expectation with no rejected difference. Literal mesh equality remains honestly false, while the narrow noncoordinate contract passes.

All six actual private-copy mutation controls rejected: UV coordinate, custom normals, custom attribute, material slot, manual texture-space mode and a Generated-to-ImageTexture connection. The custom-normal control records actual custom normals present. The Generated connection is rejected by the live UV-source guard; its assertion has no message, which is consistent with that explicit source predicate. Exact proposed coordinates, metadata and graphs were rechecked after the controls, followed by complete retained/original state restoration. This evidence closes the texture-space instrument issue for this exact scene; it grants no exemption for other fields or other materials.

## Fixed bounds failed

The following are the native receipt's maxima. Every legacy bound remains 50 micrometres.

| Check | Actual additional amount | Population / failures over 50 micrometres |
| --- | ---: | --- |
| Lid/cornea penetration | 1,328.331960 micrometres | 19,591 surface samples / 1,946 failures |
| Lash-root penetration | 225.189684 micrometres | 964 fixed baseline-selected roots / 54 failures |
| Lash-root separation | 85.614597 micrometres | Same roots / 10 failures |
| Brow separation, additional conservative check | 86.008168 micrometres | 1,642 evaluated brow vertices / 76 failures |

No sample was reported unresolved by the instrument's boundary/tangent checks. The raw brow maximum is 86.008168 micrometres; 85.614597 is the lash separation maximum. The evaluated eye proxies remain exactly unchanged, so these failures are not caused by an unreported globe resize.

The most severe eye witness is evaluated skin row 1107. Its world Z moves from 1.552466035 m to 1.550696254 m while X/Y remain exact. Native nearest-normal penetration changes from 11.162938 micrometres to 1,339.494898 micrometres. The baseline already had a small measured contact penetration; the required comparison correctly measures the additional amount instead of pretending that contact was absent.

## Independent geometric corroboration

I verified that every recorded ocular/lash/brow query point equals the same row in the retained actual evaluated arrays. For eye row 1107, lash rows 128 and 451 and brow row 1530, I independently minimized distance over every explicit target triangle using float64 plane projections plus all three clamped edge projections. This implementation does not call Blender's BVH or the reviewed signed-distance helper.

All eight before/after queries selected the same triangle IDs as the native receipt. Their closest points lie strictly inside the selected triangle, with positive barycentric coordinates; no open-boundary fallback is involved. The maximum discrepancy between independently computed and recorded nearest points is below 0.085 micrometres, negligible relative to these failures. Eye row 1107 selects shell triangles 9487 then 9490, with independently recomputed penetration about 11.091128 then 1,339.490264 micrometres. Both normals point outward relative to the correct eye centre. The corneal population contains 15,680 triangles, 160 boundary edges and no edge with more than two incident triangles; the witness lies in the interior of intact shell triangles, away from that open rim.

There is also direct intersection evidence independent of the distance sign. Actual skin-triangle edge **68329–81695** has these endpoints:

| State | First endpoint, metres | Second endpoint, metres |
| --- | --- | --- |
| Baseline | (-0.034938708, -0.135385290, 1.546528816) | (-0.034068096, -0.134862319, 1.546846151) |
| Proposed | (-0.034938708, -0.135385290, 1.544981837) | (-0.034068096, -0.134862319, 1.545234799) |

A read-only double-precision segment/triangle test against every corneal triangle finds no baseline intersection for that edge and finds a proposed intersection with corneal triangle **15272** at segment parameter **0.458494695**. Its triangle barycentric coordinates are approximately **(0.189731049, 0.167121350, 0.643147601)**, all strictly positive. This is a new crossing of actual evaluated skin and corneal surfaces. It rules out interpreting the large eye failure as merely a wrong nearest shell, an open-rim sign artifact or source-only proxy evidence.

The lash witnesses also corroborate the mechanism: row 128 moves from about 184.5 micrometres outside the skin to 225.2 micrometres inside; row 451 moves from about 138.9 micrometres outside to 224.5 micrometres inside. The reported absolute-distance separation failure at row 451 accompanies actual penetration, not a detached-lash interpretation that cancels it. Both inequalities fail independently under their preserved definitions.

## Checks that passed, and remaining limits

The actual new cumulative source union is 1,180 rows. Its conservative FACE closure has 34,689 evaluated surface vertices; 22,079 cumulative changed rows are completely accounted for, including 187 separately proven isolated helpers. The orbital closure has 19,591 evaluated surface vertices and accounts for all 12,243 incremental changes, including those helpers. Both missing-row lists are empty.

The original-neutral mouth material bound passes: scalar upper bound 27.907530 micrometres and vertical upper bound 5.729742 micrometres. Incremental oral rails are exact. Actual no-op, common translation, common width and 3 mm opening controls behave as required. The inward-eye negative produces 3,863.052669 micrometres additional penetration; lash and brow translation negatives produce roughly 2.949 and 3.029 mm additional separation. These controls were measured and detected, not merely present in source.

The bounded evaluated structural check reports minimum area ratio 0.814063596, normal dot 0.944303314 and zero new intersections in its checked population, retaining its documented shared-vertex exclusions. Those are skin/self-structure checks, which do not override the independently demonstrated skin/cornea crossing. All 23,000 retained hair paths and 1,449,000 segments are accounted for in the changed-skin test: 1,447,039 AABB exclusions plus 1,961 capsule certificates, with zero failures. The 2.580064 mm minimum lower bound applies to the capsule-certified subset, not to a global lower-groom clearance claim.

The actual stored-coordinate source gradient is 0.753353754, with nine exceedances; source fans retain minimum area ratio 0.652531838 and normal dot 0.910010996. The widest recorded local evaluated dihedral increase is 5.662549 degrees. These are useful continuity data, but this review does not convert them into a new passing threshold. The finding remains open while the tested reversal is rejected for the established ocular failures.

This is a bounded rejection based on exact native geometry and preserved physical limits, not a judgment about an unseen render. No full candidate was produced, and no appearance claim is made. The rejected state and all raw evidence should remain preserved. The unrelated brow-only feedback experiment and hair work are outside this report; inherited F21 remains open.

## Findings and disposition

Reject the eye reversal as-is. Independent full-target closest-point checks and a newly crossing skin edge corroborate the penetration. Narrow automatic metadata classification is valid but cannot offset physical failure. No full candidate is built.

## Verification

Exact native receipts, source and inputs remain under outputs/character-round3-20261108. Root observations after the report are explicitly separate.

## Round outcome

Seven integrated attempts used, three remain, next28. No round3 appearance accepted yet.

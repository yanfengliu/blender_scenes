# Review 41: implementation

## Target

Actual render-subdivision brow geometry and retained topology.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual Blender execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 f11d3610f2366fe151509ad8d0a76fda6edabb59cb1ddc88562712a0d0a1a3d6.

# Candidate 26 render-surface delta review

2026-11-08. Disposition: **No blocking finding in the exact source delta; ready for the root-owned build and native visual trial.** Candidate 26 repairs candidate 25's erroneous subdivision assumption and evaluates the intended finer brow surface. This is source readiness only. Candidate 25 remains a failed pre-edit/pre-render attempt, and candidate 26 has no runtime or appearance outcome at this review's completion.

The reviewed draft is `outputs/character-round3-20261108/brow-candidate26-draft/`. I recomputed the manifest SHA-256 `c64a172112c456f1b0596bc889befbf37046af04fb0ffff3830d6b667950602c`, matched every local and external hash it lists, and read the full build source plus the actual deltas against candidate 25. Exact local sources: `build_brows.py` = `e5ce5a4a5b5f74958fa127c660e54783a7ae58dfcb9472369b8c25ec8d71ed3b`; `relaxed_brows.py` = `f17fa4978b6a81cd1abcc1f2af6c72c33a2bcaf76386c24427fc5de781133aff`; `render_brows.py` = `5b5ccb23667a7a1d7102a628b8ca566d2e9ddfbdb189768247a926595d850bc1`.

The retained modifier probe at `outputs/character-round3-20261108/brow-modifier-probe/result.json`, SHA-256 `ee2506623d9e8a52fce08f0e1c9da0df5efad3120a4de77bf0a87b9653a67c88`, establishes the saved baseline's brow viewport/render levels as 1/2. Its corresponding evaluated counts are 438/384 vertices/polygons at viewport level and 1642/1536 at the render level. Eyes and body are each 2/2, with 16484 and 157230 vertices respectively in both probe modes. I also read `probe.py:8-22`: it temporarily assigns each SUBSURF viewport level to its render level, evaluates/counts, clears the temporary mesh, restores original levels in `finally`, and checks the unchanged baseline hash without saving or rendering. The process receipt reports exit 0, PID 55488 closed, 3.5242235 seconds. This is root-produced evidence I inspected, not a probe I ran.

`build_brows.py:17-30` now captures all SUBSURF viewport levels, temporarily sets them to their respective `render_levels`, updates the dependency graph, copies all evaluated points/topology/triangle ownership, then clears the evaluated mesh and restores the original levels in `finally`. Thus its returned geometry remains usable after restoration. Both the original and proposed brow snapshots use this evaluator, as does the eye surface at line 105. Temporary level changes are restored before retained-state comparisons and saving, so the repair does not intentionally change persistent modifier settings.

`build_brows.py:86-89` now requires the measured baseline contract: body 2/2, brow 1/2, and exactly 1642 evaluated brow vertices with 1536 polygons. The explicit body-level equality means that the existing skin-fitting and attachment rays use the same subdivision level as the body render; the Eyes call also takes the render-level path. The physical checks consume the finer brow topology rather than the candidate-25 viewport surface. The source does not merely weaken the previous assertion to let an unchecked surface pass.

The brow field is byte-identical to candidate 25. Other build changes are candidate labels; renderer changes are candidate/output/camera names only. The existing exact-state, saved-copy reopening, source immutability, hair-shaft, brow/eye crossing, and benchmark render logic are unchanged. The scope and coverage limitations in `brow25-source.md` still apply: evaluated-vertex skin-offset checks are not continuous triangle-interior clearance; shared-vertex triangle pairs are excluded from the overlap check; exact outer control points do not prove an exact unchanged subdivided boundary; three-dimensional ribbon thickness is not explicitly measured. These are limits on claims, not newly introduced blocking defects in this delta.

After a successful candidate-26 build, inspect all six actual native renders to determine whether the inner-brow lift visibly reduces the owner's reported frowning expression without introducing a worried/surprised expression or visible floating, embedding, pinching, or hair interference. Runtime geometry checks cannot establish expression quality, and an imperceptible difference is not sufficient. Adult proportions, inherited lower-hair F21, and the unresolved full-character criteria retain their prior scope.

I launched no Blender, renderer, browser, or GUI and performed no source edit or runtime test. The report is the only file written for this delta review, and no reviewer-owned background process remains. The root remains responsible for owned-process cleanup and final build/render result verification.

## Runtime failure addendum — 2026-11-08

Candidate 26 failed before saving or rendering, after applying the proposal in memory and obtaining its evaluated surface. The prior source disposition is preserved above; it did not detect the inherited assumption that loop-triangle identities would remain equal after vertex changes. No candidate-26 appearance outcome exists, and the failed instrument must not be treated as a geometry or appearance pass.

I read the actual `outputs/character-round3-20261108/candidate26-source/build-result.json`, log, and process receipt. The executed build script matches the reviewed `e5ce5a4a5b5f74958fa127c660e54783a7ae58dfcb9472369b8c25ec8d71ed3b`. The build-result SHA-256 is `4dc4026125c9ba83388fd55de057f199066c203e321d5315168446988be7e168`. Its traceback fails at `build_brows.py:58` on the combined assertion `old['faces'] == new['faces'] and old['triangles'] == new['triangles']`, reached from line 96. The process receipt reports exit code 1, PID 5136 closed, and 19.2381985 seconds. The log ends with Blender quitting. The combined assertion does not identify which comparison failed; a raw old/new topology capture is required before attributing it specifically to retessellation.

The root is preparing an unsaved diagnostic of the actual before/after evaluated faces, triangle triples, and owners. If it confirms equal evaluated vertex identities/count and identical ordered polygon loops, polygon connectivity can remain an exact invariant while triangle correspondence for area/orientation comparisons is constructed deterministically from each shared polygon. Apply those same vertex triples to both old and new point arrays; testing both quad diagonals or the union of old/new actual triangle triples additionally covers every actual rendered facet. Continue using the actual new loop triangles and owners for hair capsules, brow/eye intersections, and self-overlap. Removing the triangle-identity assertion alone is not a sufficient repair: preserve connectivity checks, nondegeneracy, orientation/area checks, and actual-triangle collision checks. No candidate-27 source or diagnostic outcome is accepted by this addendum yet.

## Raw-surface diagnosis addendum — 2026-11-08

I read the completed unsaved `brow-topology-probe/probe.py`, `result.json`, process receipt, and full `raw.json`, and analyzed the raw positions/topology with standard-library Python without Blender or file writes. Exact evidence: raw SHA-256 `6af54dda64cf0b18d50a1870d0d5c3e94a2b991097cb66d84bfade7ce7fc165f`; result SHA-256 `88a08e3fc7eaabda21185c91de39c459f25e140c4485239141b5cb167476b2c3`; probe script SHA-256 `aaf7ed9f64a05ad9aa4f2cf049a45d1a8f037a5c5aa2ff61c481f687ca259afa`. The process receipt reports exit 0, PID 30292 closed, and 4.0373112 seconds. The diagnostic restores source coordinates and modifier settings and verifies unchanged scene objects/baseline; it performs no save or render.

The actual evidence confirms 1642 vertices and 1536 identical ordered polygon loops in both states, with 22 differing positions in the actual loop-triangle lists. Their union has 3094 distinct vertex triples. The candidate-26 equality failure is therefore retessellation, not changed polygon connectivity. Comparing the same union triples on both geometries preserves a meaningful area/orientation test, while the final actual triangulation must remain the input for surface collision checks. This is a justified instrumentation correction, not permission to discard topology validation.

The attachment evidence does **not** establish embedding. All 1642 measured offsets are positive in both states: baseline 0.257805–0.828370 mm, proposed 0.269502–0.617698 mm. There are zero negative or newly negative measured vertices. The 50 micrometre per-correspondence diagnostic would fail for 126 inward and 31 outward changes, but its worst inward witness is reduced excess standoff, not measured skin penetration.

| Witness | Baseline front offset | Proposed front offset | Change |
|---|---:|---:|---:|
| Vertex 476, x = −24.496110 mm, proposed z = 1552.779913 mm | 0.828370 mm | 0.408173 mm | −0.420198 mm |
| Mirrored vertex 149, x = 24.496112 mm | 0.821754 mm | 0.403658 mm | −0.418097 mm |
| Vertex 491, x = −29.737912 mm | 0.351429 mm | 0.493199 mm | +0.141770 mm |
| Mirrored vertex 161, x = 29.737914 mm | 0.350833 mm | 0.492364 mm | +0.141531 mm |

The worst normal-change triangle, `(1335, 89, 477)` in polygon 986, exists in both actual triangulations. Its old/new normal dot is 0.029154 and area ratio 0.471499. It is a very thin facet: old edge lengths are approximately 1.362241, 1.331361, and 0.032079 mm. Its normalized triangle quality, `2 * sqrt(3) * double_area / sum(edge_length_squared)` with 1 meaning equilateral, is 0.011164 before and 0.005128 after. The near-right-angle normal change is consequently sensitive to a very small transverse displacement and is not by itself proof of a visible fold. The worst individual union triangle area ratio is 0.262007 for `(792, 143, 144)`, polygon 25, also present in both actual triangulations. Thirteen union triangles have old/new normal dot below 0.5, and six have area ratio below 0.5. No union triangle changes its signed XZ projection orientation.

I also checked stable polygon normals and neighboring polygon normals to avoid relying only on fragile sliver-triangle normals. All 1536 polygons retain positive old/new normal alignment, with minimum dot 0.532830. The edge topology has 3176 edges, 208 boundary edges, 2968 shared edges, zero nonmanifold edges, and zero same-direction shared-edge windings. There are real inherited sharply turning regions: adjacent polygon-normal dots below zero decrease from 36 to 26, with zero newly negative neighboring pairs. Actual triangulation adjacent-negative counts decrease from 37 to 24. These counts do not prove the surface is intersection-free.

Some inherited turns do become sharper. At edge `(143, 792)`, between polygons 24/25, the polygon-normal dot changes from −0.967655 to −0.999613. At edge `(477, 1335)`, between polygons 986/987, it changes from −0.151667 to −0.973265. The latter is near proposed `(x, y, z) = (−25.801158, −140.582979, 1552.649975)` mm. This deserves actual surface/self-intersection and native pixel inspection, even though it is not a newly negative adjacency. The smallest actual triangulated polygon-area ratio is 0.589535 at polygon 987. Polygon 217's much smaller vector-area ratio of 0.197385 is cancellation across a bent polygon; its actual summed triangle-area ratio is 0.669739, so it should not be described as an 80% loss of actual surface area.

Conclusion from the raw data: a polygon-correspondence repair is justified, but is not alone sufficient to release another full candidate. The data show no sampled embedding, no XZ orientation reversal, and no newly negative polygon adjacency; they also show local changes in already ill-conditioned, sharply turning ribbon regions. They do not prove the triangle interiors remain clear of the body or that inherited overlap/fold behavior has not worsened visibly. No appearance conclusion can be drawn without native renders.

## Proposed physical acceptance contract — design assessment only

The root proposes retaining all raw per-vertex offset changes while replacing the newly introduced brow-only per-correspondence 50 micrometre gate with a no-wider absolute standoff envelope: proposed minimum at least baseline minimum minus 50 micrometres, and proposed maximum at most baseline maximum plus 50 micrometres. Pairing this documented reclassification with a continuous body-surface separation proof and native appearance review is technically justified by the absolute evidence above. It must not be presented as a relaxation of any existing eye/lash requirement, nor as a retroactive pass for failed candidate 26. No implementation has been reviewed for this proposal yet.

For each actual final brow triangle, querying the full evaluated body's nearest-surface distance at its centroid and subtracting the maximum centroid-to-vertex distance gives a conservative lower bound throughout that triangle: distance to a fixed surface is 1-Lipschitz and a triangle lies in the convex hull of its vertices. Subtract floating-point query displacement and the stated reserve as well. Recursively split unresolved triangles into four, with every unresolved depth/node-budget leaf failing closed; completion and finite-value checks must cover every actual final triangle, not only changed or sampled vertices.

Unsigned positive surface separation alone also accepts a triangle wholly inside a body. Retain the positive front-ray offset check and establish that each ray origin is outside the body's front bounding extent, or provide an equivalent actual exterior witness. Positive separation plus an exterior witness is the relevant combination for showing the connected triangle stays on the exterior side. Continue exact polygon connectivity, union-fan nondegeneracy/orientation checks, actual new triangle self/eye/hair tests, and all six native views. Before a full candidate, exercise the certifier on clearly separated, intersecting, touching, near-clear, and deliberately unresolved cases and inspect the exact source. New geometry, an added post-subdivision projection modifier, or altered acceptance code needs its own bounded review; none is implicitly approved here.

## Findings and disposition

Candidate26 fails before save/render on equality of Blender loop-triangle tessellation. Raw diagnosis proves polygon loops and vertex identity unchanged;22 triangle entries change as the quads retessellate. The unchanged field then passes complete triangle/body separation in an unsaved probe and retains positive front-side distances, but both baseline and proposed brow ribbons have self-overlap pairs. Actual evaluated UV/alpha analysis is pending; no appearance acceptance or zero-self-intersection claim is made.

## Verification

Exact source, process ownership receipts and raw actual witnesses are retained in outputs/character-round3-20261108. Root findings are separate from the authored report. No runtime source is accepted by this record.

## Round outcome

Six integrated attempts are used and four remain. Current investigations remain bounded diagnostics; next full candidate number is27.

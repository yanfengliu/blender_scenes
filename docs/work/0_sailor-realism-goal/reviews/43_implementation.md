# Review 43: implementation

## Target

Visible brow overlap and actual UV topology.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 0c19bbe5ed5f59cac5a02cecd6bfd0a8dcee869ad7efed7b7d620d29a3315740.

# Brow overlap and UV diagnosis

2026-11-08. **Do not promote the original candidate-25/26 lift field on a transparent-padding exemption.** The complete proposed brow surface is separated from the body, but all 14 reported proposed self-intersection pairs cross texture regions with nonzero hair opacity on both surfaces. The baseline also has render-active overlaps; a smaller count is not evidence of an acceptable change because the intersection locations and texture opacity change. There is no native appearance result for this proposal.

This bounded review reads the exact saved source asset, the retained raw old/new surface, the full-surface probe and its certifier, and the actual evaluated UV/material capture. Numerical analysis used standard-library Python without Blender, a renderer, or file writes. The PNG was decoded directly from its lossless RGBA data because Pillow is absent in the repository environment; no dependency was installed. The original PNG was also opened at native resolution. This report is the only file written for this task, and no reviewer-owned background process remains.

## Evidence binding

| Input | SHA-256 |
|---|---|
| `brow-topology-probe/raw.json` | `6af54dda64cf0b18d50a1870d0d5c3e94a2b991097cb66d84bfade7ce7fc165f` |
| `brow-surface-probe/result.json` | `7fef0d3dc94280f5b1aff7d68cb169512ad8cc692145a9d1b12fcfa6aa4a39bf` |
| `brow-surface-probe/triangle_clearance.py` | `e0bb92aa2f30025c1a997c76e076a0fe47def24116cdd526e4483d8c5f0744db` |
| `brow-surface-probe/probe.py` | `5071be5e1a8eafe2a3d7319cb9683c9c47990722d4133547b0769351ac13479c` |
| `brow-uv-probe/result.json` | `2e8b0ccf4ea4274f7d43c49d32e6ed7ffb56a17f741098a88ff7961dd582eb76` |
| Asset `eyebrow007.obj` | `63326994bc56e0b0a29822d813daf96d48ba638e19523d9e21e9184e2f70e71f` |
| Asset/packed `eyebrow007.png` | `1827b24aaa1c928353027c5a86b8db59c1c22f06258b18faa2117d81f5ff9b05` |
| Asset `eyebrow007.mhclo` | `1c70518b0b4ed9cce46b5728e8b2ea1012466b54718f6ee82c03896546adb4ab` |

Probe paths above are relative to `outputs/character-round3-20261108/`. The inspected asset directory is `outputs/.worktrees/character-naturalness-round2/.tools/human_reference_assets/eyebrows/eyebrow007/`. The UV probe asserts exact correspondence of every evaluated vertex and loop triangle to the raw surface, captures every triangle's actual UV triple/material slot, and binds the actual packed texture. UVs were not guessed from the unsubdivided asset when evaluating intersections.

## What the surface evidence establishes

The source of `triangle_clearance.py` implements the reviewed whole-triangle distance bound: centroid nearest distance minus query quantization, maximum vertex radius, and reserve; unresolved nodes subdivide into four and exhaustions fail closed. The probe checks all 3072 actual triangles in both old and new states against all 293760 actual body triangles. Both states pass, with every evaluated vertex on the front/exterior side. The ray origin y = −0.5 m is outside the body's measured minimum y = −0.2237891 m. The receipt also records eight controls, unchanged baseline/raw inputs, and no save or render. Under the retained distance/reserve contract, the proposal is not embedding the brow in the body.

The baseline measured standoff range is 0.257805–0.828370 mm; the proposal is 0.269502–0.617698 mm, within a tighter absolute envelope. The earlier per-vertex relative 50 micrometre diagnostic was a separate introduced brow diagnostic and should not be confused with skin penetration or with any prior eye/lash clearance requirement. Candidate 26 remains a failed full build; these diagnoses are not a retroactive pass.

The probe reports 16 nonadjacent triangle self-intersection pairs for the old surface and 14 for the proposed surface. I independently reconstructed noncoplanar intersection segments from the retained double-precision coordinates for all 30 pairs. Validation across segment endpoints/midpoints found maximum plane residual 1.30e−16 m, minimum barycentric weight approximately −9.51e−12 from numerical error, and maximum barycentric reconstruction error 2.62e−16 m. All pairs produced intersection segments; they are not merely overlapping bounding boxes.

## Alpha does not exempt the new overlaps

The source material file declares transparency, disables backface culling, and disables cast shadows. The Blender source at `scenes/sailor_character_realistic.py:51-56` connects image Alpha directly to Principled Alpha; lines 288-300 apply it to the brow and disable its shadow visibility/specular. The actual captured material agrees: the packed image is the exact asset PNG, straight alpha, flat UV mapping, Linear interpolation, Repeat extension, active `UVMap`, and direct image-Alpha-to-shader-Alpha linkage. This is an alpha ribbon, but the topology is two connected disks, not disconnected overlapping hair cards.

I mapped each actual 3D intersection segment barycentrically into both triangles' captured UVs, then evaluated bilinear alpha using PNG row direction and pixel-center convention. Every proposed pair has simultaneously nonzero alpha on both layers. Fifteen of the 16 baseline pairs also do; only old pair `(80, 1168)` has one layer certified zero over the entire segment's conservative bilinear texel support box. None of the 14 proposed pairs has that zero-support exemption. Point alpha is not a rendered pixel prediction, but these substantial nonzero values directly reject the claim that the intersections occur only in transparent padding.

| Proposed pair; polygon owners | Segment length | Alpha on first / second surface at exact midpoint |
|---|---:|---:|
| Triangles `(92, 422)`; polygons `(46, 211)` | 41.366 micrometres | 0.479464 / 0.623785 |
| Triangles `(1612, 1959)`; polygons `(806, 979)` | 342.524 micrometres | 0.395904 / 0.565811 |
| Triangles `(38, 48)`; polygons `(19, 24)` | 2.854 micrometres | 0.051138 / 0.033391 |

For pair `(92, 422)`, the exact midpoint is `(0.024518888526, −0.140829093300, 1.552792523239)` m; its two UVs are approximately `(0.333325315425, 0.517863361612)` and `(0.335293558996, 0.521767079812)`. Along this segment, sampled alpha ranges are 0.470–0.486 and 0.619–0.627. Pair `(1612, 1959)` has midpoint `(−0.024887611134, −0.140759193231, 1.552743162398)` m and UVs approximately `(0.626623080067, 0.282953653711)` and `(0.624606805398, 0.286866746782)`; its sampled ranges are 0.375–0.464 and 0.553–0.630. These are hair-bearing regions. Native views would determine the visible severity; no appearance defect magnitude is claimed from alpha alone.

The existing coarse brow routine at `scenes/natural_face.py:72-96` expands ribbon thickness by 1.65 and refits control points to the skin before subdivision. The current field deforms this already sharply turning physical ribbon; fitting y changes where its layered portions intersect. The data do not isolate the 1.65 factor as the sole original cause. Merely projecting the same folded XZ ribbon onto the skin would not establish injectivity or remove texture-bearing overlap.

## Suitability of the source UV parameterization

The base asset has 124 vertices, 96 quads, 126 UV indices, and two disconnected disk components, each with 62 vertices and 48 faces. Each has Euler characteristic 1. There are no nonmanifold edges. Every shared base vertex has one consistent UV coordinate; the extra UV indices duplicate coordinates rather than introducing a geometric seam. All quads are strictly convex and positively oriented in UV; minimum convex turns are 1.40e−6 and 1.51e−6. Pairwise convex-polygon clipping finds no positive-area UV interior overlap above 1e−12 UV-area units in either component. This supports using the base UV layout as a disk parameterization for a different construction.

The actual evaluated UV capture has only small per-loop floating-point differences at a shared vertex, at most 2.15e−7 UV units. It should not be treated as a material seam. Any construction must deliberately choose its shared-vertex UV rather than allow face-local copies to split geometric positions.

| Property | Positive-x brow | Negative-x brow |
|---|---:|---:|
| Base face IDs | 0–47 | 48–95 |
| Evaluated vertex count | 821 | 821 |
| U range | 0.0412–0.9269 | 0.0418–0.9264 |
| Base V range | 0.4689–0.5490 | 0.2343–0.3144 |
| Current evaluated x range | +11.314 to +52.061 mm | −52.061 to −11.314 mm |
| Current evaluated z range | 1546.874–1554.734 mm | 1546.876–1554.735 mm |
| Least-squares x in mm versus U | `43.9789 * U + 9.53389` | `44.0255 * U − 52.1260` |
| Maximum x fit residual | 2.306 mm | 2.289 mm |

Increasing U increases x on both sides. Consequently U goes inner-to-outer on the positive-x brow and outer-to-inner on the negative-x brow. Mirror the anatomical direction explicitly; do not apply the same inner-lift convention to raw U on both sides. The linear fits describe current scale only and are not exact replacements for current positions.

Alpha-weighted V centers sampled through the active UV-strip vertical slice provide texture alignment guidance, not geometric acceptance targets:

| U | Positive-x brow V center | Negative-x brow V center |
|---:|---:|---:|
| 0.20 | 0.523912 | 0.290648 |
| 0.35 | 0.526731 | 0.294391 |
| 0.50 | 0.525367 | 0.290520 |
| 0.65 | 0.528825 | 0.294157 |
| 0.80 | 0.522761 | 0.286411 |

The texture tapers asymmetrically in raw U: the positive-x strip has no nonzero alpha in the tested U = 0.90 slice; the negative-x strip has none in tested U = 0.06/0.10 slices. Those samples are not a complete support-bound certificate. Retaining the existing UV/texture while mapping the disk to a monotonic physical X and a positive-width Z ribbon is a plausible distinct mechanism. However, an analytically injective formula sampled only at control vertices does not itself prove that the final subdivided triangles are injective. Verify actual final XZ triangles, disk boundaries, surface separation, hair/eye clearance, and native appearance before accepting it. No new candidate source, full attempt, or appearance is approved by this report.

## Findings and disposition

Reject the original lifted ribbon as-is. All14 proposed crossing pairs meet nonzero alpha, so transparency does not excuse the geometry. The two existing UV disks are consistent and nonoverlapping, supporting a distinct UV-derived construction. No mesh overlap count is treated as aesthetic improvement.

## Verification

Full actual receipts and source remain in outputs/character-round3-20261108. Root interpretations and subsequent outcomes are separate from the frozen report.

## Round outcome

Six integrated attempts used; four remain. No round3 runtime source accepted.

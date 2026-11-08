# Review 44: implementation

## Target

Actual derived texture-space values and narrow measurement correction.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 560c3390d444b6489522d052c95bb591489046b03027fd6c53a07d45c7af5108.

# Independent eye-probe texture-space repair review

Reviewed 2026-11-08. Scope: actual v2 noncoordinate failure, independent reproduction of its derived values, and the exact v3 repair/graph checks. Previous diagnostic failures and reports remain intact. No Blender, GPU, GUI, geometry save or render was run by this reviewer; only read-only Python checks and official Blender documentation lookup were used. This report is the only authored output.

## Decision

The actual counterevidence supports a narrowly defined derived-field contract. The six differing scalars are exact consequences of the new stored source bounds, rather than unexplained authored metadata changes. The reviewed v3 source preserves every literal value and permits only those six differences after independent geometry and shader-coordinate checks. It is suitable for one root-owned unsaved diagnostic. Actual material-graph independence and the six native negative controls have not yet been observed; they remain mandatory conditions of the live classification.

This is not an actual eye/lash/mouth safety pass. Both earlier native runs stopped before those measurements. The original 0.753494 source-gradient concern remains unresolved, and neither a candidate save nor a render is approved here.

## Actual v2 evidence

The inspected files under `C:/Users/38909/Documents/github/blender_scenes/outputs/character-round3-20261108/eye-root-probe-v2` are:

| File | SHA256 |
| --- | --- |
| `measurement.json` | `4c4e5753164c15756d4fa8dc5886742e5ecd98a92888b2bfa18a43db4055293b` |
| `noncoordinate-comparison.json` | `289f6355bfd296b1ae943ef86bdc3441637c22e128422048cb97c5ece05bd062` |
| `actual-evaluated-data.json` | `fc2f24457d4ba53248e063c08291695e34e006335d10211ec346dc549899ba48` |
| `run_probe.process.json` | `f327a1b59984fc7f37ceaa0c9f8dd967706a2d08a445d89c04e60fee55a0bb2a` |

V2 failed at its unchanged literal equality assertion. The owned process PID 54924 exited 1 and its tree closed after 48.380125 seconds. The wrapper binds runner `20b4b911406feacb00961ae24b28357de0399ad800dfbbbcb5a12bf133cc1b58` and manifest `bea95f2d606972d80a262b89d8991b642382126f588ba4245462afbc87cf4bf8`. All 48 recorded input hashes still match. The receipt records complete original scene/source/contract restoration, temporary-data cleanup and unchanged saved blend.

All 664 frozen body inputs matched. Baseline proxy replay was exact for 1,064 eye, 250 lash and 124 brow vertices, including final brow-ray Y; the complete refit no-op and proposed evaluated-eye equality passed. This establishes those baseline correspondences, not any later clearance or aperture result.

I independently traversed the entire 37 MB before/after comparison recursively. Its only six changes are brow `texspace_location` Y/Z and `texspace_size` Y/Z, plus lash location Z and size Z. The body's and eyes' complete noncoordinate records are exact. The full difference list exactly matches the retained receipt; no omitted field was inferred from a summary.

Using the independently hashed 74 MB actual coordinate artifact, I computed all eight object/state bounds directly from recorded float32 source coordinates. For each axis, location is `float32(float32(min+max)*0.5)` and size is `float32(float32(max-min)*0.5)`. Every component of both vectors matches every actual recorded value exactly, before and after, with automatic texture space enabled. No tolerance or approximate equality was needed. Thus the observed six differences are reproducible geometry-derived values. This evidence is specific to these nondegenerate meshes and installed behavior; it does not claim a universal formula for every Blender fallback or version.

## Exact v3 source and bounded replacement contract

Reviewed directory: `C:/Users/38909/Documents/github/blender_scenes/outputs/character-round3-20261108/eye-opening-native-v3-draft`.

| File | SHA256 |
| --- | --- |
| `source-manifest.json` | `3a98e6e1e08ee1956be02bf3d050a214dcff586ce4f0d46eec6e17c3855ee517` |
| `probe_native.py` | `c8d93ce9f12d67afecad841738c30cbcec0418e2a87e2d89aae73ff650b6dfac` |
| `derived_metadata.py` | `491d77f3cce8f47c34ea0442b59690a65e2ee5cc030d1753dd48798b48a084ab` |
| `actual-bounds-proof.json` | `0ca3e2e18f21518945b46cb0c880efe354ea1bd357bc29faf654457009f69365` |
| `native_checks.py` | `70e019bb1bf0384e184b478d52d3d34c966d22bc51cdd9d44d4b7debb2689984` |
| `native-inputs.json` | `1bcacc5f57c58537c2082875b6994112ce909206cca212866f65c265bc41a369` |

All 53 manifest entries independently match. The safety helper, full proposal input and exact difference reporter are byte-identical to v2. The runner diff adds only the derived-field/shader checks, native metadata negatives and restoration checks; the 664-row proposal, proxy fits, source order, populations, original-neutral mouth contract, 50 micrometre bounds and continuity checks are unchanged.

`derived_metadata.py:9-42` allows only the six exact scalar paths observed in v2. Both complete location/size vectors must still equal the independently computed before/after geometry bounds, both automatic flags must be true, every coordinate must be finite binary32, and nondegenerate bounds are required. All differences remain recorded. A changed unlisted component, wrong derived value, manual setting, UV value, custom data, topology or material field fails. Literal equality is reported honestly as false when those six fields differ; `noncoordinate_contract_pass` is the distinct causal assertion. This repairs an instrument's mistaken expectation about derived values without hiding its original failure or weakening the retained authored-state requirement.

I replayed `prove_actual_bounds.py` with its writes/printing omitted. All eight actual proofs and seven pure classifier controls exactly reproduce the retained proof JSON. They reject an incorrect derived value, manual mode, a UV-active change, custom data, unsafe mapping and a changed graph. The test's fabricated safe-mapping input is explicitly a pure control; it is not evidence about the saved material graphs.

## Shader-coordinate dependence and native negatives

The complete actual brow/lash material graphs must be captured before and after and compare exactly (`derived_metadata.py:44-83`). The supported node set is restricted to image textures, Principled/output, scalar math and explicit UV maps. TexCoord, procedural texture, group and unknown nodes reject, including disconnected unsupported nodes; this is conservative. Animated graphs, muted nodes, volume/displacement links, non-flat image projections and unpacked images also reject. Images must use the single active render UV layer either through a matching explicit UVMap or an unlinked Image Texture vector input. The latter uses the active UV map according to the official [Blender Image Texture manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/image.html?highlight=image+texture).

The snapshots include nodes, links, socket values, node/image properties, color space, packed-image hashes and texture mapping. Actual v2 metadata shows DATA-linked slots for both affected meshes before and after, so enumerating their mesh materials covers their effective materials in this exact scene. The unchanged slot comparison preserves that fact. This source does not merely trust material names or an asserted `safe` flag from an external receipt: the live extractor sets `safe` only after all supported-graph assertions pass.

The six mandatory native negatives operate on temporary private copies: a real UV edit, custom split normals, a custom attribute, a material-slot replacement, manual texture-space mode and an actual Generated-to-ImageTexture connection (`derived_metadata.py:85-120`). The custom-normal call is present in the official [Blender Mesh API](https://docs.blender.org/api/current/bpy.types.Mesh.html?highlight=_sel); runtime success is still unproved. Unsupported graph/custom-normal assertions are explicitly treated as rejection, while a mistakenly accepted mutation cannot be swallowed by that exception handler. Each copy is restored and removed in `finally`.

The final frozen runner additionally rechecks exact proposed noncoordinate metadata, every stored coordinate and the complete graph after those negatives, before continuing to the original safety measurements. Full original-scene/data/source/blend restoration remains in the outer cleanup. These controls must actually run and their recorded reasons must be inspected; their presence in source is not a native pass.

## Execution and review limits

No blocking source defect was found in this narrowly scoped revision. Root may run the exact unsaved diagnostic to obtain the actual shader graph, mutation controls and previously unreached safety evidence. Before accepting the derived-field classification, independently inspect both captured graphs, their actual coordinate-input paths, all six negative-control results and exact proposed-state restoration. If any graph is unsupported or any value differs outside the six proven paths, preserve the failure; do not broaden the exemption automatically.

The actual eye/lash/brow bounds, original-neutral mouth metric, complete topology containment, hair/skin test and evaluated continuity evidence remain unmeasured at this review point. Even a successful v3 classification would close only the metadata issue. Prior failures remain failures in their preserved records; the face experiment and inherited F21 are not accepted. All read-only reviewer commands completed, and no reviewer-owned persistent process remains.

## Findings and disposition

The v3 native diagnostic subsequently proves UV-only material graphs and all six unrelated-mutation negatives, while preserving complete values and state. It then rejects the proposed eye-opening geometry on actual1.328mm additional eye penetration and lash fit failures. The instrument correction does not accept the geometry.

## Verification

Full actual receipts and source remain in outputs/character-round3-20261108. Root interpretations and subsequent outcomes are separate from the frozen report.

## Round outcome

Six integrated attempts used; four remain. No round3 runtime source accepted.

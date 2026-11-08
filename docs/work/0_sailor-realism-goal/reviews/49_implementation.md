# Review 49: implementation

## Target

Exact production UV-brow integration, maintained saved/production geometry checks and reopened character regression.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns delivery and native acceptance.

## Reports

Complete authored report, SHA-256 `534c26768e153400dc8c3ccb187b34d708366fdb9db9f1f21a72bc08937fde65`.

# Production brow integration review — 2026-11-08

**No blocking finding in the reviewed production integration or maintained regression checker.** The production helper reproduces the accepted candidate-27 construction, and the root-owned execution of the actual production call site produced exactly the accepted float32 brow coordinates and UVs. This review approves the localized source integration; it does not declare the whole character finished or independently repeat candidate 27's visual acceptance.

## Exact reviewed source

Paths below are relative to `outputs/.worktrees/character-naturalness-round2`. The baseline is main `7d7b7e0aab821db1707033ccd5927fcefe30a45f`; the pre-change Python source archive is `outputs/character-round3-20261108/runtime-source-before-brows/manifest.json`.

| File | SHA-256 |
| --- | --- |
| `scenes/relaxed_brows.py` | `68d3f8e8cff35cfa77d7dac48362bda999dbca78ff2e5962fd9d8d74d2f4f689` |
| `scenes/sailor_character_realistic.py` | `4cc5a800ca14f61893e53f5c9a52384e7f58a8a0c29122bb8402409f9cd04f70` |
| `tools/check_relaxed_brows.py` | `fd7029ce3643447fa2822a0c8710716707b355e8a25112a3301b2455112308fa` |
| `tools/check_realistic_character.py` | `714ea8893f221eb79500cfadd82ef232f82b59afc64f574aa455c5ef9991e3d4` |
| `tools/brow_uv_checks.py` | `495f3ec0de82524c11f31c6a9b947ff81c09bc88759ec2d6fd2ae0606a7f95fa` |
| `tools/triangle_clearance.py` | `e0bb92aa2f30025c1a997c76e076a0fe47def24116cdd526e4483d8c5f0744db` |

The accepted prototype helper is `candidate27-source/uv_brows.py`, SHA-256 `e5c0f1208d19bc856b950d285d208d9bcdc3d146f31fe03837c6b80e7624178b`. I compared both source and parsed syntax trees: production differs only by importing `hashlib` and asserting the packed texture hash `1827b24aaa1c928353027c5a86b8db59c1c22f06258b18faa2117d81f5ff9b05`. All coordinate calculations are identical. The projected-disk checker and continuous triangle certifier are exact previously reviewed copies; their original geometric scope and numerical limits remain as recorded in `brow-uv-construction.md`.

## Integration and retained state

The scene delta removes the legacy `fit_fuller_brows` call, creates the same native proxy mesh with the same topology, UVs, material and subdivision settings, then changes only that object's vertex coordinates through `fit_uv_brows`. The legacy fit returned every `point.x` unchanged, so skipping it preserves the x bounds used by the new parameterization. Both routes first store those coordinates in Blender float32 values. Material setup after the call, eye assignment, eyelash handling, body construction, hair construction, clothes, lights and cameras are unchanged in the source diff.

One real integration difference required verification: production fits brows before `finalize_upper_frame`, whereas candidate 27 fitted the finished saved body. The frame map is zero at forehead height, but whole-body ray evaluation can still require exact runtime comparison. The verification executed the actual parsed production prefix, including the new call, and then its real final frame assignment. It compared every body vertex, brow vertex and brow UV loop against the accepted saved candidate. All were exactly equal, resolving this concern for the reviewed source and assets. This is stronger evidence than running the helper only on the already-final saved body.

## Checker and observed verification

`validate_brows` is called by the maintained whole-character validator. It pins the accepted source-coordinate hash `fdaf6f8106f99f88086eeafe9e6d5c798d9c19d774ec4aa709ef5e93d946db28`, evaluates actual render subdivision levels and restores them in `finally`, checks two simple front-projected disks, establishes positive exterior front-ray offsets, and certifies every actual triangle clear of the actual body surface. The coordinate pin preserves the visually accepted expression; it is intentionally not a general classifier of attractive or relaxed eyebrows. The body separation check proves continuous surface separation rather than relying on vertex samples alone.

I read `brow-production-verification/verify.py` (SHA-256 `24c53af440f0c89d2e6320c14f8a9d33ecba4810eb4acc5877b8a031e7b0319e`), its log, and `result.json` (SHA-256 `5d4a25aa250d2de4b40725be4413895ad74e656f98546b3074848fa9e46a2554`). The root reports owned PID 51148 exited 0 and closed after 11.7865 seconds; the log ends with Blender quitting. Both saved and production geometry have 3,072 positive projected triangles, two simple 104-edge boundaries, minimum signed double area `1.7618706493749414e-9 m²`, and 3,072 successful continuous body-clearance certificates. Both report the same positive standoff range, 0.2087652683–0.4645287991 mm.

The actual legacy candidate-10 folded projection was rejected. Saved and production runs each rejected four controls: folded surface, inner hook, buried brows and floating brows. Buried/floating controls disable the visual-coordinate pin so they exercise physical geometry checks; the inner-hook control intentionally exercises the accepted-shape pin. Mutation controls restore original coordinates in `finally` and verify the accepted coordinate hash afterward. I independently parsed all six reviewed production/checker files and ran all eight pure triangle-clearance controls without launching Blender.

## Limits

This was a bounded read-only review, with only this report authored. I launched no Blender, renderer, GPU job, browser or GUI. Runtime evidence above was produced by the root and inspected here. The production-prefix check omits regenerating unrelated hair and clothing; their source remains unchanged, and candidate 27's complete retained-state, physical and native-view acceptance belongs to its existing evidence. The whole-character saved checker is still running as of this report and is not claimed passed here. Hair realism and inherited lower-hair F21 remain outside this localized brow acceptance. No new native appearance claim or unrelated eye change is made.

## Saved-checker completion addendum

The root-owned whole-character saved checker subsequently completed successfully. I read its process receipt: PID 24120 exited 0, its process tree closed after 22.679682 seconds, and the script SHA matches the reviewed `check_realistic_character.py` above. I parsed the complete JSON report from `check_realistic_character.log` (SHA-256 `5ef702a166dada9cad7547d5352850eaf8953c34bde9743e34a4f39a8865174e`) and verified that every field in `saved-check-summary.json` (SHA-256 `77f5ef0c6f69e1109d9c1aa462af80f6ddb6d6ccbaad08b7287c256a11cc803e`) matches it exactly. Overall status and the newly integrated brow check are both `pass`; the log ends with Blender quitting. This resolves the pending saved-checker item above. Its report still explicitly does not certify whole-character visual acceptance, and this review preserves that limit.


## Findings and disposition

No blocking findings. Root accepts the exact production integration, which reproduces all accepted body/brow coordinates and brow UVs. Runtime repository gates remain required before committing.

## Verification

The actual production prefix and saved file both pass all 3,072 continuous brow-triangle certificates and geometry controls. The historical folded surface is rejected. The full reopened character checker passes existing eye, hair, neck, sock and live smile checks plus the new brow gate. Receipts are retained under `outputs/character-round3-20261108/brow-production-verification`.

## Round outcome

Candidate 27 is accepted locally. Seven integrated attempts used, three remain, next 28.

# Review 47: implementation

## Target

Six native candidate-27 views against the baseline and adult reference.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns execution, integration and visual acceptance.

## Reports

Complete authored report, SHA-256 `fa82ca19828813643e9079b6d1d00a2fcca06c0c1dfec852d15564770636ba76`.

# Candidate 27 independent native visual review

Date: 2026-11-08. Scope: visible local brow and expression improvement over unchanged candidate 10 for the requested natural, cute adult expression. Verdict: **ACCEPT as a local brow improvement. Whole-character realism remains open.**

I inspected the original reference first, then all six candidate-10 PNGs, then all six candidate-27 PNGs using `view_image` with `detail: original`. I formed the visual verdict before reading render-receipt metadata. I did not read the author's proposal, source code, geometry reports, or other aesthetic reviews. Source files were subsequently hashed without reading their contents. Repository instructions and the fleet review runbook were read; `docs/learning/lessons.md` was absent in this checkout. No Blender, GPU job, browser, GUI, or background process was launched; there are no task-owned persistent processes to clean up.

The baseline's inner eyebrow ends make conspicuous dark, downward hooks toward the bridge of the nose. Those shapes tighten the expression even though the mouth has a small smile. Candidate 27 visibly removes that inward pinching impression. Its flatter, finer brows make the forehead read relaxed in the portrait and oblique views. I do not read the new expression as frowning, worried, or surprised. This is a visible change at the supplied native portrait resolution, rather than a change inferred from measurements.

The new brows have a fine, tapered hair-line appearance with visible strand variation, particularly around the inner ends. Their outline no longer looks like a heavy hooked strip. They are still unusually thin, faint, and neatly combed compared with the fuller, irregular brows in the reference; this is a remaining realism limitation, not a reason to reject the evident expression improvement. The brow shape sits plausibly against the face in the supplied views. I see no visible fold, doubled band, detached/floating edge, or brow clipping artifact. The fringe partly conceals their upper boundary, so these images cannot establish invisible geometry correctness.

| Native view | Size | Observation |
|---|---|---|
| `portrait.png` | 1200 x 1200 | Strongest evidence of improvement. Both dark medial hooks are replaced by softer, nearly level inner sections. The eyes and slight smile now work together more calmly. No high arch or raised medial peak creates a surprised or worried expression. Fine brow texture remains visible, though sparse and more groomed than the reference. |
| `face_oblique.png` | 1200 x 1200 | The near eyebrow follows the forehead without the baseline's abrupt downward end. The far eyebrow remains coherent beneath the fringe. The relaxed expression holds from this angle; no obvious brow lift, fold, or separation from the skin is visible. |
| `hero.png` | 1280 x 1600 | Brow changes are subtle at the smaller face scale, but the brow region does not create a new severe expression. Overall head, face, body, clothing, and pose retain the same adult character proportions. This view alone would be insufficient for judging individual hairs. |
| `profile.png` | 1200 x 1200 | Most of the eyebrow is occluded or strongly foreshortened. The visible portion near the fringe has no obvious protruding or floating strip. Facial profile and adult identity remain visually consistent with the baseline. Limited evidence for the full brow shape. |
| `back.png` | 880 x 1100 | No eyebrows are visible. This is a silhouette and proportion regression check; no apparent change in the head, body, or clothing silhouette. It supplies no positive brow evidence. |
| `torso_random.png` | 1200 x 1400 | The gentler brow impression survives this alternate view. The face reads softly attentive with a small smile, without the baseline's stronger inward brow pinch. Body proportions and adult presentation remain consistent. Fine strand quality is less assessable than in the portrait. |

The character remains recognizably the same adult model. I see no new juvenile proportion shift, large facial change, or identity regression. Acceptance is limited to the brow/expression delta. The full character still falls short of the photographic reference in hair mass and natural irregularity, facial surface/feature realism, and clothing behavior; those broader issues were not repaired or approved by this review.

## Artifact binding

All six candidate-27 file SHA-256 values and PNG header dimensions were computed independently and match `render-receipt.json`. Its status is `rendered_pending_native_visual_review`, candidate number 27. All six required image entries exist and were viewed. Receipt SHA-256: `8af3e25f50b8afaa9e923aa17597a97d46c736561dc7230086a968f5042c5b8f`.

Candidate image root: `outputs/sailor_character_realism_goal/candidate-27/`.

| File | SHA-256 |
|---|---|
| `hero.png` | `4917e20b8ff991aff9ee19106ec324a9420c5da2ea3d94752ec673c8b6638dfc` |
| `portrait.png` | `fccce2ac20a3c8a8c8531e35dd822cc943128db83771a6d8849a004ab7d2b00f` |
| `profile.png` | `d0975c1eec2b060fdb0f1c7a105483bde4d766e24e0da3b76d94c6de207a0b83` |
| `face_oblique.png` | `d0f4fb9c8dedfd15081436b1d7d3b1a81f32578c825f61c12d482adf6d52fa29` |
| `back.png` | `d41319f08dc69f265c774e8c38e25f66707561ed899b41c00350f1259dcd0cb2` |
| `torso_random.png` | `8f3621fd917e1d2ec8b5e3d5bd3e083382a39da116ea886df1887551e278ffa4` |

Source/artifact root: `outputs/character-round3-20261108/candidate27-source/`. Independently computed hashes:

| File | SHA-256 |
|---|---|
| `build_brows.py` | `41887a14a11bda58d9d34458d2f2d841a79e7dfe8341a2da3f65ac1e519965d4` |
| `render_brows.py` | `c6cd180865cec35cc139e6c9fdc454b6e0b977e14d7e99feceba71da5cfdfd8f` |
| `build-result.json` | `f26d7afca99032bf04f6c0fa376c1db1a6975a5d850d389d317bb79962219b2c` |
| `source-manifest.json` | `4e243d5ac51f770f141e14c1f40717f114a3d7840589d885e129e2e30c2d613f` |
| `provisional.blend` | `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2` |

The render script, build-result, and saved blend hashes match their receipt fields. This binds the visual review to these artifacts; it does not independently prove their internal geometric properties or that the scripts reproduce them.

Reference: `outputs/sailor_character_proportions/references/character-reference.png`, 1713 x 918, SHA-256 `ea71fef894f068da0736a177ce4619ef176d0719581033cab8781b63f18e1139`.

Baseline image root: `outputs/sailor_character_realism_goal/candidate-10/`. Dimensions match the corresponding candidate-27 views.

| File | SHA-256 |
|---|---|
| `hero.png` | `1c1895fadb01bf4af7578b6f77d0f68dbb867656810a2a18d14ae13930fa9503` |
| `portrait.png` | `8a312efd5f083cf04d3daddd9c18f893584b58faac8bdb8c13029ee6dfe65a09` |
| `profile.png` | `4c33b1807012a4284bcaea04863f3f77c6a4a0967bf457fa1a5b75939aa46046` |
| `face_oblique.png` | `48d051b2c71898d58a1e11249bba83de0bb1565468f6dd95113991c7fa9a4a9b` |
| `back.png` | `98dd22cc70a791aaabfae1eeeda29f5f550d5b52b96d543c73440fec150e7d49` |
| `torso_random.png` | `722a04eb44240abf56978e920dc21db4257f1a7ac0d51818148bea7f5da883b1` |

This is a static native-render review of the six supplied cameras, including the supplied random torso camera. No animation, additional camera, different lighting, source-level implementation, or numerical clearance gate was tested. The author/integrator owns those checks. No full-character completion claim is warranted.


## Findings and disposition

Root accepts the local brow improvement; complete character realism remains open.

## Verification

Exact reports, source and native receipts are retained under `outputs/character-round3-20261108`.

## Round outcome

Seven integrated attempts used, three remain, next 28. Candidate 27 is accepted for the local brow scope.

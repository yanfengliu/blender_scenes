# Review 0: integration

## Target

Goal candidate1 against accepted proportions2, base0b79ee16f9bb0aeedc4503507f38c735276879ca. The uncommitted used sources and exact patch are retained under outputs/sailor_character_realism_goal/candidate-1/source and natural_face.patch. Skin source SHA290E64545F2CFA95E115AD8F773E01555516338A29BA2DB62CA24DFB6C484611. Saved blend SHA CA22A22F6441AE8543B830C58A50A1378C336C45443C43CE50C4FE48D14864F6. Exact five image digests are in the immutable artifact-manifest.json and oblique-receipt.json; changing those bytes requires a new review.

## Reviewers and coverage

Root and independent visual_review inspected all four canonical images plus the fixed opposite-side oblique natively against baseline and reference. build_runner independently inspected those views and ran the saved structural and data-comparison checks. No reviewer claimed photographic completion.

## Reports

### visual_review

Retain skin candidate1 as a small material improvement. Photographic skin remains unmet. Nose and lower-lip highlights describe their curvature more clearly. No broad lacquered shine, new limb glare, or visible surrounding regression appeared across the five views. Cheeks/jaw remain very smooth; reflections lack the reference's fine surface breakup. More roughness/IOR tuning alone is unlikely to close that gap.

### root

Retain skin1 as a bounded local material improvement: clearer nose/lower-lip reflection without broad new glare. This is not a photorealism pass. The reflection-only tuning route is insufficient for missing fine breakup; keep the goal active.

### build_runner

Actual saved comparison permits only the eight declared reflection sockets and output path. All115 captured object states,27 material-attribute mesh sets,16 other material graphs and four packed images remain exact baseline. Native review still finds broad smooth pale cheeks, forward mouth form and rigid curtain hair dominant.

## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
| --- | --- | --- | --- |
| F0 | Skin reflection gain is local; fine breakup and photographic likeness remain missing. | Retain the increment; do not close CHR-001. | Test separately justified geometry/groom mechanisms instead of another scalar pass. |
| F1 | Forward mouth form and rigid curtain hair remain far from reference. | Unresolved; source/data identity does not certify form. | Separate perioral and regional-groom families under the fixed benchmark. |

## Verification

Canonical4 at1600/128 and the fixed85mm opposite-side oblique at1200square/128 rendered successfully. Unchanged standalone checker and reflection-only saved comparison both exit0; both saved files remain unchanged. Capture excludes arbitrary RNA pointers and expanded curve tubes. Geometry-fit evidence transfers only over the exact unchanged deterministic geometry inputs. Full receipts are in candidate-1/verification-summary.json; all owned Blender jobs closed.

## Round outcome

Candidate1 is retained as a local material improvement. Full realism remains incomplete; no later candidate inherits this image review.

## Correction — global finding IDs, 2026-09-08

The original table above used IDs local to this review. Findings are now assigned once across this work unit, as required by the shared work-doc format. This appendix preserves the closed report and makes its mapping explicit: round0 F0 is global F0 (skin response and fine detail); round0 F1 is global F1 (face form and grooming). Later rounds reuse these global IDs for the same findings. The exact pre-correction document is retained at snapshots/20260908-before-finding-corrections/0_integration.md.

Pre-correction snapshot SHA256: `5b161396c85e5258b07972e8322f1218088da63368fb7f7df617c0ef18edd21c`.

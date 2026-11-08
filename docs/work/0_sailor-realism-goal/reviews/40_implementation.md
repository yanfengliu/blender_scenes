# Review 40: implementation

## Target

Brow-only medial lift, exact retained scene and native six-view source.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual Blender execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 2a2f199e65daab8616dc99efed158e388180a1cb1ed27c5feb0cec35c810c81a.

# Candidate 25 bounded brow source review

2026-11-08. Disposition: **No blocking source finding; ready for the root-owned build and native appearance trial.** This is approval of the bounded experiment's source, not acceptance of the brow appearance or the full character. I did not run Blender, a GPU renderer, browser, GUI, or the candidate scripts. I read the three draft Python files, their manifest, and relevant imported helpers. The report is the only file I wrote; no reviewer-owned background process remains.

The exact reviewed manifest is `outputs/character-round3-20261108/brow-candidate25-draft/source-manifest.json`, SHA-256 `4cec167ae5b96fdf88b22263789ab9f98a80cad15a7c4847c013c0ccf0e62236`. I recomputed and matched all three local hashes and every external-source/artifact hash in that manifest. The files reviewed were `build_brows.py` (`eeef336cc59e8b92d912952f86256c21224990fccf24eb3ce8365acb089a54db`), `relaxed_brows.py` (`f17fa4978b6a81cd1abcc1f2af6c72c33a2bcaf76386c24427fc5de781133aff`), and `render_brows.py` (`96538943ca27f43d8e0186d63f1629c08bbc526f29f57e3ad92f82cda8cdd1d5`). A subsequent source change invalidates this exact-revision disposition where it changes the reviewed behavior.

The correction in `relaxed_brows.py:5-10` is a symmetric, bounded 2 mm inner lift with a smooth transition to zero at an absolute lateral coordinate of 32 mm. The fit at `relaxed_brows.py:13-33` leaves x coordinates intact, leaves zero-lift control points exactly intact, and moves changed points to the existing 0.45 mm forward skin-offset convention. The baseline implementation at `outputs/.worktrees/character-naturalness-round2/scenes/natural_face.py:72-96` uses the same ray direction and offset. There is no enlargement of eyes, head, or body and no material edit in this trial's implementation. The source does not establish that this amount produces the desired expression; that must be judged after rendering.

The retained-state wrapper at `build_brows.py:33-39` temporarily restores only original brow coordinates for `fixed_state()`, then restores the candidate coordinates in a `finally` path. It separately hashes body coordinates, which the imported face-only `fixed_state()` intentionally excludes. The imported state helper at `outputs/character-round3-20261108/candidate24-source/face_candidate24_helpers.py:33-78` binds the remaining scene, materials, cameras, render settings, and hair state; the underlying retained-mesh snapshot at `outputs/.worktrees/character-naturalness-round2/tools/check_character_variant.py:51-65` includes mesh topology and attribute data. Thus restoring brow positions for the comparison does not also mask topology, UV/attribute, modifier, or material changes. The build's exact coordinate, retained-state, saved-copy reopening, and source hash checks at `build_brows.py:79-107` are appropriate to this static baseline experiment.

The evaluated checks use the same vertex/topology identities for baseline and proposal, reject degenerate or reversed triangles and substantial area collapse, and reject nonadjacent triangle intersections (`build_brows.py:51-64`). The changed-patch hair check is applied to the evaluated brow surface rather than the body: the imported `changed_skin_hair()` needs only the matching evaluated topology/positions and polygon ownership supplied by `evaluated()`. Inspection of `face_candidate24_helpers.py:114-159` confirms that this helper checks every stored strand against all affected final polygons, with capsule radius and fail-closed adaptive subdivision. Its copied labels still say changed skin; for this call they mean changed brow ribbon. The full-brow/eye intersection check follows at `build_brows.py:96-98`.

The renderer requires the passing build receipt, exact saved scene, baseline and source hashes before rendering. It reloads baseline and candidate independently and rechecks exact retained state (`render_brows.py:14-34`). The four existing cameras and two benchmark auxiliary views are recreated consistently; the fixed seed and receipt checks preserve the random torso camera (`render_brows.py:50-64`). It uses native benchmark dimensions, 128-sample Cycles, and OptiX, and leaves appearance pending. Its `finally` block restores scene camera/settings, removes the two task-created cameras, and checks saved inputs and retained state again (`render_brows.py:75-89`). Process ownership/termination remains the root launcher's responsibility and was not verified by this source review.

Coverage limits, not blocking findings for this small trial:

- The 50 micrometre attachment comparison in `build_brows.py:42-48` and `build_brows.py:89-93` samples every evaluated brow vertex. It is not a continuous clearance proof for triangle interiors and compares offset change to the baseline rather than proving an absolute baseline clearance. Describe it as an evaluated-vertex fit check, and use native oblique/profile inspection to catch visible embedding or floating.
- The self-intersection filter excludes every triangle pair that shares a vertex. Its successful result certifies the tested nonadjacent pairs, not every possible adjacent-fan overlap. The bounded x-preserving lift, topology preservation, normal/area checks, and native inspection provide the relevant additional safeguards here; avoid claiming a general arbitrary-mesh self-intersection certificate.
- Exact unchanged outer positions are asserted on the control vertices. Subdivision can transmit an inner control-point motion into nearby evaluated points. The trial does not establish an exact unchanged evaluated outer half by that control assertion alone; native appearance must confirm that the outer brow remains visually consistent.
- The source preserves UV data and applies the same vertical lift at the same x. It does not explicitly measure physical ribbon thickness after refitting to the curved skin, so an unqualified numerical claim of exact three-dimensional thickness preservation would exceed these checks.

Required acceptance remains a root-owned successful build/reopen result and all six exact native renders. Judge whether the inner ends look relaxed rather than frowning, worried, or surprised; check both frontal and oblique views for brow/skin continuity and hair interference. An invisible difference does not resolve the owner's complaint. Keep adult proportions and expression; the inherited lower-hair F21 and whole-character realism remain open. No independent runtime test or appearance approval is claimed in this report.

## Runtime failure addendum — 2026-11-08

Candidate 25 failed before any proposed coordinate edit, save, or render. The original source-review disposition above is retained as authored; it did not establish the actual saved baseline modifier settings, and the runtime failure now supersedes readiness to execute this exact revision successfully. This is an instrumentation/assumption failure, with no brow appearance outcome.

I read the actual retained `outputs/character-round3-20261108/candidate25-source/build-result.json`, process receipt, and log. The executed three Python files and manifest have the same SHA-256 values as the reviewed draft. The build-result SHA-256 is `4de0457d7584714a945b39c8976d9c7919929bbec817c5487044c9398fcff396`; its status is `failed`, with the traceback at `build_brows.py:80`. The assertion assumed the single brow SUBSURF modifier had both viewport `levels` and `render_levels` equal to 1. The root reports that the saved modifier instead has render level 2. The scene source at `outputs/.worktrees/character-naturalness-round2/scenes/sailor_character_realistic.py:86-96` confirms that `mesh()` sets `mod.levels = sub` and does not set `render_levels`; the exact live settings still require the root's planned unsaved diagnostic. The read process receipt reports exit code 1, PID 33824, `process_tree_closed: true`, and 2.9539304 seconds; the log ends with Blender quitting.

The assertion is before the initial coordinate copy/state snapshot at line 81 and before `fit_relaxed_brows()` at line 83, consistent with there being no candidate deformation or saved scene. Candidate 25 must remain a failed attempt, not a rejected or accepted appearance. The root's attempt accounting is five used and five remaining after this failure.

Candidate 26 is a separate proposed instrumentation repair with the same brow field: determine the actual modifier contract, explicitly evaluate the rendered subdivision level for physical checks, and restore temporary level changes in a `finally` path. That revision has not yet been reviewed here. The correction must also ensure that supporting skin rays and compared brow/eye surfaces use the intended evaluation mode; simply changing the line-80 expected constant would leave viewport-only checks unable to certify the finer rendered ribbon. No files from candidate 25 were changed by this reviewer.

## Findings and disposition

Candidate25 fails before geometry changes because the driver assumes viewport and render subdivision are both1. The actual read-only modifier capture proves viewport1/render2. No save/render or appearance result. Same brow field remains under investigation.

## Verification

Exact source, process ownership receipts and raw actual witnesses are retained in outputs/character-round3-20261108. Root findings are separate from the authored report. No runtime source is accepted by this record.

## Round outcome

Six integrated attempts are used and four remain. Current investigations remain bounded diagnostics; next full candidate number is27.

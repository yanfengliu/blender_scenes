# Review 26: implementation

## Target

Final round-2 attempt 20, based on 0032b5963128707ad23044b18000efc4fdfe828c. Exact 12-source target, controls, failed outcome and authored preflight remain in outputs/character-round2-20261107/hair-attempt20-evidence; archive-manifest.json SHA256 e851896722260d2712873d2c84e34a20007cb7528db0fdc1b7743f4e8943796b. No production changes. The reviewer completed source readiness; a subsequent model usage limit prevented an independently authored runtime addendum. Root dispositions below are separately attributed.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 8677acd0a65cc8665f198b8f86510e1bcc0682e35d117b3e49569f5a38cacd9e.

# Independent attempt20 source readiness review

## Decision and scope

Reviewed 2026-11-08. READY for one bounded final attempt using the exact sources below. I found no material source blocker in the two authorized construction changes or the renderer target adaptation. This is source readiness only: no attempt20 geometry, stored population, saved scene or appearance is accepted. At the end of source inspection, `result.json`, `process.json` and `candidate20-provisional.blend` did not exist in this directory. Nine substantive attempts were already used; this readiness does not authorize a retry, tuning loop or additional integrated attempt after20.

The parent identified base `0032b59` with unchanged dc67-era runtime. The review binds the ignored instrument bytes directly, rather than treating that Git base as their identity. I reviewed the complete changed shared-field and probe paths, compared them with the reviewed attempt19 sources, checked the retained acceptance and save paths, and inspected the renderer diff. I independently verified every manifest hash and Python AST, and reran all four pure control suites with bundled Python and bytecode writing disabled. Those imported control calls did not write their entry-point artifacts. I launched no Blender, renderer, GUI or additional agent, and changed no implementation or plan.

## Exact reviewed targets

The following paths are relative to this report's `outputs/round2-hair-search/attempt20` directory in the isolated `character-naturalness-round2` worktree. `preflight-sha256.json` has SHA256 `5e797fb134379ac90c12eb8f8b1e61ce6c1f933c8cf1dba2870c139126089889`; `preflight.md` has SHA256 `68c3bc69a6cf7eaddd7b8c11444dc0536557746a9f7e757cd2c8d36e02a78025`. All 12 manifest entries matched their current file bytes at review time.

| Source | SHA256 |
| --- | --- |
| `shared_field.py` | `35735c2a7867bc946e0b66162bf4f1976b402ef8e5925ea1a4f5d6f551352bf2` |
| `probe.py` | `41dd754aeb01ee9036beb6582f6e8f77f04926a3b11d78cea93f73f5d0ae9022` |
| `run.py` | `83e3cef4a862a68820f2132cffe8c7aaaa4322e4a5c61b08af37ac803ed9e48a` |
| `adaptive_ball.py` | `04bf5807480d3c157c853f26220e33de3fb9fb77f0e66ae59563e027dc5a1da3` |
| `adaptive_controls.py` | `d05abd5a93c178ff90efee0e39cafc313a3eccc9bdb96797cbc2093747d1fb43` |
| `reference_controls.py` | `d4e2f6cd6869640620943aa9b7ebffdbbcf0e7ec85dbe34434de859297e47e12` |
| `cell_certificate.py` | `af5417d2aac6f1010dc4bf2cfe07540df24686034d2da1adfc5d9f2c1d31d024` |
| `complete_lower.py` | `0af6595c670e5140ab3505c1443a9e36d3e2f8e2a7696c3854f9d0c9831aa1d6` |
| `global_route_core.py` | `a986d8d147ebaecc7ca2599e7c942becbeb7c0d2eaaf4308874fa697aa5fcc8a` |
| `groom-source.py` | `d86665075b80352d5ff1ce659a1abbb4143d151aa8dbf4861861b8bdf3e0d78f` |
| `mathematical_controls.py` | `7c59b4d3c90687bb5c32a16b6e3c3d9d332b338311f208ff1cde273e0780aaca` |
| `prescreen_controls.py` | `ef1a42359358e6ae419598314e70c01a4b095c628b3ed6b06d1dba6a88d192a6` |

The final six entries in that table are byte-identical to attempt19. `adaptive_ball.py` is byte-identical to the independently reviewed one-cell diagnosis; `adaptive_controls.py` differs from that diagnosis's control source only in its standalone output filename. The diagnosis is reviewed separately in `../attempt19-diagnosis/independent-review.md`, SHA256 `55282040ecb405e3136cc88f268e0a2bde928038fcd9fbfcd762960770c65e0b`, with its actual receipt and numerical limits preserved.

Primary `outputs/character-round2-20261107/render_candidate20.py` has SHA256 `54dff60c56dfa6353401b7a0a2c89af22be00d8654641353bae627acf1f6d312`. Its diff from reviewed renderer19 is exactly three line substitutions: attempt source directory, output directory and temporary camera name. The shared render-state helper remains pinned in the producer to `cc63b9b80f4e819d8a96c87417a1576729b5dddd4e9a0a69b7dadf9846d60dbf`. The candidate10 input remains pinned to `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`.

## Fixed-cell certificate integration

`shared_field.py:147–156` restricts the adaptive call to records marked wholly fixed, supplies the unchanged construction target, 0.1 micrometre reserve, depth12 and node511 bounds, and requires an explicit pass with at least one leaf and body/clothing minimum bounds at or above the target. An ordinary uncertified or inside result is retained in the failure witness and raises; malformed helper/support failures propagate. It does not turn noncertification into a skip.

The fixed-clipped-vertex selection at lines277–300 remains unchanged in meaning. Variable cells with incompatible fixed vertices still fail. A wholly fixed cell may use the 3D certificate when its old horizontal certificate is unavailable or insufficient, or when the selected horizontal plane is not outward from the head axis. Existing valid horizontal certificates continue through the original path. No free guide or child receives this exemption. During final replay, lines394–403 check corner heights, reconstruct the clipped vertices, reject changed supposedly fixed geometry and rerun the full certificate against the same complete trees.

The underlying proof and its limits remain those of the separate diagnostic review: real convex-union subdivision, propagated coordinate-rounding allowances, actual float32 anchor displacement subtraction, complete body/clothing distance-minus-radius bounds, exterior-body sign check and bounded failure. Its real positive witness required one midpoint ball at depth0; recursive subdivision was exercised on synthetic planes. This source integration does not enlarge that prior runtime evidence.

## Reference-cell normal selection

`reference_corridor` at lines8–36 validates finite reference coordinates, nondegenerate obstacle input shape, head center and target; calls the existing separator; and validates a finite unit normal and consistent minimum gap for a separated result. Only the geometric cases of overlap, insufficient gap or a nonoutward plane return an explicit fallback reason. Unexpected kinds, malformed results or separator exceptions abort. The unchanged separator itself rejects a degenerate obstacle hull; the pure controls exercise that path.

The integration at lines277–309 uses original XY coordinates for variable corners together with the already intended final corner heights from `_point_expression`, then applies the unchanged clipping weights. It tries the new direction only when there are no fixed clipped vertices. The same complete obstacle slab with 6 mm Z padding supplies the hull. Selection requires all original clipped vertices to satisfy the same 5.001 mm target and the plane to lie outward from the head axis. Otherwise the original anatomical direction remains. This is a different sufficient-constraint direction motivated by the measured fallback-plane failure, not a reduced physical margin or altered guide objective.

Both selected and fallback directions enter the existing residual decomposition at lines324–332 and knot-split C2 Bezier inequalities at lines333–346. Every final clipped vertex and span is replayed after all independent QPs at lines394–413. Consequently an originally feasible POLY reference cell is not assumed to certify the new spline, all child offsets, or even the independent per-guide sufficient constraints without deformation. A source-valid plane choice can still lead to infeasible or unattractive fitted guides; the readiness verdict makes no prediction of success.

## Retained gates, evidence and ownership

The original and float32 prescreen, typed physical/noncertification dispatch, exact preservation of dual-pass guides, no-free-tail rejection, QP objective and equality conditions, preferred-field transport, guide turn/collapse limits and upper neighborhood checks are unchanged from19. Preserved guides still receive independent final checks; prescreen counters do not stand in for final counts. The complete render-evaluated support construction at `shared_field.py:71–122` retains every clothing face, restores temporary modifier settings and hashes both full support populations. This unchanged source is relevant to both new certificate choices: neither uses a narrower replacement body or clothing set.

The final distance verifier at lines456–508 still requires actual emitted lower segments, including band-boundary segments, to pass body and clothing rays, exterior-body checks and bounded continuous distance estimates. Guide margin remains 5 mm. Child margin remains 1.5 mm from the shaft surface, with the maximum emitted endpoint radius included for each segment. The source construction's radius allowance and the stored float32/radius recheck remain separate. Original lower-entry shape checks and independent upper coverage/intersection guards remain mandatory.

The probe still requires counts `[11425, 11425, 150]`, all 23,000 actual stored splines with 64 points each, the complete stored physical recheck, fringe/crown/temple coverage, zero face/ear intersections, root/local-lift limits and the independent complete lower-body/clothing checker. It first asserts candidate10/11 complete support equality. Its three added actual controls require the retained reference plane to preserve original feasibility, repeat the exact failed19 cell's adaptive positive on matching current supports, and reject a real clear-endpoint head-crossing hull through the strict fixed-cell caller. Existing historical failed-guide, enlarged stored-radius, lower-entry kink, fixed-cell positive and inside-body controls remain. These eight actual controls are required by source but have not run for20 as part of this readiness review.

Partial cell/span lists are now attached to the recorder before construction finishes, so completed branch decisions survive a later failure. Construction entries are not final replay passes: `replayed_ball`, `final_vertex_gaps_m` and final span-gap fields are added only after their respective checks succeed. Failure in the currently attempted fixed cell is separately retained in `failure_witness`. A consumer must distinguish those partial records from the successful final bank metrics. This is an evidence improvement, not an acceptance shortcut.

`probe.py:233–242` refuses to overwrite the provisional blend, computes the full actual hair render-state fingerprint after all geometry and independent checks, then saves `candidate20-provisional.blend` and binds its SHA256 and size. The status remains `geometry_pass_pending_appearance`. The source map includes the shared fingerprint helper, the variant snapshot dependency, all new helpers and the diagnosis receipt. The final input/candidate11/production/source immutability checks remain fatal, and a Python-path failure after save begins removes only this provisional output. As previously reviewed, an external hard termination may leave incomplete files, but it cannot produce the required passing receipt for renderer acceptance.

The owned launcher retains its 900-second wall deadline and `finally` Windows Job cleanup; its only change is the attempt purpose text. The renderer adaptation retains all prior saved-file, immutable-source, actual curve coordinates/radii/material state, nonhair scene and fixed benchmark checks, the fresh six-image/receipt guard and temporary-camera cleanup. Its existing supported static-scene/fingerprint limits are unchanged; this delta is not a claim of a new generic scene serialization or arbitrary compositor contract.

## Checks performed and limits

All 12 exact source hashes matched and all parsed successfully. I independently reran `mathematical_controls.run_controls`, `prescreen_controls.run_controls`, `adaptive_controls.run_controls` and `reference_controls.run_controls`; each passed without rewriting artifacts. The reference controls reproduce the retained 5.877665162 mm separator, test its nonmutating feasibility, and reject malformed/nonfinite/degenerate inputs and an unexpected separator exception. They distinguish the intended overlap, below-target and nonoutward fallback cases. The adaptive suite includes 3,015 partition cases, depth12 exact-rational coordinate coverage, genuine synthetic recursive certification and budget/inside/degenerate controls. Root separately reported the same four pure suites passing; that report is not substituted for the independent checks above.

Retained source-control receipt hashes are `d87afdc962f4da05b33b00530513679c4c8fa8ce1c05341242ef7eebbb7b3d37` (`adaptive-controls.json`), `2c410a9369eb8b6251d5781f2be00c0de92cb4bb88b9222228364b5c2ad34289` (`reference-controls.json`), `7bded22faddfee4d4f0b9cd1ea3e52e973b7c6c76180250bd4af5aa5b92e9965` (`mathematical-controls.json`) and `7931b8cd950578d01d3c0c3b7f12fa6cf89f480ca8d49a2f2df20c322875622b` (`prescreen-controls.json`). These are source/synthetic evidence, not attempt20 Blender receipts.

The fresh full attempt must still demonstrate all actual controls, guide fits, complete stored children, source/input immutability and process cleanup. Only a passing geometry receipt may proceed to the exact saved-scene renderer, followed by independent native-resolution judgment of all six fixed/held-out views. The 132 previously unsafe guides and complete groom remain unproven. Full naturalness and the user's appearance criteria remain open regardless of source readiness; using the last authorized attempt does not lower those criteria.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F33 | Wholly fixed cell needed a less conservative proof. | Bounded source correction passes its controls; 17 partial fixed-cell certificates are constructed in this run. | No complete bank replay or population pass. |
| F32 | Projected shared constraints can unnecessarily restrict safe fixed geometry. | Still open for mixed fixed/free cells: attempt 20 stops at cell 29/30, points 105-106. | Preserve exact evidence; no unsupported impossibility claim. |
| F21 | Complete actual guide/child proof remains open. | No QP, final replay, children or save. | Round 2 ends at ten attempts. |
| F12 | Hair naturalness remains unresolved. | No new render or appearance acceptance. | Further work requires new authorization. |

## Verification

Root independently reran all four pure suites. Actual run passes eight physical controls, complete candidate10/11 support equivalence, 192 dual prescreens and all four immutability checks. It rejects a mixed cell whose fixed projected gap is 2.279173 mm against 5.001 mm. Those fixed points are actually 38.197-38.273 mm from the body and 25.093-27.804 mm from clothing; one variable corner is 4.047650 mm from clothing and needs repair. The 87 partial cells include 17 adaptive fixed proofs, 68 fixed-normal and two feasible-reference selections; 31 spans await replay. These are construction records, not complete verification. PID 50620 exits 1 and closes after 20.006 seconds. Result SHA256 142cda6129b8140e4a77130287511fd02a823f1a48ae4e2dc3acae391a2d1598. Root read the actual failure; independent runtime addendum was unavailable due the reviewer model usage limit.

## Round outcome

Source readiness allowed the final bounded run, whose mixed-domain construction failed. Round 2 is closed at ten substantive attempts, with no face/hair repair accepted from these final experiments. The requested anatomy revision remains delivered. A later user Continue message authorizes a separately accounted round 3; it does not retroactively rescore this failure.

# Review 33: implementation

## Target

Continuous goal events on frozen candidate23 and the actual eleven-path diagnostic.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns every Blender execution.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 bbda0ebc3cd4f8cb2e758d73552a15cfb0a83b9fedb87441bd19284e4dd71dc7.

# Candidate21 short-goal failure and v4 source review

Final decision: diagnosis independently confirmed; no blocking source finding in the frozen v4 continuous-event repair. The root-owned corrected 11-path actual-geometry diagnostic has now passed and was independently inspected. The unchanged full builder/runner with the reviewed v4 core may proceed to the single full candidate23 experiment. This is bounded geometry evidence, not a full-population pass or appearance acceptance. Candidate21 failed closed at 526 completed strands and produced no saved candidate; its earlier review and raw failure remain preserved.

## Reviewed bytes

- Failed candidate21 `first-strand-failure.json`: SHA-256 `80ddffa24315ab1765c7fbe92e1d770a4a9173e6d2d9f50416ad011ecb594f87`.
- Original frozen `candidate21-source/surface_groom_core.py`: `44469cc3c1b727972e7241ee4b53f126e7f3a3de4b3ef485f7850f480ad8add6`.
- Fixed `surface-hair-v4/surface_groom_core.py`: `82a5cbe0be11d54f7f237222f8e8e8f4f8bf9444119564b347b575279c65324f`.
- `surface-hair-v4/check_goal_events.py`: `ac52cd3a425672afedacef97fcbc5fb0a4cd41c2d3b5f89859c62ff394092da1`.
- Final `surface-hair-v4/run_bounded_goal_events.py`: `539b03c9840e3630019013bb59fa1977a73721d8915349baf8d74f4422e6eb32`.
- `surface-hair-v4/goal-event-controls.json`: `ae936252c5123d09b1febda24bb81b3e4889849f62670905d8a36737fb421e48`.

All entries in the author's manifest-v4.json matched their files at report creation. Source remained read-only; this separate report is the only file written by this reviewer. No other reviewer report was read. No Blender, renderer, GPU process or subagent was launched.

## Independent witness calculation

The failed strand has 180 stored points, 179 segments and total travel 300.000009484205 mm. No stored vertex is within the requested 2 mm sphere; the closest vertex is 2.009982856549 mm away. For actual segment 99, direct double-precision projection onto the stored float32 chord gives endpoint distances 2.009982856549 and 2.049385850033 mm, a closest parameter t=0.48000693088744545, and an interior distance of 1.765889496458 mm. This is a real segment crossing with both endpoints outside, not a near-miss or a tolerance proposal.

The original core's current-point test at lines 133-135 can therefore miss short scalp arrival. Its continuous segment-ball logic at lines 214-224 was limited to an already released long strand. The raw error is the explicit travel-limit failure, not an acceptable terminal event. The stored segment99 certificate has a 0.003896384034305811 m complete-support starting distance and a 0.0018160419839638741 m conservative shaft clearance bound, above the 0.00001 m requirement. This supports the diagnosis that the already certified segment reached the goal and its event was missed. It does not replace a fresh BVH query.

Applying the fixed helper to those exact endpoints yields stored point (-0.02023274078965187, -0.1435643583536148, 1.5492650270462036), strictly 1.999572433820 mm from the unchanged goal. The archived start distance gives a fresh-length recomputed bound of 3.794115380465 mm for that shortened chord; the bounded Blender diagnostic must still requery actual support.

## Repair assessment

1. V4 `surface_groom_core.py:94-114` solves the continuous chord/sphere intersection, rejects tangency and boundary-only contact, and tests float32 candidate points strictly inside the original sphere with a positive numerical reserve. It never inflates the arrival sphere. The bounded interior fractions choose a representable interior point; the result should be described as an interior clip, not an exact earliest representable root. Extremely shallow intersections without a tested representable interior remain fail-closed rather than becoming false arrivals.

2. V4 lines 226-251 apply that event logic to the complete affected class: short scalp arrival, long scalp release and measured long terminal arrival. The release event continues the long path from the clipped stored point. A short or terminal event terminates only after adding its validated segment. Long release geometry can change, and the author explicitly acknowledges and tests that scope. Travel and step exhaustion still raise, and no failed strand is omitted.

3. V4 lines 235-244 recompute actual clipped length and maximum endpoint height-ramp demand, query complete supports afresh at both endpoints, reject either inside-body endpoint, reject a degenerate segment and re-establish the whole-segment shaft bound from the fresh starting distance. Float32 rounding away from the original mathematical chord therefore cannot inherit an unchecked certificate. The unchanged full builder later rechecks actual emitted radii and all stored segments as before. V4 also removes the old positive 0.2 micrometre long terminal tolerance and requires strict interior arrival there.

4. The new code changes no strand count, sampling specification, root tolerance, 2 mm short-goal radius, 5 mm guide clearance, 1.5 mm shaft clearance, 75-degree turn ceiling, source materials or render benchmark. Earlier full-builder findings and limitations in `full-groom21.md` remain applicable.

## Controls and remaining gate

The author control program was independently rerun in memory against the exact v4 core, with its output-writing tail omitted and Python bytecode writes disabled. The actual segment99 witness passed. All seven reported geometric controls passed: outside/outside chord entry; tangent miss; outside miss; boundary-only miss; 6 mm long scalp release sphere; world-height float32 entry; and the regression proving that naive storage of -0.002 becomes -0.0020000000949949026, outside the unchanged 2 mm ball.

The reviewer additionally ran 12 independent analytic-sphere `march` cases, using four scalp travel angles (0.37, 0.51, 0.65, 0.83 radians) and three azimuths (-0.74, 0.22, 1.31 radians). Every case reached `short_scalp_goal_arrival`, emitted only float32 coordinates, ended strictly inside 2 mm, retained nonnegative physical certificate slack, and marked its last segment with a fresh short-goal proof. Counts ranged from 40 to 72 points; final goal distances ranged from 1.998542833101 to 1.999784875132 mm. These are analytic controls, not new human-mesh evidence. AST parsing also passed for all three v4 Python files.

The reviewed root-owned diagnostic precommits the original failed strand, eight held-out short strands and two held-out long strands. It uses the unchanged actual specification and complete-support fingerprints, checks whole-path physical clearance and the retained head repair guard, and requires the original failed path's first 100 points to remain exact. The initial draft's exit-code gap was reported during review; final script SHA539b03c9840e3630019013bb59fa1977a73721d8915349baf8d74f4422e6eb32 now explicitly asserts exactly 11 rows and `bounded_pass`, as well as immutability. Parent should still inspect all rows and retained metrics, not merely exit status.

The 11-path diagnostic was not executed by this reviewer. Until its actual-geometry receipt passes, the fix has source and analytic support only. Even a passing bounded diagnostic cannot substitute for all 23,000 stored strands or six native rendered views. No full-groom or aesthetic acceptance is claimed.

## Actual diagnostic addendum and instrument defect disposition

The source-only assessment above was completed before the root supplied the actual diagnostic receipts. The first actual run, preserved at `goal-probe-v4/bounded-goal-events.json` SHA-256 `ffd8252d7b1ba974496201f2bb999d8a227201de675a7b134f08f5a75c1816b0`, reports ten held-out passes and one failure of the original-prefix assertion. This reviewer independently inspected that counterevidence rather than treating it as trajectory failure or silently discarding it.

Finding FG21-EVT1: the diagnostic runner compared the in-memory `list[tuple]` path to the JSON-derived `list[list]` prefix. The source-only review did not catch that container-type mismatch. The original row had already passed adaptive shape, fresh whole-path distance proof, both lower guide/shaft checks, the head repair guard, strict short-goal distance and scanline checks before this assertion. After both records are read from JSON, the first 100 coordinates compare exactly; independent maximum coordinate-distance difference is 0.0. Its actual shortened path has 101 points and terminates 1.999572433820 mm from the unchanged goal. The final actual segment is 0.021968653841 mm long, carries `goal_event=short_scalp_goal_arrival` and `fresh_goal_event_proof=true`, and has a 3.794115380465 mm fresh complete-support shaft bound against a 0.01 mm demand. The failure was an instrument defect, not a physical violation.

The root preserved the failed harness and created `goal-probe-v4b/run_bounded_goal_events.py`, SHA-256 `e1a56227ccf4aaafda6a7969663607d7168377712f91a80f094aff903d1d805a`. Independent diff inspection confirms its only code change is normalizing both prefix sequences to tuples before exact equality. The fixed core remains SHA-256 `82a5cbe0be11d54f7f237222f8e8e8f4f8bf9444119564b347b575279c65324f`; no trajectory construction or physical threshold changed.

The rerun receipt `goal-probe-v4b/bounded-goal-events.json`, SHA-256 `db866203f12d32f58e543e8498b0e0a343fa3066fa6c6f04b6b0cff59962aac1`, has exactly 11 rows, all `bounded_geometry_pass_pending_appearance`, overall `bounded_pass`, and true base/failure/source immutability. Every bound source hash was independently checked against disk. The original prefix flag is true; direct independent comparison of the first 100 coordinates to the archived candidate21 failure is exact. All 11 complete point sequences also match the first diagnostic's corresponding sequences exactly, confirming the rerun changed the instrument only. The two held-out long paths reach measured terminal balls, retain lower-turn maxima of 0.8165936814 and 14.8532040847 degrees, and have minimum lower-edge lengths 1.7833404965 and 0.6353671898 mm. All nine short paths reach their strict 2 mm arrival spheres and pass the maintained forehead scanline requirement. The root recorded internal elapsed time 5.1919032 seconds.

Disposition: FG21-EVT1 is fixed and independently checked. There is no remaining blocker from this review to using the unchanged candidate21 full builder/driver with the v4 core in the next root-owned full experiment. All 23,000 actual emitted strands, all original full-population/coverage/face/ear checks, save/binding guards and six-view appearance review are still required. The short-event repair and bounded diagnostic are not an integrated appearance attempt or an acceptance claim. The reviewer launched no Blender process; root owns and reported cleanup of both diagnostic processes.

## Frozen candidate23 integration binding

Independently rechecked `candidate23-source/`: core SHA-256 `82a5cbe0be11d54f7f237222f8e8e8f4f8bf9444119564b347b575279c65324f`, unchanged builder `87910f655b40530d47500f3ad473cf1b95dfaf699db33dd481e5a6a155f255ba`, and unchanged OUT-relative driver `5043f0b891e186b8c93dd8329108d2eb0ba25960dd31c50349408a2af2dae29b`. The frozen full-source control receipt binds those same hashes and contains all seven passing/expected-failure controls. AST parsing passed.

Renderer `render_candidate23.py` has SHA-256 `b56e739e5cb8467351e74c1782ec170989ab48ff628fc9e6d7eeef347276712d`. A byte-for-byte transformation check confirms its complete contents equal the previously reviewed candidate21 renderer with only literal replacements `candidate21` to `candidate23` and `candidate-21` to `candidate-23`. Its physical-receipt, saved-scene, full fingerprint, population, source and unchanged-benchmark checks are therefore preserved, with source/output paths routed to candidate23. No renderer logic change remains to review. The source/actual-diagnostic decision above applies to this exact frozen candidate23 integration; full geometry and appearance remain pending.


## Findings and disposition

Accepted the continuous-event correction and the tuple/list diagnostic repair. The subsequent full candidate23 failed a different ear-envelope requirement after5293 strands; no full population or appearance pass.

## Verification

Seven source controls, twelve independent analytic cases and eleven root-owned actual paths pass. Original failed path first100 coordinates are exact; root process47708 exits zero and closes after7.814seconds. Full23 process43512 exits1 and closes after82.957seconds.

## Round outcome

Candidate23 rejected before save/render. Its exact source and new ear failure remain retained; all earlier event failures and harness counterevidence are preserved.

# Review 37: implementation

## Target

Outer-ear route, retained valid terminals and actual bounded failure evidence.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns actual Blender execution and acceptance.

## Reports

### Independent Codex reviewer, Astra xhigh

Complete authored report, SHA256 94c0e20cb5f1e51fcba7276701baf9294595ee778df0e713ed1bddf84afa2d9b.

# Outer-ear route v1: independent bounded review snapshot

Decision: v1 is not ready for a full groom. The root-owned actual diagnostic has only 5 of 11 passing paths, and the reviewer independently reproduced a travel-budget bypass in the new terminal shortcut. No full candidate or appearance approval is given. This report freezes the v1 judgment and counterevidence; a later design requires its own exact-source and actual-diagnostic review.

## Exact reviewed evidence

The root-staged v1 under `outputs/character-round3-20261108/ear-route-probe/` binds:

- `surface_groom_core.py`: SHA-256 `a2f8dca5a1c9219d00a767f111e8f00bef421535fa724c9937b9b83c7728b5cf`.
- `outer_ear_support.py`: `3e08d3742b9f3eb27deec60c787b250f4f584fe4456eb7657dbe104de4b10d3b`.
- `run_bounded_ear_steering.py`: `4889792c6cbfb522bd0f723ee14af710d7b360b6cb9d1e944b6d5437c1791a0a`.
- Actual `bounded-ear-steering.json`: `573ee8c048fcc5aa638b47c9f55c71748b04250fe52c8c1767b1f72ba074fe2e`.
- Earlier actual `ear-root-probe/ear-envelope-result.json`: `9c665c76eda9e8b4319b9b56e2b57777b9d0a5fa4b00c08542474fd0596db1f3`.
- Candidate23 first failure used by those receipts: `75bca33bf43c3822b4b314e5c9dfe68e467fd047d4fa603cd4e2cddb9afdbaff`.

The reviewer read the source, old guard and retained actual receipts; reran the pure controls in memory without writing their output; and computed witness geometry directly from retained coordinates. Source was read only. This report was the only file written by this reviewer. No Blender, GPU job, browser or subagent was launched. Root owns the actual diagnostic and reported its process cleaned after exit 1.

## Diagnosis supported by raw evidence

The original v4 endpoint was a `first_feasible_surface_approach`, 135.697455629 mm from the requested terminal. Its original terminal had already been selected as physically valid, with 28.138022870 mm minimum complete-support distance. Moving that valid goal was not necessary to explain the failure. The raw replay reports no body/clothing segment crossings, while the worst measured radial guard deficit is 7.014461167 mm at a point only 1.244528568 mm from the actual Euclidean body surface. The reconstructed repair amplitude is 7.264461167 mm, exceeding the unchanged 6 mm guard. These measurements concern different geometric conditions; radial extension cannot be represented as Euclidean clearance.

The proposed support wrapper correctly keeps those roles separate at source level. `OuterEarQuery.__call__` delegates physical queries to the original body/clothing query. Complete canonical body geometry is independently reconstructed and hash-compared before selecting all body polygons overlapping the stated ear region. The convex hulls supply additional construction contacts only; they are not substituted for physical body support. The root probe still invokes the original entire-path physical verifier, 5 mm guide and 1.5 mm shaft checks, adaptive shape check and old radial repair guard. Removing first-approach success and requiring terminal-ball arrival is appropriate to the retained valid-goal counterevidence.

## Blocking findings and failures

EAR-1 — The new final-chord shortcut bypasses the travel budget. In reviewed v1 `surface_groom_core.py`, the `certified_terminal_chord_capture` branch precedes the travel-limit check and does not require its stored float32 segment to fit the remaining travel. Independently reproduced without Blender: query returns distance p.z to plane z=0, root=scalp_goal=(0,0,0.00658), tip=(0,0.0005,0.00548), long=True, length=0.0005, low=0, high=0.01. The function returns `measured_terminal_ball_arrival` with length 0.001208304601760543 m, exceeding the 0.0005 m budget by more than 2.4 times. Its physical bound passes; this is a completion-limit defect. Bound actual stored capture length by remaining travel and retain a negative control before full integration. Root was notified immediately. Any unreviewed v2 repair is outside this v1 decision.

EAR-2 — The root's actual v1 diagnostic fails 6 of 11 precommitted cases. Passing the original ear case cannot waive those failures. The rows are:

| Case | Actual v1 result |
|---|---|
| original ear failure | Pass; original terminal preserved; path length 0.247402744601 m; requested terminal distance 0.001999595994 m |
| original fringe regression | Fail: entered/exhausted construction envelope |
| left ear 0.42 | Pass |
| left ear 0.50 | Fail: travel limit before terminal event |
| left ear 0.58 | Fail: entered/exhausted construction envelope |
| right ear 0.42 | Pass |
| right ear 0.50 | Pass after invalid terminal projection |
| right ear 0.58 | Pass after invalid terminal projection |
| valid thin goal | Fail: unchanged 75-degree lower-turn guard |
| left rear invalid goal | Fail: entered/exhausted construction envelope |
| right rear invalid goal | Fail: outside projection anchor invalid |

The thin-goal path's last segment is the new certified terminal shortcut. Independent calculation from its last three stored points gives a 79.234224460-degree final joint. The unchanged 75-degree guard correctly rejects that geometry; this cannot be waived because its distance certificate passed. The left 0.50 path also remains an actual unreached-terminal failure rather than a successful first approach.

## Hull-sign counterevidence, with mechanism still open

The raw receipt does not store the failing closest hull points, normals or all hull planes, so the proposed nearest-face-normal misclassification mechanism has not been directly re-queried by this reviewer. It remains a hypothesis requiring actual evidence.

There is nevertheless stronger concrete counterevidence than the error text alone. Independently comparing each failed endpoint with BOTH recorded convex-hull AABBs proves the following minimum possible Euclidean distances to either hull:

- Original fringe endpoint (-0.018341651186347008, -0.11885809153318405, 1.6262447834014893): at least 49.472318916 mm from the nearer hull AABB.
- Left 0.58 endpoint (-0.1046348437666893, -0.022826358675956726, 1.3968640565872192): at least 84.883196056 mm from the nearer hull AABB.
- Left rear endpoint (-0.032512497156858444, 0.003032881999388337, 1.6300592422485352): at least 42.452298002 mm from the nearer hull AABB.

Each endpoint is outside both hull boxes and far beyond the 1.5803 mm construction centerline demand. If those boxes describe the queried hulls, genuine proximity/exhaustion cannot explain the reported construction failure. The immediately preceding certificates also have large positive construction reserves. This supports investigating signed-distance/orientation/query consistency, but does not establish that a particular all-face-plane or nearest-vector implementation is already correct. Freeze diagnostic counterevidence and verify any sign/normal repair against actual hull geometry before relying on it.

## Controls, integration requirements and limits

The seven author pure controls passed when independently rerun against the reviewed v1 core: simultaneous contacts, infeasible cone rejection, 24 four-contact systems compared with 2,000 independent directions each, preservation of a physically valid thin goal, projection only for invalid goals, a physically certified thin-goal capture, and rejection of an unreached long goal. Those controls did not cover EAR-1 or the actual 79-degree final turn and do not override the bounded failures. Python AST parsing passed for the four reviewed source files.

Eventual full integration must explicitly wire OuterEarQuery for construction; the existing full builder still initializes its original physical query. Retain a separate original physical query for actual-shaft verification, preserve the old postguard and face/ear checks, and bind the new helper plus changed builder/core in the saved source receipt. Retain construction-hull records without presenting them as body geometry. This is an integration observation, not approval of a yet-unwritten full builder.

Root is preparing a separate v2 and actual diagnostic. Review is released now; no need to keep this reviewer idle. Re-engagement should name frozen hashes, retained v1 counterevidence, the repair of EAR-1 and new actual probe receipts. All 23,000 stored paths, actual float32 radii, complete support, unchanged root/shape/coverage/face/ear guards, source/save/render bindings and native visual review remain required. No full build or aesthetic acceptance is authorized by this snapshot.

## Findings and disposition

Reject full-groom integration: only5/11 bounded paths pass. Preserve the travel-cap bypass, premature prior endpoint, unresolved construction geometry and79.23-degree terminal turn. Root subsequently proves both actual BMesh hulls nonconvex by about1.4mm; all normal formulations agree, and centered uniform normalization does not repair it. These subsequent facts are root measurements, separate from the frozen authored report.

## Verification

Exact source and retained evidence are under ignored outputs/character-round3-20261108. Reports are preserved verbatim above; root outcomes are recorded separately in the plan. No runtime source is accepted by this record.

## Round outcome

Continue within the existing ten-attempt round. Bounded unsaved diagnostics do not consume an integrated appearance attempt.

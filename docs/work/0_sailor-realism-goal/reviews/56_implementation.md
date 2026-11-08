# Review 56: implementation

## Target

Analytic terminal heading-cone and arrival-ball intersection, exact native thirteen-path replay.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns native execution, visual acceptance and delivery.

## Reports

Complete authored report, SHA-256 `f8f6fa581c242d80300514551eb6e54b6ad2c7583a0187d582154c1c5c6e9c75`.

# Independent terminal-cone v4 review — 2026-11-08

Source decision: no blocker for the root-owned bounded 13-case diagnostic. The exact change stays inside the agreed final-capture scope: only after the old center chord passes physical/exterior/construction/travel proof does it check shape, preserving valid center captures and proposing one analytic chord into the unchanged terminal ball for an otherwise shape-invalid capture. Every proposed point must pass fresh stored-geometry checks before acceptance. Full candidate30 remains separate and requires the actual bounded result and exact integration review. This reviewer launched no Blender/GPU process and mutated no source.

## Exact frozen source

Bundle `surface-terminal-cone-v4` has manifest SHA256 `864161d4794945f86181c517bf65f9ea2f51b7de2a78b997f52c7069ea6864b2`. All seven local and44 external source/input hashes independently match. Core SHA256 is `02747395c9b6b9807e03db4b97b3afaebd1caae1caff6bfd5c2f655ff3d15fff`; `run_bounded_terminal_cone.py` is `61ed66c938dc60ee03ec880620a573a9a2c44ed5cb20000006d1f2f882719ddb`. The unchanged construction helpers remain `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2` and `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2`.

I regenerated the unified core diff against actual candidate29 core `815ead7941b2951da64425f52d53fbd797d9d293bda274f99e290dd64a3c2fa3`; it exactly matches `core-diff.patch`. Only a new `terminal_capture_point` helper and the final-capture branch change. Terminal eligibility, all hard-reserve radius calculation, goal projection, ordinary integration/contact steering, continuous event clipping, failure metadata and limits remain otherwise unchanged.

The raw candidate29 failure is bound as `19d47cad4393d40c3e65ca9ec690a5346bd271df824e408792b3a98bd380a07b`, and prior native12 evidence as `c56fcfc57590514e063f4ba11f559c1c5fc117909e54f15be0fdefe33e8ac0c5`. The independent diagnosis is retained in `review/hair29-failure-diagnosis.md`: one 80.15578614112698-degree center-capture corner at point202, all earlier turns below8.836 degrees, valid original terminal center and unchanged0.2537549370765692 mm ball. No invalid-goal projection is justified for that failure.

## Geometry and acceptance reasoning

The branch first evaluates the original center chord with the same fresh physical/exterior queries, conservative physical/construction bounds and total travel limit as candidate29. Failed earlier center attempts do not enter the new proposal helper. This condition is crucial: proposing a shorter ball chord at earlier points would alter the previously reviewed trajectory. There is still a2 mm center-distance trigger; no enlarged capture range is introduced.

The helper uses the actual incoming stored segment and float32 terminal center. If the existing center direction is below75 degrees, it returns that exact center and original event kind. Otherwise, for a point outside the ball, it calculates the ball's angular radius `asin(R/d)` and the nearest admissible ray angle relative to the incoming direction. A nonempty intersection with the open75-degree cone supplies the midpoint between that nearest tangent angle and the upper permitted angle. The ray's closest-approach point is rounded to float32, then the existing continuous `segment_ball_entry` selects a strict interior float32 endpoint. The helper measures that actual rounded chord again and declines it unless its turn is strictly below75 degrees and its endpoint lies strictly inside the unchanged sphere. This is an analytic choice within a feasible interval, not a fitted angle or a radius change.

Non-finite input coordinates/radius/heading, nonpositive radius, float32 overflow, vanishing directions, disjoint or tangent-only cone/ball intersections, and exact/near antiparallel cases are declined. The helper does not certify physical support and is not treated as doing so. A declined proposal leaves ordinary bounded march/failure behavior in control.

For a cone proposal the caller freshly queries complete support at both start and proposed endpoint and obtains fresh construction fields at the start. It requires exterior endpoints, positive nondegenerate actual step, unchanged total travel budget, available point budget, actual stored turn below75 degrees, strict unchanged-ball arrival, the whole-segment conservative physical bound against maximum endpoint required margin, and all construction bounds. Only then are one point and its matching certificate appended. The certificate records the new event kind and measured turn. Valid center captures reuse their existing fresh query results and geometry. No 900-step, 0.5/0.3 m travel, body/root, clearance or final adaptive-shape guard is weakened.

As before, runtime physical/construction fields come from the fixed finite native geometry adapters. The new helper explicitly rejects non-finite geometric proposal inputs; this is not a claim to replace adapter validation for arbitrary malformed query implementations. Independent final emitted-path checks remain mandatory.

## Pure verification

I reran the authored controls in memory with bytecode and receipt writes disabled: all seven cone-control groups pass, including the exact failed native witness; valid center preservation; ten non-finite/degenerate/disjoint negatives; tangent-only boundary rejection; execution of the actual capture-branch AST; seven physical/construction/exterior/angle/sphere/point/travel negatives; and all prior native valid center captures remaining exact. The AST positive case appends exactly one matching point/certificate and makes four physical queries for the new proposal branch. Its rejected cases append neither a point nor certificate. The inherited ten terminal-plan controls and five capture-budget cases also pass their expected outcomes.

I additionally exercised320 independent scale/angle/radius combinations at both zero height and actual character-scale height: four distances from0.01 to2 mm, ten center bearings including75-degree and antiparallel neighborhoods, and four sphere-to-distance ratios. There were160 returned endpoints and160 declines. Every returned endpoint was exact float32, had actual turn strictly below75 degrees and lay strictly inside its unchanged sphere. This checks safety of accepted outputs, not universal convergence for all feasible inputs.

For exact failed6524, the new helper proposes `[-0.05636036768555641,-0.036391232162714005,1.3965879678726196]`. Its actual turn is73.77666318604157 degrees, chord length1.7678738025422767 mm, and distance to the unchanged center0.2536751999467807 mm, inside the unchanged0.2537549370765692 mm radius. Using the recorded fresh start query, conservative body bound is5.153926545930318 mm, construction reserve86.01397487326362 mm, and replacement total travel0.2669187396487454 m. These are pure stored-data measurements; fresh native endpoint, whole-path and brow/head results must come from root's actual diagnostic.

## Bounded runner and outstanding result

The runner binds accepted27 input `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`, complete body/clothing geometry, both construction envelopes, exact failed6524 specification, prior failures and actual native12 receipt. It constructs the same first12 cases plus failed6524. For each prior case it asserts every path point equals the previous actual native path. For failed6524 it asserts all203 pre-capture points exactly equal the failed path prefix, with exactly the final event replaced by `certified_terminal_ball_cone_capture`. The original valid terminal goal must remain selected.

All inherited checks still run: exact anatomical body root attachment, actual adaptive shape, complete-path physical proof at conservative0.08 mm radius, lower5 mm guide/1.5 mm shaft validation, unchanged head/radial postguard and complete evaluated-brow shaft proof. Missing/failed rows cannot become a partial pass: the final status and assertion require all13 rows, plus source/input immutability. The prior-point assertions protect this narrow repair from silently changing previously valid routes. There is no full population, scene save or renderer in this runner.

At this source-review checkpoint native13 execution and its result have not been independently inspected. Root must supply that receipt before a positive actual-path decision. The final integrated attempt30 remains reserved; no fullbuild or appearance acceptance is implied by pure/source success.

## Actual native13 result, inspected after source review

The root-owned run subsequently completed `bounded_pass`; root reports PID5396 exited zero and was closed after13.2364 seconds. `terminal-cone-v4-root-probe/bounded-terminal-cone.json` SHA256 is `61a2650d4c608fe947d4a1cf98093153ab7b6b2d64403df152c5909302006f6e`, with internal elapsed8.5333502 seconds. All52 recorded source/input hashes independently match. Root-staged core, runner and both helpers are byte-identical to the frozen files reviewed above. Input/failure/source flags and the object-name inventory check are true; that inventory is not itself a geometry fingerprint. This reviewer ran no native process.

I directly compared all12 prior names, specifications and complete point arrays with the previous native12 receipt: every one is exactly equal. The failed6524 case preserves exactly203 preceding points and its complete terminal plan, including original goal and0.2537549370765692 mm radius. Only the last point is replaced, exactly as predicted by the source-only witness. The result remains204 points/203 segments with total length0.2669187396487454 m and final angle73.77666318604157 degrees. Its final event is `certified_terminal_ball_cone_capture`, endpoint distance0.2536751999467807 mm, fresh body bound5.153926545930318 mm and construction reserve86.01397487326362 mm. Whole-path physical margin is0.020295410033728123 mm; root distance is0.11971162894042209 mm. All native shape, lower guide/shaft, head/radial and brow guards pass.

Across all13 rows I independently recomputed total lengths, strict final sphere arrival and actual float32 coordinate representability; all point counts and travel budgets remain within their limits. Maximum root distance is0.11993543012067676 mm; maximum lower turn is the repaired73.77666318604157-degree corner; maximum path length remains0.3488376809306132 m. The brow receipt accounts for all13 paths and2,550/2,550 segments, all separated by the expanded AABB proof against unchanged accepted27 evaluated brows (`4c857cd5efda96be78410718f85c7a406f485a860597a7cfc1601eff956d0a4b`,1,642 vertices/3,072 triangles). This sample does not exercise its recursive capsule branch.

Updated decision: source and actual bounded13 review pass without a remaining blocker in this scope. These direct comparisons confirm the agreed narrow repair and retained limits. Candidate30's complete integration bundle still needs exact-source binding review, and only a complete 23,000-strand build, final emitted-radius/population checks, save/reopen and native visual inspection can establish further acceptance.


## Findings and disposition

Accept the bounded correction with all original twelve paths and the failed thirteenth prefix exact. Actual stored endpoint, turn, body/ear/head/brow and budget checks pass; this is not whole-groom visual acceptance.

## Verification

Exact source, pure controls and native thirteen-path receipt remain under `outputs/character-round3-20261108`. The frozen full bundle is `candidate30-source`; every attempt is counted before dispatch.

## Round outcome

Ten of ten integrated attempts used. Candidate 30 is running; zero further full attempts remain authorized.

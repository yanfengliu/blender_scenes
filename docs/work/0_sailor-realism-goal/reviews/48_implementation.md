# Review 48: implementation

## Target

Distance-limited terminal approach, anatomical body-root guard and eleven native bounded paths.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns execution, integration and visual acceptance.

## Reports

Complete authored report, SHA-256 `0dd623173b1a763aec597fe97bdff9f66dddadb1481c1bb22e628e31a0a72763`.

# Terminal integration resolution: independent bounded source review

Decision: the frozen core change and pure controls support the next root-owned eleven-path diagnostic. No construction blocker was found in that change. One new diagnostic-root measurement issue (ROOT-1 below) must be corrected or independently measured before claiming that its anatomical attachment guard passed. This report does not approve a full candidate, complete population or appearance. Actual route evidence remains pending.

## Exact reviewed bytes

All entries in `surface-ear-halfspace-terminal-v2/manifest.json` matched disk during review:

- `surface_groom_core.py`: SHA-256 `91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78`.
- `run_bounded_ear_steering.py`: `c92c6314a821ab5a26800389a73fd0013d791c9311b7db91e2d701068dda3086`.
- Unchanged `outer_ear_support.py`: `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2`.
- Unchanged `support_envelope.py`: `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2`.
- `check_terminal_sampling.py`: `2b65ba6f27d3096fd1e2a672978607a609fd5c6275e1dbf78e630cde8a5fa393`.
- `check_capture_budget.py`: `c84bd909ddc0af657d49978dc2cfdc5f104d2396dd498eaa5fb95cd02dfdf375`.
- Prior actual native receipt `ear-halfspace-root-probe/bounded-ear-steering.json`: `ff8befdea7b55dc2de7aff31371ad9e331d18752095536283c67a460b7698aeb`.

The reviewer inspected exact diffs, source and raw prior receipts, reran both pure-control programs in memory with their output-writing tails removed, disabled bytecode output and parsed all Python sources. Source remained read-only; this report was the only file written. No Blender/GPU process, renderer, browser, subagent or dependency installation was launched. All prior reports and failure evidence remain intact.

## Counterevidence and mechanism

The prior actual halfspace probe has ten passing rows and one failure, `heldout_ear_-1_0.5`, which reaches its 0.5 m travel limit before terminal arrival. Its records show clear actual support and large construction reserves around the initial turn-away; the relevant contact heading corrections are effectively zero. Starting from actual point 181 and its incoming direction, the pure free-flight recurrence reproduces native points 182 through 186 bit-for-bit. Those early segments do not intersect the 2 mm terminal sphere. This establishes that the observed initial turn-away is explained by the existing discrete heading/integration recurrence, without invoking an unsupported collision hypothesis.

The pure legacy recurrence does eventually arrive in empty space, after 98.398821948 mm and 50 segments. It would be inaccurate to claim permanent free-space divergence. The new recurrence reaches the same unchanged sphere after 3.828299982 mm in 17 segments, ending at 1.999882579 mm goal distance with maximum local turn 2.025117439 degrees. This is evidence for the recorded state, not a global convergence proof or a replacement for actual mesh queries.

The prior thin-goal 79.234-degree failure has not been waived: the intervening actual halfspace receipt now reports the same thin-goal case passing with a 64.372159464-degree maximum lower turn. That improvement is actual retained evidence, not a result invented for this source change. The new eleven-case probe must still retain the unchanged 75-degree guard and reject any regression.

## Exact change assessment

The new `march_step_limit` retains the minimum of nominal 2 mm step, 0.65 times physical/construction allowance and remaining travel, while adding 0.1 times current terminal-goal distance only after release. Attached scalp growth keeps its original nominal resolution. At goal distances of at least 20 mm, the original 2 mm cap remains the tighter nominal bound. The existing 0.85/0.15 heading blend, 0.7 goal/0.3 gravity, chosen goal, terminal sphere, physical margins, construction envelopes and travel allowance are unchanged.

For a step no longer than 0.1 times the distance to a fixed goal, elementary geometry bounds its one-step change in goal bearing by arcsin(0.1), approximately 5.74 degrees. This is a useful local integration-resolution bound, not a convergence guarantee; the source correctly retains an exactly opposite-heading failure control.

The existing bounded float32 retry loop now rejects a stored ordinary step that exceeds either remaining travel or, when released, the goal-distance cap. It halves and retries rather than allowing rounding to overrun those bounds. Continuous goal-event clips are freshly rechecked against both limits as well as the original complete-support physical proof. The separate certified <=2 mm terminal-chord capture remains unchanged and retains its actual float32 travel-budget guard; it is an explicitly separate event path, not an ordinary released step. Postconstruction shape, actual-radius, radial, coverage and face/ear checks are not weakened.

The dependency fix is sound: the runner adds `hair_groom.py` to source hashes, asserts its established candidate10 SHA-256 `b8e20fc59389e6f2095c1cd24f22addb4e6f64a8a3d7d5e9f0a8f89b19e320e5`, and checks the resolved imported module path. The two construction helpers are byte-identical to the previously reviewed halfspace version.

## ROOT-1: added anatomical-root guard measures the wrong minimum

The runner's new `root_check=physical_query(path[0])` is followed by an attachment test using `root_check[0]`. The imported `actual_query` returns the minimum of complete body and clothing distances in that field. Consequently, a hypothetical exterior root 20 mm from the body but 0.1 mm from clothing satisfies this new test despite being detached from the anatomy. The code must select the complete-body entry from the query's support list, or independently query the actual anatomical head/body BVH, when recording and asserting the 0.3 mm anatomical attachment distance. The exterior flag is already body-specific and should remain required.

This is a diagnostic guard-class finding, not an allegation that any of the unchanged precommitted roots moved or that the full builder's original head-root check is broken. Root was notified immediately. It does not prevent a read-only bounded run whose root distances are independently inspected, but its current pass field alone cannot certify anatomical attachment. A corrected runner hash or explicit actual body-only measurements must accompany later acceptance of that bounded evidence.

## Independently rerun controls

Both control programs passed when rerun against the exact frozen core. The terminal-sampling controls reproduce the native prefix exactly, verify the 17-step improvement above, retain far-goal/scalp/physical-allowance/travel-remainder behavior, and reject both the 2 mm remaining-budget and exactly opposite-heading cases. They make no actual-support or global-convergence claim.

All five capture-budget controls passed: the preserved original overrun is reproduced; the new 0.5 mm budget is rejected with a 0.499920572443 mm stored prefix; exact rounded-chord budget equality is accepted; a one-ULP-smaller budget cannot authorize that capture and fails with a prefix below its budget; ample budget retains the same physical direct capture. The expected stored chord is 1.208304601761 mm. Python AST parsing passed for every Python file in the frozen folder.

## Next evidence and limits

The next actual diagnostic must retain all eleven cases and all inherited physical/shape/radial checks, bind the imported dependencies and report body-only root measurements. A failure remains a failure; there is no permission to discard a strand, relax a margin, replace a valid goal or accept a travel-limit event. The new core may still fail on untested states or exceed its bounded step count.

Existing invalid-goal projections of approximately 15/51/109 mm remain separate appearance concerns. This local integration change does not justify those projections or imply that the full groom will look natural. Only after the actual diagnostic passes should the full-builder wiring be reviewed; complete 23,000-strand geometry, actual emitted radii, all coverage/face/ear guards, immutable scene/source/render bindings and native visual review remain mandatory. No full candidate is approved here.

## ROOT-1 corrected-runner disposition

Root preserved the original runner and staged `ear-terminal-root-probe/run_bounded_ear_steering.py`, SHA-256 `8287e7d3ca012d15a7bf619550152f395d7c59bff3523df19e3be18bddbee471`. Independent diff inspection confirms its only change selects support records whose owner is exactly `body`, requires exactly one, records that body-only distance, and applies the exterior and inclusive 0..0.3 mm checks to it. Missing or ambiguous body support now raises. The core and both construction helpers are byte-identical to the reviewed terminal-v2 sources.

The reviewer extracted and executed the exact five AST statements of this staged guard without importing Blender or rewriting source. Eight independent cases passed their expected outcomes: valid body accepted; near clothing with detached body rejected; interior rejected; NaN body distance rejected; positive infinity rejected; missing body rejected; duplicate body rejected; exact 0.3 mm boundary accepted. For accepted cases the recorded value was confirmed to be body distance even when clothing was nearer. Root's four-case `root-guard-controls.json` binds the same corrected runner hash.

Disposition: ROOT-1 is fixed and independently checked for this staged runner. The earlier finding remains retained above as history, but no longer blocks claiming the corrected guard's measured result. Source approval for the eleven-path actual diagnostic now applies to runner SHA8287e7d3ca012d15a7bf619550152f395d7c59bff3523df19e3be18bddbee471 with core SHA91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78 and unchanged helpers. Actual route completion remains pending, and this disposition gives no full-groom or appearance approval. No Blender/GPU process was launched by the reviewer.


## Findings and disposition

Root accepts the bounded source for full candidate preparation and exact review. No complete-groom or visual acceptance is claimed.

## Verification

Exact reports, source and native receipts are retained under `outputs/character-round3-20261108`.

## Round outcome

Seven integrated attempts used, three remain, next 28. Candidate 27 is accepted for the local brow scope.

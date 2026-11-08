# Review 11: integration

## Target

Final authorized candidate 10, based on `2e95c6b0a1655ca2e6c4f067348bcdbbdaa231c1`. Exact source is retained under primary-checkout `outputs/sailor_character_realism_goal/candidate-10/source/`. Its 30-file `source-manifest.json` has SHA-256 `07193511b7ee577e619839c013dd94bbb48b185cb365e81ae310e4f067264609`; I recomputed all 30 hashes and matched the manifest. This review applies to those frozen bytes and the artifacts below, not subsequent worktree changes.

| Key candidate 10 source | SHA-256 |
|---|---|
| `scenes/sailor_character_realistic.py` | `809c9a0d92520901dd03a37ad3ab659020dbbe7d41fd851d11e93e7bc1ef010c` |
| `scenes/lower_cheek.py` | `dd856fc8eb4c6e3e62b948bc965a40f1430160af3f220fe43ecaea98fa7e32e0` |
| `scenes/perioral_shape.py` | `a5596d068bf7ce5d3c80caf5a549060b124e21c9f2c96f341eac99e8668db926` |
| `scenes/natural_hair.py` | `9aa0e2e0c67cb0b619b61fd531de8674818b668b02e0360af960082ad72f4af8` |
| `scenes/hair_groom.py` | `b8e20fc59389e6f2095c1cd24f22addb4e6f64a8a3d7d5e9f0a8f89b19e320e5` |
| `tools/check_lower_cheek.py` | `4f1aa3b470ed9c3ca7ebb55cd84d99d2442385c554c81058ab2e7770095dfff1` |
| `tools/check_lip_contour.py` | `a162bee7b897dfe2c375b46ae93432f01ee4d0942b3511a58f9e65ec3326b1f5` |
| `tools/check_realistic_character.py` | `0aa9f7294a034dcad295164b547fcb999c24e5ce371dd4b4572a667c0a2c9133` |
| `tools/verify_reference_smile.py` | `235cf8e41c676394abe80c5bd6c157ca44962ae398766708395a4b3b48cc5df4` |

| Candidate 10 artifact | SHA-256 |
|---|---|
| `hero.png` | `1c1895fadb01bf4af7578b6f77d0f68dbb867656810a2a18d14ae13930fa9503` |
| `portrait.png` | `8a312efd5f083cf04d3daddd9c18f893584b58faac8bdb8c13029ee6dfe65a09` |
| `profile.png` | `4c33b1807012a4284bcaea04863f3f77c6a4a0967bf457fa1a5b75939aa46046` |
| `back.png` | `98dd22cc70a791aaabfae1eeeda29f5f550d5b52b96d543c73440fec150e7d49` |
| `face_oblique.png` | `48d051b2c71898d58a1e11249bba83de0bb1565468f6dd95113991c7fa9a4a9b` |
| `torso_random.png` | `722a04eb44240abf56978e920dc21db4257f1a7ac0d51818148bea7f5da883b1` |
| `sailor_character.blend` | `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41` |

Comparison targets remain the frozen adult-20 reference images identified and hashed in round 8, candidate 6 as the original appearance negative, and candidates 8–9 as the immediately preceding reviewed renders. The fixed benchmark and disqualifiers in this unit's `design.md` were retained. Root owns final commit binding, gates, status and delivery.

Supplemental verification-only target: `tools/check_character_finish.py`, SHA-256 `62a7aeabcd5c42fc920df94b933e2128f03fea3277d6c6273c831a345a4a726e`, retained separately under candidate 10's `verification-source/`. It is not one of the 30 frozen render inputs and does not change the reviewed scene or pixels. The supplemental review below applies to these exact initial checker bytes; any repair needs its own exact binding and verification before closure.

Supplemental repair target, reviewed before this round closed: `verification-source/check_character_finish-v3.py`, SHA-256 `2fb43449929926946fe9ed07adab66feed428b5dec15470803c4189259773fef`, matching the repaired worktree tool. The original checker and its positive receipt remain retained as `verification-source/check_character_finish.py` and `saved-verification-v2.json`; the latter's SHA-256 is `0373338623472580e6b3b5052d51b379f6b2a713304a559646c29243be71b463`. Both checker targets remain separate from the 30 render sources.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the frozen changes against candidate 9, the complete new cheek implementation and regression, lip-test integration, revised pin/count, hair guide and temple-coverage changes, and the exact-source receipts described below. I inspected all six candidate 10 images through `view_image` at original detail: hero, portrait, profile, back, opposite oblique and seeded torso. I hashed those images and the saved blend. I did not launch Blender, render, run tests, change source or inspect a live saved scene. This round contains the actual final visual judgment, not an inference from geometry checks.

## Reports

### Independent Codex reviewer

Candidate 10 is not accepted as completion of the user's appearance request. There is meaningful bounded progress: the upper body is narrower, candidate 9's long exposed scalp wedge is closed, and its sharp side-flow ridge is substantially smoother. The remaining hair silhouette is broad and helmet-like, and the face still does not achieve the requested soft natural appeal. This rejection applies to the bounded naturalness brief itself. Full photographic realism is also not established. Exhausting the ten attempts does not change that judgment.

| User objection | Observed candidate 10 result | Reviewer disposition |
|---|---|---|
| Upper body too wide | Hero and seeded torso retain the visibly narrowed shoulder/upper-torso direction, fuller bust and slim waist. The candidate 7 collar step does not recur. | Materially addressed within this static silhouette scope. |
| Hair looks sparse or balding | Forehead and central crown coverage are full; the opposite oblique closes candidate 9's conspicuous straight scalp wedge. Profile flow is smoother. However, the front and oblique show pronounced rounded temple volume, a dense fringe, long stiff side curtains and a helmet-like overall mass. | Specific sparse-gap defects repaired; natural hair appearance remains unaccepted. |
| Face lacks the requested appeal/naturalness | The cheek inset is subtle and preserves the adult chin/skull. The face remains smooth and mannequin-like, with prominent pale mouth contours and limited convincing cheek/eye/lip integration against the reference. | Not achieved. |

The canonical portrait is decisive for the remaining hair silhouette: the temples bow outward substantially before tapering into the long vertical side locks. The oblique confirms continuous coverage but also shows that broad rounded mass. The profile no longer has candidate 9's abrupt common ear-height band; the continuous fall is an improvement. Fine strand detail and a closed gap do not make the global shape natural. The back and lower ends remain comparatively uniform. This falls within the fixed dense-helmet disqualifier, so the improved coverage cannot close F12 as a whole.

The face is slightly narrower through the lower cheeks, but this does not transform its overall reading. The change preserves the adult character and avoids compensating with larger eyes or a shortened skull. Those are appropriate constraints. Nevertheless, the native portrait and oblique still show the smooth, artificial form/surface relationship previously identified in F13. I do not equate a five-millimetre source section reduction with visual appeal, and I do not claim the user's subjective preference has been satisfied on their behalf.

The new `lower_cheek.py` mechanism is bounded and intelligible. It validates the finite 19,158-row adult topology and inspected stature range, maps native points to scene metres, and applies only a lateral inset capped at 2.5 mm. The field excludes the central 27 mm half-width and fades above 1.535 m; the depth gate restricts it to forward lower-cheek tissue. It checks that the raw field is zero on all complete oral and ocular anchor rows before protection, excludes helpers, and preserves Y/Z. This is a targeted local field rather than blanket removal of the existing widening or a change to adult skull scale. I found no blocking code defect in the exact implementation.

`check_lower_cheek.py` reconstructs actual production input and independently rebuilds a no-op control by replacing the invoked cheek function. It measures real source-edge sections, requires the central chin section unchanged and a bounded width response at the two cheek heights, rejects the no-op, and checks affected fan area/orientation and edge displacement gradients. It then runs the existing perioral and reference-smile chain on both inputs and requires all 76 oral XYZ rows to remain identical. The companion lip regression now includes the actual cheek stage in its production AST and preserves the former-contour negative control. These checks substantiate the source invariants; their documentation correctly excludes aesthetic acceptance and evaluated appearance.

The cheek change alters the smile support population from 514 to 516 rows. The binder and live verifier require that exact revised count, and the main and canonical checker both pin `52d36d7c9db5b4750807bb97dec4c0270f7cc4b3aa2296407b36c00194a9ab2e`. I read the receipt for independent neutral/proposed construction across all 516 rows. The count is explicitly revised rather than made arbitrary, and the live 50 micrometre mouth-aperture bounds are unchanged. Whole-chain oral equality and a changed surrounding smile-support population are compatible: the complete oral rails stay fixed while nearby cheek support changes.

The hair changes address a real source mechanism behind the oblique wedge. Removing the clamp that collapsed the blended fringe-to-temple sector onto the last short guide preserves those guide intervals. The free fall now uses one tangent-matched cubic instead of common brow/ear stations. Guide clearance uses a broad local radial lift rather than carrying an ear-driven offset across the entire crown. Tip feathering and the new transition coverage instrument add useful controls. These mechanisms are coherent, but the local lift and resulting broad temple mass still need to be judged in the pixels. The worker's own warning that smaller side volume was unproved was warranted by the final portrait.

`temple_coverage` measures actual POLY strand intervals outside the anatomical scalp at three heights per side. It checks identity world transforms, unmodified 3D curves and opaque material assumptions, and limits the largest angular gap to 0.02 radians. The known candidate 9 negative fails this instrument, while the revised groom passes. The source makes the boundary explicit: six angular slices do not measure rendered projected gaps, the global silhouette or naturalness. The original frontal fringe and central crown checks remain unchanged. The saved centerline intersection checks also omit physical strand radius; neither type of numeric pass can override the final appearance rejection.

F15 is fixed by the explicit `counts_scope` field in `apply_perioral_shape`. Top-level counts are now identified as the upper-lip/width stage, the nested lower report describes its stage, and the maintained lip verifier owns combined geometry statistics. F14's final-stage ordering guard remains fixed. The final upper-frame implementation is byte-identical to candidate 9, and no unrelated broader architecture change was introduced in this source review.

The supplemental saved-finish CLI follows the right positive verification path: it calls the canonical live checker, reconstructs the complete anatomical body from saved coordinates for garment clearance, runs the real saved-body penetration control with restoration, evaluates the nine accessories against the same complete surface, and measures actual saved strand intervals. The unchanged `scenes/body_proportions.py:149` context manager removes its temporary unculled object and mesh in `finally`; `tools/check_garment_isolation.py:278` restores every modified source coordinate after the intrusion control. The new CLI hashes the blend before and after and never saves. These mechanisms avoid substituting an unposed or visible-only body for the hidden torso.

I found two bounded fail-closed gaps in the initial reusable checker. F16: `check_character_finish.py:32` loads the canonical asset directly, bypassing the `BASE_SHA` check in `check_garment_isolation.py:327`. The called `clearance` checks population, manifoldness and the visible-face subset, but those checks do not establish the exact hidden canonical topology. Reuse the existing base digest guard before loading, and use `targets=()` because only canonical topology/groups are required. F17: the ornament loop at `check_character_finish.py:43` selects a name prefix and only requires nine results. It does not require the exact accepted nine identities or nonempty evaluated triangles. The unchanged `measure` at `check_garment_isolation.py:216` starts its minimum at infinity, so no-sample input is not explicitly rejected. Require the exact identities and nonempty evaluated geometry before measuring, with a real empty-ornament negative. The existing canonical checker does not supply those ornament guards. These findings affect the reusable rejection contract; the observed candidate 10 receipt contains nine nonempty, measured ornaments and does not show either defect in the delivered scene.

## Findings and disposition

The table records this reviewer's final observed dispositions for candidate 10. Root owns delivery status and may append gate/commit evidence without rewriting the authored judgment. No additional integrated repair attempt is requested or implied.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F11 | Candidate 7 collar/stripe shoulder steps. | Specific visible regression remains repaired in all six candidate 10 views. | Retain final evaluated support evidence separately from visual judgment. |
| F12 | Hair coverage and shape fail natural appearance. | Long oblique scalp wedge and sharp side ridge are repaired; broad helmet-like temple/fringe mass and stiff side curtains remain. | Unresolved appearance limitation at the ten-attempt stop. |
| F13 | Face does not achieve the requested soft natural adult appeal. | Cheek geometry is bounded and subtly narrower; native appearance remains insufficient. | Unresolved appearance limitation at the ten-attempt stop. |
| F14 | Production AST final-stage ordering relation missing. | Earlier fix remains present. | Closed for this source target. |
| F15 | Perioral top-level diagnostics appear to describe combined geometry. | Explicit `counts_scope` now distinguishes stages and points to the combined verifier. | Closed for this source target. |
| F16 | Supplemental finish verifier bypasses the pinned canonical base asset guard. | Reported against initial checker `62a7aeab...`; exact hidden topology is not established by counts/manifoldness alone. | Reuse the existing digest guard before reconstruction and bind repaired checker bytes. |
| F17 | Supplemental ornament checks permit an unverified nine-object population and do not explicitly reject empty sampled geometry. | Reported against initial checker `62a7aeab...`; actual candidate 10's nine positive meshes are nonempty. | Require exact names and nonempty evaluation, and verify an empty-ornament negative. |

Supplemental repair disposition, preserving the original findings above: root repaired F16/F17 in `2fb43449...`, and I independently read those exact bytes. The existing pinned base digest is now asserted before `load_body(targets=())`. The candidate's exact nine ornament names are required, and one shared `checked_ornament` path requires nonempty evaluated vertices and triangles before measurement. A real empty Blender mesh uses that same path, must fail for the explicit no-surface reason, and is removed with its data in `finally`. Strict finite JSON serialization also prevents an infinite no-sample minimum from becoming a valid receipt. I accept these code repairs; the original positive result and findings are retained rather than rewritten. The runtime receipt for this exact repair is recorded below.

## Verification

I recomputed all 30 frozen source hashes, inspected all six native renders and hashed them and the saved blend. I read source and evidence only; no test or Blender run is attributed to this reviewer. The first candidate 10 pure-test receipts named an earlier main hash, so I did not treat them as exact final-source evidence. Root reran the two checks; I then read `outputs/character-naturalness-20261107/final-lower-cheek.json` and `final-lip-contour.json`, whose main and relevant source/test hashes match this frozen target.

The final lower-cheek receipt reports PASS, no-op rejected, 446 changed rows, cheek sections 99.876900 to 94.901333 mm and 123.019609 to 118.035715 mm, unchanged 27.024369 mm central chin section, minimum source-fan area ratio 0.830608, minimum normal dot 0.983254, maximum edge gradient 0.178553, and all 76 oral XYZ rows exact after the full lip/smile chain. These are actual source-edge sections and invariants, not rendered face measurements.

The final lip-contour receipt reports PASS and former-contour rejection, unchanged accepted source heights/projection of about 6.104/6.660/2.207 mm, 445 combined perioral changed rows, 984 affected triangles, maximum displacement 2.332381 mm, minimum source-fan area ratio 0.576954 and normal dot 0.855480, with all 76 oral Y/Z and 5,788 protected rows exact. This continues to describe source geometry, not likeness or rendered lip contact.

I read `candidate10-input-preflight.json`: 516 independent neutral rows and 516 proposed rows match the new explicit pin. I read the saved candidate 10 `reference-smile-gate.json` top-level status, pin and failure count: `pass; live evaluated geometry and controls, within stated bounds`, the `52d36d7c...` pin above, and zero listed failures. I did not rerun the gate or audit every large witness array.

I read the hair probe's `final-source-hashes.json`, `temple-regression.json`, `unchanged-guards.json` and relevant `probe-receipt.json` fields under isolated `outputs/hair-probe10-corridor/`. Its two hair source hashes match the frozen candidate. The historical negative's maximum temple gap is 0.0460957 radians and the revised maximum is 0.00257145 against the unchanged 0.02 bound. The receipt reports zero protected face/ear centerline intersections across 1,449,000 checked segments, with curve radius omitted, and the saved input unchanged. The native oblique independently confirms closure of the specific visible wedge. These results do not certify the remaining hair silhouette.

I read the initial exact supplemental CLI run's `saved-verification.json` and `verify_saved10_v2.process.json`: status pass, exit zero, process tree closed, saved blend SHA-256 unchanged and equal to the artifact table. It reports 19,158 saved source vertices, all 13,378 canonical body faces with 4,198 hidden faces restored, 428,096 evaluated triangles, and successful rejection of a 457-vertex actual-body intrusion. All nine ornament results contain 480–9,856 evaluated triangles, positive sample counts, zero overlap pairs and minimum gaps of 14.543–40.082 mm. Fringe, crown and temples pass. I read these receipts; I did not run the CLI. This positive result does not exercise the new F16/F17 rejection cases or override the appearance findings.

I subsequently read the repaired run's `saved-verification.json`, SHA-256 `87c27d1e68502dc566ae4496cbbbefac7d3ed0f1de5bd1237dd27f7d1e7006e8`, and `verify_saved10_v3.process.json`. They report status pass, exit zero, process tree closed, exact verification-source hash `2fb43449...`, the existing pinned canonical-base hash `8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c`, the real empty-ornament control rejected, and the same saved blend hash unchanged. Canonical validation, clothing clearance, body-intrusion rejection, all nine ornament measurements and all three hair coverage guards pass. This verifies the new empty-geometry rejection on an actual Blender object; it is not a mocked predicate. The base guard is directly inspected against the existing pinned constant; no deliberate asset-tampering run is claimed. F16/F17 are resolved for this exact repaired checker, with no scene change or further appearance attempt.

Root owns expression and repository gates and process cleanup. This report does not invent their results or assert Git delivery. Geometry verification can establish a usable partial artifact while the appearance request remains unmet.

## Round outcome

The final authorized candidate is not accepted as completion of the appearance goal. The narrower upper body and specific sparse-gap repairs are real progress; F12's remaining hair shape and F13's facial naturalness remain unresolved against the fixed adult reference and benchmark. I found no blocking code defect in the reviewed new mechanics, and F15 is clarified. All ten integrated attempts are used: stop appearance adjustments, retain the exact evidence and report the partial result and unmet criteria honestly. This review does not lower the standard, authorize another candidate, or mark full realism complete.

The supplemental saved-finish checker repairs are accepted at `2fb43449...` after exact-source review and reading the final positive/negative-control receipt. No unresolved verifier finding remains in this round. This technical closure does not change the appearance rejection above.

# Review 13: integration

## Target

Candidate 11, the first integrated appearance attempt in the newly authorized second round, based on `1ef6de511a0214234b676277dbb1f27c20b47a63`. Exact inputs are retained under primary-checkout `outputs/sailor_character_realism_goal/candidate-11/source/`. The adjacent 34-file `source-manifest.json` has SHA-256 `bb4e5d00c5158cc1f25d37feda56d810379d6d6d637b78ed0242dd3842a83666`; I recomputed all 34 file hashes and lengths and matched it. This is a hair-only integrated change. The main scene is byte-identical to frozen candidate 10 and does not import or call the rejected orbital proposal.

| Key exact source | SHA-256 |
|---|---|
| `scenes/natural_hair.py` | `e359925b0104958c708c87216f4a1d8bf2619e15edba638193a1fd1e326c1f00` |
| `scenes/hair_groom.py` | `22422f22eb182473ab33ea833c9f646a508dac0dab4f2ff398fcf2aa2535d3d0` |
| `scenes/sailor_character_realistic.py` | `809c9a0d92520901dd03a37ad3ab659020dbbe7d41fd851d11e93e7bc1ef010c` |
| `tools/check_character_finish.py` | `2fb43449929926946fe9ed07adab66feed428b5dec15470803c4189259773fef` |

The hair-groom difference from candidate 10 is only a trailing blank line. Other retained cheek/frame/shape-check differences are line-ending normalization, not behavior changes. The variant tools in this manifest are the exact round 12 targets and are outside this dressed appearance review. All remaining unchanged source coverage is bounded by the prior reviews and the new manifest rather than claimed as a fresh full audit.

| Candidate 11 artifact | SHA-256 |
|---|---|
| `hero.png` | `c5c67f32edfe7f2f2d61b81eb0265525d7fe4bad40b558c7ed8ce050170c679d` |
| `portrait.png` | `a48f7d80417f64b9c5204cbdda553bc1a677491ead995b41a2ff71d008d88054` |
| `profile.png` | `fa03bb4416dfdc0f9f719d026752795b54affa37b8f7e5914dc1ae4a697a34d7` |
| `back.png` | `78a7079e19f3f605d5381e489ac7f6f780ac45a9a137c1926e38af9062435239` |
| `face_oblique.png` | `cb6dc5902a9a4f18fa774d8fb64261932c7c4d6748ce6e3d1aeddba720187550` |
| `torso_random.png` | `a312840403a6901fe94cd774257dc1c0778904b2f99ad409d722beb7cbce4067` |
| `sailor_character.blend` | `655715f58168c6339aad28df3c9085d57ff4bb44ab75dcec33618932af4811aa` |

The separate rejected orbital proposal remains recoverable under `outputs/character-round2-20261107/rejected-orbital-source/`; its manifest SHA-256 is `4073c1bf5bab22f58d1e4245467c3740520a8bb17a601796990b8289a4008a36`. I verified all four retained hashes. The proposal main was `e5b2bfafc41911a8c2f7ccb0a2427a5650993e3cec305af91a7145e067344f50`, helper `f991c646944d5721690bb933deef09ec744cc25094085f4b41ff73f337b6474b`, source checker `23203f8aea54d73091f26f217363ab212a345b79a9af5967575227775a9a4c21`, and final diagnostic fit checker `baa4d797da13463d20347929f992d68eb778310f263cfa9e7bdb58081591edcf`. Their status is rejected experimental evidence, not shipped candidate 11 behavior.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. I read the exact frozen hair change and its unchanged clearance/coverage dependencies, compared the source manifest against candidate 10, and read the actual-head probe's selected measurements and guard results. I inspected all six candidate 11 images with `view_image` at original detail, and re-opened candidate 10 portrait and profile at original detail for direct comparison. The previously reviewed frozen adult reference and round 2 benchmark remain the acceptance target. I also read the proposed orbital helper/source checker, initial evaluated failure receipt and authored location analysis; I did not independently audit every line of its later diagnostic fit checker. I launched no Blender/GPU process, rendered nothing, ran no tests in this round and edited only this report. Root owns all runtime gates and delivery.

## Reports

### Independent Codex reviewer

Reject candidate 11 as an improvement to the hair appearance and as completion of the overall naturalness goal. The portrait is narrower around the temples, but conspicuous side shelves now terminate at approximately ear height before the lower locks continue. The profile and opposite oblique show a pronounced ballooned rear/side mass with an abrupt inward waist and a visible upper transition ridge. The back confirms the inflated upper mass and pinched lower outline. These shapes are more artificial than candidate 10's smoother, already unaccepted curtain. The lower locks remain predominantly rigid vertical curtains; small inward bends and feathered tips do not establish the organic lock structure required by the benchmark.

This is a decisive native-image rejection, not an inference from a source metric. The early portrait alone showed an unacceptable common-height step, and the profile/oblique/back make the broader shape regression clearer. Frontal width reduction cannot compensate for the rear balloon and synchronized release ridge. Full forehead coverage remains, but density was never the sole acceptance requirement. The face reads unchanged, as the exact main source predicts. The narrowed upper body, bust/waist direction and smooth collar remain visibly consistent in hero and seeded torso. Thus F12 worsens in this candidate while F13 remains unresolved; neither the local hair goal nor the broader adult appearance goal is achieved.

The source has a coherent motivation: free-fall guides previously cut across the ear and forced a broad radial correction. `_Head` now derives an ear-bottom landmark from lateral anatomical rows. `_surface_turn` routes guides over the actual scalp/ear surface, samples neighboring radial constraints and smooths that local envelope. `_ear_turn` supplies a posterior angular sweep, and `_lower_lock` applies unequal inward curl and sweep below the jaw. Existing actual-strand clearance, child-lift cap, strand count, fringe/crown/temple checks and face/ear tests are retained. I found no unrelated source mutation or relaxed geometric threshold in this exact hair change.

However, `scenes/natural_hair.py:386` sets every fully routed guide's target to `head.ear_bottom - .010`. For the broad population with route weight one, the new surface route therefore ends at a shared vertical station before the free fall begins. This reintroduces the class of synchronized ear-height bend that earlier work removed. The visible shelves and pinched release region align with that mechanism. The source relationship is definite; the precise contribution of the surface envelope versus the subsequent clearance lift to each rendered ridge is not separately isolated by this review. The actual probe's larger rear correction is consistent with the expanded rear silhouette and rules out claiming that overall clearance inflation was solved.

The unchanged `clear_interpolated_strand` at `scenes/natural_hair.py:176` only checks its documented face/ear band, with `in_band` lower bound 1.442 m at line 186. New `_lower_lock` deformation continues below the jaw toward the shoulder-level ends, outside that proof. I specifically inspected neck, collar and shoulder relationships in profile, back, oblique and seeded torso and saw no obvious new penetration in these rendered views. That visual observation is not a whole-neck/shoulder collision certificate. The probe's side-width scanlines also begin above the ends. Any future accepted revision retaining those lower curls needs appropriate contact evidence if their placement changes or visible overlap appears; I do not invent a collision finding from the coverage gap alone.

The rejected orbital experiment illustrates why source bounds cannot substitute for evaluated fit. Its helper limited motion to the lower orbit/upper cheek, preserved X, oral rows, canthi and ocular anchors, and used a local circular approximation about the eye helper. Its source checker independently built a no-op production control, rejected that control, verified source fans and protected rows, and found unchanged source eye/lash proxies. Those are useful bounds, but the unchanged lash proxy is also why skin motion can disrupt attachment. The evaluated receipt rejects the proposal under the unchanged 50 micrometre guard. Root removed the proposal before candidate 11, and I agree with that disposition. No native improvement is claimed for an experiment that never reached an accepted fit.

F18 records this separate evaluated-fit failure. The first receipt reports 144.694 micrometres of additional signed eye penetration and 400.561 micrometres of additional lash penetration, with 301.908 micrometres of additional lash separation elsewhere. The follow-up authored location analysis identifies a central lower-lid sample close to the real lower corneal surface, so the local regression cannot be dismissed merely because distant cheek samples see an open-shell signed-distance artifact. It separately identifies a fixed lash root overtaken by the raised lower lid. The complete evaluated globe and all 516 smile-contract rows remain exact, but that does not repair contact. The route was appropriately excluded; adding its displacement to lashes alone would not establish ocular clearance.

## Findings and disposition

The following are this reviewer's observed dispositions. Root owns final selection and may append delivery evidence without rewriting the native judgment. Candidate 11 is one consumed appearance attempt in the new round; this report does not prescribe exhausting the remaining attempts.

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F11 | Prior collar/stripe shoulder regression. | Not observed in candidate 11; the visible body/garment direction remains intact. | No repair requested by this round. |
| F12 | Hair shape fails the natural appearance benchmark. | Candidate 11 adds side shelves, a ballooned rear silhouette, a common-height waist/ridge and still-rigid lower locks. Reject the candidate as a hair improvement. | Retain the failed evidence; a subsequent route must remove the shared release shape without relaxing clearance or hiding it through cameras. |
| F13 | Face does not achieve the requested soft natural adult appearance. | Face remains candidate 10, intentionally unchanged after the orbital rejection. | Unresolved; this hair-only candidate does not claim facial progress. |
| F18 | Proposed orbital deformation fails evaluated eye/lash fit despite passing source checks. | Root excluded the proposal before integration; reviewer agrees with exclusion on the observed red receipt and localized witnesses. | Preserved as rejected evidence. Any future ocular route needs actual evaluated shell/attachment evidence and independent native judgment. |

## Verification

I independently recomputed the 34 source hashes/lengths, all six image hashes and the final saved-blend hash. The adjacent artifact manifest agrees for the blend and four canonical renders; I hashed the two held-out images directly and checked their receipts. The seeded torso receipt records seed 20261107, its actual camera/target and the same saved-blend hash, with the temporary camera removed and saved blend unchanged. I did not infer appearance from these receipts: all six images were actually inspected at original detail.

The actual-head hair probe uses saved candidate 10's evaluated body and the exact `e359925b...` hair source. Its original and revised maximum guide correction are approximately 23.393 and 34.578 mm respectively. The largest revised correction is in the rear-side population, not the original upper temple witness. Its reported protected face/ear centerline crossings are zero across 1,449,000 segments; strand radius is omitted by those tests. It retains 23,000 roots/strands, reports maximum root distance about 0.1202 mm, maximum child lift about 1.1342 mm, and passes the unchanged frontal fringe, central crown and finite upper-temple coverage checks. These are prebuild geometry-probe results, not a full saved candidate 11 collision certificate or aesthetic acceptance.

I read the candidate 11 `reference-smile-gate.json` top-level status and failure count: pass for live evaluated geometry/controls within its stated bounds, zero failures. I did not audit every large witness array or run that gate. The initial orbital receipt and authored follow-up analysis were read as failed experimental evidence; no repaired orbital fit is claimed. Root-owned fleet, donut, saved-finish and process-cleanup results are not independently asserted here unless separately retained and reviewed by root.

## Round outcome

Candidate 11 is rejected as an appearance improvement. Narrower front-side width is real, but the new shelves, rear bulge and shared release ridge fail the fixed natural-hair benchmark, while the face remains unresolved. Preserve candidate 10 as the comparison/fallback and retain candidate 11 as failed evidence rather than silently replacing the prior artifact. The excluded orbital route remains rejected on evaluated fit. This report does not approve the overall appearance goal, infer contact safety outside the checked bands or transfer this review to a later source revision.

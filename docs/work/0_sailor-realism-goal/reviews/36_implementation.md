# Review 36: implementation

## Target

Candidate24 actual six-view native face appearance, compared with unchanged candidate10 and the original adult-20 reference.

## Reviewers and coverage

Fresh independent Codex visual reviewer, Astra xhigh, received the reference and benchmark without the author's proposal or earlier aesthetic conclusions. Root separately inspected all six native candidate views and the baseline portrait, opposite oblique and profile. Root owns rendering.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 6ac7a8eebf8c89f77ffd82aea5d9c7fbd5e24dc8e13e606c2d7aff4c034eb3ac.

# Candidate 24 independent native visual review

2026-11-08. Scope: the face-only adult20 trial compared with candidate 10 and the supplied original character reference. Verdict: **REJECT as material local visual progress.** The six native renders do not show a convincing improvement in adult naturalness, appeal, expression, cheekâ€“lip integration, or profile. No conspicuous new face artifact was found, but preserving the baseline is not sufficient to accept this trial. This is not an acceptance of the full character.

I inspected the supplied reference and all six candidate-10 images before seeing candidate 24, then inspected all six candidate-24 PNGs with `view_image` at `detail: original`. Before forming the verdict and writing the report, I did not read the author's face proposal, implementation rationale, or another reviewer's aesthetic findings. No image-difference score, geometry metric, or successful render was treated as evidence of visual success. No Blender, GPU renderer, browser, or GUI was launched by this reviewer, and no reviewer-owned background process remains. The report is the only file this reviewer wrote.

**C24-V1 â€” The intended face improvement is not visibly established.** In the native portrait, the broad, smooth cheek fields and the pale, prominently edged lower lip still give essentially the same synthetic face and lightly fixed smile as candidate 10. The corners form a distinct mouth curve without a clearly more convincing response in the adjacent cheek and lower-eye region. The oblique view preserves the same impression: the mouth still reads somewhat applied to a smooth lower face, and the cheek-to-mouth transition has not visibly become more anatomical or expressive. Against the supplied adult reference, the candidate still lacks the reference's integrated cheek, eyelid, and closed-smile expression. I cannot identify a meaningful gain that would be apparent to a viewer without being told that geometry changed. This finding is about the visible result, not an assertion that the mesh is unchanged.

| Native view | Observation |
|---|---|
| `portrait.png`, 1200 Ã— 1200 | Same overall face identity, eye expression, cheek fullness, and mouth reading as baseline. The eyes remain conspicuously open and reflective, and the smile is still concentrated at the lips rather than clearly coordinated through the face. No visible material improvement in adult naturalness or appeal. No new tear, sharp dimple, lip break, or obvious left/right distortion. |
| `face_oblique.png`, 1200 Ã— 1200 | Cheek/lip integration remains weak in the same way as baseline; the bright lip and dark mouth curve remain visually distinct from the smooth surrounding face. The chin and jaw continue smoothly without a newly visible kink. No convincing improvement in expression at this angle. |
| `profile.png`, 1200 Ã— 1200 | The visible noseâ€“lipâ€“chin silhouette and lower-face projection read essentially the same as candidate 10. No clear advance toward the more naturally integrated profile in the reference. No new profile protrusion, collapse, or silhouette discontinuity is apparent. Hair hides much of the jaw/ear/neck transition, limiting inspection there. |
| `hero.png`, 1280 Ã— 1600 | No meaningful face improvement at full-character viewing scale. The adult body/head relationship and existing pose are maintained; the trial does not visibly enlarge the eyes/head or shorten the lower face into a juvenile substitute. The existing broad upper-body impression remains, as expected for a face-only trial. |
| `back.png`, 880 Ã— 1100 | No face can be evaluated directly. Hair, clothing, and body silhouette remain visually consistent with the baseline, with no apparent collateral change. |
| `torso_random.png`, 1200 Ã— 1400 | The same slightly fixed smile and smooth facial construction persist from this second three-quarter direction. No apparent new facial artifact or collateral body/clothing change. No material gain in how the face reads within the upper body. |

The supplied reference shows a young adult with adult facial proportions and a restrained, integrated smile. Candidate 24 retains the baseline adult scale and does not introduce an obvious juvenile-proportion shortcut. Its lack of visible progress should not be answered merely by increasing eye size, shrinking the jaw, or rounding the face; the missing quality is coordinated facial form and expression.

Hair remains an inherited limitation: its uniform crown/fringe and straight sheet-like falls differ visibly from the reference, and the profile's lower-hair gap/termination issue persists. These are not new regressions caused by candidate 24. The known lower-hair F21 remains open; this review does not certify the groom, body proportions, cloth realism, or full-character completion. The current images show no conspicuous newly introduced face defect, but small unseen mesh problems cannot be excluded by these views.

The render receipt was read only after the independent visual judgment. Its status at binding was `rendered_pending_native_visual_review`; `saved_inputs_unchanged`, `all_retained_state_exact`, and `temporary_cameras_removed` are true, and `whole_groom_pass` is false. These are receipt claims, not independent code or scene-state certification. The actual saved `.blend` SHA-256 and all six actual PNG SHA-256 values were recomputed and matched the receipt. After the blind judgment and report were written, the root agent confirmed renderer exit 0, closure of its owned PID 21608, and the same final receipt hash. This reviewer did not independently inspect or stop that process. Runtime completion therefore no longer awaits root confirmation; it does not change the visual rejection.

Artifact binding, SHA-256:

| Artifact | SHA-256 |
|---|---|
| Candidate-24 `render-receipt.json` | `7c76d9dad4f8f452b17d9c68d1ce8299cb8602899f8ab9dc111464fae0fa6c0b` |
| Candidate-24 actual saved `candidate24-source/provisional.blend` | `35b7c1f2e06bd2d04aa97c7f4f74bcb40d9a5fc0c51a464cdf8b3d71af1c0a0f` |
| Build result, as bound by receipt | `675bebea1ead32c3467d55d6b4a9e31e20f0331888701b70b4fd20f97a9901d2` |
| Render script, as bound by receipt | `6171d65cade20fd651699e07bae4338104524ca35dfebb69218f8e0ce9f58d3a` |
| Candidate-24 `hero.png` | `bdb8c69ced70d7ad0258833553f1b359cf751fe94cf5db00b9660d83fcc8b8c4` |
| Candidate-24 `portrait.png` | `59d6c9815c03ebba53bd35dceb3f551c05e1b7c58fcf838631fac4767fefc038` |
| Candidate-24 `profile.png` | `ad9c0754c6c69d9c4be78619888b4603e3725e99aa5fd267b084c4d77e6224c1` |
| Candidate-24 `back.png` | `1ea715d2be6d8f41f33ceae73c8938123fc407e3fb8c993678c41ba7dac626ff` |
| Candidate-24 `face_oblique.png` | `0f0e8112c1d18d2650c354e4dc4ff242b4bd1ea79366055d3790499222f2b3c1` |
| Candidate-24 `torso_random.png` | `23122378bc4127abbde617a692e370f69ebc77011122c76d8aabe95012064874` |
| Original `character-reference.png` | `ea71fef894f068da0736a177ce4619ef176d0719581033cab8781b63f18e1139` |
| Candidate-10 `hero.png` | `1c1895fadb01bf4af7578b6f77d0f68dbb867656810a2a18d14ae13930fa9503` |
| Candidate-10 `portrait.png` | `8a312efd5f083cf04d3daddd9c18f893584b58faac8bdb8c13029ee6dfe65a09` |
| Candidate-10 `profile.png` | `4c33b1807012a4284bcaea04863f3f77c6a4a0967bf457fa1a5b75939aa46046` |
| Candidate-10 `back.png` | `98dd22cc70a791aaabfae1eeeda29f5f550d5b52b96d543c73440fec150e7d49` |
| Candidate-10 `face_oblique.png` | `48d051b2c71898d58a1e11249bba83de0bb1565468f6dd95113991c7fa9a4a9b` |
| Candidate-10 `torso_random.png` | `722a04eb44240abf56978e920dc21db4257f1a7ac0d51818148bea7f5da883b1` |

Reviewed input folders are `outputs/sailor_character_realism_goal/candidate-10/`, `outputs/sailor_character_realism_goal/candidate-24/`, and `outputs/sailor_character_proportions/references/character-reference.png`. Repository AGENTS, retention rules, and fleet review pins were read. `docs/learning/lessons.md` was absent from the main checkout. No source edits or runtime tests were required or performed for this bounded visual review.


## Findings and disposition

Reject candidate24 as material local visual progress. Root agrees with the independent reading: the face and expression remain essentially the same; the small cheek/mouth change does not visibly resolve the user's complaint. No obvious new deformation appears. Geometric safety is retained but does not rescue an aesthetically ineffective result. No production runtime source changes are accepted.

## Verification

All six images are native dimensions and match the final receipt hashes. Renderer PID21608 exits zero and closes after108.196 seconds. All retained state, source and saved inputs remain exact and temporary cameras are removed. The final render receipt hashes to7c76d9dad4f8f452b17d9c68d1ce8299cb8602899f8ab9dc111464fae0fa6c0b. Complete source, blend, render and process evidence is archived outside the worktree.

## Round outcome

Four of ten round3 attempts are used; six remain, next number25. Candidate24 is rejected, not delivered as improved. Candidate10 remains the dressed draft and accepted anatomy14 is unchanged. The next face investigation addresses the actual eye-opening additions and visible anatomical placement rather than increasing the rejected lateral field amplitude. The next hair investigation addresses outer-ear routing and actual terminal arrival.

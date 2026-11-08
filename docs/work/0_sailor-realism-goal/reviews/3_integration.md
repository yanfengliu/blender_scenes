# Review 3: ocular layer integration

## Target

Goal candidate4 against candidate3, base0b79ee16f9bb0aeedc4503507f38c735276879ca. Exact uncommitted code is retained under outputs/sailor_character_realism_goal/candidate-4/source with all16 used sources and source.patch SHA382E677AF59CED965562B9EAD0158232915A3462CA6B1CDF4C662089C133B051. Main SHA F997A6CC7AC69EA93686F5E9B79F2F640708D69FEAD320FE8FA5CE14CC1EE6CB, ocular helper468DC427C55499EE6ECDF6D0F75259EBA422215A886416238C0A6649B5E02A59 and checker7186BD4D07CD2CBBF8C6D87AE49CEEEAE54DE8AA75ED60536D02145B2FB3FA38. Saved blend B9CB210243C7E05B9EAE904E20F344EB683ED1F2E3DCA3A3A77B88FC5DA43837. The natural_face change is only the previously reviewed docstring correction.

| Image | SHA256 |
| --- | --- |
| hero.png | `1492572750453C7857F3633D1C293987B58D29CA49FEEA9E766761B305C0B288` |
| portrait.png | `5BC4C849DDF205DF47F184A6145DCA51DF026300FE56CBB6FA7D71B48D5BEC3A` |
| profile.png | `D2678BC5DFB152CB955901C5B8ABB3933E7DACC8E3F491159FA6E5DBF85903E4` |
| back.png | `DABD1464A1F118A976C4589722F0DCE03EC85E45B8D35FE9AC971886BB756FDF` |
| face_oblique.png | `5BC4AA7DC6D71FB3AC3D38F4BEAEC31E8B0BAC942ABCA3DE9E4A56CA316E25F4` |

## Reviewers and coverage

Root inspected the exact source patch, corrected raw-byte reconciliation, five native integrated images and saved proof. build_runner inspected all five native integrated images against the frozen reference and owns runtime verification. face_reference_review separately inspected the five integrated images; its diagnostic and integrated authored verdicts are retained separately below.

## Reports

### face_reference_review — authored diagnostic verdict

I inspected native portrait SHA23992CBEF8CB1CCBB57EAC4A2A2F92047D3686A88F1F302BCD4E9C566AF077A8 and oblique SHA94D57888A04B9999D501EE9E96B7BE41ED839C49E683C266CAC441CB5227DBDF. Both remove candidate3’s broad pale iris crescents. Dark brown ocular areas remain clear against sclera in the opposite oblique, the critical previously failed view. Localized bright spots are consistent with two studio lights; I see no duplicated iris/pupil contour in these images. Accept this specific ocular improvement for integration, not overall photographic likeness. Irises look nearly black with strong reflections relative to reference, but reducing shininess without isolating lighting would be premature. Falsifier: any return of pale rim/crescent, duplicated pupil boundary, cut scleral patch, or lid gap in integrated portrait/profile/oblique.

### face_reference_review — authored integrated verdict

I separately inspected all five actual candidate4 images at native resolution against frozen candidate3 and the original reference. Portrait SHA5BC4C849DDF205DF47F184A6145DCA51DF026300FE56CBB6FA7D71B48D5BEC3A and oblique SHA5BC4AA7DC6D71FB3AC3D38F4BEAEC31E8B0BAC942ABCA3DE9E4A56CA316E25F4 retain removal of broad pale iris crescents; dark irises and localized catchlights remain coherent with no duplicated pupil contour. Profile SHAD2678BC5DFB152CB955901C5B8ABB3933E7DACC8E3F491159FA6E5DBF85903E4 is largely occluded and weak for iris optics but shows no new visible facial/profile regression. Hero SHA1492572750453C7857F3633D1C293987B58D29CA49FEEA9E766761B305C0B288 and back SHADABD1464A1F118A976C4589722F0DCE03EC85E45B8D35FE9AC971886BB756FDF preserve visible body/uniform/pose/hair. Accept the ocular increment for these exact five hashes, subject to saved structural/mutation checks. Overall realism remains incomplete: smooth pale skin, restrained smile and stiff curtain hair persist. This is a separate integrated artifact review, not approval transferred from the earlier diagnostic renders.

### root — authored integrated visual judgment

Root actualnative5 candidate4 review completed against3/reference. Retain ocular increment CONDITIONAL on savedisolation/checkermutationproof: bothportrait5BC4C849...BEC3A andoblique5BC4AA7D...E25F4 preserveclear darkbrowniris/sclera distinctionwithoutpale crescents/duplicatedcontour/newlidgap. Profilehas no visibleocularregression but isoccluded/weakirisview. Hero/back preserveapprovedbody/uniform andno newvisiblefitdefect. Darkeyes, smoothpaleskin, levelmouth/weakcheeksmile andcurtainhairremain; overallnotrealistic/referenceaccepted. No moreeyetuningwithoutdistinctmechanism; proceedverifiedhair/smile.

### build_runner — authored integrated judgment

I inspected all five integrated images at native resolution against the frozen character reference. Portrait and opposite-side oblique retain dark iris/sclera separation without the old broad pale crescents. I see no doubled pupil contour, new lid gap or abrupt scleral patch; the profile is a weak iris view because of occlusion. Hero and back retain the approved body and clothing fit without a new visible break. The dark, strongly reflected eyes, smooth pale face, mottled knees, level mouth and rigid curtain hair still differ from the reference. Retain the local ocular gain if independent integrated review agrees; this is not full realism.

## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
| --- | --- | --- | --- |
| F4 | Broad pale iris crescents persisted after material-only tuning. | The existing cornea was transparent from the shared texture while inner concave tissue had direct specular reflection. The separated layers remove that visual defect in the two critical views. | Preserve independent integrated review and the exact saved layer contract; dark irises remain a realism limitation. |
| F6 | The prior checker required image alpha on every eye material. | That rule incorrectly rejected the supported untextured corneal dielectric. Its failure is retained as instrument evidence. | New canonical gate validates actual complete components/UV/material slots; actual alpha, transmission and assignment mutations plus old3 fail while4 passes. |
| F2 | Local checks do not certify optical realism or all geometry. | Keep finite evaluated-layer and saved-capture bounds explicit. | Native five views remain required; no corneal thickness, full optical-path or global lid/lash clearance claim. |
| F0 | Skin still differs from the reference. | Unresolved and unaffected by this eye-only integration. | A separate supported mechanism is needed. |
| F1 | Smile and hair still differ from the reference. | Unresolved and unaffected by this eye-only integration. | Separate staged mechanisms remain unimported until their own review. |

## Verification

Canonical four views at1600/128 and fixed85mm opposite-side oblique at1200square/128 render successfully. Current standalone checker exits0. Exact saved comparison exits0: all114 other objects,16 other materials,27 material-attribute meshes, four packed images, eye source positions/UV/modifier inputs and all studio inputs remain candidate3. The eye graphs match the accepted diagnostic exactly. Complete evaluated shell/tissue tessellations have zero overlaps;25,522 nearest samples have minimum0.168891mm clearance and7,148 forward iris rays have no misses. No expanded hair tubes or arbitrary RNA pointers are covered.

Actual Alpha0, Transmission0 and one misplaced shell-face mutations are rejected; restored4 passes. Actual prior single-material3 fails the new eye contract. The unchanged old checker exits1 only on its obsolete corneal image-alpha rule. Each process closes its owned job and saved files remain unchanged. All16 frozen used files match live bytes and all26 current scenes/tools Python files parse. Full receipts and hashes are in candidate-4/verification-summary.json. The initial newline-only patch artifact is retained; raw hashes prove no corresponding source drift.

## Round outcome

Four of ten integrated attempts are used. Root and independent integrated five-view review retain the local ocular improvement. Their historical conditional wording above is satisfied by the actual saved and mutation checks described here; no report was rewritten to remove its original qualifier. Overall realism and CHR-001 remain open. Historical diagnostic approval does not transfer automatically to these integrated pixels. No hair/smile source is imported and no Git delivery occurs in this round.

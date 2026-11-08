# Review 4: documentation checkpoint status correction

## Target

The independent review targets the exact 16-file candidate4-v2 documentation payload at base 3863928adbc9138f4a9daa18abdf50adeba80045. It does not review or accept character source or pixels. The complete authored report below has source SHA256 7299E85883206759B555D6579571F31FECE8F78A907E96C884E33EE829D169CA. Its companion raw evidence has SHA256 C3C281CDCC9E098EACC1E780CAE157AB167A0F666C610D5988871F6A7515864C and remains ignored in the Fleet review directory.

The exact reviewed plan is preserved in snapshots/20260908-before-fleet-status/plan.md, SHA256 BA1C4CBB44CEB74FDD0DED3F8544C71A3EAC9976D3EDCA0930BD29EBB4C85AD2. It was recovered unchanged from the already frozen v2 payload after the current plan correction. The original v2 payload and manifest remain unchanged.

## Reviewers and coverage

scenes_docs_review independently read the exact v2 documentation payload and its supporting evidence. Root inspected the same payload, hashes and Fleet test. build_runner corrected the current status and preserved the reviewed target. No product code or visual acceptance is claimed by this review.

## Reports

The following is the complete independent authored report, preserved verbatim.

# Blender candidate4-v2 documentation review

Reviewer: scenes_docs_review, independent read-only documentation reviewer. Date: 2026-09-08.

Verdict: one current-status correction remains, F7. No other actionable documentation finding was identified in this frozen checkpoint. This review grants no writer window, Git action, product acceptance or change to an owner hold.

## Exact target

Base: blender_scenes at 3863928adbc9138f4a9daa18abdf50adeba80045. Historical source-review base: 0b79ee16f9bb0aeedc4503507f38c735276879ca, verified as an ancestor of the checkpoint base.

The target is exactly the 16 documents, 84,789 bytes, under outputs/sailor_character_realism_goal/docs-checkpoint-candidate4-v2/payload. Manifest SHA-256: 8e74a6a235b6b4793073eafb287798d29a9a2a0a97e12a9e5100080412b4f93b. Expected staged patch SHA-256: a2c3297c927d5840360e35d6e90e4b6319d7bc85c544a9269586ad0b31e1cb32. Per-file hashes and verification details are retained in the companion evidence.json.

## Finding

**F7 — [P2] Update the plan's current Fleet verification result.** In docs/work/0_sailor-realism-goal/plan.md:38, the current Outcome still ends its verification account with the old 83/84 Fleet result and says that no new green claim is made. The same frozen checkpoint records a fresh official Fleet run with exit 0, 102 tests, 102 passes and zero failures. I verified the receipt and log against the manifest's hashes; this is a contradictory current-status account, not an unavailable check. Readers following the required single current status record would retain the obsolete blocker or fail to discover the completed verification.

The owner should update the current Outcome to name the dated 102/102 result and its Fleet-only scope, keeping Blender realism incomplete at 4/10 and preserving the historical 83/84 account in the existing snapshot/history. Preserve this reviewed plan target before editing, then freeze the revised document and manifest for focused re-review. F7 is the next unused global finding ID after the checkpoint's F0–F6. This agrees with the coordinator's separately observed current-status concern.

## Coverage and results

I read all four review rounds, all four retained plan/report snapshots, the current plan, applicable repository rules, the shared work-document contract, and the supporting manifests and receipts. Every frozen payload file matches its declared size and SHA-256. The expected patch reconstructs exactly those 16 files from the stated Git base after line-ending normalization; reconstruction happened in memory without applying a patch to a worktree or index. The partial devlog snapshot contains only the four selected goal entries plus the original HEAD content. It intentionally differs from the broader live devlog; unrelated entries remain excluded.

The pre-correction round 0 and round 1 texts are preserved exactly before their new appendices. Round 2 preserves its original text apart from the explicitly labelled eye_study heading correction; its original heading and bytes remain in the snapshot. The global mapping is coherent: F0 skin; F1 form/groom; F2 verification scope; F3 the evaluated-position instrument; F4 eyes; F5 measurement independence; F6 the obsolete eye-alpha checker. Round 3 reuses those IDs and retains the original conditional verdict wording. Its two available independent authored reports and the builder's authored report appear in full. Round 2 honestly identifies the unavailable full eye_study report and retains the surviving summary without inventing a replacement.

Recoverability checks matched all 60 named frozen source files across candidates 1–4 and all 24 saved model/image artifacts, including the separate candidate-1 oblique receipt. Each candidate's source patch is present; candidate 4's patch matches the hash printed in round 3. This establishes present byte recovery, not product correctness or permanent availability after cleanup. Those ignored targets remain required active evidence until the owner binds them to an appropriately retained or committed target.

The five declared read-only dependencies match the manifest and remain outside the 16-path payload. The scoped work-doc attributes contain exactly '* -text' plus LF. The official work-doc checker exited 0 for one unit. The independently inspected Fleet receipt/log match the declared hashes and show 102/102 passing. The full Fleet suite was not rerun during this review.

The plan, reports and defect record consistently leave overall realism and CHR-001 open, with four of ten integrated attempts used. Local ocular retention is distinguished from full likeness and from prior diagnostic approval. No image was visually inspected, no product source correctness was judged, and no Blender, browser or server was launched. No sibling file, Git index, ref or configuration was changed. Final rehashes retained the manifest, patch and payload bytes at the reviewed target; HEAD remained 3863928adbc9138f4a9daa18abdf50adeba80045.

## Findings and disposition

| ID | Finding | Disposition | Verification |
| --- | --- | --- | --- |
| F7 | The current plan repeats an obsolete 83/84 Fleet result despite fresh green evidence. | Corrected only the current Outcome to state the dated 102/102 result and Fleet-only scope. Historical failure records and the reviewed plan bytes remain preserved. | The normal-OS-temp official npm test exited 0 with 102 tests and zero failures. The current work-doc checker passes for one unit. Focused re-review of the revised payload remains pending. |

## Verification

The fresh Fleet log and receipt show 102/102 passing with exit 0. The reviewed v2 target and original report hashes were verified before copying. The current official work-doc checker and scoped diff check are required for the revised payload; focused independent re-review is pending.

## Round outcome

The documentation checkpoint is prepared for review. Character source remains uncommitted; no Git action or product delivery occurs in this round. Overall realism and CHR-001 remain open at four of ten integrated attempts. The revised payload excludes README and preserves the partial devlog scope. This round adds only the necessary reviewed-plan snapshot and this authored report with its disposition.

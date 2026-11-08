# Review 35: implementation

## Target

Candidate24 complete body-loop state serialization, unchanged face geometry proposal and the native state/capsule preflight.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns the actual headless Blender controls and subsequent integrated build.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 e0575ecdae1d9f7ae346d47f544b6bce5ea6f85effb6eb067e3d05638480b728.

# Independent candidate-24 state-serialization fix review

Reviewed 2026-11-08. This is a bounded follow-up to the actual candidate-22 failure recorded in `review/face22-driver.md` SHA `d988cca8e9456b98e9eaf03f0337b14729fc6e64792147c2119e876b8f8d520f`. That failed candidate and report are preserved. I ran no Blender, GPU, geometry build or render. This report is the only reviewer-authored output for this follow-up.

## Exact source and decision

No blocking source defect was found in the serialization repair. It retains the complete input map as deterministic JSON-compatible records. Candidate 24 has no proposal, aperture-bound, hair-clearance, camera, lighting, sampling or saved-scene validation change relative to the reviewed candidate 22. Root may exercise the exact repaired driver in an owned geometry build once its native preflight is inspected. Rendering remains conditional on the actual complete changed-skin/shaft check, face/ear guards and exact reopened-state bindings. Inherited F21 remains open; this review does not approve whole-groom acceptance or appearance.

All files are in `C:/Users/38909/Documents/github/blender_scenes/outputs/character-round3-20261108/candidate24-source`.

| File | SHA256 |
| --- | --- |
| `build_face_candidate24.py` | `d3dd26edc69497634660ed8402f497ee5f4fa3935420a48c7d063dcf80397b02` |
| `face_candidate24_helpers.py` | `1b8beb2748d3e19542eaf81a844425a99841237757106c903ad04f1137a84e10` |
| `render_face_candidate24.py` | `6171d65cade20fd651699e07bae4338104524ca35dfebb69218f8e0ce9f58d3a` |
| `prepare_manifest.py` | `6a1c7e4b4a63869b637677fa00462e5f3ed947b0bfdcf772fb3b2e451643fa4d` |
| `test_capsule_bound.py` | `5f5274dd8674a665d40aa7b50cc54e5a27cd7dc0778ddbdf9ca2c5e3b26535b4` |
| `source-manifest.json` | `fa14c68c54ab74880dfca48e4600230ec6b57495dda736c12fe46007f1cf4e5e` |

I independently rehashed all five local and 24 external manifest entries; all matched. The 24 external pins are identical to candidate 22, including the original baseline blend, accepted topology measurement, unchanged material-aperture instrument, exact stored coordinates, native hair fingerprint evidence and six camera/image references. The manifest's descriptive `runtime_base_revision` still names a docs commit; the exact file pins establish source identity.

## Repair and independent controls

After normalizing only the candidate labels and integer candidate ID from 22 to 24, the five Python source files are byte-for-byte equivalent to candidate 22 except for the new comment and assignment at `face_candidate24_helpers.py:41-42`. The assignment converts `shape['loops']` from `{vertex_tuple: attributes}` to sorted `(list(vertex_tuple), attributes)` records before the existing digest. It neither drops polygon settings/UVs/colors nor changes their values. Unique tuple keys become unique integer lists, and lexicographic sorting makes dictionary insertion order immaterial. Sorting cannot reach dictionary-value comparisons because the incoming dictionary keys are unique.

I extracted and executed that exact assignment with Python AST in a read-only process. A complete representative map round-trips to exactly the original tuples and payloads; reversing map insertion order produces the same records; changing a vertex key, polygon setting, UV coordinate or color value changes the resulting JSON digest. All five source files parse successfully. No `bpy` import or evidence-file write was involved in these controls. The existing body snapshot's tuple-key map semantics remain unchanged apart from representation; this fix does not claim to expand the original snapshot schema.

The source-level candidate-22 P1 is repaired at the failing boundary: the actual map now reaches `json.dumps` with JSON-compatible keys and without losing its polygon payload. A native pass is still necessary because pure serialization controls do not exercise Blender RNA state, the large hair population or saved-scene behavior.

## Native preflight scope

The root-owned `face-state24-probe/run_state_probe.py` SHA `2a4cdbeac64e0185a20cc315967cf8fef85924166daa3776ab5a91d50c2c58b1` loads the immutable candidate-10 blend, calls the real complete `fixed_state()` twice, mutates and restores a real body UV and a real hair point radius, and confirms body positions are intentionally excluded from that state digest but caught by the separate coordinate hash. It also invokes the actual Blender BVH capsule helper on clear, centerline-crossing and radius-only-intersection cases. The final checks require the original retained-state/hair fingerprints, exact body coordinates, unchanged source files and unchanged baseline blend. Partial control progress is not an overall pass.

This preflight does not save a blend, apply the face proposal or render. Save/reopen equivalence remains an execution condition of the unchanged full builder and renderer; it is not established by the preflight and must not be inferred from it. Testing that condition in the owned build is acceptable because the saved candidate is isolated and no render may start until the reopened candidate passes all exact checks. Root owns process cleanup and must supply the completed receipt and process result for the native decision.

## Completed native preflight and bounded conclusion

I inspected the completed `face-state24-probe/state-controls.json` SHA `4222f446179f85453af0fdc9421f4752677943762661f9f8ac020d96dcbbc35e` and `run_state_probe.process.json` SHA `39e999e590b312686c80d3d2f962c5c0e43d22ef1584861fd8f660d85b950059`. The process record binds the exact script above and records PID 52948, exit code 0, 149.390269 seconds and a closed process tree. I independently rehashed all four recorded source dependencies and the baseline blend afterward; they match. The prior candidate-22 review remains unchanged.

All seven native controls passed. The complete actual baseline state serialized twice to `3ae690ec3f29f4a9197814be219d1bf34cb27b47a667a37c4d1ad37d087d3521`. The real body-loop UV mutation changed the digest and restoration recovered it. The real hair-radius mutation changed both the separate full-hair fingerprint and complete retained-state digest; restoration recovered the original state. The body-position mutation left the deliberately coordinate-excluding state digest unchanged while changing the independent coordinate hash, and exact positions were restored.

The actual Blender BVH clear-segment control was certified after seven nodes and depth two, with a 1.439899937 mm minimum computed clearance lower bound. The centerline-crossing and radius-only-intersection controls were both rejected after depth-budget exhaustion, with negative lower bounds. These negatives demonstrate conservative rejection; they are not successful clearance certificates. The final receipt requires and records all native state restored, baseline/source unchanged, no save and no render. The exact source ensures those flags are set only after all seven controls and final state assertions, with exceptions marking failure.

This native evidence resolves candidate 22's actual serialization blocker for the frozen helper. The source and preflight are sufficient for root to run the exact candidate-24 geometry build. There is still no candidate-24 changed-skin clearance result, saved/reopened scene pass or image in this review. Those remain mandatory before rendering, using the unchanged original 50 micrometre mouth/ocular evidence, complete retained hair identity and all current fail-closed shaft/face/ear checks. Full-groom F21 acceptance remains outside this face-only experiment.

## Subsequent actual geometry-build addendum

The preceding source and preflight judgments are preserved. I subsequently inspected the completed root-owned geometry run in `candidate24-source/build-result.json` SHA `675bebea1ead32c3467d55d6b4a9e31e20f0331888701b70b4fd20f97a9901d2` and `build_face_candidate24.process.json` SHA `0a9561448b52b6b7b34b7f13a72a3ebacca0d12c4c91a904bf75da3b02cb0440`. The process record binds reviewed build SHA `d3dd26edc69497634660ed8402f497ee5f4fa3935420a48c7d063dcf80397b02` and records PID 53272, exit code 0, 110.698730 seconds and a closed process tree. The result status is `face_geometry_pass_pending_native_appearance`. The saved `provisional.blend` independently hashes to its reported SHA `35b7c1f2e06bd2d04aa97c7f4f74bcb40d9a5fc0c51a464cdf8b3d71af1c0a0f`.

The complete retained hair population is 23,000 paths and 1,449,000 segments. The changed-skin certificate accounts for every segment exactly: 1,435,082 are excluded by the radius-padded AABB proof and 13,918 are certified by the capsule distance lower bound, with zero failures or unresolved segments. The latter needed one node per segment and no subdivision in this actual run. Their minimum computed clearance lower bound is 0.484343107 mm, including the existing 0.1 micrometre reserve. That number is the minimum for the capsule-certified subset; the AABB-excluded population has a separate positive-separation proof, not a reported numerical minimum of 0.484 mm. Neither measurement is a whole-groom 1.5 mm clearance claim.

The complete final changed-skin patch contains 11,964 incrementally changed evaluated vertices, all 12,330 polygons incident to those vertices, and 24,660 triangles. Its polygon identity digest is `9d25dc90f998c7da2414afdd8d61ae7be5df79c0371707f428afae161a3f3d6e`. This incremental patch is the correct population for new intersections against unchanged candidate-10 hair; the earlier mouth safety instrument separately retains the full cumulative original-neutral influence and 642-row union. The preserved centerline-only front-face and ear guards each checked all 1,449,000 segments and found zero crossings; the complete changed-patch capsule proof supplies the strand-radius protection omitted by those inherited regional guards.

The actual build reports exact replay of all 512 requested rows, exact retention of the other 18,646 source rows and all 1,269 ocular guards, and the unchanged original mouth contract. Its full source-coordinate digest is `cc111c3c06ce9f8ada56768831e960fa726095b231c430a14fc200cbfa3feeda`; its factual binding digest is `15b0439aa9cf1deea98dbf869f7aa0d44112d4839c476e0c52e99815c35b1c97`. The accepted measurement remains `c9f2ed283b0b2b964a7aa346a09e660dd27c84be6d731f0dacf1c90083ec6027`. The retained-state digest is exactly the native preflight baseline `3ae690ec3f29f4a9197814be219d1bf34cb27b47a667a37c4d1ad37d087d3521`; the complete retained-hair render digest is `948e256419f866cc1e35a487f686ebb55b692020b83306bc30a52c9c5e15a07e`.

The builder's lines 113-118 reopen the saved bytes and require exact factual binding, historical contract, every body position, complete retained-state digest and full-hair fingerprint before setting `reopened_source_and_retained_state_exact`. This actual result passed those assertions. I independently rehashed all 30 recorded source/baseline/manifest entries afterward; there are no mismatches. The baseline remains unchanged, and source-row and segment accounting are arithmetically complete. The root-reported operating-system thumbnail-cache warning did not prevent these actual file/hash/reopen checks; it is not used as evidence for or against geometry quality.

The reviewed source conditions for one face-only six-view native render are now met for this exact saved artifact. The unchanged renderer must still pass its own independent baseline/reopen comparisons, use the frozen native cameras and 128-sample GPU settings, and restore all temporary state. I have not inspected a candidate-24 image or completed render receipt in this addendum. Appearance improvement, final-character acceptance and inherited F21 full-groom clearance remain unapproved.


## Findings and disposition

Accepted the instrument correction. Complete loop keys and attributes are retained as sorted records; all other changes are candidate identifiers and corresponding hash bindings. The same exact face field and physical limits remain. Candidate22's actual failure stays preserved.

## Verification

All seven native controls pass: deterministic complete baseline hashing, UV mutation/restoration, hair-radius mutation/restoration, explicit position exclusion with separate coordinate hashing, and actual BVH clear/crossing/radius-only capsule cases. Baseline/source bytes and in-memory state are restored. PID52948 exits zero and closes after149.390 seconds. This preflight saves no scene and makes no appearance claim.

## Round outcome

Actual candidate24 geometry, complete changed-skin shaft coverage, retained state and saved-scene reopening now pass. All 1,449,000 hair segments are accounted for: 1,435,082 have positive AABB separation and 13,918 have capsule distance certificates, with zero failures. PID53272 exits zero and closes after110.699 seconds. Six native views are rendering; no appearance acceptance is claimed. Full-groom F21 remains open. This is the fourth integrated round3 attempt.

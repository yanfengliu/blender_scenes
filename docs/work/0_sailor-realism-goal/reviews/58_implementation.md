# Review 58: implementation

## Target

Final candidate-30 failure and authorized round closeout.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Read-only source and retained-data review; root owns closeout and delivery.

## Reports

Complete authored report, SHA-256 `5a3d723a84e64685eb81ca94f54d1900b46ba8ce14435339c27292ec1f2a67b2`.

# Round3 final disposition — 2026-11-08

Candidate30 failed and is not accepted. Root's round ledger is exhausted at10/10 integrated attempts; no repair, new candidate, Blender run or further integrated attempt is authorized. Retain accepted27 brows in both production variants as directed by root; this audit makes no new whole-model or hair-naturalness acceptance claim. Reviewer performed only source/data reads and wrote this report, with no source mutation or native process.

## Bound final failure

`candidate30-source/first-strand-failure.json` SHA256: `d6a887d199a7b6d5662ecde3576c9f845b50be3c6d455e54b5deb379f0788792`. `candidate30-source/result.json` SHA256: `3d5982e92c1ad4c63f55d1077680d22b2f87ccd56d4ea9707df50903b9cee643`. All37 recorded source/input bindings independently rehash without mismatch. Runtime core is `02747395c9b6b9807e03db4b97b3afaebd1caae1caff6bfd5c2f655ff3d15fff`, builder `0be6573f8b3dc7aec0d39c7b5bcc4931017792c298493f8085e8162f15350431`, and manifest `8c690c9db36a3aadfcc26dfdfcc5c6a4a1b0e8fd6a374a3a7341b91a2846d479`. Accepted27 input remains bound to `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`.

The first failure is left strand2350 after exactly2,350 completed paths: sample0.20577137532772605, parameter−0.8267668125666128, `long=True`, `fringe=False`, requested tip height1.551215234813953 m. It raises `Surface integration step budget exhausted` inside march. There are901 exact-float32 construction points and900 certificates, length0.36320150240793175 m below the0.5 m travel limit, and no completion event. Release occurred on segment91 at length0.12203771992975777 m. Actual emitted radii are empty because the failed strand never reached emission or final stored-path checks. The result reports input/production/source unchanged, has no saved-scene entry, and no provisional blend exists. Root reports PID48164 exited1 and was closed after40.997 seconds; receipt internal duration is37.9083786 seconds.

## Confirmed guard-scope regression

The old `adaptive_shape` checks75-degree turns only after the path first overlaps the lower zone. Actual support bounds are `[1.299999976158142,1.472693078994751]` metres. Every point of this failed path is above that ceiling: minimum height1.5267976522445679 m. The v4 terminal helper/caller instead impose their75-degree capture restriction globally, without testing that zone. This extends the behavioral restriction to a region where the unchanged final adaptive guard imposes no such angle limit.

Using each recorded start distance and conservative construction certificate, I recomputed the old center-capture predicates along the released path. The first qualifying point is120:

| Measurement | Value |
| --- | ---: |
| Distance to original float32 center | 1.4960716994941291 mm |
| Incoming-to-center turn | 79.28055253438934° |
| Conservative body bound | 2.4469469451188983 mm |
| Required physical margin at this height | 0.010 mm |
| Conservative ear reserve | 0.0040118876476855515 mm |
| Total travel after old center capture | 0.12978630851203493 m |

The selected original goal is exterior and all-hard-valid. Start exterior is enforced by the march before these recorded advancing certificates. The old predicate therefore permits this center chord from the stored measurements, while v4's helper returns `None`. Its unchanged ball is extremely small:0.030138173395823716 mm, limited by the ear hard reserve0.030438173395823716 mm. At point120 its angular half-width is1.1542942446376976 degrees, so the nearest ball ray remains78.12625828975165 degrees from the incoming direction; there is no ray in the new open75-degree cone at that state. Subsequent ordinary motion does not reach the ball: the entire recorded polyline's nearest point is on segment121 at distance1.4699644205608097 mm, well outside its0.030138173395823716 mm radius.

I executed the exact unchanged `adaptive_shape` function on the stored prefix through point120 plus the original center. It passes and reports no lower-zone segments/turns (`maximum_lower_turn_degrees=0.0`, `minimum_lower_segment_m=None`). Eleven recorded released starts satisfy the old center bounds; the new global angle restriction blocks these local opportunities. This is concrete counterevidence to treating the capture change as behavior-preserving across all regions.

Candidate29's retained failure record establishes that its run completed6,524 paths, including this earlier strand index, with the same builder/seed. That is consistent with the source/data replay above. No candidate29 path archive for strand2350 was available for direct point-array comparison, and I did not rerun it; the detailed old-capture conclusion is a pure stored-data/source reconstruction, not a new native trajectory proof.

The previous13 bounded cases and exact-prefix checks passed honestly, but did not cover this upper-zone distinction. My positive source review verified the narrow branch mechanics and those regressions without identifying the broader zone restriction as a full-population regression risk. The final failed run supersedes any inference that those probes were sufficient for full-groom completion.

## Closeout

Preserve candidate30 failure/source/process evidence alongside candidate29 and earlier failures. No provisional hair result from30 exists to promote, and no complete23,000-strand, save/reopen or six-view appearance acceptance was obtained. Accepted27 brow work remains the retained production result under root's separate verification; the requested complete hair result remains unmet. No fix or follow-on experiment is proposed or executed in this exhausted round.


## Findings and disposition

Root rejects the final groom. The added capture-angle predicate applied to upper-fringe paths beyond the old lower-zone turn check, creating a scope regression that the thirteen bounded cases missed. The old safe-capture reconstruction is evidence about the recorded source/path, not a newly rerun full groom. No repair or further attempt is made after the round's ten-attempt limit.

## Verification

Candidate30 retains exact source/input/production hashes, the complete failed path and plans, and its closed owned-process receipt. No provisional model or new native render exists. Candidate27 relaxed brows and both delivered variants retain separate completed source, saved-geometry, native visual and independent review evidence.

## Round outcome

Round3 closed at ten of ten. Accepted brows are retained; full face/hair naturalness remains open. All work intended for Git delivery is merged and pushed by root; experimental source and failure evidence remain in ignored outputs, with no active repair process.

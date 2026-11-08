# Review 30: implementation

## Target

Transported-material mouth instrument and its second saved-scene runner, including the retained failure of the POINT-attribute influence mask. No face geometry or tolerance changes.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. The authored report reviews exact source, mathematical bounds, positive and negative controls and the failed actual-scene receipt. Root owns Blender execution.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 ab1073ae2ab3f5da353cb1e50735046806a2dee764d62948632dba22672a373c.

# Independent review of the transported-material face instrument

Reviewed 2026-11-08. This report reviews the exact second instrument revision and its failed root-owned measurement. It preserves `face-source.md` and `face-instrument.md`. No new shape or coordinate delta was proposed here; no Blender, render, installation, production edit or GUI was run by this reviewer. Read-only pure Python controls were permitted and used.

## Decision

The material-correspondence definition and its continuous real-arithmetic bounds are coherent for the fixed, traced evaluated lip-rail topology. They address the fixed-world-X transport defect without increasing the 50 micrometre allowance or dropping terminal alternatives. The six analytic controls pass, and my two earlier gap-preserving transport counterexamples now pass with zero measured increase and a 1 nm guarded upper bound.

The frozen runner is nevertheless blocked: its generic point-attribute influence mask misses 1,972 actually changed evaluated vertices, including oral anchors 520, 523, 537 and 540. Its fail-closed check correctly stops before aperture measurement. There is no actual material-aperture verdict, actual no-op/transport success or completed structure result from this run. Do not render under this result. A corrected influence construction must be reviewed and evaluated separately; the failure must remain preserved.

## Exact reviewed artifacts

Paths are relative to `C:/Users/38909/Documents/github/blender_scenes`.

| Artifact | SHA256 |
| --- | --- |
| `outputs/character-round3-20261108/face-form/probe_saved_candidate10_material.py` | `7fe9099935a14defa986a15ba4a179bcf7abff769d5cd401fdca34d2bc064717` |
| `outputs/character-round3-20261108/face-form/material_aperture.py` | `3c6543c722fe41860b3be96910c300e363daabca980aa9445804483b872bf01e` |
| `outputs/character-round3-20261108/face-form/material-arithmetic-checks.json` | `f4510fb173886c92810793b197fd53be8dee2eaa86fc86d1d8f41815b25106bc` |
| `outputs/character-round3-20261108/face-material-probe/saved-candidate10-material-measurement.json` | `513f03c00bddc00795edff418dd113f88a37066d1def28609e26024a83c575d4` |

The source-input receipt, original 512-row coordinate field, saved candidate-10 blend, original mouth verifier and reused eye/lash functions retain the identities recorded in `face-instrument.md`. The new runner pins the material module hash and retains the original pre-smile neutral and complete 642-row cumulative source union. This review does not replace those original artifacts with a new baseline.

## FACE-MAT-1 â€” A generic interpolated attribute is not the complete geometry influence mask

Priority: P1, blocks the current runner and appearance rendering. `probe_saved_candidate10_material.py:88-107` sets a scalar POINT attribute to one at the 642 changed source rows and treats positive evaluated attribute values as the complete positional influence support. `:109-118` independently compares the actual evaluated positions and checks that every changed row belongs to that support. That assertion fails on the real scene.

The receipt reports 11,358 marker-positive evaluated rows, minimum positive weight 0.0625, and 13,266 cumulatively changed evaluated rows. The actual set difference contains 1,972 rows; it is not merely the difference between those two population counts. In particular, 520/523/537/540 are missing. These are direct counterexamples to using this attribute interpolation as a geometry-stencil support proof. Different generic-attribute and Catmull-Clark/limit-position interpolation is a plausible explanation, but the exact Blender mechanism was not independently isolated in this review.

Required disposition: derive a conservative positional-influence population from the actual geometry construction/topology or validated positional stencils, and keep the assertion that every actual changed evaluated vertex belongs to it. Retain the missing-row evidence and include explicit oral-anchor controls. Do not discard the missing rows, lower a positivity cutoff, union them in silently and continue calling the original marker a complete independent proof, or suppress the assertion. An observed-change union can be useful additional coverage, but must be named and checked as such.

The later structure expansion at `:161-168` is a sensible way to use a valid influence superset: retain the old oral/corner population, add every polygon incident to influenced vertices, and add descendants of neighboring source faces. It preserves the original coverage, area/orientation, nonadjacent intersection and central-gap assertions. It has not executed successfully in this revision because its prerequisite influence mask is invalid. Coverage of all changed vertices also does not alone prove collision coverage against arbitrary distant unchanged surfaces; retain the scope of the old local surface checks and separately verify required complete body/groom interactions.

## Material correspondence assessment

`material_aperture.py:87-121` enumerates every pair of upper/lower neutral evaluated edges whose X projections overlap. It computes the neutral edge interpolation weights once and transports those same material weights to the same evaluated edge identities in the proposal. It does not choose a new nearest partner after inspecting the proposal or select only a favorable terminal branch. Relative X displacement between the two transported points contributes to the three-dimensional scalar distance. Thus common translation or common lateral transport is distinguished from relative lip separation.

For two nonvertical edges, the common neutral-X overlap is an interval, and both separation vectors are affine functions of its parameter. If only one edge is vertical in X, the entire material interval on that edge is retained. If both are vertical, the full two-parameter material box is retained. Degenerate point overlaps and the shared topological terminal remain explicit (`:93-117`). The module enumerates all edge pairs at both depths and checks coverage of the entire neutral common-X domain (`:124-149`). This resolves the previous design's dropped/unsupported branch alternatives at the algorithm level. It must still pass the actual scene's no-op and transported-rail controls.

This is a physically meaningful bounded material-separation contract for the retained topology: the same opposing parts of the neutral rails are compared after deformation. It is not the rejected fixed-world-X occupancy measurement, and is not a general proof about arbitrary remeshing, new disconnected lip spans, every rail point outside the neutral common-X domain, or all possible rendered cavity exposure. The runner still requires actual traced topology/anchor identity and separate structure checks. Those restrictions are part of the contract, not optional qualifications after a pass.

## Continuous bound mathematics

I checked `continuous_change` at `material_aperture.py:38-85` independently of the dense-sampling receipt. Let `a(q)` and `b(q)` be old/new separation vectors over one parameter box. They are affine. The desired scalar increase is `norm(b(q)) - norm(a(q))`.

- The maximum of each convex norm over a box is bounded by its maximum at the box corners.
- The old norm is bounded below by `max(0, norm(a(center)) - max_corner norm(a(corner)-a(center)))`, from the triangle inequality and affine convexity.
- Consequently `max_corner norm(b) - lower_old_norm` is a valid upper bound on scalar increase.
- Independently, the reverse triangle inequality gives scalar increase at most `norm(b-a)`; its maximum is also at a box corner. Taking the smaller of these two upper bounds is sound.
- Proposed-minus-neutral vertical separation is affine, so its maximum is at a box corner. Subdivision is not needed for that bound.

The branch-and-bound loop refines only potentially decisive boxes. A lower witness at or above the unchanged 50 micrometre threshold rejects the proposal; an upper bound below it can pass; hitting the resolution/box budget without resolving the threshold does not pass. The 1 nm numerical guard is added outward to scalar and vertical upper bounds, making the decision more conservative. The code labels this real-arithmetic reasoning with a floating-point guard, not a formal interval-arithmetic proof. I found no algebraic under-bound in the reviewed affine cases. This conclusion is for the scene's small finite coordinate scale, not an unlimited guarantee for arbitrary huge floating-point inputs.

The two-dimensional corner ordering and affine consistency assertion at `:46-49` match the vertical-edge `(u,l)` boxes produced by `edge_pair`. Every reported continuous record uses the same endpoints/weights in old and new states. Interior maxima are not reduced to endpoint-only sampling.

## Independent controls and supplied arithmetic evidence

I executed the module in memory with bytecode writing disabled and ran all six analytic controls: interior norm maximum, both-vertical alternatives, a true vertical opening, shared corner, common translation and common width. All passed. I then reused the mirrored closed-rail counterexample from `face-instrument.md` with two nonuniform interior stations. Exact no-op, rigid +1 mm X translation and shared +0.9% X-width transport each return zero scalar/vertical increase, a 1 nm scalar/vertical upper bound, no unresolved boxes and a pass. This directly repairs the previous false rejection, rather than testing a new easier fixture.

Single-point threshold probes confirm conservative boundary behavior: 49.998 micrometres passes with a 49.999 micrometre guarded upper bound; 49.999 micrometres does not pass because its guarded upper reaches exactly 50; exactly 50 and 50.001 micrometres fail. No tolerance was enlarged.

I also inspected `test_material_aperture.py` and its supplied receipt. Its 80 seeded one-/two-dimensional affine cases independently evaluate 68,880 interior samples using a direct expression rather than the module's affine interpolation helper. Every sample is below the reported continuous upper bound, and sampled scalar/vertical values respect the strict limit whenever the bound reports a pass. These finite tests support the implementation; they do not replace the mathematical inequalities or certify a Blender result. The receipt binds the test script as `f93a0e7b989b1a01b35d4e031993906c4167278f352639f7370e0eb57176cbf7` and the material module to the reviewed hash.

## Prior finding dispositions and runtime limits

FACE-INST-1: the source-level transport defect is addressed by fixed neutral material correspondence, with direct counterexample evidence. Actual aperture acceptance remains pending because this runner stops first.

FACE-INST-2: the source-level omission of terminal/vertical alternatives is addressed by exhaustive neutral edge-pair intervals/boxes. The runner now requires `mouth_no_op.material_bound_pass` and real-rail common-translation/common-width controls at `probe_saved_candidate10_material.py:122-137`. None of those actual controls ran after the current influence failure, so actual-scene resolution remains pending.

FACE-INST-3: unresolved in the exact current runner; FACE-MAT-1 identifies the new prerequisite failure. The coverage assertion is retained and correctly rejects its incomplete instrument population. A repaired topology/stencil construction and completed actual structure run are still required.

The root-produced receipt has `status: diagnostic_failed` and error `Actual evaluated movement outside complete source-derived influence.` It reports restored original source mesh and mouth contract, cleaned temporary datablocks and unchanged saved blend. No mouth, ocular or complete surface result from this second run is inferred from the earlier run. The earlier bounded ocular result remains separate evidence for the unchanged field, not proof that this failed invocation completed it.

The face-only scheduling clarification in `face-instrument.md` remains in force: exact unchanged complete candidate-10 hair may retain its openly rejected inherited lower-hair defects, but no new skin/groom intersections may be introduced, and final full-groom requirements are not waived. This instrument does not implement those complete groom checks.

Only this authored report was written by this review. All reviewer-owned pure Python commands completed normally; no Blender, browser, GUI or server process was started. Later runner revisions require their own exact source identity and result review; the failed bytes and raw receipt above must remain recoverable.


## Findings and disposition

Accepted the instrument defect finding. Preserved the failed runner and receipt, replaced the POINT mask with a separately reviewed conservative source-topology superset, and reran the unchanged face proposal. The later result is recorded separately; this failed revision is not reclassified as a pass.

## Verification

Reviewed material-control mathematics and actual failed POINT-marker receipt. The native run stopped before aperture measurement; the later topology correction is reviewed separately.

## Round outcome

Rejected this runner pending positional influence repair. No render authorized by this revision.

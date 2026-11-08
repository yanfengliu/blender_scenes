# Review 50: implementation

## Target

Complete candidate-28 groom builder, saved/reopened shaft and brow checks, and six-view renderer.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh. Root owns launch and acceptance.

## Reports

Complete authored report, SHA-256 `64645b95b868d520e6abe53e4442277c917962f5455ffb7cf24acb10310729a0`.

# Candidate28 full bundle: independent exact-source review

Decision: no remaining blocking source finding in the final bundle. The root-owned candidate28 experiment may proceed with the accepted candidate27 input and the exact bindings below. This is permission to run and inspect the full experiment, not a full-population geometry pass, visual acceptance, or a claim that startup cannot fail in Blender. No Blender/GPU job was launched by this reviewer. Only this report was written; source was read only.

## Exact reviewed bundle

Folder: `outputs/character-round3-20261108/surface-full-candidate28/`, to be frozen at the same directory depth for execution. The initially reviewed source manifest was SHA-256 `7694f5512da237b639e51c172f663f66d89a3ba6b830ff1b7e02c801ca69af50`. The final manifest after the reviewed dependency-only correction is `f819a02033b0110f1fd8ac60bc5a9cf9b3d20534bceb47a5fc6a0e347d594775`; all 8 local and 23 external bindings were independently verified against disk.

- `run_full_surface_groom.py`: `4029833828b7511513c1b393b265bd1524fd41023e1c5dc7abdea5551ea5428b`.
- `build_surface_groom.py`: `0441e36b3d82df1cd361c44ed9ad5b7fb10732a671044a4c78156c32b087bb74`.
- `brow_hair_clearance.py`: `73ad537cb48a64d25401982a98727d8e926184d80d7ae785753857cd0f44cdd9`.
- `render_candidate28.py`: `e867e7276640a162f5caee202c676c531d1268caf298f0179ebd061b5689fc58`.
- `surface_groom_core.py`: `91e3d1b23f2ed25b7e13bd4403596d7fe43894ab720a1ab7aaa825bc80d71c78`.
- `outer_ear_support.py`: `f3af019d4ad9416348129388c8cd9ee1167a17f83a36025e23f2b93fa29cbea2`.
- `support_envelope.py`: `6faf8fc7961656980426becc39de533cc442ef9fd553ade95b1790938ff97cc2`.
- `check_full_builder.py`: `dba5f5a6450255b0b688a2b74f156d90706741eb770dd190a252e59dc90f32e3`.

Default input is accepted `candidate27-source/provisional.blend`, independently hashed as `1db32dcf5f00d2a36d2c1023ba6858290a861c9db0640a1c313fe135558accf2`. Candidate10 remains the pinned source/assets and camera/lighting benchmark, with blend SHA `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. Runtime brow source edits are not used to reconstruct or replace that accepted input. Primary and WORK scene Python hashes are captured at launch and must remain unchanged through completion. This decision assumes the reviewed default candidate27 input; a different explicit input would change the target under review.

## Binding finding resolved during review

H28-1: the initially pinned WORK `check_realistic_character.py` transitively imports four local tools absent from the manifest. The reviewer identified this startup/immutability gap, read the imports and sources, and independently checked their current hashes. The author changed the source manifest only to add:

- `verify_reference_smile.py`: `235cf8e41c676394abe80c5bd6c157ca44962ae398766708395a4b3b48cc5df4`.
- `check_relaxed_brows.py`: `fd7029ce3643447fa2822a0c8710716707b355e8a25112a3301b2455112308fa`.
- `brow_uv_checks.py`: `495f3ec0de82524c11f31c6a9b947ff81c09bc88759ec2d6fd2ae0606a7f95fa`.
- `triangle_clearance.py`: `e0bb92aa2f30025c1a997c76e076a0fe47def24116cdd526e4483d8c5f0744db`.

All source bytes remained unchanged. The final f819a020 manifest includes those pins, and the driver's before/after source checks and renderer's source checks now cover them. H28-1 is fixed and independently verified. Importing the generic scene checker does import these tools and changes Python search-path ordering, but the reviewed growth modules and frozen candidate10 hair functions are already loaded, and the relevant imports resolve to existing pinned files. Their unrelated validation functions do not run merely through import.

## Full construction and physical guards

The driver wires the previously reviewed mechanism correctly at `run_full_surface_groom.py:107-115`: a separate original `physical_query`, an `OuterEarQuery` wrapping it for construction, and a brow guard created from the actual accepted scene are passed explicitly to the full builder. `build_surface_groom.py:118-174` uses only the construction wrapper for `march`; root attachment and entire stored-shaft verification use the original physical query. The lower verifier still independently checks actual body/clothing BVHs. No support-plane field is presented as body geometry or substituted for Euclidean physical distance.

The three growth/helper source files are byte-identical to the actual eleven-path pass, whose receipt SHA is `cb1da67b6c22d8e1798b374f65ba1704097d8153d936bdd8a66aae23cd1dfd4a`. This review independently inspected all eleven passing rows and true source/input/failure/object immutability flags. All long cases actually reached a terminal ball; the original fringe case reached its scalp sphere. Maximum reported root distance was 0.119935430121 mm and the largest lower turn was 53.124580744 degrees in the thin-goal case. This evidence supports the mechanism, not the entire population.

Population remains exactly 11,425 left, 11,425 right and 150 loose strands, with the original seed, strand specifications, actual radius distribution, material weighting and arclength taper. Every emitted path must contain 2..901 POLY points, preserve its already-rounded float32 coordinates exactly, and satisfy nondegeneracy, unchanged 75-degree lower turns and the original local head repair guard. Any required nonzero repair fails rather than silently moving a certified strand.

The added `anatomical_root_distance` at `build_surface_groom.py:27` requires exactly one body support, finite nonnegative body distance at most 0.3 mm and body exterior status. Near clothing cannot conceal a detached body root. Every actual emitted segment then receives the fresh whole-support proof using its maximum actual endpoint radius, and the inherited lower checks retain 5 mm guide and 1.5 mm physical shaft margins. The strict stored-float travel and terminal integration guards are inherited unchanged from the actually validated core.

The first failing strand raises after preserving its specification, points, available construction certificate, actual radii, terminal plan, completion/length and any brow witness. Completed-path counts advance only after all physical checks. There is no `continue` fallback or strand omission. Exact final counts, all three actual coverage guards, face and ear checks and brow segment accounting must pass before `build` returns. The imported face/ear checks still raise on collisions rather than returning an unchecked failed dictionary.

## New whole-brow/whole-hair capsule proof

`brow_hair_clearance.py:24-60` evaluates the complete actual `Eyebrows` mesh with render-enabled modifiers and render subdivision levels, restoring temporary modifier settings afterward. It includes all evaluated triangles without an alpha, region or sampled-vertex exclusion. Geometry is fingerprinted from all evaluated world vertices and triangle identities.

Every successfully emitted strand passes all its actual stored segment endpoints and actual radii to this guard. For each segment, a radius-expanded whole-segment AABB can prove separation from the complete brow AABB; otherwise the pinned capsule helper recursively proves the entire max-endpoint-radius capsule clear of the actual triangle BVH. Its midpoint unsigned-distance lower bound subtracts half segment length, query-coordinate quantization, actual radius and a 0.1 micrometre reserve. Unresolved node/depth branches reject. This is a whole swept-shaft proof, not endpoint or centerline-only sampling. It is explicitly unsigned separation from the brow surface and does not invent a nearest-normal inside classification.

The guard counts every path and segment. Its final receipt requires path and segment totals to match the complete builder and requires every segment to belong to exactly one certified category. It re-evaluates the current brow geometry and requires the same fingerprint. Empty brows, malformed radii, insufficient proof, changed brow geometry or incomplete accounting all fail. The accepted candidate27 brows are therefore preserved and checked against the newly emitted hair, rather than relying on candidate27's inherited old-hair clearance result.

## Save, reopen and renderer contract

`run_full_surface_groom.py:116-138` compares nonhair membership, geometry/settings, transforms, materials and scene state with the pinned candidate27 input, binds all stored coordinates, point counts and full hair render state, checks the deadline, then saves. It immediately reopens that saved file and recomputes the same hair bindings and nonhair/material/scene comparisons. The existing brow guard stores pure coordinate/triangle data and a bpy module reference, not an old live eyebrow RNA object; its post-reopen `receipt` looks up the new `Eyebrows` object and re-evaluates it. Thus the reopen check does not accidentally read deleted old-scene object references. Only after these checks does the receipt set `saved_geometry_exact` and geometry-pass status.

The full hair fingerprint binds object/curve/spline settings, matrices, materials, every point's homogeneous coordinates, radius and tilt, and rejects unsupported animation/modifier/parent/bevel/taper states. Exact binding after reopen ensures the emitted physical proof belongs to the saved curves rather than a dense construction precursor. Source/input/production immutability can still downgrade the receipt to failure after saving; a provisional file's existence is never evidence of success.

The candidate28 renderer checks candidate number, geometry/brow completion, full counts, reopened-save binding, all source hashes, saved-scene bytes and input bytes before rendering. It compares nonhair state against accepted candidate27, and separately compares the fixed camera/render/light/world benchmark against candidate10. It uses the four fixed native views and the retained oblique and seeded random views, requires OptiX, preserves existing output, binds each rendered file and removes its temporary cameras in `finally`. Its output remains `rendered_pending_visual_review`; no automatic appearance approval is introduced.

## Independently executed checks and limits

The complete pure `check_full_builder.py` controls were rerun in memory with bytecode writing disabled and their output-writing tail omitted. Eight anatomical-root cases passed expected outcomes. Eight exact imported capsule/AABB controls passed for clear, crossing, touching, unresolved node/depth, two-sided surface, disjoint box and radius expansion cases. The actual BrowHairClearance wrapper rejected a maximum-endpoint-radius collision and accounted for a clear segment. The source-identity and exact 23,000-population controls passed. AST parsing passed for all bundle Python and the four additional bound imports. All final manifest paths exist and hashes match; the default scene and diagnostic receipts match their pins. No startup binding mismatch was found.

Blender execution, full geometry, native rendering and appearance were not run by this reviewer. The eleven-path receipt is not a performance or full-population guarantee. Startup assertions occur before the driver's guarded build body, so a failed startup may produce no result.json; root must still record that process outcome in its attempt ledger as required. No permission to retry without accounting, omit a strand or weaken a guard follows from this source review.

Retained limitations remain relevant: finite coverage scans cannot certify naturalness; the legacy fringe retention receipt samples 80% of point indices while taper construction is by arclength; invalid-goal projection costs can be visually consequential; and full candidate28 must still expose actual terminal/projection counts, complete geometry receipts and all six native views for judgment. The final source decision is to run one concrete, reviewable experiment, not to accept its result in advance.


## Findings and disposition

The transitive source-binding gap was fixed and independently rechecked before launch. Root accepted the exact source for one full experiment. Candidate 28 then failed after 2,391 completed paths because one strand exhausted the integration step budget; no scene or render was saved. No source, input or production geometry was modified. The failure and every recorded point are retained for bounded diagnosis.

## Verification

Owned Blender PID 42784 exited with failure and its process tree closed after 39.7759 seconds. Raw source, result and first-strand failure are retained under `outputs/character-round3-20261108/candidate28-source`.

## Round outcome

Eight integrated attempts used, two remain, next 29. The accepted candidate-27 brow runtime is merged and pushed as `91d2132f7e6700099644ee283c583eccfdea2055`; the exact revision has no GitHub Actions runs. Hair remains unaccepted.

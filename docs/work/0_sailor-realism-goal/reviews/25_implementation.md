# Review 25: implementation

## Target

Bounded adaptive fixed-cell certificate diagnostic based on 0032b5963128707ad23044b18000efc4fdfe828c. All exact source, mathematical controls, actual receipts and authored report remain in outputs/character-round2-20261107/hair-attempt19-diagnosis; archive-manifest.json SHA256 1c885d218eba5eeb1e4faf68ebe2b4307a14f45bd43936596be5a0ea020202a7. Executed attempt 19 remains separate and unchanged. No production code or integrated candidate is part of this diagnostic.

## Reviewers and coverage

Independent Codex reviewer, Astra xhigh, inspected exact source and supplied evidence. Root owns actual execution and acceptance. No reviewer-run Blender or native appearance judgment is claimed.

## Reports

### Independent Codex reviewer, Astra xhigh

The complete authored report follows, SHA256 55282040ecb405e3136cc88f268e0a2bde928038fcd9fbfcd762960770c65e0b.

# Independent fixed-cell certificate review

## Scope and decision

Reviewed 2026-11-08 against the exact attempt19 diagnosis sources and retained result below. This is a read-only review of the failed fixed cell from side 0, guides 26/27, points 100–101, and of the proposed bounded containing-ball certificate. No Blender, groom construction, render, scene save, production edit or additional agent was launched by this reviewer. I independently ran the pure mathematical controls with bundled Python and bytecode writing disabled, and independently recomputed the successful receipt's ball arithmetic. The actual Blender observations are from the root/worker-run receipts, not a reviewer runtime.

Decision: the source and bounded evidence support using this certificate for wholly fixed cells in the forthcoming attempt20 source proposal. I found no material blocker in this exact helper for that role. The existing cell is now positively certified against the unchanged complete body and clothing supports, rather than merely having clear sampled vertices. This does not approve attempt20's source, run, full groom, appearance or a broader relaxation of physical requirements. Fresh complete source review remains required before the last full attempt.

## Exact targets

All paths in this table are relative to this report's directory, `outputs/round2-hair-search/attempt19-diagnosis`, in the isolated `character-naturalness-round2` worktree. Hashes were independently read from current bytes; every file recorded in the executed result's source map still matched its recorded hash at review time.

| Target | SHA256 |
| --- | --- |
| `adaptive_ball.py` | `04bf5807480d3c157c853f26220e33de3fb9fb77f0e66ae59563e027dc5a1da3` |
| `probe.py` | `434883efca5cea43f12ab65fe1c1c003f9fbd61ef45930a62945931c0c61f614` |
| `mathematical_controls.py` | `fdb0c508af07cb0c0244a5507a442d4b9cd810afd23574faf330354ac12d2217` |
| `run.py` | `336e5ba72539cdae738a02e12fff2e0d2361076b11844f4087e22e7b2ef3917a` |
| `source-sha256.json` | `9ad206df4e1c7bedfa1859934573b55600695545e71f6eeece436102bab4d02e` |
| `result.json` | `0bbb4e06f0512f1d3889458ce4a4803e126850bff7e5e2234fd2f5dc646f6dc1` |
| `process.json` | `142713130d8269d2a1589cbf82928f05b57a9c3b5fade477777d219494652cdd` |
| `mathematical-controls.json` | `fdd4efd20dbfecdc8a19d625745b6cb6792e423f874274498da2d17580c8190b` |
| `handoff.md` | `ebcbde587f04191ff010d5ea8ca5fdc54fa3b1a86596fed7cc16b11c09e5b3cc` |

The executed input is frozen candidate10 `sailor_character.blend`, SHA256 `eb03703745ab5c88c378f1babb7a2ea4dd965da4fddec6289ab6bc6af4911f41`. The evaluated complete body and clothing hashes are respectively `7a132a535cf7bc2b40cad40f3619d9eff4893df2e0e3f37f72981700828ec1ce` and `96769a86d72d36623113b370ffa128b44da1d582226f1e8139d41e2008e79bb2`. `probe.py:27–39` binds the exact failed attempt19 activity, reconstructs the same clipped cell, and asserts the complete support hashes and clipped vertices agree with the original failure. Neither an altered cell nor a cropped replacement support is used to obtain the positive result.

## Mathematical and implementation assessment

The split in `adaptive_ball.py:10–25` preserves the parent convex hull as the union of its two children in real arithmetic. For midpoint m=(a+b)/2 and nonnegative parent coefficients alpha, if alpha_a >= alpha_b, replace b by m and use coefficients alpha_a-alpha_b at a and 2*alpha_b at m. Otherwise use the symmetric replacement of a. The coefficients stay nonnegative and retain their sum and represented point. Each child is itself inside the parent because its new midpoint is a convex combination. This argument does not require affinely independent vertices, a tetrahedron, or a particular choice of the pair; choosing the farthest pair is an efficiency choice.

The implementation starts each root with identity barycentric weights and zero coordinate errors. At the reviewed depth limit of 12, the generated root weights remain exact dyadic fractions. Every midpoint inherits half of each endpoint's coordinate-error allowance plus a conservative binary64 midpoint-arithmetic allowance. The containing radius includes the per-vertex error balls. Thus the finite-coordinate child hull is not silently substituted for the exact mathematical partition. The source also checks nonnegative normalized weights and agreement with root-coordinate reconstruction before accepting a node. This is a bounded metre-scale implementation, not a formal arbitrary-magnitude floating-point library.

For any exact cell point x inside a ball centered at c with radius R, distance(x, support) is at least distance(c, support)-R. `query_ball` additionally subtracts the actual displacement from c to the float32 `Vector` used for the BVH query, and a 0.1 micrometre reserve. It queries both complete trees and requires the resulting lower bounds to exceed the same 5.001 mm construction target. The body nearest-normal sign is checked before acceptance; this retains the existing oriented-body exterior test. This review does not establish a general inside/outside classifier for arbitrary non-manifold meshes or a formal bound on arbitrary BVH implementations.

The `certify` loop accepts only certified leaves. It retains both children after a split. Exhausting a node or depth budget produces `status: fail`, not a partly certified success; queued cells are retained in the failure receipt and the currently inspected cell remains in `nodes`. Zero-diameter cells either pass a direct ball test or explicitly fail. Malformed support queries propagate as instrument errors rather than being recast as ordinary geometric noncertification. The integration must consume the explicit status: this helper deliberately returns a failure report for `InsideCell` and `UncertifiedCell` rather than raising them to its caller.

## Actual bounded evidence and independent checks

The original vertex-anchored certificate still fails in the executed probe. The centroid ball also fails, with only 3.714101 mm certified body clearance. The successful anchor is the midpoint of clipped vertices 1 and 5, the farthest pair. I independently recomputed the radius and query displacement from the stored vertices and query center, without using the helper's arithmetic: radius 4.895709433825 mm; float32 query displacement 0.016747488381 micrometre. Subtracting both, and the 0.1 micrometre reserve, from the recorded actual nearest distances gives exactly 6.322769137183 mm body clearance and 91.533395150760 mm clothing clearance. These exceed 5.001 mm. The positive real cell used one node, one leaf and depth zero. It validates the improved root anchor, not real-body recursive subdivision performance.

The real negative with endpoints on opposite sides of the head is meaningful: both endpoints are exterior, 73.957473 mm from the body and over 176 mm from clothing, yet an actual body ray crosses at X=-74.162222 mm. The certificate rejects its convex interior as `InsideCell`. A separate small inside-head cell also fails. These prevent the specific false inference that sufficiently clear vertices prove a clear convex interior. They do not prove every possible topological or numerical edge case.

I independently reran `mathematical_controls.run_controls()` as an imported pure-Python function, avoiding its artifact-writing entry point. All 3,015 partition cases passed with maximum recorded discrepancy 4.440892098501e-16. The clear synthetic wide cell required genuine recursive work and passed with 111 nodes, 56 leaves and depth 6; minimum certified plane distance was 5.219569206 mm. A one-node budget failed with both child cells retained. Inside, malformed-support, duplicate clear-point and degenerate insufficient-clearance controls behaved as required. The exact-rational comparison of propagated coordinate errors passed through depth 12 on the selected alternating subdivision path. That rational control is a useful implementation check, not exhaustive enumeration of all trees.

The actual receipt reports `feasible_fixed_cell_only`, unchanged input and sources, and matching evaluated supports. The owned process receipt reports PID 5376, exit 0, closed true, no timeout and 10.005125 seconds under a 120-second deadline. The source launcher puts `close_owned_process(process, job)` in `finally`. These are inspected root/worker-run receipts. This reviewer created no Blender or GUI process and made no production or evidence-source changes.

## Conditions for the next source review

Keep this proof confined to wholly fixed clipped cells and require `status == 'pass'` at construction and final replay. Preserve the reviewed complete support construction, 5.001 mm target, positive numerical reserve and bounded node/depth settings. A certificate failure, invalid support or exhausted budget must remain a full failure; it must not become a cell skip or an eligibility exception.

Keep all final original-guide and float32 checks, clipped-vertex and C2 span constraints, actual stored guide 5 mm margins, actual stored child shaft-surface 1.5 mm margins to both body and clothing, original upper/turn/collapse/negative controls, immutable sources and exact saved-render binding. The fixed-cell proof covers the cell core only, so it cannot replace tests for offset children, shaft radii or the rendered groom.

The separately proposed original-reference-cell normal selection is a permissible sufficient-constraint construction choice in principle, provided it uses the same complete padded obstacle hull, final clipping heights, 5.001 mm target and outward condition, and retains all original constraints and final replay. It is not exercised by this diagnostic. Its concrete implementation must still be reviewed, including fallback/error handling. The 132 guides needing repair, all 23,000 stored children, the integrated saved scene and appearance remain unproven. Attempt19 remains a failed full attempt; this diagnostic does not change that historical disposition or authorize the final run by itself.


## Findings and disposition

| ID | Finding | Disposition and reason | Repair or follow-up |
|---|---|---|---|
| F33 | Vertex-anchored whole-cell balls fail to prove a physically clear fixed region. | Accepted as a conservative instrument limitation; a midpoint ball certifies the unchanged failed cell. | Bounded adaptive proof may replace fixed-cell fallback with strict success checking, numerical coverage and complete replay. |
| F21 | Complete actual guide/child proof remains open. | This evidence concerns one fixed cell, not the complete field. | Final attempt source review and full population checks remain required. |

## Verification

Reviewer independently reran 3,015 pure partition cases, exact-rational rounding coverage, synthetic subdivision and budget/inside/degenerate/invalid-support controls. The actual read-only diagnostic reproduces the original certificate failure and proves the unchanged cell at the root midpoint: 6.322769 mm body and 91.533395 mm clothing bounds after rounding and 0.1 micrometre reserve. Actual clear endpoints span a confirmed body ray crossing; the adaptive proof rejects its interior, and a separate inside negative rejects. PID 5376 exits 0 and closes after 10.005 seconds; all input and attempt 19 source hashes remain unchanged. No actual adaptive subdivision, complete groom, child, save or render is claimed.

## Round outcome

The bounded fixed-cell certificate change is supported for source preparation. Every leaf must pass unchanged limits, exhausted budgets must fail, and the final actual guide/shaft checks remain mandatory. This is not approval of a complete run or appearance; one substantive attempt remains.

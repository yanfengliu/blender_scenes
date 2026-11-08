# Relaxed eyebrows

The owner reported that the brows made the adult character look as though she was frowning. Candidate 27 removes the dark downward inner hooks by constructing the existing textured ribbons from their UV disks. It preserves the existing topology, texture, materials and all other scene geometry. Six native views and independent review accept the local expression improvement; the brows remain fine and groomed, and overall face/hair naturalness remains open.

`scenes/relaxed_brows.py` now supplies the production fit. `tools/check_relaxed_brows.py` validates the accepted coordinates, actual render-level disk geometry, exterior forehead attachment and continuous skin separation. The real production call reproduces all accepted body/brow coordinates and brow UVs exactly. The old folded geometry and deliberate fold, hook, buried and detached controls are rejected. The normal reopened scene checker includes the new brow check. Source checks do not replace native visual review.

Delivery verification and exact revision review are recorded in the work plan and review records. No gate exception is used.

Run the isolated regression in owned background Blender with `--python tools/check_relaxed_brows.py` on the saved scene, or add `-- --production` to exercise the actual main-scene anatomy/eye prefix. The full reopened checker also includes the brow gate.

Required gates pass: fleet 563/563 with no failures/skips, instruction sync 35 current, Python AST 41 files, official Blender Lab MCP build and all three native donut views. The first restricted test run failed on Windows Git Bash process access; the unchanged full suite passes with normal process permissions. No exception is used. Independent production review 49 reports no blockers.

The same accepted brows are also delivered in the earlier refined unclothed model. Native saved-copy verification preserves all anatomy and all ten retained materials; the sole save difference is a proven zero-user obsolete skin material. Root and independent review accept the 1200-pixel portrait. Both original and updated files remain intact.

Round 3 closes at the owner's ten-attempt limit. Final hair candidate 30 stops before saving on a 900-step strand budget, and all new hair experiments remain excluded from production. Face/hair naturalness remains open; the accepted deliverable is the local brow improvement.

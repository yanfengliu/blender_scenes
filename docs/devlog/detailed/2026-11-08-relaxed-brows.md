# Relaxed eyebrows

The owner reported that the brows made the adult character look as though she was frowning. Candidate 27 removes the dark downward inner hooks by constructing the existing textured ribbons from their UV disks. It preserves the existing topology, texture, materials and all other scene geometry. Six native views and independent review accept the local expression improvement; the brows remain fine and groomed, and overall face/hair naturalness remains open.

`scenes/relaxed_brows.py` now supplies the production fit. `tools/check_relaxed_brows.py` validates the accepted coordinates, actual render-level disk geometry, exterior forehead attachment and continuous skin separation. The real production call reproduces all accepted body/brow coordinates and brow UVs exactly. The old folded geometry and deliberate fold, hook, buried and detached controls are rejected. The normal reopened scene checker includes the new brow check. Source checks do not replace native visual review.

Delivery verification and exact revision review are recorded in the work plan and review records. No gate exception is used.

Run the isolated regression in owned background Blender with `--python tools/check_relaxed_brows.py` on the saved scene, or add `-- --production` to exercise the actual main-scene anatomy/eye prefix. The full reopened checker also includes the brow gate.

Required gates pass: fleet 563/563 with no failures/skips, instruction sync 35 current, Python AST 41 files, official Blender Lab MCP build and all three native donut views. The first restricted test run failed on Windows Git Bash process access; the unchanged full suite passes with normal process permissions. No exception is used. Independent production review 49 reports no blockers.

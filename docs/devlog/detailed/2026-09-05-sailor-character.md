# 2026-09-05 — Sailor character

Built an original static adult character from local procedural geometry, with three inspection cameras and a direct headless Blender runner.

Hero, portrait, and rear inspection exposed calf penetration through initially straight socks, upper-thigh penetration through the skirt, floating collar braid, and separate thumb roots after subdivision.
Socks now follow the posed leg paths, the skirt provides more clearance, and collar trim follows the cloth edge.
Thumb roots extend into the palms before voxel remeshing; scene construction now rejects any disconnected component in either complete arm and hand mesh.
The connectivity check covers the generated posed arms; it does not certify arbitrary edits, clothing clearance, or anatomy, which still require visual inspection.

The result remains editable as named meshes, curves, and materials, with no animation rig or external assets.
The runner owns its hidden Blender process and descendants and removes successful build scratch files and logs.

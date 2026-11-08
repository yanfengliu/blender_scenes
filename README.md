# Blender scenes

## Reference-led sailor character rebuild

The latest editable draft is `outputs/sailor_character_realism_goal/candidate-10/sailor_character.blend`, with native hero, portrait, profile, back, fixed face-oblique and seeded torso views beside it. It narrows the upper frame, softens the lip/lower-cheek geometry, and closes the sparse fringe/temple gaps. Root and independent six-view review still reject the final appearance: the face remains mannequin-like and the hair has a broad helmet silhouette. All ten attempts in this round are used; the [current plan](docs/work/0_sailor-realism-goal/plan.md) records the incomplete result. Candidate 6 remains the preserved garment-repair baseline, and candidates 7�9 remain negative evidence.

Haru is an original adult woman intended to be age 20. Frozen references and prompts remain in `outputs/sailor_character_proportions/references/`; the separately approved leaner waist and fuller bust remain intact. Photographic likeness is still incomplete: smooth pale facial skin, mottled knees, straight curtain hair and stiff fitted cloth remain visibly CG. CHR-001 stays open. The earlier proportions candidate 2, refinement candidate 10, and realism candidates 1–5 remain preserved comparison evidence.

[scenes/sailor_character_realistic.py](scenes/sailor_character_realistic.py) uses an anatomical MakeHuman base, photographic UV skin, natural eye materials and 23,000 hair strands. `natural_face.py`, `gentle_expression.py`, `perioral_shape.py` and `lower_cheek.py` shape the face and materials; `natural_hair.py` uses `fitted_hair.py` and `hair_groom.py` for strand/material construction. `upper_frame.py` maps the finished body and clothing together, preserving forward bust depth and the fitted collar outline. `body_proportions.py` applies the smooth body/helper deformation, while `fitted_body_clearance.py` fits the thickened blouse against complete unculled anatomy. `fitted_blouse.py`, `fitted_collar.py` and `cloth_finish.py` provide connected clothing, sharp collar rim shading, bounded drape and the pocket. `relaxed_character_details.py` supplies the pose, fitted shoes and scarf. The saved model is statically posed with editable meshes/curves, packed image textures and no animation rig. Rebuilding requires `.tools/human_reference_assets`. The MakeHuman base and bundled assets are CC0; see the [official asset license](https://github.com/makehumancommunity/makehuman/blob/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.md).

Rebuild current source into a separate output folder, and use another folder for a face preview. Choose fresh folder names for later runs to preserve reviewed artifacts:

```powershell
.venv\Scripts\python.exe tools\build_sailor_character.py --scene scenes/sailor_character_realistic.py --output-dir outputs/sailor_character_realism_rebuild --views hero,portrait,profile,back --size 1600 --samples 128
.venv\Scripts\python.exe tools\build_sailor_character.py --scene scenes/sailor_character_realistic.py --output-dir outputs/sailor_character_realism_preview --views portrait --size 900 --samples 24
```

`--views` selects a comma-separated subset of `hero,portrait,back,profile` and overrides `--preview`; profile renders square and covers the head. Relative paths resolve against the runner's repository root. Choose a fresh output directory for every candidate so reviewed files are never overwritten. The saved scene is editable and its textures are packed.

The canonical reopened check is Blender `--background <saved.blend> --python-exit-code 1 --python tools/check_realistic_character.py`. The fuller saved check is `--python tools/check_character_finish.py -- --output <receipt.json>` with the same background Blender invocation; it measures complete unculled-body clothing and ornament clearance, a body-intrusion negative, and actual fringe/crown/temple coverage. `tools/check_expression_fit.py` exercises four production scenes for facial isolation and responsive torso fitting. `tools/check_character_shape.py` checks actual shoulder/eyelid response and independent smile inputs in background Blender. The pure-Python `tools/check_lip_contour.py` and `tools/check_lower_cheek.py` exercise production inputs and reject old/no-op controls. Each header documents its scope and invocation. Historical candidate 4/5/6 garment comparisons remain in `tools/check_garment_isolation.py`. These bounded checks do not establish attractive or natural appearance.

For frozen proportions candidate2 replay, create a new empty directory and copy the complete `outputs/sailor_character_proportions/candidate-2/source/scenes/` and `source/tools/` trees into its `scenes/` and `tools/` directories. Copy the required `.tools/human_reference_assets` tree into that new directory as well, and verify every copied source against that candidate's `source-manifest.json`. Invoke the copied `tools/build_sailor_character.py` with the existing absolute Python interpreter, `--scene scenes/sailor_character_realistic.py`, a fresh `--output-dir`, `--views hero,portrait,profile,back --size 1600 --samples 128`, and Blender 5.2. The copied runner sets its working directory to the new root. Passing only a frozen main file to the live runner is not an isolated replay because the main file imports helpers from the runner's working directory. Inspect and hash fresh renders; source identity does not transfer prior pixel approval.

## Rejected stylized sailor baseline

The original version below is retained as rejected comparison evidence: the user found the face creepy, the appearance insufficiently realistic, and the skin toy-like.

Haru is an original stylized adult woman, age 20, wearing a Japanese sailor-style uniform. The static posed figure has editable meshes, curves, and materials grouped by anatomy, face, hair, clothing, and studio. It has no animation rig and uses no external models, textures, or fonts.

Open `outputs/sailor_character/sailor_character.blend` in Blender; the hero camera is selected. The same folder contains `hero.png`, `portrait.png`, and `back.png` for full-body, face, and rear views. Generated scenes and renders stay local under ignored `outputs/`; reusable source lives in [scenes/sailor_character.py](scenes/sailor_character.py).

Rebuild from this repository in PowerShell with Blender 5.2 and Python:

```powershell
.venv\Scripts\python.exe tools\build_sailor_character.py
.venv\Scripts\python.exe tools\build_sailor_character.py --preview --size 800 --samples 24
```

The direct headless runner defaults to 80 Cycles samples and renders a 1280 × 1600 hero, 1200 × 1200 portrait, and 880 × 1100 back view. `--preview` rebuilds the scene and renders only `hero.png`; `--no-render` saves the scene without rendering. Use `--blender 'C:\path\to\blender.exe'` for another Blender installation. The runner closes its Blender process and descendants and removes successful build logs and scratch files.

## Strawberry donut

A procedural strawberry-glazed donut built and rendered through the **official Blender Lab MCP** in headless Blender 5.2.
The scene includes uneven fried dough with procedural pores, a pale proofing band, solid icing with drips, individual sugar sprinkles, a porcelain plate, linen, coffee, three cameras, and Cycles lighting.
All geometry and materials are editable, and no external textures or models are required.

## Open the result

Open `outputs/donut/strawberry_donut.blend` in Blender.
The hero camera is already selected; press **Numpad 0** for the camera view and **F12** to render.
The rendered images are `outputs/donut/hero.png`, `overhead.png`, and `detail.png`.
Generated `.blend` files and renders remain local under ignored `outputs/`; the small procedural source is tracked.
Follow the [repository retention rules](docs/policies/local-rules.md): retain reusable source, scripts, and documentation in Git, and remove completed debug/scratch artifacts after use.

## Rebuild headlessly on Windows

Requirements: Blender 5.2, Git, and [uv](https://docs.astral.sh/uv/getting-started/installation/).
This machine already has them.
From this repository in PowerShell:

```powershell
.\tools\setup_blender_mcp.ps1
.venv\Scripts\python.exe tools\build_donut_mcp.py
```

Use `--blender 'C:\path\to\blender.exe'` if Blender is installed elsewhere.
For a quick preview, append `--size 1100 --samples 40`.
The default is a 1500 × 1200 hero render at 96 samples, plus two 900 × 900 inspection renders.
The runner launches its own headless Blender instance on an available loopback port, connects an actual MCP client to `blender-mcp`, and calls `execute_blender_code` for both modeling and rendering.
It closes its Blender process and MCP stdio connection in cleanup, including when a request fails.
It does not attach to an already open Blender instance or modify user preferences.

The setup script pins Blender Lab MCP commit `4309a39646e644261624bfcd2bca669b343b7621` and MCP SDK `1.29.1`.
The upstream package currently allows MCP 2.x even though it imports the removed `mcp.server.fastmcp` API; the SDK pin avoids that verified startup failure.
Do not replace this setup with plain `uvx blender-mcp`: the similarly named community project is a different implementation.

## Connect Blender MCP to Codex for interactive editing

1. In Blender 5.2, open **Edit → Preferences → Get Extensions**, allow online access, and add `https://lab.blender.org/` as an extension repository. Install the **MCP** extension from Blender Lab.
2. In **Preferences → Add-ons**, expand **MCP**, set its host to `127.0.0.1` and port to `9876`, then select **Start MCP Bridge Server**. Keep this Blender instance open while using it.
3. In Codex, open **Settings → MCP servers → Add server**, select **STDIO**, name it `blender`, and use the executable installed by this project: `C:\Users\38909\Documents\github\blender_scenes\.venv\Scripts\blender-mcp.exe`. No command arguments are needed. Set `BLENDER_MCP_HOST=127.0.0.1` and `BLENDER_MCP_PORT=9876` in its environment.
4. Save and restart the MCP server. If the tool list in an existing task is not refreshed, reopen the task or start a new task. Ask it to inspect the current Blender scene before editing.

Equivalent entry to merge into your existing `C:\Users\38909\.codex\config.toml` (preserve its other settings):

```toml
[mcp_servers.blender]
command = 'C:\Users\38909\Documents\github\blender_scenes\.venv\Scripts\blender-mcp.exe'
startup_timeout_sec = 30
tool_timeout_sec = 300

[mcp_servers.blender.env]
BLENDER_MCP_HOST = '127.0.0.1'
BLENDER_MCP_PORT = '9876'
```

This configuration has been provided for you to apply; the automated build does not install the add-on into your interactive Blender or edit Codex's global configuration.
Stop the bridge using its add-on control when finished.

References: [Blender Lab MCP](https://www.blender.org/lab/mcp-server/), [official source and headless CLI](https://projects.blender.org/lab/blender_mcp), and [OpenAI MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

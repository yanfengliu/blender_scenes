# Blender scenes

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

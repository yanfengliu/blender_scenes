"""Load the official Blender Lab addon only in this owned Blender process."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.tools/blender_mcp/addon'))
import blender_mcp_addon

blender_mcp_addon.register()

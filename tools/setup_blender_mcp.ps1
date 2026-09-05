# Install the official Blender Lab MCP into this project, without global config changes.
$ErrorActionPreference = 'Stop'
$sceneRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $sceneRoot '.tools\blender_mcp'
$pythonExe = Join-Path $sceneRoot '.venv\Scripts\python.exe'
$sourceCommit = '4309a39646e644261624bfcd2bca669b343b7621'
$oldCache = $env:UV_CACHE_DIR
try {
    $env:UV_CACHE_DIR = Join-Path $sceneRoot '.tools\uv-cache'
    if (-not (Test-Path -LiteralPath $sourceDir)) {
        git clone https://projects.blender.org/lab/blender_mcp.git $sourceDir
        if ($LASTEXITCODE -ne 0) { throw 'Could not clone the official Blender Lab MCP repository.' }
        git -C $sourceDir checkout --detach $sourceCommit
        if ($LASTEXITCODE -ne 0) { throw 'Could not check out the verified Blender Lab MCP version.' }
    }
    $actualCommit = git -C $sourceDir rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $actualCommit -ne $sourceCommit) {
        throw "Expected Blender Lab MCP commit $sourceCommit at $sourceDir. Preserve any existing work and use that version."
    }
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        uv venv (Join-Path $sceneRoot '.venv') --python 3.13
        if ($LASTEXITCODE -ne 0) { throw 'Could not create the project Python 3.13 environment. Install uv first.' }
    }
    uv pip install --python $pythonExe (Join-Path $sourceDir 'mcp') 'mcp[cli]==1.29.1'
    if ($LASTEXITCODE -ne 0) { throw 'Could not install Blender Lab MCP and its compatible MCP SDK.' }
    Write-Output 'Ready. Run: .venv\Scripts\python.exe tools\build_donut_mcp.py'
} finally {
    $env:UV_CACHE_DIR = $oldCache
}

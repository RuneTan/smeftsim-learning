$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $projectRoot '.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'analyze_tutorial.py') @args
if ($LASTEXITCODE -ne 0) { throw "Analysis failed: exit code $LASTEXITCODE" }

$ErrorActionPreference = 'Stop'
$wslPath = 'C:\Program Files\WSL\wsl.exe'
if (-not (Test-Path -LiteralPath $wslPath)) { $wslPath = 'C:\Windows\System32\wsl.exe' }
& $wslPath -d SMEFTsim -u smeft --cd /home/smeft/smeftsim
if ($LASTEXITCODE -ne 0) { throw 'Cannot enter the project guest. Complete resume-install.ps1 first.' }

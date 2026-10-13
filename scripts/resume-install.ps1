$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$wslPath = 'C:\Program Files\WSL\wsl.exe'
if (-not (Test-Path -LiteralPath $wslPath)) { $wslPath = 'C:\Windows\System32\wsl.exe' }
$env:WSL_UTF8 = '1'
$logRoot = Join-Path $projectRoot 'outputs\installation'
$image = Join-Path $projectRoot 'vm\downloads\ubuntu22.04-rootfs.tar.gz'
$diskRoot = Join-Path $projectRoot 'vm\SMEFTsim'
$expectedHash = '1483cc5c1dce13064f774834cbffdff226559fd522a67a381a8ea77d63fb4109'
if ((Get-FileHash -LiteralPath $image -Algorithm SHA256).Hash.ToLower() -ne $expectedHash) {
    throw 'Ubuntu image hash mismatch.'
}
$distributions = @(& $wslPath --list --quiet)
if ($LASTEXITCODE -ne 0) { throw 'WSL is unavailable. Restart Windows after installing the runtime.' }
if ($distributions -notcontains 'SMEFTsim') {
    & $wslPath --import SMEFTsim $diskRoot $image --version 2 2>&1 | Tee-Object -FilePath (Join-Path $logRoot 'ubuntu-import.log')
    if ($LASTEXITCODE -ne 0) { throw 'Ubuntu import failed. Inspect ubuntu-import.log; a Windows restart may still be required.' }
} else {
    $registered = Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss' | Get-ItemProperty | Where-Object { $_.DistributionName -eq 'SMEFTsim' }
    if (-not $registered -or $registered.BasePath.Replace('\\?\','').TrimEnd('\') -ne $diskRoot.TrimEnd('\')) {
        throw 'A different SMEFTsim distribution exists; it will not be modified.'
    }
}
& $wslPath -d SMEFTsim -u root -- /bin/true
if ($LASTEXITCODE -ne 0) { throw 'The project guest cannot start. Restart Windows and retry.' }
$linuxSource = '/mnt/' + $projectRoot.Substring(0,1).ToLower() + $projectRoot.Substring(2).Replace('\','/')
& $wslPath -d SMEFTsim -u root -- bash ($linuxSource + '/scripts/bootstrap_guest.sh') $linuxSource 2>&1 | Tee-Object -FilePath (Join-Path $logRoot 'guest-setup.log')
if ($LASTEXITCODE -ne 0) { throw 'Guest setup failed; inspect guest-setup.log.' }
& $wslPath --terminate SMEFTsim
if ($LASTEXITCODE -ne 0) { throw 'Could not restart the project guest after configuration.' }
& $wslPath -d SMEFTsim -u smeft -- bash /home/smeft/smeftsim/scripts/validate_smoke.sh 2>&1 | Tee-Object -FilePath (Join-Path $logRoot 'guest-validation.log')
if ($LASTEXITCODE -ne 0) { throw 'Generation / reweighting validation failed; inspect guest-validation.log.' }
& $wslPath -d SMEFTsim -u smeft -- cp /home/smeft/smeftsim/outputs/smoke_validation.json ($linuxSource + '/outputs/installation/smoke_validation.json')
if ($LASTEXITCODE -ne 0) { throw 'Copying the validation report failed.' }
& $wslPath -d SMEFTsim -u smeft -- cp /home/smeft/smeftsim/work/Material/Hvlvl_SM/Events/smoke_sm_2000/unweighted_events.lhe.gz ($linuxSource + '/outputs/installation/smoke_sm_2000.lhe.gz')
if ($LASTEXITCODE -ne 0) { throw 'Copying the generated sample failed.' }
$rootAnalysis = @'
set -e
cd /home/smeft/smeftsim
source .venv/bin/activate
mkdir -p outputs/local_smoke_root
gzip -dc work/Material/Hvlvl_SM/Events/smoke_sm_2000/unweighted_events.lhe.gz > outputs/local_smoke_root/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/local_smoke_root/events.lhe outputs/local_smoke_root/Hvlvl_SM.root
cd outputs/local_smoke_root
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
'@
& $wslPath -d SMEFTsim -u smeft -- bash -lc $rootAnalysis
if ($LASTEXITCODE -ne 0) { throw 'ROOT analysis of the generated sample failed.' }
$hostRootAnalysis = Join-Path $projectRoot 'outputs\local_smoke_root'
New-Item -ItemType Directory -Force -Path $hostRootAnalysis | Out-Null
& $wslPath -d SMEFTsim -u smeft -- cp -a /home/smeft/smeftsim/outputs/local_smoke_root/. ($linuxSource + '/outputs/local_smoke_root/')
if ($LASTEXITCODE -ne 0) { throw 'Copying ROOT analysis outputs failed.' }
Write-Output 'Project Ubuntu, model import, 2000 SM events, cHl3 reweighting, and ROOT analysis passed in the unified .venv.'

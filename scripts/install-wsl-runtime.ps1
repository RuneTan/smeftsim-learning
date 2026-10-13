$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$logRoot = Join-Path $projectRoot 'outputs\installation'
$installer = Join-Path $projectRoot 'vm\downloads\wsl-x64.msi'
Start-Transcript -Path (Join-Path $logRoot 'wsl-admin-install.log') -Force
try {
    $principal = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'This step requires an elevated Windows process.'
    }
    if ((Get-AuthenticodeSignature -LiteralPath $installer).Status -ne 'Valid') {
        throw 'Invalid Microsoft installer signature.'
    }
    $taskResult = [ordered]@{ installerExitCode = $null; featureState = $null; restartRequired = $false; error = $null }
    $taskProcess = Start-Process -FilePath 'msiexec.exe' -ArgumentList @('/i', ('"' + $installer + '"'), '/qn', '/norestart', '/L*v', ('"' + (Join-Path $logRoot 'wsl-msi.log') + '"')) -WindowStyle Hidden -Wait -PassThru
    $taskResult.installerExitCode = $taskProcess.ExitCode
    if ($taskProcess.ExitCode -notin @(0, 3010)) { throw "WSL installer exit code $($taskProcess.ExitCode)" }
    $feature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    if ($feature.State -ne 'Enabled') {
        $featureResult = Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart
        $taskResult.restartRequired = [bool]$featureResult.RestartNeeded
    }
    if ($taskProcess.ExitCode -eq 3010) { $taskResult.restartRequired = $true }
    $taskResult.featureState = [string](Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform).State
    $taskResult | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $logRoot 'runtime-install-result.json')
} catch {
    [ordered]@{ error = $_.Exception.Message } | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $logRoot 'runtime-install-error.json')
    throw
} finally {
    Stop-Transcript
}

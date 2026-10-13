param(
    [ValidateSet('direct', 'reweight', 'closure')]
    [string]$Stage = 'direct',
    [string]$SMRun,
    [string]$LinearRun,
    [string]$SquareRun,
    [string]$PropRun,
    [string]$Output = 'outputs\learning_comparison'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$outputPath = if ([IO.Path]::IsPathRooted($Output)) { [IO.Path]::GetFullPath($Output) } else { [IO.Path]::GetFullPath((Join-Path $projectRoot $Output)) }
if (-not $outputPath.StartsWith($projectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Choose an output directory inside smeftsim.'
}
function Convert-LinuxPath([string]$WindowsPath) {
    $normalized = $WindowsPath.Replace('\', '/')
    if ($normalized -notmatch '^([A-Za-z]):/(.*)$') { throw 'Expected a local drive path.' }
    return '/mnt/' + $Matches[1].ToLower() + '/' + $Matches[2]
}
$guestScript = Convert-LinuxPath (Join-Path $PSScriptRoot 'lesson_guest.py')
$guestOutput = Convert-LinuxPath $outputPath
if ($Stage -ne 'closure') {
    $guestStage = if ($Stage -eq 'direct') { 'prepare' } else { 'reweight' }
    $guestArgs = @('-d', 'SMEFTsim', '-u', 'smeft', '--', '/home/smeft/smeftsim/.venv/bin/python', $guestScript,
                   '--stage', $guestStage, '--output', $guestOutput)
    if ($SMRun) { $guestArgs += @('--sm-run', $SMRun) }
    if ($LinearRun) { $guestArgs += @('--linear-run', $LinearRun) }
    if ($SquareRun) { $guestArgs += @('--square-run', $SquareRun) }
    if ($PropRun) { $guestArgs += @('--prop-run', $PropRun) }
    & wsl.exe @guestArgs
    if ($LASTEXITCODE -ne 0) { throw 'Sample staging/reweighting failed; inspect the reported log.' }
}
if ($Stage -eq 'reweight') {
    Write-Output 'Reweighting completed. Next: .\scripts\lesson.ps1 -Stage closure'
    return
}
$originalUtf8 = [Environment]::GetEnvironmentVariable('PYTHONUTF8', 'Process')
try {
    $env:PYTHONUTF8 = '1'
    & (Join-Path $projectRoot '.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'compare_lesson.py') --stage $Stage --folder $outputPath
    if ($LASTEXITCODE -ne 0) { throw 'Comparison failed. Read the validation error before interpreting the plots.' }
} finally {
    [Environment]::SetEnvironmentVariable('PYTHONUTF8', $originalUtf8, 'Process')
}
Write-Output "Plots and reports: $outputPath"

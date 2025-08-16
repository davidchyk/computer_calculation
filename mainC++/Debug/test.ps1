# test.ps1
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe       = Join-Path $scriptDir 'app.exe'

# Set arguments here if needed (string or array). Leave as $null when none.
# Examples:
# $procArgs = '-i input.txt -n 100'
# $procArgs = @('-i','input.txt','-n','100')
$procArgs  = $null

if (-not (Test-Path $exe)) { Write-Error "Not found: $exe"; exit 1 }

try {
    $startParams = @{
        FilePath   = $exe
        PassThru   = $true
        ErrorAction= 'Stop'
        NoNewWindow= $true
    }
    if ($procArgs -ne $null -and -not [string]::IsNullOrWhiteSpace(($procArgs -join ' '))) {
        $startParams['ArgumentList'] = $procArgs
    }
    $p = Start-Process @startParams
} catch {
    Write-Error ("Failed to start: " + $_.Exception.Message)
    exit 1
}

$peakWS = 0
$peakPriv = 0

while ($true) {
    $proc = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
    if ($null -eq $proc) { break }
    $peakWS   = [Math]::Max($peakWS,   $proc.WorkingSet64)
    $peakPriv = [Math]::Max($peakPriv, $proc.PrivateMemorySize64)
    Start-Sleep -Milliseconds 50
}

"{0,-12} {1:N2} MiB" -f "Peak WS:",   ($peakWS / 1MB)
"{0,-12} {1:N2} MiB" -f "Peak Priv:", ($peakPriv / 1MB)
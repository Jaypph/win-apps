# Detect the current Windows platform without changing the host.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File .\platform\detect.ps1
[CmdletBinding()]
param([switch]$Json)

$os = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
$arch = switch ($env:PROCESSOR_ARCHITECTURE) {
    "AMD64" { "x86_64" }
    "ARM64" { "arm64" }
    "x86"   { "x86" }
    default { $env:PROCESSOR_ARCHITECTURE.ToLowerInvariant() }
}

$result = [ordered]@{
    os            = "windows"
    product       = $os.Caption
    version       = $os.Version
    build         = $os.BuildNumber
    arch          = $arch
    packageManager = if (Get-Command winget -ErrorAction SilentlyContinue) { "winget" } else { "none" }
}

if ($Json) {
    $result | ConvertTo-Json -Compress
} else {
    $result.GetEnumerator() | ForEach-Object { "{0}={1}" -f $_.Key, $_.Value }
}

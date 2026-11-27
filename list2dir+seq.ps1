$PathsFile = "C:\path\to\paths.txt"
$DestDir   = "D:\Destination_Folder"

if (-not (Test-Path -Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
}

$lines = Get-Content -Path $PathsFile -Encoding UTF8 |
    ForEach-Object { $_.Trim().Trim('"').Trim("'") } |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

$i = 1
foreach ($rawPath in $lines) {
    if (Test-Path -LiteralPath $rawPath -PathType Leaf) {
        $fileName = Split-Path -LiteralPath $rawPath -Leaf
        $numberedName = "{0:D3}_{1}" -f $i, $fileName
        $destPath = Join-Path -Path $DestDir -ChildPath $numberedName
        Copy-Item -LiteralPath $rawPath -Destination $destPath -Force
        $i++
    } else {
        Write-Warning "لم يتم العثور على الملف: $rawPath"
    }
}

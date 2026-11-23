param($in, $out)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$d = $w.Documents.Open($in, $false, $true)
$d.ExportAsFixedFormat($out, 17)
$d.Close($false)
if ($w.Documents.Count -eq 0) { $w.Quit() }

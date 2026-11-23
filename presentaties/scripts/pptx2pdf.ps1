param($in, $out)
$app = New-Object -ComObject PowerPoint.Application
$p = $null
for($t=0; $t -lt 20 -and -not $p; $t++){ try { $p = $app.Presentations.Open($in, $true, $false, $false) } catch { Start-Sleep -Milliseconds 500 } }
$ok=$false; for($t=0;$t -lt 20 -and -not $ok;$t++){ try { $p.ExportAsFixedFormat($out, 2, 1); $ok=$true } catch { Start-Sleep -Milliseconds 500 } }
$p.Close()
if ($app.Presentations.Count -eq 0) { $app.Quit() }

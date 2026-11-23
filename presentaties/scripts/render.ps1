param($in, $outdir, $w=1280, $h=720)
$app = New-Object -ComObject PowerPoint.Application
$p = $null
for($t=0; $t -lt 20 -and -not $p; $t++){ try { $p = $app.Presentations.Open($in, $true, $false, $false) } catch { Start-Sleep -Milliseconds 500 } }
New-Item -ItemType Directory -Force $outdir | Out-Null
$i=1; foreach($s in $p.Slides){ $ok=$false; for($t=0;$t -lt 20 -and -not $ok;$t++){ try { $s.Export("$outdir\s$('{0:D3}' -f $i).png","PNG",$w,$h); $ok=$true } catch { Start-Sleep -Milliseconds 500 } }; $i++ }
$p.Close()
if ($app.Presentations.Count -eq 0) { $app.Quit() }

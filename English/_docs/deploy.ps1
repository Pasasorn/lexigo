# Deploy ทุกอย่างในคำสั่งเดียว:
#   scan secrets -> push Code.gs ขึ้น Apps Script (ทับ deployment เดิม) -> ตรวจ version live -> git push (Cloudflare auto build)
# วิธีใช้ (PowerShell ในโฟลเดอร์ English):
#   .\_docs\deploy.ps1 -m "fix translations"      ทำครบ
#   .\_docs\deploy.ps1 -m "copy" -SkipGas          เฉพาะหน้าเว็บ (Code.gs ไม่เปลี่ยน)
#   .\_docs\deploy.ps1 -SkipGit                    เฉพาะ Apps Script
param(
  [Alias('m')][string]$Message = '',
  [switch]$SkipGas,
  [switch]$SkipGit
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$gas  = Join-Path $root '_gas'
Set-Location $root

Write-Host "== scan secrets ==" -ForegroundColor Cyan
py (Join-Path $root '_docs\scan_secrets.py')
if ($LASTEXITCODE -ne 0) { Write-Host 'STOP: secret scan failed' -ForegroundColor Red; exit 1 }

$code = Get-Content (Join-Path $root 'Code.gs') -Raw -Encoding UTF8
$vm = [regex]::Match($code, "version:'(v\d+)'")
$ver = if ($vm.Success) { $vm.Groups[1].Value } else { '?' }

if (-not $SkipGas) {
  Write-Host "`n== Apps Script: $ver ==" -ForegroundColor Cyan
  if (-not (Test-Path (Join-Path $gas 'deploy.json'))) { Write-Host 'run .\_docs\setup_clasp.ps1 first' -ForegroundColor Red; exit 1 }
  $cfg = Get-Content (Join-Path $gas 'deploy.json') -Raw | ConvertFrom-Json
  Remove-Item (Join-Path $gas 'Code.gs') -ErrorAction SilentlyContinue   # clasp 3 ใช้นามสกุล .js ถ้ามีทั้ง .gs และ .js จะชนกัน
  Copy-Item (Join-Path $root 'Code.gs') (Join-Path $gas 'Code.js') -Force
  Push-Location $gas
  try {
    clasp push -f | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'clasp push failed' }
    clasp deploy -i $cfg.deploymentId -d "$ver $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'clasp deploy failed' }
  } finally { Pop-Location }

  Write-Host "verify live version..." -NoNewline
  $live = $null
  foreach ($i in 1..6) {
    Start-Sleep -Seconds 5
    try { $live = (Invoke-RestMethod "$($cfg.execUrl)?action=version").version } catch {}
    if ($live -eq $ver) { break }
    Write-Host '.' -NoNewline
  }
  if ($live -eq $ver) { Write-Host " live = $live OK" -ForegroundColor Green }
  else { Write-Host " live = $live (expected $ver) — check Apps Script > Manage deployments" -ForegroundColor Yellow }
}

if (-not $SkipGit) {
  Write-Host "`n== git push (Cloudflare Pages builds automatically) ==" -ForegroundColor Cyan
  $top = git rev-parse --show-toplevel
  Set-Location $top
  # กันไฟล์ใหญ่หลุดเข้า commit (GitHub จำกัด 100 MB)
  $big = git -c core.quotepath=off ls-files --others --exclude-standard | ForEach-Object {
    $f = $_.Trim(); if ($f -and (Test-Path -LiteralPath $f) -and (Get-Item -LiteralPath $f).Length -gt 95MB) { $f } }
  if ($big) { Write-Host "STOP: file > 95 MB: $big" -ForegroundColor Red; exit 1 }
  git add -A
  if (-not $Message) { $Message = "deploy $ver $(Get-Date -Format 'yyyy-MM-dd')" }
  git commit -m $Message 2>&1 | Out-Host
  git push | Out-Host
  Write-Host "pushed — Cloudflare Pages will be live in ~1-2 min: https://peekaword.pages.dev/English/" -ForegroundColor Green
}

# ตั้งค่า clasp ครั้งเดียว เพื่อให้ deploy.ps1 ส่ง Code.gs ขึ้น Apps Script ได้อัตโนมัติ
# วิธีใช้ (PowerShell ในโฟลเดอร์ English):  .\_docs\setup_clasp.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot      # โฟลเดอร์ English
$gas  = Join-Path $root '_gas'

Write-Host "== 1/5 check Node + clasp =="
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Host "Node.js not found. Install from https://nodejs.org (LTS) then run again." -ForegroundColor Red; exit 1
}
if (-not (Get-Command clasp -ErrorAction SilentlyContinue)) {
  npm install -g @google/clasp@2
}
clasp --version

Write-Host "`n== 2/5 enable Apps Script API (one-time) =="
Write-Host "Opening https://script.google.com/home/usersettings  -> turn ON 'Google Apps Script API', then press Enter"
Start-Process 'https://script.google.com/home/usersettings'
Read-Host 'Press Enter after enabling'

Write-Host "`n== 3/5 clasp login (browser) =="
if (-not (Test-Path (Join-Path $HOME '.clasprc.json'))) { clasp login } else { Write-Host "already logged in" }

Write-Host "`n== 4/5 link script =="
Write-Host "Script ID: Apps Script editor -> Project Settings (gear) -> 'Script ID' -> Copy"
$scriptId = (Read-Host 'Paste Script ID').Trim()
if ($scriptId.Length -lt 20) { Write-Host 'Script ID looks wrong' -ForegroundColor Red; exit 1 }

# Deployment ID อ่านจาก URL ที่หน้าเว็บใช้อยู่ (…/macros/s/<ID>/exec) เพื่อ deploy ทับตัวเดิม URL ไม่เปลี่ยน
$login = Get-Content (Join-Path $root 'login.html') -Raw -Encoding UTF8
$m = [regex]::Match($login, 'https://script\.google\.com/macros/s/([A-Za-z0-9_-]+)/exec')
if (-not $m.Success) { Write-Host 'exec URL not found in login.html' -ForegroundColor Red; exit 1 }
$deployId = $m.Groups[1].Value
$execUrl  = $m.Value
Write-Host "Deployment ID (from login.html): $($deployId.Substring(0,10))..."

New-Item -ItemType Directory -Force $gas | Out-Null
@{ scriptId = $scriptId; rootDir = '.' } | ConvertTo-Json | Set-Content (Join-Path $gas '.clasp.json') -Encoding ASCII
@{ deploymentId = $deployId; execUrl = $execUrl } | ConvertTo-Json | Set-Content (Join-Path $gas 'deploy.json') -Encoding ASCII

Write-Host "`n== 5/5 pull appsscript.json =="
Push-Location $gas
clasp pull | Out-Host          # ได้ appsscript.json + Code.gs เวอร์ชันที่อยู่บน server (ไฟล์ใน _gas เป็นแค่ staging)
Pop-Location
Remove-Item (Join-Path $gas 'Code.gs') -ErrorAction SilentlyContinue   # clasp 3 ใช้นามสกุล .js ถ้ามีทั้ง .gs และ .js จะชนกัน
  Copy-Item (Join-Path $root 'Code.gs') (Join-Path $gas 'Code.js') -Force   # ใช้ไฟล์หลักของเราเสมอ

Write-Host "`nDONE. Next:  .\_docs\deploy.ps1 -m `"message`"" -ForegroundColor Green

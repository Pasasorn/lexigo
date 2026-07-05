@echo off
:: เช็คว่า port 8000 มี server รันอยู่แล้วมั้ย
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
  echo Server already running — opening browser...
  start "" "http://localhost:8000/admin.html"
  exit
)

echo Starting local server...
start "" "http://localhost:8000/admin.html"
npx --yes serve -l 8000 .

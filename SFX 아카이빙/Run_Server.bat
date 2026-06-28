@echo off
:: 배치 파일이 위치한 폴더로 경로 고정
cd /d %~dp0

:: 1. 시스템 기본 브라우저를 찾아 웹앱 모드(--app)로 HTML 실행
:: 엣지(msedge)를 우선으로 하되, 시스템 환경에 맞춰 동작합니다.
start "" "msedge.exe" --app="%~dp0SMART_AI_Helper.html"

:: 만약 엣지가 없다면 크롬으로 시도
if %errorlevel% neq 0 start "" "chrome.exe" --app="%~dp0SMART_AI_Helper.html"

exit
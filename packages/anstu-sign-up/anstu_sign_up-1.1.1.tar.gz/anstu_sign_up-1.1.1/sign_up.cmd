@echo off

cd /d %~dp0

if exist ".\ahstu_sign_up\ahstu_sign_up.exe" (
    .\ahstu_sign_up\ahstu_sign_up.exe
) else (
    echo ERROR: ahstu_sign_up.exe not found
)
goto exit

:exit
echo ... & pause
exit
@echo off
setlocal
chcp 65001 >nul
title Pi Agents - SSH local

echo =======================================
echo     Pi Agents ^| SSH local
 echo =======================================
echo.
echo Conectando usando el alias SSH pi-agents-local...
ssh pi-agents-local
set "SSH_EXIT=%ERRORLEVEL%"
echo.
if not "%SSH_EXIT%"=="0" echo Error o desconexion SSH. Codigo: %SSH_EXIT%
echo Sesion SSH finalizada.
pause

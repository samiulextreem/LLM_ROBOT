@echo off
setlocal
call "%~dp0kit\kit.exe" "%%~dp0apps/omni.isaac.sim.headless.native.kit" --ext-folder "%~dp0/apps" --no-window  %*

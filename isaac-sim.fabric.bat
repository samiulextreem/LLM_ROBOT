@echo off
setlocal
call "%~dp0kit\kit.exe" "%%~dp0apps/omni.isaac.sim.fabric.kit" --ext-folder "%~dp0/apps"  %*

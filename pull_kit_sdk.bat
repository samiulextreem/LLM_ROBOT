@echo off
setlocal

if exist "%~dp0kit\python\python.exe" (
    "%~dp0kit\python\python.exe" "%~dp0dev\tools\tinypull.py" %*
) else (
    call "%~dp0dev\repo" pull_extensions -c release %*
)

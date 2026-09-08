@echo off
echo ========================================
echo AI File Analyzer .exe yaratish skripti
echo ========================================
echo.

REM Direktoriyani tekshirish
if not exist "%~dp0" (
    echo Xato: Direktoriyani topa olmadim
    exit /b 1
)

echo 1. PyInstaller o'rnatish (agar kerak bo'lsa)
pip install pyinstaller 2>&1 | findstr /i "already satisfied\|Successfully" || echo "O'rnatish tugadi"

echo.
echo 2. AI File Analyzer .exe yaratish...
echo.

pyinstaller --onefile --windowed ^
  --name "AI_File_Analyzer" ^
  --hidden-import pymupdf ^
  --hidden-import docx ^
  --hidden-import openpyxl ^
  --hidden-import customtkinter ^
  --hidden-import tk ^
  --hidden-import tkinter.ttk ^
  --hidden-import tkinter.scrolledtext ^
  --hidden-import tkinter.filedialog ^
  --hidden-import tkinter.messagebox ^
  --hidden-import tkinter.simpledialog ^
  --hidden-import dotenv ^
  --hidden-import requests ^
  --hidden-import lxml ^
  --hidden-import lxml.etree ^
  --hidden-import lxml.html ^
  --hidden-import ai_client ^
  --hidden-import file_parser ^
  --hidden-import config ^
  --hidden-import ui.main_window ^
  main.py

echo.
if exist dist\AI_File_Analyzer.exe (
    echo ========================================
    echo MUVAFFAQQIY!
    echo ========================================
    echo .exe fayl tayyor: dist\AI_File_Analyzer.exe
    echo Hajmi: 
    dir dist\AI_File_Analyzer.exe /-C
    echo.
    echo Foydalanish uchun .exe ni bosing yoki double-click qiling.
) else (
    echo ========================================
    echo XATO! .exe yaratilmadi.
    echo ========================================
)

pause

@echo off
title SS Kopyala - Build
echo ============================================
echo  SS Kopyala - EXE Builder
echo ============================================
echo.

echo [1/4] PyInstaller kuruluyor...
pip install pyinstaller pillow pytesseract pyperclip pystray keyboard >nul 2>&1
echo  OK

echo [2/4] Ikon olusturuluyor...
python create_icon.py
echo  OK

echo [3/4] EXE derleniyor (biraz surebilir)...
pyinstaller --onedir ^
            --windowed ^
            --icon=icon.ico ^
            --name="SS Kopyala" ^
            --add-data "icon.ico;." ^
            --hidden-import=pystray._win32 ^
            --hidden-import=PIL._tkinter_finder ^
            app.py

echo.
echo [4/4] Klasor masaustune kopyalaniyor...
if exist "dist\SS Kopyala" (
    xcopy /E /I /Y "dist\SS Kopyala" "%USERPROFILE%\Desktop\SS Kopyala" >nul
    echo  OK - Masaustunde "SS Kopyala" klasoru hazir!
    echo  Icerisindeki "SS Kopyala.exe" yi calistir.
) else (
    echo  HATA: Build basarisiz, yukaridaki hatalara bak.
)

echo.
echo ============================================
echo  Bitti! Masaustunden calistirabilirsin.
echo ============================================
pause

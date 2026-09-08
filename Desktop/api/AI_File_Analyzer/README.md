# AI File Analyzer - Windows Desktop Dasturi

Zamonaviy, professional AI ta'sirida fayllarni (PDF, DOCX, TXT, XLSX, CSV) tahlil qiluvchi Windows desktop dasturi.

## O'rnatish

### 1. Python o'rnatish
Python 3.8+ o'rnating: https://www.python.org/downloads/

### 2. Bog'liqliklarni o'rnatish
```bash
cd AI_File_Analyzer
pip install -r requirements.txt
```

### 3. API kaliti sozlash
```bash
copy .env.example .env
```
Keyin `.env` faylini oching va `KIMI_API_KEY` ni o'rnating.

### 4. Dasturni ishga tushirish
```bash
python main.py
```

## Fayl Turlari

| Format | Qo'shimcha paketlar |
|--------|---------------------|
| PDF    | PyMuPDF             |
| DOCX   | python-docx         |
| TXT    | Standard library    |
| XLSX   | openpyxl            |
| CSV    | Standard library    |

## AI Integration

Dastur Kimi K2P6 API dan foydalanadi. AI keyingi xususiyatlari:
- Chunklarga ajratish (katta fayllar uchun)
- Smart chunking: so'z va yangi satr holatlarini saqlash
- Chunklarni mashq qilish
- Savol-javob chat

## PyInstaller bilan .exe yaratish

### O'rnatish:
```bash
pip install pyinstaller
```

### .exe yaratish:
```cmd
pyinstaller --onefile --windowed --name "AI_File_Analyzer" ^
  --icon=assets\icon.ico ^
  --add-data "assets;assets" ^
  --hidden-import fitz ^
  --hidden-import docx ^
  --hidden-import openpyxl ^
  main.py
```

### Natija:
- `dist\AI_File_Analyzer.exe`

### PyInstaller yechimi (build.bat):
```batch
@echo off
echo AI File Analyzer .exe yaratish...

REM Bog'liqliklarni o'rnatish
pip install -r requirements.txt

REM PyInstaller o'rnatish
pip install pyinstaller

REM .exe yaratish
pyinstaller --onefile --windowed ^
  --name "AI_File_Analyzer" ^
  --icon=assets\icon.ico ^
  main.py

echo.
echo .exe tayyor! dist\AI_File_Analyzer.exe
pause
```

## Loyiha Strukturasi

```
AI_File_Analyzer/
├── main.py              # Dastur kirish nuqtasi
├── ai_client.py         # Kimi API clienti
├── file_parser.py       # Fayl parserlari
├── config.py            # Konfiguratsiya
├── requirements.txt     # Python paketlar
├── .env.example         # Kalitlar namunasi
├── README.md            # Hujjat
├── assets/             # Iconlar va boshqa fayllar
├── ui/
│   └── main_window.py   # GUI interfeys
└── dist/               # .exe chiqish joyi (PyInstaller dan keyin)
```

## Permissions

PyInstaller --onefile .exe istifadan fayl tanlash uchun:
- Fayl ochergi uchun "tanla..." dialogi ishlaydi
- Fayl tarkibini o'qish uchun o'qish ruxsati kerak

## Tech Stack

- CustomTkinter - Zamonaviy dark theme GUI
- PyMuPDF (fitz) - PDF o'qish
- python-docx - DOCX o'qish
- openpyxl - XLSX/CSV o'qish
- requests - HTTP API call
- python-dotenv - .env konfiguratsiyasi

## License

MIT

## Muallif

Upstage Solar Pro4

"""
PyInstaller konfiguratsiyasi - .exe yaratish uchun yordamchi fayl.
"""

import sys

# PyInstaller uchun yashirin importlar ro'yxati
hiddenimports = [
    # Fayl parserlari
    'pymupdf',         # PyMuPDF (fitz)
    'docx',           # python-docx
    'docx.opc', 
    'docx.oxml',
    'docx.oxml.ns',
    'openpyxl',       # XLSX
    'openpyxl.styles',
    'openpyxl.worksheet',
    'openpyxl.utils',
    
    # UI
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    
    # AI Client
    'ai_client',
    'file_parser',
    'config',
    'ui.main_window',
    
    # Bog'liqliklar
    'dotenv',
    'requests',
    'lxml',
    'lxml.etree',
    'lxml.html',
    
    # Tizim modullari
    'os',
    'sys',
    'json',
    'threading',
    'pathlib',
    'datetime',
    'csv',
    'io',
    
    # Paketlar
    'packaging',
    'darkdetect',
    'et_xmlfile',
]

# Qo'shimcha paketlarni qo'shish
packages = [
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'tkinter.colorchooser',
]

# Qo'shimcha fayllar
datas = [
    ('assets/*', 'assets'),
]

# Kutiladigan modullar (chiqarib tashlash)
excludedimports = [
    'tkinter.test',
    'tkinter.test.test_tkinter',
]


def get_pyinstaller_args():
    """PyInstaller uchun asosiy argumentlar."""
    return {
        "onefile": True,
        "windowed": True,
        "name": "AI_File_Analyzer",
        "icon": "assets/icon.ico" if __import__('os').path.exists("assets/icon.ico") else None,
        "hiddenimports": hiddenimports,
        "packages": packages,
        "datas": datas,
        "exclude": excludedimports,
    }


if __name__ == "__main__":
    args = get_pyinstaller_args()
    print("PyInstaller argumentlari:")
    for key, value in args.items():
        if value:
            print(f"  --{key.replace('_', '-')}: {value}")

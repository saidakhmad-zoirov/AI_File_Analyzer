"""
File Parser - Turli formatdagi fayllarni o'qish va tarkibini olish modul.
Poddleklar: PyMuPDF, python-docx, openpyxl
"""

import os
from pathlib import Path
from typing import Optional, List, Tuple

# PDF o'qish uchun PyMuPDF
try:
    import pymupdf as fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Ogohlantirish: PyMuPDF o'rnatilmagan. PDF fayllarni qo'llab-quvvatlamaydi.")

# DOCX o'qish uchun python-docx
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Ogohlantirish: python-docx o'rnatilmagan. DOCX fayllarni qo'llab-quvvatlamaydi.")

# XLSX o'qish uchun openpyxl
try:
    from openpyxl import load_workbook
    XLSX_AVAILABLE = True
except ImportError:
    XLSX_AVAILABLE = False
    print("Ogohlantirish: openpyxl o'rnatilmagan. XLSX fayllarni qo'llab-quvvatlamaydi.")


class FileParser:
    """Fayl turlarini parse qilish uchun asosiy klass."""
    
    SUPPORTED_FORMATS = {
        ".pdf": "PDF",
        ".docx": "DOCX",
        ".txt": "TXT",
        ".xlsx": "XLSX",
        ".csv": "CSV",
    }
    
    DEFAULT_CHUNK_SIZE = 15000
    CHUNK_OVERLAP = 500
    
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def parse(self, file_path: str) -> Optional[str]:
        """Faylni o'qib, uning tarkibini string ko'rinishida qaytaradi."""
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == ".pdf":
                return self._parse_pdf(file_path)
            elif file_ext == ".docx":
                return self._parse_docx(file_path)
            elif file_ext == ".txt":
                return self._parse_txt(file_path)
            elif file_ext == ".xlsx":
                return self._parse_xlsx(file_path)
            elif file_ext == ".csv":
                return self._parse_csv(file_path)
            else:
                print(f"Qo'llab-quvvatlanmaydigan format: {file_ext}")
                return None
        except Exception as e:
            print(f"Fayl parse xatosi ({file_ext}): {e}")
            return None
    
    def _parse_pdf(self, file_path: str) -> Optional[str]:
        """PDF faylni o'qish."""
        if not PDF_AVAILABLE:
            raise ImportError("PyMuPDF o'rnatilmagan. `pip install PyMuPDF`")
        
        try:
            doc = fitz.open(file_path)
            text_parts = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_parts.append(f"[Sahifa {page_num + 1}]\n{text}")
            
            doc.close()
            return "\n\n".join(text_parts)
            
        except Exception as e:
            print(f"PDF o'qishda xato: {e}")
            return None
    
    def _parse_docx(self, file_path: str) -> Optional[str]:
        """DOCX faylni o'qish."""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx o'rnatilmagan. `pip install python-docx`")
        
        try:
            doc = Document(file_path)
            paragraphs = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            # Jadvallardan ma'lumot
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text)
                    if row_text:
                        paragraphs.append(" | ".join(row_text))
            
            return "\n\n".join(paragraphs)
            
        except Exception as e:
            print(f"DOCX o'qishda xato: {e}")
            return None
    
    def _parse_txt(self, file_path: str) -> Optional[str]:
        """TXT faylni o'qish."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"TXT o'qishda xato: {e}")
                return None
        except Exception as e:
            print(f"TXT o'qishda xato: {e}")
            return None
    
    def _parse_xlsx(self, file_path: str) -> Optional[str]:
        """XLSX (Excel) faylni o'qish."""
        if not XLSX_AVAILABLE:
            raise ImportError("openpyxl o'rnatilmagan. `pip install openpyxl`")
        
        try:
            workbook = load_workbook(file_path, data_only=True)
            parts = []
            
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                parts.append(f"\n=== {sheet_name} ===\n")
                
                for row in sheet.iter_rows(values_only=True):
                    row_values = []
                    for cell in row:
                        if cell is not None:
                            row_values.append(str(cell))
                    
                    if row_values:
                        parts.append(" | ".join(row_values))
            
            workbook.close()
            return "\n".join(parts)
            
        except Exception as e:
            print(f"XLSX o'qishda xato: {e}")
            return None
    
    def _parse_csv(self, file_path: str) -> Optional[str]:
        """CSV faylni o'qish."""
        try:
            import csv
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                lines = []
                
                for row in reader:
                    if row:
                        lines.append(" | ".join(row))
                
                return "\n".join(lines)
                
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    reader = csv.reader(f)
                    lines = []
                    
                    for row in reader:
                        if row:
                            lines.append(" | ".join(row))
                    
                    return "\n".join(lines)
            except Exception as e:
                print(f"CSV o'qishda xato: {e}")
                return None
        except Exception as e:
            print(f"CSV o'qishda xato: {e}")
            return None
    
    def get_file_info(self, file_path: str) -> dict:
        """Fayl haqida ma'lumot olish."""
        path = Path(file_path)
        stat = path.stat()
        size_bytes = stat.st_size
        
        if size_bytes < 1024:
            size_human = f"{size_bytes} bayt"
        elif size_bytes < 1024 * 1024:
            size_human = f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_human = f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            size_human = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        
        import datetime
        created = datetime.datetime.fromtimestamp(stat.st_ctime)
        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        
        return {
            "name": path.name,
            "extension": path.suffix.lower(),
            "format": self.SUPPORTED_FORMATS.get(path.suffix.lower(), "Noma'lum"),
            "size": size_bytes,
            "size_human": size_human,
            "created": created.strftime("%Y-%m-%d %H:%M"),
            "modified": modified.strftime("%Y-%m-%d %H:%M"),
            "path": str(path.absolute()),
        }
    
    def chunk_content(self, content: str) -> List[Tuple[int, str]]:
        """Uzoq matnni qismlarga (chunk) ajratish."""
        if not content or len(content.strip()) == 0:
            return []
        
        chunks = []
        start = 0
        chunk_num = 0
        
        while start < len(content):
            end = start + self.chunk_size
            
            if end >= len(content):
                chunk_text = content[start:].strip()
                if chunk_text:
                    chunk_num += 1
                    chunks.append((chunk_num, chunk_text))
                break
            
            chunk_raw = content[start:end]
            
            # So'z chegarasidan kesishni xavfsizlashtirish
            last_space = chunk_raw.rfind(" ")
            last_newline = chunk_raw.rfind("\n")
            
            cut_point = max(last_space, last_newline)
            
            if cut_point > self.chunk_overlap:
                chunk_text = content[start:start + cut_point].strip()
                start = start + cut_point + 1
            else:
                chunk_text = content[start:end].strip()
                start = end
            
            if chunk_text:
                chunk_num += 1
                chunks.append((chunk_num, chunk_text))
        
        return chunks
    
    def detect_format(self, file_path: str) -> Optional[str]:
        """Fayl formatini aniqlash."""
        ext = Path(file_path).suffix.lower()
        return self.SUPPORTED_FORMATS.get(ext)

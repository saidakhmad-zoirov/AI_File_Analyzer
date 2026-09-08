#!/usr/bin/env python3
"""
AI File Analyzer - Zamonaviy Windows Desktop Dasturi
Fayllarni (PDF, DOCX, TXT, XLSX, CSV) AI orqali tahlil qilish.
"""

import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

# Bog'lanishi va o'zini yangilash imkonini beruvchi UI
from ui.main_window import MainWindow
from ai_client import KimiAIClient
from file_parser import FileParser
from config import load_config


class App:
    """Asosiy dastur klassi."""
    
    def __init__(self):
        # Load config from .env
        self.config = load_config()
        
        # AI client ini
        self.api_key = self.config.get('KIMI_API_KEY', '')
        self.ai_client = KimiAIClient(api_key=self.api_key) if self.api_key else None
        
        # File parser
        self.file_parser = FileParser()
        
        # State
        self.current_file_path = None
        self.current_file_content = None
        self.current_file_name = None
        self.is_analyzing = False
        
        # UI
        self.root = ctk.CTk()
        self.main_window = MainWindow(self.root, self)
        
    def select_file(self):
        """Fayl tanlash dialogi."""
        file_types = [
            ("Barcha qo'llab-quvvatlanayotgan fayllar", "*.pdf *.docx *.txt *.xlsx *.csv"),
            ("PDF fayllar", "*.pdf"),
            ("DOCX hujjatlar", "*.docx"),
            ("TXT matn fayllari", "*.txt"),
            ("XLSX jadvalar", "*.xlsx"),
            ("CSV jadvalar", "*.csv"),
        ]
        
        file_path = filedialog.askopenfilename(
            title="Faylni tanlang",
            filetypes=file_types,
            initialdir=os.path.expanduser("~")
        )
        
        if file_path:
            self._load_file(file_path)
    
    def _load_file(self, file_path: str):
        """Faylni yuklab, tarkibini o'qish."""
        try:
            self.current_file_path = file_path
            self.current_file_name = Path(file_path).name
            
            # Faylni parse qilish
            content = self.file_parser.parse(file_path)
            
            if not content:
                messagebox.showerror(
                    "Xato",
                    f"Faylni o'qishda xato yuz berdi: {file_path}"
                )
                self._clear_file()
                return
            
            self.current_file_content = content
            
            # UI ga ma'lumot berish
            self.main_window.update_file_info(self.current_file_name, len(content))
            
            # Fayl katta bo'lsa, chunklarga ajratish haqida xabar
            if len(content) > 50000:
                self.main_window.show_warning(
                    "Katta fayl",
                    f"Fayl juda katta ({len(content):,} belgi). "
                    "Tahlil uchun fayl avtomatik ravishda qismlarga ajratiladi."
                )
            
            self.main_window.enable_analyze_button()
            
        except Exception as e:
            messagebox.showerror("Xato", f"Faylni yuklashda xato: {str(e)}")
            self._clear_file()
    
    def _clear_file(self):
        """Fayl ma'lumotlarini tozalash."""
        self.current_file_path = None
        self.current_file_content = None
        self.current_file_name = None
        self.main_window.reset_file_info()
        self.main_window.disable_analyze_button()
    
    def analyze_file(self):
        """Faylni AI tahlil qilish."""
        if not self.current_file_content:
            messagebox.showwarning("Ogohlantirish", "Iltimos, avval fayl tanlang!")
            return
        
        if self.is_analyzing:
            return
        
        if not self.ai_client:
            messagebox.showerror(
                "API Kaliti Yo'q",
                "Kimi AI API kaliti topilmadi.\n\n"
                "Iltimos, .env faylida KIMI_API_KEY ni o'rnating.\n"
                "Yoki .env.example faylni nusxa olib, .env ga qo'llang."
            )
            return
        
        self.is_analyzing = True
        self.main_window.set_analyzing_state(True)
        self.main_window.clear_results()
        self.main_window.append_status("Tahlil boshlandi... Iltimos, kuting.")
        
        # Faylni qismlarga ajratish
        chunks = self.file_parser.chunk_content(self.current_file_content)
        self.main_window.append_status(f"Fayl {len(chunks)} ta qismga bo'lingan.")
        
        # Har bir chunk ni alohida tahlil qilish
        all_results = []
        total_chunks = len(chunks)
        
        def process_chunks():
            try:
                for i, chunk in enumerate(chunks, 1):
                    if i > 1:
                        self.main_window.append_status(f"Qism {i}/{total_chunks} tahlil...")
                    
                    # Prompt yaratish
                    prompt = self._create_analysis_prompt(chunk, i, total_chunks)
                    
                    # AI ga yuborish
                    result = self.ai_client.analyze(prompt)
                    all_results.append((i, result))
                    
                    # Natijani saqlash (chunk tahlili)
                    self.main_window.append_status(f"Qism {i}/{total_chunks} yakunlandi.")
                
                # Yagona xulosa yaratish
                self._compile_final_results(all_results, chunks)
                
            except Exception as e:
                self.root.after(0, self._on_analysis_error, str(e))
            finally:
                self.root.after(0, self._on_analysis_complete)
        
        thread = threading.Thread(target=process_chunks, daemon=True)
        thread.start()
    
    def _create_analysis_prompt(self, chunk: str, chunk_num: int, total_chunks: int) -> str:
        """AI uchun tahlil prompt yaratish."""
        return f"""Siz — professional hujjat tahlili bo'lib, men sizga quyidagi fayl ma'lumotlarini yuboryapman.

 chunk {chunk_num} / {total_chunks} bo'lib, bu faylning umumiy qismi.

 Keling, ushbu qism uchun quyidagilarni aniq va tizimli ravishda tayyorlang:

1. BU QISM UCHUN QISQA XULOSA (2-4 ta gap)
2. ASOSIY MAVZU(N) - 3-5 ta
3. MUHIM MA'LUMOTLAR - 5-8 ta (bullet yoki sonli ro'yxat)
4. BARCHA MUHIM Faktlar
5. Savol-Javob (agar kerak bo'lsa):

Fayl qismi:
---START---
{chunk[:15000]}  # Chunk hajmi 15000 belgidan oshmasligi kerak
---END---

JAVOB KETMA-KETLIGI:
{{
  "quvoshqa_xulosa": "...",
  "asosiy_mavzular": ["...", "..."],
  "muhim_ma'lumotlar": ["...", "..."],
  "asosiy_faktlar": ["...", "..."],
  "qo'shimcha_tushuntirish": "...",
  "savollar_javoblar": []
}}

Javob faqat JSON formatida bo'lsin!"""
    
    def _compile_final_results(self, all_results: list, chunks: list):
        """Barcha chunk natijalarini yagona xulosaga aylantirish."""
        # Barcha chunk larni birlashtirish
        combined_summary_parts = []
        all_topics = set()
        all_key_facts = []
        all_important_data = []
        
        for chunk_num, result in all_results:
            try:
                if isinstance(result, str):
                    import json
                    result = json.loads(result)
                
                if "quvoshqa_xulosa" in result:
                    combined_summary_parts.append(f"[Qism {chunk_num}]: {result['quvoshqa_xulosa']}")
                if "asosiy_mavzular" in result:
                    all_topics.update(result["asosiy_mavzular"])
                if "muhim_ma'lumotlar" in result:
                    all_important_data.extend(result["muhim_ma'lumotlar"])
                if "asosiy_faktlar" in result:
                    all_key_facts.extend(result["asosiy_faktlar"])
                if "savollar_javoblar" in result:
                    for qna in result["savollar_javoblar"]:
                        all_important_data.append(f"Q: {qna.get('question', '')} | A: {qna.get('answer', '')}")
                
            except (json.JSONDecodeError, Exception) as e:
                combined_summary_parts.append(f"[Qism {chunk_num}]: Tahlil qilinmadi ({str(e)})")
        
        # Yakuniy JSON yaratish
        final_prompt = f"""Quyida bir necha chunk dan foydalanib, faylning yakuniy tahlili berilgan.

Har bir chunk uchun alohida tahlil:
{chr(10).join([f"Qism {i}: {r}" for i, r in all_results])}

Yaqinlashtirilgan maqsad: Ushbu faylni butunlay tahlil qilish uchun quyidagi ma'lumotlarni  JSON ko'rinishida taqdim eting:

1. Faylning QISQA XULOSA (3-5 gap)
2. ASOSIY MAVZULAR (3-5 ta, birgalikda)
3. MUHIM MA'LUMOTLAR (5-8 ta, barcha faylni qamrab olgan)
4. ASOSIY Faktlar 
5. Qo'shimcha tushuntirish

Javob JSON:
{{
  "qisqacha_xulosa": "...",
  "asosiy_mavzular": ["...", "..."],
  "muhim_ma'lumotlar": ["...", "..."],
  "asosiy_faktlar": ["...", "..."],
  "qo'shimcha_tushuntirish": "...",
  "savollar_javoblar": []
}}

FAQAT JSON!"""
        
        def get_final_analysis():
            try:
                response = self.ai_client.analyze(final_prompt)
                self.root.after(0, self._display_final_results, response)
            except Exception as e:
                self.root.after(0, self._on_analysis_error, str(e))
        
        thread = threading.Thread(target=get_final_analysis, daemon=True)
        thread.start()
    
    def _display_final_results(self, result_text: str):
        """Yakuniy natijalarni ko'rsatish."""
        self.main_window.append_status("Yakuniy tahlil tayyor...")
        
        try:
            import json
            result = json.loads(result_text)
            
            self.main_window.display_results(result)
            
        except (json.JSONDecodeError, Exception) as e:
            # Agar JSON bo'lmasa, to'g'ridan-to'g'ri ko'rsatish
            self.main_window.display_raw_results(result_text)
    
    def ask_question(self, question: str):
        """Foydalanuvchi savolini AI ga berish."""
        if not question or not question.strip():
            return
        
        if not self.ai_client:
            messagebox.showerror("Xato", "API kaliti yo'q!")
            return
        
        if not self.current_file_content:
            messagebox.showwarning("Ogohlantirish", "Avval fayl tanlang!")
            return
        
        self.is_analyzing = True
        self.main_window.set_analyzing_state(True)
        
        # Savol bilan birgalikda fayl ma'lumotlarini yuborish
        prompt = f"""Siz professional hujjat tahlili. Foydalanuvchi quyidagi fayl haqida savol berdi.

FAYL MA'LUMOTLARI:
===
NOMI: {self.current_file_name}
HARFLARI: {len(self.current_file_content):,}
MATNI:
{self.current_file_content[:20000]}  # Eng muhim 20k belgi
===

FOYDALUVCHİNİN SAVOSI:
{question}

JAVOB:
Fayl ma'lumotlariga asosan, aniq va foydali javob ber.
Agar faylda ma'lumot yo'q bo'lsa, "Faylda ushbu ma'lumot topilmadi" de.
"""
        
        def get_answer():
            try:
                response = self.ai_client.analyze(prompt)
                self.root.after(0, self.main_window.add_chat_message, "AI", response)
            except Exception as e:
                self.root.after(0, self._on_analysis_error, str(e))
            finally:
                self.root.after(0, self._on_analysis_complete)
        
        thread = threading.Thread(target=get_answer, daemon=True)
        thread.start()
    
    def _on_analysis_complete(self):
        """Tahlil yakunlandi."""
        self.is_analyzing = False
        self.main_window.set_analyzing_state(False)
        self.main_window.enable_question_input()
    
    def _on_analysis_error(self, error_msg: str):
        """Xato yuz berdi."""
        self.is_analyzing = False
        self.main_window.set_analyzing_state(False)
        self.main_window.append_status(f"Xato yuz berdi: {error_msg}")
        messagebox.showerror("Xato", f"Tahlilda xato yuz berdi:\n{error_msg}")


def main():
    """Dasturga kirish nuqtasi."""
    # High DPI support
    ctk.set_widget_scaling(1.0)
    
    # Theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = App()
    app.root.title("AI File Analyzer")
    app.root.geometry("900x700")
    app.root.minsize(800, 600)
    
    # Center on screen
    app.root.eval('tk::PlaceWindow . center')
    
    app.root.mainloop()


if __name__ == "__main__":
    main()

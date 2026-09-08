"""UI - Zamonaviy AI File Analyzer asosiy oyna"""

import customtkinter as ctk
from tkinter import scrolledtext, messagebox
from pathlib import Path
from typing import Optional

# Ranglar
DARK_BG = "#0d1117"
DARK_BORDER = "#21262d"
ACCENT = "#58a6ff"
SUCCESS = "#3fb950"
WARNING = "#d29922"
ERROR = "#f85149"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"


class MainWindow:
    """Asosiy darshatdar oynasi."""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        
        self.analyzing = False
        self.file_loaded = False
        
        self._create_widgets()
        self._apply_theme()
    
    def _create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_header()
        self._create_file_section()
        self._create_file_info_section()
        self._create_results_section()
        self._create_question_section()
        self._create_status_section()
    
    def _create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG)
        header_frame.pack(fill="x", pady=(0, 20))
        
        self.logo_label = ctk.CTkLabel(
            header_frame,
            text="🤖",
            font=("Segoe UI", 32),
        )
        self.logo_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="AI FILE ANALYZER",
            font=ctk.CTkFont(size=24, weight="bold", family="Segoe UI"),
            text_color=TEXT_PRIMARY,
        )
        title_label.pack(side="left")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Katta fayllarni AI orqali tahlil qiling",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=TEXT_SECONDARY,
        )
        subtitle_label.pack(side="left", padx=(15, 0), pady=(5, 0))
    
    def _create_file_section(self):
        file_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=8)
        file_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            file_frame,
            text="FAYL TANLANG",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            text_color=ACCENT,
        ).pack(anchor="w", pady=(10, 5))
        
        btn_frame = ctk.CTkFrame(file_frame, fg_color=DARK_BG)
        btn_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.select_btn = ctk.CTkButton(
            btn_frame,
            text="📁  SELECT FILE",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            fg_color=ACCENT,
            hover_color="#4a96e6",
            command=self.app.select_file,
            height=40,
            corner_radius=6,
        )
        self.select_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.analyze_btn = ctk.CTkButton(
            btn_frame,
            text="🔍  ANALYZE",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            fg_color=DARK_BORDER,
            hover_color="#333842",
            text_color=TEXT_SECONDARY,
            state="disabled",
            height=40,
            corner_radius=6,
        )
        self.analyze_btn.pack(side="left", expand=True, fill="x")
        
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="✕",
            font=ctk.CTkFont(size=16, family="Segoe UI"),
            fg_color="transparent",
            hover_color="#333842",
            text_color=TEXT_SECONDARY,
            width=40,
            height=40,
            corner_radius=6,
            state="disabled",
        )
        self.clear_btn.pack(side="right")
    
    def _create_file_info_section(self):
        info_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=8)
        info_frame.pack(fill="x", pady=(0, 15))
        
        self.file_info_label = ctk.CTkLabel(
            info_frame,
            text="Fayl: Hech qanday fayl tanlanmagan",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            text_color=TEXT_SECONDARY,
            anchor="w",
        )
        self.file_info_label.pack(fill="x", padx=20, pady=(10, 5))
        
        self.file_detail_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=11, family="Segoe UI", slant="italic"),
            text_color="#5d6a7e",
            anchor="w",
        )
        self.file_detail_label.pack(fill="x", padx=20)
    
    def _create_results_section(self):
        results_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=8)
        results_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        ctk.CTkLabel(
            results_frame,
            text="AI NATIJALARI",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            text_color=ACCENT,
        ).pack(anchor="w", pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            bg="#0d1117",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            font=("Consolas", 12),
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            wrap="word",
            state="disabled",
            padx=15,
            pady=15,
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.results_text.tag_config("summary", foreground=ACCENT, font=("Segoe UI", 13, "bold"))
        self.results_text.tag_config("topic", foreground="#e6edf3", font=("Segoe UI", 12))
        self.results_text.tag_config("info", foreground=SUCCESS, font=("Segoe UI", 11))
        self.results_text.tag_config("fact", foreground=TEXT_SECONDARY, font=("Consolas", 11))
        self.results_text.tag_config("qna", foreground="#f0883e", font=("Segoe UI", 11))
        self.results_text.tag_config("divider", foreground="#30363d", font=("Segoe UI", 10))
        
        self.results_text.insert("1.0", "Faylni tanlang va ANALYZE tugmasini bosing.\n")
        self.results_text.insert("end", "AI faylni tahlil qilib, quyidagi ma'lumotlarni taqdim etadi:\n")
        self.results_text.insert("end", "• Qisqacha xulosa\n• Asosiy mavzular\n• Muhim ma'lumotlar\n• Asosiy faktlar\n")
        self.results_text.insert("end", "• Savollar va javoblar (kerak bo'lsa)")
        
        from tkinter import END
        self.results_text.tag_add("divider", "end-2c", "end-1c")
        self.results_text.tag_configure("placeholder", foreground="#5d6a7e", font=("Segoe UI", 11))
        self.results_text.tag_add("placeholder", "1.0", "end")
    
    def _create_question_section(self):
        q_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=8)
        q_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            q_frame,
            text="SAVOL BERISH",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            text_color=ACCENT,
        ).pack(anchor="w", pady=(10, 5))
        
        q_input_frame = ctk.CTkFrame(q_frame, fg_color=DARK_BG)
        q_input_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.question_entry = ctk.CTkEntry(
            q_input_frame,
            placeholder_text="Fayl haqida savol bering...",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            fg_color="#161b22",
            border_color="#30363d",
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5d6a7e",
            height=36,
            corner_radius=6,
        )
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.question_entry.bind("<Return>", self._on_question_submit)
        
        self.ask_btn = ctk.CTkButton(
            q_input_frame,
            text="❓  SO'RASH",
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            fg_color=ACCENT,
            hover_color="#4a96e6",
            command=self._on_question_submit,
            height=36,
            corner_radius=6,
        )
        self.ask_btn.pack(side="right")
        
        self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=8)
        self.chat_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        ctk.CTkLabel(
            self.chat_frame,
            text="CHAT",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            text_color=ACCENT,
        ).pack(anchor="w", pady=(10, 5))
        
        self.chat_text = scrolledtext.ScrolledText(
            self.chat_frame,
            bg="#0d1117",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            font=("Consolas", 12),
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            wrap="word",
            state="disabled",
            padx=10,
            pady=10,
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.chat_text.insert("1.0", "Faylni tahlil qilgandan so'ng, undan savol bera olasiz.")
    
    def _create_status_section(self):
        status_frame = ctk.CTkFrame(self.main_frame, fg_color=DARK_BG, corner_radius=4)
        status_frame.pack(fill="x", pady=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Tayyor",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=TEXT_SECONDARY,
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=15, pady=8)
        
        self.progress = ctk.CTkProgressBar(
            status_frame,
            mode="indeterminate",
            fg_color=DARK_BG,
            progress_color=ACCENT,
        )
        self.progress.pack(fill="x", padx=15, pady=(0, 5))
        self.progress.stop()
    
    def _apply_theme(self):
        self.root.configure(fg_color=DARK_BG)
    
    # ==================== UI METHODS ====================
    
    def update_file_info(self, file_name: str, content_length: int):
        self.file_info_label.configure(text=f"📄  Fayl: {file_name}")
        
        if content_length < 1024:
            size_text = f"{content_length} belgi"
        elif content_length < 1024 * 1024:
            size_text = f"{content_length / 1024:.1f} KB ({content_length:,} belgi)"
        else:
            size_text = f"{content_length / (1024*1024):.1f} MB ({content_length:,} belgi)"
        
        self.file_detail_label.configure(text=f"O'lchami: {size_text}")
        self.file_loaded = True
    
    def reset_file_info(self):
        self.file_info_label.configure(
            text="Fayl: Hech qanday fayl tanlanmagan",
            text_color=TEXT_SECONDARY,
        )
        self.file_detail_label.configure(text="")
        self.file_loaded = False
    
    def enable_analyze_button(self):
        self.analyze_btn.configure(
            state="normal",
            fg_color=SUCCESS,
            hover_color="#2ea043",
            text_color="#ffffff",
        )
        self.clear_btn.configure(state="normal")
    
    def disable_analyze_button(self):
        self.analyze_btn.configure(
            state="disabled",
            fg_color=DARK_BORDER,
            hover_color="#333842",
            text_color=TEXT_SECONDARY,
        )
        self.clear_btn.configure(state="disabled")
    
    def set_analyzing_state(self, active: bool):
        self.analyzing = active
        
        if active:
            self.analyze_btn.configure(state="disabled")
            self.select_btn.configure(state="disabled")
            self.question_entry.configure(state="disabled")
            self.ask_btn.configure(state="disabled")
            self.progress.start()
        else:
            self.analyze_btn.configure(
                state="normal",
                fg_color=SUCCESS,
                hover_color="#2ea043",
                text_color="#ffffff",
            )
            self.select_btn.configure(state="normal")
            self.progress.stop()
    
    def clear_results(self):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "Tahlil boshlandi... Iltimos, kuting.")
        self.results_text.tag_add("placeholder", "1.0", "end")
        self.results_text.configure(state="disabled")
    
    def append_status(self, message: str):
        self.status_label.configure(text=message)
    
    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)
    
    def enable_question_input(self):
        self.question_entry.configure(state="normal")
        self.ask_btn.configure(state="normal")
    
    # ==================== NATIJALAR KO'RSATISH ====================
    
    def display_results(self, result: dict):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        
        if result.get("qisqacha_xulosa"):
            summary = result["qisqacha_xulosa"]
            self.results_text.insert("end", "📋  QISQACHA XULOSA\n")
            self.results_text.insert("end", f"{summary}\n\n")
            from tkinter import END
            self.results_text.tag_add("summary", "end-2c", "end-1c")
        
        topics = result.get("asosiy_mavzular", [])
        if topics:
            self.results_text.insert("end", "🎯  ASOSIY MAVZULAR\n")
            for i, topic in enumerate(topics, 1):
                self.results_text.insert("end", f"  {i}. {topic}\n")
            self.results_text.insert("end", "\n")
            from tkinter import END
            self.results_text.tag_add("topic", "end-2c", "end-1c")
        
        important = result.get("muhim_ma'lumotlar", [])
        if important:
            self.results_text.insert("end", "📌  MUHIM MA'LUMOTLAR\n")
            for i, item in enumerate(important, 1):
                self.results_text.insert("end", f"  • {item}\n")
            self.results_text.insert("end", "\n")
            from tkinter import END
            self.results_text.tag_add("info", "end-2c", "end-1c")
        
        facts = result.get("asosiy_faktlar", [])
        if facts:
            self.results_text.insert("end", "🔑  ASOSIY FAKTLAR\n")
            for i, fact in enumerate(facts, 1):
                self.results_text.insert("end", f"  {i}. {fact}\n")
            self.results_text.insert("end", "\n")
            from tkinter import END
            self.results_text.tag_add("fact", "end-2c", "end-1c")
        
        qnas = result.get("savollar_javoblar", [])
        if qnas:
            self.results_text.insert("end", "💬  SAVOL-JAVOBLAR\n")
            for qna in qnas:
                q = qna.get("question", "")
                a = qna.get("answer", "")
                self.results_text.insert("end", f"  ❓ {q}\n")
                self.results_text.insert("end", f"  💡 {a}\n\n")
            from tkinter import END
            self.results_text.tag_add("qna", "end-2c", "end-2c")
        
        extra = result.get("qo'shimcha_tushuntirish", "")
        if extra:
            self.results_text.insert("end", "📝  QO'SHIMCHA\n")
            self.results_text.insert("end", f"{extra}\n")
        
        self.results_text.configure(state="disabled")
    
    def display_raw_results(self, text: str):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
        self.results_text.tag_add("placeholder", "1.0", "end")
        self.results_text.configure(state="disabled")
    
    def add_chat_message(self, sender: str, message: str):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"\n>>> {sender}:\n")
        self.chat_text.insert("end", f"{message}\n\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")
    
    def _on_question_submit(self, event=None):
        question = self.question_entry.get().strip()
        if question:
            self.app.ask_question(question)
            self.question_entry.delete(0, "end")


# Test
if __name__ == "__main__":
    import customtkinter as ctk
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = ctk.CTk()
    root.title("AI File Analyzer")
    root.geometry("900x700")
    
    class FakeApp:
        def select_file(self): pass
        def ask_question(self, q): pass
    
    window = MainWindow(root, FakeApp())
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from config_manager import save_user_config

def open_language_window(root, on_language_change):
    lang_window = tk.Toplevel(root)
    lang_window.title("Language Settings")
    lang_window.geometry("300x120")
    lang_window.option_add("*Font", ("Segoe UI", 11))
    lang_window.grab_set()

    langs = {
        "English": "en",
        "繁體中文": "zh_tw",
        "简体中文": "zh_cn",
        "日本語": "ja"
    }

    # === 容器放 Label + Combobox ===
    top_frame = ttk.Frame(lang_window)
    top_frame.pack(pady=12, padx=10)

    ttk.Label(top_frame, text="Select Language:").pack(side="left", padx=5)

    lang_var = tk.StringVar(value="English")
    combo = ttk.Combobox(top_frame, 
                         values=list(langs.keys()), 
                         textvariable=lang_var, 
                         state="readonly", width=10)
    combo.pack(side="left", padx=5)

    # === 底部 Confirm 按鈕 ===
    bottom_frame = ttk.Frame(lang_window)
    bottom_frame.pack(pady=5)
    
    def confirm_language():
        selected = combo.get()
        lang_code = langs[selected]   # e.g., "en"
        save_user_config(lang_code)
        on_language_change(lang_code)  # 更新 GUI
        lang_window.destroy()

    ttk.Button(bottom_frame, text="Confirm", command=confirm_language, width=10).pack()

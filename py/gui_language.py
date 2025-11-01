import tkinter as tk
from tkinter import ttk
from config_manager import save_user_config

def open_language_window(root, on_language_change):
    lang_window = tk.Toplevel(root)
    lang_window.title("Language Settings")
    lang_window.geometry("360x360")
    lang_window.option_add("*Font", ("Segoe UI", 14))
    lang_window.grab_set()

    langs = {
        "English": "en",
        "繁體中文": "zh_tw",
        "简体中文": "zh_cn",
        "日本語": "ja"
    }

    ttk.Label(lang_window, text="Select Language:").pack(pady=20)

    lang_var = tk.StringVar(value="English")
    combo = ttk.Combobox(lang_window, values=list(langs.keys()), textvariable=lang_var, state="readonly", width=20)
    combo.pack(pady=10)

    def confirm_language():
        selected = combo.get()
        lang_code = langs[selected]
        save_user_config(lang_code)
        on_language_change(lang_code)
        lang_window.destroy()

    ttk.Button(lang_window, text="Confirm", command=confirm_language, width=12).pack(pady=20)

import tkinter as tk
import os

# 🌐 多語系文字定義
LANG_TEXTS = {
    "en": {
        "title": "Auto File Renamer",
        "select_folder": "Select Folder",
        "include_subfolders": "Include Subfolders",
        "preview": "Preview (Tree View)",
        "rename": "Rename Files",
        "exit": "Exit",
        "log_prompt": "Would you like to generate a rename.log file?",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "preview_title": "Rename Preview",
        "no_folder": "Please select a folder first!",
        "done": "Renaming completed!",
        "folder_label": "Selected Folder:",
        "prefix_label": "Custom Prefix (optional):",
        "find_label": "Find Text (optional):",
        "replace_label": "Replace With:",
        "pattern_label": "Naming Pattern:",
        "preview_example": "Example Preview:",
        "startnum_label": "Start Number:",
        "language_select": "Select Language",
        "lang_en": "🇺🇸 English",
        "lang_zh_tw": "🇹🇼 Traditional Chinese",
        "change_lang": "🌐 Change Language",
        "patterns": [
            "① Prefix + 3-Digit Number",
            "② Original Name + 3-Digit Number",
            "③ 3-Digit Number + Original Name",
            "④ Replaced Name + 3-Digit Number",
            "⑤ Prefix + Original Name + 3-Digit Number"
        ]
    },
    "zh_tw": {
        "title": "自動檔案重新命名工具",
        "select_folder": "選擇資料夾",
        "include_subfolders": "包含子資料夾",
        "preview": "預覽（樹狀圖）",
        "rename": "開始重新命名",
        "exit": "離開",
        "log_prompt": "是否要產生 rename.log 記錄檔？",
        "confirm": "確認",
        "cancel": "取消",
        "preview_title": "預覽更名結果",
        "no_folder": "請先選擇資料夾！",
        "done": "重新命名完成！",
        "folder_label": "目前選擇的資料夾：",
        "prefix_label": "自訂名稱前綴（可留空）：",
        "find_label": "搜尋文字（可留空）：",
        "replace_label": "取代為：",
        "pattern_label": "命名格式：",
        "preview_example": "命名範例：",
        "startnum_label": "起始編號：",
        "language_select": "選擇語言",
        "lang_en": "🇺🇸 English",
        "lang_zh_tw": "🇹🇼 繁體中文",
        "change_lang": "🌐 切換語言",
        "patterns": [
            "① 前綴 + 三位數",
            "② 原檔名 + 三位數",
            "③ 三位數 + 原檔名",
            "④ 取代結果 + 三位數",
            "⑤ 前綴 + 原檔名 + 三位數"
        ]
    }
}

# 🗂️ 語言設定檔案
CONFIG_FILE = "config_lang.txt"


def load_language_setting():
    """
    讀取語言設定。如果找不到設定檔，回傳 None。
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lang = f.read().strip()
                if lang in LANG_TEXTS:
                    return lang
        except Exception:
            pass
    return None


def save_language_setting(lang_code):
    """
    儲存語言設定到 config_lang.txt
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(lang_code)
    except Exception as e:
        print(f"[Warning] Failed to save language setting: {e}")


def select_language():
    """
    顯示語言選擇視窗。
    選擇語言後會儲存設定並關閉視窗。
    """
    lang_window = tk.Tk()
    lang_window.title("Select Language / 選擇語言")
    lang_window.geometry("320x220")
    lang_window.configure(bg="#1e1e1e")

    title_label = tk.Label(
        lang_window,
        text="🌐 Select Language / 選擇語言",
        font=("Segoe UI", 12, "bold"),
        fg="gold",
        bg="#1e1e1e"
    )
    title_label.pack(pady=20)

    def set_lang(l):
        save_language_setting(l)
        lang_window.destroy()

    btn_style = {
        "font": ("Segoe UI", 11, "bold"),
        "fg": "#f0f0f0",
        "bg": "#2b2b2b",
        "activebackground": "#444",
        "width": 20,
        "height": 2,
        "relief": "flat"
    }

    # 🇺🇸 English 按鈕
    tk.Button(
        lang_window,
        text="🇺🇸 English",
        command=lambda: set_lang("en"),
        **btn_style
    ).pack(pady=5)

    # 🇹🇼 中文按鈕
    tk.Button(
        lang_window,
        text="🇹🇼 繁體中文",
        command=lambda: set_lang("zh_tw"),
        **btn_style
    ).pack(pady=5)

    lang_window.mainloop()

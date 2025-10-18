import tkinter as tk
import os

LANG_TEXTS = {
    # ---------------- English ----------------
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
        "lang_zh_cn": "🇨🇳 Simplified Chinese",
        "lang_ja": "🇯🇵 Japanese",
        "change_lang": "🌐 Change Language",
        "patterns": [
            "① Prefix + 3-Digit Number",
            "② Original Name + 3-Digit Number",
            "③ 3-Digit Number + Original Name",
            "④ Replaced Name + 3-Digit Number",
            "⑤ Prefix + Original Name + 3-Digit Number"
        ]
    },

    # ---------------- Traditional Chinese ----------------
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
        "lang_zh_cn": "🇨🇳 簡體中文",
        "lang_ja": "🇯🇵 日文",
        "change_lang": "🌐 切換語言",
        "patterns": [
            "① 前綴 + 三位數",
            "② 原檔名 + 三位數",
            "③ 三位數 + 原檔名",
            "④ 取代結果 + 三位數",
            "⑤ 前綴 + 原檔名 + 三位數"
        ]
    },

    # ---------------- Simplified Chinese ----------------
    "zh_cn": {
        "title": "自动文件重命名工具",
        "select_folder": "选择文件夹",
        "include_subfolders": "包含子文件夹",
        "preview": "预览（树状图）",
        "rename": "开始重命名",
        "exit": "退出",
        "log_prompt": "是否生成 rename.log 记录文件？",
        "confirm": "确认",
        "cancel": "取消",
        "preview_title": "预览重命名结果",
        "no_folder": "请先选择文件夹！",
        "done": "重命名完成！",
        "folder_label": "当前选择的文件夹：",
        "prefix_label": "自定义前缀（可留空）：",
        "find_label": "查找文字（可留空）：",
        "replace_label": "替换为：",
        "pattern_label": "命名格式：",
        "preview_example": "命名示例：",
        "startnum_label": "起始编号：",
        "language_select": "选择语言",
        "lang_en": "🇺🇸 英文",
        "lang_zh_tw": "🇹🇼 繁体中文",
        "lang_zh_cn": "🇨🇳 简体中文",
        "lang_ja": "🇯🇵 日语",
        "change_lang": "🌐 切换语言",
        "patterns": [
            "① 前缀 + 三位数",
            "② 原文件名 + 三位数",
            "③ 三位数 + 原文件名",
            "④ 替换结果 + 三位数",
            "⑤ 前缀 + 原文件名 + 三位数"
        ]
    },

    # ---------------- Japanese ----------------
    "ja": {
        "title": "自動ファイルリネーマー",
        "select_folder": "フォルダを選択",
        "include_subfolders": "サブフォルダを含む",
        "preview": "プレビュー（ツリービュー）",
        "rename": "名前を変更",
        "exit": "終了",
        "log_prompt": "rename.log ファイルを作成しますか？",
        "confirm": "確認",
        "cancel": "キャンセル",
        "preview_title": "リネームプレビュー",
        "no_folder": "先にフォルダを選択してください！",
        "done": "リネームが完了しました！",
        "folder_label": "選択中のフォルダ：",
        "prefix_label": "接頭辞（任意）：",
        "find_label": "検索文字列（任意）：",
        "replace_label": "置換後の文字列：",
        "pattern_label": "命名パターン：",
        "preview_example": "プレビュー例：",
        "startnum_label": "開始番号：",
        "language_select": "言語を選択",
        "lang_en": "🇺🇸 英語",
        "lang_zh_tw": "🇹🇼 繁体字中国語",
        "lang_zh_cn": "🇨🇳 簡体字中国語",
        "lang_ja": "🇯🇵 日本語",
        "change_lang": "🌐 言語を変更",
        "patterns": [
            "① 接頭辞 + 3桁番号",
            "② 元の名前 + 3桁番号",
            "③ 3桁番号 + 元の名前",
            "④ 置換後の名前 + 3桁番号",
            "⑤ 接頭辞 + 元の名前 + 3桁番号"
        ]
    }
}

CONFIG_FILE = "config_lang.txt"

def load_language_setting():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            lang = f.read().strip()
            if lang in LANG_TEXTS:
                return lang
    return None

def save_language_setting(lang_code):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(lang_code)

def select_language():
    lang_window = tk.Tk()
    lang_window.title("Select Language / 選擇語言 / 选择语言 / 言語を選択")
    lang_window.geometry("350x360")
    lang_window.configure(bg="#1e1e1e")

    title_label = tk.Label(lang_window, text="🌐 Choose Your Language",
                           font=("Segoe UI", 12, "bold"), fg="gold", bg="#1e1e1e")
    title_label.pack(pady=20)

    def set_lang(l):
        save_language_setting(l)
        lang_window.destroy()

    btn_style = {"font": ("Segoe UI", 11, "bold"), "fg": "#f0f0f0",
                 "bg": "#2b2b2b", "activebackground": "#444",
                 "width": 22, "height": 2, "relief": "flat"}

    tk.Button(lang_window, text="🇺🇸 English", command=lambda: set_lang("en"), **btn_style).pack(pady=4)
    tk.Button(lang_window, text="🇹🇼 繁體中文", command=lambda: set_lang("zh_tw"), **btn_style).pack(pady=4)
    tk.Button(lang_window, text="🇨🇳 简体中文", command=lambda: set_lang("zh_cn"), **btn_style).pack(pady=4)
    tk.Button(lang_window, text="🇯🇵 日本語", command=lambda: set_lang("ja"), **btn_style).pack(pady=4)

    lang_window.mainloop()

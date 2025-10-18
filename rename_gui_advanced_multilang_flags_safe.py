import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# -------------------------------
# 🌐 三語版本：English / 繁體中文 / 简体中文
# -------------------------------
LANG_TEXTS = {
    "en": {
        "title": "Auto File Renamer",
        "select_folder": "Select Folder",
        "include_subfolders": "Include Subfolders",
        "preview": "Preview",
        "rename": "Rename Files",
        "exit": "Exit",
        "log_prompt": "Would you like to generate a rename.log file?",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "preview_title": "Rename Preview",
        "no_folder": "Please select a folder first!",
        "done": "Renaming completed!",
        "folder_label": "Selected Folder:",
        "language_select": "Select Language",
        "lang_en": "🇺🇸 English",
        "lang_zh_tw": "🇹🇼 繁體中文",
        "lang_zh_cn": "🇨🇳 简体中文",
        "change_lang": "🌐 Change Language"
    },
    "zh_tw": {
        "title": "自動檔案重新命名工具",
        "select_folder": "選擇資料夾",
        "include_subfolders": "包含子資料夾",
        "preview": "預覽",
        "rename": "開始重新命名",
        "exit": "離開",
        "log_prompt": "是否要產生 rename.log 記錄檔？",
        "confirm": "確認",
        "cancel": "取消",
        "preview_title": "預覽更名結果",
        "no_folder": "請先選擇資料夾！",
        "done": "重新命名完成！",
        "folder_label": "目前選擇的資料夾：",
        "language_select": "選擇語言",
        "lang_en": "🇺🇸 English",
        "lang_zh_tw": "🇹🇼 繁體中文",
        "lang_zh_cn": "🇨🇳 简体中文",
        "change_lang": "🌐 切換語言"
    },
    "zh_cn": {
        "title": "自动文件重命名工具",
        "select_folder": "选择文件夹",
        "include_subfolders": "包含子文件夹",
        "preview": "预览",
        "rename": "开始重命名",
        "exit": "退出",
        "log_prompt": "是否要生成 rename.log 记录文件？",
        "confirm": "确认",
        "cancel": "取消",
        "preview_title": "预览重命名结果",
        "no_folder": "请先选择文件夹！",
        "done": "重命名完成！",
        "folder_label": "当前选择的文件夹：",
        "language_select": "选择语言",
        "lang_en": "🇺🇸 English",
        "lang_zh_tw": "🇹🇼 繁體中文",
        "lang_zh_cn": "🇨🇳 简体中文",
        "change_lang": "🌐 切换语言"
    }
}

CONFIG_FILE = "config_lang.txt"


# -------------------------------
# 💾 語言設定存取
# -------------------------------
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


# -------------------------------
# 🪟 語言選擇視窗（含旗幟）
# -------------------------------
def select_language():
    lang_window = tk.Tk()
    lang_window.title("Language / 語言選擇")
    lang_window.geometry("320x240")
    lang_window.resizable(False, False)
    lang_window.configure(bg="#1e1e1e")

    title_label = tk.Label(lang_window, text="🌐 Select Language / 選擇語言", font=("Segoe UI", 12, "bold"), fg="gold", bg="#1e1e1e")
    title_label.pack(pady=20)

    selected_lang = tk.StringVar(value="en")

    def set_lang(l):
        selected_lang.set(l)
        save_language_setting(l)
        lang_window.destroy()

    btn_style = {"font": ("Segoe UI", 11, "bold"), "fg": "#f0f0f0", "bg": "#2b2b2b", "activebackground": "#444", "width": 20, "height": 2, "relief": "flat"}

    tk.Button(lang_window, text="🇺🇸 English", command=lambda: set_lang("en"), **btn_style).pack(pady=5)
    tk.Button(lang_window, text="🇹🇼 繁體中文", command=lambda: set_lang("zh_tw"), **btn_style).pack(pady=5)
    tk.Button(lang_window, text="🇨🇳 简体中文", command=lambda: set_lang("zh_cn"), **btn_style).pack(pady=5)

    lang_window.mainloop()
    return selected_lang.get()


# -------------------------------
# 🧰 主程式介面
# -------------------------------
def main_app(language):
    text = LANG_TEXTS[language]

    # 🔒 取得目前執行的檔案名稱（.py 或 .exe）
    current_executable = os.path.basename(sys.argv[0])

    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    def preview_files():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning(text["title"], text["no_folder"])
            return

        preview_window = tk.Toplevel(root)
        preview_window.title(text["preview_title"])
        preview_window.geometry("400x400")

        text_box = tk.Text(preview_window, wrap="word")
        text_box.pack(fill="both", expand=True)

        counter = 1
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if file in ("rename_log.txt", current_executable):
                    continue
                text_box.insert("end", f"{file} -> {counter}{os.path.splitext(file)[1]}\n")
                counter += 1
            if not include_subfolders.get():
                break

    def rename_files():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning(text["title"], text["no_folder"])
            return

        counter = 1
        renamed_files = []
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if file in ("rename_log.txt", current_executable):
                    continue
                old_path = os.path.join(root_dir, file)
                ext = os.path.splitext(file)[1]
                new_name = f"{counter}{ext}"
                new_path = os.path.join(root_dir, new_name)
                os.rename(old_path, new_path)
                renamed_files.append((file, new_name))
                counter += 1
            if not include_subfolders.get():
                break

        if messagebox.askyesno(text["title"], text["log_prompt"]):
            with open(os.path.join(folder, "rename.log"), "w", encoding="utf-8") as f:
                for old, new in renamed_files:
                    f.write(f"{old} -> {new}\n")

        messagebox.showinfo(text["title"], text["done"])

    def change_language():
        save_language_setting("")  # 清除設定
        root.destroy()
        os.system(f"python \"{__file__}\"")  # 重新啟動程式

    # 建立主視窗
    root = tk.Tk()
    root.title(text["title"])
    root.geometry("460x320")

    folder_var = tk.StringVar()
    include_subfolders = tk.BooleanVar()

    tk.Label(root, text=text["folder_label"]).pack(pady=5)
    tk.Entry(root, textvariable=folder_var, width=50).pack(pady=5)
    tk.Button(root, text=text["select_folder"], command=select_folder).pack(pady=5)

    tk.Checkbutton(root, text=text["include_subfolders"], variable=include_subfolders).pack()

    tk.Button(root, text=text["preview"], command=preview_files, width=22).pack(pady=10)
    tk.Button(root, text=text["rename"], command=rename_files, width=22).pack(pady=5)
    tk.Button(root, text=text["change_lang"], command=change_language, width=22).pack(pady=5)
    tk.Button(root, text=text["exit"], command=root.destroy, width=22).pack(pady=5)

    root.mainloop()


# -------------------------------
# 🚀 啟動程式
# -------------------------------
if __name__ == "__main__":
    user_lang = load_language_setting()
    if not user_lang:
        user_lang = select_language()
    main_app(user_lang)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gui_language import open_language_window
from config_manager import load_user_config
from language_manager import LANG_TEXTS
from rename_logic import rename_files
import os
import time


def main_app():
    config = load_user_config()
    lang = config.get("language", "en")

    root = tk.Tk()
    root.title("File Renamer")
    root.geometry("1000x600")
    root.minsize(800, 500)
    root.option_add("*Font", ("Segoe UI", 12))

    text = LANG_TEXTS[lang]

    # ==================== Functions ====================
    def update_language(new_lang):
        nonlocal lang, text
        lang = new_lang
        text = LANG_TEXTS[lang]

        # 更新標籤文字
        btn_language.config(text=text["language"])
        lbl_folder.config(text=text["select_folder"])
        btn_browse.config(text=text["browse"])
        seq_frame.config(text=text["sequential"])
        replace_frame.config(text=text["replace"])
        prefix_frame.config(text=text["prefix"])
        lbl_start_number.config(text=text["start_number"])
        lbl_find.config(text=text["find"])
        lbl_replace_with.config(text=text["replace_with"])
        lbl_prefix_text.config(text=text["prefix_text"])
        lbl_func.config(text=text["function"])
        btn_start.config(text=text["start"])
        btn_exit.config(text=text["exit"])
        progress_label.config(text="")

        func_choice["values"] = [text["sequential"], text["replace"], text["prefix"]]
        if func_choice.current() == -1:
            func_choice.current(0)

        tree.heading("original", text=text["original_name"])
        tree.heading("new", text=text["new_name"])
        refresh_preview()

    # ==================== 第一層：資料夾選擇 ====================
    top_frame = ttk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=10)

    btn_language = ttk.Button(top_frame, text=text["language"],
                              command=lambda: open_language_window(root, update_language))
    btn_language.pack(side="left", padx=5)

    lbl_folder = ttk.Label(top_frame, text=text["select_folder"])
    lbl_folder.pack(side="left", padx=10)

    folder_var = tk.StringVar()
    entry_folder = ttk.Entry(top_frame, textvariable=folder_var, width=60)
    entry_folder.pack(side="left", padx=5)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)
            refresh_preview()

    btn_browse = ttk.Button(top_frame, text=text["browse"], command=browse_folder)
    btn_browse.pack(side="left", padx=5)

    # ==================== 第二層：功能設定區 ====================
    mid_frame = ttk.Frame(root)
    mid_frame.pack(fill="x", padx=10, pady=10)

    # ---- Sequential ----
    seq_frame = ttk.LabelFrame(mid_frame, text=text["sequential"])
    seq_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    lbl_start_number = ttk.Label(seq_frame, text=text["start_number"])
    lbl_start_number.pack(pady=5)
    seq_start = tk.IntVar(value=1)
    ttk.Entry(seq_frame, textvariable=seq_start, width=10).pack(pady=5)

    # ---- Replace ----
    replace_frame = ttk.LabelFrame(mid_frame, text=text["replace"])
    replace_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    lbl_find = ttk.Label(replace_frame, text=text["find"])
    lbl_find.pack(pady=5)
    find_text = tk.StringVar()
    ttk.Entry(replace_frame, textvariable=find_text, width=20).pack(pady=5)
    lbl_replace_with = ttk.Label(replace_frame, text=text["replace_with"])
    lbl_replace_with.pack(pady=5)
    replace_text = tk.StringVar()
    ttk.Entry(replace_frame, textvariable=replace_text, width=20).pack(pady=5)

    # ---- Prefix ----
    prefix_frame = ttk.LabelFrame(mid_frame, text=text["prefix"])
    prefix_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    lbl_prefix_text = ttk.Label(prefix_frame, text=text["prefix_text"])
    lbl_prefix_text.pack(pady=5)
    prefix_var = tk.StringVar()
    ttk.Entry(prefix_frame, textvariable=prefix_var, width=20).pack(pady=5)

    # ==================== 第三層：功能與操作按鈕 ====================
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(fill="x", padx=10, pady=10)

    lbl_func = ttk.Label(bottom_frame, text=text["function"])
    lbl_func.pack(side="left", padx=5)

    func_choice = ttk.Combobox(bottom_frame, values=[
        text["sequential"], text["replace"], text["prefix"]
    ], state="readonly", width=15)
    func_choice.set(text["sequential"])
    func_choice.pack(side="left", padx=5)

    # ==================== 預覽功能 ====================
    def refresh_preview(*_):
        tree.delete(*tree.get_children())
        folder = folder_var.get()
        if not folder or not os.path.isdir(folder):
            return

        files = [f for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f))
                 and not f.lower().endswith(".exe")]

        func = func_choice.get()
        for idx, filename in enumerate(sorted(files), start=seq_start.get()):
            name, ext = os.path.splitext(filename)
            preview_name = filename

            if func == text["sequential"]:
                preview_name = f"{idx:03d}{ext}"

            elif func == text["replace"]:
                if find_text.get():
                    preview_name = name.replace(find_text.get(), replace_text.get()) + ext

            elif func == text["prefix"]:
                if prefix_var.get():
                    preview_name = f"{prefix_var.get()}_{filename}"

            tree.insert("", "end", values=(filename, preview_name))

    # 綁定即時更新事件
    func_choice.bind("<<ComboboxSelected>>", refresh_preview)
    seq_start.trace_add("write", refresh_preview)
    find_text.trace_add("write", refresh_preview)
    replace_text.trace_add("write", refresh_preview)
    prefix_var.trace_add("write", refresh_preview)

    # ==================== 進度列 ====================
    progress_frame = ttk.Frame(root)
    progress_frame.pack(fill="x", padx=10, pady=5)

    progress_label = ttk.Label(progress_frame, text="", anchor="center")
    progress_label.pack(fill="x")

    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
    progress_bar.pack(fill="x", pady=5)

    # ==================== 執行按鈕 ====================
    def run_rename():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder.")
            return

        # 取得檔案清單
        files = [f for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f))
                 and not f.lower().endswith(".exe")]

        total = len(files)
        if total == 0:
            messagebox.showinfo("Info", "No files to rename.")
            return

        progress_bar["value"] = 0
        progress_bar["maximum"] = total

        # 改名邏輯 + 即時進度
        for idx, filename in enumerate(sorted(files), start=seq_start.get()):
            name, ext = os.path.splitext(filename)
            new_name = filename
            func = func_choice.get()

            if func == text["sequential"]:
                new_name = f"{idx:03d}{ext}"
            elif func == text["replace"] and find_text.get():
                new_name = name.replace(find_text.get(), replace_text.get()) + ext
            elif func == text["prefix"] and prefix_var.get():
                new_name = f"{prefix_var.get()}_{filename}"

            src = os.path.join(folder, filename)
            dst = os.path.join(folder, new_name)
            if src != dst:
                os.rename(src, dst)

            # 更新進度
            progress_bar["value"] += 1
            progress_label.config(text=f"Renaming {progress_bar['value']} / {total} files...")
            root.update()

        progress_label.config(text="✅ Rename complete!")
        messagebox.showinfo("Done", "Files renamed successfully.")
        refresh_preview()

    btn_start = ttk.Button(bottom_frame, text=text["start"], command=run_rename)
    btn_start.pack(side="left", padx=5)

    btn_exit = ttk.Button(bottom_frame, text=text["exit"], command=root.destroy)
    btn_exit.pack(side="right", padx=5)

    # ==================== 最下層：預覽表格 ====================
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=("original", "new"), show="headings")
    tree.heading("original", text=text["original_name"])
    tree.heading("new", text=text["new_name"])
    tree.column("original", width=300)
    tree.column("new", width=300)
    tree.pack(fill="both", expand=True)

    root.mainloop()

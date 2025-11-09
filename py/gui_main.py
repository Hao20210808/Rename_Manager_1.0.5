import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gui_language import open_language_window
from config_manager import load_user_config
from language_manager import LANG_TEXTS
from rename_logic import rename_files
import os, re

def main_app():
    config = load_user_config()
    lang = config.get("language", "en")

    root = tk.Tk()
    root.title("File Renamer ver1.0.5")
    root.geometry("620x480")
    root.minsize(600, 300)

    try:
        root.iconbitmap("icon.ico")
    except Exception as e:
        print("Icon 設定失敗:", e)
        
    # 字體清晰
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(".", font=("Microsoft JhengHei", 11))

    text = LANG_TEXTS[lang]

    def natural_key(name):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

    # ===== 更新語言 =====
    def update_language(new_lang_code):
        nonlocal lang, text
        lang = new_lang_code
        text = LANG_TEXTS[lang]

        # 更新 Label / Button / Combobox / Treeview
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
        func_choice["values"] = [text["sequential"], text["replace"], text["prefix"]]
        func_choice.set(text["sequential"])
        tree.heading("original", text=text["original_name"])
        tree.heading("new", text=text["new_name"])
        refresh_preview()

    # ===== 第一層：資料夾選擇 =====
    top_frame = ttk.Frame(root)
    top_frame.pack(fill="x", padx=8, pady=6)

    btn_language = ttk.Button(top_frame, text=text["language"],
                              command=lambda: open_language_window(root, update_language))
    btn_language.pack(side="left", padx=5)

    lbl_folder = ttk.Label(top_frame, text=text["select_folder"])
    lbl_folder.pack(side="left", padx=5)

    folder_var = tk.StringVar()
    entry_folder = ttk.Entry(top_frame, textvariable=folder_var, width=40)
    entry_folder.pack(side="left", padx=5)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)
            refresh_preview()

    btn_browse = ttk.Button(top_frame, text=text["browse"], command=browse_folder, width=8)
    btn_browse.pack(side="left", padx=5)

    # ===== 第二層：功能設定 =====
    mid_frame = ttk.Frame(root)
    mid_frame.pack(fill="x", padx=8, pady=6)

    seq_frame = ttk.LabelFrame(mid_frame, text=text["sequential"])
    seq_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    lbl_start_number = ttk.Label(seq_frame, text=text["start_number"])
    lbl_start_number.pack(pady=5)
    seq_start = tk.IntVar(value=1)
    ttk.Entry(seq_frame, textvariable=seq_start, width=10).pack(pady=5)

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

    prefix_frame = ttk.LabelFrame(mid_frame, text=text["prefix"])
    prefix_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    lbl_prefix_text = ttk.Label(prefix_frame, text=text["prefix_text"])
    lbl_prefix_text.pack(pady=5)
    prefix_var = tk.StringVar()
    ttk.Entry(prefix_frame, textvariable=prefix_var, width=20).pack(pady=5)

    # ===== 第三層：按鈕區 =====
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(fill="x", padx=8, pady=6)

    lbl_func = ttk.Label(bottom_frame, text=text["function"])
    lbl_func.pack(side="left", padx=5)

    func_choice = ttk.Combobox(bottom_frame, values=[
        text["sequential"], text["replace"], text["prefix"]
    ], state="readonly", width=10)
    func_choice.set(text["sequential"])
    func_choice.pack(side="left", padx=5)

    # ===== 預覽表格 =====
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=8, pady=6)

    y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
    x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")

    tree = ttk.Treeview(tree_frame, columns=("original","new"), show="headings",
                        yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    tree.heading("original", text=text["original_name"])
    tree.heading("new", text=text["new_name"])
    tree.pack(fill="both", expand=True)

    y_scroll.config(command=tree.yview)
    x_scroll.config(command=tree.xview)

    def adjust_columns(event=None):
        total_width = tree_frame.winfo_width()
        col_width = total_width // 2 - 2
        tree.column("original", width=col_width, anchor="w", stretch=True)
        tree.column("new", width=col_width, anchor="w", stretch=True)

    tree.bind("<Configure>", adjust_columns)

    # ===== 預覽刷新函數 =====
    def refresh_preview(*_):
        tree.delete(*tree.get_children())
        folder = folder_var.get()
        if not folder or not os.path.isdir(folder):
            return

        func = func_choice.get()
        start_num = seq_start.get()
        for root_dir, dirs, files in os.walk(folder):
            rel_dir = os.path.relpath(root_dir, folder)
            if rel_dir == ".":
                rel_dir = os.path.basename(folder)
            tree.insert("", "end", values=(rel_dir,""), tags=("folder",))
            # 過濾 desktop.ini 與 exe
            files = [f for f in files if not f.lower().endswith(".exe") and f.lower() != "desktop.ini"]
            files.sort(key=natural_key)
            counter = start_num
            used_names = set()
            for filename in files:
                name, ext = os.path.splitext(filename)
                preview_name = filename
                color = "black"
                if func == text["sequential"]:
                    while True:
                        candidate = f"{counter:03d}{ext}"
                        if candidate not in used_names:
                            preview_name = candidate
                            used_names.add(candidate)
                            counter +=1
                            break
                        else:
                            preview_name = f"{candidate} ⚠️"
                            color="red"
                            counter+=1
                            break
                elif func==text["replace"] and find_text.get():
                    preview_name = name.replace(find_text.get(), replace_text.get())+ext
                    if preview_name in used_names:
                        preview_name += " ⚠️"
                        color="red"
                    used_names.add(preview_name)
                elif func==text["prefix"] and prefix_var.get():
                    preview_name = f"{prefix_var.get()}_{filename}"
                    if preview_name in used_names:
                        preview_name += " ⚠️"
                        color="red"
                    used_names.add(preview_name)
                child_id = tree.insert("", "end", values=(filename, preview_name))
                if color=="red":
                    tree.item(child_id, tags=("red",))
        tree.tag_configure("red", foreground="red")
        tree.tag_configure("folder", background="#f2f2f2", font=("Microsoft JhengHei",12,"bold"))

    func_choice.bind("<<ComboboxSelected>>", refresh_preview)
    seq_start.trace_add("write", refresh_preview)
    find_text.trace_add("write", refresh_preview)
    replace_text.trace_add("write", refresh_preview)
    prefix_var.trace_add("write", refresh_preview)

    # ===== 執行按鈕 =====
    progress_frame = ttk.Frame(root)
    progress_frame.pack(fill="x", padx=8, pady=6)

    progress_label = ttk.Label(progress_frame, text="", anchor="center")
    progress_label.pack(fill="x")

    style.configure("green.Horizontal.TProgressbar",
                    troughcolor="#f0f0f0", background="#4CAF50", thickness=20)
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal",
                                   length=100, mode="determinate",
                                   style="green.Horizontal.TProgressbar")
    progress_bar.pack(fill="x", pady=5)

    def run_rename():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder.")
            return
        progress_label.config(text="")
        progress_bar["value"] = 0
        root.update_idletasks()

        success, failed, errors = rename_files(
            folder,
            func_choice.get(),
            seq_start.get(),
            find_text.get(),
            replace_text.get(),
            prefix_var.get(),
            text
        )

        total = success + failed
        progress_bar["maximum"] = max(1,total)
        for i in range(total):
            progress_bar["value"]=i+1
            progress_label.config(text=f"{i+1}/{total} files processed...")
            root.update_idletasks()

        msg = f"✅ Success: {success}\n❌ Failed: {failed}"
        if errors:
            msg += "\n\nDetails:\n" + "\n".join(errors[:10])
        messagebox.showinfo("Result", msg)
        progress_label.config(text="✅ Rename complete!")
        refresh_preview()

    btn_start = ttk.Button(bottom_frame, text=text["start"], command=run_rename)
    btn_start.pack(side="left", padx=5)
    btn_exit = ttk.Button(bottom_frame, text=text["exit"], command=root.destroy, width=5)
    btn_exit.pack(side="right", padx=5)

    root.mainloop()

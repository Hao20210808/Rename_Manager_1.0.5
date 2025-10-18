import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from rename_logic import generate_new_name, perform_rename
from language_manager import LANG_TEXTS, save_language_setting
from config_manager import load_user_config, save_user_config


def main_app(language):
    text = LANG_TEXTS[language]
    current_executable = os.path.basename(sys.argv[0])

    root = tk.Tk()
    root.title(text["title"])
    root.geometry("520x680")
    root.configure(bg="#1e1e1e")

    # ==============================
    # 讀取使用者設定
    # ==============================
    user_config = load_user_config()

    folder_var = tk.StringVar()
    prefix_var = tk.StringVar(value=user_config["prefix"])
    find_var = tk.StringVar(value=user_config["find_text"])
    replace_var = tk.StringVar(value=user_config["replace_text"])
    startnum_var = tk.StringVar(value=user_config["start_number"])
    pattern_var = tk.StringVar(value=text["patterns"][user_config["pattern_index"]])
    preview_text = tk.StringVar()
    include_subfolders = tk.BooleanVar(value=user_config["include_subfolders"])

    # ==============================
    # 預覽更新
    # ==============================
    def update_preview(*_):
        try:
            start_num = int(startnum_var.get())
        except ValueError:
            start_num = 1
        preview_text.set(generate_new_name("example.jpg", start_num, pattern_var.get(),
                                           prefix_var.get(), find_var.get(), replace_var.get()))

    for var in (prefix_var, find_var, replace_var, pattern_var, startnum_var):
        var.trace("w", update_preview)
    update_preview()

    # ==============================
    # 選擇資料夾
    # ==============================
    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    # ==============================
    # 樹狀預覽
    # ==============================
    def preview_files():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning(text["title"], text["no_folder"])
            return

        win = tk.Toplevel(root)
        win.title(text["preview_title"])
        win.geometry("680x480")
        win.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.configure("Treeview", background="#2a2a2a", foreground="white", fieldbackground="#2a2a2a")
        style.map("Treeview", background=[("selected", "#444")])

        tree = ttk.Treeview(win, columns=("new_name"), show="tree headings")
        tree.heading("#0", text="File / Folder")
        tree.heading("new_name", text="Renamed To")
        tree.column("#0", width=320)
        tree.column("new_name", width=320)
        tree.pack(fill="both", expand=True)

        counter = [int(startnum_var.get())]

        def insert_tree(parent, path):
            for entry in os.scandir(path):
                if entry.is_file():
                    if entry.name in ("rename_log.txt", "rename.log", current_executable):
                        continue
                    new_name = generate_new_name(entry.name, counter[0], pattern_var.get(),
                                                 prefix_var.get(), find_var.get(), replace_var.get())
                    tree.insert(parent, "end", text=entry.name, values=(new_name,))
                    counter[0] += 1
                elif entry.is_dir() and include_subfolders.get():
                    node = tree.insert(parent, "end", text=f"📁 {entry.name}")
                    insert_tree(node, entry.path)

        insert_tree("", folder)

    # ==============================
    # 執行重新命名
    # ==============================
    def rename_files():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning(text["title"], text["no_folder"])
            return

        renamed = perform_rename(
            folder,
            include_subfolders.get(),
            startnum_var.get(),
            pattern_var.get(),
            prefix_var.get(),
            find_var.get(),
            replace_var.get(),
            exclude_files=["rename_log.txt", "rename.log", current_executable]
        )

        if messagebox.askyesno(text["title"], text["log_prompt"]):
            with open(os.path.join(folder, "rename.log"), "w", encoding="utf-8") as f:
                for o, n in renamed:
                    f.write(f"{o} -> {n}\n")

        messagebox.showinfo(text["title"], text["done"])

    # ==============================
    # 切換語言
    # ==============================
    def change_language():
        save_language_setting("")
        root.destroy()
        os.system(f"python \"{__file__}\"")

    # ==============================
    # 重置設定
    # ==============================
    def reset_config():
        if messagebox.askyesno(text["title"], "確定要重置所有設定嗎？（這會清除 config_user.json）"):
            try:
                os.remove("config_user.json")
            except FileNotFoundError:
                pass
            messagebox.showinfo(text["title"], "設定已重置，請重新啟動程式。")

    # ==============================
    # 離開時儲存設定
    # ==============================
    def on_close():
        save_user_config({
            "prefix": prefix_var.get(),
            "find_text": find_var.get(),
            "replace_text": replace_var.get(),
            "start_number": startnum_var.get(),
            "pattern_index": text["patterns"].index(pattern_var.get()) if pattern_var.get() in text["patterns"] else 0,
            "include_subfolders": include_subfolders.get()
        })
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # ==============================
    # GUI Layout
    # ==============================
    def label(text_):
        return tk.Label(root, text=text_, fg="white", bg="#1e1e1e", anchor="w")

    label(text["folder_label"]).pack(pady=(10, 2))
    tk.Entry(root, textvariable=folder_var, width=55, bg="#2b2b2b", fg="white", relief="flat").pack()
    tk.Button(root, text=text["select_folder"], command=select_folder, bg="#444", fg="white", relief="flat").pack(pady=5)

    label(text["prefix_label"]).pack(); tk.Entry(root, textvariable=prefix_var, bg="#2b2b2b", fg="white", relief="flat").pack()
    label(text["find_label"]).pack(); tk.Entry(root, textvariable=find_var, bg="#2b2b2b", fg="white", relief="flat").pack()
    label(text["replace_label"]).pack(); tk.Entry(root, textvariable=replace_var, bg="#2b2b2b", fg="white", relief="flat").pack()
    label(text["startnum_label"]).pack(); tk.Entry(root, textvariable=startnum_var, bg="#2b2b2b", fg="white", relief="flat").pack()

    label(text["pattern_label"]).pack()
    ttk.Combobox(root, textvariable=pattern_var, values=text["patterns"], width=40, state="readonly").pack()

    tk.Label(root, text=text["preview_example"], fg="gold", bg="#1e1e1e").pack(pady=(8, 2))
    tk.Label(root, textvariable=preview_text, fg="#00ffcc", font=("Consolas", 11, "bold"), bg="#1e1e1e").pack()

    tk.Checkbutton(root, text=text["include_subfolders"], variable=include_subfolders,
                   fg="white", bg="#1e1e1e", selectcolor="#333").pack(pady=5)

    # Buttons
    btn_style = {"bg": "#444", "fg": "white", "relief": "flat", "width": 20, "height": 1}
    tk.Button(root, text=text["preview"], command=preview_files, **btn_style).pack(pady=5)
    tk.Button(root, text=text["rename"], command=rename_files, **btn_style).pack(pady=5)
    tk.Button(root, text=text["change_lang"], command=change_language, **btn_style).pack(pady=5)
    tk.Button(root, text="🧹 Reset Settings", command=reset_config, **btn_style).pack(pady=5)
    tk.Button(root, text=text["exit"], command=on_close, **btn_style).pack(pady=(10, 10))

    root.mainloop()

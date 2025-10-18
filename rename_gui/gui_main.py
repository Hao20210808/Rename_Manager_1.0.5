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
    user_config = load_user_config()

    folder_var = tk.StringVar()
    prefix_var = tk.StringVar(value=user_config["prefix"])
    find_var = tk.StringVar(value=user_config["find_text"])
    replace_var = tk.StringVar(value=user_config["replace_text"])
    startnum_var = tk.StringVar(value=user_config["start_number"])
    pattern_var = tk.StringVar(value=text["patterns"][user_config["pattern_index"]])
    include_subfolders = tk.BooleanVar(value=user_config["include_subfolders"])


    root = tk.Tk()
    root.title(text["title"])
    root.geometry("520x640")

    folder_var = tk.StringVar()
    prefix_var = tk.StringVar()
    find_var = tk.StringVar()
    replace_var = tk.StringVar()
    startnum_var = tk.StringVar(value="1")
    pattern_var = tk.StringVar(value=text["patterns"][0])
    preview_text = tk.StringVar()
    include_subfolders = tk.BooleanVar()

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

    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    def preview_files():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning(text["title"], text["no_folder"])
            return

        win = tk.Toplevel(root)
        win.title(text["preview_title"])
        win.geometry("640x460")
        tree = ttk.Treeview(win, columns=("new_name"), show="tree headings")
        tree.heading("#0", text="File")
        tree.heading("new_name", text="Renamed To")
        tree.column("#0", width=300)
        tree.column("new_name", width=300)
        tree.pack(fill="both", expand=True)

        counter = [int(startnum_var.get())]

        def insert_tree(parent, path):
            for entry in os.scandir(path):
                if entry.is_file():
                    if entry.name in ("rename_log.txt", current_executable):
                        continue
                    new_name = generate_new_name(entry.name, counter[0], pattern_var.get(),
                                                 prefix_var.get(), find_var.get(), replace_var.get())
                    tree.insert(parent, "end", text=entry.name, values=(new_name,))
                    counter[0] += 1
                elif entry.is_dir() and include_subfolders.get():
                    node = tree.insert(parent, "end", text=f"📁 {entry.name}")
                    insert_tree(node, entry.path)
        insert_tree("", folder)

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
            exclude_files=["rename_log.txt", current_executable]
        )

        if messagebox.askyesno(text["title"], text["log_prompt"]):
            with open(os.path.join(folder, "rename.log"), "w", encoding="utf-8") as f:
                for o, n in renamed:
                    f.write(f"{o} -> {n}\n")

        messagebox.showinfo(text["title"], text["done"])

    def change_language():
        save_language_setting("")
        root.destroy()
        os.system(f"python \"{__file__}\"")

    tk.Label(root, text=text["folder_label"]).pack(pady=5)
    tk.Entry(root, textvariable=folder_var, width=55).pack()
    tk.Button(root, text=text["select_folder"], command=select_folder).pack(pady=5)
    tk.Label(root, text=text["prefix_label"]).pack(); tk.Entry(root, textvariable=prefix_var).pack()
    tk.Label(root, text=text["find_label"]).pack(); tk.Entry(root, textvariable=find_var).pack()
    tk.Label(root, text=text["replace_label"]).pack(); tk.Entry(root, textvariable=replace_var).pack()
    tk.Label(root, text=text["startnum_label"]).pack(); tk.Entry(root, textvariable=startnum_var).pack()
    tk.Label(root, text=text["pattern_label"]).pack()
    ttk.Combobox(root, textvariable=pattern_var, values=text["patterns"], width=40, state="readonly").pack()
    tk.Label(root, text=text["preview_example"], fg="gold").pack(pady=(8, 2))
    tk.Label(root, textvariable=preview_text, fg="#00ffcc", font=("Consolas", 11, "bold")).pack()
    tk.Checkbutton(root, text=text["include_subfolders"], variable=include_subfolders).pack()
    tk.Button(root, text=text["preview"], command=preview_files).pack(pady=5)
    tk.Button(root, text=text["rename"], command=rename_files).pack(pady=5)
    tk.Button(root, text=text["change_lang"], command=change_language).pack(pady=5)
    def exit_and_save():
        save_user_config({
            "prefix": prefix_var.get(),
            "find_text": find_var.get(),
            "replace_text": replace_var.get(),
            "start_number": startnum_var.get(),
            "pattern_index": text["patterns"].index(pattern_var.get()),
            "include_subfolders": include_subfolders.get()
        })
        root.destroy()

    tk.Button(root, text=text["exit"], command=exit_and_save).pack(pady=5)

    root.mainloop()

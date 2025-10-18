import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from threading import Thread

class RenameTool:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 Rename Manager Pro v2.0")
        self.root.geometry("950x640")
        self.root.resizable(False, False)

        # 狀態變數
        self.folder_path = tk.StringVar()
        self.start_num = tk.IntVar(value=1)
        self.zero_fill = tk.IntVar(value=3)
        self.extension_filter = tk.StringVar(value="全部")
        self.preview_data = []
        self.rename_log = []
        self.progress_value = tk.IntVar(value=0)

        self.create_widgets()

    # === 建立介面 ===
    def create_widgets(self):
        frm_top = tk.Frame(self.root, pady=10)
        frm_top.pack(fill="x")

        tk.Label(frm_top, text="選擇資料夾：", font=("微軟正黑體", 10)).pack(side="left", padx=5)
        tk.Entry(frm_top, textvariable=self.folder_path, width=70).pack(side="left", padx=5)
        tk.Button(frm_top, text="📂 瀏覽", command=self.select_folder).pack(side="left", padx=5)

        frm_options = tk.LabelFrame(self.root, text="改名設定", padx=10, pady=5)
        frm_options.pack(fill="x", padx=10, pady=5)

        tk.Label(frm_options, text="起始編號：").grid(row=0, column=0)
        tk.Entry(frm_options, textvariable=self.start_num, width=6).grid(row=0, column=1, padx=5)
        tk.Label(frm_options, text="前導零長度：").grid(row=0, column=2)
        tk.Entry(frm_options, textvariable=self.zero_fill, width=6).grid(row=0, column=3, padx=5)
        tk.Label(frm_options, text="副檔名篩選（例：jpg,png 或 全部）：").grid(row=0, column=4)
        tk.Entry(frm_options, textvariable=self.extension_filter, width=15).grid(row=0, column=5, padx=5)

        frm_btn = tk.Frame(self.root, pady=5)
        frm_btn.pack(fill="x")

        tk.Button(frm_btn, text="🌳 預覽樹狀結構", width=18, command=self.preview).pack(side="left", padx=5)
        tk.Button(frm_btn, text="🚀 執行改名", width=18, command=lambda: Thread(target=self.rename_files).start()).pack(side="left", padx=5)
        tk.Button(frm_btn, text="↩️ 還原名稱", width=18, command=self.restore_files).pack(side="left", padx=5)
        tk.Button(frm_btn, text="❌ 離開", width=10, command=self.root.quit).pack(side="right", padx=5)

        self.tree = ttk.Treeview(self.root, columns=("old", "new"), show="tree headings", height=22)
        self.tree.heading("old", text="原始檔名")
        self.tree.heading("new", text="改名預覽")
        self.tree.column("#0", width=250)
        self.tree.column("old", width=300)
        self.tree.column("new", width=300)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        frm_bottom = tk.Frame(self.root, pady=5)
        frm_bottom.pack(fill="x", padx=10)
        ttk.Progressbar(frm_bottom, variable=self.progress_value, maximum=100).pack(fill="x", expand=True)
        self.status = tk.StringVar(value="請選擇資料夾以開始。")
        tk.Label(self.root, textvariable=self.status, anchor="w", bg="#f0f0f0").pack(fill="x", padx=10, pady=5)

    # === 資料夾選擇 ===
    def select_folder(self):
        folder = filedialog.askdirectory(title="選擇要改名的資料夾")
        if folder:
            self.folder_path.set(folder)
            self.status.set(f"已選擇資料夾：{folder}")

    # === 預覽 ===
    def preview(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("警告", "請先選擇資料夾！")
            return
        self.tree.delete(*self.tree.get_children())
        self.preview_data.clear()

        self.status.set("正在建立預覽樹狀結構...")
        self.root.update_idletasks()
        self.add_tree_nodes("", Path(folder))
        self.status.set("預覽完成，可開始改名。")

    def add_tree_nodes(self, parent, path, level=0):
        node = self.tree.insert(parent, "end", text=f"📁 {path.name}", values=("", ""))
        ext_filter = [e.strip().lower() for e in self.extension_filter.get().split(",")] if self.extension_filter.get() != "全部" else []
        count = self.start_num.get()

        for file in sorted(path.iterdir()):
            if file.is_dir():
                self.add_tree_nodes(node, file, level + 1)
            elif file.name not in ("rename_log.txt", os.path.basename(__file__)):
                if ext_filter and file.suffix.lower().replace(".", "") not in ext_filter:
                    continue
                ext = file.suffix
                new_name = f"{str(count).zfill(self.zero_fill.get())}{ext}"
                self.tree.insert(node, "end", text="", values=(file.name, new_name))
                self.preview_data.append((file, file.parent / new_name))
                count += 1

    # === 執行改名 ===
    def rename_files(self):
        if not self.preview_data:
            messagebox.showwarning("警告", "請先建立預覽！")
            return
        if not messagebox.askyesno("確認", "確定要執行改名嗎？"):
            return

        total = len(self.preview_data)
        renamed = 0
        self.progress_value.set(0)
        self.rename_log.clear()

        for idx, (old_path, new_path) in enumerate(self.preview_data, 1):
            if not old_path.exists():
                continue
            try:
                old_path.rename(new_path)
                self.rename_log.append((str(new_path), str(old_path)))
                renamed += 1
            except Exception as e:
                print(f"❌ {e}")
            self.progress_value.set(int(idx / total * 100))
            self.status.set(f"正在改名：{idx}/{total}")
            self.root.update_idletasks()

        if renamed > 0:
            if messagebox.askyesno("是否建立記錄", "是否要建立 rename_log.txt？"):
                log_path = Path(self.folder_path.get()) / "rename_log.txt"
                with open(log_path, "w", encoding="utf-8") as f:
                    for new, old in self.rename_log:
                        f.write(f"{new}|{old}\n")
                messagebox.showinfo("完成", f"✅ 已建立 rename_log.txt\n共改名 {renamed} 個檔案。")
            else:
                messagebox.showinfo("完成", f"✅ 改名完成，共 {renamed} 個檔案。")

        self.progress_value.set(100)
        self.status.set(f"改名完成，共 {renamed} 個檔案。")

    # === 還原 ===
    def restore_files(self):
        folder = Path(self.folder_path.get())
        log_path = folder / "rename_log.txt"
        if not log_path.exists():
            messagebox.showerror("錯誤", "找不到 rename_log.txt，無法還原。")
            return

        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        restored = 0
        for line in lines:
            new, old = line.strip().split("|")
            new_path = Path(new)
            old_path = Path(old)
            if new_path.exists():
                try:
                    new_path.rename(old_path)
                    restored += 1
                except:
                    pass

        messagebox.showinfo("完成", f"↩️ 已還原 {restored} 個檔案。")
        self.status.set(f"已還原 {restored} 個檔案。")

# === 主程式入口 ===
if __name__ == "__main__":
    root = tk.Tk()
    app = RenameTool(root)
    root.mainloop()

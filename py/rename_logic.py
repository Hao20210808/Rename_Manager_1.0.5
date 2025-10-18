import os
import shutil

def rename_files(folder, func_type, start_num, find_str, replace_str, prefix, text):
    if not folder or not os.path.isdir(folder):
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    backup = {}

    for idx, filename in enumerate(sorted(files), start=start_num):
        name, ext = os.path.splitext(filename)
        new_name = filename

        if func_type == text["sequential"]:
            new_name = f"{idx:03d}{ext}"

        elif func_type == text["replace"]:
            if not find_str:
                continue
            new_name = name.replace(find_str, replace_str) + ext

        elif func_type == text["prefix"]:
            new_name = f"{prefix}_{filename}"

        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)
        if src != dst:
            os.rename(src, dst)
            backup[new_name] = filename

    # 建立還原檔
    with open(os.path.join(folder, "rename_log.txt"), "w", encoding="utf-8") as f:
        for new, old in backup.items():
            f.write(f"{new}|{old}\n")

def undo_rename(folder, text):
    log_file = os.path.join(folder, "rename_log.txt")
    if not os.path.exists(log_file):
        return

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        new, old = line.strip().split("|")
        src = os.path.join(folder, new)
        dst = os.path.join(folder, old)
        if os.path.exists(src):
            os.rename(src, dst)

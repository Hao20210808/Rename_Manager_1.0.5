# file: rename_logic.py
import os
import re

def natural_key(name):
    """用於自然排序：001, 002, 010, 100..."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

def rename_files(folder, func_type, start_num, find_str, replace_str, prefix, text):
    """
    執行批次重新命名功能。
    支援三種模式：
      1️⃣ 排序命名 (Sequential)
      2️⃣ 批次取代 (Replace)
      3️⃣ 加上前綴 (Prefix)
    自動略過資料夾、.exe 檔案與 desktop.ini。
    """
    if not folder or not os.path.isdir(folder):
        return 0, 0, ["Invalid folder"]

    success, failed = 0, 0
    errors = []

    for root_dir, _, files in os.walk(folder):
        files = [f for f in files if not f.lower().endswith(".exe") and f.lower() != "desktop.ini"]
        files.sort(key=natural_key)
        if not files:
            continue

        used_names = set()  # 只追蹤已改過的檔名
        counter = start_num

        for filename in files:
            src = os.path.join(root_dir, filename)
            name, ext = os.path.splitext(filename)
            new_name = filename

            try:
                if func_type == text["sequential"]:
                    while True:
                        candidate = f"{counter:03d}{ext}"
                        if candidate not in used_names and not os.path.exists(os.path.join(root_dir, candidate)):
                            new_name = candidate
                            used_names.add(candidate)
                            counter += 1
                            break
                        counter += 1

                elif func_type == text["replace"] and find_str:
                    new_name = name.replace(find_str, replace_str) + ext
                    if new_name in used_names:
                        new_name += "_dup"
                    used_names.add(new_name)

                elif func_type == text["prefix"] and prefix:
                    new_name = f"{prefix}_{filename}"
                    if new_name in used_names:
                        new_name += "_dup"
                    used_names.add(new_name)

                dst = os.path.join(root_dir, new_name)
                if src != dst:
                    os.rename(src, dst)
                    success += 1

            except Exception as e:
                failed += 1
                rel_path = os.path.relpath(src, folder)
                errors.append(f"{rel_path} → {new_name} ❌ {e}")

    return success, failed, errors

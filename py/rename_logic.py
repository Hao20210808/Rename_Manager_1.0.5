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
    自動略過資料夾與 .exe 檔案。

    回傳：
      (成功筆數, 失敗筆數, 錯誤訊息列表)
    """

    if not folder or not os.path.isdir(folder):
        return 0, 0, ["Invalid folder"]

    files = [f for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))
             and not f.lower().endswith(".exe")]

    if not files:
        return 0, 0, ["No files found"]

    files.sort(key=natural_key)

    success = 0
    failed = 0
    errors = []

    used_names = set(os.listdir(folder))
    counter = start_num

    for filename in files:
        src = os.path.join(folder, filename)
        name, ext = os.path.splitext(filename)
        new_name = filename  # 預設不變

        try:
            # === 1️⃣ 排序 ===
            if func_type == text["sequential"]:
                # 找到未重複的遞增名稱
                while True:
                    candidate = f"{counter:03d}{ext}"
                    dst = os.path.join(folder, candidate)
                    if not os.path.exists(dst) and candidate not in used_names:
                        new_name = candidate
                        used_names.add(candidate)
                        counter += 1
                        break
                    counter += 1

            # === 2️⃣ 取代 ===
            elif func_type == text["replace"] and find_str:
                new_name = name.replace(find_str, replace_str) + ext
                if new_name in used_names:
                    raise FileExistsError(f"Duplicate filename: {new_name}")
                used_names.add(new_name)

            # === 3️⃣ 前綴 ===
            elif func_type == text["prefix"] and prefix:
                new_name = f"{prefix}_{filename}"
                if new_name in used_names:
                    raise FileExistsError(f"Duplicate filename: {new_name}")
                used_names.add(new_name)

            # === 執行改名 ===
            dst = os.path.join(folder, new_name)
            if src != dst:
                os.rename(src, dst)
                success += 1

        except Exception as e:
            failed += 1
            errors.append(f"{filename} → {new_name} ❌ {e}")

    return success, failed, errors

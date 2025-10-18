import os

def rename_files(folder, func_type, start_num, find_str, replace_str, prefix, text):
    """
    批次重新命名檔案（排序、取代、前綴）
    不處理資料夾與 .exe 檔案
    排序功能會自動略過已存在的檔案名稱
    """
    if not folder or not os.path.isdir(folder):
        return

    files = [f for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))
             and not f.lower().endswith(".exe")]

    files.sort()

    for filename in files:
        name, ext = os.path.splitext(filename)
        new_name = filename

        # === 排序功能 ===
        if func_type == text["sequential"]:
            counter = start_num
            # 找到第一個可用的檔名
            while True:
                new_name = f"{counter:03d}{ext}"
                dst = os.path.join(folder, new_name)
                if not os.path.exists(dst):  # 找到可用編號
                    break
                counter += 1
            start_num = counter + 1  # 下一輪從下個編號開始

        # === 取代功能 ===
        elif func_type == text["replace"]:
            if find_str:
                new_name = name.replace(find_str, replace_str) + ext

        # === 前綴功能 ===
        elif func_type == text["prefix"]:
            if prefix:
                new_name = f"{prefix}_{filename}"

        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)

        if src != dst:
            try:
                os.rename(src, dst)
            except Exception as e:
                print(f"❌ Rename failed for {filename}: {e}")

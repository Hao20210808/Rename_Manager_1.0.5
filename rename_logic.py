import os


def generate_new_name(file, counter, pattern, prefix, find_text, replace_text):
    """
    根據使用者設定產生新的檔案名稱
    """
    name, ext = os.path.splitext(file)

    # 進行文字取代（若有輸入）
    replaced_name = name.replace(find_text, replace_text) if find_text else name

    # 編號格式（補零）
    numbered = f"{counter:03d}"

    # 各種命名模式
    if "①" in pattern:
        # 前綴 + 三位數
        new_name = f"{prefix + ' ' if prefix else ''}{numbered}{ext}"

    elif "②" in pattern:
        # 原檔名 + 三位數
        new_name = f"{name}_{numbered}{ext}"

    elif "③" in pattern:
        # 三位數 + 原檔名
        new_name = f"{numbered}_{name}{ext}"

    elif "④" in pattern:
        # 取代結果 + 三位數
        new_name = f"{replaced_name}_{numbered}{ext}"

    elif "⑤" in pattern:
        # 前綴 + 原檔名 + 三位數
        new_name = f"{prefix + '_' if prefix else ''}{name}_{numbered}{ext}"

    else:
        # 預設：原檔名 + 三位數
        new_name = f"{name}_{numbered}{ext}"

    return new_name


def perform_rename(folder, include_subfolders, start_number, pattern,
                   prefix, find_text, replace_text, exclude_files=None):
    """
    執行實際的重新命名作業
    - folder: 目標資料夾
    - include_subfolders: 是否包含子資料夾
    - start_number: 起始編號
    - pattern: 命名格式
    - prefix: 自訂前綴文字
    - find_text: 要尋找的文字
    - replace_text: 要取代成的文字
    - exclude_files: 不要被改名的檔案清單（例如執行檔或日誌）
    """
    if exclude_files is None:
        exclude_files = []

    renamed_files = []
    counter = int(start_number)

    # 使用 os.walk 走訪資料夾
    for root_dir, dirs, files in os.walk(folder):
        # 只更改檔案，不更改資料夾名稱
        for file in files:
            # 跳過排除名單
            if file in exclude_files:
                continue

            old_path = os.path.join(root_dir, file)

            # 產生新名稱
            new_name = generate_new_name(
                file,
                counter,
                pattern,
                prefix,
                find_text,
                replace_text
            )

            new_path = os.path.join(root_dir, new_name)

            # 如果新舊名稱不同才執行改名
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    renamed_files.append((file, new_name))
                    counter += 1
                except Exception as e:
                    print(f"[Error] Failed to rename {file}: {e}")

        # 若不包含子資料夾，就只跑第一層
        if not include_subfolders:
            break

    return renamed_files


# ✅ 若獨立執行此檔案，進行簡單測試
if __name__ == "__main__":
    test_folder = os.getcwd()
    renamed = perform_rename(
        folder=test_folder,
        include_subfolders=False,
        start_number="1",
        pattern="① Prefix + 3-Digit Number",
        prefix="Test",
        find_text="old",
        replace_text="new",
        exclude_files=["rename_logic.py", "rename_log.txt"]
    )
    print("Renamed files:", renamed)

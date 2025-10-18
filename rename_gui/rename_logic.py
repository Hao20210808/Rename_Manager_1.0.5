import os

def generate_new_name(file, counter, pattern, prefix, find_text, replace_text):
    name, ext = os.path.splitext(file)
    replaced_name = name.replace(find_text, replace_text) if find_text else name
    numbered = f"{counter:03d}"

    if "①" in pattern:
        new_name = f"{prefix + ' ' if prefix else ''}{numbered}{ext}"
    elif "②" in pattern:
        new_name = f"{name}_{numbered}{ext}"
    elif "③" in pattern:
        new_name = f"{numbered}_{name}{ext}"
    elif "④" in pattern:
        new_name = f"{replaced_name}_{numbered}{ext}"
    elif "⑤" in pattern:
        new_name = f"{prefix + '_' if prefix else ''}{name}_{numbered}{ext}"
    else:
        new_name = f"{name}_{numbered}{ext}"
    return new_name

def perform_rename(folder, include_subfolders, start_number, pattern, prefix, find_text, replace_text, exclude_files):
    renamed_files = []
    counter = int(start_number)

    for root_dir, _, files in os.walk(folder):
        for file in files:
            if file in exclude_files:
                continue
            old_path = os.path.join(root_dir, file)
            new_name = generate_new_name(file, counter, pattern, prefix, find_text, replace_text)
            new_path = os.path.join(root_dir, new_name)
            os.rename(old_path, new_path)
            renamed_files.append((file, new_name))
            counter += 1
        if not include_subfolders:
            break

    return renamed_files

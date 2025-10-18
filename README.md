# Auto File Renamer
## Overview
### a Python-based utility that automatically renames all files within a selected folder.

- Files will be renamed sequentially starting from 001, 
- The program ensures that filenames **do not conflict or overwrite existing files**.
- GUI (no command-line knowledge required for users).

## Features

- 🗂 Automatic sequential renaming (e.g., 1.jpg, 2.jpg, 3.jpg, …)
- 📁 Supports subfolders : optional recursive renaming mode
- 🚫 Excludes specific files (e.g., the main script, log files, or configuration files)
- 🔍 Preview mode : shows how filenames will change before applying
- 🧱 Folder-safe : directories are never renamed
- 🧾 Optional rename log : user can choose whether to save a record after renaming

## Usage

1. Launch the program:
`python rename_gui_advanced.py
`

2. In the GUI:

- Select the folder you want to rename files in. 
- Choose whether to include subfolders.
- Click Preview to see the renaming plan.
- Click Rename to execute.

3. After completion, you’ll be asked whether to generate a rename.log file containing all changes.

## Notes

- The program **does not rename folders** — only files inside them.
- Files like _rename_log.txt_ and the program itself (.exe) are automatically excluded from renaming.
- If two files would end up with **the same name**, the program handles them safely by numbering them sequentially.

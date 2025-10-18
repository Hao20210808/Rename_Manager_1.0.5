import json
import os

CONFIG_FILE = "config_user.json"

DEFAULT_CONFIG = {
    "prefix": "",
    "find_text": "",
    "replace_text": "",
    "start_number": "1",
    "pattern_index": 0,
    "include_subfolders": False
}

def load_user_config():
    """讀取使用者上次設定（若不存在則回傳預設值）"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_CONFIG, **data}
        except Exception:
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_user_config(config_dict):
    """儲存使用者設定至 config_user.json"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[Warning] Failed to save user config: {e}")

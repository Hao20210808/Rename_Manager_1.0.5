import json
import os

CONFIG_FILE = "config.json"

def load_user_config():
    if not os.path.exists(CONFIG_FILE):
        return {"language": "en"}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"language": "en"}

def save_user_config(lang_code):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"language": lang_code}, f, indent=4, ensure_ascii=False)

import json
import os

# 設定檔名稱
CONFIG_FILE = "config_user.json"

# 預設設定
default_config = {
    "prefix": "",
    "find_text": "",
    "replace_text": "",
    "start_number": "1",
    "pattern_index": 0,
    "include_subfolders": False
}


def load_user_config():
    """
    讀取使用者設定檔。
    若檔案不存在或損壞，則自動回傳預設設定。
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 合併預設值（確保新版本多出的鍵不會出錯）
                return {**default_config, **data}
        except (json.JSONDecodeError, OSError):
            print("[Warning] Config file is corrupted, resetting to default.")
            return default_config.copy()
    else:
        return default_config.copy()


def save_user_config(data):
    """
    儲存使用者設定到 JSON 檔案。
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[Warning] Failed to save config: {e}")


def reset_user_config():
    """
    重置使用者設定檔，恢復為預設值。
    """
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        save_user_config(default_config)
        print("[Info] User configuration has been reset to default.")
    except Exception as e:
        print(f"[Error] Failed to reset config: {e}")


def ensure_config_exists():
    """
    確保設定檔存在，若無則自動建立。
    """
    if not os.path.exists(CONFIG_FILE):
        save_user_config(default_config)


# 測試用（可獨立執行）
if __name__ == "__main__":
    print("🔧 Config Manager Test")

    ensure_config_exists()
    config = load_user_config()
    print("目前設定：", config)

    print("\n📝 修改設定...")
    config["prefix"] = "照片"
    config["start_number"] = "10"
    save_user_config(config)

    print("✅ 重新載入設定：", load_user_config())

    print("\n🔁 重置設定...")
    reset_user_config()
    print("🔄 重置後設定：", load_user_config())

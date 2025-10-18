from language_manager import load_language_setting, select_language
from gui_main import main_app

if __name__ == "__main__":
    # 嘗試讀取語言設定
    lang = load_language_setting()

    # 若未設定語言，顯示語言選擇視窗
    if not lang:
        select_language()
        lang = load_language_setting()

    # 啟動主介面
    main_app(lang)

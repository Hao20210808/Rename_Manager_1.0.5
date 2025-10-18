from language_manager import load_language_setting, select_language
from gui_main import main_app

if __name__ == "__main__":
    lang = load_language_setting()
    if not lang:
        select_language()
        lang = load_language_setting()
    main_app(lang)

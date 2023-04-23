# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from datetime import datetime

from typing import Dict
import random
import string
import json


class Constant:
    @staticmethod
    def id_generator() -> str:
        generated_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return generated_id

    @staticmethod
    def load_stylesheets_main() -> str:
        with open("assets/stylesheets/stylesheets_main.css", "r+", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def load_stylesheets_dialog() -> str:
        with open("assets/stylesheets/stylesheets_dialog.css", "r+", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def load_stylesheets_display() -> str:
        with open("assets/stylesheets/stylesheets_display.css", "r+", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def get_font() -> str:
        font_name = "assets/fonts/Lexend-VariableFont.ttf"
        return font_name

    @staticmethod
    def get_icon() -> str:
        file_name = "icon.ico"
        return file_name

    @staticmethod
    def get_music() -> str:
        filename = "assets/storage/I only say morning.mp3"
        return filename

    @staticmethod
    def current_time() -> str:
        get_timezone = datetime.utcnow().astimezone().tzinfo
        time_now = datetime.now(get_timezone)
        display_current_time = time_now.strftime("%H:%M:%S")

        return display_current_time

    @staticmethod
    def load_config() -> Dict[str, str]:
        filename = "config.json"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(filename, "w", encoding="utf-8") as file:
                document = {"play_music": True, "current_directory": ""}
                file.write(json.dumps(document, indent=4))

            with open(filename, "r", encoding="utf-8") as _file:
                return json.load(_file)

    @staticmethod
    def change_config(keyword: str, value: str) -> None:
        filename = "config.json"
        with open(filename, "r", encoding="utf-8") as file:
            get_json = json.load(file)
            get_json[keyword] = value

        with open(filename, "w", encoding="utf-8") as _file:
            save_json = json.dumps(get_json, indent=4)
            _file.write(save_json)

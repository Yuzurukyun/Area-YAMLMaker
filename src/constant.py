# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from datetime import datetime

import random
import string


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
    def current_time():
        get_timezone = datetime.utcnow().astimezone().tzinfo
        time_now = datetime.now(get_timezone)
        display_current_time = time_now.strftime("%H:%M:%S")

        return display_current_time

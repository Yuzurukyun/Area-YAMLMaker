# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'YAML Maker.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtWidgets import QApplication
from src.main_window import YAMLMaker
import sys

if __name__ == "__main__":
    try:
        from ctypes import windll
        my_app_id = 'dro.yamlmaker.area.list'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    except ImportError:
        from ctypes import windll
        pass

    app = QApplication(sys.argv)
    program = YAMLMaker()
    program.show()
    sys.exit(app.exec_())
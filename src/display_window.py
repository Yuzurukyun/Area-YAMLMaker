# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.constant import Constant
from src.yaml_dataclass import TableData

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt


class DisplayScreen(QtWidgets.QDialog):
    def __init__(self, main_window):
        super(DisplayScreen, self).__init__()
        self.main_window = main_window
        self.current_table_name = str()

        self.setObjectName("DisplayContent")
        self.setEnabled(True)
        self.setFixedSize(600, 350)
        self.setStyleSheet(Constant.load_stylesheets_display())

        self.display_text = QtWidgets.QPlainTextEdit(self)
        self.display_text.setGeometry(QtCore.QRect(20, 50, 561, 281))
        self.display_text.setObjectName("display_text")

        self.display_area = QtWidgets.QLineEdit(self)
        self.display_area.setGeometry(QtCore.QRect(30, 10, 391, 31))
        self.display_area.setObjectName("display_area")
        self.display_area.setReadOnly(True)
        self.display_area.setAlignment(Qt.AlignCenter)

        self.confirm = QtWidgets.QPushButton(self)
        self.confirm.setGeometry(QtCore.QRect(440, 10, 121, 31))
        self.confirm.setObjectName("confirm")
        self.confirm.pressed.connect(lambda: self.button_send())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DisplayScreen", "Display Content"))
        self.confirm.setText(_translate("DisplayScreen", "Confirm"))

    # == Functions: List Related == #

    def button_send(self) -> None:
        print(self.current_table_name)
        get_table_data = TableData().get_parameters_list()
        get_table_index = get_table_data.index(self.current_table_name)
        display_text_data = self.display_text.toPlainText().strip()

        self.main_window.log_send(f"Changed Data for {self.display_area.text()}")
        self.main_window.area_details.setItem(get_table_index, 0, QTableWidgetItem(display_text_data))
        self.clear_data()
        self.close()

    # == Functions: Event Related == #

    def clear_data(self) -> None:
        self.display_area.clear()
        self.display_text.clear()

    def closeEvent(self, event) -> None:
        self.clear_data()
        super(DisplayScreen, self).closeEvent(event)

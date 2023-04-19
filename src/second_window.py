# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.constant import Constant

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt


class ReachableScream(QtWidgets.QDialog):
    def __init__(self, main_window):
        super(ReachableScream, self).__init__()
        self.setObjectName("ReachableScream")
        self.main_window = main_window
        self.setEnabled(True)
        self.setFixedSize(600, 350)
        self.setStyleSheet(Constant.load_stylesheets_dialog())

        self.select_areas = QtWidgets.QListWidget(self)
        self.select_areas.setGeometry(QtCore.QRect(20, 50, 271, 281))
        self.select_areas.setObjectName("select_areas")
        self.select_areas.setDragEnabled(False)
        self.select_areas.setWordWrap(False)
        self.select_areas.itemDoubleClicked.connect(lambda: self.select_list_doubleclick())

        self.chosen_areas = QtWidgets.QListWidget(self)
        self.chosen_areas.setGeometry(QtCore.QRect(305, 50, 271, 281))
        self.chosen_areas.setObjectName("chosen_areas")
        self.chosen_areas.setDragEnabled(False)
        self.chosen_areas.setWordWrap(False)
        self.chosen_areas.itemDoubleClicked.connect(lambda: self.chosen_list_doubleclick())

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
        self.setWindowTitle(_translate("ReachableScream", "Reachable Areas Setter"))
        self.confirm.setText(_translate("ReachableScream", "Confirm List"))

    # == Functions: List Related == #

    def button_send(self) -> None:
        new_data = list()
        if self.chosen_areas.count():
            for number in range(self.chosen_areas.count()):
                new_data.append(self.chosen_areas.item(number).text())

            new_data = list(dict.fromkeys(new_data))
            data_str = ", ".join(new_data)
            self.main_window.area_details.setItem(3, 0, QTableWidgetItem(data_str))
            self.main_window.log_send(f"Generated and Inserted the following to Reachable Areas: \n>>> " + '\n>>> '.join(new_data))

        self.clear_data()
        self.close()

    def chosen_list_doubleclick(self) -> None:
        item = self.chosen_areas.currentItem().text()
        new_data = list()
        if self.chosen_areas.count():
            for number in range(self.chosen_areas.count()):
                new_data.append(self.chosen_areas.item(number).text())

            for data in new_data:
                if data == item:
                    get_index = new_data.index(item)
                    self.chosen_areas.takeItem(get_index)
                    return

    def select_list_doubleclick(self) -> None:
        item = self.select_areas.currentItem().text()
        new_data = list()
        if self.chosen_areas.count():
            for number in range(self.chosen_areas.count()):
                new_data.append(self.chosen_areas.item(number).text())

        if item not in new_data:
            self.chosen_areas.addItem(item)

    # == Functions: Event Related == #

    def clear_data(self) -> None:
        self.select_areas.clear()
        self.chosen_areas.clear()

    def closeEvent(self, event) -> None:
        self.clear_data()
        super(ReachableScream, self).closeEvent(event)

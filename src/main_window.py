# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.display_window import DisplayScreen
from src.second_window import ReachableScream
from src.yaml_dataclass import TableData
from src.constant import Constant
from src.logger import Logging

from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog, QHeaderView, QListWidget, QMenu, QAction
from PyQt5.QtGui import QCursor, QFontDatabase
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt

from typing import Any, Dict, List
from copy import deepcopy
from pathlib import Path

import json
import yaml
import os


class YAMLMaker(QtWidgets.QMainWindow):
    def __init__(self):
        super(YAMLMaker, self).__init__()
        # Import all of the Widgets
        self.second_window = ReachableScream(self)
        self.display_screen = DisplayScreen(self)
        self.file_dialog = QFileDialog()
        self.config = Constant.load_config()

        # important attrs
        self.current_json_list = list()
        self.old_item_selected = str()
        self._stylesheets = Constant.load_stylesheets_main()
        self._fonts = Constant.get_font()
        self.parameters_length = TableData().__len__()
        self.yaml_parameters = TableData().get_parameters_list()

        # File Related Part 1
        self.main_directory = os.getcwd()
        self.current_directory = os.getcwd() if not self.config['current_directory'] else self.config['current_directory']
        self.save_path = str()
        self.yaml_json_list = dict()
        self.open_filename = "Untitled"
        self.open_file_extension = ".json"
        self.application_title = "Danganronpa Online YAMLMaker"
        self.version_number = "1.1.1"

        self.setStyleSheet(self._stylesheets)
        self.load_font()

        self.setObjectName("DRO YAMLMaker")
        self.setFixedSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.container = QtWidgets.QWidget(self.centralwidget)
        self.container.setGeometry(QtCore.QRect(10, 10, 781, 561))
        self.container.setStyleSheet(self._stylesheets)
        self.container.setObjectName("container")

        self.area_list = QtWidgets.QListWidget(self.container)
        self.area_list.setGeometry(QtCore.QRect(10, 10, 251, 341))
        self.area_list.setObjectName("area_list")
        self.area_list.setDragEnabled(True)
        self.area_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.area_list.setMovement(QtWidgets.QListView.Free)
        self.area_list.setProperty("isWrapping", False)
        self.area_list.setWordWrap(False)
        self.area_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.area_list.setItemAlignment(QtCore.Qt.AlignLeading)
        self.area_list.installEventFilter(self)
        self.area_list.currentItemChanged.connect(lambda: self.change_table_data())

        self.area_details = QtWidgets.QTableWidget(self.container)
        self.area_details.setGeometry(QtCore.QRect(270, 10, 501, 341))
        self.area_details.setObjectName("area_details")

        self.area_details.setRowCount(self.parameters_length)
        self.area_details.setColumnCount(1)
        self.table_stylesheet()

        self.area_details.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.area_details.setHorizontalHeaderLabels(["Parameter Details"])

        self.area_details.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.area_details.setVerticalHeaderLabels(TableData().get_parameters_list())
        self.area_details.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.area_details.setWordWrap(True)

        self.area_details.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.area_details.viewport().installEventFilter(self)
        self.area_details.customContextMenuRequested.connect(self.customMenuRequested)

        self.logging = QtWidgets.QTextBrowser(self.container)
        self.logging.setGeometry(QtCore.QRect(10, 360, 761, 192))
        self.logging.setObjectName("logging")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.setMenuBar(self.menubar)

        self.menubar_openfile = QtWidgets.QAction(self)
        self.menubar_openfile.setObjectName("menubar_openfile")
        self.menubar_openfile.triggered.connect(lambda: self.openfile_json_menu())

        self.menubar_savefile = QtWidgets.QAction(self)
        self.menubar_savefile.setObjectName("menubar_savefile")
        self.menubar_savefile.triggered.connect(lambda: self.savefile_json_menu())

        self.menubar_saveasfile = QtWidgets.QAction(self)
        self.menubar_saveasfile.setObjectName("menubar_saveasfile")
        self.menubar_saveasfile.triggered.connect(lambda: self.savefile_json_menu(True))

        self.menubar_openyaml = QtWidgets.QAction(self)
        self.menubar_openyaml.setObjectName("menubar_openyaml")
        self.menubar_openyaml.triggered.connect(lambda: self.openfile_yaml_menu())

        self.menubar_exportyaml = QtWidgets.QAction(self)
        self.menubar_exportyaml.setObjectName("menubar_exportyaml")
        self.menubar_exportyaml.triggered.connect(lambda: self.exportfile_yaml_menu())

        self.menubar_githubpage = QtWidgets.QAction(self)
        self.menubar_githubpage.setObjectName("menubar_githubpage")
        self.menubar_githubpage.triggered.connect(lambda: self.open_github())

        self.menubar_newfile = QtWidgets.QAction(self)
        self.menubar_newfile.setObjectName("menubar_newfile")
        self.menubar_newfile.triggered.connect(lambda: self.newfile_popup())

        self.menubar_check_area_validity = QtWidgets.QAction(self)
        self.menubar_check_area_validity.setObjectName("menubar_check_area_validity")
        self.menubar_check_area_validity.triggered.connect(lambda: self.check_area_validity())

        self.menuFile.addAction(self.menubar_newfile)

        self.menuFile.addAction(self.menubar_openfile)
        self.menuFile.addAction(self.menubar_savefile)
        self.menuFile.addAction(self.menubar_saveasfile)
        self.menuFile.addAction(self.menubar_openyaml)
        self.menuFile.addAction(self.menubar_exportyaml)

        self.menuTools.addAction(self.menubar_check_area_validity)

        self.menuHelp.addAction(self.menubar_githubpage)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # == Functions: Initiates on Startup == #

        self.area_list_details_initialise()
        self.log_send()

    # == Functions: Main Window Related == #

    def is_area_name_duplicate(self, area_name: str) -> bool:
        get_list = [d['area'] for d in self.current_json_list]
        if area_name in get_list:
            return True
        return False

    def load_font(self) -> None:
        QFontDatabase.addApplicationFont(self._fonts)

    def set_window_title(self, modified: bool = False) -> None:
        title_name = self.window_title(modified)
        self.setWindowTitle(title_name)

    def table_stylesheet(self):
        ssh = "::section{background-color: #4F4557; border: 1px solid white; border-left:none;}"
        ssv = "::section{background-color: #4F4557; border: 1px solid white; border-top:none;}"
        self.area_details.horizontalHeader().setStyleSheet(ssh)
        self.area_details.verticalHeader().setStyleSheet(ssv)

    def window_title(self, modified: bool = False) -> str:
        title_name = f"{self.open_filename}{self.open_file_extension} - {self.application_title} ({self.version_number})"
        if modified:
            title_name = f"*{title_name}"

        return title_name

    # == Functions: Logger Related == #

    def log_send(self, message: str = None) -> None:
        if message:
            prepare_log = Logging(message=message).prepare_message()
        else:
            prepare_log = Logging().prepare_message()

        self.logging.insertPlainText(prepare_log)

    # == Functions: Area List Related == #

    def add_item_list(self, item_list: List[str]) -> None:
        for item in item_list:
            self.area_list.addItem(item)

    def change_item_name(self, current_item: str, item: str) -> None:
        self.log_send(f"Item Named Changed from {current_item} to {item}.")
        get_index = self.find_list_index(current_item)
        self.area_list.insertItem(get_index + 1, item)
        self.area_list.takeItem(get_index)

    def delete_areas_list(self) -> None:
        self.log_send(f"Area List Deleted.")
        for _ in range(self.area_list.count() - 1):
            self.area_list.takeItem(1)

    def get_value_list(self) -> List[str]:
        new_data = [self.area_list.item(number).text() for number in range(self.area_list.count())]
        new_data = list(dict.fromkeys(new_data))
        return new_data

    def reorder_data(self) -> None:
        get_list = self.get_value_list()
        new_list = list()
        for item in get_list:
            for d in self.current_json_list:
                if (d['area_id'] == item) or \
                        (d['area'] == item):
                    new_list.append(d)

        self.log_send(f"Current JSON List Reordered.")
        self.current_json_list = new_list

    # Potential Update to include Indexs before the Name

    # def insert_index_item_list(self) -> None:
    #    get_list = self.get_value_list()
    #    new_list = [f"{get_list.index(item)} :: {item}" for item in get_list]
    #    self.delete_areas_list()
    #    self.area_list.addItems(new_list)
    #    self.area_list.takeItem(0)

    # == Functions: Area Details Related == #

    def area_list_details_initialise(self) -> None:
        self.log_send(f"Area List and Details Initialised.")
        self.log_send(f"Welcome to Danganronpa Online Area List YAMLMaker!")
        get_table = self.create_table_data()
        list_get_table = list(get_table.values())
        self.data_to_json(get_table)
        self.set_value_table(list_get_table)
        self.add_item_list([list_get_table[0]])

    def create_table_data(self, table_data: List[str] = None) -> Dict[str, str]:
        if table_data:
            get_table = TableData(*table_data).get_parameters_as_dict()
        else:
            get_table = TableData().new_table()
        return get_table

    def get_value_table(self) -> List[str]:
        new_data = [self.area_details.item(number, 0).text() for number in range(self.parameters_length)]
        return new_data

    def set_value_table(self, table_list: List[str]) -> None:
        for item, number in zip(table_list, range(self.parameters_length)):
            self.area_details.setItem(number, 0, QTableWidgetItem(str(item)))

    # == Functions: Area List + Area Details Related == #

    def find_data_index(self, item: str) -> int:
        get_index = self.current_json_list.index(self.find_data_by_item(item))
        return get_index

    def find_list_index(self, item: str) -> int:
        get_data = self.get_value_list()
        get_index = get_data.index(item)
        return get_index

    def find_data_by_item(self, item: str) -> Dict[str, str]:
        for d in self.current_json_list:
            if (d['area_id'] == item) or (d['area'] == item):
                return d

    # == Functions: Current JSON List Related == #

    def change_table_data(self) -> None:
        # Signals File is Modified
        self.set_window_title(True)

        # Saves old Data before switching to new.
        if self.old_item_selected:
            self.save_table_data(self.old_item_selected)

        current_item = self.area_list.currentItem().text()
        change_data = self.find_data_by_item(current_item)
        change_data_list = list(change_data.values())
        self.set_value_table(change_data_list)

        self.reorder_data()
        self.old_item_selected = current_item

    def data_to_json(self, table_dict: Dict[str, str]) -> None:
        return self.current_json_list.append(table_dict)

    def data_to_json_extend(self, item_list: List[Dict[str, str]]) -> None:
        return self.current_json_list.extend(item_list)

    def delete_current_json(self) -> None:
        self.log_send(f"Current JSON List Deleted.")
        for _ in range(len(self.current_json_list) - 1):
            self.current_json_list.pop(1)

    # == Functions: JSON Conversion Related == #

    def is_valid_json_file(self, json_file_path: str) -> bool:
        with open(json_file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return False

            for d in data:
                value_params = len(d.keys())
                if not value_params == self.parameters_length:
                    return False
            return True

    # == Functions: YAML Conversion Related == #

    def is_valid_yaml_file(self, yaml_file) -> bool:
        try:
            with open(yaml_file, "r", encoding="utf-8") as stream:
                load_yaml = yaml.safe_load(stream)
                get_json = json.loads(json.dumps(load_yaml, indent=4))
                for data in get_json:
                    for k in data.keys():
                        if k in self.yaml_parameters:
                            self.yaml_json_list = get_json
                            return True

        except yaml.parser.ParserError:
            return False
        except FileNotFoundError as err:
            raise err

        return True

    # == Functions: Menu Bar Related == #

    def check_area_popup(self, error_list: List[List]) -> None:
        if error_list:
            threatening_error_details = list()
            non_threatening_error_details = list()
            empty_value_error_details = list()

            error_title = "You Failure"
            error_icon = QMessageBox.Critical

            # error_type: 0 - Non-threatening Errors, 1 - Threatening Errors, 2 - Empty Value After Comma Error
            for detail in error_list:
                list_type = 'REACHABLE AREAS' if detail[2] == 0 else 'SCREAM RANGE'
                if detail[3] == 0:
                    value_type = f"{list_type.title()} list is empty."
                    detail_str = f"[{list_type}] {detail[0]['area']}: {value_type}"
                    non_threatening_error_details.append(detail_str)
                elif detail[3] == 1:
                    value_type = f"Area [{detail[1]}] doesn't exist."
                    detail_str = f"[{list_type}] {detail[0]['area']}: {value_type}"
                    threatening_error_details.append(detail_str)
                elif detail[3] == 2:
                    value_type = f"{detail[0]['area']}'s [{list_type.title()}] list has a stray comma."
                    detail_str = f"[{list_type}] {detail[0]['area']}: {value_type}"
                    empty_value_error_details.append(detail_str)

            error_message_prep = "\n> ".join(threatening_error_details)
            error_message_prep += "\n> ".join(empty_value_error_details)
            error_message_prep += "\n> ".join(non_threatening_error_details)
            
            error_message = f"Here are the Errors:\n" \
                            f"> {error_message_prep}"

        else:
            error_title = "No Errors Found"
            error_icon = QMessageBox.Information
            error_message = f"No Errors Found. Good job!"

        popup = QMessageBox()
        _icon_file = QtGui.QIcon(Constant.get_icon())
        popup.setStyleSheet(self._stylesheets)
        popup.setWindowIcon(_icon_file)
        popup.setIcon(error_icon)
        popup.setWindowTitle(error_title)
        popup.setText(error_message)
        popup.setDefaultButton(QMessageBox.Cancel)
        popup.exec_()

    def check_area_validity(self) -> None:
        current_item = self.area_list.currentItem().text()
        self.save_table_data(current_item)

        get_all_areas = [_area['area'] for _area in self.current_json_list]
        error_list = list()

        # error: 0 - Reachable Area Error, 1 - Scream Range Error
        # error_type: 0 - Non-threatening Errors, 1 - Threatening Errors, 2 - Empty Value After Comma Error
        # [dict, str, error, error_type]
        for area in self.current_json_list:
            if not area['reachable_areas'] == "<ALL>":
                if not area['reachable_areas']:
                    error_list.append([area, area['area'], 0, 0])
                else:
                    for a in area['reachable_areas'].split(","):
                        if not a.strip():
                            error_list.append([area, a.strip(), 0, 2])
                        else:
                            if not a.strip() in get_all_areas:
                                error_list.append([area, a.strip(), 0, 1])

            if not area['scream_range'] == "<REACHABLE_AREAS>":
                if area['scream_range']:
                    for s in area['scream_range'].split(","):
                        if not s.strip():
                            error_list.append([area, s.strip(), 1, 2])
                        else:
                            if not s.strip() in get_all_areas:
                                error_list.append([area, s.strip(), 1, 1])

        self.check_area_popup(error_list)

    def export_json_file(self, destination) -> None:
        with open(destination, "w", encoding="utf-8") as file:
            json_file = json.dumps(self.current_json_list, indent=4)
            file.write(json_file)

    def exportfile_yaml_menu(self) -> None:
        path_to_file = os.path.join(str(self.current_directory), Path(self.open_filename).stem)
        filename, _ = self.file_dialog.getSaveFileName(self, 'Export YAML File', path_to_file, "YAML File (*.yaml)")
        if not filename:
            return

        final_list = list()
        for document in self.current_json_list:
            get_data = TableData(**document).export(self.current_json_list[0])
            final_list.append(get_data)

        yaml_data = self.json_to_yaml_convert(final_list)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(yaml_data)

        self.log_send(f"YAML File Exported.")
        self.open_filename = Path(filename).stem
        self.open_file_extension = Path(filename).suffix
        self.current_directory = Path(filename).parent
        Constant.change_config('current_directory', str(self.current_directory))
        self.set_window_title()

    def open_github(self) -> None:
        import webbrowser

        url = "https://github.com/Yuzurukyun/Area-YAMLMaker"
        webbrowser.open(url)

    def openfile_json_menu(self) -> None:
        filename, _ = self.file_dialog.getOpenFileName(self, 'Open JSON File', str(self.current_directory), "JSON File (*.json)")
        while True:
            try:
                if not self.is_valid_json_file(filename):
                    filename, _ = self.file_dialog.getOpenFileName(self, 'Open a VALID JSON File', str(self.current_directory), "JSON File (*.json)")
                else:
                    break
            except FileNotFoundError:
                return

        with open(filename, "r", encoding="utf-8") as file:
            json_file = json.load(file)

            # This helps not crashing the program (?????)
            self.area_list.setCurrentRow(0)

            # Clears both lists except for index 0
            self.delete_current_json()
            self.delete_areas_list()

            self.data_to_json_extend(json_file)
            self.add_item_list([item["area"] for item in json_file])

            # I don't know why clearing everything in the list doesn't work
            # This is genuinely the only workaround I have that functions
            self.area_list.takeItem(0)
            self.current_json_list.pop(0)

        self.log_send(f"File Opened.")
        self.open_filename = Path(filename).stem
        self.open_file_extension = Path(filename).suffix
        self.set_window_title()
        self.current_directory = Path(filename).parent
        Constant.change_config('current_directory', str(self.current_directory))

    def openfile_yaml_menu(self) -> None:
        filename, _ = self.file_dialog.getOpenFileName(self, 'Import YAML File', str(self.current_directory), "YAML File (*.yaml *.yml)")
        while True:
            try:
                if not self.is_valid_yaml_file(filename):
                    filename, _ = self.file_dialog.getOpenFileName(self, 'Import a VALID YAML File', str(self.current_directory), "YAML File (*.yaml *.yml)")
                else:
                    break
            except FileNotFoundError:
                return

        if not self.yaml_json_list:
            # Verification Failed, not a complete valid area yaml list.
            return

        # This helps not crashing the program (?????)
        self.area_list.setCurrentRow(0)

        final_conversion_list = self.yaml_to_json_convert()

        # Clears both lists except for index 0
        self.delete_current_json()
        self.delete_areas_list()

        self.data_to_json_extend(final_conversion_list)
        self.add_item_list([item["area"] for item in final_conversion_list])

        # I don't know why clearing everything in the list doesn't work
        # This is genuinely the only workaround I have that functions
        self.area_list.takeItem(0)
        self.current_json_list.pop(0)

        self.log_send(f"YAML File Opened.")
        self.open_filename = Path(filename).stem
        self.open_file_extension = Path(filename).suffix
        self.current_directory = Path(filename).parent
        Constant.change_config('current_directory', str(self.current_directory))
        self.set_window_title()

    def savefile_json_menu(self, save_as: bool = False) -> None:
        path_to_file = os.path.join(str(self.current_directory), Path(self.open_filename).stem)
        if not self.save_path or save_as:
            filename, _ = self.file_dialog.getSaveFileName(self, 'Save JSON File', path_to_file, "JSON File (*.json)")
            if not filename:
                return

            self.export_json_file(filename)
        else:
            filename = self.save_path
            self.export_json_file(filename)

        self.log_send(f"File Saved.")
        self.save_path = filename
        self.open_filename = Path(filename).stem
        self.open_file_extension = Path(filename).suffix
        self.current_directory = Path(filename).parent
        Constant.change_config('current_directory', str(self.current_directory))
        self.set_window_title()

    # == Functions: New File Menu Bar Related == #

    def newfile_action(self) -> None:
        self.current_directory = self.main_directory
        self.save_path = str()
        self.yaml_json_list = dict()
        self.open_filename = "Untitled"
        self.open_file_extension = ".json"

        self.log_send(f"New File was Created.")
        self.delete_areas_list()
        self.area_list_details_initialise()
        self.area_list.takeItem(0)

    def newfile_popup(self) -> None:
        popup = QMessageBox()
        _icon_file = QtGui.QIcon(Constant.get_icon())
        popup.setStyleSheet(self._stylesheets)
        popup.setWindowIcon(_icon_file)
        popup.setIcon(QMessageBox.Critical)
        popup.setWindowTitle("Confirmation Popup")
        popup.setText("Are you sure? Pressing [ OK ] will reset the program")
        popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        popup.setDefaultButton(QMessageBox.Cancel)
        popup.buttonClicked.connect(self.popup_button)
        popup.exec_()

    def popup_button(self, button) -> None:
        if button.text() == "OK":
            self.newfile_action()

    # == Functions: Conversions Related == #

    def json_to_yaml_convert(self, json_list) -> Any:
        converted_yaml_data = yaml.safe_dump(json_list, sort_keys=False)
        return converted_yaml_data

    def yaml_to_json_convert(self) -> List[Dict[str, str]]:
        get_parameters = TableData().get_parameters_list()
        converted_dict = dict()
        final_conversion_list = list()
        for a in self.yaml_json_list:
            for k, v in a.items():
                if k.lower() in get_parameters:
                    if isinstance(v, dict):
                        v = ', '.join([f"{k}: {v}" for k, v in v.items()])
                    converted_dict[k.lower()] = v
            converted_dict['area_id'] = a['area']
            converted_data_dict = TableData(**converted_dict).get_dict_from_parameters()
            final_conversion_list.append(converted_data_dict)
            converted_dict = dict()

        return final_conversion_list

    # == Functions: Event Handlers 1 Related == #

    def eventFilter(self, source, event) -> Any:
        if event.type() == QEvent.ContextMenu and source is self.area_list:
            list_menu = QMenu()
            list_menu.setStyleSheet(self._stylesheets)

            add_area = QAction("Add Area", self)
            remove_area = QAction("Remove Area", self)
            duplicate_area = QAction("Duplicate Area", self)

            add_area.triggered.connect(lambda: self.list_add_area())

            source_item_pos = source.itemAt(event.pos())
            try:
                item = source_item_pos.text()
                remove_area.triggered.connect(lambda: self.list_remove_area(item))
                duplicate_area.triggered.connect(lambda: self.list_duplicate_area(item))
            except AttributeError:
                pass

            if self.area_list.count() <= 1:
                remove_area.setVisible(False)

            if not source.itemAt(event.pos()):
                remove_area.setVisible(False)
                duplicate_area.setVisible(False)

            list_menu.addActions([add_area, remove_area, duplicate_area])
            list_menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)

    def list_add_area(self) -> None:
        while True:
            new_data = TableData().new_table()
            if not any((d['area'] == new_data['area']) or
                       (d['area_id'] == new_data['area'])
                       for d in self.current_json_list):
                self.log_send(f"Area [{new_data['area']}] Added.")
                self.data_to_json(new_data)
                self.add_item_list([new_data["area"]])
                return

    def list_remove_area(self, item: str) -> None:
        get_index = self.find_data_index(item)

        self.log_send(f"Area [{self.get_value_list()[get_index]}] Deleted.")
        self.area_list.takeItem(get_index)
        self.current_json_list.pop(get_index)

    def list_duplicate_area(self, item: str) -> None:
        duplicate_id = f"_{Constant.id_generator()[0:2]}"
        get_index = self.find_data_index(item)
        get_json = self.find_data_by_item(item)
        new_json = deepcopy(get_json)
        new_json["area"] += duplicate_id
        new_json["area_id"] += duplicate_id

        self.log_send(f"Area [{new_json['area']}] Duplicated.")
        self.data_to_json(new_json)
        self.area_list.insertItem(get_index + 1, new_json["area"])

    # == Functions: Event Handlers 2 Related == #

    def customMenuRequested(self) -> None:
        custom_menu = QMenu(self)

        display_full_content = QAction("Display Full Content", self)
        store_table_data = QAction("Store Current Table", self)
        open_quick_reach_screen = QAction("Open Reachable Areas Selection", self)
        transfer_reachable_to_scream = QAction("Transfer Reachable Areas Data to Scream Range", self)

        current_item = self.area_list.currentItem().text()
        current_item_index = self.area_details.currentRow()

        display_full_content.triggered.connect(lambda: self.display_full_content(current_item_index))
        store_table_data.triggered.connect(lambda: self.save_table_data(current_item))
        open_quick_reach_screen.triggered.connect(lambda: self.reachable_selection_screen())
        transfer_reachable_to_scream.triggered.connect(lambda: self.transfer_reachable_scream())

        custom_menu.addActions([display_full_content, open_quick_reach_screen, transfer_reachable_to_scream, store_table_data])
        custom_menu.exec_(QCursor.pos())

    def display_full_content(self, get_index: int) -> None:
        get_content = self.get_value_table()[get_index]
        get_table_data = TableData().get_parameters_list()

        self.display_screen.current_table_name = get_table_data[get_index]
        self.display_screen.display_area.setText(get_table_data[get_index])
        self.display_screen.display_text.setPlainText(get_content)
        self.display_screen.setWindowModality(Qt.ApplicationModal)
        self.display_screen.show()

    def save_table_data(self, item: str) -> None:
        get_data = self.get_value_table()
        get_index = self.find_data_index(item)

        if not self.is_table_changed(item, get_data):
            return

        if not self.is_area_name_duplicate(item):
            get_data[0] = get_data[-1]

        if len(get_data[0].strip()) == 0:
            get_data[0] = get_data[-1]

        self.change_item_name(item, get_data[0])

        self.log_send("Table Data Saved.")
        new_data = TableData(*get_data).get_dict_from_parameters()
        self.current_json_list[get_index] = new_data

    def is_table_changed(self, item_change: str, table_data: List[str]) -> bool:
        get_data = self.find_data_by_item(item_change)
        get_data = list(get_data.values())

        if get_data == table_data:
            return False
        return True

    def reachable_selection_screen(self) -> None:
        self.send_data_to_second_window()

        self.log_send("Reachable Area Generator Screen Open.")
        self.second_window.setWindowModality(Qt.ApplicationModal)
        self.second_window.show()

    def send_data_to_second_window(self) -> None:
        self.reorder_data()
        get_list = self.get_value_list()
        get_chosen_list = self.get_value_table()[3].split(", ")

        self.second_window.select_areas.addItems(get_list)
        self.second_window.chosen_areas.addItems(get_chosen_list)
        self.second_window.display_area.setText(self.area_list.currentItem().text())

    def transfer_reachable_scream(self) -> None:
        reachable = self.area_details.item(3, 0).text()
        self.area_details.setItem(4, 0, QTableWidgetItem(reachable))
        self.log_send("Reachable Areas transferred to Scream Range.")

    def retranslateUi(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        _icon_file = QtGui.QIcon(Constant.get_icon())
        self.setWindowIcon(_icon_file)
        self.second_window.setWindowIcon(_icon_file)

        self.setWindowTitle(_translate("YAMLMaker", self.window_title()))

        self.menuFile.setTitle(_translate("YAMLMaker", "File"))
        self.menuHelp.setTitle(_translate("YAMLMaker", "Help"))
        self.menuTools.setTitle(_translate("YAMLMaker", "Tools"))

        self.menubar_openfile.setText(_translate("YAMLMaker", "Open File"))
        self.menubar_openfile.setToolTip(_translate("YAMLMaker", "Opens a Project File"))
        self.menubar_openfile.setShortcut(_translate("YAMLMaker", "Ctrl+O"))
        self.menubar_savefile.setText(_translate("YAMLMaker", "Save File"))
        self.menubar_savefile.setToolTip(_translate("YAMLMaker", "Saves the Project File"))
        self.menubar_savefile.setShortcut(_translate("YAMLMaker", "Ctrl+S"))
        self.menubar_saveasfile.setText(_translate("YAMLMaker", "Save As..."))
        self.menubar_saveasfile.setToolTip(_translate("YAMLMaker", "Saves to a Different Project File"))
        self.menubar_saveasfile.setShortcut(_translate("YAMLMaker", "Ctrl+Shift+S"))
        self.menubar_openyaml.setText(_translate("YAMLMaker", "Open YAML"))
        self.menubar_openyaml.setToolTip(_translate("YAMLMaker", "Opens a YAML file"))
        self.menubar_openyaml.setShortcut(_translate("YAMLMaker", "Ctrl+Shift+O"))
        self.menubar_exportyaml.setText(_translate("YAMLMaker", "Export YAML"))
        self.menubar_exportyaml.setToolTip(_translate("YAMLMaker", "Export the file into a YAML"))
        self.menubar_exportyaml.setShortcut(_translate("YAMLMaker", "Ctrl+Shift+E"))
        self.menubar_githubpage.setText(_translate("YAMLMaker", "Github Page"))
        self.menubar_githubpage.setToolTip(_translate("YAMLMaker", "Opens the Main Github Page on your Browser"))
        self.menubar_githubpage.setShortcut(_translate("YAMLMaker", "Ctrl+Shift+H"))

        self.menubar_check_area_validity.setText(_translate("YAMLMaker", "Check Area Validity"))
        self.menubar_check_area_validity.setToolTip(_translate("YAMLMaker", "Checks the validity of the Area Lists"))
        self.menubar_check_area_validity.setShortcut(_translate("YAMLMaker", "Ctrl+Alt+C"))

        self.menubar_newfile.setText(_translate("YAMLMaker", "New File"))
        self.menubar_newfile.setToolTip(_translate("YAMLMaker", "Opens up a New File"))
        self.menubar_newfile.setShortcut(_translate("YAMLMaker", "Ctrl+N"))

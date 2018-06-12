from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QTextCursor, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.Qt import Qt
from gui_py.main_window_gui import Ui_MainWindow
from window_classes.AddonWindow import AddonWindow
from window_classes.SettingsWindow import SettingsWindow
import sys
import os
import zipfile
from PyQt5.QtWidgets import QTreeView
from Worker import Worker
from Settings import Settings
from Downloader import Downloader
from UpdateChecker import UpdateChecker
from overrides.internal_overrides import MainWindowPrompt
import logging

sys._excepthook = sys.excepthook
logging.basicConfig(level=logging.INFO)


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

HANDLE_STYLE = """
QSplitter::handle:horizontal {

border: 1px solid #777;
width: 13px;
margin-top: 2px;
margin-bottom: 2px;
border-radius: 4px;
}

QSplitter::handle {
background: #ccc;
}
"""


class MainWindow(MainWindowPrompt):

    try:
        OpenAddonAdder = pyqtSignal()
        OpenSettingsWindow = pyqtSignal()
        OutputUpdater = pyqtSignal(str)
        PromptUpdate = pyqtSignal(list)
        DownloadStart = pyqtSignal()
        MessageBox = pyqtSignal(str, str, str)
        UpdateTreeView = pyqtSignal()

        # settings = Settings()

    except Exception as e:
        print(e)

    def __init__(self):
        super(MainWindowPrompt, self).__init__()

        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self)
        self.settings = Settings()

        self.download_worker = Worker(self.execute_download)
        self.update_worker = Worker(self.execute_check_updates)
        self.init_ui()

    def init_ui(self):
        self.window.ui.splitter.setStyleSheet(HANDLE_STYLE)

        self.OpenAddonAdder.connect(self.add_addon)
        self.OpenSettingsWindow.connect(self.show_settings_window)
        self.OutputUpdater.connect(self.insert_output_text)
        self.PromptUpdate.connect(self.prompt_to_update)
        self.DownloadStart.connect(self.execute_download)
        self.MessageBox.connect(self.show_message_box)
        self.UpdateTreeView.connect(self.update_tree_view)

        self.window.ui.actionAddAddon.triggered.connect(self.OpenAddonAdder.emit)
        self.window.ui.actionSettings.triggered.connect(self.OpenSettingsWindow.emit)
        self.window.ui.btnCheckForUpdates.clicked.connect(self.update_worker.start)
        self.window.ui.actionUpdateTreeView.triggered.connect(self.UpdateTreeView.emit)

        self.UpdateTreeView.emit()

    @pyqtSlot()
    def add_addon(self):
        addon_window = AddonWindow(self.settings, self)
        addon_window.exec()

    @pyqtSlot(str)
    def insert_output_text(self, text):
        self.window.ui.teditOutput.insertPlainText(text + '\n')
        self.window.ui.teditOutput.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def show_settings_window(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()

    @pyqtSlot()
    def update_tree_view(self):
        tree_model = self.window.ui.tviewAddons
        model = QStandardItemModel(tree_model)
        tree_model.setModel(model)

        tree_data = self.settings.data['addons']
        logging.debug("Tree view data: {0}".format(tree_data))

        # No addons are loaded.
        # TODO: Insert blank row indicating there are no addons.
        if len(tree_data) == 0:
            return
        else:
            model.clear()

        for parent_name in tree_data:
            parent_item = QStandardItem(tree_data[parent_name]['name'])
            url_item = QStandardItem("Addon Link: {0}".format(tree_data[parent_name]['url']))
            curr_ver_item = QStandardItem("Current Version: {0}".format(tree_data[parent_name]['current_version']))
            latest_ver_item = QStandardItem("Latest Version:    {0}".format(tree_data[parent_name]['latest_version']))

            logging.debug("Parent item: {0}".format(parent_name))

            model.appendRow(parent_item)

            # Append URL, Current Version, and Latest Version to the parent
            parent_item.appendRow(url_item)
            parent_item.appendRow(curr_ver_item)
            parent_item.appendRow(latest_ver_item)

        model.setHeaderData(0, Qt.Horizontal, "Addons")

    @pyqtSlot(str, str, str)
    def show_message_box(self, message='', inform='', message_type='warn'):
        message_box = QMessageBox()

        if message_type == 'inform':
            message_box.setIcon(QMessageBox.Information)
        elif message_type == 'warn':
            message_box.setIcon(QMessageBox.Warning)
        else:
            message_box.setIcon(QMessageBox.Critical)

        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.setWindowTitle("Hey Listen!")
        message_box.setText(message)
        message_box.setInformativeText(inform)
        message_box.exec()

    def execute_check_updates(self):

        if self.settings.data['settings']['wow_dir'] == '':
            self.MessageBox.emit("Addons directory not found",
                                 "Please specify the directory where you want the addons to be downloaded to from "
                                 "'File' -> 'Settings'."
                                 "This is usually 'World of Warcraft/Addons'.", 'inform')
            return

        if len(self.settings.data['addons']) == 0:
            self.MessageBox.emit("No addons have been specified.",
                                 "To add an addon, press 'Addon' -> 'Add Addon' and enter the URL of the addon.",
                                 "warn")
            return

        self.OutputUpdater.emit("Checking for updates...")
        updater = UpdateChecker(self)
        update_list = updater.check_for_updates()

        self.PromptUpdate.emit(update_list)

    @pyqtSlot(list)
    def prompt_to_update(self, update_list):

        if update_list:
            self.OutputUpdater.emit("Addons out of date:")
            for addon in update_list:
                self.OutputUpdater.emit("\n{0}: \n\tCurrent version: {1} \n\tNew version:      {2}\n".format(addon.name.title(),
                                                                                            addon.current_version,
                                                                                            addon.latest_version))
            message_box = QMessageBox.question(None, "Updates found.",
                                               "{0} update{1} found. Would you like to download {2} now?".format(
                                                   len(update_list),
                                                   "s" if len(update_list) > 1 else "",
                                                   "them" if len(update_list) > 1 else "it"),
                                               QMessageBox.Yes, QMessageBox.No)
            if message_box == QMessageBox.Yes:
                self.download_worker.start()

        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("Checker")
            message_box.setText("All addons are up to date!")
            message_box.setStandardButtons(QMessageBox.Ok)

            message_box.exec()

    @pyqtSlot()
    def execute_download(self):
        d = Downloader(self.settings)
        # to_update = d.check_for_updates()
        to_update = self.settings.files_to_update
        logging.info("Update list: {0}".format(to_update))
        for item in to_update:
            self.OutputUpdater.emit("Downloading files for {0} to {1}".format(item.name.title(),
                                                                                 os.path.abspath(d.zip_dir)))
            response, file_dir = d.download_from_url(item)
            file_dir = os.path.abspath(file_dir)
            logging.info("Item: {0}".format(item.url))
            logging.debug("File to extract: {0}".format(file_dir))

            if response:
                self.OutputUpdater.emit("Download complete.")
            else:
                self.OutputUpdater.emit("Download failed.")
                return False

            # Unzip the recently downloaded file
            self.OutputUpdater.emit("Extracting files to {0}".format(file_dir))
            try:
                zipper = zipfile.ZipFile(file_dir, 'r')
                zipper.extractall(self.settings.data['settings']['wow_dir'] + '/' + item.name)
                zipper.close()
                self.OutputUpdater.emit("Extraction complete.")

                # Set the addon's current version to the latest.
                for key in self.settings.data['addons']:
                    logging.debug("Key: {0}".format(str(key)))
                    logging.debug("Item name: {0}".format(item.name))
                    logging.debug("Transformed name: {0}".format(item.name.title().replace("-", " ").replace("_", " ")))
                    logging.debug("Transformed key: {0}".format(key.title().replace("-", " ").replace("_", " ")))

                    if str(key) == item.name:
                        logging.debug("Addon found for key!")
                        logging.debug("Item's latest version: {0}".format(item.latest_version))
                        self.settings.data['addons'][key]['current_version'] = item.latest_version
                        logging.debug("New current version: {0}".format(self.settings.data['addons'][key]['current_version']))

                        self.settings.save_config()
                        self.settings.load_config()

            except Exception as ze:
                logging.critical("Error unzipping addon: {0}".format(ze))
                self.OutputUpdater.emit("Error unzipping addon: {0}".format(ze))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

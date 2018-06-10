from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from gui_py.main_window_gui import Ui_MainWindow
from window_classes.AddonWindow import AddonWindow
from window_classes.SettingsWindow import SettingsWindow
import sys
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

        settings = Settings()

    except Exception as e:
        print(e)

    def __init__(self):
        super(MainWindowPrompt, self).__init__()

        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self)

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

        self.window.ui.actionAddAddon.triggered.connect(self.OpenAddonAdder.emit)
        self.window.ui.actionSettings.triggered.connect(self.OpenSettingsWindow.emit)
        self.window.ui.btnCheckForUpdates.clicked.connect(self.update_worker.start)


    @pyqtSlot()
    def add_addon(self):
        addon_window = AddonWindow(self.settings, self)
        addon_window.exec()

    @pyqtSlot(str)
    def insert_output_text(self, text):
        self.window.ui.teditOutput.insertPlainText(text + '\n')

    @pyqtSlot()
    def show_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.exec()

    def execute_check_updates(self):
        updater = UpdateChecker(self.settings)
        update_list = updater.check_for_updates()

        self.PromptUpdate.emit(update_list)

    @pyqtSlot(list)
    def prompt_to_update(self, update_list):

        if update_list:
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
            message_box.setText("All addons are up to date!")
            message_box.setStandardButtons(QMessageBox.Ok)

            message_box.exec()

    @pyqtSlot()
    def execute_download(self):
        d = Downloader(self.settings, './')
        # to_update = d.check_for_updates()
        to_update = self.settings.files_to_update
        logging.info("Update list: {0}".format(to_update))
        for item in to_update:
            self.OutputUpdater.emit("Downloading files for {0}...".format(item.name.title()))
            response, file_dir = d.download_from_url(item)
            logging.info("Item: {0}".format(item.url))
            if response:
                self.OutputUpdater.emit("Download complete.")
            else:
                self.OutputUpdater.emit("Download failed.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

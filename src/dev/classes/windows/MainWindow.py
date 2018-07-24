from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QTreeView, QPushButton
from PyQt5.Qt import QSizePolicy
from PyQt5.QtGui import QTextCursor, QStandardItemModel, QStandardItem, QMovie, QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QItemSelectionModel
from src.gui_py.main_window_gui import Ui_MainWindow
from src.dev.classes.windows.AddonWindow import AddonWindow
from src.dev.classes.windows.SettingsWindow import SettingsWindow
from src.dev.classes.windows.AboutWindow import AboutWindow
import sys
from src.dev.classes.addon.Addon import Addon
from src.dev.classes.workers.Worker import Worker
from src.dev.classes.application.Settings import Settings
from src.dev.classes.updates.Downloader import Downloader
from src.dev.classes.updates.UpdateChecker import UpdateChecker
import logging
import src.icons_rc

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


class MainWindow(QMainWindow):

    try:
        OpenAddonAdder = pyqtSignal()
        OpenSettingsWindow = pyqtSignal()
        OutputUpdater = pyqtSignal(str)
        PromptUpdate = pyqtSignal(list)
        DownloadStart = pyqtSignal()
        MessageBox = pyqtSignal(str, str, str)
        UpdateTreeView = pyqtSignal()
        AddAddon = pyqtSignal(Addon, QTreeView, QStandardItemModel)
        # UpdateProgressBarValue = pyqtSignal(int)
        # UpdateProgressBarMax = pyqtSignal(int)
        RemoveAddon = pyqtSignal(str)
        LoadingGifSignal = pyqtSignal(bool)
        SetUpdateCount = pyqtSignal(int, int)

    except Exception as e:
        print(e)

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self)
        self.app = QApplication(sys.argv)

        self.settings = Settings()
        self.movie = QMovie(":/app/loading_icon.gif")

        self.download_worker = Worker(self.execute_download)
        self.update_worker = Worker(self.execute_check_updates)

        self.tree_model = self.window.ui.tviewAddons
        self.model = QStandardItemModel(self.tree_model)

        self.window.ui.actionClose.triggered.connect(self.close)
        self.window.ui.actionAbout.triggered.connect(self.open_about_window)

        self.init_ui()

    def closeEvent(self, event):
        if self.settings.config['settings']['prompt_to_close']:
            prompt = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to quit?',
                                          QMessageBox.Yes, QMessageBox.No)

            if prompt == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def init_ui(self):
        self.window.ui.splitter.setStyleSheet(HANDLE_STYLE)

        self.OpenAddonAdder.connect(self.add_addon)
        self.OpenSettingsWindow.connect(self.show_settings_window)
        self.OutputUpdater.connect(self.insert_output_text)
        self.PromptUpdate.connect(self.prompt_to_update)
        self.DownloadStart.connect(self.execute_download)
        self.MessageBox.connect(self.show_message_box)
        self.UpdateTreeView.connect(self.update_tree_view)
        self.AddAddon.connect(self.add_addon_to_tree_view)
        # self.UpdateProgressBarValue.connect(self.set_progress_bar_value)
        # self.UpdateProgressBarMax.connect(self.set_progress_bar_max)
        self.RemoveAddon.connect(self.remove_addon)
        self.LoadingGifSignal.connect(self.toggle_loading_gif)
        self.SetUpdateCount.connect(self.set_update_count_value)

        self.window.ui.actionAddAddon.triggered.connect(self.OpenAddonAdder.emit)
        self.window.ui.actionSettings.triggered.connect(self.OpenSettingsWindow.emit)
        self.window.ui.btnCheckForUpdates.clicked.connect(self.update_worker.start)
        self.window.ui.btnDownloadUpdates.clicked.connect(self.download_worker.start)
        self.window.ui.actionUpdateTreeView.triggered.connect(self.UpdateTreeView.emit)

        # self.UpdateProgressBarMax.emit(10)
        # self.UpdateProgressBarValue.emit(0)
        # self.window.ui.progressBar.setVisible(False)

        # Setting the header to hidden removes the drag bar for column width resizing.
        # self.window.ui.tviewAddons.setHeaderHidden(True)

        self.UpdateTreeView.emit()

        self.settings.check_for_wow_directory(self)
        self.window.ui.label.setHidden(True)
        self.window.ui.btnDownloadUpdates.setHidden(True)

        self.window.ui.tviewAddons.setColumnWidth(0, 300)

        self.window.ui.lblLoadingMovie.setMovie(self.movie)
        self.window.ui.lblLoadingMovie.setMaximumHeight(50)
        self.window.ui.lblLoadingMovie.setScaledContents(True)
        self.window.ui.lblLoadingMovie.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.window.ui.frameUpdate.setVisible(False)

    @pyqtSlot()
    def add_addon(self):
        addon_window = AddonWindow(self.settings, self)
        addon_window.exec()

    @pyqtSlot()
    def open_about_window(self):
        about_window = AboutWindow(self)
        about_window.exec()

    @pyqtSlot(str)
    def insert_output_text(self, text):
        self.window.ui.teditOutput.insertPlainText(text + '\n')
        self.window.ui.teditOutput.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def show_settings_window(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()

    @pyqtSlot(int)
    def set_progress_bar_value(self, val):
        self.window.ui.progressBar.setValue(val)

    @pyqtSlot(bool)
    def toggle_loading_gif(self, enabled):
        if enabled:
            self.window.ui.frameUpdate.setVisible(True)
            self.window.ui.btnCheckForUpdates.setVisible(False)
            self.movie.start()
        else:
            self.window.ui.frameUpdate.setVisible(False)
            self.window.ui.btnCheckForUpdates.setVisible(True)
            self.movie.stop()

    @pyqtSlot(int, int)
    def set_update_count_value(self, current, max):
        self.window.ui.lblCurrentUpdate.setText("( {0} out of {1} )".format(current, max))

    @pyqtSlot(int)
    def set_progress_bar_max(self, val):
        self.window.ui.progressBar.setMaximum(val)

    @pyqtSlot(Addon, QTreeView, QStandardItemModel)
    def add_addon_to_tree_view(self, addon, tree_model, model):
        tree_model.setModel(model)

        parent_item = QStandardItem(addon.name)
        col1 = QStandardItem()

        url_item = QStandardItem()
        remove_addon_item = QStandardItem()

        # Create a QLabel to allow following hyperlinks in the table.
        url_label = QLabel()
        url_label.setTextFormat(1)
        url_label.setOpenExternalLinks(True)
        url_text = "<a href=\"" + addon.url + "\"> " + addon.name + "</a>"
        url_label.setText(url_text)

        remove_addon_button = QPushButton()
        remove_addon_button.setText("Remove {0}".format(addon.name))
        remove_addon_button.clicked.connect(lambda: self.RemoveAddon.emit(addon.name))
        remove_addon_button.setMaximumSize(80 + (len(remove_addon_button.text()) * 5), 30)

        curr_ver_item = QStandardItem(addon.current_version)
        latest_ver_item = QStandardItem(addon.latest_version)

        logging.debug("Parent item: {0}".format(addon.name))

        model.appendRow([parent_item, col1])

        url_item_identifier = QStandardItem("Addon Link: ")
        curr_ver_item_identifier = QStandardItem("Current Version: ")
        latest_ver_item_identifier = QStandardItem("Latest Version: ")
        remove_addon_item_identifier = QStandardItem("Remove Addon: ")

        # Append URL, Current Version, and Latest Version to the parent
        parent_item.appendRow([url_item_identifier, url_item])

        # Append URL as a QLabel to allow the hyperlink to be clicked on.
        self.window.ui.tviewAddons.setIndexWidget(url_item.index(), url_label)

        parent_item.appendRow([curr_ver_item_identifier, curr_ver_item])
        parent_item.appendRow([latest_ver_item_identifier, latest_ver_item])

        parent_item.appendRow([remove_addon_item_identifier, remove_addon_item])
        self.window.ui.tviewAddons.setIndexWidget(remove_addon_item.index(), remove_addon_button)

        # self.window.ui.tviewAddons.setColumnWidth(0, self.window.ui.tviewAddons.columnWidth(0) + 50)

        # Comment out header as I don't like the look at the moment.
        self.model.setHeaderData(0, 0x01, "Addons")
        self.model.setHeaderData(1, 0x01, "")

    @pyqtSlot(str)
    def remove_addon(self, addon_name):
        if addon_name not in self.settings.addons['addons']:
            return

        message_box = QMessageBox.question(None, "Confirmation",
                                           "Are you sure you want to remove {0}?".format(addon_name),
                                           QMessageBox.Yes, QMessageBox.No)
        if message_box == QMessageBox.Yes:
            del self.settings.addons['addons'][addon_name]
            # print(self.settings.data.pop(key, None))
            self.settings.save_addons()
            self.settings.load_addons()

            index = self.window.ui.tviewAddons.selectionModel().selectedRows()[0]
            parent = index.parent()

            self.window.ui.tviewAddons.selectionModel().setCurrentIndex(self.window.ui.tviewAddons.indexAbove(index),
                                                                        QItemSelectionModel.ClearAndSelect)
            self.model.removeRow(parent.row())

    @pyqtSlot()
    def update_tree_view(self):
        tree_data = self.settings.addons['addons']
        logging.debug("Tree view data: {0}".format(tree_data))

        # No addons are loaded.
        # TODO: Insert blank row indicating there are no addons.
        if len(tree_data) == 0:
            pass
        if self.model.hasChildren():
            self.model.removeRows(0, self.model.rowCount())

        for parent_name in tree_data:
            current_addon = Addon(tree_data[parent_name]['url'], tree_data[parent_name]['name'],
                                  tree_data[parent_name]['current_version'], tree_data[parent_name]['latest_version'])

            self.AddAddon.emit(current_addon, self.tree_model, self.model)

        self.window.ui.tviewAddons.sortByColumn(0, 0x00)

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
        message_box.setWindowIcon(QIcon(":/app/icon.ico"))
        message_box.exec()

    def execute_check_updates(self):

        if not self.settings.check_for_wow_directory(self):
            return

        if len(self.settings.addons['addons']) == 0:
            self.MessageBox.emit("No AddOns have been specified.",
                                 "To add an addon, press 'Addon' -> 'Add Addon' and enter the URL of the addon.",
                                 "warn")
            return

        self.window.ui.btnCheckForUpdates.setText("Checking {0} Addons For Updates...".format(
            len(self.settings.addons['addons'])))
        self.window.ui.btnCheckForUpdates.setDisabled(True)
        self.OutputUpdater.emit("Checking for updates...")

        updater = UpdateChecker(self)
        self.LoadingGifSignal.emit(True)

        update_list = updater.check_for_updates()
        self.LoadingGifSignal.emit(False)

        self.window.ui.btnCheckForUpdates.setText("Check For Updates")
        self.window.ui.btnCheckForUpdates.setEnabled(True)

        # if update_list:
        self.PromptUpdate.emit(update_list)

    @pyqtSlot(list)
    def prompt_to_update(self, update_list):

        if update_list:
            self.window.ui.btnDownloadUpdates.setVisible(True)
            self.OutputUpdater.emit("AddOns out of date:")
            for addon in update_list:
                self.OutputUpdater.emit("\n{0}: \n\tCurrent version: {1} \n\tNew version:      {2}\n".format(addon.name,
                                                                                            addon.current_version,
                                                                                            addon.latest_version))
            message_box = QMessageBox.question(None, "Updates found",
                                               "{0} update{1} found. Would you like to download {2} now?".format(
                                                   len(update_list),
                                                   "s" if len(update_list) > 1 else "",
                                                   "them" if len(update_list) > 1 else "it"),
                                               QMessageBox.Yes, QMessageBox.No)
            if message_box == QMessageBox.Yes:
                self.download_worker.start()

        else:
            # message_box = QMessageBox()
            # message_box.setWindowTitle("Checker")
            # message_box.setText("All AddOns are up to date!")
            self.OutputUpdater.emit("\nAll AddOns are currently up to to date.")
            # message_box.setStandardButtons(QMessageBox.Ok)
            #
            # message_box.exec()

    @pyqtSlot()
    def execute_download(self):
        d = Downloader(self)
        to_update = self.settings.files_to_update
        logging.info("Update list: {0}".format(to_update))
        self.LoadingGifSignal.emit(True)
        current_download_val = 1
        download_failed_list = []
        self.window.ui.btnDownloadUpdates.setVisible(False)

        for addon in to_update:
            self.SetUpdateCount.emit(current_download_val, len(to_update))

            if not d.update_addon(addon):
                download_failed_list.append(addon.name)

            self.SetUpdateCount.emit(current_download_val, len(to_update))
            current_download_val += 1

        self.LoadingGifSignal.emit(False)

        # If downloads failed, tell the user.
        if download_failed_list:
            update_text = "The following AddOns failed to download: {0}".format(download_failed_list)

            self.MessageBox.emit("Status", update_text, "warn")
        else:
            update_text = "All AddOns were downloaded and extracted successfully to AddOns folder."
            self.MessageBox.emit("Complete", update_text, "inform")

        self.OutputUpdater.emit(update_text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

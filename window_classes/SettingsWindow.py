from gui_py.settings_gui import Ui_Settings
from PyQt5.QtWidgets import QDialog, QFileDialog
import logging


class SettingsWindow(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_Settings()
        self.window.ui.setupUi(self)
        self.parent = parent
        self.window.ui.btnBrowseWowDirectory.clicked.connect(lambda: self.set_wow_dir(self.parent.settings))

        self.init_ui()

    def init_ui(self):
        self.window.ui.btnApply.clicked.connect(self.save_settings)
        self.window.ui.btnBox.accepted.connect(self.ok_settings)
        self.window.ui.btnBox.rejected.connect(self.close)
        self.window.ui.leditWowDirectory.setText(self.parent.settings.data['settings']['wow_dir'])

    def save_settings(self):
        self.parent.settings.data['settings']['wow_dir'] = self.window.ui.leditWowDirectory.text()
        self.parent.settings.save_config()
        self.parent.settings.load_config()

    def ok_settings(self):
        self.save_settings()
        self.close()

    def set_wow_dir(self, settings):
        file_name = open_file_dialog("Browse for World of Warcraft Game Directory")

        if file_name is not None:

            if str(file_name).endswith("/AddOn"):
                file_name.strip("/AddOn")

            self.window.ui.leditWowDirectory.setText(file_name)
            settings.data['settings']['wow_dir'] = file_name


def open_file_dialog(title):
    try:
        options = QFileDialog.Options()

        file_name = QFileDialog.getExistingDirectory(None, title, "", options=options)

        if file_name != "":
            print(file_name)
            return file_name
        else:
            return None

    except Exception as e:
        logging.critical("Error opening File Dialog: {0}".format(e))


def main():
    SettingsWindow()


if __name__ == '__main__':
    main()



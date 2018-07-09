from src.gui_py.settings_gui import Ui_Settings
from PyQt5.QtWidgets import QDialog, QFileDialog
import logging
import os


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

        self.load_settings()

    def load_settings(self):
        self.window.ui.leditWowDirectory.setText(self.parent.settings.config['settings']['wow_dir'])
        self.window.ui.cboxPromptToClose.setChecked(self.parent.settings.config['settings']['prompt_to_close'])
        self.window.ui.cboxReplaceArchive.setChecked(self.parent.settings.config['settings']['remove_old_archive'])

    def save_settings(self):
        self.parent.settings.config['settings']['wow_dir'] = self.window.ui.leditWowDirectory.text()
        self.parent.settings.config['settings']['prompt_to_close'] = self.window.ui.cboxPromptToClose.isChecked()
        self.parent.settings.config['settings']['remove_old_archive'] = self.window.ui.cboxReplaceArchive.isChecked()
        self.parent.settings.save_config()
        self.parent.settings.load_config()

    def ok_settings(self):
        self.save_settings()
        self.close()

    def set_wow_dir(self, settings):
        file_name = open_file_dialog("Browse for World of Warcraft AddOns Directory")

        if file_name is not None:

            if not str(file_name).endswith('/Interface/AddOns'):

                if str(file_name).endswith('/Interface'):
                    file_name += '/AddOns'
                else:
                    file_name += '/Interface/AddOns'

            if not os.path.isdir(os.path.abspath(file_name)):
                self.parent.MessageBox.emit("Could not verify AddOns directoy.",
                                            "{0} does not seem to be a valid WoW directory. Please verify WoW AddOns "
                                            "directory.".format(file_name.strip('/Interface/AddOns')), "warn")

                return

            self.window.ui.leditWowDirectory.setText(file_name)
            settings.config['settings']['wow_dir'] = file_name


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



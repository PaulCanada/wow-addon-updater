from gui_py.settings_gui import Ui_Settings
from PyQt5.QtWidgets import QDialog


class SettingsWindow(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_Settings()
        self.window.ui.setupUi(self)
        self.parent = parent

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


def main():
    SettingsWindow()


if __name__ == '__main__':
    main()



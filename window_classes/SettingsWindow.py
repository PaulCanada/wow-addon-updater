from gui_py.settings_gui import Ui_Settings
from PyQt5.QtWidgets import QDialog


class SettingsWindow(QDialog):

    def __init__(self):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_Settings()
        self.window.ui.setupUi(self)


def main():
    SettingsWindow()


if __name__ == '__main__':
    main()



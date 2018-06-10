from gui_py.settings_gui import Ui_Settings
from PyQt5.QtWidgets import QWidget


class SettingsWindow(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.window = QWidget()
        self.window.ui = Ui_Settings()
        self.window.ui.setupUi(self)
        self.window.show()


def main():
    SettingsWindow()


if __name__ == '__main__':
    main()



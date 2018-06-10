from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from gui_py.main_window_gui import Ui_MainWindow
from window_classes.AddonWindow import AddonWindow
from window_classes.SettingsWindow import SettingsWindow
import sys
from Settings import Settings
from overrides.internal_overrides import MainWindowPrompt

sys._excepthook = sys.excepthook

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
        settings = Settings()

    except Exception as e:
        print(e)

    def __init__(self):
        super(MainWindowPrompt, self).__init__()

        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self)
        self.window.ui.splitter.setStyleSheet(HANDLE_STYLE)

        self.OpenAddonAdder.connect(self.add_addon)
        self.OpenSettingsWindow.connect(self.show_settings_window)

        self.window.ui.actionAddAddon.triggered.connect(self.OpenAddonAdder.emit)
        self.window.ui.actionSettings.triggered.connect(self.OpenSettingsWindow.emit)

    @pyqtSlot()
    def add_addon(self):
        addon_window = AddonWindow(self.settings, self)
        addon_window.exec()

    @pyqtSlot()
    def show_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.exec()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_py.main_window_gui import Ui_MainWindow
import sys
from overrides.internal_overrides import MainWindowPrompt

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

    def __init__(self):
        super(MainWindowPrompt, self).__init__()

        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self)
        self.window.ui.splitter.setStyleSheet(HANDLE_STYLE)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

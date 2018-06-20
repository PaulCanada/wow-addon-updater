from src.dev.classes.windows.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import logging

sys._excepthook = sys.excepthook
logging.getLogger().setLevel(logging.CRITICAL)


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

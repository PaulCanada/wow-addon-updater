from window_classes.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
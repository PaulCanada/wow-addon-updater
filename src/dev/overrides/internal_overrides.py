from PyQt5.QtWidgets import QMainWindow, QMessageBox


class MainWindowPrompt(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

    def closeEvent(self, event):
        prompt = QMessageBox.question(self, 'Are you sure you want to quit?', 'Task is in progress !',
                                      QMessageBox.Yes, QMessageBox.No)

        if prompt == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

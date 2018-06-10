from gui_py.addon_window_gui import Ui_Form
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import requests
import requests.exceptions
import sys


class AddonWindow(QDialog):

    ErrorBox = pyqtSignal(str, str)

    def __init__(self):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_Form()
        self.window.ui.setupUi(self)
        self.window.ui.buttonBox.accepted.connect(self.add)
        self.window.ui.buttonBox.rejected.connect(self.close)
        self.ErrorBox.connect(self.show_error)


    def add(self):
        print(self.window.ui.leditAddonUrl.text())
        try:
            response = requests.get(self.window.ui.leditAddonUrl.text())

            print(response)

        except requests.exceptions.MissingSchema as e:
            print(e)
            self.ErrorBox.emit("Invalid URL: missing scehma.", "URL is missing 'http' or 'https'.")
        except requests.exceptions.ConnectionError as ce:
            print(ce)
            self.ErrorBox.emit("Invalid URL", "Cannot reach requested URL: {0}".format(
                self.window.ui.leditAddonUrl.text()))

    @pyqtSlot(str, str)
    def show_error(self, message='', inform=''):
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText(message)
        error.setInformativeText(inform)
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        error.exec()

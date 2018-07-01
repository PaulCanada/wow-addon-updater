from src.gui_py.about_gui import Ui_About
from PyQt5.QtWidgets import QDialog


class AboutWindow(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_About()
        self.window.ui.setupUi(self)
        self.parent = parent

        self.init_ui()

    def init_ui(self):

        self.window.ui.lblGit.setTextFormat(1)
        self.window.ui.lblGit.setOpenExternalLinks(True)

        self.window.ui.lblGit.setText("Find an issue? Report it on the <a href=\"" +
                                      'https://github.com/PaulCanada/wow-addon-updater' +
                                      "\"> " + 'GitHub Repository' + "</a>.")

        self.window.ui.lblLicense.setTextFormat(1)
        self.window.ui.lblLicense.setOpenExternalLinks(True)
        self.window.ui.lblLicense.setText("This application is licensed under <a href=\"" +
                                          'https://github.com/PaulCanada/wow-addon-updater/blob/master/LICENSE' +
                                          "\"> " + 'GNU General Public License v3.0' + "</a>.")

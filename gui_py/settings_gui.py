# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(400, 459)
        self.formLayout = QtWidgets.QFormLayout(Settings)
        self.formLayout.setObjectName("formLayout")
        self.lblWowDirectory = QtWidgets.QLabel(Settings)
        self.lblWowDirectory.setObjectName("lblWowDirectory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblWowDirectory)
        self.leditWowDirectory = QtWidgets.QLineEdit(Settings)
        self.leditWowDirectory.setObjectName("leditWowDirectory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.leditWowDirectory)
        self.pushButton = QtWidgets.QPushButton(Settings)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnBox = QtWidgets.QDialogButtonBox(Settings)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnBox.setObjectName("btnBox")
        self.horizontalLayout.addWidget(self.btnBox)
        self.btnApply = QtWidgets.QPushButton(Settings)
        self.btnApply.setObjectName("btnApply")
        self.horizontalLayout.addWidget(self.btnApply)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.lblWowDirectory.setText(_translate("Settings", "WoW Directory:"))
        self.pushButton.setText(_translate("Settings", "Browse..."))
        self.btnApply.setText(_translate("Settings", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings = QtWidgets.QWidget()
    ui = Ui_Settings()
    ui.setupUi(Settings)
    Settings.show()
    sys.exit(app.exec_())


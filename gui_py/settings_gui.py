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
        Settings.resize(400, 342)
        Settings.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout_2 = QtWidgets.QFormLayout(Settings)
        self.formLayout_2.setObjectName("formLayout_2")
        self.frame = QtWidgets.QFrame(Settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.lblWowDirectory = QtWidgets.QLabel(self.frame)
        self.lblWowDirectory.setObjectName("lblWowDirectory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblWowDirectory)
        self.leditWowDirectory = QtWidgets.QLineEdit(self.frame)
        self.leditWowDirectory.setObjectName("leditWowDirectory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.leditWowDirectory)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnBox = QtWidgets.QDialogButtonBox(Settings)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnBox.setObjectName("btnBox")
        self.horizontalLayout.addWidget(self.btnBox)
        self.btnApply = QtWidgets.QPushButton(Settings)
        self.btnApply.setObjectName("btnApply")
        self.horizontalLayout.addWidget(self.btnApply)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)

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


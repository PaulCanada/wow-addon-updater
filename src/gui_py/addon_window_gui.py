# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\addon_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(589, 88)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.lblAddonUrl = QtWidgets.QLabel(Form)
        self.lblAddonUrl.setObjectName("lblAddonUrl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblAddonUrl)
        self.leditAddonUrl = QtWidgets.QLineEdit(Form)
        self.leditAddonUrl.setObjectName("leditAddonUrl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.leditAddonUrl)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.SpanningRole, spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblAddonUrl.setText(_translate("Form", "Addon URL:"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


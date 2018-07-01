# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\addon_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddonWindow(object):
    def setupUi(self, AddonWindow):
        AddonWindow.setObjectName("AddonWindow")
        AddonWindow.resize(589, 88)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddonWindow.setWindowIcon(icon)
        self.formLayout = QtWidgets.QFormLayout(AddonWindow)
        self.formLayout.setObjectName("formLayout")
        self.lblAddonUrl = QtWidgets.QLabel(AddonWindow)
        self.lblAddonUrl.setObjectName("lblAddonUrl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblAddonUrl)
        self.leditAddonUrl = QtWidgets.QLineEdit(AddonWindow)
        self.leditAddonUrl.setObjectName("leditAddonUrl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.leditAddonUrl)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddonWindow)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.SpanningRole, spacerItem)

        self.retranslateUi(AddonWindow)
        QtCore.QMetaObject.connectSlotsByName(AddonWindow)

    def retranslateUi(self, AddonWindow):
        _translate = QtCore.QCoreApplication.translate
        AddonWindow.setWindowTitle(_translate("AddonWindow", "Add an AddOn"))
        self.lblAddonUrl.setText(_translate("AddonWindow", "Addon URL:"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddonWindow = QtWidgets.QWidget()
    ui = Ui_AddonWindow()
    ui.setupUi(AddonWindow)
    AddonWindow.show()
    sys.exit(app.exec_())


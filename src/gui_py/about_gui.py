# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(400, 233)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QtCore.QSize(0, 233))
        About.setMaximumSize(QtCore.QSize(600, 233))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About.setWindowIcon(icon)
        self.formLayout = QtWidgets.QFormLayout(About)
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.lblHeader = QtWidgets.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblHeader.setFont(font)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.lblHeader)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.lblInfo = QtWidgets.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblInfo.setFont(font)
        self.lblInfo.setObjectName("lblInfo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.lblInfo)
        spacerItem2 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(7, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.label = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lblLicense = QtWidgets.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblLicense.setFont(font)
        self.lblLicense.setObjectName("lblLicense")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.lblLicense)
        self.lblGit = QtWidgets.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblGit.setFont(font)
        self.lblGit.setObjectName("lblGit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.lblGit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(9, QtWidgets.QFormLayout.LabelRole, spacerItem4)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.lblHeader.setText(_translate("About", "WoW Addon Updater"))
        self.lblInfo.setText(_translate("About", "Unnoficial AddOn updater for popular the game World of Warcraft."))
        self.label.setText(_translate("About", "Made by Paul Canada, 2018"))
        self.lblLicense.setText(_translate("About", "This application is licensed under GNU v3."))
        self.lblGit.setText(_translate("About", "Find an issue? Report it on the GibHub Repository."))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    About = QtWidgets.QDialog()
    ui = Ui_About()
    ui.setupUi(About)
    About.show()
    sys.exit(app.exec_())


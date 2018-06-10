# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.frameAddons = QtWidgets.QFrame(self.splitter)
        self.frameAddons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAddons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameAddons.setObjectName("frameAddons")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frameAddons)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tviewAddons = QtWidgets.QTreeView(self.frameAddons)
        self.tviewAddons.setObjectName("tviewAddons")
        self.gridLayout_3.addWidget(self.tviewAddons, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frameAddons)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.frameOutput = QtWidgets.QFrame(self.splitter)
        self.frameOutput.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutput.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutput.setObjectName("frameOutput")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameOutput)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.teditOutput = QtWidgets.QTextEdit(self.frameOutput)
        self.teditOutput.setObjectName("teditOutput")
        self.gridLayout_2.addWidget(self.teditOutput, 1, 0, 1, 1)
        self.lblOutput = QtWidgets.QLabel(self.frameOutput)
        self.lblOutput.setObjectName("lblOutput")
        self.gridLayout_2.addWidget(self.lblOutput, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wow Addon Updater"))
        self.label.setText(_translate("MainWindow", "Addons"))
        self.lblOutput.setText(_translate("MainWindow", "Output"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


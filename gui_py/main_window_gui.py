# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 634)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.tviewAddons.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 2)
        self.btnCheckForUpdates = QtWidgets.QPushButton(self.centralwidget)
        self.btnCheckForUpdates.setMinimumSize(QtCore.QSize(0, 40))
        self.btnCheckForUpdates.setObjectName("btnCheckForUpdates")
        self.gridLayout.addWidget(self.btnCheckForUpdates, 2, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAddon = QtWidgets.QMenu(self.menubar)
        self.menuAddon.setObjectName("menuAddon")
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
        self.actionAddAddon = QtWidgets.QAction(MainWindow)
        self.actionAddAddon.setObjectName("actionAddAddon")
        self.actionUpdateTreeView = QtWidgets.QAction(MainWindow)
        self.actionUpdateTreeView.setObjectName("actionUpdateTreeView")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionClose)
        self.menuAddon.addAction(self.actionAddAddon)
        self.menuAddon.addAction(self.actionUpdateTreeView)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAddon.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WoW Addon Updater"))
        self.label.setText(_translate("MainWindow", "Addons"))
        self.lblOutput.setText(_translate("MainWindow", "Output"))
        self.btnCheckForUpdates.setText(_translate("MainWindow", "Check For Updates"))
        self.progressBar.setFormat(_translate("MainWindow", "%v/%m"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAddon.setTitle(_translate("MainWindow", "Addon"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAddAddon.setText(_translate("MainWindow", "Add Addon"))
        self.actionUpdateTreeView.setText(_translate("MainWindow", "Update Tree View"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


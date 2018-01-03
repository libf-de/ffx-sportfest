# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/xorg/eric/Sportfest/main.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menuBar.setObjectName("menuBar")
        self.menuDatei = QtWidgets.QMenu(self.menuBar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuSch_ler = QtWidgets.QMenu(self.menuBar)
        self.menuSch_ler.setObjectName("menuSch_ler")
        MainWindow.setMenuBar(self.menuBar)
        self.actionDatenbank_bearbeiten = QtWidgets.QAction(MainWindow)
        self.actionDatenbank_bearbeiten.setObjectName("actionDatenbank_bearbeiten")
        self.actionBeenden = QtWidgets.QAction(MainWindow)
        self.actionBeenden.setObjectName("actionBeenden")
        self.menuDatei.addAction(self.actionBeenden)
        self.menuSch_ler.addAction(self.actionDatenbank_bearbeiten)
        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuSch_ler.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menuSch_ler.setTitle(_translate("MainWindow", "Schüler"))
        self.actionDatenbank_bearbeiten.setText(_translate("MainWindow", "Datenbank bearbeiten"))
        self.actionBeenden.setText(_translate("MainWindow", "Beenden"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


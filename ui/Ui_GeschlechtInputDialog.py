# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/xorg/eric/Sportfest/ui/GeschlechtInputDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 260)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.forAllButton = QtWidgets.QPushButton(Dialog)
        self.forAllButton.setCheckable(True)
        self.forAllButton.setObjectName("forAllButton")
        self.gridLayout.addWidget(self.forAllButton, 3, 1, 1, 1)
        self.helpButton = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/dialog_buttons/help"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.helpButton.setIcon(icon)
        self.helpButton.setFlat(False)
        self.helpButton.setObjectName("helpButton")
        self.gridLayout.addWidget(self.helpButton, 3, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/dialog_buttons/cancel"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon1)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 3, 2, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.femaleButton = QtWidgets.QPushButton(self.widget)
        self.femaleButton.setMinimumSize(QtCore.QSize(0, 80))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(102, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(102, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(102, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.femaleButton.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.femaleButton.setFont(font)
        self.femaleButton.setStyleSheet("QPushButton:pressed {\n"
"    background-color: rgba(225,0,0,255);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton {\n"
"     background-color: #ff0000; border: 1px solid black;\n"
"     border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(102, 0, 0)\n"
"}")
        self.femaleButton.setCheckable(True)
        self.femaleButton.setAutoDefault(False)
        self.femaleButton.setObjectName("femaleButton")
        self.gridLayout_2.addWidget(self.femaleButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 2)
        self.maleButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maleButton.sizePolicy().hasHeightForWidth())
        self.maleButton.setSizePolicy(sizePolicy)
        self.maleButton.setMinimumSize(QtCore.QSize(0, 80))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 102))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 102))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 102))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.maleButton.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.maleButton.setFont(font)
        self.maleButton.setStyleSheet("QPushButton:pressed {\n"
"    background-color: rgba(0,220,220,255);\n"
"    border: 2px solid black;\n"
"}\n"
"QPushButton {\n"
"     background-color: #00ffff; border: 1px solid black;\n"
"     border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(0, 102, 102)\n"
"}")
        self.maleButton.setCheckable(False)
        self.maleButton.setChecked(False)
        self.maleButton.setAutoDefault(False)
        self.maleButton.setFlat(True)
        self.maleButton.setObjectName("maleButton")
        self.gridLayout_2.addWidget(self.maleButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.cancelButton, self.maleButton)
        Dialog.setTabOrder(self.maleButton, self.femaleButton)
        Dialog.setTabOrder(self.femaleButton, self.forAllButton)
        Dialog.setTabOrder(self.forAllButton, self.helpButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FFSportfest - Geschlecht auswählen"))
        self.forAllButton.setToolTip(_translate("Dialog", "<html><head/><body><p>Wendet die Auswahl auf alle folgenden ungültigen Geschlechter an</p></body></html>"))
        self.forAllButton.setText(_translate("Dialog", "Für alle"))
        self.helpButton.setText(_translate("Dialog", " Hilfe"))
        self.cancelButton.setText(_translate("Dialog", " Abbrechen"))
        self.femaleButton.setText(_translate("Dialog", "Weiblich"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:20pt;\">Max Mustermann</span></p><p>(männlich)</p></body></html>"))
        self.maleButton.setText(_translate("Dialog", "Männlich"))

import oxyicons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


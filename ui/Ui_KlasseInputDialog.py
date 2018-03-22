# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/xorg/eric/Sportfest/ui/KlasseInputDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(377, 177)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.dlgText = QtWidgets.QLabel(self.widget)
        self.dlgText.setWordWrap(True)
        self.dlgText.setObjectName("dlgText")
        self.gridLayout_2.addWidget(self.dlgText, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.yesBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yesBtn.sizePolicy().hasHeightForWidth())
        self.yesBtn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/dialog_buttons/ok"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.yesBtn.setIcon(icon)
        self.yesBtn.setObjectName("yesBtn")
        self.horizontalLayout.addWidget(self.yesBtn)
        self.yesToAllBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yesToAllBtn.sizePolicy().hasHeightForWidth())
        self.yesToAllBtn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/dialog_buttons/all"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.yesToAllBtn.setIcon(icon1)
        self.yesToAllBtn.setObjectName("yesToAllBtn")
        self.horizontalLayout.addWidget(self.yesToAllBtn)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelBtn.sizePolicy().hasHeightForWidth())
        self.cancelBtn.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/dialog_buttons/cancel"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelBtn.setIcon(icon2)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FFSportfest - Ungültige Daten"))
        self.label.setText(_translate("Dialog", "Klasse:"))
        self.dlgText.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Max Mustermann</span> (Zeile <span style=\" font-weight:600; font-style:italic;\">X</span>) hat eine ungültige Klasse (<span style=\" font-weight:600; font-style:italic;\">Y</span>). Um fortzufahren geben Sie eine gültige Klasse (z.B. 5.1) ein und bestätigen Sie mit &quot;<span style=\" font-weight:600;\">Ja</span>&quot; (für diesen Eintrag) / &quot;<span style=\" font-weight:600;\">Ja für alle</span>&quot; (für alle folgenden ungültigen Einträge) oder &quot;<span style=\" font-weight:600;\">Abbrechen</span>&quot; um den Vorgang abzubrechen.</p></body></html>"))
        self.yesBtn.setText(_translate("Dialog", " &Ja"))
        self.yesToAllBtn.setText(_translate("Dialog", " Ja, &alle"))
        self.cancelBtn.setText(_translate("Dialog", " Abbrechen"))

import oxyicons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


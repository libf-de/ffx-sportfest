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
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Yes|QtWidgets.QDialogButtonBox.YesToAll)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.dlgText = QtWidgets.QLabel(self.widget)
        self.dlgText.setWordWrap(True)
        self.dlgText.setObjectName("dlgText")
        self.gridLayout_2.addWidget(self.dlgText, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FFSportfest - Ungültige Daten"))
        self.label.setText(_translate("Dialog", "Klasse:"))
        self.dlgText.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Max Mustermann</span> (Zeile <span style=\" font-weight:600; font-style:italic;\">X</span>) hat eine ungültige Klasse (<span style=\" font-weight:600; font-style:italic;\">Y</span>). Um fortzufahren geben Sie eine gültige Klasse (z.B. 5.1) ein und bestätigen Sie mit &quot;<span style=\" font-weight:600;\">Ja</span>&quot; (für diesen Eintrag) / &quot;<span style=\" font-weight:600;\">Ja für alle</span>&quot; (für alle folgenden ungültigen Einträge) oder &quot;<span style=\" font-weight:600;\">Abbrechen</span>&quot; um den Vorgang abzubrechen.</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


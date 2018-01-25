# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/xorg/eric/Sportfest/ui/SettingsPortable.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(458, 230)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(71, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.hboxlayout, 1, 0, 1, 2)
        self.widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.templateBtn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.templateBtn.sizePolicy().hasHeightForWidth())
        self.templateBtn.setSizePolicy(sizePolicy)
        self.templateBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/menu_icons_16/open"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.templateBtn.setIcon(icon)
        self.templateBtn.setFlat(True)
        self.templateBtn.setObjectName("templateBtn")
        self.gridLayout_5.addWidget(self.templateBtn, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 1, 0, 1, 1)
        self.templateLbl = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.templateLbl.sizePolicy().hasHeightForWidth())
        self.templateLbl.setSizePolicy(sizePolicy)
        self.templateLbl.setObjectName("templateLbl")
        self.gridLayout_5.addWidget(self.templateLbl, 0, 0, 1, 2)
        self.placeCount = QtWidgets.QSpinBox(self.groupBox_3)
        self.placeCount.setMinimumSize(QtCore.QSize(0, 20))
        self.placeCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.placeCount.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.placeCount.setMinimum(1)
        self.placeCount.setObjectName("placeCount")
        self.gridLayout_5.addWidget(self.placeCount, 1, 1, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ignoreNonPart = QtWidgets.QCheckBox(self.groupBox)
        self.ignoreNonPart.setObjectName("ignoreNonPart")
        self.gridLayout_3.addWidget(self.ignoreNonPart, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.okButton.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Einstellungen"))
        self.okButton.setText(_translate("Dialog", "&OK"))
        self.groupBox_3.setTitle(_translate("Dialog", "Auswertung"))
        self.label.setText(_translate("Dialog", "Anzahl der Platzierungen:"))
        self.templateLbl.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Urkundenvorlage:</span><span style=\" font-family:\'monospace\'; color:#ff0000;\">&lt;kein&gt;</span></p></body></html>"))
        self.groupBox.setTitle(_translate("Dialog", "Allgemein"))
        self.ignoreNonPart.setText(_translate("Dialog", "Nicht abgelegte Disziplinen ignorieren"))

import oxyicons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


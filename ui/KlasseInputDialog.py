# -*- coding: utf-8 -*-

"""
Module implementing KlasseInputDialog.
"""

from PyQt5.QtCore import pyqtSlot,  QRegExp
from PyQt5.QtGui import QRegExpValidator,  QValidator
from PyQt5.QtWidgets import QDialog, QAbstractButton,  QDialogButtonBox

from .Ui_KlasseInputDialog import Ui_Dialog


class KlasseInputDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    retVal = 1
    retKl = "5.1"
    def __init__(self, name,  vorname, klasse,  zeile, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(KlasseInputDialog, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("^([0-9]{1,2})\.([0-9]{1})$")))
        self.dlgText.setText("<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">{} {}</span> (Zeile <span style=\" font-weight:600; font-style:italic;\">{}</span>) hat eine ungültige Klasse (<span style=\" font-weight:600; font-style:italic;\">{}</span>). Um fortzufahren geben Sie eine gültige Klasse (z.B. 5.1) ein und bestätigen Sie mit &quot;<span style=\" font-weight:600;\">Ja</span>&quot; (für diesen Eintrag) / &quot;<span style=\" font-weight:600;\">Ja für alle</span>&quot; (für alle folgenden ungültigen Einträge) oder &quot;<span style=\" font-weight:600;\">Abbrechen</span>&quot; um den Vorgang abzubrechen.</p></body></html>".format(vorname, name, zeile, klasse))
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        
        @param button DESCRIPTION
        @type QAbstractButton
        """
        # TODO: not implemented yet
        self.retKl = self.lineEdit.text()
        if button == self.buttonBox.button(QDialogButtonBox.Yes):
            self.retVal = 2
        elif button == self.buttonBox.button(QDialogButtonBox.YesToAll):
            self.retVal = 3
        else:
            self.retVal = 1
        self.accept()
    
    def getReturnValue(self):
        return self.retVal
        
    def getReturnKlasse(self):
        return self.retKl
    
    @pyqtSlot(str)
    def on_lineEdit_textChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        validator = self.lineEdit.validator()
        state = validator.validate(p0, 0)[0]
        if state == QValidator.Acceptable:
            self.buttonBox.setEnabled(True)
            color = '#c4df9b' # green
        elif state == QValidator.Intermediate:
            self.buttonBox.setEnabled(False)
            color = '#fff79a' # yellow
        else:
            self.buttonBox.setEnabled(False)
            color = '#f6989d' # red
        
        self.lineEdit.setStyleSheet('QLineEdit { background-color: %s }' % color)

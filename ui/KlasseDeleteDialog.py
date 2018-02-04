# -*- coding: utf-8 -*-

"""
Module implementing KlasseDeleteDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_KlasseDeleteDialog import Ui_Dialog


class KlasseDeleteDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    
    klasseToDelete = None
    
    def __init__(self, klassen, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(KlasseDeleteDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.comboBox.addItems(klassen)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.klasseToDelete = self.comboBox.currentText()
        self.accept()
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.reject()

    def getKlasse(self):
        return self.klasseToDelete

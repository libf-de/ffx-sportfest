# -*- coding: utf-8 -*-

"""
Module implementing ExportDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
import os, json

from .Ui_ExportDialog import Ui_Dialog


class ExportDialog(QDialog, Ui_Dialog):
    
    JSN = {}
    klassen = [ ]
    
    """
    Class documentation goes here.
    """
    def __init__(self, JSN, klassen, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.JSN = JSN
        self.klassen = klassen
        
        self.comboBox.addItems(klassen)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        name, _ = QFileDialog.getSaveFileName(self, "Mobile Datenbank exportieren", os.path.expanduser("~"), "Mobile Datenbank (*.fmd)")
        if name:
            filename = str(name)
            if not filename.endswith(".fmd"):
                filename+= ".fmd"
            
            try:
                klassenstufe = str(self.comboBox.currentText())
                JSNE = {k:v for (k,v) in self.JSN.items() if k.startswith(klassenstufe)}
                with open(filename, 'w') as f:
                    json.dump(JSNE, f, indent=4, sort_keys=True, ensure_ascii=False)
            except PermissionError as per:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Die mobile Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diesen Ort besitzen. Bitte wählen Sie einen anderen Ort aus!")
                msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                msg.setDetailedText("Dateipfad: " + str(filename) + "\n" + str(per))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.reject()

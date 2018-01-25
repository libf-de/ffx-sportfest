# -*- coding: utf-8 -*-

"""
Module implementing SettingsPortableDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog

import os

from .Ui_SettingsPortable import Ui_Dialog


class SettingsPortableDialog(QDialog, Ui_Dialog):
    """
    Einstellungen-Dialog für portablen Modus
    """
    def __init__(self, configuration, parent=None):
        """
        Konstruktor
        
        @param parent Referenz zum Eltern-Fenster
        @type QWidget
        @param configuration Referenz zum Einstellungs-API
        @type Configuration
        """
        super(SettingsPortableDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.cfg = configuration
        
        self.setTemplatePath(self.cfg.getTemplate())
        
        self.ignoreNonPart.blockSignals(True)
        self.placeCount.blockSignals(True)
        self.ignoreNonPart.setChecked(self.cfg.getNonPart())
        self.placeCount.setValue(self.cfg.getPlaceCount())
        self.ignoreNonPart.blockSignals(False)
        self.placeCount.blockSignals(False)
        
    def setTemplatePath(self, path):
        if path is None:
            path = "&lt;kein&gt;"
        if os.path.isfile(path):
            self.templateLbl.setText("<html><head/><body><p><span style=\" font-weight:600;\">Urkundenvorlage:</span> <span style=\" font-family:'monospace'; color:#00ff00;\">{}</span></p></body></html>".format(path))
        else:
            self.templateLbl.setText("<html><head/><body><p><span style=\" font-weight:600;\">Urkundenvorlage:</span> <span style=\" font-family:'monospace'; color:#ff0000;\">{}</span></p></body></html>".format(path))
    
    @pyqtSlot()
    def on_templateBtn_clicked(self):
        """
        Vorlage öffnen-Button geklickt
        """
        tplfile,  _ = QFileDialog.getOpenFileName(self, "Dokumentenvorlage öffnen", os.path.expanduser("~"), "Word-Dokumente (*.docx)");
        if tplfile:
            self.cfg.setTemplate(str(tplfile))
            self.setTemplatePath(str(tplfile))
    
    @pyqtSlot(int)
    def on_placeCount_valueChanged(self, p0):
        """
        Anzahl der Plätze für Urkundendruck geändert
        
        @param p0 Anzahl
        @type int
        """
        self.cfg.setPlaceCount(self.placeCount.value())
    
    @pyqtSlot(bool)
    def on_ignoreNonPart_toggled(self, checked):
        """
        Nicht-Teilnahme ignorieren geändert
        
        @param checked Ignorieren ja/nein
        @type bool
        """
        self.cfg.setNonPart(checked)

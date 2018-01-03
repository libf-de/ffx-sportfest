# -*- coding: utf-8 -*-

"""
Module implementing SettingsDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog

import os

from .Ui_SettingsDialog import Ui_Dialog


class SettingsDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    
    cfg = None
    
    def __init__(self, configuration, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.cfg = configuration
        
        self.setTemplatePath(self.cfg.getTemplate())
        
        self.loadLastDb.blockSignals(True)
        self.crashSave.blockSignals(True)
        self.backupDb.blockSignals(True)
        self.ignoreNonPart.blockSignals(True)
        self.instantSort.blockSignals(True)
        self.wipeResults.blockSignals(True)
        self.guessGender.blockSignals(True)
        self.loadLastDb.setChecked(self.cfg.getLoadLastDb())
        self.crashSave.setChecked(self.cfg.getRecovery())
        self.backupDb.setChecked(self.cfg.getBackupFile())
        self.ignoreNonPart.setChecked(self.cfg.getNonPart())
        self.instantSort.setChecked(self.cfg.getInstantSort())
        self.wipeResults.setChecked(self.cfg.getWipeResults())
        self.guessGender.setChecked(self.cfg.getGuessGender())
        self.loadLastDb.blockSignals(False)
        self.crashSave.blockSignals(False)
        self.backupDb.blockSignals(False)
        self.ignoreNonPart.blockSignals(False)
        self.instantSort.blockSignals(False)
        self.wipeResults.blockSignals(False)
        self.guessGender.blockSignals(False)
        
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
        Slot documentation goes here.
        """
        tplfile,  _ = QFileDialog.getOpenFileName(self, "Dokumentenvorlage öffnen", os.path.expanduser("~"), "Word-Dokumente (*.doc *.docx)");
        if tplfile:
            self.cfg.setTemplate(str(tplfile))
            self.setTemplatePath(str(tplfile))
    
    @pyqtSlot(bool)
    def on_loadLastDb_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setLoadLastDb(checked)
    
    @pyqtSlot(bool)
    def on_crashSave_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setRecovery(checked)
    
    @pyqtSlot(bool)
    def on_backupDb_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setBackupFile(checked)
    
    @pyqtSlot(bool)
    def on_ignoreNonPart_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setNonPart(checked)
    
    @pyqtSlot(bool)
    def on_instantSort_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setInstantSort(checked)
    
    @pyqtSlot(bool)
    def on_wipeResults_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setWipeResults(checked)
    
    @pyqtSlot(bool)
    def on_guessGender_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.cfg.setGuessGender(checked)

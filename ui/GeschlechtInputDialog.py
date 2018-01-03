# -*- coding: utf-8 -*-

"""
Module implementing GeschlechtInputDialog.
"""

from PyQt5.QtCore import pyqtSlot,  Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QKeyEvent

from .Ui_GeschlechtInputDialog import Ui_Dialog


class GeschlechtInputDialog(QDialog, Ui_Dialog):
    
    forAll = False
    selected = "M"
    
    """
    Schnell-Auswahldialog für Geschlecht
    """
    def __init__(self, name,  vorname, geschlecht, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GeschlechtInputDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.label.setText("<html><head/><body><p><span style=\" font-size:20pt;\">{} {}</span></p><p>({})</p></body></html>".format(vorname,  name,  geschlecht))
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_M:
            self.selected = "M"
            self.accept()
        elif event.key() == Qt.Key_W:
            self.selected = "W"
            self.accept()
    
    @pyqtSlot(bool)
    def on_forAllButton_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        self.forAll = checked
    
    @pyqtSlot()
    def on_helpButton_clicked(self):
        """
        Slot documentation goes here.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Sie sehen diese Meldung da ein ungültiges Geschlecht in der Excel-Tabelle gefunden wurde. Das Geschlecht muss mit »M« oder »W« (für männlich/weiblich) in der Excel-Tabelle angegeben sein. Um die Korrektur möglichst schnell ausführen zu können wird nur das Wichtigste angezeigt: Oben mittig wird groß der Vor- und Nachname des Schülers angezeigt. Darunter steht in Klammern der ungültige Wert aus der Tabelle. Darunter befinden sich die Knöpfe um Männlich oder Weiblich für diesen Schüler auszuwählen (ein Klick auf diese bestätigt die Auswahl sofort) - die Auswahl kann auch über die Tastatur mit den Tasten »M« und »W« erfolgen! Wird der Knopf »Für Alle« aktiviert wird die Auswahl auf alle weiteren ungültigen Geschlechter übertragen. Der Knopf »Abbrechen« bricht die Erstellung der Datenbank komplett ab.")
        msg.setWindowTitle("FFSportfest - Hilfe")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
    
    @pyqtSlot()
    def on_femaleButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.selected = "W"
        self.accept()
    
    @pyqtSlot()
    def on_maleButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.selected = "M"
        self.accept()
        
    def getSelection(self):
        return self.selected

    def getForAll(self):
        return self.forAll

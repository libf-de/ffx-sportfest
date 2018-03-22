# -*- coding: utf-8 -*-

"""
Module implementing DatabaseEditor.
"""

from PyQt5.QtCore import pyqtSlot,  Qt,  QTimer
from PyQt5.QtWidgets import QMainWindow,  QFileDialog,  QProgressDialog,  QMessageBox,  QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QColor
import os,  json,  shutil,  uuid,  codecs, re
from lib.Constants import TableCols, TableParams
from lib.Delegates import GeschlechtDelegate,  KlasseDelegate,  ReadonlyDelegate
from lib.NameUtil import NameUtil
from ui.ExcelDialog import ExcelImporter
from ui.KlasseDeleteDialog import KlasseDeleteDialog

from .Ui_DatabaseForm import Ui_MainWindow


class DatabaseEditor(QMainWindow, Ui_MainWindow):
    
    cfg = None
    nu = None
    loadPD = None
    doubleEnter = False
    enterBox = None
    
    mDbPath = None
    
    parent = None
    
    hasChanged = False
    fileName = None
    
    JSN = {}
    
    klasseZeile = 0
    klasseText = ""
    
    T1V = True
    T2V = True
    T3V = True
    T4V = True
    TVR = 0
    
    sortingEnabled = True
    
    """
    Datenbankeditor
    Erstellt und bearbeitet Schülerdatenbanken
    
    TODO: Nach Schließen Datenbank wieder öffnen
    """
    def __init__(self, config, parent=None, opened=None):
        """
        Konstruktor
        """
        super(DatabaseEditor, self).__init__(parent)
        self.setupUi(self)
        
        self.cfg = config
        
        self.parent = parent
        
        self.nu = NameUtil()
        
        self.initTable()
        
        if not opened is None:
            self.fileName = str(opened)
            self.setWindowTitle("{} - Datenbankeditor - FFSportfest".format(str(os.path.basename(opened))))
            self.mDbPath = opened
            self.loadDb(opened)
    
    def mOpen(self, path):
        self.fileName = str(path)
        self.setWindowTitle("{} - Datenbankeditor - FFSportfest".format(str(os.path.basename(path))))
        self.mDbPath = path
        self.loadDb(path)
    
    def considerFeedback(self):
        if self.parent.dbPath is None and self.mDbPath is not None:
            self.parent.loadDb(self.mDbPath)
        
    def closeEvent(self,  event):
        """
        Wird aufgerufen wenn das Fenster geschlossen wird
        Wenn ungespeicherte Änderungen vorliegen wird Meldung angezeigt
        """
        if self.hasChanged:
            reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert. Möchten Sie die Änderungen speichern?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.on_actionSave_triggered()
                if self.hasChanged:
                    event.ignore()
                else:
                    self.considerFeedback()
                    event.accept()
            elif reply == QMessageBox.Discard:
                self.considerFeedback()
                event.accept()
            else:
                event.ignore()
        else:
            self.considerFeedback()
        
    def initTable(self):
        """
        Initialisiert die Tabelle (versteckt Spalten, setzt Überschriften, etc.)
        """
        tW = self.tableWidget
        tW.blockSignals(True)
        tW.setRowCount(0)
        tW.setColumnCount(20)
        tW.setSelectionMode(QAbstractItemView.SingleSelection)
                
        tW.setColumnHidden(TableCols.UID,  True)
        tW.setColumnHidden(TableCols.NAME,  False)
        tW.setColumnHidden(TableCols.VORNAME,  False)
        tW.setColumnHidden(TableCols.GESCHLECHT,  False)
        tW.setColumnHidden(TableCols.KLASSE,  False)
        tW.setColumnHidden(TableCols.SPRINT_V,  True)
        tW.setColumnHidden(TableCols.SPRINT_P,  True)
        tW.setColumnHidden(TableCols.SPRINT_N,  True)
        tW.setColumnHidden(TableCols.LAUF_V,  True)
        tW.setColumnHidden(TableCols.LAUF_P,  True)
        tW.setColumnHidden(TableCols.LAUF_N,  True)
        tW.setColumnHidden(TableCols.SPRUNG_V,  True)
        tW.setColumnHidden(TableCols.SPRUNG_P,  True)
        tW.setColumnHidden(TableCols.SPRUNG_N,  True)
        tW.setColumnHidden(TableCols.WURF_V,  True)
        tW.setColumnHidden(TableCols.WURF_P,  True)
        tW.setColumnHidden(TableCols.WURF_N,  True)
        tW.setColumnHidden(TableCols.PUNKTE,   True)
        tW.setColumnHidden(TableCols.NOTE,   True)
        tW.setColumnHidden(TableCols.KRANK,  False)
        
        tW.setItemDelegateForColumn(TableCols.GESCHLECHT, GeschlechtDelegate(self))
        tW.setItemDelegateForColumn(TableCols.KLASSE,  KlasseDelegate(self))
        tW.setItemDelegateForColumn(TableCols.KRANK,  ReadonlyDelegate(self))
        tW.setHorizontalHeaderLabels( TableParams.HEADER_LBL )
        tW.setIgnoredKeys([Qt.Key_Return,  Qt.Key_Enter,  Qt.Key_Tab,  Qt.Key_Backspace])
        tW.blockSignals(False)
    
    @pyqtSlot(int)
    def on_tableWidget_keyPressed(self, key):
        """
        Wird aufgerufen wenn Taste in Tabellenwidget gedrückt
        
        @param key Gedrückte Taste
        @type int
        """
        tw = self.tableWidget
        ccol = tw.currentColumn()
        crow = tw.currentRow()
        ccount = tw.columnCount()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.nextRow(crow,  ccol)
        elif key == Qt.Key_Tab:
            if ccount - 1 == ccol:
                return
            tw.setCurrentCell(crow, ccol+1)
        elif key == Qt.Key_Backspace:
            tw.setCurrentCell(crow, TableCols.NAME)
            print("BKSPACE");
        elif key == Qt.Key_Delete:
            self.removeCurrent(True)
        
    def getSUID(self):
        """
        Gibt einen Identifier (zufälliger String) für einen Schüler zurück
        """
        return str(uuid.uuid4().hex[:8])
        
    def removeCurrent(self,  showconfirm):
        """
        Entfernt den ausgewählten Schüler aus der Datenbank
        @param showconfirm Bestätigungsdialog anzeigen?
        """
        if len(self.tableWidget.selectedIndexes()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Es ist nichts ausgewählt! Bitte wählen Sie den Schüler aus, den Sie löschen wollen.")
            msg.setWindowTitle("FFSportfest")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        row = self.tableWidget.selectedItems()[0].row()
        SKlasse = self.tableWidget.item(row,  TableCols.KLASSE).text()
        
        if not (self.T1V and self.T2V and self.T3V and self.T4V):
            if not row == self.TVR:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese zunächst!")
                msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
                msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}".format(str(self.TVR + 1)))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            else:
                SKlasse = "working"
                showconfirm = False
                self.T1V = True
                self.T2V = True
                self.T3V = True
                self.T4V = True
                self.TVR = 0
        
        if showconfirm:
            SName = self.tableWidget.item(row,  TableCols.NAME).text()
            SVorname = self.tableWidget.item(row,  TableCols.VORNAME).text()
            reply = QMessageBox.question(self, 'FFSportfest', "Möchten Sie den/die Schüler/-in <b>{} {}</b> (Klasse {}) wirklich löschen?".format(SVorname,  SName, SKlasse), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if not reply == QMessageBox.Yes:
                return
                
        SUID = self.tableWidget.item(row,  TableCols.UID).text()
        self.tableWidget.removeRow(row)
        del self.JSN[SKlasse][SUID]
        if len(self.JSN[SKlasse]) == 0: #Klasse aus Datenbank löschen wenn keine weiteren Schüler enthalten sind
                    del self.JSN[SKlasse]
                    
        self.setChanged(True)
                    
    def getFilename(self):
        """
        Gibt den Dateinamen für die Titelleiste zurück (Unbenannt wenn neue Datenbank)
        """
        if self.fileName is None:
            return "Unbenannt"
        else:
            return os.path.basename(self.fileName)
        
    def setChanged(self, value):
        """
        Setzt ob die Datenbank verändert wurde
        @param value Verändert?
        """
        if not value == self.hasChanged:
            if value:
                self.setWindowTitle("{}* - Datenbankeditor - FFSportfest".format(self.getFilename()))
                self.hasChanged = True
            else:
                self.setWindowTitle("{} - Datenbankeditor - FFSportfest".format(self.getFilename()))
                self.hasChanged = False

    def moveKlassen(self):
        """
        Verschiebt die Klassen um eine Klassenstufe nach Oben
        """
        JSNC = self.JSN
        klist = list(JSNC.keys())
        klist.sort(key=float, reverse=True)
        
        print(klist)
        for k in JSNC.keys(): 
            if k.startswith("10"): 
                JSNC[k] = {}
                print("wipe {}".format(k))
                
        for src in klist:
            kls = src.split(".")
            tgt = str("{}.{}").format(str(int(kls[0]) + 1), str(kls[1]))
            
            if tgt in JSNC:
                #TODO: Target not empty!
                print("Target not empty!!!")
                return
            
            JSNC[tgt] = JSNC[src]
            del JSNC[src]
            
        self.JSN = JSNC
        self.fillTable()
        
        
    def addNew(self):
        """
        Fügt einen neuen Schüler hinzu
        """
        self.tableWidget.blockSignals(True)
        self.actionSort.setEnabled(False)
        self.sortingEnabled = False
        #self.tableWidget.setSortingEnabled(False)
        sc = self.tableWidget.rowCount()
        print("AddNew: rowCount is {}".format(str(sc)))
        SUID = self.getSUID()
        if not "working" in self.JSN:
            self.JSN["working"] = {}
    
        if not SUID in self.JSN["working"]:
            self.JSN["working"][SUID] = {}
        
        self.JSN["working"][SUID]['name'] = ""
        self.JSN["working"][SUID]['vorname'] = ""
        self.JSN["working"][SUID]['geschlecht'] = ""
        self.JSN["working"][SUID]['sprint_v'] = 0.0
        self.JSN["working"][SUID]['sprint_p'] = 0
        self.JSN["working"][SUID]['sprint_n'] = 6
        self.JSN["working"][SUID]['lauf_v'] = 0
        self.JSN["working"][SUID]['lauf_p'] = 0
        self.JSN["working"][SUID]['lauf_n'] = 6
        self.JSN["working"][SUID]['sprung_v'] = 0.0
        self.JSN["working"][SUID]['sprung_p'] = 0
        self.JSN["working"][SUID]['sprung_n'] = 6
        self.JSN["working"][SUID]['wurf_v'] = 0.0
        self.JSN["working"][SUID]['wurf_p'] = 0
        self.JSN["working"][SUID]['wurf_n'] = 6
        self.JSN["working"][SUID]['punkte'] = 0
        self.JSN["working"][SUID]['note'] = 6
        self.JSN["working"][SUID]['krank'] = False
        self.tableWidget.setRowCount(sc + 1)
        self.tableWidget.setItem(sc,TableCols.UID, QTableWidgetItem(SUID))
        self.tableWidget.setItem(sc,TableCols.NAME, QTableWidgetItem(""))
        self.tableWidget.setItem(sc,TableCols.VORNAME, QTableWidgetItem(""))
        self.tableWidget.setItem(sc,TableCols.GESCHLECHT, QTableWidgetItem(""))
        self.tableWidget.setItem(sc,TableCols.KLASSE, QTableWidgetItem(""))
        self.tableWidget.setItem(sc,TableCols.SPRINT_V, QTableWidgetItem("0.0"))
        self.tableWidget.setItem(sc,TableCols.SPRINT_P, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.SPRINT_N, QTableWidgetItem("6"))
        self.tableWidget.setItem(sc,TableCols.LAUF_V, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.LAUF_P, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.LAUF_N, QTableWidgetItem("6"))
        self.tableWidget.setItem(sc,TableCols.SPRUNG_V, QTableWidgetItem("0.0"))
        self.tableWidget.setItem(sc,TableCols.SPRUNG_P, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.SPRUNG_N, QTableWidgetItem("6"))
        self.tableWidget.setItem(sc,TableCols.WURF_V, QTableWidgetItem("0.0"))
        self.tableWidget.setItem(sc,TableCols.WURF_P, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.WURF_N, QTableWidgetItem("6"))
        self.tableWidget.setItem(sc,TableCols.PUNKTE, QTableWidgetItem("0"))
        self.tableWidget.setItem(sc,TableCols.NOTE, QTableWidgetItem("6"))
        #krankbox = QTableWidgetItem("Krank")
        #krankbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        #krankbox.setCheckState(self.checkedBool(False))
        #self.tableWidget.setItem(sc, TableCols.KRANK,  krankbox)
        self.tableWidget.setItem(sc,TableCols.KRANK, QTableWidgetItem(str(self.getKrank(False)))) #TODO: getKrank
        self.T1V = False
        self.T2V = False
        self.T3V = False
        self.T4V = False
        self.TVR = sc
        for i in range(self.tableWidget.columnCount()):
            try:
                itm = self.tableWidget.item(sc, i)
                itm.setBackground(QColor(255, 0, 0))
            except Exception:
                print("Error")
        self.tableWidget.setCurrentCell(sc, TableCols.NAME)
        self.tableWidget.blockSignals(False)
        self.setChanged(True)
        
    def istKrank(self, text):
        """
        Gibt zurück ob der Schüler krank ist (Checkbox-Ersatz)
        @param text Text
        """
        if text.startswith("☒"):
            return True
        else:
            return False
            
    def getKrank(self, bval):
        """
        Gibt den Checkbox-Ersatz zurück
        @param bval Krank oder nicht
        """
        if bval:
            return "☒ Krank"
        else:
            return "☑ Anwesend"
        
    def nextRow(self,  crow,  ccol):
        """
        Geht zur nächsten Zeile und erstellt sie ggf.
        """
        print("RC: " + str(self.tableWidget.rowCount()) + ", CR: " + str(crow))
        if self.tableWidget.rowCount() - 1 == crow:
            if self.doubleEnter:
                if self.T1V and self.T2V and self.T3V and self.T4V:
                    self.resetDoubleEnter()
                    self.addNew()
                else:
                    self.resetDoubleEnter()
                    self.statusBar.showMessage("Bitte zuletzt hinzugefügten Schüler erst vervollständigen!",  2000) 
            else:
                self.doubleEnter = True
                self.statusBar.showMessage("Erneut ENTER drücken um neuen Schüler hinzuzufügen...",  2000) 
                timer = QTimer()
                timer.timeout.connect(self.resetDoubleEnter)
                timer.start(2000)
        else:
            #if self.tableWidget.item(crow+1,  TableCols.KRANK).checkState() == Qt.Checked:
            if self.istKrank(self.tableWidget.item(crow+1,  TableCols.KRANK).text()):
                self.gotoNextHealthyCell(crow+1,  ccol)
            else:
                self.tableWidget.setCurrentCell(crow+1, ccol)
            
    def resetDoubleEnter(self):
        """
        Setzt "2x Enter für neuen Schüler" zurück
        """
        self.doubleEnter = False
    
    @pyqtSlot()
    def on_actionAdd_triggered(self):
        """
        Button "Schüler hinzufügen"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            self.addNew()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese zunächst!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    
    @pyqtSlot()
    def on_actionRemove_triggered(self):
        """
        Button "Schüler entfernen"
        """
        self.removeCurrent(True)
    
    @pyqtSlot()
    def on_actionMoveKlasse_triggered(self):
        """
        Button "Klasse verschieben"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            reply = QMessageBox.question(self, 'FFSportfest', "Möchten Sie die Klassen wirklich verschieben? Dies verschiebt alle Schüler um eine Klassenstufe (5.→6., 6.→7.) <b>und löscht alle Schüler der jetzigen 10. Klasse</b>.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if not reply == QMessageBox.Yes:
                return
            self.moveKlassen()
            
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese zunächst!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    
    @pyqtSlot()
    def on_actionNeue_Datenbank_triggered(self):
        """
        Button "Neue Datenbank erstellen"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            if self.hasChanged:
                reply = QMessageBox.question(self, 'FFSportfest', "Die Datenbank wurde geändert. Möchten Sie die Datenbank speichern?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.on_actionSave_triggered()
                    if self.hasChanged:
                        return
                elif reply == QMessageBox.Cancel:
                    return
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese, bevor Sie die Datenbank speichern!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}\nDatenbanken mit unvollständig ausgefüllten Schülern können nicht gespeichert werden!".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
            
        self.JSN = {}
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0);
        self.tableWidget.setRowCount(0)
        self.fileName = None
        self.T1V = True
        self.T2V = True
        self.T3V = True
        self.T4V = True
        self.TVR = 0
        self.hasChanged = False
        self.setChanged(True)
        self.addNew()
        self.mDbPath = None
        self.setUserInput(True)
        self.tableWidget.setFocus()
        
    
    @pyqtSlot()
    def on_actionSave_triggered(self):
        """
        Button "Speichern"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            if not self.fileName is None:
                try:
                    with open(self.fileName, 'w',  encoding='utf8') as f:
                        json.dump(self.JSN, f, indent=4, sort_keys=True, ensure_ascii=False)
                        self.setChanged(False)
                except PermissionError as per:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diese Datei besitzen. Sie können entweder die Datei unter einem anderen Namen speichern (Datei - Speichern unter…) oder Schreibrechte für die Datei erlangen.")
                    msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                    msg.setDetailedText("Dateipfad: " + str(self.fileName) + "\n" + str(per))
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
            else:
                self.on_actionSaveAs_triggered()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese, bevor Sie die Datenbank speichern!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}\nDatenbanken mit unvollständig ausgefüllten Schülern können nicht gespeichert werden!".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    
    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        """
        Button "Speichern unter"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            opts = QFileDialog.Options()
            name, _ = QFileDialog.getSaveFileName(self, "Datenbank speichern unter", os.path.expanduser("~"), "FFD-Datenbank (*.ffd)",  options=opts)
            if name:
                filename = str(name)
                if not filename.endswith(".ffd"):
                    filename+= ".ffd"
                print("FN: " + filename)
                try:
                    with open(filename, 'w',  encoding='utf8') as f:
                        json.dump(self.JSN, f, indent=4, sort_keys=True, ensure_ascii=False)
                    self.fileName = filename
                    self.setChanged(False)
                except PermissionError as per:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diese Datei besitzen. Sie können entweder die Datei unter einem anderen Namen speichern (Datei - Speichern unter…) oder Schreibrechte für die Datei erlangen.")
                    msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                    msg.setDetailedText("Dateipfad: " + str(filename) + "\n" + str(per))
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese, bevor Sie die Datenbank speichern!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}\nDatenbanken mit unvollständig ausgefüllten Schülern können nicht gespeichert werden!".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        
    
    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Button "Öffnen"
        """
        self.statusBar.showMessage("Öffne Datenbank...") 
        opts = QFileDialog.Options()
        db_file,  _ = QFileDialog.getOpenFileName(self, "Datenbank öffnen", os.path.expanduser("~"), "FFD-Datenbank (*.ffd);;Sicherungsdateien (*.ffd~);;Alle Dateien (*.*)",  options=opts);

        if db_file:
            self.fileName = str(db_file)
            self.setWindowTitle("{} - Datenbankeditor - FFSportfest".format(str(os.path.basename(db_file))))
            self.mDbPath = str(db_file)
            self.loadDb(db_file)
    
    @pyqtSlot()
    def on_actionFromExcel_triggered(self):
        """
        Button "Von Excel importieren"
        """
        if self.T1V and self.T2V and self.T3V and self.T4V:
            if self.hasChanged:
                reply = QMessageBox.question(self, 'FFSportfest', "Die Datenbank wurde geändert. Möchten Sie die Datenbank speichern?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.on_actionSave_triggered()
                    if self.hasChanged:
                        return
                elif reply == QMessageBox.Cancel:
                    return
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Datenbank enthält unvollständig ausgefüllte Schüler. Bitte vervollständigen Sie diese, bevor Sie die Datenbank speichern!")
            msg.setWindowTitle("FFSportfest - Unvollständige Schüler")
            msg.setDetailedText("Unvollständig ausgefüllter Schüler auf Zeile: {}\nDatenbanken mit unvollständig ausgefüllten Schülern können nicht gespeichert werden!".format(str(self.TVR + 1)))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
            
        impt = ExcelImporter()
        impt.exec_()
        if not impt.getReturnDb() is None:
            self.fileName = str(impt.getReturnDb())
            self.mDbPath = str(impt.getReturnDb())
            self.loadDb(impt.getReturnDb())
            self.hasChanged = True
            self.setChanged(False)
    
    @pyqtSlot()
    def on_actionClose_triggered(self):
        """
        Button "Schließen"
        """
        if self.hasChanged:
            reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert. Möchten Sie die Änderungen speichern?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.on_actionSave_triggered()
                if not self.hasChanged:
                    self.considerFeedback()
                    self.close()
            elif reply == QMessageBox.Discard:
                self.considerFeedback()
                self.close()
        else:
            self.considerFeedback()
            self.close()
        
    def setUserInput(self, enable):
        """
        De-/Aktiviert die Eingabe
        @param enable Aktiv?
        """
        self.tableWidget.setEnabled(enable)
        self.actionAdd.setEnabled(enable)
        self.actionRemove.setEnabled(enable)
        self.actionMoveKlasse.setEnabled(enable)
        self.actionSave.setEnabled(enable)
        self.actionSaveAs.setEnabled(enable)
        self.actionDeleteKlasse.setEnabled(enable)
        
    def loadDb(self,  path):
        """
        Lädt eine Datenbank
        """
        self.loadPD = QProgressDialog()
        self.loadPD.setWindowTitle("Lade Datenbank...")
        self.loadPD.setLabelText("Lade Datenbank, bitte warten!")
        self.loadPD.setCancelButton(None)
        self.loadPD.setRange(0,  5)
        self.loadPD.show()
        self.loadPD.setValue(1)
        if not os.path.isfile(path):
            return False
        self.dbPath = path
        try:
            self.loadPD.setValue(2)
            #self.JSN = json.load(open(str(path)))
            self.JSN = json.load(codecs.open(str(path), 'r', 'utf-8-sig'))
            self.loadPD.setValue(3)
            self.fillTable()
            self.loadPD.setValue(4)
            self.setUserInput(True)
        except PermissionError as per:
            self.loadPD.cancel()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Die Datenbank konnte nicht geladen werden, da Sie keine Leserechte für diese Datei besitzen. Sie müssen Leserechte für diese Datei erlangen um sie zu öffnen.")
            msg.setWindowTitle("FFSportfest - Fehler beim Laden")
            msg.setDetailedText("Dateipfad: " + str(self.dbPath) + "\n\n" + str(per))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except json.decoder.JSONDecodeError as exc:
            self.loadPD.cancel()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Die Datenbank konnte nicht geladen werden! Sie ist möglicherweise beschädigt.")
            msg.setInformativeText("Sie können versuchen, falls aktiviert und vorhanden, die zugehörige Sicherungsdatei (Dateiname.ffd~) zu öffnen oder die Datenbank per Hand mit einem Texteditor zu reparieren. Klicken Sie auf Details anzeigen um zu sehen wo und welcher Fehler aufgetreten ist.")
            msg.setWindowTitle("FFSportfest - Fehler beim Öffnen")
            msg.setDetailedText(str(exc))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        if self.cfg.getBackupFile():
            try:
                shutil.copy2(str(path), str(path) + "~") 
            except PermissionError as perb:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Es konnte keine Sicherungsdatei erstellt werden, da Sie nicht die nötigen Berechtigungen für den Ordner besitzen. Die Datenbank sollte aber trotzdem problemlos geladen worden sein.")
                msg.setWindowTitle("FFSportfest - Warnung")
                msg.setDetailedText("Quellpfad: " + str(path) + "\n\n" + str(perb))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        self.loadPD.setValue(5)
        self.loadPD.cancel()
        self.statusBar.showMessage("Datenbank geladen!")
        
    def validKlasse(self, input):
        try:
            float(input)
        except Exception:
            return False
        return True
        
    def fillTable(self):
        """
        Füllt die Tabelle mit den JSON-Daten
        """
        self.tableWidget.blockSignals(True)
        self.actionSort.setEnabled(False)
        self.sortingEnabled = False
        #self.tableWidget.setSortingEnabled(False)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0);
            #uiditem.setFlags(uiditem.flags() ^ Qt.ItemIsEnabled)
        self.tableWidget.setRowCount(0)
        sc = 0
        for klasse,  schueler in self.JSN.items():
            for uid, det in schueler.items():
                try:
                    self.verifyJSON(det)
                except Exception as expt:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Die Datenbank konnte nicht überprüft werden - Laden abgebrochen! Die Datenbank ist wahrscheinlich beschädigt.")
                    msg.setWindowTitle("FFSportfest - Fehler")
                    msg.setDetailedText("Fehlernachricht:" + str(expt.message))
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                iskrank = det['krank']
                self.tableWidget.setItem(sc,TableCols.UID, QTableWidgetItem(uid))
                self.tableWidget.setItem(sc,TableCols.NAME, QTableWidgetItem(det['name']))
                self.tableWidget.setItem(sc,TableCols.VORNAME, QTableWidgetItem(det['vorname']))
                self.tableWidget.setItem(sc,TableCols.GESCHLECHT, QTableWidgetItem(det['geschlecht']))
                self.tableWidget.setItem(sc,TableCols.KLASSE, QTableWidgetItem(klasse))
                if not self.validKlasse(klasse):
                    itm = self.tableWidget.item(sc, TableCols.KLASSE)
                    itm.setBackground(QColor(244, 170, 66))
                self.tableWidget.setItem(sc,TableCols.SPRINT_V, QTableWidgetItem(str(det['sprint_v'])))
                self.tableWidget.setItem(sc,TableCols.SPRINT_P, QTableWidgetItem(str(det['sprint_p'])))
                self.tableWidget.setItem(sc,TableCols.SPRINT_N, QTableWidgetItem(str(det['sprint_n'])))
                self.tableWidget.setItem(sc,TableCols.LAUF_V, QTableWidgetItem(int(det['lauf_v'])))
                self.tableWidget.setItem(sc,TableCols.LAUF_P, QTableWidgetItem(str(det['lauf_p'])))
                self.tableWidget.setItem(sc,TableCols.LAUF_N, QTableWidgetItem(str(det['lauf_n'])))
                self.tableWidget.setItem(sc,TableCols.SPRUNG_V, QTableWidgetItem(str(det['sprung_v'])))
                self.tableWidget.setItem(sc,TableCols.SPRUNG_P, QTableWidgetItem(str(det['sprung_p'])))
                self.tableWidget.setItem(sc,TableCols.SPRUNG_N, QTableWidgetItem(str(det['sprung_n'])))
                self.tableWidget.setItem(sc,TableCols.WURF_V, QTableWidgetItem(str(det['wurf_v'])))
                self.tableWidget.setItem(sc,TableCols.WURF_P, QTableWidgetItem(str(det['wurf_p'])))
                self.tableWidget.setItem(sc,TableCols.WURF_N, QTableWidgetItem(str(det['wurf_n'])))
                self.tableWidget.setItem(sc,TableCols.PUNKTE, QTableWidgetItem(str(det['punkte'])))
                if 'note' in det:
                    self.tableWidget.setItem(sc,TableCols.NOTE, QTableWidgetItem(str(det['note'])))
                #krankbox = QTableWidgetItem("Krank")
                #krankbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                #krankbox.setCheckState(self.checkedBool(iskrank))
                #self.tableWidget.setItem(sc, TableCols.KRANK,  krankbox)
                self.tableWidget.setItem(sc,TableCols.KRANK, QTableWidgetItem(str(self.getKrank(iskrank))))
                sc += 1
        #self.tableWidget.setSortingEnabled(True)
        self.sortingEnabled = True
        self.actionSort.setEnabled(True)
        self.cfg.doSortBy(self.tableWidget)
        self.tableWidget.blockSignals(False) 
        
    def verifyJSON(self,  det):
        """
        Überprüft ob Schüler alle nötigen Daten enthält und ergänzt sie ggf.
        """
        if not 'name' in det:
            det['name'] = "Mustermann"
        if not 'vorname' in det:
            det['vorname'] = "Max"
        if not 'geschlecht' in det:
            det['geschlecht'] = "M"
        if not det['geschlecht'].lower() in ("m",  "w"):
            det['geschlecht'] = "W"
            print('WARNUNG: Ungueltiges Geschlecht bei ' + det['vorname'] + " " + det['name'] + "!") #TODO
        if not 'sprint_v' in det:
            det['sprint_v'] = 0.0
        if not 'sprint_p' in det:
            det['sprint_p'] = 0
        if not 'sprint_n' in det:
            det['sprint_n'] =  6
        if not 'lauf_v' in det:
            det['lauf_v'] = 0.0
        if not 'lauf_p' in det:
            det['lauf_p'] = 0
        if not 'lauf_n' in det:
            det['lauf_n'] =  6
        if not 'sprung_v' in det:
            det['sprung_v'] = 0.0
        if not 'sprung_p' in det:
            det['sprung_p'] = 0
        if not 'sprung_n' in det:
            det['sprung_n'] =  6
        if not 'wurf_v' in det:
            det['wurf_v'] = 0.0
        if not 'wurf_p' in det:
            det['wurf_p'] = 0
        if not 'wurf_n' in det:
            det['wurf_n'] =  6
        if not 'punkte' in det:
            det['punkte'] = 0
        if not 'note' in det:
            det['note'] = 6
        if not 'krank' in det:
            det['krank'] = False
            
    def checkedBool(self,  input):
        """
        Boolean -> Qt.Checked
        """
        if input:
            return Qt.Checked
        else:
            return Qt.Unchecked
            
    def boolChecked(self,  input):
        """
        Qt.Checked -> Boolean
        """
        if input == Qt.Checked:
            return True
        else:
            return False
            
    def getCurrentRowKlasse(self, row):
        """
        Gibt die Klasse der ausgewählten Zeile zurück
        """
        klasse = self.tableWidget.item(row,  TableCols.KLASSE).text()
        if klasse == "":
            return "working"
        else:
            return klasse
    
    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemChanged(self, item):
        """
        Daten in der Tabelle bearbeitet
        
        @param item Geänderte Zelle
        @type QTableWidgetItem
        """
        self.setChanged(True)
        UID = self.tableWidget.item(item.row(),  TableCols.UID).text()
        print("EDITOR: ITEMCHANGED")
        if item.column() == TableCols.KLASSE:
            print("EDITOR: ITEMCHANGED: KLASSE")
            print("EDITOR: KZ: {} IR: {}".format(str(self.klasseZeile), str(item.row())))
            if self.klasseZeile == item.row():
                print("EDITOR: ITEMCHANGED: ZEILE")
                if self.klasseText == "":
                    self.klasseText = "working"
                    
                if not item.text() in self.JSN:
                    self.JSN[item.text()] = {}
                self.JSN[item.text()][UID] = self.JSN[self.klasseText][UID]
                del self.JSN[self.klasseText][UID]
                if len(self.JSN[self.klasseText]) == 0:
                    print("Entferne Klasse " + self.klasseText)
                    del self.JSN[self.klasseText]
            print("IR: " + str(item.row()) + " TVR: " + str(self.TVR))
            if item.row() == self.TVR:
                self.T4V = True
                print("V4 GOOD")
        elif item.column() == TableCols.NAME:
            self.JSN[self.getCurrentRowKlasse(item.row())][UID]['name'] = item.text().title()
            if item.row() == self.TVR:
                self.T1V = True
                print("V1 GOOD")
        elif item.column() == TableCols.VORNAME:
            self.JSN[self.getCurrentRowKlasse(item.row())][UID]['vorname'] = item.text().title()
            if self.cfg.getGuessGender():
                guessed = NameUtil().rateGeschlecht(item.text())
                if not guessed is None:
                    self.JSN[self.getCurrentRowKlasse(item.row())][UID]['geschlecht'] = guessed
                    self.tableWidget.item(item.row(),  TableCols.GESCHLECHT).setText(guessed)
            if item.row() == self.TVR:
                self.T2V = True
                print("V2 GOOD")
        elif item.column() == TableCols.GESCHLECHT:
            self.JSN[self.getCurrentRowKlasse(item.row())][UID]['geschlecht'] = item.text().upper()
            if item.row() == self.TVR:
                self.T3V = True
                print("V3 GOOD")
        elif item.column() == TableCols.KRANK:
            #self.JSN[self.getCurrentRowKlasse(item.row())][UID]['krank'] = self.boolChecked(item.checkState())
            self.JSN[self.getCurrentRowKlasse(item.row())][UID]['krank'] = self.istKrank(item.text())
            
        if item.row() == self.TVR:
            if self.T1V and self.T2V and self.T3V and self.T4V:
                print("ALL GOOD")
                self.tableWidget.blockSignals(True)
                for i in range(self.tableWidget.columnCount()):
                    try:
                        itm = self.tableWidget.item(item.row(), i)
                        itm.setBackground(QColor(255, 255, 255))
                    except Exception:
                        print("Error")
                self.tableWidget.blockSignals(False)
                self.actionSort.setEnabled(True)
                self.sortingEnabled = True
                #self.tableWidget.setSortingEnabled(True)
                
        
        print("changed")
        if not self.cfg is None:
            #if self.cfg.getInstantSort() and self.tableWidget.isSortingEnabled():
            if self.cfg.getInstantSort() and self.sortingEnabled:
                print("SORITNG!!!")
                self.cfg.doSortBy(self.tableWidget)
    
    @pyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def on_tableWidget_currentItemChanged(self, current, previous):
        """
        Ausgewählte Zelle geändert
        
        @param current neue Zelle
        @type QTableWidgetItem
        @param previous vorherige Zelle
        @type QTableWidgetItem
        """
        # TODO: Wertzuweisung wenn nichts ausgewählt #← But why wenn dieses Event auftritt sollte immer etwas ausgewählt sein???
        if not len(self.tableWidget.selectedIndexes()) == 0 and current is not None: #← Was hab ich da getan?
            if current.column() == TableCols.KLASSE:
                print("Klasse gemerkt")
                self.klasseZeile = current.row()
                self.klasseText = current.text()
    
    @pyqtSlot()
    def on_actionSort_triggered(self):
        """
        Erzwingt eine Neusortierung der Schüler
        """
        self.cfg.doSortBy(self.tableWidget)
    
    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemClicked(self, item):
        """
        Wird aufgerufen wenn Item in Tabelle angeklickt wurde (für Krank-Toggle)
        """
        if item.column() == TableCols.KRANK:
            krank = not self.istKrank(item.text())
            #if self.boolChecked(item.checkState()):
            item.setText(self.getKrank(krank))
            #self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['krank'] = krank
            self.JSN[self.getCurrentRowKlasse(item.row())][self.tableWidget.item(item.row(), TableCols.UID).text()]['krank'] = self.istKrank(item.text())
    
    @pyqtSlot()
    def on_actionDeleteKlasse_triggered(self):
        """
        Entfernt eine Klasse
        """
        #TODO: Alle Klassen und Klassenstufen abrufen
        rx = re.compile(r'^([0-9]{1,2})\.([0-9]{1})$')
        klassen = [i for i in sorted(self.JSN.keys()) if rx.search(i)]
        klassenstufen = [ ]
        for klasse in klassen:
            klassenstufen.append(re.findall("^[^\d]*(\d+)", klasse)[0])
        klassen.extend(set(klassenstufen))
        klassen.sort()
        print(klassen)
        #regex = re.compile(r'^([0-9]{1,2})$')
        exp = KlasseDeleteDialog(klassen,  self)
        exp.exec_()
        res = exp.getKlasse()
        if res is not None:
            if re.match("^([0-9]{1,2})\.([0-9]{1})$",  res):
                del self.JSN[res]
            else:
                for kst in [ v for v in self.JSN.keys() if v.startswith(res)]:
                    del self.JSN[kst]
        self.setChanged(True)
        self.fillTable()
        #del self.JSN[SKlasse][SUID]
        #QMessageBox.warning(self, "FFSportfest", "Diese Funktion wurde noch nicht implementiert!", QMessageBox.Ok, QMessageBox.Ok)


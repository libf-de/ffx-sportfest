# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os,  json, re,  shutil
from PyQt5.QtCore import pyqtSlot,  Qt,  QRegExp
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QFileDialog, QMessageBox, QProgressDialog, QHeaderView, QAction
from PyQt5.QtGui import QColor,  QDoubleValidator,  QRegExpValidator,  QPageLayout, QTextDocument, QTextCursor, QTextTableFormat,  QTextFrameFormat, QFont, QTextBlockFormat
from PyQt5.QtPrintSupport import QPrintPreviewDialog
from lib.Delegates import NumDelegate,  ReadonlyDelegate,  TimeDelegate
from lib.Constants import TableCols,  TableHide,  TableParams,  FFSportfest
from lib.CalcPoints import CalcPoints
from lib.CalcNote import CalcNote
from Configuration import Configuration
from ui.EvaluateForm import EvalWindow
from ui.SettingsDialog import SettingsDialog
from ui.SettingsPortable import SettingsPortableDialog
from ui.DatabaseForm import DatabaseEditor
from ui.ExportDialog import ExportDialog

from .Ui_MainForm import Ui_MainWindow

from jsonmerge import merge

from pprint import pprint

import codecs


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    TODO: Format der Klasse beim öffnen überprüfen
    """
    
    JSD = {};
    prevRow = -1;
    pCalc = None
    nCalc = None
    dbPath = None
    pCfg = None
    loadLastDb = False
    doRec = False
    dataChanged = False
    ignNonPart = True
    healthyRows = 0
    EvalW = None
    dbf = None
    RemoteEdit = False
    
    ConfirmDelete = False
    
    alleKlassen = []
    
    loadPD = None
    
    splash = None
    
    args = None

    def __init__(self, args=None,  splash=None, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        uExecPath = None
        if not args is None:
            uExecPath = args.uexecpath
            
        self.pCfg = Configuration(uExecPath)
        self.loadLastDb = self.pCfg.getLoadLastDb()
        self.doRec = self.pCfg.getRecovery()
        
        self.EvalW = EvalWindow(self.pCfg, self)
        self.dbf = DatabaseEditor(self.pCfg, self, self.dbPath)
        
        self.disableUserInput()
        
        dblV = QDoubleValidator()
        self.sprintSecEdit.setValidator(dblV)
        self.sprungMeterEdit.setValidator(dblV)
        self.wurfMeterEdit.setValidator(dblV)
        
        rgx = QRegExp('^([0-9]|[0-5][0-9]):[0-5][0-9]$')
        rgxV = QRegExpValidator(rgx)
        self.LaufSecEdit.setValidator(rgxV)

        tW = self.tableWidget
        tW.blockSignals(True)
        tW.setRowCount(0)
        tW.setColumnCount(20)
        tW.setSelectionMode(QAbstractItemView.SingleSelection)
        hdr = self.tableWidget.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeToContents)
        hdr.setMinimumSectionSize(50)
        hdr.setSectionResizeMode(TableCols.NAME, QHeaderView.Interactive)
        hdr.setSectionResizeMode(TableCols.VORNAME, QHeaderView.Interactive)
                
        tW.setColumnHidden(TableCols.UID,  TableHide.UID)
        tW.setColumnHidden(TableCols.NAME,  TableHide.NAME)
        tW.setColumnHidden(TableCols.VORNAME,  TableHide.VORNAME)
        tW.setColumnHidden(TableCols.GESCHLECHT,  TableHide.GESCHLECHT)
        tW.setColumnHidden(TableCols.KLASSE,  TableHide.KLASSE)
        tW.setColumnHidden(TableCols.SPRINT_V,  TableHide.SPRINT_V)
        tW.setColumnHidden(TableCols.SPRINT_P,  TableHide.SPRINT_P)
        tW.setColumnHidden(TableCols.SPRINT_N,  TableHide.SPRINT_N)
        tW.setColumnHidden(TableCols.LAUF_V,  TableHide.LAUF_V)
        tW.setColumnHidden(TableCols.LAUF_P,  TableHide.LAUF_P)
        tW.setColumnHidden(TableCols.LAUF_N,  TableHide.LAUF_N)
        tW.setColumnHidden(TableCols.SPRUNG_V,  TableHide.SPRUNG_V)
        tW.setColumnHidden(TableCols.SPRUNG_P,  TableHide.SPRUNG_P)
        tW.setColumnHidden(TableCols.SPRUNG_N,  TableHide.SPRUNG_N)
        tW.setColumnHidden(TableCols.WURF_V,  TableHide.WURF_V)
        tW.setColumnHidden(TableCols.WURF_P,  TableHide.WURF_P)
        tW.setColumnHidden(TableCols.WURF_N,  TableHide.WURF_N)
        tW.setColumnHidden(TableCols.PUNKTE,   TableHide.PUNKTE)
        tW.setColumnHidden(TableCols.NOTE,   TableHide.NOTE)
        tW.setColumnHidden(TableCols.KRANK,  TableHide.KRANK)
        
        tW.setItemDelegateForColumn(TableCols.SPRINT_V,  NumDelegate(self))
        tW.setItemDelegateForColumn(TableCols.LAUF_V,  TimeDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRUNG_V,  NumDelegate(self))
        tW.setItemDelegateForColumn(TableCols.WURF_V,  NumDelegate(self))
        tW.setItemDelegateForColumn(TableCols.UID,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.NAME,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.VORNAME,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.GESCHLECHT,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.KLASSE,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRINT_P,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRINT_N,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.LAUF_P,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.LAUF_N,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRUNG_P,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRUNG_N,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.WURF_P,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.WURF_N,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.PUNKTE,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.NOTE,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.KRANK,  ReadonlyDelegate(self))
        
        tW.setHorizontalHeaderLabels( TableParams.HEADER_LBL )
        
        tW.setIgnoredKeys([Qt.Key_Return,  Qt.Key_Enter,  Qt.Key_Tab,  Qt.Key_Backspace,  Qt.Key_Space, Qt.Key_Delete])
        
        tW.blockSignals(False)
        
        klasseCb = self.klasseCombo
        klasseCb.blockSignals(True)
        klasseCb.addItem("Alle")
        klasseCb.blockSignals(False)
        
        gCb = self.geschlechtCombo
        gCb.blockSignals(True)
        gCb.addItem("Alle")
        gCb.addItem("Jungen")
        gCb.addItem("Mädchen")
        gCb.blockSignals(False)
        
        self.pCalc = CalcPoints()
        self.nCalc = CalcNote()
        
        self.setRemoteUI(False)
        if self.doRec and os.path.isfile(self.pCfg.getRecoverFile()):
            reply = QMessageBox.question(self, 'FFSportfest', 'Es wurde eine Absturzsicherung gefunden - wahrscheinlich ist das Programm abgestürzt. Möchten Sie die Daten laden? Wenn nicht werden die Daten gelöscht - eine Wiederherstellung ist dann nicht mehr möglich!', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.loadRecovery()
            else:
                self.clearRecovery()
                
        if not args.filename is None and os.path.isfile(args.filename): #TODO: Relativer Pfad?
            if str(args.filename).endswith(".fmd"):
                self.setRemoteUI(True)
                self.loadDb(args.filename)
            else:
                self.loadDb(args.filename)
        else:
            packDb = self.pCfg.considerLoadDb()
            if packDb:
                self.loadDb(packDb)
            else:
                if self.loadLastDb:
                    print("Loading last db...")
                    self.loadDb(self.pCfg.getLastDb())
        
        if not splash is None:
            splash.finish(self)
            
        #self.setRemoteUI(True)
    
    def setSplash(self,  splash):
        self.splash = splash
        
    def resizeTable(self):
        hdr = self.tableWidget.horizontalHeader()
        hdr.resizeSection(TableCols.NAME, hdr.sectionSize(TableCols.NAME) + 20)
        hdr.resizeSection(TableCols.VORNAME, hdr.sectionSize(TableCols.VORNAME) + 20)
    
    def setRemoteUI(self,  value):
        self.RemoteEdit = value
        if value:
            self.menuDatei.menuAction().setVisible(False)
            self.actionDatenbank_bearbeiten_2.setEnabled(False)
            self.actionDatenbank_laden.setEnabled(False)
            self.actionDatenbank_speichern.setEnabled(False)
            self.actionDatenbank_speichern_unter.setEnabled(False)
            self.actionEinstellungen.setEnabled(False)
            self.actionEinstellungenPortable.setEnabled(True)
            self.actionEinstellungenPortable.setMenuRole(QAction.PreferencesRole)
            self.actionSpeichernPortable.setEnabled(True)
            self.actionBeendenPortable.setEnabled(True)
            self.actionBeendenPortable.setMenuRole(QAction.QuitRole)
            self.actionBeenden.setEnabled(False)
            self.menuPortableDatei.menuAction().setVisible(True)
            self.menuZusammenarbeit.menuAction().setVisible(False)
            self.actionExport.setEnabled(False)
            self.actionImport.setEnabled(False)
        else:
            self.menuDatei.menuAction().setVisible(True)
            self.actionDatenbank_bearbeiten_2.setEnabled(True)
            self.actionDatenbank_laden.setEnabled(True)
            self.actionDatenbank_speichern.setEnabled(True)
            self.actionDatenbank_speichern_unter.setEnabled(True)
            self.actionEinstellungen.setEnabled(True)
            self.actionEinstellungen.setMenuRole(QAction.PreferencesRole)
            self.actionEinstellungenPortable.setEnabled(False)
            self.actionSpeichernPortable.setEnabled(False)
            self.actionBeendenPortable.setEnabled(False)
            self.actionBeenden.setEnabled(True)
            self.actionBeenden.setMenuRole(QAction.QuitRole)
            self.menuPortableDatei.menuAction().setVisible(False)
            self.menuZusammenarbeit.menuAction().setVisible(True)
            self.actionExport.setEnabled(True)
            self.actionImport.setEnabled(True)
    
    def disableUserInput(self):
        self.tableWidget.setEnabled(False)
        self.klasseCombo.setEnabled(False)
        self.geschlechtCombo.setEnabled(False)
        self.sprintSecEdit.setEnabled(False)
        self.LaufSecEdit.setEnabled(False)
        self.sprungMeterEdit.setEnabled(False)
        self.wurfMeterEdit.setEnabled(False)
        self.klasseEdit.setEnabled(False)
        self.nameEdit.setEnabled(False)
        self.vornameEdit.setEnabled(False)
        self.geschlechtEdit.setEnabled(False)
        self.sprintPunkteEdit.setEnabled(False)
        self.LaufPunkteEdit.setEnabled(False)
        self.sprungPunkteEdit.setEnabled(False)
        self.wurfPunkteEdit.setEnabled(False)
        self.punkteTotalEdit.setEnabled(False)
        self.actionDatenbank_speichern.setEnabled(False)
        self.actionDatenbank_speichern_unter.setEnabled(False)
        self.openEvaluationButton.setEnabled(False)
        self.actionExport.setEnabled(False)
        self.actionImport.setEnabled(False)
        
    def closeDatabase(self):
        self.tableWidget.blockSignals(True)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0);
        self.tableWidget.blockSignals(False)
        self.blankDetails()
        self.disableUserInput()
        self.dbPath = None
        
    def enableUserInput(self):
        self.tableWidget.setEnabled(True)
        self.klasseCombo.setEnabled(True)
        self.geschlechtCombo.setEnabled(True)
        self.sprintSecEdit.setEnabled(True)
        self.LaufSecEdit.setEnabled(True)
        self.sprungMeterEdit.setEnabled(True)
        self.wurfMeterEdit.setEnabled(True)
        self.klasseEdit.setEnabled(True)
        self.nameEdit.setEnabled(True)
        self.vornameEdit.setEnabled(True)
        self.geschlechtEdit.setEnabled(True)
        self.sprintPunkteEdit.setEnabled(True)
        self.LaufPunkteEdit.setEnabled(True)
        self.sprungPunkteEdit.setEnabled(True)
        self.wurfPunkteEdit.setEnabled(True)
        self.punkteTotalEdit.setEnabled(True)
        if not self.RemoteEdit:
            self.actionDatenbank_speichern.setEnabled(True)
            self.actionDatenbank_speichern_unter.setEnabled(True)
            self.actionExport.setEnabled(True)
        self.actionImport.setEnabled(True)
        self.openEvaluationButton.setEnabled(True)
        
    def blankDetails(self):
        self.sprintSecEdit.setText("")
        self.LaufSecEdit.setText("")
        self.sprungMeterEdit.setText("")
        self.wurfMeterEdit.setText("")
        self.klasseEdit.setText("")
        self.nameEdit.setText("")
        self.vornameEdit.setText("")
        self.geschlechtEdit.setText("")
        self.sprintPunkteEdit.setText("")
        self.LaufPunkteEdit.setText("")
        self.sprungPunkteEdit.setText("")
        self.wurfPunkteEdit.setText("")
        self.punkteTotalEdit.setText("")
        self.sprintSecEdit.setReadOnly(True)
        self.LaufSecEdit.setReadOnly(True)
        self.sprungMeterEdit.setReadOnly(True)
        self.wurfMeterEdit.setReadOnly(True)
        self.prevRow = -1
        
    def closeEvent(self,  event):
        if self.dataChanged:
            if self.RemoteEdit:
                reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert und nicht gespeichert! Möchten Sie das Programm wirklich beenden?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.clearRecovery()
                    event.accept()
                else:
                    event.ignore()
            else:
                reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert. Möchten Sie die Änderungen speichern und dann das Programm beenden?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.on_actionDatenbank_speichern_triggered()
                    self.clearRecovery()
                    event.accept()
                elif reply == QMessageBox.Discard:
                    self.clearRecovery()
                    event.accept()
                else:
                    event.ignore()
        else:
            self.clearRecovery()
            event.accept()
    
    def setChanged(self, value):
        """
        Setzt ob die Datenbank verändert wurde
        @param value Verändert?
        """
        if not value == self.dataChanged:
            if value:
                self.setWindowTitle("{}* - FFSportfest".format(os.path.basename(self.dbPath)))
                self.dataChanged = True
            else:
                self.setWindowTitle("{} - FFSportfest".format(os.path.basename(self.dbPath)))
                self.dataChanged = False
    
    @pyqtSlot(int, int)
    def on_tableWidget_cellChanged(self, row, column):
        """
        Wird aufgerufen wenn Daten geändert werden
        
        @param row Geänderte Zeile
        @type int
        @param column Geänderte Spalte
        @type int
        """
        rowComplete = True
        for i in TableParams.CHECK_COLS:
            itm = self.tableWidget.item(row, i)
            if itm is None:
                rowComplete = False
                break
                
            if itm.text() == "":
                rowComplete = False
                break
        self.tableWidget.blockSignals(True)
        for i in range(self.tableWidget.columnCount()):
                try:
                    itm = self.tableWidget.item(row, i)
                    if not rowComplete:
                        itm.setBackground(QColor(255, 0, 0))
                    else:
                        itm.setBackground(QColor(255, 255, 255))
                except Exception:
                    print("Error")
        self.tableWidget.blockSignals(False)
        
    def calcAll(self):
        self.loadPD = QProgressDialog()
        self.loadPD.setWindowTitle("Berechne")
        self.loadPD.setLabelText("Berechne alle Punkte und Noten, bitte warten!")
        self.loadPD.setCancelButton(None)
        self.loadPD.setRange(0,  self.tableWidget.rowCount() - 1)
        self.loadPD.show()
        
        for c in range(0, self.tableWidget.rowCount()):
            self.calcRow(c)
            self.loadPD.setValue(c)
            
        self.loadPD.cancel()
    
    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemChanged(self, item):
        """
        Wird aufgerufen wenn Daten geändert werden (Item-basiert)
        
        @param item Geändertes Item
        @type QTableWidgetItem
        """
        updateDetails = self.tableWidget.currentRow() == item.row()
        
        if item.column() in TableParams.CHECK_COLS:
            self.sprintSecEdit.blockSignals(True)
            item.setText(item.text().replace(",",  "."))
            self.sprintSecEdit.blockSignals(False)
        
        if item.column() == TableCols.SPRINT_V:
            if updateDetails:
                self.sprintSecEdit.blockSignals(True)
                self.sprintSecEdit.setText(item.text())
                self.sprintSecEdit.blockSignals(False)
            self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['sprint_v'] = item.text()
        if item.column() == TableCols.LAUF_V:
            if updateDetails:
                self.LaufSecEdit.blockSignals(True)
                self.LaufSecEdit.setText(item.text())
                self.LaufSecEdit.blockSignals(False)
            self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['lauf_v'] = self.getSec(item.text())
        if item.column() == TableCols.SPRUNG_V:
            if updateDetails:
                self.sprungMeterEdit.blockSignals(True)
                self.sprungMeterEdit.setText(item.text())
                self.sprungMeterEdit.blockSignals(False)
            self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['sprung_v'] = item.text()
        if item.column() == TableCols.WURF_V:
            if updateDetails:
                self.wurfMeterEdit.blockSignals(True)
                self.wurfMeterEdit.setText(item.text())
                self.wurfMeterEdit.blockSignals(False)
            self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['wurf_v'] = item.text()
        self.calcRow(item.row())
        self.considerRecovery()
        
    def calcRow(self,  row):
        self.setChanged(True)
        self.tableWidget.blockSignals(True)
        klasse = self.tableWidget.item(row, TableCols.KLASSE).text()
        imale = (self.tableWidget.item(row, TableCols.GESCHLECHT).text().lower() == "m")
        sprintSec = float(self.tableWidget.item(row,  TableCols.SPRINT_V).text())
        laufSec = float(self.getSec(self.tableWidget.item(row,  TableCols.LAUF_V).text()))
        sprungMet = float(self.tableWidget.item(row,  TableCols.SPRUNG_V).text())
        wurfMet = float(self.tableWidget.item(row,  TableCols.WURF_V).text())
        
        sprintPkt = int(self.pCalc.Sprint(klasse,  sprintSec,  imale))
        sprintNot = int(self.nCalc.Sprint(klasse,  sprintSec,  imale))
        laufPkt = int(self.pCalc.Lauf(klasse,  laufSec,  imale))
        laufNot = int(self.nCalc.Lauf(klasse,  laufSec,  imale))
        sprungPkt = int(self.pCalc.Sprung(klasse,  sprungMet,  imale))
        sprungNot = int(self.nCalc.Sprung(klasse,  sprungMet,  imale))
        wurfPkt = int(self.pCalc.Wurf(klasse,  wurfMet,  imale))
        wurfNot = int(self.nCalc.Wurf(klasse,  wurfMet,  imale))
        totalPkt = sprintPkt + laufPkt + sprungPkt + wurfPkt
        
        noteFlt = 0.0
        noteCnt = 0
        totalNot = 6
        if self.ignNonPart:
            if sprintSec > 0:
                noteFlt += sprintNot
                noteCnt += 1
            if laufSec > 0:
                noteFlt += laufNot
                noteCnt += 1
            if sprungMet > 0:
                noteFlt += sprungNot
                noteCnt += 1
            if wurfMet > 0:
                noteFlt += wurfNot
                noteCnt += 1
            if noteCnt > 0:
                totalNot = round(float(noteFlt / noteCnt), 1)
            else:
                totalNot = 6
        else:
            totalNot = round(float((sprintNot + laufNot + sprungNot + wurfNot) / 4), 1)
            
        #print("Calc'd {}".format(str(totalNot)))
        
        self.tableWidget.item(row,  TableCols.SPRINT_P).setText(str(sprintPkt))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['sprint_p'] = sprintPkt
        self.tableWidget.item(row,  TableCols.SPRINT_N).setText(str(sprintNot))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['sprint_n'] = sprintNot
        
        self.tableWidget.item(row,  TableCols.LAUF_P).setText(str(laufPkt))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['lauf_p'] = laufPkt
        self.tableWidget.item(row,  TableCols.LAUF_N).setText(str(laufNot))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['lauf_n'] = laufNot
        
        self.tableWidget.item(row,  TableCols.SPRUNG_P).setText(str(sprungPkt))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['sprung_p'] = sprungPkt
        self.tableWidget.item(row,  TableCols.SPRUNG_N).setText(str(sprungNot))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['sprung_n'] = sprungNot
        
        self.tableWidget.item(row,  TableCols.WURF_P).setText(str(wurfPkt))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['wurf_p'] = wurfPkt
        self.tableWidget.item(row,  TableCols.WURF_N).setText(str(wurfNot))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['wurf_n'] = wurfNot
        
        self.tableWidget.item(row,  TableCols.PUNKTE).setText(str(totalPkt))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['punkte'] = totalPkt
        
        self.tableWidget.item(row,  TableCols.NOTE).setText(str(totalNot))
        self.JSD[klasse][self.tableWidget.item(row, TableCols.UID).text()]['note'] = totalNot
        
        self.tableWidget.blockSignals(False)
        
        if row == self.tableWidget.currentRow():
            self.sprintPunkteEdit.setText(str(sprintPkt) + " / " + str(sprintNot))
            self.LaufPunkteEdit.setText(str(laufPkt) + " / " + str(laufNot))
            self.sprungPunkteEdit.setText(str(sprungPkt) + " / " + str(sprungNot))
            self.wurfPunkteEdit.setText(str(wurfPkt) + " / " + str(wurfNot))
            self.punkteTotalEdit.setText(str(totalPkt))
            #TODO: Note!!!
        self.syncToEval()
        
    def syncToEval(self):
        print("SendTo Eval...")
        if self.EvalW is not None:
            print("ST isnt none")
            self.EvalW.refreshData(self.JSD)
            
    """
    Gibt zurück ob der Schüler krank ist (Checkbox-Ersatz)
    @param text Text
    """
    def istKrank(self, text):
        if text.startswith("☒"):
            return True
        else:
            return False
            
    """
    Gibt den Checkbox-Ersatz zurück
    @param bval Krank oder nicht
    """
    def getKrank(self, bval):
        if bval:
            return "☒ Krank"
        else:
            return "☑ Anwesend"
            
    
    @pyqtSlot(str)
    def on_klasseCombo_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        self.blankDetails()
        self.fillTable(p0,  self.getGeschlechtFromLong(self.geschlechtCombo.currentText()),  False)
        
    def gotoNextHealthyCell(self,  crow,  ccol):
        if self.tableWidget.rowCount() == crow:
                print("LAST ROW")
                return
        if self.tableWidget.item(crow+1,  TableCols.KRANK) is None:
            print('NEXT ROW NONEXISTENT!')
            return
        #if self.tableWidget.item(crow+1,  TableCols.KRANK).checkState() == Qt.Checked:
        if self.istKrank(self.tableWidget.item(crow+1,  TableCols.KRANK).text()):
            self.gotoNextHealthyCell(crow+1,  ccol)
        else:
            self.tableWidget.setCurrentCell(crow+1, ccol)
    
    @pyqtSlot(int)
    def on_tableWidget_keyPressed(self, key):
        """
        Slot documentation goes here.
        """
        tw = self.tableWidget
        ccol = tw.currentColumn()
        crow = tw.currentRow()
        #rcount = tw.rowCount()
        ccount = tw.columnCount()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.gotoNextHealthyCell(crow, ccol)
        elif key == Qt.Key_Tab:
            if ccount - 1 == ccol:
                self.gotoNextHealthyCell(crow, TableCols.NAME)
                #return
            ncol = ccol
            while ncol < (ccount - 1):
                ncol += 1
                if not tw.isColumnHidden(ncol):
                    tw.setCurrentCell(crow, ncol)
                    break
            #tw.setCurrentCell(crow, ccol+1)
        elif key == Qt.Key_Backspace:
            tw.setCurrentCell(crow, TableCols.NAME)
            print("BKSPACE");
        elif key == Qt.Key_Delete:
            if not ccol in TableParams.CHECK_COLS:
                return
            if not self.ConfirmDelete:
                reply = QMessageBox.question(self, 'FFSportfest', 'Möchten Sie diesen Wert löschen? Wählen Sie "Ja, alle" um diese Abfrage nicht mehr anzuzeigen.', QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.YesToAll:
                    self.ConfirmDelete = True
                elif reply == QMessageBox.No:
                    return
            
            if ccol == TableCols.SPRINT_V:
                tw.setItem(crow,  ccol,  QTableWidgetItem("0.0"))
            elif ccol == TableCols.LAUF_V:
                tw.setItem(crow,  ccol,  QTableWidgetItem("0:00"))
            elif ccol == TableCols.SPRUNG_V:
                tw.setItem(crow,  ccol,  QTableWidgetItem("0.0"))
            elif ccol == TableCols.WURF_V:
                tw.setItem(crow,  ccol,  QTableWidgetItem("0.0"))
        elif key == Qt.Key_Space:
            if ccol == TableCols.KRANK:
                itm = tw.item(crow, ccol)
                #krank = not self.boolChecked(itm.checkState())
                krank = not self.istKrank(itm.text())
                if krank:
                    self.healthyRows -= 1
                else:
                    self.healthyRows += 1
                itm.setText(self.getKrank(krank))
                self.toggleRow(crow,  krank)
                self.JSD[self.tableWidget.item(crow, TableCols.KLASSE).text()][self.tableWidget.item(crow, TableCols.UID).text()]['krank'] = krank
                self.syncToEval()
        #elif key == Qt.Key_Delete:
        #    if ccol in TableParams.CHECK_COLS:
        #        tw.setItem(crow,  ccol,  QTableWidgetItem(""))
        #        print("DELETE");
    
    @pyqtSlot()
    def on_tableWidget_itemSelectionChanged(self):
        """
        Slot documentation goes here.
        """
        
        if not self.prevRow == self.tableWidget.currentRow():
            self.prevRow = self.tableWidget.currentRow()
            try:
                self.nameEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.NAME).text())
                self.vornameEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.VORNAME).text())
                self.klasseEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.KLASSE).text())
                self.geschlechtEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.GESCHLECHT).text())
                self.sprintSecEdit.blockSignals(True)
                self.LaufSecEdit.blockSignals(True)
                self.sprungMeterEdit.blockSignals(True)
                self.wurfMeterEdit.blockSignals(True)
                self.sprintSecEdit.setReadOnly(False)
                self.sprintSecEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRINT_V).text())
                self.LaufSecEdit.setReadOnly(False)
                self.LaufSecEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.LAUF_V).text())
                self.sprungMeterEdit.setReadOnly(False)
                self.sprungMeterEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRUNG_V).text())
                self.wurfMeterEdit.setReadOnly(False)
                self.wurfMeterEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.WURF_V).text())
                self.sprintSecEdit.blockSignals(False)
                self.LaufSecEdit.blockSignals(False)
                self.sprungMeterEdit.blockSignals(False)
                self.wurfMeterEdit.blockSignals(False)
                self.sprintPunkteEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRINT_P).text() + " / " + self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRINT_N).text())
                self.LaufPunkteEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.LAUF_P).text() + " / " + self.tableWidget.item(self.tableWidget.currentRow(), TableCols.LAUF_N).text())
                self.sprungPunkteEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRUNG_P).text() + " / " + self.tableWidget.item(self.tableWidget.currentRow(), TableCols.SPRUNG_N).text())
                self.wurfPunkteEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.WURF_P).text() + " / " + self.tableWidget.item(self.tableWidget.currentRow(), TableCols.WURF_N).text())
                self.punkteTotalEdit.setText(self.tableWidget.item(self.tableWidget.currentRow(), TableCols.PUNKTE).text())
                #TODO: Note
            except  Exception:
                print("Exception in tW_iSC")
            
        #crow = self.tableWidget.currentRow()
        
        
        
        print("ItemSelectionChanged")
    
    @pyqtSlot(str)
    def on_geschlechtCombo_currentIndexChanged(self, p0):
        """
        Wird aufgerufen wenn der Geschlecht-Filter geändert wurde
        """
        self.blankDetails()
        self.fillTable(str(self.klasseCombo.currentText()),  self.getGeschlechtFromLong(p0),  False)
    
    @pyqtSlot()
    def on_wurfMeterEdit_editingFinished(self):
        """
        Wird aufgerufen wenn das Textfeld "Wurf/Stoß"-Distanz geändert wurde
        """
        self.wurfMeterEdit.blockSignals(True)
        self.wurfMeterEdit.setText(self.wurfMeterEdit.text().replace(",",  "."))
        self.wurfMeterEdit.blockSignals(False)
        crow = self.tableWidget.currentRow()
        self.tableWidget.blockSignals(True)
        self.tableWidget.setItem(crow, TableCols.WURF_V, QTableWidgetItem(self.wurfMeterEdit.text()))
        self.tableWidget.blockSignals(False)
        self.calcRow(crow)
        
    
    @pyqtSlot()
    def on_sprintSecEdit_editingFinished(self):
        """
        Wird aufgerufen wenn das Textfeld "Sprint"-Zeit geändert wurde
        """
        self.sprintSecEdit.blockSignals(True)
        self.sprintSecEdit.setText(self.sprintSecEdit.text().replace(",",  "."))
        self.sprintSecEdit.blockSignals(False)
        crow = self.tableWidget.currentRow()
        self.tableWidget.blockSignals(True)
        self.tableWidget.setItem(crow, TableCols.SPRINT_V, QTableWidgetItem(self.sprintSecEdit.text()))
        self.tableWidget.blockSignals(False)
        self.calcRow(crow)
        
    def getSec(self, time_str):
        m, s = time_str.split(':')
        return int(m) * 60 + int(s)
        
    def getTime(self, secs):
        m, s = divmod(secs, 60)
        return "%d:%02d" % (m, s)
        
    def openDataset(self):
        self.statusBar.showMessage("Öffne Datenbank...") 
        db_file,  _ = QFileDialog.getOpenFileName(self, "Datenbank öffnen", os.path.expanduser("~"), "FFD-Datenbank (*.ffd);;Sicherungsdateien (*.ffd~);;Alle Dateien (*.*)");

        if db_file:
            
            self.loadDb(db_file)
            
    def loadDb(self,  path, recovery=False):
        if not os.path.isfile(path):
            return False
        self.loadPD = QProgressDialog()
        self.loadPD.setWindowTitle("Lade Datenbank...")
        self.loadPD.setLabelText("Lade Datenbank, bitte warten!")
        self.loadPD.setCancelButton(None)
        self.loadPD.setRange(0,  5)
        self.loadPD.show()
        self.loadPD.setValue(1)
        if not recovery:
            self.dbPath = path
        if self.loadLastDb and not self.RemoteEdit and not recovery:
            self.pCfg.setLastDb(str(path))
        try:
            self.loadPD.setValue(2)
            self.JSD = json.load(codecs.open(str(path), 'r', 'utf-8-sig'))
            self.setWindowTitle("{} - FFSportfest".format(str(os.path.basename(path))))
            self.loadPD.setValue(3)
            self.fillTable("Alle",  "Alle",  True)
            self.loadPD.setValue(4)
            self.enableUserInput()
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
        if self.pCfg.getBackupFile() and not recovery:
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
        self.syncToEval()
        self.loadPD.setValue(5)
        self.loadPD.cancel()
        self.statusBar.showMessage("Datenbank geladen!") 
        
    def clearAlleKlassen(self):
        self.alleKlassen.clear()
        
    def addKlasse(self,  klasse):
        if not klasse in self.alleKlassen:
            self.alleKlassen.insert(len(self.alleKlassen),  klasse)
        ks = self.getKlassenstufe(klasse)
        if not ks in self.alleKlassen:
            self.alleKlassen.insert(len(self.alleKlassen),  ks)
        
    def validKlasse(self, input):
        try:
            float(input)
        except Exception:
            return False
        return True
        
    def getKlassenstufe(self,  input):
        return re.findall("^[^\d]*(\d+)",  input)[0]

            
    def doFilter(self,  filter,  compareTo):
        if not filter:
            return True;
            
        if filter == "Alle":
            return True;
        
        pe = re.compile("(^[0-9]{1}\\.[0-9])+")
        me = pe.match( filter )
        pa = re.compile("^[-+]?[0-9]+$")
        ma = pa.match( filter )
        if me:
            return filter == compareTo;
        elif ma:
            return compareTo.startswith(filter);
        else:
            return True;
            
    def toggleRow(self,  row,  disabled):
        for i in range(self.tableWidget.columnCount()):
                try:
                    itm = self.tableWidget.item(row, i)
                    #if not i == TableCols.KRANK:
                    if disabled:
                        itm.setFlags(itm.flags() ^ Qt.ItemIsEnabled)
                    else:
                        itm.setFlags(itm.flags() | Qt.ItemIsEnabled)
                        
                    
                except Exception:
                    print("Error")
            
    def checkedBool(self,  input):
        if input:
            return Qt.Checked
        else:
            return Qt.Unchecked
            
    def boolChecked(self,  input):
        if input == Qt.Checked:
            return True
        else:
            return False
            
    def getGeschlechtFromLong(self,  long):
        print(str(long).lower())
        if str(long).lower() == "alle":
            return "Alle"
        elif str(long).lower() == "jungen":
            return "M"
        else:
            return "W"
            
    def considerRecovery(self):
        if self.doRec:
            try:
                with open(self.pCfg.getRecoverFile(), 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Die Absturzsicherungsdatei konnte nicht geschrieben werden! Bitte überprüfen Sie ob Sie für die folgende Datei Schreibrechte besitzen: \n" + str(self.rcv) + "\nDie Funktion wird zunächst abgeschaltet, damit Sie weiterarbeiten können!")
                msg.setWindowTitle("FFSportfest - Absturzsicherung")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.pCfg.setRecovery(False)
                    
    def clearRecovery(self):
        if self.doRec:
            rcv = self.pCfg.getRecoverFile()
            try:
                if os.path.isfile(rcv):
                    os.remove(rcv)
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Die Datei der Absturzsicherung konnte nicht gelöscht werden. Sie werden möglicherweise beim nächsten Programmstart über einen Programmabsturz benachrichtigt, obwohl das Programm nicht abgestürzt ist. Sie können die Datei manuell löschen, sie befindet sich hier: \n" + str(self.rcv))
                msg.setWindowTitle("FFSportfest - Absturzsicherung")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                
    def loadRecovery(self):
        self.loadDb(self.pCfg.getRecoverFile(), True)
        self.setWindowTitle("(Wiederhergestellt) - FFSportfest")
        
    def clearBackup(self):
        try:
            if os.path.isfile(self.dbPath + "~"):
                os.remove(self.dbPath + "~")
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die Sicherungsdatei konnte nicht entfernt werden (dies sind die Dateien mit dem Suffix ~) - Sie können dies manuell tun indem Sie folgende Datei löschen: \n" + str(self.dbPath + "~"))
            msg.setWindowTitle("FFSportfest - Sicherungsdatei")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            
    def verifyJSON(self,  det):
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
            
    def saveRec(self):
        if self.doRec:
            try:
                with open(self.pCfg.getRecoverFile(), 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
            except Exception as ex:
                print("WARN: Could not save recovery file: " + str(ex))
            
    def fillTable(self,  filterKlasse,  filterGeschlecht, dbLoad):
        print("Klasse: " + filterKlasse,  " Geschlecht: " + filterGeschlecht)
        self.tableWidget.blockSignals(True)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0);
            #uiditem.setFlags(uiditem.flags() ^ Qt.ItemIsEnabled)
        self.blankDetails()
        if dbLoad:
            self.clearAlleKlassen()
        self.tableWidget.setRowCount(0)
        sc = 0
        for klasse,  schueler in self.JSD.items():
            if not self.validKlasse(klasse):
                print("Ignoriere ungueltige Klasse {}".format(klasse))
                continue
            if dbLoad:
                self.addKlasse(klasse)
            if self.doFilter(filterKlasse,  klasse):
                print("Allowing student, FK: {}, K: {}".format(str(filterKlasse), str(klasse)))
                for uid, det in schueler.items():
                    self.verifyJSON(det)
                    if not filterGeschlecht == "Alle":
                        if not filterGeschlecht.lower() == det['geschlecht'].lower():
                            continue
                            
                    self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                    iskrank = det['krank']
                    if not iskrank:
                        self.healthyRows += 1
                    self.tableWidget.setItem(sc,TableCols.UID, QTableWidgetItem(uid))
                    self.tableWidget.setItem(sc,TableCols.NAME, QTableWidgetItem(det['name']))
                    self.tableWidget.setItem(sc,TableCols.VORNAME, QTableWidgetItem(det['vorname']))
                    self.tableWidget.setItem(sc,TableCols.GESCHLECHT, QTableWidgetItem(det['geschlecht']))
                    self.tableWidget.setItem(sc,TableCols.KLASSE, QTableWidgetItem(klasse))
                    self.tableWidget.setItem(sc,TableCols.SPRINT_V, QTableWidgetItem(str(det['sprint_v'])))
                    self.tableWidget.setItem(sc,TableCols.SPRINT_P, QTableWidgetItem(str(det['sprint_p'])))
                    self.tableWidget.setItem(sc,TableCols.SPRINT_N, QTableWidgetItem(str(det['sprint_n'])))
                    self.tableWidget.setItem(sc,TableCols.LAUF_V, QTableWidgetItem(self.getTime(int(det['lauf_v']))))
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
                    self.tableWidget.setItem(sc,TableCols.KRANK, QTableWidgetItem(str(self.getKrank(iskrank))))
                    #krankbox = QTableWidgetItem("Krank")
                    #krankbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    #krankbox.setCheckState(self.checkedBool(iskrank))
                    #self.tableWidget.setItem(sc, TableCols.KRANK,  krankbox)
                    
                    self.toggleRow(sc,  iskrank)
                    
                    #CALCULATE!!
                    print("UID: " + uid)
                    print("Name: " + det['name'])
                    sc += 1
        self.pCfg.doSortBy(self.tableWidget)
        self.tableWidget.blockSignals(False) 
        if dbLoad:
            self.alleKlassen.sort()
            self.klasseCombo.blockSignals(True)
            self.klasseCombo.clear()
            self.klasseCombo.addItem("Alle")
            self.klasseCombo.addItems(self.alleKlassen)
            self.klasseCombo.blockSignals(False)
            
            if self.EvalW is not None:
                self.EvalW.refreshKlassen(self.alleKlassen)
            
            self.klasseCombo.setCurrentIndex(0)
        
        #self.resizeTable()
                
    
    @pyqtSlot()
    def on_LaufSecEdit_editingFinished(self):
        """
        Slot documentation goes here.
        """
        #self.LaufSecEdit.blockSignals(True)
        #self.LaufSecEdit.setText(self.LaufSecEdit.text().replace(",",  "."))
        #self.LaufSecEdit.blockSignals(False)
        crow = self.tableWidget.currentRow()
        self.tableWidget.blockSignals(True)
        self.tableWidget.setItem(crow, TableCols.LAUF_V, QTableWidgetItem(self.LaufSecEdit.text()))
        self.tableWidget.blockSignals(False)
        self.calcRow(crow)
        
    
    @pyqtSlot()
    def on_sprungMeterEdit_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.sprungMeterEdit.blockSignals(True)
        self.sprungMeterEdit.setText(self.sprungMeterEdit.text().replace(",",  "."))
        self.sprungMeterEdit.blockSignals(False)
        crow = self.tableWidget.currentRow()
        self.tableWidget.blockSignals(True)
        self.tableWidget.setItem(crow, TableCols.SPRUNG_V, QTableWidgetItem(self.sprungMeterEdit.text()))
        self.tableWidget.blockSignals(False)
        self.calcRow(crow)
    
    @pyqtSlot()
    def on_actionDatenbank_laden_triggered(self):
        """
        Öffnet eine Datenbank
        """
        self.openDataset()
    
    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemClicked(self, item):
        """
        Wird aufgerufen wenn Item in Tabelle angeklickt wurde (für Krank-Toggle)
        """
        if item.column() == TableCols.KRANK:
            krank = not self.istKrank(item.text())
            #if self.boolChecked(item.checkState()):
            if krank:
                self.healthyRows -= 1
            else:
                self.healthyRows += 1
            item.setText(self.getKrank(krank))
            self.toggleRow(item.row(),  krank)
            self.JSD[self.tableWidget.item(item.row(), TableCols.KLASSE).text()][self.tableWidget.item(item.row(), TableCols.UID).text()]['krank'] = krank
            self.syncToEval()
    
    @pyqtSlot()
    def on_actionDatenbank_speichern_triggered(self):
        """
        Speichert die Datenbank unter dem gleichen Namen wieder ab (oder unter einem neuen falls sie nicht existiert (sollte nicht passieren)
        """
        if self.dbPath:
            if str(self.dbPath).endswith("~"):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Sie haben eine Sicherungsdatei geöffnet und es kann nicht in Sicherungsdateien gespeichert werden. Speichern Sie die Datei bitte unter einem anderen Namen (Datei - Speichern unter…)")
                msg.setWindowTitle("FFSportfest - Sicherungsdatei")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            
            try:
                with open(self.dbPath, 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
                    self.setChanged(False)
            except PermissionError as per:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diese Datei besitzen. Sie können entweder die Datei unter einem anderen Namen speichern (Datei - Speichern unter…) oder Schreibrechte für die Datei erlangen.")
                msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                msg.setDetailedText("Dateipfad: " + str(self.dbPath) + "\n" + str(per))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            
            self.clearBackup()
        else:
            self.on_actionDatenbank_speichern_unter_triggered()
    
    @pyqtSlot()
    def on_actionDatenbank_speichern_unter_triggered(self):
        """
        Speichert die Datenbank unter einem anderen Namen ab
        """
        opts = QFileDialog.Options()
        name, _ = QFileDialog.getSaveFileName(self, "Datenbank speichern unter", os.path.expanduser("~"), "FFD-Datenbank (*.ffd)",  options=opts)
        if name:
            filename = str(name)
            if not filename.endswith(".ffd"):
                filename+= ".ffd"
            
            try:
                with open(filename, 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
                    self.setChanged(False)
            except PermissionError as per:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diesen Ort besitzen. Bitte wählen Sie einen anderen Ort aus!")
                msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                msg.setDetailedText("Dateipfad: " + str(filename) + "\n" + str(per))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            
            self.setChanged(False)
            self.clearBackup()
    
    @pyqtSlot()
    def on_action_ber_FFSportfest_triggered(self):
        """
        Zeigt Informationen über das Programm an
        """
        QMessageBox.about(self, "Über FFSportfest...",  "<h1>Über FFSportfest</h1><small>Version " + FFSportfest.VERSION + " (" + FFSportfest.CODENAME + ")</small><p>Geschrieben von Fabian Schillig</p><br><code>Dieses Programm ist Freie Software: Sie können es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation, Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren veröffentlichten Version, weiterverbreiten und/oder modifizieren.<br><br>Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK. Siehe die GNU General Public License für weitere Details.<br><br>Sie sollten eine Kopie der GNU General Public License zusammen mit diesem Programm erhalten haben. Wenn nicht, siehe <a href='http://www.gnu.org/licenses/'>http://www.gnu.org/licenses/</a>.</code><br><p>© Fabian Schillig 2017-2018. Der Quellcode ist unter <a href='https://github.com/XorgMC/ffx-sportfest'>https://github.com/XorgMC/ffx-sportfest</a> erhältlich.</p>")
    
    @pyqtSlot()
    def on_action_ber_Qt_triggered(self):
        """
        Zeigt Informationen über Qt an
        """
        QMessageBox.aboutQt(self,  "Über Qt...")
    
    @pyqtSlot()
    def on_actionDrucken_triggered(self):
        """
        Druckt die aktuelle Anzeige aus
        """
        # TODO: Entfernen
        dialog = QPrintPreviewDialog()
        dialog.printer().setPageOrientation(QPageLayout.Landscape)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
        
    def isRowKrank(self,  row):
        if self.tableWidget.item(row,  TableCols.KRANK) is None:
            return False
        #return self.tableWidget.item(row,  TableCols.KRANK).checkState() == Qt.Checked
        return self.isKrank(self.tableWidget.item(row,  TableCols.KRANK).text())
        
    def getPrintHeader(self):
        #sK = str(self.klasseCombo.currentText) TODO
        sK = "Alle"
        if sK.lower() == "alle":
            return TableParams.PRINTM_LBL
        elif sK.startswith("5"):
            return TableParams.PRINTM5_LBL
        elif sK.startswith("6"):
            return TableParams.PRINTM6_LBL
        elif sK.startswith("7"):
            return TableParams.PRINTM7_LBL
        
    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    # PRINTM_LBL = [ "Name",  "Vorname",  "Klasse",  "Sprint",  "Pkt/Nt.",  "Lauf",  "Pkt/Nt.",  "Sprung",  "Pkt/Nt.",  "Wu/St",  "Pkt/Nt.",  "Punkte",  "Note"]
    def makeTableDocument(self):
        document = QTextDocument()
        cursor = QTextCursor(document)
        rows = self.tableWidget.rowCount()
        #rows = self.healthyRows
        #columns = self.tableWidget.columnCount()
        tfmt = QTextTableFormat()
        tfmt.setCellPadding(5.0)
        tfmt.setCellSpacing(-1)
        tfmt.setBorder(2)
        tfmt.setBorderStyle(QTextFrameFormat.BorderStyle_Solid)
        tfmt.setBorderBrush(QColor(0, 0,  0))
        table = cursor.insertTable(self.healthyRows + 1, 17,  tfmt)
        format = table.format()
        format.setHeaderRowCount(1)
        table.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QFont.Bold)
        header = self.getPrintHeader()
        print(header)
        for c in range(0, 17):
            cursor.setCharFormat(format)
            cursor.insertText(header[c])
            cursor.movePosition(QTextCursor.NextCell)
#        for column in range(columns):
#            cursor.setCharFormat(format)
#            cursor.insertText(self.tableWidget.horizontalHeaderItem(column).text())
#            cursor.movePosition(QtGui.QTextCursor.NextCell)

        aCen = QTextBlockFormat()
        aCen.setAlignment(Qt.AlignCenter)
        for row in range(rows):
            if self.isRowKrank(row):
                continue
            cursor.insertText(self.tableWidget.item(row, TableCols.NAME).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.VORNAME).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.KLASSE).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_V).text() + "s")
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_P).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_N).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_V).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_P).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_N).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_V).text() + "m")
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_P).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_N).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_V).text() + "m")
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_P).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_N).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.PUNKTE).text())
            cursor.movePosition(QTextCursor.NextCell)
            cursor.setBlockFormat(aCen)
            cursor.insertText(self.tableWidget.item(row, TableCols.NOTE).text())
            cursor.movePosition(QTextCursor.NextCell)
#            for column in range(columns):
#                cursor.insertText(
#                    self.tableWidget.item(row, column).text())
#                cursor.movePosition(QtGui.QTextCursor.NextCell)
        return document
        
    
    @pyqtSlot()
    def on_openEvaluationButton_clicked(self):
        """
        Öffnet das Auswertungsfenster
        """
        if self.RemoteEdit:
            reply = QMessageBox.question(self, 'FFSportfest', 'Es wird empfohlen die Auswertung auf dem Hauptrechner durchzuführen. Möchten Sie die Auswertung trotzdem öffnen?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if not reply == QMessageBox.Yes:
                return
                
        if self.EvalW is not None:
            print("evalw is not none")
            if not self.EvalW.isVisible():
                self.EvalW.show()
            else:
                # this will remove minimized status 
                # and restore window with keeping maximized/normal state
                self.EvalW.setWindowState(self.EvalW.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
                # this will activate the window
                self.EvalW.activateWindow()
    
    @pyqtSlot()
    def on_actionDatenbank_bearbeiten_2_triggered(self):
        """
        Öffnet den Datenbankeditor
        """
        if self.dataChanged:
            reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert. Möchten Sie die Änderungen speichern?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.on_actionDatenbank_speichern_triggered()
            elif reply == QMessageBox.Discard:
                self.clearRecovery() #TODO: Datenbank sauber schließen
            else:
                return
        if self.dbPath:
            if not self.dbf is None:
                self.dbf.mOpen(self.dbPath)
            self.closeDatabase()
        if not self.dbf is None:
            if not self.dbf.isVisible():
                self.dbf.show()
            else:
                self.dbf.setWindowState(self.dbf.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
                self.dbf.activateWindow()
    
    @pyqtSlot()
    def on_actionSpeichernPortable_triggered(self):
        """
        Datenbank speichern (portabler Modus)
        """
        if self.dbPath:
            try:
                with open(self.dbPath, 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
                    self.setChanged(False)
            except PermissionError as per:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diese Datei besitzen! Bitte speichern Sie die Datei im folgenden Dialog an einem anderen Ort ab.")
                msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                msg.setDetailedText("Dateipfad: " + str(self.dbPath) + "\n" + str(per))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.portableSaveAs()
        else:
            self.portableSaveAs()
            
    def portableSaveAs(self):
        opts = QFileDialog.Options()
        name, _ = QFileDialog.getSaveFileName(self, "Datenbank speichern unter", os.path.expanduser("~"), "FMD-Datenbank (*.fmd)",  options=opts)
        if name:
            filename = str(name)
            if not filename.endswith(".fmd"):
                filename+= ".fmd"
            
            try:
                with open(filename, 'w') as f:
                    json.dump(self.JSD, f, indent=4, sort_keys=True, ensure_ascii=False)
                    self.setChanged(False)
            except PermissionError as per:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Die Datenbank konnte nicht gespeichert werden, da Sie keine Schreibrechte für diesen Ort besitzen.")
                msg.setWindowTitle("FFSportfest - Fehler beim Speichern")
                msg.setDetailedText("Dateipfad: " + str(filename) + "\n" + str(per))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return;
    
    @pyqtSlot()
    def on_actionBeendenPortable_triggered(self):
        """
        Beenden (portabler Modus)
        """
        if self.dataChanged:
            reply = QMessageBox.question(self, 'FFSportfest', 'Die Datenbank wurde verändert und nicht gespeichert! Möchten Sie das Programm wirklich beenden?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.close()
                
    
    @pyqtSlot()
    def on_actionExport_triggered(self):
        """
        Erstellt eine portable Datenbank (für simultanes Arbeiten an mehreren PCs)
        """
        regex = re.compile(r'^([0-9]{1,2})$')
        exp = ExportDialog(self.JSD, filter(regex.search, self.alleKlassen),  self)
        exp.exec_()
    
    @pyqtSlot()
    def on_actionImport_triggered(self):
        """
        Importiert eine portable Datenbank (für simultanes Arbeiten an mehreren PCs)
        """
        db_file,  _ = QFileDialog.getOpenFileName(self, "Datenbank öffnen", os.path.expanduser("~"), "FFD-Datenbank (*.fmd)");

        if db_file:
            MDB = json.load(codecs.open(str(db_file), 'r', 'utf-8-sig'))
            self.JSD = merge(self.JSD, MDB)
            pprint(self.JSD, width=40)
            self.fillTable("Alle",  "Alle",  True)
            self.statusBar.showMessage("Mobile Datenbank wurde importiert!",  5000) 
    
    @pyqtSlot()
    def on_actionEinstellungen_triggered(self):
        """
        Einstellungsdialog öffnen
        """
        prefs = SettingsDialog(self.pCfg, self)
        prefs.exec_()
        self.loadLastDb = self.pCfg.getLoadLastDb()
    
    @pyqtSlot()
    def on_actionEinstellungenPortable_triggered(self):
        """
        Öffnet den portablen Einstellungsdialog
        """
        pprefs = SettingsPortableDialog(self.pCfg, self)
        pprefs.exec_()
    
    @pyqtSlot()
    def on_actionBeenden_triggered(self):
        """
        Slot documentation goes here.
        """
        self.close()

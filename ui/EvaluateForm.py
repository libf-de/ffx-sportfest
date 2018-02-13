# -*- coding: utf-8 -*-

"""
Module implementing EvalWindow.
"""

from PyQt5.QtCore import pyqtSlot,  Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,  QAbstractItemView,  QDialog,  QMessageBox, QFileDialog, QHeaderView
from lib.Delegates import ReadonlyDelegate
from lib.Constants import TableCols, ETableCols,  TableHide,  TableParams
from Configuration import Configuration
from FTableWidgetItem import FTableWidgetItem
import re,  datetime,  os, sys, subprocess 

from PyQt5 import QtGui,  QtPrintSupport

from .Ui_EvaluateForm import Ui_MainWindow

#DOCX
from docxtpl import DocxTemplate
#/DOCX


class EvalWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    par = None
    JSD = None
    pCfg = None
    hCount = 0
    
    Filter1 = "Alle"
    Filter2 = "Alle"
    Klassen = [ "Alle" ]
    
    def __init__(self, config, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EvalWindow, self).__init__(parent)
        self.setupUi(self)

        #self.pCfg = Configuration()
        self.pCfg = config
        #self.setWindowIcon(QIcon(self.pCfg.getIconPath("eval"))) TODO: Icon
        
        self.par = parent
        
        tW = self.tableWidget
        tW.blockSignals(True)
        tW.setRowCount(0)
        tW.setColumnCount(20)
        tW.setSelectionMode(QAbstractItemView.SingleSelection)
                
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
        
        #tW.setItemDelegateForColumn(TableCols.SPRINT_V,  NumDelegate(self))
        #tW.setItemDelegateForColumn(TableCols.LAUF_V,  TimeDelegate(self))
        #tW.setItemDelegateForColumn(TableCols.SPRUNG_V,  NumDelegate(self))
        #tW.setItemDelegateForColumn(TableCols.WURF_V,  NumDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRINT_V,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.LAUF_V,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.SPRUNG_V,  ReadonlyDelegate(self))
        tW.setItemDelegateForColumn(TableCols.WURF_V,  ReadonlyDelegate(self))
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
        tW.setHorizontalHeaderLabels( TableParams.HEADER_LBL )
        tW.blockSignals(False)
        
        hdr = self.tableWidget.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeToContents)
        hdr.setMinimumSectionSize(50)
        hdr.setSectionResizeMode(TableCols.NAME, QHeaderView.Interactive)
        hdr.setSectionResizeMode(TableCols.VORNAME, QHeaderView.Interactive)
        
        sF = self.sortFirstCombo
        sF.blockSignals(True)
        sF.addItem("Nichts")
        sF.addItem("Punkte")
        sF.addItem("Note")
        sF.addItem("Klasse")
        sF.addItem("Nachname")
        sF.addItem("Vorname")
        sF.blockSignals(False)
        
        sS = self.sortSecondCombo
        sS.blockSignals(True)
        sS.addItem("Nichts")
        sS.addItem("Punkte")
        sS.addItem("Note")
        sS.addItem("Klasse")
        sS.addItem("Nachname")
        sS.addItem("Vorname")
        sS.blockSignals(False)
        
    def sortColByName(self,  inp):
        if inp.lower() == "punkte":
            self.tableWidget.sortItems(ETableCols.PUNKTE,  Qt.DescendingOrder)
        elif inp.lower() == "note":
            self.tableWidget.sortItems(ETableCols.NOTE,  Qt.AscendingOrder)
        elif inp.lower() == "klasse":
            self.tableWidget.sortItems(ETableCols.KLASSE,  Qt.AscendingOrder)
        elif inp.lower() == "nachname":
            self.tableWidget.sortItems(ETableCols.NAME,  Qt.AscendingOrder)
        elif inp.lower() == "vorname":
            self.tableWidget.sortItems(ETableCols.VORNAME,  Qt.AscendingOrder)
        
    def resortData(self):
        fSort = str(self.sortFirstCombo.currentText())
        sSort = str(self.sortSecondCombo.currentText())
        if not sSort.lower() == "nichts":
            self.sortColByName(sSort)
        if not fSort.lower() == "nichts":
            self.sortColByName(fSort)
        
    def refreshData(self, data):
        print("REFRESH!")
        self.JSD = data
        self.fillTable(self.Filter1, self.Filter2)
        self.resortData()
        
    def refreshKlassen(self,  klassen):
        self.Klassen = [ "Alle" ]
        self.Klassen.extend(klassen)
        
        print(self.Klassen)
        
        self.filterSecondCombo.blockSignals(True)
        self.filterSecondCombo.clear()
        self.filterSecondCombo.addItem("aller Klassen")
        
        for i in self.Klassen:
            if i == "Alle":
                continue
            if re.match("^([0-9]{1,2})\.([0-9]{1})$",  str(i)):
                self.filterSecondCombo.addItem(str("der Klasse {}").format(i))
            else:
                self.filterSecondCombo.addItem(str("der {}. Klassen").format(i))
                
        self.filterSecondCombo.blockSignals(False)
        
        
    def fillTable(self,  filterKlasse,  filterGeschlecht):
        self.tableWidget.blockSignals(True)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
            
        self.tableWidget.setRowCount(0)
        sc = 0
        for klasse,  schueler in self.JSD.items():
            if self.doFilter(filterKlasse,  klasse):
                for uid, det in schueler.items():
                    if not filterGeschlecht == "Alle":
                        if not filterGeschlecht.lower() == det['geschlecht'].lower():
                            continue
                            
                    iskrank = det['krank']
                    if iskrank:
                        continue
                    self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
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
                    self.tableWidget.setItem(sc,TableCols.PUNKTE, FTableWidgetItem(str(det['punkte'])))
                    if 'note' in det:
                        self.tableWidget.setItem(sc,TableCols.NOTE, QTableWidgetItem(str(det['note'])))
                    krankbox = QTableWidgetItem("Krank")
                    krankbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    
                    self.tableWidget.setItem(sc, TableCols.KRANK,  krankbox)
                    
                    #CALCULATE!!
                    print("UID: " + uid)
                    print("Name: " + det['name'])
                    sc += 1
        self.tableWidget.blockSignals(False)   
        
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
            
    def getSec(self, time_str):
        m, s = time_str.split(':')
        return int(m) * 60 + int(s)
        
    def getTime(self, secs):
        m, s = divmod(secs, 60)
        return "%d:%02d" % (m, s)
    
    @pyqtSlot(str)
    def on_sortFirstCombo_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        self.resortData()
    
    @pyqtSlot(str)
    def on_sortSecondCombo_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        self.resortData()

    @pyqtSlot()
    def on_actionDrucken_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.printer().setPageOrientation(QtGui.QPageLayout.Landscape)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
        
    def isRowKrank(self,  row):
        if self.tableWidget.item(row,  TableCols.KRANK) is None:
            return False
        return self.tableWidget.item(row,  TableCols.KRANK).checkState() == Qt.Checked
        
    def getPrintHeader(self):
        #sK = str(self.klasseCombo.currentText) TODO
        sK = "Alle"
        if sK.lower() == "alle":
            return TableParams.PRINTE_LBL
        elif sK.startswith("5"):
            return TableParams.PRINTE5_LBL
        elif sK.startswith("6"):
            return TableParams.PRINTE6_LBL
        elif sK.startswith("7"):
            return TableParams.PRINTE7_LBL
        
    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)
        
    def getGermanDayName(self, ix):
        return ["Sonntag", "Montag", "Dienstag",  "Mittwoch", "Donnerstag", "Freitag",  "Samstag"][ix]

    def makeTableDocument(self):
        now = datetime.datetime.now()
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        rows = self.tableWidget.rowCount()
        tfmt = QtGui.QTextTableFormat()
        tfmt.setCellPadding(5.0)
        tfmt.setCellSpacing(-1)
        tfmt.setBorder(2)
        tfmt.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
        tfmt.setBorderBrush(QColor(0, 0,  0))
        cursor.insertText("Sportfest am " + self.getGermanDayName(int(now.strftime("%w"))) + ", den " + now.strftime("%d.%m.%Y") + "\n")
        cursor.movePosition(QtGui.QTextCursor.NextBlock)
        if self.sortFirstCombo.currentText() == "Punkte":
            cursor.insertText("Ausdruck: Platzierung " + self.filterFirstCombo.currentText() + " " + self.filterSecondCombo.currentText() + "\n\n")
        else:
            cursor.insertText("Ausdruck: " + self.filterFirstCombo.currentText() + " " + self.filterSecondCombo.currentText() + ", sortiert nach " + self.sortFirstCombo.currentText() + "/" + self.sortSecondCombo.currentText() + "\n\n")
        cursor.movePosition(QtGui.QTextCursor.NextBlock)
        cursor.movePosition(QtGui.QTextCursor.NextBlock)
        table = cursor.insertTable(rows + 1, 18,  tfmt)
        format = table.format()
        format.setHeaderRowCount(1)
        table.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QtGui.QFont.Bold)
        header = self.getPrintHeader()
        print(header)
        for c in range(0, 18):
            cursor.setCharFormat(format)
            cursor.insertText(header[c])
            cursor.movePosition(QtGui.QTextCursor.NextCell)
        aCen = QtGui.QTextBlockFormat()
        aCen.setAlignment(Qt.AlignCenter)
        for row in range(rows):
            if self.isRowKrank(row):
                continue
            cursor.insertText(str(row + 1))
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.NAME).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.VORNAME).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.KLASSE).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_V).text() + "s")
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_P).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRINT_N).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_V).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_P).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.LAUF_N).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_V).text() + "m")
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_P).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.SPRUNG_N).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_V).text() + "m")
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_P).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.WURF_N).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.insertText(self.tableWidget.item(row, TableCols.PUNKTE).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
            cursor.setBlockFormat(aCen)
            cursor.insertText(self.tableWidget.item(row, TableCols.NOTE).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)
        return document
        
    def getGeschlechtFromLong(self,  long):
        print(str(long).lower())
        if str(long).lower() == "alle schüler":
            return "Alle"
        elif str(long).lower() == "jungen":
            return "M"
        else:
            return "W"
    
    @pyqtSlot()
    def on_actionPPreview_triggered(self):
        """
        Zeigt die Druckvorschau an
        """
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.printer().setPageOrientation(QtGui.QPageLayout.Landscape)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    
    @pyqtSlot(str)
    def on_filterFirstCombo_currentIndexChanged(self, p0):
        """
        Aufgerufen wenn 1. Filter geändert wurde. Filtert die Daten neu
        
        @param p0 DESCRIPTION
        @type str
        """
        self.Filter2 = self.getGeschlechtFromLong(p0)
        self.fillTable(self.Filter1,  self.Filter2)
        self.resortData()
    
    @pyqtSlot(int)
    def on_filterSecondCombo_currentIndexChanged(self, index):
        """
        Aufgerufen wenn 2. Filter geändert wurde. Filtert die Daten neu
        
        @param index DESCRIPTION
        @type int
        """
        self.Filter1 = self.Klassen[index]
        self.fillTable(self.Filter1,  self.Filter2)
        self.resortData()
    
    @pyqtSlot()
    def on_actionRefreshData_triggered(self):
        """
        Aktualisiert die Daten aus dem Hauptfenster
        """
        if not self.par is None:
            self.par.syncToEval()
    
    @pyqtSlot()
    def on_actionRecalc_triggered(self):
        """
        Berechnet alle Punkte und Noten neu
        """
        if not self.par is None:
            self.par.calcAll()
            self.par.syncToEval()
            self.resortData()
    
    @pyqtSlot()
    def on_actionRePlace_triggered(self):
        """
        Sortiert die Daten neu (nach Punkten falls keine Sortierung ausgewählt ist)
        """
        self.par.syncToEval()
        if self.sortFirstCombo.currentIndex() == 0:
            self.sortFirstCombo.setCurrentIndex(1)
        self.resortData()
    
    @pyqtSlot()
    def on_actionDoPrint_triggered(self):
        """
        Druckt die Auswertungstabelle
        """
        dialog = QtPrintSupport.QPrintDialog()
        dialog.printer().setPageOrientation(QtGui.QPageLayout.Landscape)
        if dialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())
    
    @pyqtSlot()
    def on_actionClose_triggered(self):
        """
        Schließt das Auswertungsfenster
        """
        self.close()
        
    def getBereich(self):
        F1 = self.Filter1.lower() #Klasse
        F2 = self.Filter2.lower() #Geschlecht M W
        if F1 == "alle" and F2 == "alle":
            return "Gesamtsieger"
            
        if F1 == "alle":
            if F2 == "m":
                return "Gesamtsieger Jungen"
            else:
                return "Gesamtsieger Mädchen"
                
        if F2 == "alle":
            return "Gesamtsieger Klasse {}".format(self.Fiter1)
        elif F2 == "m":
            return "Sieger Jungen Klasse {}".format(self.Filter1)
        else:
            return "Sieger Mädchen Klasse {}".format(self.Filter1)
        
        
    @pyqtSlot()
    def on_actionUrkunde_triggered(self):
        """
        Slot documentation goes here.
        """
        path = self.pCfg.getTemplate()
        if path is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Es wurde noch keine Urkundenvorlage eingestellt! Um diese Funktion benutzen zu können müssen Sie zuerst eine Vorlage in den Einstellungen auswählen.")
            msg.setWindowTitle("FFSportfest - Urkundendruck")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if not os.path.isfile(path):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Die ausgewählte Urkundenvorlage wurde nicht gefunden - bitte überprüfen Sie ob die Datei verschoben wurde!")
            msg.setWindowTitle("FFSportfest - Urkundendruck")
            msg.setDetailedText("Ausgewählte Datei: " + str(path))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        self.tableWidget.sortItems(ETableCols.PUNKTE,  Qt.DescendingOrder)
        
        #PLACE_NUM = 3
        
        doc = DocxTemplate(path)
        
        now = datetime.datetime.now()
        context = { 'DATUM' : str(now.strftime("%A") + ", den " + now.strftime("%d.%m.%Y")), "BEREICH": self.getBereich() } 
        
        for plz in range(0, self.pCfg.getPlaceCount()):
            if not plz <= self.tableWidget.rowCount():
                print("Kein Schüler auf Platz {}".format(str(plz + 1)))
                continue
            if self.tableWidget.item(plz,  ETableCols.GESCHLECHT).text() == "W":
                context['TITEL_' + str(plz + 1)] = "die Schülerin"
            else:
                context['TITEL_' + str(plz + 1)] = "der Schüler"
            context['VORNAME_' + str(plz + 1)] = self.tableWidget.item(plz,  ETableCols.VORNAME).text()
            context['NACHNAME_' + str(plz + 1)] = self.tableWidget.item(plz,  ETableCols.NAME).text()
            context['PUNKTE_' + str(plz + 1)] = self.tableWidget.item(plz,  ETableCols.PUNKTE).text()
            context['NOTE_' + str(plz + 1)] = self.tableWidget.item(plz,  ETableCols.NOTE).text()
            context['KLASSE_' + str(plz + 1)] = self.tableWidget.item(plz,  ETableCols.KLASSE).text()
        
        doc.render(context)
        
        
        opts = QFileDialog.Options()
        name, _ = QFileDialog.getSaveFileName(self, "Datenbank speichern unter", os.path.join(self.pCfg.dlgPath(), "Urkunde-{}.docx".format(now.strftime("%d_%m_%Y-%H_%M_%S"))), "Word-Dokumente (*.docx)",  options=opts)
        if name:
            filename = str(name)
            if not filename.endswith(".docx"):
                filename+= ".docx"
            doc.save(filename)
            
            try:
                if sys.platform.startswith('darwin'):
                    subprocess.call(('open', filename))
                elif os.name == 'nt':
                    os.startfile(filename)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open', filename))
            except Exception:
                print("Fehler beim Öffnen der Datei!")
        
        self.resortData()

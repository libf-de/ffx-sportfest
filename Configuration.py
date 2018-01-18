from configparser import ConfigParser
from PyQt5.QtCore import Qt
from lib.Constants import TableCols
from lib.debug import Debug
import os,  sys

class Configuration:
    """ Enthält Funktionen um das Programm konfigurierbar zu machen """
    
    oExecPath = None
    ExecPath = None
    cnf = None
    cfgFilePath = None
    isPortable = False
    
    def storeExecutablePath(self,  prov):
        """
        Setzt die Variable, die den Pfad beinhaltet, von welchem das Programm ausgeführt wird
        @param prov: Manuelle Angabe des Pfades (für selbstentpackende Archive)
        """
        if not prov is None:
            upr = os.path.dirname(os.path.realpath(str(prov)))
            if os.path.exists(upr):
                self.ExecPath = upr
                Debug.d("CNF: Using provided executable Path: " + str(upr))
                return
            else:
                Debug.d("CNF: Provided executable Path does not exist: " + str(prov))
        
        if getattr( sys, 'frozen', False ):
            self.ExecPath = os.path.dirname(str(sys.executable))
            return
        self.ExecPath = os.path.dirname(str(__file__))
        return
    
    def getExecutablePath(self):
        """
        Ruft den  Pfad ab von welchem das Programm ausgeführt wird
        @return: Ausführungspfad
        """
        return self.ExecPath
        """if not self.oExecPath is None:
            if os.path.exists(self.oExecPath):
                Debug.d("CNF: Using provided executable Path: " + str(self.oExecPath))
                return os.path.dirname(str(self.oExecPath))
            else:
                Debug.d("CNF: Provided executable Path does not exist: " + str(self.oExecPath))
        
        if getattr( sys, 'frozen', False ):
            return os.path.dirname(str(sys.executable))
        return os.path.dirname(str(__file__))"""
        
    def getLocalDir(self):
        """
        Ruft den lokalen Konfigurationsorder ab und erstellt ihn ggf.
        @return: lokaler Konfigurationsordner
        """
        ff_dir = os.path.expanduser("~/.ffd")
        if not os.path.exists(ff_dir):
            os.makedirs(ff_dir)
        return ff_dir
            
    def createBlankConfig(self):
        """
        Erstellt eine neue Konfiguration mit den Standardwerten
        """
        self.cnf['GENERAL'] = {'load_last_db': False, 'last_db': '', 'create_backup_file': True,  'enable_file_recovery': False,  'ignore_non_participation': True,  'use_native_dialogs': True }
        self.cnf['EDITOR'] = { 'sort_instantly': True,  'reset_results': False,  'guess_gender': True }
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def getNativeDialogs(self):
        """
        Gibt zurück ob native Dialoge verwendet werden sollen
        @return Native Dialoge verweden
        """
        return self.cnf.getboolean('GENERAL',  'use_native_dialogs',  fallback=True)    
        
    def getGuessGender(self):
        """
        Gibt zurück ob das Geschlecht geraten werden soll
        @return Geschlecht raten
        """
        return self.cnf.getboolean('EDITOR',  'guess_gender',  fallback=True)    
        
    def setGuessGender(self,  enable):
        """
        Setzt ob das Geschlecht geraten werden soll
        @param enable: Geschlecht raten
        @type load: boolean
        """
        self.cnf['GENERAL']['guess_gender'] = bool(enable)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def getRecoverFile(self):
        """
        Gibt den Pfad für Wiederherstellungsdateien zurück (je nachdem ob Portabel oder Installiert ausgeführt)
        @return: Pfad für Wiederherstellungsdateien
        """
        if self.isPortable:
            return os.path.join(self.ExecPath, 'ffdrec.bak')
        else:
            return os.path.join(self.getLocalDir(), 'ffdrec.bak')
            
    def considerLoadDb(self):
        """
        Erwägt das Laden einer Datenbank für den portablen Modus. Hierzu muss in der portablen
        Konfigurationsdatei unter dem Abschnitt PORTABLE der zu ladende Dateiname unter der
        Option "load_db" angegeben werden.
        @return: Pfad der zu ladenden Datenbank oder FALSE
        """
        if not self.isPortable:
            return False
        
        if self.cnf.has_option('PORTABLE',  'load_db'):
            portDb = os.path.join(self.ExecPath, self.cnf.get('PORTABLE',  'load_db'))
            if os.path.isfile(portDb):
                return portDb
            else:
                return False
        else:
            return False
    
    def __init__(self,  execPath=None):
        """
        Initialisiert die Konfiguration (wählt Portable/Lokale Konfiguration und lädt/erstellt sie)
        """
        self.storeExecutablePath(execPath)
        portablePath = os.path.join(self.ExecPath, "ffd-config.ini")
        if os.path.isfile(portablePath):
            self.cfgFilePath = portablePath
            self.isPortable = True
        else:
            self.cfgFilePath = os.path.join(self.getLocalDir(),  "config.ini")
            
        self.cnf = ConfigParser()
        
        if not os.path.isfile(self.cfgFilePath):
            self.createBlankConfig()
        else:
            with open(self.cfgFilePath, 'r', encoding='utf-8') as f:
                self.cnf.read_file(f)
                
        print('Config: using file ' + self.cfgFilePath)
                
    def getLoadLastDb(self):
        """
        Gibt zurück ob zuletzt geöffnete Datenbank automatisch geöffnet werden soll
        @return Zuletzt geöffnet öffnen
        """
        return self.cnf.getboolean('GENERAL',  'load_last_db',  fallback=False)
        
    def getInstantSort(self):
        """
        Gibt zurück ob die Tabelle nach dem Bearbeiten sofort sortiert werden soll
        @return Sofort sortieren
        """
        return self.cnf.getboolean('EDITOR',  'sort_instantly',  fallback=True)
        
    def setInstantSort(self,  enable):
        """
        Setzt ob die Tabelle nach dem Bearbeiten sofort sortiert werden soll
        @param enable: Sofort sortieren
        @type load: boolean
        """
        self.cnf['EDITOR']['sort_instantly'] = bool(enable)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    #######################
    """
    Sortierabkürzungen:
    K = Klasse
    N = Nachname
    V = Vorname
    G = Geschlecht
    Standard: KNV
    """
    
    
    def getSortBy(self):
        """
        Gibt die Standard-Sortierreihenfolge zurück
        @return Sofort sortieren
        """
        return self.cnf.get('GENERAL',  'sort_by',  fallback="KNV")
        
    def setSortBy(self,  sortby):
        """
        Setzt die Standard-Sortierreihenfolge
        @param enable: Sortierreihenfolge
        @type load: boolean
        """
        self.cnf['GENERAL']['sort_by'] =str(sortby)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def doSortBy(self,  tableWidget):
        """
        Sortiert die übergebene Tabelle nach der Standard-Sortierreihenfolge
        @param tableWidget: zu sortierende Tabelle
        @type tableWidget: QTableWidget
        """
        sortBy = str(self.getSortBy())[::-1].lower()
        for k in sortBy:
            if k == "k":
                tableWidget.sortItems(TableCols.KLASSE,  Qt.AscendingOrder)
            elif k == "n":
                tableWidget.sortItems(TableCols.NAME,  Qt.AscendingOrder)
            elif k == "v":
                tableWidget.sortItems(TableCols.VORNAME,  Qt.AscendingOrder)
            elif k == "g":
                tableWidget.sortItems(TableCols.GESCHLECHT,  Qt.AscendingOrder)
            
###############################
    def getWipeResults(self):
        """
        Gibt zurück ob alle Ergebnisse beim Bearbeiten einer Datenbank gelöscht werden sollen
        @return Ergebnisse löschen
        """
        return self.cnf.getboolean('EDITOR',  'reset_results',  fallback=False)
        
    def setWipeResults(self,  enable):
        """
        Setzt ob alle Ergebnisse beim Bearbeiten einer Datenbank gelöscht werden sollen
        @param enable: Ergebnisse löschen
        @type load: boolean
        """
        self.cnf['EDITOR']['reset_results'] = bool(enable)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
        
    def getLastDb(self):
        """
        Gibt den Pfad der zuletzt geöffneten Datenbank an
        @return Pfad der zuletzt geöffneten Datenbank
        """
        return self.cnf.get('GENERAL',  'last_db', fallback=None)
        
    def getTemplate(self):
        """
        Gibt den Pfad zur Urkundenvorlage zurück
        @return Pfad der Vorlage
        """
        return self.cnf.get('GENERAL',  'template_path', fallback=None)
    
    def setTemplate(self, path):
        """
        Setzt den Pfad der Urkundenvorlage
        @param path: Pfad der Vorlage
        @type path: String
        """
        self.cnf['GENERAL']['template_path'] = path
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
        
    def getBackupFile(self):
        """
        Gibt zurück ob Dateien vor dem Öffnen gesichert werden sollen (in Dateiname~)
        @return Dateien vor Öffnen sichern
        """
        return self.cnf.getboolean('GENERAL',  'create_backup_file',  fallback=True)
        
    def setBackupFile(self,  enable):
        """
        Setzt ob Dateien vor dem Öffnen gesichert werden sollen (in Dateiname~)
        @param enable: Dateien vor Öffnen sichern
        @type load: boolean
        """
        self.cnf['GENERAL']['create_backup_file'] = bool(enable)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
        
    def getNonPart(self):
        """
        Gibt zurück ob Disziplinen, die nicht abgelegt wurden, in der Durchschnittsnote berücksichtigt werden sollen
        WAHR = Nicht teilgenommen entfernen
        FALSCH = Alle Disziplinen berücksichtigen (Nicht Teilgenommen = 6)
        @return Nicht-Teilnahme ignorieren
        """
        return self.cnf.getboolean('GENERAL',  'ignore_non_participation',  fallback=True)    
        
    def getRecovery(self):
        """
        Gibt zurück ob Wiederherstellungsdateien erstellt werden sollen (möglicherweise langsam!)
        @return Erstelle Wiederherstellungsdateien
        """
        return self.cnf.getboolean('GENERAL',  'enable_file_recovery',  fallback=False)
        
    def setRecovery(self,  enable):
        """
        Setzt ob Wiederherstellungsdateien erstellt werden sollen (möglicherweise langsam!)
        @param load: Erstelle Wiederherstellungsdateien
        @type load: boolean
        """
        self.cnf['GENERAL']['enable_file_recovery'] = bool(enable)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
        
    def setLoadLastDb(self,  load):
        """
        Setzt ob zuletzt geöffnete Datenbank beim Start geladen werden soll
        @param load: Zuletzt geöffnete Datenbank beim Start laden
        @type load: boolean
        """
        self.cnf['GENERAL']['load_last_db'] = bool(load)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def setLastDb(self,  path):
        """
        Setzt den Pfad der zuletzt geöffneten Datenbank
        @param path: Pfad der zuletzt geöffneten Datenbank
        @type path: String
        """
        self.cnf['GENERAL']['last_db'] = path
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def setNonPart(self,  ign):
        """
        Setzt ob Nicht-Teilnahme bei der Durchschnittsnote berücksichtigt werden soll
        @param ign: Ignorieren Ja/Nein
        @type ign: boolean
        """
        self.cnf['GENERAL']['ignore_non_participation'] = bool(ign)
        with open(self.cfgFilePath, 'w', encoding='utf-8') as configfile:
            self.cnf.write(configfile)
            
    def dlgPath(self):
        return os.path.expanduser("~")

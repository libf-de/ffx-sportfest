from PyQt5.QtGui import QColor

class TableCols:
    UID = 0
    NAME = 1
    VORNAME = 2
    GESCHLECHT = 3
    KLASSE = 4
    SPRINT_V = 5
    SPRINT_P = 6
    SPRINT_N = 7
    LAUF_V = 8
    LAUF_P = 9
    LAUF_N = 10
    SPRUNG_V = 11
    SPRUNG_P = 12
    SPRUNG_N = 13
    WURF_V = 14
    WURF_P = 15
    WURF_N = 16
    PUNKTE = 17
    NOTE = 18
    KRANK = 19
    
class ETableCols:
    UID = 0
    NAME = 1
    VORNAME = 2
    GESCHLECHT = 3
    KLASSE = 4
    SPRINT_V = 5
    SPRINT_P = 6
    SPRINT_N = 7
    LAUF_V = 8
    LAUF_P = 9
    LAUF_N = 10
    SPRUNG_V = 11
    SPRUNG_P = 12
    SPRUNG_N = 13
    WURF_V = 14
    WURF_P = 15
    WURF_N = 16
    PUNKTE = 17
    NOTE = 18
    KRANK = 19
    
class TableHide:
    UID = True
    NAME = False
    VORNAME = False
    GESCHLECHT = False
    KLASSE = False
    SPRINT_V = False
    SPRINT_P = True
    SPRINT_N = True
    LAUF_V = False
    LAUF_P = True
    LAUF_N = True
    SPRUNG_V = False
    SPRUNG_P = True
    SPRUNG_N = True
    WURF_V = False
    WURF_P = True
    WURF_N = True
    PUNKTE = False
    NOTE = False
    KRANK = False
    
class TableColors:
    NORMAL = QColor(255, 255, 255)
    MISSING = QColor(255, 0,  0)
    DISABLE = QColor(146, 146, 146)
    
class TableParams:
    CHECK_COLS = [ TableCols.SPRINT_V,  TableCols.LAUF_V, TableCols.SPRUNG_V,  TableCols.WURF_V ]
    HEADER_LBL = [ "UID", "Name",  "Vorname",  "Geschl.",  "Klasse",  "Sprint",  "Sprint (Pkt)",  "Sprint (Note)",  "Lauf", "Lauf (Pkt)",  "Lauf (Note)",   "Sprung", "Sprung (Pkt)", "Sprung (Note)",  "Wurf/Stoß",  "W/S (Pkt)",  "W/S (Note)",  "Punkte", "Ø Note",  "Krank"]
    PRINTM_LBL = [ "Name",  "Vorname",  "Klasse",  "Sprint",  "Pkt",  "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wu/St",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM5_LBL = [ "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM6_LBL = [ "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM7_LBL = [ "Name",  "Vorname",  "Klasse",  "75m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Stoß",  "Pkt", "Nt",  "Punkte",  "Note"]
    
    PRINTE_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "Sprint",  "Pkt",  "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wu/St",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE5_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE6_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE7_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "75m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Stoß",  "Pkt", "Nt",  "Punkte",  "Note"]

class FFSportfest:
    VERSION =  "a0.1"
    CODENAME = "Test Release"

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
    UID = True #0
    NAME = False #1
    VORNAME = False #2
    GESCHLECHT = False #3
    KLASSE = False #4
    SPRINT_V = False #5
    SPRINT_P = True #6
    SPRINT_N = True #7
    LAUF_V = False #8
    LAUF_P = True #9
    LAUF_N = True #10
    SPRUNG_V = False #11
    SPRUNG_P = True #12
    SPRUNG_N = True #13
    WURF_V = False #14
    WURF_P = True #15
    WURF_N = True #16
    PUNKTE = False #17
    NOTE = False #18
    KRANK = False #19
    INDEXES = [1,  2,  3,  4,  5, 8, 11,  14,  17,  18,  19] #Sichtbare Spalten-Indexes
    
class TableColors:
    NORMAL = QColor(255, 255, 255)
    MISSING = QColor(255, 0,  0)
    DISABLE = QColor(146, 146, 146)
    
class TableParams:
    CHECK_COLS = [ TableCols.SPRINT_V,  TableCols.LAUF_V, TableCols.SPRUNG_V,  TableCols.WURF_V ]
    HEADER_LBL = [ "UID", "Name",  "Vorname",  "⚤",  "Klasse",  "Sprint",  "Sprint (Pkt)",  "Sprint (Note)",  "Lauf", "Lauf (Pkt)",  "Lauf (Note)",   "Sprung", "Sprung (Pkt)", "Sprung (Note)",  "Wurf/Stoß",  "W/S (Pkt)",  "W/S (Note)",  "Punkte", "Ø Note",  "Krank"]
    HEADER56_LBL = [ "UID", "Name",  "Vorname",  "⚤",  "Klasse",  "Sprint",  "Sprint (Pkt)",  "Sprint (Note)",  "Lauf", "Lauf (Pkt)",  "Lauf (Note)",   "Sprung", "Sprung (Pkt)", "Sprung (Note)",  "Wurf",  "Wurf (Pkt)",  "Wurf (Note)",  "Punkte", "Ø Note",  "Krank"]
    HEADER7_LBL = [ "UID", "Name",  "Vorname",  "⚤",  "Klasse",  "Sprint",  "Sprint (Pkt)",  "Sprint (Note)",  "Lauf", "Lauf (Pkt)",  "Lauf (Note)",   "Sprung", "Sprung (Pkt)", "Sprung (Note)",  "Stoß",  "Stoß (Pkt)",  "Stoß (Note)",  "Punkte", "Ø Note",  "Krank"]
    PRINTM_LBL = [ "Name",  "Vorname",  "Klasse",  "Sprint",  "Pkt",  "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wu/St",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM5_LBL = [ "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM6_LBL = [ "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTM7_LBL = [ "Name",  "Vorname",  "Klasse",  "75m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Stoß",  "Pkt", "Nt",  "Punkte",  "Note"]
    
    PRINTE_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "Sprint",  "Pkt",  "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wu/St",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE5_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE6_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "50m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Wurf",  "Pkt", "Nt",  "Punkte",  "Note"]
    PRINTE7_LBL = [ "#", "Name",  "Vorname",  "Klasse",  "75m Sp",  "Pkt", "Nt",  "Lauf",  "Pkt", "Nt",  "Sprung",  "Pkt", "Nt",  "Stoß",  "Pkt", "Nt",  "Punkte",  "Note"]

class FFSportfest:
    VERSION =  "0.2 BM"
    CODENAME = "Beta (Master)"

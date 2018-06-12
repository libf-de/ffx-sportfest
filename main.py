# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication,  QSplashScreen, QMessageBox
from PyQt5.QtCore import QTranslator,  QLibraryInfo,  Qt
from PyQt5.QtGui import QPixmap, QPainter,  QFont,  QColor
from ui.MainForm import MainWindow
if __name__ == "__main__":
    import sys,  argparse
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        
    app = QApplication(sys.argv)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--execpath',  action='store',  dest='uexecpath',  help='Ausführungspfad überschreiben')
    parser.add_argument('--nosplash',  action='store_false',  dest='splash',  help='Kein Ladebildschirm')
    parser.add_argument('filename', help='Datenbank laden',  nargs='?')
    
    results = parser.parse_args()
    
    print("*****************************************")
    print("* > FFSportfest lädt, bitte warten...")
    print("*****************************************")
    print(" ")
    
    # Create and display the splash screen
    splash = None
    if results.splash:
        splash_pix = QPixmap('splash.png')
        font = QFont()
        font.setPointSizeF(12)
        painter = QPainter()
        painter.begin(splash_pix)
        painter.setFont(font)
        painter.setPen(QColor(255,  255, 255))
        painter.drawText(210,  110, "Version 0.2BM")
        painter.end()
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()
    
    qtTranslator = QTranslator(app)
    lpath = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    print(lpath)
    if qtTranslator.load("qtbase_de",  lpath):
        app.installTranslator(qtTranslator)
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Die deutschen Sprachdateien konnten nicht gefunden werden! Teile des Programms sind eventuell nicht vollständig übersetzt.")
        msg.setWindowTitle("FFSportfest - Sprachdateien")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
    
    ui = MainWindow(results, splash)
    ui.show()
    sys.exit(app.exec_())

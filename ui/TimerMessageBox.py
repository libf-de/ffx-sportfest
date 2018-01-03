from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
class TimerMessageBox(QMessageBox):
    """
    Erzeugt eine Meldung und schließt sie automatisch nach x Sekunden
    Quelle: https://stackoverflow.com/questions/40932639/pyqt-messagebox-automatically-closing-after-few-seconds
    @param timeout Zeit bis zum Schließen
    """
    def __init__(self, timeout=3, parent=None,  backfocus=False):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("Ungültige Eingabe")
        self.time_to_wait = timeout
        self.setInformativeText("Meldung schließt sich in {0} Sekunden...".format(timeout))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()
        
        if backfocus:
            if not parent is None:
                parent.setFocus()
        

    def changeContent(self):
        self.time_to_wait -= 1
        self.setInformativeText("Meldung schließt sich in {0} Sekunden...".format(self.time_to_wait))
        if self.time_to_wait <= 0:
            self.close()
            
    def closeDlg(self):
        self.timer.stop()
        self.accept()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

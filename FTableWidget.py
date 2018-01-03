#from PyQt4.QtGui import QTableWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import pyqtSignal,  Qt

class FTableWidget(QTableWidget):
    
    ignoredKeys = [ Qt.Key_Return,  Qt.Key_Enter,  Qt.Key_Tab]
    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        self.parent = parent
        super(FTableWidget, self).__init__(parent)
        
    def setIgnoredKeys(self,  ignore):
        self.ignoredKeys = ignore
    
    def getIgnoredKeys(self):
        return self.ignoredKeys
        
    def keyPressEvent(self, event):
        self.keyPressed.emit(event.key());
        if event.key() not in self.ignoredKeys:
            super(FTableWidget, self).keyPressEvent(event)

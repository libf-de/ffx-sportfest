from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore
class FTableWidgetItem (QTableWidgetItem):
    def __init__ (self, value):
        super(FTableWidgetItem, self).__init__(str(value))

    def __lt__ (self, other):
        if (isinstance(other, FTableWidgetItem)):
            selfDataValue  = float(str(self.data(QtCore.Qt.EditRole)))
            otherDataValue = float(str(other.data(QtCore.Qt.EditRole)))
            return selfDataValue < otherDataValue
        else:
            return QTableWidgetItem.__lt__(self, other)

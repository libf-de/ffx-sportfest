from PyQt5.QtWidgets import QItemDelegate, QLineEdit
from PyQt5.QtGui import QDoubleValidator,  QRegExpValidator,  QValidator
from PyQt5.QtCore import QRegExp
import math, string,  re
class NumDelegate(QItemDelegate):

  def __init__(self, parent=None):
    super(NumDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    le = QLineEdit(parent);
    vl = QDoubleValidator()
    le.setValidator(vl)
    return le
    
class TimeDelegate(QItemDelegate):

  def __init__(self, parent=None):
    super(TimeDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    le = QLineEdit(parent);
    rex = QRegExp('^([0-9]|[0-5][0-9]):[0-5][0-9]$')
    vl = QRegExpValidator(rex)
    le.setValidator(vl)
    return le
    
class GeschlechtDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(GeschlechtDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        self.le = QLineEdit(parent);
        rex = QRegExp('^([Mm]|[Ww])$')
        vl = QRegExpValidator(rex)
        self.le.setValidator(vl)
        self.le.textEdited.connect(self.makeupper)
        return self.le
    
    def makeupper(self,  text):
        self.le.setText(text.upper())
        
class KlasseDelegate(QItemDelegate):

  def __init__(self, parent=None):
    super(KlasseDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    le = QLineEdit(parent);
    rex = QRegExp('^([0-9]{1,2})\.([0-9]{1})$')
    vl = QRegExpValidator(rex)
    le.setValidator(vl)
    return le
    
class NonEmptyDelegate(QItemDelegate):

  def __init__(self, parent=None):
    super(NonEmptyDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    le = QLineEdit(parent);
    rex = QRegExp('/.*\S.*/')
    vl = QRegExpValidator(rex)
    le.setValidator(vl)
    return le
    
class ReadonlyDelegate(QItemDelegate):

  def __init__(self, parent=None):
    super(ReadonlyDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    le = QLineEdit(parent);
    le.setReadOnly(True)
    return le

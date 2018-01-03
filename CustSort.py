from PyQt5.QtGui import *
from enum import Enum

"""
Class for sorting columns
Stored dictionary of sorted columns and theirs sort order "m_sortedColumns"
and list of sorted columns to simple handling order of sorting columns
"""
class ColumnsSorter:

    
    m_sortedColumns = {}
    m_sortedColumnsOrder = []
    m_ascIcon = None
    m_descIcon = None

    def __init__(self):
        print("INIT")

    def setIcons(self,  ascIcon,  descIcon):
        self.m_ascIcon = ascIcon
        self.m_descIcon = descIcon

    def sortColumn(self,  column,  isModifierPressed = False):
        """
        // If key modifier to multicolumn sorting is pressed
        // and column was sorted and nedded to sort only this column,
        // i.e. before user click at this column header was sorted only
        // this column, than we simple should change sort order of column.
        // Else we should clear all sorted columns and sort current
        // by defult sort order (ascending)
        """
        if not isModifierPressed:
            if (column in self.m_sortedColumns) and (len( self.m_sortedColumns ) == 1):
                self.changeSortOrder( column )
            else:
                self.clearSortedColumns()
                self.addSortedColumn( column );
        else:
            if column in self.m_sortedColumns:
                self.changeSortOrder( column )
            else:
                self.addSortedColumn( column )
                
    # Return column index
    def columnIndex(self,  columnOrder):
        return self.m_sortedColumnsOrder[columnOrder]
        
    def columnOrder(self,  column):
        return self.m_sortedColumnsOrder.index( column )
        
    def columnSortOrder(self,  column):
        return self.m_sortedColumns.get( column );
    
    def columnIcon(self,  column):
        columnIcon = None;
        if column in self.m_sortedColumns:
            if self.m_sortedColumns.get(column) == Qt.AscendingOrder:
                columnIcon = self.m_ascIcon
            else:
                columnIcon = self.m_descIcon
        return columnIcon
    
    def columnsCount(self):
        return len( self.m_sortedColumnsOrder )
        
    def addSortedColumn(self,  column):
        self.m_sortedColumns[ column ] = Qt.AscendingOrder
        self.m_sortedColumnsOrder.insert(len(self.m_sortedColumnsOrder, column))
        
    def changeSortOrder(self,  column):
        if self.m_sortedColumns[column] == Qt.AscendingOrder:
            self.m_sortedColumns[column] = Qt.DescendingOrder
        else:
            self.m_sortedColumns[column] = Qt.AscendingOrder
    
    def clearSortedColumns(self):
        self.m_sortedColumns.clear()
        self.m_sortedColumnsOrder.clear()
        
class AlphanumSortProxyModel(QtGui.QSortFilterProxyModel):
    def kappa(self):
        print("KAPPA")

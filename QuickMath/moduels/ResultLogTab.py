from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *

import os

class ResultLogTab(QWidget):
    def __init__(self, parent, conn, preferenceTableName):
        super(ResultLogTab, self).__init__(parent)
        self.mainWindow = parent
        self.conn = conn
        self.preferenceTableName = preferenceTableName
        self.initGui()
        self.connectSlots()
        self.initValues()

    def initGui(self):

        self.historyTextEdit = QPlainTextEdit()
        self.masterLayout = QVBoxLayout()

    def connectSlots(self):
        pass

    def initValues(self):
        self.masterLayout.addWidget(self.historyTextEdit)
        self.setLayout(self.masterLayout)

    def print(self, text):
        cursor = self.historyTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.historyTextEdit.setTextCursor(cursor)
        self.historyTextEdit.ensureCursorVisible()

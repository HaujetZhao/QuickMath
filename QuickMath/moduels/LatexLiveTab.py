from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView


class LatexLiveTab(QWidget):
    def __init__(self, parent):
        super(LatexLiveTab, self).__init__(parent)
        self.mainWindow = parent
        self.initGui()
        self.initValues()

    def initGui(self):
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()

    def initValues(self):
        self.browser.load(QUrl('https://www.latexlive.com'))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)

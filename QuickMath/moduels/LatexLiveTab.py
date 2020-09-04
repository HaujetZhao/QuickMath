from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView


class LatexLiveTab(QWebEngineView):
    def __init__(self, parent):
        super(LatexLiveTab, self).__init__(parent)
        self.mainWindow = parent

        self.load(QUrl('https://www.latexlive.com'))

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        actions = menu.actions()
        menu.popup(event.globalPos())

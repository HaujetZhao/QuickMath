from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


class LatexLiveTab(QWebEngineView):
    def __init__(self, parent):
        super(LatexLiveTab, self).__init__(parent)
        self.mainWindow = parent
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanPaste, True)

        self.load(QUrl('https://www.latexlive.com'))


        self.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanPaste, True)

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        actions = menu.actions()
        menu.popup(event.globalPos())

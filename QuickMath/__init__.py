import os
import sys
import platform
import sqlite3

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *

try:
    from moduels.SystemTray import SystemTray # 引入托盘栏
    from moduels.QuickMathTab import QuickMathTab # 引入书写界面的 tab
    from moduels.ConfigTab import ConfigTab # 引入设置界面的 tab
    from moduels.ResultLogTab import ResultLogTab # 引入历史记录界面的 tab
    from moduels.LatexLiveTab import LatexLiveTab # 引入LatexLive界面的 tab
    from moduels.HelpTab import HelpTab # 引入帮助界面界面的 tab
except:
    from QuickMath.moduels.SystemTray import SystemTray # 引入托盘栏
    from QuickMath.moduels.QuickMathTab import QuickMathTab # 引入书写界面的 tab
    from QuickMath.moduels.ConfigTab import ConfigTab # 引入设置界面的 tab
    from QuickMath.moduels.ResultLogTab import ResultLogTab # 引入历史记录界面的 tab
    from QuickMath.moduels.LatexLiveTab import LatexLiveTab # 引入LatexLive界面的 tab
    from QuickMath.moduels.HelpTab import HelpTab # 引入帮助界面界面的 tab


os.chdir(os.path.dirname(os.path.abspath(__file__)))
dbname = './database.db'  # 存储预设的数据库名字
preferenceTableName = 'preference'
styleFile = './style.css'
version = 'V1.3.1'
conn = sqlite3.connect(dbname)
platfm = platform.system()



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(False)
        self.windowTitle = 'Quick Math'
        self.initGui()
        self.initValue()
        self.show()
        self.resizePixmap()

        # self.loadStyleSheet()
        # self.status = self.statusBar() # 状态栏

        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initGui(self):
        # 定义中心控件为多 tab 控件
        self.tabs = QTabWidget()


        # 定义多个不同功能的 tab
        self.quickMathTab = QuickMathTab(self, conn, preferenceTableName)  # 主要功能的 tab
        self.configTab = ConfigTab(self, conn, preferenceTableName)  # 设置界面
        self.resultLogTab = ResultLogTab(self, conn, preferenceTableName)  # 历史记录界面
        self.latexLiveTab = LatexLiveTab(self)  # latexlive界面
        self.helpTab = HelpTab(version, platfm)  # 帮助界面
        #

        # self.adjustSize()

        self.setWindowFlag(Qt.WindowStaysOnTopHint) # 始终在前台



    def initValue(self):
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(self.quickMathTab, self.tr('QuickMath'))
        self.tabs.addTab(self.configTab, self.tr('设置'))
        self.tabs.addTab(self.resultLogTab, self.tr('记录'))
        self.tabs.addTab(self.latexLiveTab, self.tr('LatexLive'))
        self.tabs.addTab(self.helpTab, self.tr('帮助'))
        # # self.tabs.addTab(self.helpTab, self.tr('帮助'))

        # 设置图标
        if platfm == 'Windows':
            self.setWindowIcon(QIcon('icon.ico'))
        else:
            self.setWindowIcon(QIcon('icon.icns'))
        self.setWindowTitle(self.windowTitle)




    def resizeEvent(self, event):
        self.resizePixmap()

    def resizePixmap(self):
        self.originPixMap = self.quickMathTab.pix
        newWidth = self.quickMathTab.size().width()
        newHeight = self.quickMathTab.size().height()

        # 需要在这里调整 QuickMathTab 的画布大小，并且还要保持上面原来的图像不变。
        origin = self.quickMathTab.pix
        self.quickMathTab.pix = QPixmap(newWidth, newHeight)
        self.quickMathTab.pix.fill(Qt.white)
        self.quickMathTab.paint(origin)
        # 就在这一步, 我不知道如何将 origin 画到 self.quickMathTab.pix 这个 QPixmap 上



    def loadStyleSheet(self):
        pass
        global styleFile
        try:
            try:
                with open(styleFile, 'r', encoding='utf-8') as style:
                    self.setStyleSheet(style.read())
            except:
                with open(styleFile, 'r', encoding='gbk') as style:
                    self.setStyleSheet(style.read())
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件根目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()
        elif (event.key() == Qt.Key_Escape):
            self.quickMathTab.clearPixmap()
        elif (event.key() == Qt.Key_Enter):
            self.quickMathTab.recognize()


    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if mainWindow.configTab.hideToSystemTraySwitch.isChecked():
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
        pass


def createDB():
    cursor = conn.cursor()
    result = cursor.execute('''select * from sqlite_master where name = '%s' ''' % preferenceTableName)
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                id integer primary key autoincrement,
                                item text,
                                value text
                                )''' % preferenceTableName)
        conn.commit()
    pass

def main():
    global mainWindow
    createDB()  # 初始化数据库
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # 设定托盘图标
    if platfm == 'Windows':
        tray = SystemTray(QIcon('icon.ico'), mainWindow)
    else:
        tray = SystemTray(QIcon('icon.icns'), mainWindow)
    os.environ['PATH'] += os.pathsep + os.getcwd()  # 将当前目录加入环境变量

    sys.exit(app.exec_()) # 进入程序主循环
    conn.close()  # 退出软件后关闭数据库连接

if __name__ == '__main__':

    main()
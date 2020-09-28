import os
import sqlite3
import json
import time
import threading

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

try:
    from moduels import MathpixAPI
    from moduels import LatexLiveAPI
except:
    from QuickMath.moduels import MathpixAPI
    from QuickMath.moduels import LatexLiveAPI


class QuickMathTab(QWidget):
    def __init__(self, parent, conn, preferenceTableName):
        super(QuickMathTab, self).__init__(parent)
        self.appid = 'xxxxxx'
        self.appkey = 'xxxxxx'
        self.conn = conn
        self.clipboard = QClipboard()
        self.mainWindow = parent
        self.preferenceTableName = preferenceTableName
        self.pix = QPixmap()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.lines = []
        self.允许鼠标事件通过 = True
        self.触摸位移优化 = True
        self.第一次触摸按下 = True
        self.initGui()
        self.connectSlots()
        self.initValue()



    def initGui(self):
        self.setWindowTitle("绘图应用")
        self.resize(640, 480)
        self.pix = QPixmap(640, 480)
        self.clearButton = QPushButton('清空(Esc)')
        self.recognizeButton = QPushButton('识别(Enter)')
        self.vlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()

    def connectSlots(self):
        self.clearButton.clicked.connect(self.clearPixmap)
        self.recognizeButton.clicked.connect(self.recognize)

    def initValue(self):
        # 画布背景设为白色
        self.pix.fill(Qt.white)
        self.hlayout.addWidget(self.clearButton)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.recognizeButton)
        self.vlayout.addStretch(1)
        self.vlayout.addLayout(self.hlayout)
        self.setLayout(self.vlayout)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

    def paintEvent(self, event):
        painter = QPainter(self.pix)
        pen = QPen(Qt.black, self.mainWindow.configTab.penLineWidthSpinbox.value(), Qt.SolidLine)
        painter.setPen(pen)
        # 根据鼠标指针前后两个位置绘制直线
        for line in self.lines:
            painter.drawLine(line)
        # 让前一个坐标值等于后一个坐标值，
        # 这样就能实现画出连续的线
        self.lastPoint = self.endPoint
        self.paint(self.pix)

    def mousePressEvent(self, event):
        if self.允许鼠标事件通过 and event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            # print(event.pos())

    def mouseMoveEvent(self, event):
        if self.允许鼠标事件通过 and event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos()
            self.lines.append(QLine(self.lastPoint, self.endPoint))
            self.lastPoint = self.endPoint
            self.update()

    def mouseReleaseEvent(self, event):
        # 鼠标左键释放

        if self.允许鼠标事件通过 and event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            self.lines.append(QLine(self.lastPoint, self.endPoint))
            self.lastPoint = self.endPoint
            # 进行重新绘制
            self.update()

    def paint(self, pixmap):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, pixmap)

    def clearPixmap(self):
        self.lines = []
        self.pix.fill(Qt.white)
        self.update()


    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.TouchUpdate:
            self.触摸点移动(event)
        elif event.type() == QEvent.Type.TouchBegin:
            self.允许鼠标事件通过 = False
            self.触摸点按下(event)
        elif event.type() == QEvent.Type.TouchEnd:
            self.触摸点松开(event)
            threading.Thread(target=self.放开鼠标限制).start()
        return super().eventFilter(watched, event)

    def 放开鼠标限制(self):
        time.sleep(0.05)
        self.允许鼠标事件通过 = True

    def 触摸点按下(self, event):
        if self.触摸位移优化 and self.第一次触摸按下:
            # print('触摸按下，触摸位移优化：True，第一次触摸按下：True')
            self.第一次触摸按下 = False
            self.第一次按下的坐标 = event.touchPoints()[0].pos().toPoint()
        elif self.触摸位移优化:
            当前坐标 = event.touchPoints()[0].pos().toPoint()
            当前坐标x = 当前坐标.x()
            当前坐标y = 当前坐标.y()
            self.x轴偏移校正值 = 当前坐标x - self.第一次按下的坐标.x()
            self.y轴偏移校正值 = 当前坐标y - self.第一次按下的坐标.y()
            正确坐标值 = QPoint(当前坐标x, 当前坐标y)
            # 正确坐标值 = QPoint(当前坐标x - self.x轴偏移校正值, 当前坐标y - self.y轴偏移校正值)
            self.lastPoint = 正确坐标值
            # print(f'触摸按下，原始坐标：{当前坐标}, 正确坐标{正确坐标值}')
        else:
            # print('触摸按下，触摸位移优化：False')
            self.lastPoint = event.touchPoints()[0].pos().toPoint()
        # print(f'触摸点按下，坐标是 {正确坐标值}')

    def 触摸点移动(self, event):
        if self.触摸位移优化:
            当前坐标 = event.touchPoints()[0].pos().toPoint()
            self.endPoint = QPoint(当前坐标.x() + self.x轴偏移校正值, 当前坐标.y() + self.y轴偏移校正值)
            # print(f'点移动，原坐标：{当前坐标}, 正确坐标{self.endPoint}')
        else:
            self.endPoint = event.touchPoints()[0].pos().toPoint()
            # print(f'点移动，原坐标：{self.endPoint}')
        # print(f'点移动，坐标是 {event.touchPoints()[0].pos().toPoint()}')
        self.lines.append(QLine(self.lastPoint, self.endPoint))
        self.lastPoint = self.endPoint
        self.update()

    def 触摸点松开(self, event):
        self.第一次触摸按下 = True
        if self.触摸位移优化:
            当前坐标 = event.touchPoints()[0].pos().toPoint()
            self.endPoint = QPoint(当前坐标.x() + self.x轴偏移校正值, 当前坐标.y() + self.y轴偏移校正值)
            # print(f'点移动，原坐标：{当前坐标}, 正确坐标{self.endPoint}')
        else:
            self.endPoint = event.touchPoints()[0].pos().toPoint()
        self.lines.append(QLine(self.lastPoint, self.endPoint))
        self.lastPoint = self.endPoint
        self.update()

    def recognize(self):
        self.recognizeButton.setEnabled(False)
        self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别中')
        imagePath = './image.png'
        image = self.pix.save('./image.png', 'png')
        if self.mainWindow.configTab.mathpixApiMethodRadioButton.isChecked():
            result = MathpixAPI.recognizePixmap(imagePath, self.appid, self.appkey) # 获得识别结果
            self.mainWindow.resultLogTab.print(result + '\n\n') # 不管结果如何，先将其打印到历史记录框
            if 'error' in result:
                self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别失败，请查看记录')
            else:
                self.clipboard.setText(json.loads(result)['latex_simplified'])

                self.mainWindow.configTab.apiUsageSpinbox.setValue(self.mainWindow.configTab.apiUsageSpinbox.value() + 1) # 统计次数加1
                # print(self.mainWindow.configTab.apiUsageSpinbox.value()) # 统计次数加1
                self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别完成，已复制')
        elif self.mainWindow.configTab.latexLiveMethodRadioButton.isChecked(): # 使用 妈咪叔的 LatexLive 接口进行识别
            result = LatexLiveAPI.recognizePixmap(imagePath)  # 获得识别结果
            self.mainWindow.resultLogTab.print(result + '\n\n') # 不管结果如何，先将其打印到历史记录框
            if 'latex_styled' not in result:
                self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别失败，请查看记录')
            else:
                self.clipboard.setText(json.loads(result)['latex_styled'])
                self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别完成，已复制')
        self.recognizeButton.setEnabled(True)
        if self.mainWindow.configTab.clearPixmapWhenFinishedSwitch.isChecked():
            self.clearPixmap()
        if self.mainWindow.configTab.hideToTaskBarWhenFinishedSwitch.isChecked():
            self.mainWindow.showMinimized()
        if self.mainWindow.configTab.hideToSystemTrayWhenFinishedSwitch.isChecked():
            self.mainWindow.hide()










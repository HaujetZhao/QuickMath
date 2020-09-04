import os
import sqlite3
import json

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

try:
    from moduels import MathpixAPI
except:
    from QuickMath.moduels import MathpixAPI


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
        self.initGui()
        self.connectSlots()
        self.initValue()


    def initGui(self):

        self.setWindowTitle("绘图应用")

        self.resize(500, 500)
        self.pix = QPixmap(500, 500)
        # print()
        # self.pix = QPixmap(self.mainWindow.size().width(), self.mainWindow.size().height())

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
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos()
            self.lines.append(QLine(self.lastPoint, self.endPoint))
            self.lastPoint = self.endPoint
            self.update()

    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
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

    def recognize(self):
        self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别中')
        imagePath = './image.jpg'
        image = self.pix.save('./image.jpg', 'jpeg')
        result = MathpixAPI.recognizePixmap(imagePath, self.appid, self.appkey) # 获得识别结果
        # 这里就得到了识别的结果, 大概长这样:
        # {
        #     "detection_list": [],
        #     "detection_map": {
        #         "contains_chart": 0,
        #         "contains_diagram": 0.0001,
        #         "contains_graph": 0.0002,
        #         "contains_table": 0,
        #         "is_blank": 0.0005,
        #         "is_inverted": 0,
        #         "is_not_math": 0.0005,
        #         "is_printed": 0.0008
        #     },
        #     "latex_confidence": 0.7462203502655029,
        #     "latex_confidence_rate": 0.9728515625,
        #     "latex_simplified": "\\sqrt { 2 } \\times 6 = y",
        #     "latex_styled": "\\sqrt{2} \\times 6=y",
        #     "position": {
        #         "height": 335,
        #         "top_left_x": 0,
        #         "top_left_y": 0,
        #         "width": 545
        #     },
        #     "request_id": "71645984d2e2d742c4a24a834b0e6f29",
        #     "text": "$\\sqrt{2} \\times 6=y$"
        # }

        self.mainWindow.resultLogTab.print(result.replace('\\\\', '\\') + '\n\n\n')
        if 'error' in result:
            self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别失败，请查看记录')
        else:
            self.clipboard.setText(json.loads(result)['latex_simplified'].replace('\\\\', '\\'))

            self.mainWindow.configTab.apiUsageSpinbox.setValue(self.mainWindow.configTab.apiUsageSpinbox.value() + 1) # 统计次数加1
            # print(self.mainWindow.configTab.apiUsageSpinbox.value()) # 统计次数加1
            self.mainWindow.setWindowTitle(self.mainWindow.windowTitle + '   识别完成，已复制')
        if self.mainWindow.configTab.clearPixmapWhenFinishedSwitch.isChecked():
            self.clearPixmap()
        if self.mainWindow.configTab.hideToTaskBarWhenFinishedSwitch.isChecked():
            self.mainWindow.showMinimized()
        if self.mainWindow.configTab.hideToSystemTrayWhenFinishedSwitch.isChecked():
            self.mainWindow.hide()









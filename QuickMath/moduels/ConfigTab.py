from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *

import os

class ConfigTab(QWidget):
    def __init__(self, parent, conn, preferenceTableName):
        super(ConfigTab, self).__init__(parent)
        self.mainWindow = parent
        self.conn = conn
        self.preferenceTableName = preferenceTableName
        self.initGui()
        self.connectSlots()
        self.initValues()


    def initGui(self):

        self.hideToSystemTraySwitch = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
        self.alwaysForegroundSwitch = QCheckBox(self.tr('始终前台'))
        self.clearPixmapWhenFinishedSwitch = QCheckBox(self.tr('识别完成后清空画布'))


        self.doNotHideWhenFinishedSwitch = QRadioButton(self.tr('识别后不要最小化'))
        self.hideToTaskBarWhenFinishedSwitch = QRadioButton(self.tr('识别后最小化'))
        self.hideToSystemTrayWhenFinishedSwitch = QRadioButton(self.tr('识别后隐藏到托盘'))
        self.boxLayoutForHideOptionsWhenFinished = QHBoxLayout()
        self.boxForHideOptionsWhenFinished = QWidget()

        self.penLineWidthHint = QLabel('画笔宽度：')
        self.penLineWidthSpinbox = QSpinBox()
        self.penLineWidthBox = QHBoxLayout()

        self.apiUsageHint = QLabel('API 已使用次数：')
        self.apiUsageSpinbox = QSpinBox()
        self.apiUsageBox = QHBoxLayout()

        self.resultStyleHint = QLabel('结果样式：')
        self.resultStyleComboBox = QComboBox()
        self.boxForResultStyle = QHBoxLayout()

        self.boxLayoutForChooseMethod = QHBoxLayout()
        self.boxForChooseMethod = QWidget()
        self.chooseMethodHint = QLabel('识别方法：')
        self.mathpixApiMethodRadioButton = QRadioButton('使用 Mathpix Api')
        self.latexLiveMethodRadioButton = QRadioButton('使用 LatexLive')


        self.preferenceGroupLayout = QVBoxLayout()

        self.preferenceGroup = QGroupBox(self.tr('偏好设置'))

        self.appidHint = QLabel("App ID：")
        self.appidBox = QLineEdit()
        self.appkeyHint = QLabel("App Key：")
        self.appkeyBox = QLineEdit()

        self.apiFromBox = QFormLayout()

        self.saveApiButton = QPushButton('保存 API 设置')

        self.apiGroup = QGroupBox(self.tr('Mathpix API 设置'))

        self.masterLayout = QVBoxLayout()


    def initValues(self):


        self.boxLayoutForHideOptionsWhenFinished.addWidget(self.doNotHideWhenFinishedSwitch)
        self.boxLayoutForHideOptionsWhenFinished.addWidget(self.hideToTaskBarWhenFinishedSwitch)
        self.boxLayoutForHideOptionsWhenFinished.addWidget(self.hideToSystemTrayWhenFinishedSwitch)
        self.boxLayoutForHideOptionsWhenFinished.setContentsMargins(0,0,0,0)
        self.boxForHideOptionsWhenFinished.setContentsMargins(0,0,0,0)
        self.boxForHideOptionsWhenFinished.setLayout(self.boxLayoutForHideOptionsWhenFinished)

        self.resultStyleComboBox.addItems([r'a + b = c', r'a+b=c', r'$a + b = c$', r'$a+b=c$'])

        self.boxForResultStyle.addWidget(self.resultStyleHint)
        self.boxForResultStyle.addWidget(self.resultStyleComboBox)


        self.penLineWidthBox.addWidget(self.penLineWidthHint)
        self.penLineWidthBox.addWidget(self.penLineWidthSpinbox)

        self.apiUsageSpinbox.setMaximum(9999999)
        self.apiUsageBox.addWidget(self.apiUsageHint)
        self.apiUsageBox.addWidget(self.apiUsageSpinbox)

        self.boxLayoutForChooseMethod.addWidget(self.chooseMethodHint)
        self.boxLayoutForChooseMethod.addWidget(self.mathpixApiMethodRadioButton)
        self.boxLayoutForChooseMethod.addWidget(self.latexLiveMethodRadioButton)
        self.boxLayoutForChooseMethod.setContentsMargins(0,0,0,0)
        self.boxForChooseMethod.setContentsMargins(0,0,0,0)
        self.boxForChooseMethod.setLayout(self.boxLayoutForChooseMethod)

        self.preferenceGroupLayout.addWidget(self.hideToSystemTraySwitch)
        # self.preferenceGroupLayout.addWidget(self.alwaysForegroundSwitch)
        self.preferenceGroupLayout.addWidget(self.clearPixmapWhenFinishedSwitch)
        self.preferenceGroupLayout.addWidget(self.boxForHideOptionsWhenFinished)
        self.preferenceGroupLayout.addLayout(self.penLineWidthBox)
        self.preferenceGroupLayout.addLayout(self.apiUsageBox)
        self.preferenceGroupLayout.addWidget(self.boxForChooseMethod)
        # self.preferenceGroupLayout.addLayout(self.boxForResultStyle)




        self.preferenceGroup.setLayout(self.preferenceGroupLayout)

        self.appidBox.setEchoMode(QLineEdit.Password)
        self.appkeyBox.setEchoMode(QLineEdit.Password)

        self.apiFromBox.addRow(self.appidHint, self.appidBox)
        self.apiFromBox.addRow(self.appkeyHint, self.appkeyBox)
        self.apiFromBox.setWidget(2, QFormLayout.SpanningRole, self.saveApiButton)

        self.apiGroup.setLayout(self.apiFromBox)

        self.masterLayout.addWidget(self.preferenceGroup)
        self.masterLayout.addWidget(self.apiGroup)
        self.masterLayout.addStretch(1)
        self.setLayout(self.masterLayout)

        self.checkDB()

    def connectSlots(self):
        self.hideToSystemTraySwitch.clicked.connect(self.hideToSystemTraySwitchClicked)
        self.alwaysForegroundSwitch.clicked.connect(self.alwaysForegroundSwitchClicked)
        self.clearPixmapWhenFinishedSwitch.clicked.connect(self.clearPixmapWhenFinishedSwitchClicked)
        self.penLineWidthSpinbox.valueChanged.connect(self.penLineWidthSpinboxChanged)
        self.apiUsageSpinbox.valueChanged.connect(self.apiUsageSpinboxChanged)
        self.doNotHideWhenFinishedSwitch.clicked.connect(self.hideOptionsWhenFinishedSwitchClicked)
        self.hideToTaskBarWhenFinishedSwitch.clicked.connect(self.hideOptionsWhenFinishedSwitchClicked)
        self.hideToSystemTrayWhenFinishedSwitch.clicked.connect(self.hideOptionsWhenFinishedSwitchClicked)
        self.mathpixApiMethodRadioButton.clicked.connect(self.mathpixApiMethodRadioButtonClicked)
        self.latexLiveMethodRadioButton.clicked.connect(self.latexLiveMethodRadioButtonClicked)
        self.saveApiButton.clicked.connect(self.saveApiButtonClicked)

    def checkDB(self):
        cursor = self.conn.cursor()

        hideToSystemTrayResult = cursor.execute('''select value from %s where item = '%s'; ''' % (self.preferenceTableName, 'hideToTrayWhenHitCloseSwitch') ).fetchone()
        if hideToSystemTrayResult == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            cursor.execute('''insert into %s (item, value) values ('hideToTrayWhenHitCloseSwitch', 'False') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            hideToSystemTrayValue = hideToSystemTrayResult[0]
            if hideToSystemTrayValue == 'True':
                self.hideToSystemTraySwitch.setChecked(True)
            else:
                self.hideToSystemTraySwitch.setChecked(False)

        alwaysForegroundResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
        self.preferenceTableName, 'alwaysForegroundSwitch')).fetchone()
        if alwaysForegroundResult == None:  # 如果始终前台这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('alwaysForegroundSwitch', 'False') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            alwaysForegroundResult = alwaysForegroundResult[0]
            if alwaysForegroundResult == 'True':
                self.alwaysForegroundSwitch.setChecked(True)
            else:
                self.alwaysForegroundSwitch.setChecked(False)

        penLineWidthResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'penLineWidthSpinbox')).fetchone()
        if penLineWidthResult == None:  # 如果始终前台这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('penLineWidthSpinbox', '2') ''' % self.preferenceTableName)
            self.conn.commit()
            self.penLineWidthSpinbox.setValue(2)
        else:
            penLineWidthResult = penLineWidthResult[0]
            self.penLineWidthSpinbox.setValue(int(penLineWidthResult))

        apiUsageResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'apiUsageSpinbox')).fetchone()
        if apiUsageResult == None:  # 如果始终前台这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('apiUsageSpinbox', '0') ''' % self.preferenceTableName)
            self.conn.commit()
            self.penLineWidthSpinbox.setValue(0)
        else:
            apiUsageResult = apiUsageResult[0]
            self.apiUsageSpinbox.setValue(int(apiUsageResult))

        clearPixmapWhenFinishedResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'clearPixmapWhenFinishedSwitch')).fetchone()
        if clearPixmapWhenFinishedResult == None:  # 如果识别完成后清空画布这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('clearPixmapWhenFinishedSwitch', 'False') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            clearPixmapWhenFinishedResult = clearPixmapWhenFinishedResult[0]
            if clearPixmapWhenFinishedResult == 'True':
                self.clearPixmapWhenFinishedSwitch.setChecked(True)
            else:
                self.clearPixmapWhenFinishedSwitch.setChecked(False)

        hideOptionsWhenFinishedResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'hideOptionsWhenFinished')).fetchone()
        if hideOptionsWhenFinishedResult == None:  # 如果势必完成后是否最小化这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('hideOptionsWhenFinished', '0') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            hideOptionsWhenFinishedResult = hideOptionsWhenFinishedResult[0]
            if hideOptionsWhenFinishedResult == '0':
                self.doNotHideWhenFinishedSwitch.setChecked(True)
            elif hideOptionsWhenFinishedResult == '1':
                self.hideToTaskBarWhenFinishedSwitch.setChecked(True)
            elif hideOptionsWhenFinishedResult == '2':
                self.hideToSystemTrayWhenFinishedSwitch.setChecked(True)

        chooseMethodResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'boxLayoutForChooseMethod')).fetchone()
        if chooseMethodResult == None:
            cursor.execute(
                '''insert into %s (item, value) values ('boxLayoutForChooseMethod', 'Mathpix') ''' % self.preferenceTableName)
            self.conn.commit()
            self.mathpixApiMethodRadioButton.click()
        else:
            chooseMethodResult = chooseMethodResult[0]
            if chooseMethodResult == 'Mathpix':
                self.mathpixApiMethodRadioButton.click()
            else:
                self.latexLiveMethodRadioButton.click()

        appidResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'appid')).fetchone()
        if appidResult == None:  # 如果识别完成后清空画布这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('appid', '') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            appidResult = appidResult[0]
            self.appidBox.setText(appidResult)
            self.mainWindow.quickMathTab.appid = appidResult

        appkeyResult = cursor.execute('''select value from %s where item = '%s'; ''' % (
            self.preferenceTableName, 'appkey')).fetchone()
        if appkeyResult == None:  # 如果识别完成后清空画布这个选项还没有在数据库创建，那就创建一个
            cursor.execute(
                '''insert into %s (item, value) values ('appkey', '') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            appkeyResult = appkeyResult[0]
            self.appkeyBox.setText(appkeyResult)
            self.mainWindow.quickMathTab.appkey = appkeyResult

    def hideToSystemTraySwitchClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.hideToSystemTraySwitch.isChecked()), 'hideToTrayWhenHitCloseSwitch'))
        self.conn.commit()

    def penLineWidthSpinboxChanged(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.penLineWidthSpinbox.value()), 'penLineWidthSpinbox'))
        self.conn.commit()

    def apiUsageSpinboxChanged(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.apiUsageSpinbox.value()), 'apiUsageSpinbox'))
        self.conn.commit()

    def alwaysForegroundSwitchClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.alwaysForegroundSwitch.isChecked()), 'alwaysForegroundSwitch'))
        self.conn.commit()
        if self.alwaysForegroundSwitch.isChecked():
            self.mainWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
            # print(self.mainWindow.windowFlags())

    def clearPixmapWhenFinishedSwitchClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.clearPixmapWhenFinishedSwitch.isChecked()), 'clearPixmapWhenFinishedSwitch'))
        self.conn.commit()

    def hideOptionsWhenFinishedSwitchClicked(self):
        cursor = self.conn.cursor()
        if self.doNotHideWhenFinishedSwitch.isChecked():
            cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, '0', 'hideOptionsWhenFinished'))
        elif self.hideToTaskBarWhenFinishedSwitch.isChecked():
            cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, '1', 'hideOptionsWhenFinished'))
        elif self.hideToSystemTrayWhenFinishedSwitch.isChecked():
            cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, '2', 'hideOptionsWhenFinished'))
        self.conn.commit()

    def mathpixApiMethodRadioButtonClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, 'Mathpix', 'boxLayoutForChooseMethod'))
        self.conn.commit()

    def latexLiveMethodRadioButtonClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, 'LatexLive', 'boxLayoutForChooseMethod'))
        self.conn.commit()


    def saveApiButtonClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, self.appidBox.text(), 'appid'))
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, self.appkeyBox.text(), 'appkey'))
        self.conn.commit()
        self.mainWindow.quickMathTab.appid = self.appidBox.text()
        self.mainWindow.quickMathTab.appkey = self.appkeyBox.text()

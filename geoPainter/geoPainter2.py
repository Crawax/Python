#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class drawingWidget(QWidget):
    pass
        
class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        
        self.projectName = 'New_project'
        self.titleFont = QFont()
        self.titleFont.setBold(True)
        self.titleFont.setPointSize(15)
        self.mcGraphicStyle = ('Norway', 'Great-Canyon', 'Tropical')
        
        
        self.initMenu()
        self.initLayout()
        
    def initLayout(self):
        layoutMain = QVBoxLayout()
        layoutTop = QHBoxLayout()
        layoutMiddle = QHBoxLayout()
        layoutBottom = QHBoxLayout()
        
        self.resolution = {}
        for res in ('nx','nz','x','z','minz','maxz'):
            self.resolution[res] = self.buildSpinBox(0,255)
        
        layoutTopLeft = QGridLayout()
        layoutTopLeft.addWidget(self.buildTitle('Resolution'), 0,0,1,6)
        
        layoutTopLeft.addWidget(QLabel('nx : '),         1,0)
        layoutTopLeft.addWidget(self.resolution['nx'],   1,1)
        layoutTopLeft.addWidget(QLabel('nz : '),         2,0)
        layoutTopLeft.addWidget(self.resolution['nz'],   2,1)
        
        layoutTopLeft.addWidget(QLabel('   x : '),       1,2)
        layoutTopLeft.addWidget(self.resolution['x'],    1,3)
        layoutTopLeft.addWidget(QLabel('   y : '),       2,2)
        layoutTopLeft.addWidget(self.resolution['z'],    2,3)
        
        layoutTopLeft.addWidget(QLabel('   minz : '),    1,4)
        layoutTopLeft.addWidget(self.resolution['minz'], 1,5)
        layoutTopLeft.addWidget(QLabel('   maxz : '),    2,4)
        layoutTopLeft.addWidget(self.resolution['maxz'], 2,5)
        
        layoutTop.addItem(layoutTopLeft)
        layoutTop.addSpacerItem(QSpacerItem(10,1))
        
        layoutTopMiddle = QHBoxLayout()
        gridImage = QLabel()
        
        # Temporaire
        pixmap = QPixmap(QSize(150,150))
        pixmap.fill(QColor(100,0,0))
        gridImage.setPixmap(pixmap)
        layoutTopMiddle.addWidget(gridImage)
        layoutTop.addItem(layoutTopMiddle)
        layoutTop.addSpacerItem(QSpacerItem(10,1))
        
        layoutTopRight = QVBoxLayout()
        layoutTopRight.addWidget(self.buildTitle('Minecraft Graphic Style'))

        mcGraphicStyle = []
        for style in self.mcGraphicStyleList:
            mcGraphicStyle[0]
            
        
        mcGraphicStyle = ( { 'display-name': 'Norway', 'id': 0
                              'greatCanyon': QRadioButton('greatCanyon'),
                              'tropical':    QRadioButton('tropical') )
        mcGraphicStyle['norway'].clicked.connect(lambda: self.setMcGraphicStyle(1))
        mcGraphicStyle['greatCanyon'].clicked.connect(lambda: self.setMcGraphicStyle(2))
        mcGraphicStyle['tropical'].clicked.connect(lambda: self.setMcGraphicStyle(3))
        
        mcGraphicStyleButtonGroup = QButtonGroup()
        
        first = True
        for key in mcGraphicStyle:
            
            if first == True:
                mcGraphicStyle[key].setChecked(True)
                first = False
            mcGraphicStyleButtonGroup.addButton(mcGraphicStyle[key])
            layoutTopRight.addWidget(mcGraphicStyle[key])

        layoutTop.addItem(layoutTopRight)
        
        layoutMain.addItem(layoutTop)
        layoutMain.addItem(layoutMiddle)
        layoutMain.addItem(layoutBottom)

        
        centralWidget = QWidget(self)
        centralWidget.setLayout(layoutMain)
        self.setCentralWidget(centralWidget)
        
    def setMcGraphicStyle(self, style):
        if style == 1:
            print('setMcGraphicStyle: norway')
        elif style == 2:
            print('setMcGraphicStyle: great-canyon')
        elif style == 3:
            print('setMcGraphicStyle: tropical')
        else:
            print('setMcGraphicStyle: style error')
        
    def buildTitle(self, title):
        title = QLabel(title)
        title.setAlignment(Qt.AlignCenter|Qt.AlignBottom)
        title.setFont(self.titleFont)
        return title
        
    def buildSpinBox(self, min, max):
        spinBox = QSpinBox()
        spinBox.setRange(min,max)
        return spinBox
        
    def initMenu(self):
        self.menuBar().addAction(QAction("&Help ?", self, shortcut="Ctrl+H",
            triggered=self.showHelp))
        
    def showHelp(self):
        print('show help')

        
if __name__ == '__main__':
    application = QApplication(sys.argv)
    geoPainter = myMainWindow()
    geoPainter.show()
    sys.exit(application.exec_())
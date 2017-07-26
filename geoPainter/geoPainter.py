#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

import sys
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QDir
from PyQt5.QtGui import QImage, QPainter, QColor, qRgb, QRadialGradient, QPen, QBrush, QPixmap, QPalette
from PyQt5.QtWidgets import (QAction, QWidget, QMainWindow, QGroupBox, QApplication, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QLayout,
                            QTabWidget, QPushButton, QScrollArea, QMenu)

class myDrawWidget(QWidget):
    def __init__(self, parent=None):
        super(myDrawWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
       
        
        self.hasChanged = False
        self.isMouseLeftButtDown = False
        self.penSettings = {'width': '', 'radius': '', 'color': ''}
        self.drawingSize = (500, 500)
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()
        
        def setPenSettings(self, width=None, color=None):
            if width != None:
                self.penSettings['width'] = width
                self.penSettings['radius'] = buildPenRadius(width)
                
            if color != None:
                self.penSettings['color'] = color
                
        def buildPenRadius(self, penWidth):
            return penWidth / 2 + 2
            
   
class myProjectSettingsPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        
        settingsGridLayout = QGridLayout()
        
        # Project name
        inputProjectName = QLineEdit()
        inputProjectName.setMaxLength(60)
        settingsGridLayout.addWidget(QLabel('Name'), 0, 0)
        settingsGridLayout.addWidget(inputProjectName, 1, 0)
        
        # Res X
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Res X'), 0, 1)
        settingsGridLayout.addWidget(inputResX, 1, 1)
        
        # Res Y
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Res Y'), 0, 2)
        settingsGridLayout.addWidget(inputResX, 1, 2)
        
        # Min X
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Min X'), 0, 3)
        settingsGridLayout.addWidget(inputResX, 1, 3)
        
        # Max X
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Max X'), 0, 4)
        settingsGridLayout.addWidget(inputResX, 1, 4)
        
        # Min Y
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Min Y'), 0, 5)
        settingsGridLayout.addWidget(inputResX, 1, 5)
        
        # Max Y
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Max Y'), 0, 6)
        settingsGridLayout.addWidget(inputResX, 1, 6)
        
        # Min Z
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Min Z'), 0, 7)
        settingsGridLayout.addWidget(inputResX, 1, 7)
        
        # Max Z
        inputResX = QSpinBox()
        inputResX.setMaximum(255)
        settingsGridLayout.addWidget(QLabel('Max Z'), 0, 8)
        settingsGridLayout.addWidget(inputResX, 1, 8)
        
        # Ok
        buttonOk = QPushButton('Ok')
        buttonOk.clicked.connect(self.validateSettings)
        settingsGridLayout.addWidget(buttonOk, 2, 0)
        # Cancel

        
        self.setLayout(settingsGridLayout)
        
        
    def validateSettings(self):
        print('validateSettings')
        
   
class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        
        self.initMenuBar()
        
        # Create the layout that will contain every other widget
        self.mainVBoxLayout = QVBoxLayout()
        
        self.initBrushGroup()
        self.initDrawingTab()
        
        
        # Create an empty widget an apply the layout to it
        mainWidget = QWidget()
        mainWidget.setLayout(self.mainVBoxLayout)
        
        self.popup = myProjectSettingsPopup()
        self.popup.show()
        
        
    def initBrushGroup(self):
        print('initBrushGroup')
        
    def initDrawingTab(self):
        print('initDrawingTab')
        
    def initMenuBar(self):
        # menuFile
        actionOpenProject = QAction("&Open project", self, shortcut="Ctrl+O", triggered=self.openProject)
        actionSaveProject = QAction("&Save project", self, shortcut="Ctrl+S", triggered=self.saveProject)
        menuFile = QMenu("&File", self)
        menuFile.addAction(actionOpenProject)
        menuFile.addAction(actionSaveProject)
        self.menuBar().addMenu(menuFile)

        # menuSettings
        actionProjectSettings = QAction("&Project settings", self, shortcut="Ctrl+E", triggered=self.projectSettings)
        menuSettings = QMenu("S&ettings", self)
        menuSettings.addAction(actionProjectSettings)
        self.menuBar().addMenu(menuSettings)
        
    def openProject(self):
        print('openProject')  
        
    def saveProject(self):
        print('saveProject')   
        
    def projectSettings(self):
        print('projectSettings')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    geoPainter = myMainWindow()
    geoPainter.setWindowTitle('geoPainter')
    geoPainter.show()
    
    sys.exit(app.exec_())
    
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class drawWidget(QWidget):
    def __init__(self, parent=None):
        super(drawWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        
        self.setLayout(QVBoxLayout())
        
        self.changedSinceLastSave = False
        self.LeftMouseButtonDown = False
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()
        self.drawing = QImage()
        
        self.penWidth = 25
        self.penWidthRad = self.penWidth / 2 + 2
        self.penColor = QColor(0, 0, 0, 30)

    
    # Qt Buildin Event
    def resizeEvent(self, event):
        self.resizeDrawing(event.size())
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.drawing, event.rect())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.LeftMouseButtonDown = True
            self.lastPoint = self.currentPoint
            self.currentPoint = event.pos()
            self.drawLine()
    
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.LeftMouseButtonDown:
            self.lastPoint = self.currentPoint
            self.currentPoint = event.pos()
            self.drawLine()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.LeftMouseButtonDown = False
    # /Qt Event
    
    
    def buildPen(self, point):
        gradient = QRadialGradient(point.x(), point.y(), self.penWidth)
        gradient.setColorAt(0, self.penColor);
        gradient.setColorAt(0.5, QColor.fromRgbF(1, 1, 1, 0));
        return QPen(QBrush(gradient),
                    self.penWidth,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin
                    )
    
    def drawLine(self):
        painter = QPainter(self.drawing)
        painter.setPen(self.buildPen(self.currentPoint))
        
        
        painter.drawLine(self.lastPoint, self.currentPoint)
        self.changedSinceLastSave = True
        
        radius = self.penWidth / 2 + 2
        self.update(QRect(self.lastPoint, self.currentPoint)
            .normalized().adjusted(-radius, -radius, +radius, +radius))
    
    def resizeDrawing(self, size):
        print('resizeDrawing')
        print('New size : ', size.width(),size.height())
        if not size == self.drawing.size():
            newDrawing = QImage(size, QImage.Format_RGB32)
            newDrawing.fill(qRgb(255,255,255))
            
            painter = QPainter(newDrawing)
            
            painter.drawImage(QPoint(
                size.width() / 2 - self.drawing.width() / 2,
                size.height() / 2 - self.drawing.height() / 2
            ), self.drawing)
            
            self.drawing = newDrawing
            self.setFixedSize(self.drawing.size())
        else:
            print('resizeDrawing : nothing to do')
            
    def changed(self):
        if self.changedSinceLastSave:
            return True
            
            
    def save(self, fileName, extention):
        if self.drawing.save(fileName, extention):
            self.changedSinceLastSave = False
            return True
            
        return False
    
class sizeWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        self.parentWindowRef = None # Allow self to be owned by PyQt instead of Qt
        
        self.parentWindow = None # Used to send back values
        
        inputLayout = QGridLayout()
        
        
        self.inputSizeX = QSpinBox()
        self.inputSizeX.setRange(200,5000)
        inputLayout.addWidget(QLabel('Size X : '),0,0) 
        inputLayout.addWidget(self.inputSizeX,    0,1)
        
        self.inputSizeY = QSpinBox()
        self.inputSizeY.setRange(200,5000)
        inputLayout.addWidget(QLabel(' Size Y : '),0,2)
        inputLayout.addWidget(self.inputSizeY,     0,3)
        
        buttonValidate = QPushButton('Confirm')
        buttonValidate.clicked.connect(self.sendSize)
        
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.hide)
        
        mainLayout = QVBoxLayout()
        mainLayout.addItem(inputLayout)
        mainLayout.addWidget(buttonValidate)
        mainLayout.addWidget(buttonCancel)
        self.setLayout(mainLayout)
        
    def sendSize(self):
        self.parentWindow.setSize(QSize(
            self.inputSizeX.value(),
            self.inputSizeY.value()
            ))
        self.hide()
        
class resolutionWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        self.parentWindowRef = None # Allow self to be owned by PyQt instead of Qt
        
        self.parentWindow = None # Used to send back values
        
        
        inputLayout = QGridLayout()
        
        self.inputMinX = QSpinBox()
        self.inputMinX.setRange(0,255)
        inputLayout.addWidget(QLabel('Min X : '),0,0)
        inputLayout.addWidget(self.inputMinX,    0,1)
        
        self.inputMaxX = QSpinBox()
        self.inputMaxX.setRange(0,255)
        inputLayout.addWidget(QLabel(' Max X : '),0,2)
        inputLayout.addWidget(self.inputMaxX,     0,3)
        
        self.inputMinY = QSpinBox()
        self.inputMinY.setRange(0,255)
        inputLayout.addWidget(QLabel('Min Y : '),1,0)
        inputLayout.addWidget(self.inputMinY,    1,1)
        
        self.inputMaxY = QSpinBox()
        self.inputMaxY.setRange(0,255)
        inputLayout.addWidget(QLabel(' Max Y : '),1,2)
        inputLayout.addWidget(self.inputMaxY,     1,3)
        
        self.inputMinZ = QSpinBox()
        self.inputMinZ.setRange(0,255)
        inputLayout.addWidget(QLabel('Min Z : '),2,0)
        inputLayout.addWidget(self.inputMinZ,    2,1)
        
        self.inputMaxZ = QSpinBox()
        self.inputMaxZ.setRange(0,255)
        inputLayout.addWidget(QLabel(' Max Z : '),2,2)
        inputLayout.addWidget(self.inputMaxZ,     2,3)
        
        buttonValidate = QPushButton('Confirm')
        buttonValidate.clicked.connect(self.sendResolution)
        
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.hide)
        
        mainLayout = QVBoxLayout()
        mainLayout.addItem(inputLayout)
        mainLayout.addWidget(buttonValidate)
        mainLayout.addWidget(buttonCancel)
        self.setLayout(mainLayout)
        
    def sendResolution(self):
        self.parentWindow.setResolution((
            (self.inputMinX.value(),self.inputMaxX.value()),
            (self.inputMinY.value(),self.inputMaxY.value()),
            (self.inputMinZ.value(),self.inputMaxZ.value())))
        self.hide()

class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        
        self.name = 'New_project'
        
        self.drawings = {}
        self.drawings['Topology'] = drawWidget()
        self.drawings['Uplift'] = drawWidget()
        self.drawings['Precipitation'] = drawWidget()
        
        
        
        self.tab = QTabWidget()
        self.tab.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
            )
        # self.tab.palette = self.tab.palette()
        # self.tab.palette.setColor(self.backgroundRole(), Qt.gray)
        # self.tab.setPalette(self.tab.palette)
        
        
        for key in self.drawings:
            self.tab.addTab(self.drawings[key], key)
        
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.tab)

        

        myCentralLayout = QVBoxLayout()
        #myCentralLayout.setSizeConstraint(QLayout.SetFixedSize)
        myCentralLayout.addWidget(scrollArea)
        
        myCentralWidget = QWidget(self)
        myCentralWidget.setLayout(myCentralLayout)
        
        self.setCentralWidget(myCentralWidget)
        
        
        self.setSize(QSize(200,200))
        self.buildMenu()
        
    def buildMenu(self):
        file = QMenu("&File", self)
        file.addAction(QAction("&Open a project", self, shortcut="Ctrl+O",
            triggered=self.openProject))
        file.addAction(QAction("&Save the project", self, shortcut="Ctrl+S",
            triggered=self.save))
        file.addAction(QAction("&New project", self, shortcut="Ctrl+N", 
            triggered=self.newProject))
        file.addAction(QAction("&Quit", self, shortcut="Ctrl+Q",
            triggered=self.quit))
        self.menuBar().addMenu(file)
        
        settings = QMenu("S&ettings", self)
        settings.addAction(QAction("Project na&me", self, shortcut="Ctrl+M",
            triggered=self.setName))
        settings.addAction(QAction("Edit S&ize", self, shortcut="Ctrl+i",
            triggered=self.showSizeWindow))
        settings.addAction(QAction("Edit &Resolution", self, shortcut="Ctrl+R",
            triggered=self.showResolutionWindow))
        self.menuBar().addMenu(settings)
        
    def openProject(self):
        pass
        
    def save(self):
        fileName, extention =  QFileDialog.getSaveFileName(self, "Save As", 
                    QDir.currentPath() + '/' + self.name,
                    "%s Files (*.%s);;All Files (*)" % ('PNG', 'png'))
                    
        if fileName:
            for key in self.drawings:
                self.drawings[key].save(
                    fileName.replace('.png', '_' + key + '.png'),
                    'png'
                )
            return True
            
        return False
            
        
    def newProject(self):
        pass
        
    def showResolutionWindow(self):
        try:
            self.resolutionPopup
        except AttributeError:
            self.resolutionPopup = resolutionWindow()
            self.resolutionPopup.parentWindow = self
            
        self.resolutionPopup.show()  
        
    def showSizeWindow(self):
        try:
            self.sizePopup
        except AttributeError:
            self.sizePopup = sizeWindow()
            self.sizePopup.parentWindow = self
            
        self.sizePopup.show()
        
    def setSize(self, size):
        for key in self.drawings:
            self.drawings[key].resizeDrawing(size)
            
        
        self.tab.resize(size)
         # Add margin to avoid scrolling bar
        self.resize(size.width() + 20,size.height() + 41)
        
    def setResolution(self, resolution):
        for drawingKey in self.drawings:
            self.drawings[drawingKey].resizeDrawing(QSize(resolution['x'],
                resolution['y']))
        
    def quit(self):
        pass
        
    def setName(self):
        newName, okPressed = QInputDialog.getText(self,
            "Project name", "Choose a new project name:", QLineEdit.Normal,
            self.name)
        if okPressed == True and not newName == '' and not newName == self.name:
            self.name = newName
            self.updateWindowTitle()
        else:
            print('setName : nothing to do')

    def updateWindowTitle(self):
        self.setWindowTitle(self.name)
        
    def needSave(self):
        needSave = False
        for key in drawings:
            if drawings[key].changed():
                needSave = True
                break
        
if __name__ == '__main__':
    application = QApplication(sys.argv)
    geoPainter = myMainWindow()
    geoPainter.show()
    sys.exit(application.exec_())
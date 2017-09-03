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
        self.gradientColor = (
            {'position': 0,   'color': QColor(0, 0, 0, 10)},
            {'position': 0.2, 'color': QColor(0, 0, 0, 5)},
            {'position': 0.6, 'color': QColor.fromRgbF(1, 1, 1, 0)})
        self.penColor = QColor(0, 0, 0, 10)

    
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
            self.lastPoint = event.pos()
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
    
    
    def buildPen(self):
        gradient = QRadialGradient(self.currentPoint, self.penWidth)

        for color in self.gradientColor:
            gradient.setColorAt(color['position'],color['color'])
        
        return QPen(QBrush(gradient),
                    self.penWidth,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin)
    
    def drawLine(self):
        painter = QPainter(self.drawing)
        painter.setPen(self.buildPen())
        
        if self.lastPoint == self.currentPoint:
            painter.drawPoint(self.currentPoint)
        else:
            painter.drawLine(self.lastPoint, self.currentPoint)
            
        self.changedSinceLastSave = True
        
        radius = self.penWidth / 2 + 2
        self.update(QRect(self.lastPoint, self.currentPoint)
            .normalized().adjusted(-radius, -radius, +radius, +radius))
    
    def resizeDrawing(self, size):
        if not size == self.drawing.size():
            newDrawing = QImage(size, QImage.Format_RGB32)
            newDrawing.fill(qRgb(255,255,255))
            
            painter = QPainter(newDrawing)
            
            painter.drawImage(QPoint(
                size.width() / 2 - self.drawing.width() / 2,
                size.height() / 2 - self.drawing.height() / 2),
                self.drawing)
            
            self.drawing = newDrawing
            self.setFixedSize(self.drawing.size())
            
    def changed(self):
        return self.changedSinceLastSave
        
    def size(self):
        return self.drawing.size()
            
    def save(self, fileName, extention):
        if self.drawing.save(fileName, extention):
            self.changedSinceLastSave = False
            return True
        return False
        
    def open(self, fileName):
        openedDrawing = QImage()
        if not openedDrawing.load(fileName):
            print('fail to load image : ', fileName)
            return False
            
        newSize = openedDrawing.size()
        
        newDrawing = QImage(newSize,QImage.Format_RGB32)
        newDrawing.fill(qRgb(255, 255, 255))
        
        painter = QPainter(newDrawing)
        painter.drawImage(QPoint(0,0), openedDrawing)
        
        self.drawing = newDrawing
        
        self.setFixedSize(newSize)
        self.changedSinceLastSave = False
        self.update()
        return True
        
    def create(self, size):
        newDrawing = QImage(size,QImage.Format_RGB32)
        newDrawing.fill(qRgb(255, 255, 255))
        self.drawing = newDrawing
        self.setFixedSize(size)
        self.changedSinceLastSave = False
        self.update()
    
class sizeWindow(QWidget):
    def __init__(self, parentWindow):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        self.parentWindowRef = None # Allow self to be owned by PyQt instead of Qt
        
        self.parentWindow = parentWindow # Used to send back values
        
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
    def __init__(self, parentWindow):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        self.parentWindowRef = None # Allow self to be owned by PyQt instead of Qt
        
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

class brushWindow(QWidget):
    def __init__(self, parentWindow):
        QWidget.__init__(self)
        super(brushWindow, self).__init__(parentWindow)
        self.parentWindowRef = None # Allow self to be owned by PyQt instead of Qt
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.Tool)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        
        self.parentWindow = parentWindow
        
        mainLayout = QVBoxLayout()
        
        brushList = []
        brushList.append({
            'brush': [
                {'position': 0,  'color': QColor(0, 0, 0, 10)},
                {'position': 0.2,'color': QColor(0, 0, 0, 5)},
                {'position': 0.6,'color': QColor(1, 1, 1, 0)}],
            'name': 'Brush 01',
            'label': None})
        brushList.append({
            'brush': [
                {'position': 0,  'color': QColor(0, 0, 0, 10)},
                {'position': 0.2,'color': QColor(0, 0, 0, 5)},
                {'position': 0.6,'color': QColor(1, 1, 1, 0)}],
            'name': 'Brush 02',
            'label': None})
        # brushList.append({
            # 'brush': [
                # {'position': 0,  'color': QColor(0, 0, 0, 10)},
                # {'position': 0.2,'color': QColor(0, 0, 0, 5)},
                # {'position': 0.6,'color': QColor(1, 1, 1, 0)}],
            # 'name': 'Brush 03',
            #'label': None})
        # brushList.append({
            # 'brush': [
                # {'position': 0,  'color': QColor(0, 0, 0, 10)},
                # {'position': 0.2,'color': QColor(0, 0, 0, 5)},
                # {'position': 0.6,'color': QColor(1, 1, 1, 0)}],
            # 'name': 'Brush 03',
            #'label': None})
        
        topLayout = QVBoxLayout()
        
        id = 0
        for item in brushList:
            newLayout = QHBoxLayout()
            print('0')
            buttonName = QPushButton(item['name'])
            buttonEdit = QPushButton('edit')
            
            buttonName.clicked.connect(lambda state,
                lambdaId=id: self.selectBrush(lambdaId))
            buttonEdit.clicked.connect(lambda state,
                lambdaId=id: self.editBrush(lambdaId))
            print('1')
            previewImage = QImage(QSize(70,70), QImage.Format_RGB32)
            previewImage.fill(QColor(255, 255, 255))
            print('2')
            painter = QPainter(previewImage)
            print('3')
            painter.setPen(QPen(QBrush(QRadialGradient(QPoint(35,35), 60)),60,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
            print('4')
            painter.drawPoint(QPoint(35,35))
            self.update()

            preview = QPixmap(QSize(70,70))
            preview.fromImage(previewImage)
            painter = None # Delete the painter so we can reuse the variable
            
            label = QLabel()
            label.setPixmap(preview)
            brushList[id]['label'] = label

            newLayout.addWidget(item['label'])
            newLayout.addWidget(buttonName)
            newLayout.addWidget(buttonEdit)
            
            
            topLayout.addLayout(newLayout)
            id = id + 1
        
        bottomLayout = QVBoxLayout()
        
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        
        self.setLayout(mainLayout)
        
    def selectBrush(self, id):
        print('selectBrush: ' + str(id))
        
    def editBrush(self, id):
        print('editBrush: ' + str(id))
        
class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        
        self.name = 'New_project'
        self.defaultSize = QSize(500,500)
        
        self.drawings = {}
        self.drawings['Topology'] = drawWidget()
        self.drawings['Uplift'] = drawWidget()
        self.drawings['Precipitation'] = drawWidget()

        self.tab = QTabWidget()        
        
        for key in self.drawings:
            self.tab.addTab(self.drawings[key], key)
        
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.tab)

        myCentralLayout = QVBoxLayout()
        myCentralLayout.addWidget(scrollArea)
        
        myCentralWidget = QWidget(self)
        myCentralWidget.setLayout(myCentralLayout)
        
        self.setCentralWidget(myCentralWidget)
        
        self.setSize(self.defaultSize)
        
        self.buildMenu()
        
    def buildMenu(self):
        file = QMenu("&File", self)
        file.addAction(QAction("&Open a project", self, shortcut="Ctrl+O",
            triggered=self.open))
        file.addAction(QAction("&Save the project", self, shortcut="Ctrl+S",
            triggered=self.save))
        file.addAction(QAction("&New project", self, shortcut="Ctrl+N", 
            triggered=self.create))
        file.addAction(QAction("&Quit", self, shortcut="Ctrl+Q",
            triggered=self.close))
        self.menuBar().addMenu(file)
        
        brush = QMenu("&Brush", self)
        brush.addAction(QAction("Br&ush Window",self,shortcut="Crtl+U",
            triggered=self.showBrushWindow))
        self.menuBar().addMenu(brush)
        
        settings = QMenu("S&ettings", self)
        settings.addAction(QAction("Project na&me", self, shortcut="Ctrl+M",
            triggered=self.setName))
        settings.addAction(QAction("Edit S&ize", self, shortcut="Ctrl+i",
            triggered=self.showSizeWindow))
        settings.addAction(QAction("Edit &Resolution", self, shortcut="Ctrl+R",
            triggered=self.showResolutionWindow))
        self.menuBar().addMenu(settings)
        
    def open(self):
        self.needSave()
        fileName, extention =  QFileDialog.getOpenFileName(self, "Open project", 
            QDir.currentPath())
        if fileName:
            baseName = fileName
            for key in self.drawings:
                baseName = baseName.replace('_' + key + '.png', '')
                print(baseName)
                
            for key in self.drawings:   
                self.drawings[key].open(baseName + '_' + key + '.png')
                
            size = self.drawings[next(iter(self.drawings))].size()
            self.tab.resize(size)
            #Add margin to avoid scrolling bar
            self.resize(size.width() + 20,size.height() + 41)
        
        
    def save(self):
        fileName, extention =  QFileDialog.getSaveFileName(self, "Save As", 
                    QDir.currentPath() + '/' + self.name,
                    "%s Files (*.%s);;All Files (*)" % ('PNG', 'png'))
                    
        if fileName:
            for key in self.drawings:
                self.drawings[key].save(
                    fileName.replace('.png', '_' + key + '.png'),'png')
            return True
        return False
        
    def create(self):
        for key in self.drawings:
            self.drawings[key].create(self.defaultSize)
            
        self.tab.resize(self.defaultSize)
        # Add margin to avoid scrolling bar
        self.resize(self.defaultSize.width(),self.defaultSize.height() + 41)
        
    def showResolutionWindow(self):
        try:
            self.resolutionPopup
        except AttributeError:
            self.resolutionPopup = resolutionWindow(self)

        self.resolutionPopup.show()  
        
    def showSizeWindow(self):
        try:
            self.sizePopup
        except AttributeError:
            self.sizePopup = sizeWindow(self)

        self.sizePopup.show()
        
    def showBrushWindow(self):
        try:
            self.brushPopup
        except AttributeError:
            self.brushPopup = brushWindow(self)
            
        self.brushPopup.show()
        
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
        
    def closeEvent(self, event):
        self.needSave()
        event.accept()

    def setName(self):
        newName, okPressed = QInputDialog.getText(
            self,
            "Project name",
            "Choose a new project name:",
            QLineEdit.Normal,
            self.name)
        if okPressed == True and not newName == '' and not newName == self.name:
            self.name = newName
            self.updateWindowTitle()

    def updateWindowTitle(self):
        self.setWindowTitle(self.name)
        
    def needSave(self):
        for key in self.drawings:
            if self.drawings[key].changed():
                return self.save()
            return False
        
if __name__ == '__main__':
    application = QApplication(sys.argv)
    geoPainter = myMainWindow()
    geoPainter.show()
    sys.exit(application.exec_())

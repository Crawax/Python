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
        
        self.changeSinceLastSave = False
        self.drawingInProgress = False
        self.drawingButton = Qt.LeftButton
        
        self.penWidth = 25
        self.drawingSize = QSize(500,500)
        self.setFixedSize(self.drawingSize)
        self.drawing = QImage(self.drawingSize, QImage.Format_ARGB32)
        self.drawing.fill(QColor(255, 255, 255, 255))
        
        self.initLayer(10)
        
        self.gradientColor = (
            {'position': 0,   'color': QColor(0, 0, 0, 100)},
            {'position': 0.2, 'color': QColor(0, 0, 0, 5)},
            {'position': 0.6, 'color': QColor.fromRgbF(1, 1, 1, 0)})
        
        
    def rotateLayersForward(self):
        self.layersId = self.layersId[self.layerIdListSize:] + self.layersId[:self.layerIdListSize]

    def rotateLayersBackward(self):
        self.layersId = self.layersId[-self.layerIdListSize:] + self.layersId[:-self.layerIdListSize]

    def initLayer(self, layerCount):
        self.layers = [] # Contain the layer, layer are fully transparent image
        self.layersId = [] # We don't change the order of the image in the layer list
                           # work on the id list to be faster
        self.layerIdListSize = layerCount - 1
        
        for layerId in range(0, layerCount):
            self.layersId.append(layerId)
            self.layers.append(QImage(self.drawingSize, QImage.Format_ARGB32))
            self.layers[layerId].fill(QColor(0, 0, 0, 0))

        self.hiddenLayer = QImage(self.drawingSize, QImage.Format_RGB32)
        self.hiddenLayer.fill(QColor(255, 255, 255))

    def resizeEvent(self, event):
        self.resize(event.size())
        self.update()
        
    def resize(self, size):
        self.mergeLayersToDrawing()
        self.resizeDrawing(size)
        self.resizeLayers(size)
        
    def resizeLayers(self, size):
        pass
        
    def mergeLayersToDrawing(self):
        pass
        
    def resizeDrawing(self, size):
        if size != self.drawing.size():
            newDrawing = QImage(size, QImage.Format_ARGB32)
            newDrawing.fill(QColor(255,255,255,0))
            painter = QPainter(newDrawing)
            painter.drawImage(QPoint(
                            size.width() / 2 - self.drawing.width() / 2,
                            size.height() / 2 - self.drawing.height() / 2),
                            self.drawing)

            self.drawing = newDrawing
            self.setFixedSize(self.drawing.size())
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.drawing, event.rect())
        for layerId in self.layersId:
            painter.drawImage(event.rect(), self.layers[layerId], event.rect())
           
        #painter.drawImage(event.rect(), self.hiddenLayer, event.rect())
        
    def mousePressEvent(self, event):
        if event.button() == self.drawingButton:
            self.startDrawing(event.pos())
            
    def mouseReleaseEvent(self, event):
        if event.button() == self.drawingButton:
            self.stopDrawing()
            
    def mouseMoveEvent(self, event):
        if self.drawingInProgress == True:
            self.draw(event.pos())
            
            
    def mergeLastLayer(self):
        painter = QPainter(self.drawing)
        painter.drawImage(QPoint(self.drawingSize.width() / 2 - self.drawing.width() / 2,
                                 self.drawingSize.height() / 2 - self.drawing.height() / 2),
                                 self.layers[self.layersId[0]])
        self.layers[self.layersId[0]].fill(QColor(0, 0, 0, 0))
        self.rotateLayersForward()
        
    def draw(self, currentPoint):
        
        self.lastPoint = self.currentPoint
        self.currentPoint = currentPoint
        self.hiddenLayer.fill(QColor(255,255,255))
        painter = QPainter(self.hiddenLayer)
        painter.setPen(QColor(0,0,0))
        painter.drawLine(self.lastPoint, self.currentPoint)
        
        rect = [0,0,0,0]

        if self.lastPoint.x() < self.currentPoint.x():
            rect[0] = self.lastPoint.x()
            rect[1] = self.currentPoint.x()
        else:
            rect[0] = self.currentPoint.x()
            rect[1] = self.lastPoint.x()
            
        if self.lastPoint.y() < self.currentPoint.y():
            rect[2] = self.lastPoint.y()
            rect[3] = self.currentPoint.y()
        else:
            rect[2] = self.currentPoint.y()
            rect[3] = self.lastPoint.y()
            
        print(rect)
        
        pointList = []
        
        if rect[0] == rect[1]:
            for y in range(rect[2], rect[3]):
                pointList.append(QPoint(rect[0],y))
        elif rect[2] == rect[3]:
            for x in range(rect[0], rect[1]):
                pointList.append(QPoint(x,rect[2]))
        else:            
            for x in range(rect[0], rect[1]):
                for y in range(rect[2], rect[3]):
                    if self.hiddenLayer.pixel(x,y) == 4278190080:
                        pointList.append(QPoint(x,y))

                        
        print(pointList)
        for point in pointList:
            self.drawPoint(point)
        
    def stopDrawing(self):
        self.drawingInProgress = False
        self.mergeLastLayer()
        
    def startDrawing(self, position):
        self.currentPoint = position
        self.drawingInProgress = True
        self.changeSinceLastSave = True
        
        self.drawPoint(position)
        
    def drawPoint(self, position):
        painter = QPainter(self.layers[self.layersId[self.layerIdListSize]])
        painter.setPen(self.buildPen(position))
        painter.drawPoint(position)
        self.update()
            
    def buildPen(self, position):
        gradient = QRadialGradient(position, self.penWidth)

        for color in self.gradientColor:
            gradient.setColorAt(color['position'],color['color'])
        
        return QPen(QBrush(gradient),
                    self.penWidth,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin)
                    
                    
    def undo(self):
        print(self.layersId)

        self.layers[self.layersId[self.layerIdListSize - 1]].fill(QColor(0, 0, 0, 0))
        self.rotateLayersForward()
        
class myPopupWindow(QWidget):
    pass

        
class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        
        self.name = 'New_project'
        self.size = [500,500]
        
        self.allDrawing = ('Topography', 'Uplift', 'Precipitation', 'Erodability')
        
        self.drawingList = {}
        for drawing in self.allDrawing:
            self.drawingList[drawing] = drawWidget()
        
            
        self.initFont()
        self.initMenu()
        
        # === Top start ===
        layoutTop = QGridLayout()
        layoutTop.setAlignment(Qt.AlignLeft)
        
        self.resolutionInput = {'nx': self.buildSpinBox(0,255),
                                'nz': self.buildSpinBox(0,255),
                                'x': self.buildSpinBox(0,255),
                                'z': self.buildSpinBox(0,255),
                                'minz': self.buildSpinBox(0,255),
                                'maxz': self.buildSpinBox(0,255)}

        layoutTop.addWidget(self.buildLabelTitle('Resolution'), 0,0,1,6)

        layoutTop.addWidget(QLabel('nx : '),            1,0)
        layoutTop.addWidget(self.resolutionInput['nx'], 1,1)
        layoutTop.addWidget(QLabel('nz : '),            2,0)
        layoutTop.addWidget(self.resolutionInput['nz'], 2,1)

        layoutTop.addWidget(QLabel('  x (m) : '),      1,2)
        layoutTop.addWidget(self.resolutionInput['x'], 1,3)
        layoutTop.addWidget(QLabel('  z (m) : '),      2,2)
        layoutTop.addWidget(self.resolutionInput['z'], 2,3)

        layoutTop.addWidget(QLabel('  minz (m) : '),      1,4)
        layoutTop.addWidget(self.resolutionInput['minz'], 1,5)
        layoutTop.addWidget(QLabel('  maxz (m) : '),      2,4)
        layoutTop.addWidget(self.resolutionInput['maxz'], 2,5)
        

        layoutTop.addWidget(self.buildLabelTitle('===========\n !       Image       ! \n==========='),0,6,3,1)
        
        layoutTop.addWidget(self.buildLabelTitle('Minecraft Graphic Style'),0,7)
        
        self.mcGraphStyleInput = {  'norway': QRadioButton('Norway'),
                                    'great-canyon': QRadioButton('Great Canyon'),
                                    'tropical': QRadioButton('Tropical')}

        mcGraphStyleButtonGroup = QButtonGroup()
        mcGraphStyleButtonGroup.addButton(self.mcGraphStyleInput['norway'])
        mcGraphStyleButtonGroup.addButton(self.mcGraphStyleInput['great-canyon'])
        mcGraphStyleButtonGroup.addButton(self.mcGraphStyleInput['tropical'])
        self.mcGraphStyleInput['norway'].setChecked(True)
        
        layoutTop.addWidget(self.mcGraphStyleInput['norway'],1,7)
        layoutTop.addWidget(self.mcGraphStyleInput['great-canyon'],2,7)
        layoutTop.addWidget(self.mcGraphStyleInput['tropical'],3,7)
        # === Top end ===

        

        # === Middle start ===

        layoutBrush = QVBoxLayout()
        layoutBrush.setAlignment(Qt.AlignTop)
        layoutBrush.addWidget(QPushButton('Brush 01'))
        layoutBrush.addWidget(QPushButton('Brush 02'))
        layoutBrush.addWidget(QPushButton('Brush 03'))
        layoutBrush.addWidget(QPushButton('Brush 04'))
        layoutBrush.addWidget(QPushButton('Brush 05'))
        layoutBrush.addWidget(QPushButton('Brush 06'))

        
        self.drawningTab = QTabWidget()
        for key in self.drawingList:
            self.drawningTab.addTab(self.drawingList[key], key)
            #self.drawingList[key].resize(QSize(500,500))

        layoutDrawing = QVBoxLayout()
        layoutDrawing.addWidget(self.drawningTab)
        
        layoutMiddleleft = QHBoxLayout()
        layoutMiddleleft.addItem(layoutBrush)
        layoutMiddleleft.addItem(layoutDrawing)
        
        
        
        self.fastScapeInput = {  'erodability': self.buildSpinBox(0,255),
                                 'coefone': self.buildSpinBox(0,255),
                                 'coeftwo': self.buildSpinBox(0,255),
                                 'timestep': self.buildSpinBox(0,255)}
                                 
        layoutfastScape = QGridLayout()
        layoutfastScape.addWidget(QLabel('\n'))
        layoutfastScape.addWidget(QLabel('Erodability (Kf) : '),      1,0)
        layoutfastScape.addWidget(self.fastScapeInput['erodability'], 1,1)
        layoutfastScape.addWidget(QLabel('Coef 1(m) : '),             2,0)
        layoutfastScape.addWidget(self.fastScapeInput['coefone'],     2,1)
        layoutfastScape.addWidget(QLabel('  Coef 2 (n) : '),          1,2)
        layoutfastScape.addWidget(self.fastScapeInput['coeftwo'],     1,3)
        layoutfastScape.addWidget(QLabel('  Timestep (dt) : '),       2,2)
        layoutfastScape.addWidget(self.fastScapeInput['timestep'],    2,3)
        
        layoutMiddleRight = QVBoxLayout()
        layoutMiddleRight.setAlignment(Qt.AlignTop)
        layoutMiddleRight.addItem(layoutfastScape)
        layoutMiddleRight.addWidget(self.buildLabelTitle('===========\n !       Image       ! \n==========='))
        
        
        self.riverInput = {'width': self.buildSpinBox(0,255),
                           'depth': self.buildSpinBox(0,255)}

        layoutBottomRight = QGridLayout()
        layoutBottomRight.setAlignment(Qt.AlignLeft)
        layoutBottomRight.addWidget(QLabel('River width : '), 0,0)
        layoutBottomRight.addWidget(self.riverInput['width'], 0,1)
        layoutBottomRight.addWidget(QLabel('River Depth : '), 1,0)
        layoutBottomRight.addWidget(self.riverInput['depth'], 1,1)
        
        layoutMiddleRight.addItem(layoutBottomRight)


        layoutMiddle = QHBoxLayout()
        layoutMiddle.addItem(layoutMiddleleft)
        layoutMiddle.addItem(layoutMiddleRight)
        # === Middle end ===
        
        centralWidgetLayout = QVBoxLayout()

        centralWidgetLayout.addItem(layoutTop)
        centralWidgetLayout.addItem(layoutMiddle)
        layoutExtParam = QGridLayout()
        
        centralWidget = QWidget(self)
        centralWidget.setLayout(centralWidgetLayout)
        self.setCentralWidget(centralWidget)
        
    def initFont(self):
        self.myFont = {}
        self.myFont['title'] = QFont()
        self.myFont['title'].setPointSize(12)
        
    def buildLabelTitle(self, title):
        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(self.myFont['title'])
        return titleLabel
        
        
    def initMenu(self):
        self.menuBar().addAction(QAction("&Help ?", self, shortcut="Ctrl+H",
            triggered=self.help))
            
        self.menuBar().addAction(QAction("Undo <", self, shortcut="Ctrl+Z",
            triggered=self.undo))
        
    def undo(self):
        self.drawingList[self.allDrawing[self.drawningTab.currentIndex()]].undo()
        
    def help(self):
        print('help')
        
    def buildSpinBox(self, min=0, max=255):
        spinBox = QSpinBox()
        spinBox.setRange(min,max)
        return spinBox
        
    def showHelp(self):
        print('help')

if __name__ == '__main__':
    application = QApplication(sys.argv)
    geoPainter = myMainWindow()
    geoPainter.show()
    sys.exit(application.exec_())
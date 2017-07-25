#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

import sys
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QDir
from PyQt5.QtGui import QImage, QPainter, QColor, qRgb, QRadialGradient, QPen, QBrush, QPixmap, QPalette
from PyQt5.QtWidgets import (QAction, QWidget, QMainWindow, QGroupBox, QApplication, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QLayout,
                            QTabWidget, QPushButton, QScrollArea)

class DrawWidget(QWidget):
    def __init__(self, parent=None):
        super(DrawWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)

        
        self.setAutoFillBackground(True)
        self.palette = self.palette()
        self.palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(self.palette)
        
        self.hasChanged = False
        self.leftButtonDown = False
        self.penWidth = 25
        self.penWidthRad = self.penWidth / 2 + 2
        self.penColor = QColor(0, 0, 0, 50)
        
        imageSize =  (500, 500)
        
        self.image = QImage(QSize(imageSize[0], imageSize[1]), 5)
        self.lastPoint = QPoint()
        
        self.setFixedSize(imageSize[0], imageSize[1])
        
        self.primaryImage = None
        
    def setPenColor(self, color):
        self.penColor = color         
        
    def getPenColor(self):
        return self.penColor        
        
    def setPenWidth(self, width):
        self.penWidth = width
        self.penWidthRad = self.penWidth / 2 + 2
        
    def getPenWidth(self, width):
        return self.penWidth 
        
    def getlefButtonStatus(self):
        return self.leftButtonDown
    
    def loadImage(self, FileName):
        loadedImage = QImage()
        if not not loadedImage.load(fileName):
            print('Error while opening the image')
            return False
        
        self.resizeImage(loadedImage, loadedImage.size().expandedTo(self.size()))
        self.image = loadedImage
        
        self.hasChanged = False
        self.update()
        
        return True
       
    def buildPen(self,x, y):
        gradient = QRadialGradient(x, y, self.penWidth)
        gradient.setColorAt(0, self.penColor);
        gradient.setColorAt(0.5, QColor.fromRgbF(1, 1, 1, 0));
        return QPen(QBrush(gradient), self.penWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
       
    def saveImage(self, FileName):
        if self.image.save(fileName, 'png'):
            self.hasChanged = False
            return True
        else:
            print('Error when saving the image')
            return False

    def resetImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.hasChanged = True
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.leftButtonDown = True
            self.drawLineTo(event.pos())
        elif event.button() == Qt.RightButton:
            self.palette.setColor(self.backgroundRole(), Qt.red)
            self.setPalette(self.palette)
            
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.leftButtonDown:
            self.drawLineTo(event.pos())
            
    def mouseReleaseEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.leftButtonDown:
            self.drawLineTo(event.pos())
            self.leftButtonDown = False
            
    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)
        
    def resizeEvent(self, event):
        print('resizeEvent')
        self.resizeImage(self.image, QSize(self.width(), self.height()))
        self.update()
        super(DrawWidget, self).resizeEvent(event)
        
    def drawLineTo(self, currentPoint):
        painter = QPainter(self.image)
        painter.setPen(self.buildPen(currentPoint.x(), currentPoint.y()))
        
        if self.lastPoint == currentPoint:
            painter.drawPoint(currentPoint)
        else:
            painter.drawLine(self.lastPoint, currentPoint)
        self.hasChanged = True
        
        self.update(QRect(self.lastPoint, currentPoint).normalized().adjusted(-self.penWidthRad, -self.penWidthRad, +self.penWidthRad, +self.penWidthRad))
        self.lastPoint = QPoint(currentPoint)
        
    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return
            
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image) # Ici pour choisir comme redimentionné ?
        
        self.image = newImage
         
                
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle('geoPainter')
        
        self.drawingZoneTopol = DrawWidget()
        self.drawingZoneTopolSCA = QScrollArea()
        self.drawingZoneTopolSCA.setWidget(self.drawingZoneTopol)
        
        self.drawingZoneUplift = DrawWidget()
        self.drawingZoneUpliftSCA = QScrollArea()
        self.drawingZoneUpliftSCA.setWidget(self.drawingZoneUplift)
        
        self.drawingZonePrecip = DrawWidget()
        self.drawingZonePrecipSCA = QScrollArea()
        self.drawingZonePrecipSCA.setWidget(self.drawingZonePrecip)
        
        # DRAWING
        self.drawingTab = QTabWidget()
        self.drawingTab.currentChanged.connect(self.updateBackground)
        self.drawingTab.addTab(self.drawingZoneTopolSCA, "TOPOLOGY")
        self.drawingTab.addTab(self.drawingZoneUplift, "UPLIFT")
        self.drawingTab.addTab(self.drawingZonePrecip, "PRECIPITATION")
        
        self.drawingTab.palette = self.drawingTab.palette()
        self.drawingTab.palette.setColor(self.backgroundRole(), Qt.gray)
        self.drawingTab.setPalette(self.drawingTab.palette)
        # /DRAWING
        
        
        
        self.createBrushButton()
        self.createGeometryEditing()
        
        
        mainVBoxLayout = QVBoxLayout()
        mainVBoxLayout.addWidget(self.geometryGB)
        mainVBoxLayout.addWidget(self.brushAndDrawing)

        mainWidget = QWidget(self)
        mainWidget.setLayout(mainVBoxLayout)
        self.setCentralWidget(mainWidget)
      

    def createGeometryEditing(self):
        
        geometryGBLayout = QGridLayout()
        geometryGBLayout.setSizeConstraint(QLayout.SetFixedSize)
        
        geometryGBLayout.addWidget(QLabel('Name'),0,0)
        self.buttonName = QLineEdit()
        self.buttonName.setMaxLength(60)
        geometryGBLayout.addWidget(self.buttonName,1,0)
        
        geometryGBLayout.addWidget(QLabel('Res X'),0,1)
        self.inputResX = QSpinBox()
        self.inputResX.setMaximum(255)
        geometryGBLayout.addWidget(self.inputResX,1,1)
        
        geometryGBLayout.addWidget(QLabel('Res Y'),0,2)
        self.inputResY = QSpinBox()
        self.inputResY.setMaximum(255)
        geometryGBLayout.addWidget(self.inputResY,1,2)
        
        geometryGBLayout.addWidget(QLabel('Min  X'),0,3)
        self.inputMinX = QSpinBox()
        self.inputMinX.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMinX,1,3)
        
        geometryGBLayout.addWidget(QLabel('Max X'),0,4)
        self.inputMaxX = QSpinBox()
        self.inputMaxX.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMaxX,1,4)
        
        geometryGBLayout.addWidget(QLabel('Min  Y'),0,5)
        self.inputMinY = QSpinBox()
        self.inputMinY.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMinY,1,5)
        
        geometryGBLayout.addWidget(QLabel('Max Y'),0,6)
        self.inputMaxY = QSpinBox()
        self.inputMaxY.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMaxY,1,6)

        geometryGBLayout.addWidget(QLabel('Min  Z'),0,7)
        self.inputMinZ = QSpinBox()
        self.inputMinZ.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMinZ,1,7)
        
        geometryGBLayout.addWidget(QLabel('Max Z'),0,8)
        self.inputMaxZ = QSpinBox()
        self.inputMaxZ.setMaximum(255)
        geometryGBLayout.addWidget(self.inputMaxZ,1,8)
        
        self.buttonSetGeo = QPushButton('Validate')
        self.buttonSetGeo.clicked.connect(self.doPrint)
        geometryGBLayout.addWidget(self.buttonSetGeo, 1, 9)
        
        
        self.geometryGB = QGroupBox("DEFINE GEOMETRY")
        self.geometryGB.setLayout(geometryGBLayout)

      
    def createBrushButton(self):
        brushLayout = QVBoxLayout()
        brushLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.buttonSelBrushOne = QPushButton('Brush01')
        self.buttonSelBrushOne.clicked.connect(lambda: self.setBrush(1))
        brushLayout.addWidget(self.buttonSelBrushOne)

        self.buttonSelBrushTwo = QPushButton('Brush02')
        self.buttonSelBrushTwo.clicked.connect(lambda: self.setBrush(2))
        brushLayout.addWidget(self.buttonSelBrushTwo)

        self.buttonSelBrushThree = QPushButton('Brush03')
        self.buttonSelBrushThree.clicked.connect(lambda: self.setBrush(3))
        brushLayout.addWidget(self.buttonSelBrushThree)

        self.buttonSelBrushFour = QPushButton('Brush04')
        self.buttonSelBrushFour.clicked.connect(lambda: self.setBrush(4))
        brushLayout.addWidget(self.buttonSelBrushFour)

        self.buttonSelBrushFive = QPushButton('Brush05')
        self.buttonSelBrushFive.clicked.connect(lambda: self.setBrush(5))
        brushLayout.addWidget(self.buttonSelBrushFive)

        self.buttonSelBrushSix = QPushButton('Brush06')
        self.buttonSelBrushSix.clicked.connect(lambda: self.setBrush(6))
        brushLayout.addWidget(self.buttonSelBrushSix)

        self.buttonSelBrushSeven = QPushButton('Brush07')
        self.buttonSelBrushSeven.clicked.connect(lambda: self.setBrush(7))
        brushLayout.addWidget(self.buttonSelBrushSeven)

        self.buttonSelBrushEight = QPushButton('Brush08')
        self.buttonSelBrushEight.clicked.connect(lambda: self.setBrush(8))
        brushLayout.addWidget(self.buttonSelBrushEight)

        self.buttonSelBrushNine = QPushButton('Brush09')
        self.buttonSelBrushNine.clicked.connect(lambda: self.setBrush(9))
        brushLayout.addWidget(self.buttonSelBrushNine)

        self.buttonSelBrushTen = QPushButton('Brush10')
        self.buttonSelBrushTen.clicked.connect(lambda: self.setBrush(10))
        brushLayout.addWidget(self.buttonSelBrushTen)
        
        self.brushGB = QGroupBox("BRUSH")
        self.brushGB.setLayout(brushLayout)
        
        
        brushAndDrawingLayout = QHBoxLayout()
        brushAndDrawingLayout.addWidget(self.brushGB)
        brushAndDrawingLayout.setAlignment(self.brushGB, Qt.AlignTop)
        brushAndDrawingLayout.addWidget(self.drawingTab)
        self.brushAndDrawing = QWidget()
        self.brushAndDrawing.setLayout(brushAndDrawingLayout)
        # /DEFINE BRUSH

    def doPrint(self):
        print('clic')
        
    def setBrush(self, brush):
        print("Brush selected : " + str(brush))
        
    def updateBackground(self, event):
        if event == 1:
            self.drawingZoneUplift.palette.setBrush(QPalette.Background, QBrush(QPixmap(self.drawingZoneTopol.image)))
            self.drawingZoneUplift.setPalette(self.drawingZoneUplift.palette)
        elif event == 2:
            self.drawingZonePrecip.palette.setBrush(QPalette.Background, QBrush(QPixmap(self.drawingZoneTopol.image)))
            self.drawingZonePrecip.setPalette(self.drawingZonePrecip.palette)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    geoPainterWindow = MainWindow()
    geoPainterWindow.show()
    sys.exit(app.exec_())
    
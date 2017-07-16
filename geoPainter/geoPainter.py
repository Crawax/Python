#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

import sys
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QDir
from PyQt5.QtGui import QImage, QPainter, QColor, qRgb, QRadialGradient, QPen, QBrush, QPixmap, QPalette
from PyQt5.QtWidgets import (QAction, QWidget, QMainWindow, QGroupBox, QApplication, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QLayout,
                            QTabWidget)

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
        
        imageSize =  (700, 700)
        
        self.image = QImage(QSize(imageSize[0], imageSize[1]), 5)
        print(self.image.hasAlphaChannel())
        print(self.image.format())
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
        gradient.setColorAt(0.5, QColor.fromRgbF(0, 0, 0, 0));
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
        
        self.drawingZoneTopol = DrawWidget()
        self.drawingZoneUplift = DrawWidget()
        self.drawingZonePrecip = DrawWidget()

        # DEFINE GEOMETRY
        geometryGB = QGroupBox("DEFINE GEOMETRY")
        geometryGBLayout = QGridLayout()
        geometryGBLayout.addWidget(QLabel('Name'),0,0)
        geometryGBLayout.addWidget(QLineEdit(),1,0)
        geometryGBLayout.addWidget(QLabel('res X'),0,1)
        geometryGBLayout.addWidget(QSpinBox(),1,1)
        geometryGBLayout.addWidget(QLabel('res Y'),0,2)
        geometryGBLayout.addWidget(QSpinBox(),1,2)
        geometryGBLayout.addWidget(QLabel('min X'),0,3)
        geometryGBLayout.addWidget(QSpinBox(),1,3)
        geometryGBLayout.addWidget(QLabel('max X'),0,4)
        geometryGBLayout.addWidget(QSpinBox(),1,4)
        geometryGBLayout.addWidget(QLabel('min Y'),0,5)
        geometryGBLayout.addWidget(QSpinBox(),1,5)
        geometryGBLayout.addWidget(QLabel('max Y'),0,6)
        geometryGBLayout.addWidget(QSpinBox(),1,6)
        geometryGBLayout.addWidget(QLabel('min Z'),0,7)
        geometryGBLayout.addWidget(QSpinBox(),1,7)
        geometryGBLayout.addWidget(QLabel('max Z'),0,8)
        geometryGBLayout.addWidget(QSpinBox(),1,8)
        geometryGBLayout.setSizeConstraint(QLayout.SetFixedSize) # Don' take space for no reason
        geometryGB.setLayout(geometryGBLayout)
        # /DEFINE GEOMETRY
        
        # DRAWING
        drawingTab = QTabWidget()
        drawingTab.currentChanged.connect(self.truc)
        drawingTab.addTab(self.drawingZoneTopol,"TOPOLOGY")
        drawingTab.addTab(self.drawingZoneUplift,"UPLIFT")
        drawingTab.addTab(self.drawingZonePrecip,"PRECIPITATION")
        # /DRAWING

        mainVBoxLayout = QVBoxLayout()
        mainVBoxLayout.addWidget(geometryGB)
        mainVBoxLayout.addWidget(drawingTab)

        mainWidget = QWidget(self)
        mainWidget.setLayout(mainVBoxLayout)
        self.setCentralWidget(mainWidget)

        self.setWindowTitle('geoPainter')
        
    def truc(self, event):
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
    
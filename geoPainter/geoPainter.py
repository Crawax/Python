#!/usr/bin/python3
# -*- coding: utf-8 -*-

# With the help of the Scribble.py exemple from PyQt5

from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QDir
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QAction, QWidget

class DrawWidget(QWidget):
    def __init__(self, parent=None):
        super(DrawWidget, self).__init__(parent)
        
        self.setAttribute(Qt.WA_StaticContents)
        
        self.hasChanged = False   # Image has been modified since last save
        self.leftButtonDown = False    # Image is currently being drawn(?)
        
        self.penWidth = 25
        self.penWidthRad = self.penWidth / 2 + 2
        self.penColor = QColor(0,0,0,50)
        
        self.image = QImage()
        self.lastPoint = QPoint()
        
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
            gradient.setColorAt(0, self.myPenColor);
            gradient.setColorAt(0.5, QColor.fromRgbF(0, 0, 0, 0));
            return QPen(QBrush(gradient), self.penWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
           
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
                self.lastPoint(event.pos())
                self.leftButtonDown = True
                
                self.drawPointTo(event.pos())   # Since we can't draw a line with one point, also 
                                                #  draw a point when we start clicking
                self.drawLineTo(event.pos())
                
        def mouseMoveEvent(self, event):
            if (event.buttons() & Qt.LeftButton) and self.leftButtonDown:
                self.drawLineTo(event.pos())
                
        def mouseReleaseEvent(self, event):
            if (event.buttons() & Qt.LeftButton) and self.leftButtonDown:
                self.drawLineTo(event.pos())
                self.leftButtonDown = False
                
        def PaintEvent(self, event):
            painter = QPainter(self)
            dirtyRect = event.rect()
            painter.drawImage(dirtyRect, self.image, dirtyRect)
            
        def resizeEvent(self, event):
            self.resizeImage(self.image, QSize(self.width(), self.height()))
            self.update()
            super(ScribbleArea, self).resizeEvent(event)
            
        def drawPointTo(self, point):
            painter = QPainter(self.image)
            painter.setPen(self.buildPen(point.x(), point.y()))
            painter.drawPoint(point)
            
        def drawLineTo(self, currentPoint):
            painter = QPainter(self.image)
            painter.setPen(self.buildPen(point.x(), point.y()))
            painter.drawLine(self.lastPoint, currentPoint)
            self.hasChanged = True
            
            self.update(Qrect(self.lastPoint, currentPoint).normalized().adjusted(-self.penWidthRad,-self.penWidthRad+self.penWidthRad,+self.penWidthRad))
            self.lastPoint = QPoint(currentPoint)
            
        def resizeImage(self, image, newSize):
            if image.size() == newSize:
                return
                
            newImage = QImage(newSize, QImage.Format_RGB32)
            newImage.fill(qRgb(255, 255, 255))
            
            painter = Qpainter(newImage)
            painter.drawImage(QPoint(0, 0), image) # Ici pour choisir comme redimentionné ?
            
            self.image = newImage
                
                
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
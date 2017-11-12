#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Resize / Rescale : QImage.scaled()

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from enum import Enum
from time import sleep


class myLogo(QLabel):
    def __init__(self, parent=None):
        super(myLogo, self).__init__(parent)
        
        logoB64 = b'''
iVBORw0KGgoAAAANSUhEUgAAAPAAAABkCAMAAACPfE31AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv
8YQUAAAMAUExURQAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA4ODhAQEBERER
ISEhMTExQUFBUVFRYWFhcXFxgYGBkZGRoaGhsbGx0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJ
icnJygoKCkpKSoqKisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTY2Njc3Nzg4ODk5OTo6
Ojs7Ozw8PD09PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1NTU5
OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpaWltbW1xcXF1dXV5eXl9fX2BgYGFhYW
JiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFxcXJycnNzc3R0dHV1d
XZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWFhYaGhoeHh4iIiImJ
iYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYmJmZmZqampubm5ycnJ2
dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2tra6urq+vr7CwsL
GxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwMHBwcLCwsPDw8TEx
MXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY
2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+z
s7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///w
AAAAAAAAAAAM8VglgAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5ld
CA0LjAuMTZEaa/1AAASk0lEQVR4XuWceVxTx9rHe719+7Z3ad+397W399pWyElC2DdB9kVZRAFREAqI
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'''

        logoPM = QPixmap()
        logoPM.loadFromData(QByteArray.fromBase64(logoB64), "PNG")
        self.setPixmap(logoPM)

class myEnum(Enum):
    resizeCanvaCenter = 0
    resizeCanvaLeft = 1
    resizeCanvaTop = 2
    resizeCanvaRight = 3
    resizeCanvaBottom = 4
    resizeDrawing = 5
    english = 20
    french = 21
        
class resizeWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setWindowFlags(Qt.SubWindow)
        self.parentWindowRef = None

        resizeDrawingTitle = QLabel('Resize drawing')
        resizeDrawingTitle.setObjectName('title')
        layoutResizeDrawing = QVBoxLayout()
        layoutResizeDrawing.addWidget(resizeDrawingTitle)

        resizeCanvaTitle = QLabel('Resize canva')
        resizeCanvaTitle.setObjectName('title')
        layoutResizeCanva = QVBoxLayout()
        layoutResizeCanva.addWidget(resizeCanvaTitle)

        mainLayout = QHBoxLayout()
        mainLayout.addItem(layoutResizeDrawing)
        mainLayout.addItem(layoutResizeCanva)

        self.setLayout(mainLayout)
        
        self.setStyleSheet('''
        QLabel#title {
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            font-size: 16px;
        }
        ''') 

    def getMode(self):
        sleep(2)
        self.hide()
        
        return 'machin'
        
class drawWidget(QWidget):
    def __init__(self, parent=None):
        super(drawWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.setLayout(QVBoxLayout())
        self.setContentsMargins(0,0,0,0)
        
        # default value
        self.drawingInProgress = False
        self.drawing = QImage(QSize(0,0), QImage.Format_ARGB32)
        self.drawing.fill(Qt.transparent)
        
        self.setPenColor(Qt.black)
        self.setPenWidth(200)
        background = QImage(self.getDrawingSize(), QImage.Format_ARGB32)
        background.fill(Qt.white)
        self.setBackground(background)
        
    def initLayers(self, layersNumber):
        self.layers = []
        self.layersId = []
        self.layersIdHidden = []
        
        drawingSize = self.getDrawingSize()
        
        for layerId in range(0, layersNumber):
            layer = QImage(drawingSize, QImage.Format_ARGB32)
            layer.fill(Qt.transparent)
            self.layers.append(layer)
            self.layersId.append(layerId)

    def setBrush(self, colors, spacing):
        self.brushColors = []
        for gradientColor in colors:
           colorAlpha = QColor(self.penColor)
           colorAlpha.setAlpha(gradientColor[1])
           self.brushColors.append((gradientColor[0],colorAlpha))
           
        self.brushSpacing = spacing
        
    def initMainWindowRef(self, reference):
        self.mainWindow = reference
        
    def setLayerNumber(self, nbLayer):
        self.layerNumber = nbLayer
        
    def setGradient(self, gradient):
        self.gradient = gradient
        
    def getDrawingSize(self):
        return self.drawing.size()
        
    def setDrawingButton(self, mouseButton):
        self.drawingButton = mouseButton
        
    def resizeDrawing(self, newSize):
        if newSize != self.getDrawingSize():
            self.mergeLayersToDrawing()
        
            currentSize = self.getDrawingSize()
            
            newDrawing = QImage(newSize, QImage.Format_ARGB32)
            newDrawing.fill(Qt.transparent)
            
            painter = QPainter(newDrawing)
            painter.drawImage(QPoint(newSize.width() / 2 - currentSize.width() / 2,
                                     newSize.height() / 2 - currentSize.height() / 2),
                                     self.drawing)
                                     
            self.drawing = newDrawing
            
            
            for layerId in range(0, len(self.layers)):
                newLayer = QImage(newSize, QImage.Format_ARGB32)
                newLayer.fill(Qt.transparent)
                self.layers[layerId] = newLayer
                
            self.setFixedSize(newSize)
        
    def mergeLayersToDrawing(self):
        pass
        
    def rescaleDrawing(self, newSize):
        if newSize != self.getDrawingSize():
            self.setFixedSize(newSize)
        
    def setBackground(self, image):
        self.background = image

    def setPenWidth(self, width):
        self.penWidth = width
        self.penWidthRadius = width / 2 + 2
        
    def setPenColor(self, color):
        self.penColor = color
        
    def paintEvent(self, event):
        self.paintDrawing(event.rect())
        
    def paintDrawing(self, rect):
        painter = QPainter(self)
        painter.drawImage(rect, self.background, rect)
        painter.drawImage(rect, self.drawing, rect)
        
        for layerId in self.layersId:
            painter.drawImage(rect, self.layers[layerId], rect)
        
    def mousePressEvent(self, event):
        if event.button() == self.drawingButton:
            self.startDrawing(event.pos())
            
    def mouseMoveEvent(self, event):
        if self.drawingInProgress:
            self.draw(event.pos())
            
    def mouseReleaseEvent(self, event):
        if event.button() == self.drawingButton and self.drawingInProgress:
            self.stopDrawing()
            
    def stopDrawing(self):
        self.drawingInProgress = False
        self.mergeLastLayerToDrawing()
            
    def draw(self, pointPosition):
        self.path.lineTo(QPointF(pointPosition))
        pathLength = self.path.length()
        while self.pathLastPos < pathLength and pathLength - self.pathLastPos > self.brushSpacing:
            self.drawPoint(self.path.pointAtPercent(self.path.percentAtLength(self.pathLastPos + self.brushSpacing)))
            self.pathLastPos = self.pathLastPos + self.brushSpacing
            
            
    def startDrawing(self, pointPosition):
        self.drawingInProgress = True
        self.mainWindow.drawingHasChanged()
        self.drawPoint(pointPosition)
        self.path = QPainterPath()
        self.path.moveTo(QPointF(pointPosition))
        self.pathLastPos = 0
        
        # Quand on reprend le dessin on supprimer l'historique
        for layerId in self.layersIdHidden:
            self.layers[layerId].fill(Qt.transparent)
            self.layersId.insert(0, layerId)
            
        self.layersIdHidden = []
        
    def drawPoint(self, pointPosition):
        gradient = QRadialGradient(pointPosition, self.penWidth * 0.2)

        for color in self.brushColors:
            gradient.setColorAt(color[0],color[1])
    
        painter = QPainter(self.layers[self.layersId[len(self.layersId) - 1]])
        painter.setPen(QPen(QBrush(gradient),
                       self.penWidth,
                       Qt.SolidLine,
                       Qt.RoundCap,
                       Qt.RoundJoin))

        painter.drawPoint(pointPosition)
        
        x = pointPosition.x()
        y = pointPosition.y()
        self.update(QRect(QPoint(x - self.penWidth,
                                 y - self.penWidth),
                          QPoint(x + self.penWidth,
                                 y + self.penWidth)))
                                 
    def getDrawing(self):
        drawingSize = self.getDrawingSize()
        fullDrawing = QImage(drawingSize, QImage.Format_ARGB32)
        fullDrawing.fill(Qt.white)
        
        painter = QPainter(fullDrawing)
        painter.drawImage(QPoint(drawingSize.width() / 2 - drawingSize.width() / 2,
                                drawingSize.height() / 2 - drawingSize.height() / 2),
                                self.drawing)
                                
        for layerId in self.layersId:
            painter.drawImage(QPoint(drawingSize.width() / 2 - drawingSize.width() / 2,
                                drawingSize.height() / 2 - drawingSize.height() / 2),
                                self.layers[layerId])
        return fullDrawing
        
    def mergeLastLayerToDrawing(self):
        bottomLayerId = self.layersId[0]
        drawingSize = self.getDrawingSize()
        painter = QPainter(self.drawing)
        painter.drawImage(QPoint(drawingSize.width() / 2,
                                 drawingSize.height() / 2),
                                 self.layers[bottomLayerId])

        self.layers[bottomLayerId].fill(Qt.transparent)
        
        self.rotateLayersBackward()
        
    def rotateLayersForward(self):
        self.layersId = self.layersId[len(self.layersId) + 1:] + self.layersId[:len(self.layersId) + 1]

    def rotateLayersBackward(self):
        self.layersId = self.layersId[-len(self.layersId) + 1:] + self.layersId[:-len(self.layersId) + 1]

        
    def undo(self):
        # Top layer is transparent, so we pop the seconde top layer
        self.layersIdHidden.insert(0,self.layersId[len(self.layersId) - 2])
        self.layersId.pop(len(self.layersId) - 2)

        self.update()
    
    def redo(self):
        if not len(self.layersIdHidden) == 0:
            self.layersId.insert(len(self.layersId) - 1, self.layersIdHidden[0])
            self.layersIdHidden.pop(0)
    
        self.update()
    

class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        self.initMenu()
        self.initSettings()
        self.updateWindowTitle()
        self.initDrawings()
        self.initText()
        self.initLayout()
        self.initStyleSheet()
        self.postLaunch()

    def updateWindowTitle(self):
        if self.changedSinceLastSave:
            self.setWindowTitle(self.projectName + '*')
        else:
            self.setWindowTitle(self.projectName)
        
    def postLaunch(self):
        self.changeDrawingSise(myEnum.resizeDrawing)
        
    def initStyleSheet(self):
        self.setStyleSheet('''
        QLabel#title {
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            font-size: 16px;
        }
        QWidget#top, QWidget#brush, QWidget#middleLeft, QWidget#middleRight {
            border: 1px solid black;
            border-radius: 7px;
        } 
        QWidget#widgetTab {
            border: 1px solid black;
            border-bottom: 1px solid black;
            
        } 
        QWidget#widgetTabRes {
            border-bottom: 1px solid black;
        }
        ''') 
    
    def initDrawings(self):
        self.drawings = (
                            {
                            'name': 'Topology',
                            'widget': drawWidget(),
                            'penColor': Qt.black,
                            'mainDrawing': True,
                            'y_min': {'min': 1, 'max': 255,'default': 1},
                            'y_max': {'min': 1, 'max': 255,'default': 255}
                            },
                            {
                            'name': 'Uplift',
                            'widget': drawWidget(),
                            'penColor': Qt.red,
                            'mainDrawing': False,
                            'y_min': {'min': 1, 'max': 255,'default': 1},
                            'y_max': {'min': 1, 'max': 255,'default': 255}
                            },
                            {
                            'name': 'Precipitation',
                            'widget': drawWidget(),
                            'penColor': Qt.cyan,
                            'mainDrawing': False,
                            'y_min': {'min': 1, 'max': 255,'default': 1},
                            'y_max': {'min': 1, 'max': 255,'default': 255}
                            },
                            {
                            'name': 'Erodability',
                            'widget': drawWidget(),
                            'penColor': Qt.green,
                            'mainDrawing': False,
                            'y_min': {'min': 1, 'max': 255,'default': 1},
                            'y_max': {'min': 1, 'max': 255,'default': 255}
                            }
                        )
        for drawingId in range(0,len(self.drawings)):
            if self.drawings[drawingId]['mainDrawing']:
                self.mainDrawingId = drawingId
                break
                            
        background = QImage(QSize(
            self.settings['drawing_width_default'],
            self.settings['drawing_height_default']),
            QImage.Format_ARGB32)
        background.fill(Qt.white)
        
        for drawingId in range(0,len(self.drawings)):
            self.drawings[drawingId]['widget'].initMainWindowRef(self)
            self.drawings[drawingId]['widget'].setPenColor(self.drawings[drawingId]['penColor'])
            self.drawings[drawingId]['widget'].setDrawingButton(self.settings['drawing_button'])
            self.drawings[drawingId]['widget'].setGradient(self.brushs[self.settings['default_brush']])
            self.drawings[drawingId]['widget'].initLayers(self.settings['drawing_layer_number'])
            self.drawings[drawingId]['widget'].resizeDrawing(
                QSize(self.settings['drawing_width_default'], self.settings['drawing_height_default']))
            self.drawings[drawingId]['widget'].setBackground(background)
            self.drawings[drawingId]['widget'].setBrush(self.brushs[self.currentBrushId]['colors'],
                                                        self.brushs[self.currentBrushId]['spacing'])

            

    
    def initSettings(self):
        self.settings = {'res_nx_min': 255,
                         'res_nx_max': 4096,
                         'res_nx_default': 1024,
                         'res_nz_min': 255,
                         'res_nz_max': 4096,
                         'res_nz_default': 1024,
                         'res_x_min': 1,
                         'res_x_max': 9999,
                         'res_x_default': 2000,
                         'res_z_min': 1,
                         'res_z_max': 9999,
                         'res_z_default': 2000,
                         'run_erodability_min': 1,
                         'run_erodability_max': 255,
                         'run_erodability_default': 127,
                         'run_coef_one_min': 1,
                         'run_coef_one_max': 255,
                         'run_coef_one_default': 127,
                         'run_coef_two_min': 1,
                         'run_coef_two_max': 255,
                         'run_coef_two_default': 127,
                         'run_timestep_min': 1,
                         'run_timestep_max': 255,
                         'run_timestep_default': 127,
                         'river_width_min': 1,
                         'river_width_max': 255,
                         'river_width_default': 127,
                         'river_depth_min': 1,
                         'river_depth_max': 255,
                         'river_depth_default': 127,
                         'drawing_width_default': 512,
                         'drawing_height_default': 512,
                         'drawing_button': Qt.LeftButton,
                         'default_brush': 0,
                         'drawing_layer_number': 30,
                         'drawing_has_changed': False,
                         'language': myEnum.english}
        
        self.brushs = [
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,200),
                                   (0.5, 200),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,255),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,50),
                                   (1, 0)],
                        'spacing': 5},
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                       {'colors': [(0 ,150),
                                   (1, 0)],
                        'spacing': 10},
                      ]
        self.currentBrushId = 0
    
        self.projectName = 'New_project'
        self.changedSinceLastSave = False
    
    def initText(self):
        self.text = {myEnum.english:
                        {'res_title': 'Resolution',
                         'res_nx_label': 'nx : ',
                         'res_nx_suffix': ' px',
                         'res_nz_label': 'nz : ',
                         'res_nz_suffix': ' px',
                         'res_x_label': 'x : ',
                         'res_z_label': 'z : ',
                         'res_x_suffix': ' m',
                         'res_z_suffix': ' m',
                         'res_confirm_button': 'Confirm',
                         'style_title': 'Minecraft Graphic Style',
                         'style_one_label': 'Norway',
                         'style_two_label': 'Great Canyon',
                         'style_three_label': 'Tropical',
                         'brush_title': 'Brushs',
                         'brush_button_preffix': 'Brush ',
                         'brush_edit': 'Edit',
                         'drawing_y_min_label': 'min : ',
                         'drawing_y_max_label': 'max : ',
                         'run_erodability_label': ' Erodability',
                         'run_erodability_prefix': 'Kf ',
                         'run_coef_one_prefix': 'm ',
                         'run_coef_one_label': ' Coef 1',
                         'run_coef_two_label': ' Coef 2',
                         'run_coef_two_prefix': 'n ',
                         'run_timestep_label': ' Timestep',
                         'run_timestep_prefix': 'dt ',
                         'run_external_button': 'Run',
                         'river_width_label': 'River width',
                         'river_depth_label': 'River depth',
                         'use_initial_topo_button': 'Use initial Topology',
                         'export_drawing_button': 'Export'}
                    }
        
    def initLayout(self):
        topLayout = QGridLayout()
        self.res_nx = self.buildSpinBox(min=self.settings['res_nx_min'],
                                        max=self.settings['res_nx_max'],
                                        value=self.settings['res_nx_default'],
                                        suffix=self.text[self.settings['language']]['res_nx_suffix'])
        self.res_nz = self.buildSpinBox(min=self.settings['res_nz_min'],
                                        max=self.settings['res_nz_max'], 
                                        value=self.settings['res_nz_default'],
                                        suffix=self.text[self.settings['language']]['res_nz_suffix'])
        self.res_x = self.buildSpinBox(min=self.settings['res_x_min'],
                                       max=self.settings['res_x_max'], 
                                       value=self.settings['res_x_default'],
                                       suffix=self.text[self.settings['language']]['res_x_suffix'])
        self.res_z = self.buildSpinBox(min=self.settings['res_z_min'],
                                       max=self.settings['res_z_max'], 
                                       value=self.settings['res_z_default'],
                                       suffix=self.text[self.settings['language']]['res_z_suffix'])

        self.res_confirm = QPushButton(self.text[self.settings['language']]['res_confirm_button'], self)
        self.res_confirm.clicked.connect(self.changeDrawingSise)
        self.style_buttonGroup = QButtonGroup()
        self.style_one = QRadioButton(self.text[self.settings['language']]['style_one_label'])
        self.style_buttonGroup.addButton(self.style_one)
        self.style_one.setChecked(True)
        self.style_two = QRadioButton(self.text[self.settings['language']]['style_two_label'])
        self.style_buttonGroup.addButton(self.style_two)
        self.style_three = QRadioButton(self.text[self.settings['language']]['style_three_label'])
        self.style_buttonGroup.addButton(self.style_three)
                                      
        topLayout.addWidget(self.buildTitle(self.text[self.settings['language']]['res_title']), 0,0, 1,7)
        # Spacer usefull if the logo size became too small
        topLayout.addItem(QSpacerItem(0,10),                           1, 0)
        topLayout.addWidget(QLabel(self.text[self.settings['language']]['res_nx_label']),         2, 0, Qt.AlignRight)
        topLayout.addWidget(QLabel(self.text[self.settings['language']]['res_nz_label']),         3, 0, Qt.AlignRight)
        topLayout.setRowStretch(5,1)
        topLayout.addWidget(self.res_nx,                               2, 1)
        topLayout.addWidget(self.res_nz,                               3, 1)
        topLayout.addItem(QSpacerItem(25,0),                           1, 2)
        topLayout.addWidget(QLabel(self.text[self.settings['language']]['res_x_label']),          2, 3, Qt.AlignRight)
        topLayout.addWidget(QLabel(self.text[self.settings['language']]['res_z_label']),          3, 3, Qt.AlignRight)
        topLayout.addWidget(self.res_x,                                2, 4)
        topLayout.addWidget(self.res_z,                                3, 4)
        topLayout.addItem(QSpacerItem(20,0),                           1, 5)        
        topLayout.addWidget(self.res_confirm,                          2, 6, 2,1)
        topLayout.addItem(QSpacerItem(15,0),                           1, 7)
        topLayout.addWidget(myLogo(),                                  0, 8, 6,1)
        topLayout.addItem(QSpacerItem(15,0),                           1, 9) 
        topLayout.addWidget(self.buildTitle(self.text[self.settings['language']]['style_title']), 0,10, 1,3)
        topLayout.setColumnStretch(10,1)
        topLayout.addWidget(self.style_one,                            2,11)
        topLayout.addWidget(self.style_two,                            3,11)
        topLayout.addWidget(self.style_three,                          4,11)
        topLayout.setColumnStretch(12,1)
        widgetTop = self.buildWidget(layout=topLayout,
            objName='top', spacing=True)
        
        middleLayout = QHBoxLayout()
        middleLeftLayout = QHBoxLayout()
        brushLayout = QGridLayout()
        brushLayout.setSpacing(0)
        brushLayout.addWidget(self.buildTitle(self.text[self.settings['language']]['brush_title']), 0,0,1,2)
        brushLayout.addItem(QSpacerItem(0,10),                           1, 0)
        brushRow = 2
        self.brushsButton = []
        for brushNb in range(0, len(self.brushs)):
            brushButtonSelect = QPushButton(self.text[self.settings['language']]['brush_button_preffix'] + str(brushNb + 1),self)
            brushButtonSelect.clicked.connect(lambda state, brushId=brushNb: self.brushSelect(brushId))
            brushLayout.addWidget(brushButtonSelect, brushRow, 0)

            brushButtonEdit = QPushButton(self.text[self.settings['language']]['brush_edit'],self)
            brushButtonEdit.clicked.connect(lambda state, brushId=brushNb: self.brushEdit(brushId))
            brushButtonEdit.setMaximumSize(35,100)
            brushLayout.addWidget(brushButtonEdit, brushRow, 1)
            
            self.brushsButton.append({'select': brushButtonSelect,
                'edit': brushButtonEdit})
            
            brushRow = brushRow + 1

        widgetBrush = self.buildWidget(layout=brushLayout,
            objName='brush', spacing=True)
        self.brushSelect(0)
        
        
        middleLelftLeftLayout = QVBoxLayout()
        middleLelftLeftLayout.addWidget(widgetBrush)
        widgetMiddleLeftLeft = self.buildWidget(layout=middleLelftLeftLayout)
        middleLeftLayout.addWidget(widgetMiddleLeftLeft)
        
        
        self.drawingTab = QTabWidget()
        self.drawingTab.currentChanged.connect(self.tabChanged)
        
        
        for drawingId in range(0, len(self.drawings)):
            drawing_y_min = self.buildSpinBox(min=self.drawings[drawingId]['y_min']['min'],
                                              max=self.drawings[drawingId]['y_min']['max'],
                                              value=self.drawings[drawingId]['y_min']['default'])
            drawing_y_max = self.buildSpinBox(min=self.drawings[drawingId]['y_max']['min'],
                                              max=self.drawings[drawingId]['y_max']['max'],
                                              value=self.drawings[drawingId]['y_max']['default'])

            self.drawings[drawingId]['min'] = drawing_y_min
            self.drawings[drawingId]['max'] = drawing_y_max
            
            drawingYLayout = QHBoxLayout()
            drawingYLayout.addWidget(QLabel(self.text[self.settings['language']]['drawing_y_min_label']))
            drawingYLayout.addWidget(self.drawings[drawingId]['min'])
            drawingYLayout.addItem(QSpacerItem(15,0))
            drawingYLayout.addWidget(QLabel(self.text[self.settings['language']]['drawing_y_max_label']))
            drawingYLayout.addWidget(self.drawings[drawingId]['max'])
            drawingYLayout.addStretch(1)
            
            widgetDrawingY = self.buildWidget(layout=drawingYLayout,
                objName='drawingY', spacing=True)

            tabLayout = QVBoxLayout()
            tabLayout.addWidget(widgetDrawingY)
            tabLayout.addWidget(self.drawings[drawingId]['widget'])
            tabLayout.addStretch(1)
            
            widgetTabContent = self.buildWidget(layout=tabLayout, objName='tab')
            widgetTabContent.setContentsMargins(10,10,30,10)
            
            
            tabScrollArea = QScrollArea()
            tabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            tabScrollArea.setWidget(widgetTabContent)
            tabScrollArea.setMinimumSize(550,575)
            
            
            self.drawings[drawingId]['tabIndex'] = self.drawingTab.addTab(tabScrollArea,
                                                    self.drawings[drawingId]['name'])
                                                    
            
        middleLeftLayout.addWidget(self.drawingTab)
        widgetMiddleLeft = self.buildWidget(layout=middleLeftLayout,
                                objName='middleLeft', spacing=True)
        
        self.run_erodability = self.buildSpinBox(min=self.settings['run_erodability_min'],
                                                 max=self.settings['run_erodability_max'],
                                                 value=self.settings['run_erodability_default'],
                                                 prefix=self.text[self.settings['language']]['run_erodability_prefix'])
        self.run_coef_one = self.buildSpinBox(min=self.settings['run_coef_one_min'],
                                              max=self.settings['run_coef_one_max'],
                                              value=self.settings['run_coef_one_default'],
                                              prefix=self.text[self.settings['language']]['run_coef_one_prefix'])
        self.run_coef_two = self.buildSpinBox(min=self.settings['run_coef_two_min'],
                                              max=self.settings['run_coef_two_max'],
                                              value=self.settings['run_coef_two_default'],
                                              prefix=self.text[self.settings['language']]['run_coef_two_prefix'])
        self.run_timestep = self.buildSpinBox(min=self.settings['run_timestep_min'],
                                              max=self.settings['run_erodability_max'],
                                              value=self.settings['run_erodability_default'],
                                              prefix=self.text[self.settings['language']]['run_erodability_prefix'])
        self.run_external = QPushButton(self.text[self.settings['language']]['run_external_button'], self)    
        self.run_external.clicked.connect(self.runExternal)  

        
        runSettingsLayout = QGridLayout()
        runSettingsLayout.addWidget(self.run_erodability, 0,0)
        runSettingsLayout.addItem(QSpacerItem(10,0), 0,1)
        runSettingsLayout.addWidget(QLabel(self.text[self.settings['language']]['run_erodability_label']), 0,2)
        runSettingsLayout.addItem(QSpacerItem(20,0), 0,3)
        runSettingsLayout.addWidget(self.run_coef_two, 0,4)
        runSettingsLayout.addItem(QSpacerItem(10,0), 0,5)
        runSettingsLayout.addWidget(QLabel(self.text[self.settings['language']]['run_coef_two_label']), 0,6)
        
        runSettingsLayout.addWidget(self.run_coef_one, 1,0)
        runSettingsLayout.addItem(QSpacerItem(10,0), 1,1)
        runSettingsLayout.addWidget(QLabel(self.text[self.settings['language']]['run_coef_one_label']), 1,2)
        runSettingsLayout.addItem(QSpacerItem(20,0), 1,3)
        runSettingsLayout.addWidget(self.run_timestep, 1,4)
        runSettingsLayout.addItem(QSpacerItem(10,0), 1,5)
        runSettingsLayout.addWidget(QLabel(self.text[self.settings['language']]['run_timestep_label']), 1,6)
        runSettingsLayout.addItem(QSpacerItem(20,0), 1,7)
        runSettingsLayout.addWidget(self.run_external, 1,8)
        
        widgetRunSettings = self.buildWidget(layout=runSettingsLayout, objName='runSettings')
        
        
        middleRightLayout = QVBoxLayout()
        middleRightLayout.addWidget(widgetRunSettings)
        
        external_preview = QPixmap(QSize(512,512))
        external_preview.fill(Qt.gray)
        self.label_external_preview = QLabel()
        self.label_external_preview.setPixmap(external_preview)
        
        
        middleRightLayout.addWidget(self.label_external_preview)
        
        self.river_width = self.buildSpinBox(min=self.settings['river_width_min'],
                                             max=self.settings['river_width_max'],
                                             value=self.settings['river_width_default'])
        self.river_depth = self.buildSpinBox(min=self.settings['river_depth_min'],
                                             value=self.settings['river_depth_default'],
                                             max=self.settings['river_depth_max'])
                                              
        self.use_initial_topo = QPushButton(self.text[self.settings['language']]['use_initial_topo_button'], self)
        self.use_initial_topo.clicked.connect(self.useInitialTopo) 
        
        self.export_drawing = QPushButton(self.text[self.settings['language']]['export_drawing_button'], self)
        self.export_drawing.clicked.connect(self.exportDrawing) 
        
        bottomRight = QGridLayout()
        bottomRight.addWidget(self.river_width, 0,0)
        bottomRight.addItem(QSpacerItem(10,0), 0,1)
        bottomRight.addWidget(QLabel(self.text[self.settings['language']]['river_width_label']), 0,2)
        bottomRight.addItem(QSpacerItem(10,0), 0,3)
        bottomRight.addWidget(self.use_initial_topo, 0,4)
        
        bottomRight.addWidget(self.river_depth, 1,0)
        bottomRight.addItem(QSpacerItem(10,0), 1,1)
        bottomRight.addWidget(QLabel(self.text[self.settings['language']]['river_depth_label']), 1,2)
        bottomRight.addItem(QSpacerItem(10,0), 1,3)
        bottomRight.addWidget(self.export_drawing, 1,4)
        
        widgetBottomRight = self.buildWidget(layout=bottomRight, objName='bottomRight')
        
        middleRightLayout.addWidget(widgetBottomRight)
        
        widgetMiddleRight = self.buildWidget(layout=middleRightLayout,
            objName='middleRight', spacing=True)
            
            
    
        middleLayout.addWidget(widgetMiddleLeft)
        middleLayout.addItem(QSpacerItem(10,0))
        middleLayout.addWidget(widgetMiddleRight)
        widgetMiddle = self.buildWidget(layout=middleLayout, objName='middle')
        
    
        BottomLayout = QGridLayout()
        #content
        widgetBottom = self.buildWidget(layout=BottomLayout,
            objName='bottom', spacing=True)
   

        
        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralLayoutH = QHBoxLayout(centralWidget)
        centralLayoutV = QVBoxLayout()
        centralLayoutV.addWidget(widgetTop)
        centralLayoutV.addWidget(widgetMiddle)
        centralLayoutV.addWidget(widgetBottom)
        centralLayoutV.addStretch(1)
        centralLayoutH.addLayout(centralLayoutV)
        centralLayoutH.addStretch(1)
        
    def tabChanged(self):
        background = self.drawings[self.mainDrawingId]['widget'].getDrawing()
    
        currentTabId = self.drawingTab.currentIndex()
        for drawingId in range(0,len(self.drawings)):
            self.drawings[drawingId]['widget'].setBrush(self.brushs[self.currentBrushId]['colors'],
                                                        self.brushs[self.currentBrushId]['spacing'])
            if not drawingId == self.mainDrawingId:
                self.drawings[drawingId]['widget'].setBackground(background)
                    
        

    def drawingHasChanged(self):
        self.changedSinceLastSave = True
        self.updateWindowTitle()
        
    def useInitialTopo(self):
        print('useInitialTopo')
        
    def exportDrawing(self):
        print('exportDrawing')
        
    def runExternal(self):
        print('run_external')

    def brushSelect(self, brushId):
        self.brushsButton[self.currentBrushId]['select'].setText(self.text[self.settings['language']]['brush_button_preffix'] + str(self.currentBrushId + 1))
        
        self.brushsButton[brushId]['select'].setText(self.text[self.settings['language']]['brush_button_preffix'] + str(brushId + 1) + ' *')
         
        for drawingId in range(0,len(self.drawings)):
            self.drawings[drawingId]['widget'].setBrush(self.brushs[brushId]['colors'],
                                                        self.brushs[brushId]['spacing'])
        self.currentBrushId = brushId
        
    def brushEdit(self, brushId):
        print('brushSelect -> ' + str(brushId))
        
    def confirmRes(self):
        pass
        
    def changeDrawingSise(self, mode=False):
        '''
        Ask user if resize the drawing or the canva
        '''
        

        ratio = self.res_nz.value() / self.res_nx.value()
        x = self.settings['drawing_width_default']
        y = x * ratio
        
        if not mode:
            myResizeWindow = resizeWindow()
            myResizeWindow.show()
            mode = myResizeWindow.getMode()
            print(mode)



        #for drawingId in range(0, len(self.drawings)):
        #    self.drawings[drawingId]['widget'].resize(mode, QSize(,))

        
        
        

        
        #for drawing in self.drawings:
        #    drawing['widget'].setSize()
        
    def buildTitle(self, titleText):
        title = QLabel(titleText)
        title.setObjectName('title')
        
        return title
   
    def buildWidget(self, layout, objName=False, spacing=False, vStretch=True, hStretch=True):
        widget = QWidget()
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        if not spacing:
            layoutV.setContentsMargins(0,0,0,0)
            layoutV.setSpacing(0)
            layoutH.setContentsMargins(0,0,0,0)
            layoutH.setSpacing(0)
        
        
        layoutV.addLayout(layout)
        if vStretch:
            layoutV.addStretch(1)
        layoutH.addLayout(layoutV)
        if hStretch:
            layoutH.addStretch(1)

        widget.setLayout(layoutH)
        if objName:
            widget.setObjectName(objName)
        
        return widget
        
    def buildSpinBox(self, min, max, value=False ,prefix=False, suffix=False):
        if not value:
            value = min
        spinBox = QSpinBox()
        spinBox.setRange(min,max)
        spinBox.setValue(value)
        if prefix:
            spinBox.setPrefix(prefix + ' ')
        if suffix:
            spinBox.setSuffix(' ' + suffix)

        return spinBox
        
    def buildDoubleSpinBox(self, min, max, value=False, prefix=False, suffix=False):
        if not value:
            value = min
        doubleSpinBox = QDoubleSpinBox()
        doubleSpinBox.setRange(min,max)
        doubleSpinBox.setSingleStep(0.1)
        doubleSpinBox.setValue(value)
        if prefix:
            doubleSpinBox.setPrefix(prefix + " ")
        if suffix:
            doubleSpinBox.setSuffix(' ' + suffix)
        
        return doubleSpinBox

    def initMenu(self):
        self.menuBar().addAction(QAction("&Help ?", self, shortcut="Ctrl+H",
            triggered=self.showHelp))
            
        self.menuBar().addAction(QAction("< Undo", self, shortcut="Ctrl+Z",
            triggered=self.undo))
            
        self.menuBar().addAction(QAction("Redo >", self, shortcut="Ctrl+Y",
            triggered=self.redo))
            
    def showHelp(self):
        print('showHelp')
        
    def undo(self):
        self.drawings[self.drawingTab.currentIndex()]['widget'].undo()
        
    def redo(self):
        self.drawings[self.drawingTab.currentIndex()]['widget'].redo()

if __name__ == '__main__':
    application = QApplication(sys.argv)
    myEnumainter = myMainWindow()
    myEnumainter.show()
    sys.exit(application.exec_())
    
    
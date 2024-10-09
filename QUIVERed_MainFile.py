#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:52:02 2022

@author: caesar
"""

from PyQt5 import QtWidgets #QtGui
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
import sys

import numpy

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

#### FOR 3D drawings
#import pyqtgraph.opengl as gl
####

import GUI_Window
import draggableDots as dD
import drawingQuivers
import unicodeEncoding as uni

PositionsOfVertices = [] # members of this list will have the form {'pos':[x,y]} 
#edgesDrawn = []
selectedVertices = []
#selectedEdges = []
pathBeingFormed = []
pathsFormed = []
pathsFormedReadable = []
directionOfPaths = []
indicesOfSelectedPathsToFormRelation = []

storageRoom = [PositionsOfVertices,selectedVertices,pathBeingFormed,pathsFormed,pathsFormedReadable,indicesOfSelectedPathsToFormRelation]


class MainWindow(QtWidgets.QMainWindow, GUI_Window.Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent=parent)
        self.setupUi(self)
        
        
        self.numOfClicks = None
        
        self.timer = None # in some animations it will become QtCore.QTimer(self)
        
        self.quiverInfo = drawingQuivers.quiver()
        self.adjMatrix = []
        self.adjMatrixEnhanced = []
        self.selectedEdges = {}
        self.vertexLabels=[]
        
        self.storageRoom = [self.selectedEdges]
        
        
        
        #self.graphicsView_QuiverCanvas.setYRange(-1,1)
        
        #self.graphicsView_QuiverCanvas.setLimits(xMin=-5,xMax=5,yMin=-5,yMax=5)
        self.graphicsView_QuiverCanvas.disableAutoRange()
#        self.graphicsView_2.setYRange(self.CP_ylim_down,self.CP_ylim_up)
        self.graphicsView_QuiverCanvas.setAspectLocked(1.0)
        self.graphicsView_QuiverCanvas.hideAxis("left")
        self.graphicsView_QuiverCanvas.hideAxis("bottom")
        
        
        self.quiverVertices = dD.draggableDot()
        self.quiverVertices.setData(pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        
        self.tableWidget_coeffsAndPathsForRel.setData(numpy.array([("","")],dtype=[("Coeff",object),("Path",object)]))
        self.tableWidget_coeffsAndPathsForRel.setColumnWidth(0,55)
        self.tableWidget_coeffsAndPathsForRel.setColumnWidth(1,340)
        self.tableWidget_coeffsAndPathsForRel.setRowCount(0) #self.tableWidget_coeffsAndPathsForRel.removeRow(0) 
        self.tableWidget_coeffsAndPathsForRel.setSortingEnabled(False)
        
        
        
        self.pushButton_PathsLeftToRight.clicked.connect(self.effectOf_pushButton_PathsLeftToRight)
        self.pushButton_PathsRightToLeft.clicked.connect(self.effectOf_pushButton_PathsRightToLeft)
        self.pushButton_DeleteSelectedArrowsOrVertices.clicked.connect(self.effectOf_pushButton_DeleteSelectedArrowsOrVertices)
        self.pushButton_deleteSelectedRecordedPaths.clicked.connect(self.effectOf_pushButton_deleteSelectedRecordedPaths)
        self.pushButton_AddPathToFormRelation.clicked.connect(self.effectOf_pushButton_AddPathToFormRelation)
        self.pushButton_deleteSelectedRowInRelationBeingFormed.clicked.connect(self.effectOf_pushButton_deleteSelectedRowInRelationBeingFormed)
        self.buttonGroup_radioButtons_drawQuiver_recordPathsAndRels.buttonToggled.connect(self.effectOf_buttonGroup_radioButtons_drawQuiver_recordPathsAndRels)

        self.graphicsView_QuiverCanvas.scene().sigMouseClicked.connect(self.quiverConstruction)
        
        #self.quiverVertices.hovered.hover.connect(self.vertexIsHovered)
        self.quiverVertices.Dot.moved.connect(self.moveQuiverAround)
        
#        self.quiverVertices.scatter.sigClicked.connect(self.vertexHasBeenClicked)
                
        self.pushButton_DeleteQuiver.clicked.connect(self.effectOf_pushButton_DeleteQuiver)
        
#    def vertexHasBeenClicked(self,ev):
 #       ev.setData(brush="r")      
        
 
    def effectOf_pushButton_PathsLeftToRight(self):
        directionOfPaths.append("LtoR")
    
    def effectOf_pushButton_PathsRightToLeft(self):
        directionOfPaths.append("RtoL")
 
    def effectOf_pushButton_DeleteQuiver(self):
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        
        self.graphicsView_QuiverCanvas.setAspectLocked(1.0)      
        #self.quiverVertices.scatter.clear()
        self.graphicsView_QuiverCanvas.clear()
        self.quiverVertices = dD.draggableDot()
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        self.quiverVertices.Dot.moved.connect(self.moveQuiverAround)
        for infoStored in storageRoom:
            infoStored.clear()
        for infoStored in self.storageRoom:
            infoStored.clear()
        #self.quiverVertices.dragPoint = None
        #self.quiverVertices.dragOffset = None
        #self.quiverVertices.mypoint_index = None
        #self.quiverVertices.mydata_list = None
        #self.quiverVertices.newPos = None
        self.adjMatrix = []
        self.adjMatrixEnhanced = []
        self.vertexLabels.clear()
        #self.quiverVertices.setData()
        #self.quiverVertices.vertexPositions = []
        #print("positionsinDELETE="+str(self.quiverVertices.vertexPositions))
        
        
        
        
        
        #self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
        #self.quiverVertices.setData(size=self.quiverInfo.vertexRadius, pxMode=True, text=self.vertexLabels)
        
        
        
        
    def vertexIsHovered(self,ev):
        print("indeed")
        

    def adjMatrixEnhancedFromAdjMatrix(self,Matrix,vertexPositions):
        if len(Matrix) == 0:
            result = []
        else:
            MatrixEnhanced = numpy.empty((len(Matrix),len(Matrix)),dtype=object)
            for rowNumber in range(len(Matrix)):
                for columnNumber in range(len(Matrix)):
                    MatrixEnhanced[rowNumber,columnNumber] = []
            #self.graphicsView_QuiverCanvas.clear()
            #self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
            for vertex1 in vertexPositions:
                index1 = vertexPositions.index(vertex1)
                for vertex2 in vertexPositions:
                    index2 = vertexPositions.index(vertex2)
                    if index1 != index2:
                        if Matrix[index1,index2]>0:
                            for arrowIndex in range(Matrix[index1,index2]):
                                
                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))
                                x_coord, y_coord = curve.real, curve.imag
                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                #self.graphicsView_QuiverCanvas.addItem(drawing)
                                #self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                
                                epsilon = 0.000000000001
                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][0]+epsilon]
                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][1]+epsilon]
                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                phantomCurveForAnchoringText.setZValue(1)
                                pointOnPhantomCurve.setZValue(1)
                                #self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                text1 = pg.TextItem("a")
                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                if directionOfPaths[0] == "LtoR":
                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                if directionOfPaths[0] == "RtoL":
                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                text1.setParentItem(pointOnPhantomCurve)
                                text2.setParentItem(pointOnPhantomCurve)
                                text3.setParentItem(pointOnPhantomCurve)
                                #self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                MatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])
                                
                                
                    else:
                        if Matrix[index1,index2]>0:
                            for arrowIndex in range(Matrix[index1,index2]):
                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))
                                x_coord, y_coord = curve.real, curve.imag
                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                #self.graphicsView_QuiverCanvas.addItem(drawing)
                                #self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                
                                epsilon = 0.000000000001
                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][0]+epsilon]
                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(Matrix[index2,index1]))["pos"][1]+epsilon]
                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                phantomCurveForAnchoringText.setZValue(1)
                                pointOnPhantomCurve.setZValue(1)
                                #self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                text1 = pg.TextItem("a")
                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                if directionOfPaths[0] == "LtoR":
                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                if directionOfPaths[0] == "RtoL":
                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                text1.setParentItem(pointOnPhantomCurve)
                                text2.setParentItem(pointOnPhantomCurve)
                                text3.setParentItem(pointOnPhantomCurve)
                                #self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                MatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])      
            result = MatrixEnhanced
        return result
                      

    def addGraphicalItemsToCanvasFromMatrixEnhanced(self,EnhancedMatrix,vertexPositions):
        self.graphicsView_QuiverCanvas.clear()
        points = numpy.array([[vertexPositions[k]['pos'][0],vertexPositions[k]['pos'][1]] for k in range(len(vertexPositions))],dtype=float)
        quiverProperties = self.quiverInfo
        self.vertexLabels = ["%d" % i for i in range(len(vertexPositions))]
        self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels, pen=self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        for index1 in len(EnhancedMatrix):
            for index2 in len(EnhancedMatrix):
                for entry in EnhancedMatrix[index1,index2]:
                    self.graphicsView_QuiverCanvas.addItem(entry)
                
                

        
    def quiverConstruction(self,ev):
        global PositionsOfVertices
        global selectedVertices
        global directionOfPaths
        if len(directionOfPaths) == 0:
            pass
        else:
            if self.radioButton_DrawQuiver.isChecked() == True:
            
                x = self.graphicsView_QuiverCanvas.plotItem.vb.mapSceneToView(ev.scenePos()).x()
                y = self.graphicsView_QuiverCanvas.plotItem.vb.mapSceneToView(ev.scenePos()).y()
                
                roundedVertexPositions = [[round(vertex[0],1),round(vertex[1],1)] for vertex in self.quiverVertices.vertexPositions]  # 1=one decimal digit accuracy
                roundedxy = [round(x,1),round(y,1)]
                                
                
                def singleClick():
                    if self.numOfClicks == 2:
                        self.numOfClicks = None
                    else:
                        # next line for later possible use:
                        # self.numOfClicks = 1
                        print("single click")
                        print(ev.double())
                        
                        if roundedxy not in roundedVertexPositions:
                            selectedVertices.clear()
                            
                            points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                            quiverProperties = self.quiverInfo
                            self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                            self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels, pen=self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
          
                            

                        if len(selectedVertices) < 2 and self.quiverVertices.mypoint_index != None and roundedxy in roundedVertexPositions:
                            selectedVertices.append(self.quiverVertices.mypoint_index)
                            symbolBrushs = [None] * len(self.quiverVertices.vertexPositions)
                            
                            for vertex in selectedVertices: 
                                symbolBrushs[vertex] = pg.mkBrush(color='c')#pg.mkBrush(color=(255, 0, 0))
                            self.vertexLabels = ["%d" % i for i in range(len(self.quiverVertices.mydata_list))]
                            self.quiverVertices.setData(pos=self.quiverVertices.newPos, symbolBrush=symbolBrushs,text=self.vertexLabels)
                            
                        
                        # if len(selectedVertices) == 1 and self.quiverVertices.mypoint_index != None and roundedxy not in roundedVertexPositions:
                        #     print("length="+str(len(selectedVertices)))
                        #     selectedVertices.clear()
                            
                        #     points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                        #     quiverProperties = self.quiverInfo
                        #     self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                        #     self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels, pen=self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
                             

                        if len(selectedVertices) == 2 and self.quiverVertices.mypoint_index != None:
                            i = selectedVertices[0]
                            j = selectedVertices[1]
                            self.adjMatrix[i,j] = self.adjMatrix[i,j]+1
                            
                            for row in self.adjMatrixEnhanced:
                                for entry in row:
                                    if entry != None:
                                        for edge in entry:
                                            self.graphicsView_QuiverCanvas.removeItem(edge[0])
                                            self.graphicsView_QuiverCanvas.removeItem(edge[1])
                                            self.graphicsView_QuiverCanvas.removeItem(edge[2])
                                            self.graphicsView_QuiverCanvas.removeItem(edge[3])
                                        entry.clear()
                                        
                            def update():
                                points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                                quiverProperties = self.quiverInfo
                                self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                                self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels,pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
                                self.timer.stop()
                                
                            if self.timer:
                                self.timer.stop()
                                self.timer.deleteLater()
                            self.timer = QtCore.QTimer(self)
                            self.timer.timeout.connect(update)
                            self.timer.start(750)
                            
                            selectedVertices.clear()                        

                            self.adjMatrixEnhanced = numpy.empty((len(PositionsOfVertices),len(PositionsOfVertices)),dtype=object)
                            for rowNumber in range(len(PositionsOfVertices)):
                                for columnNumber in range(len(PositionsOfVertices)):
                                    self.adjMatrixEnhanced[rowNumber,columnNumber] = []
                            self.graphicsView_QuiverCanvas.clear()
                            self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
                            for vertex1 in self.quiverVertices.vertexPositions:
                                index1 = self.quiverVertices.vertexPositions.index(vertex1)
                                for vertex2 in self.quiverVertices.vertexPositions:
                                    index2 = self.quiverVertices.vertexPositions.index(vertex2)
                                    if index1 != index2:
                                        if self.adjMatrix[index1,index2]>0:
                                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                                
                                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                                x_coord, y_coord = curve.real, curve.imag
                                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                                
                                                epsilon = 0.000000000001
                                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                                phantomCurveForAnchoringText.setZValue(1)
                                                pointOnPhantomCurve.setZValue(1)
                                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                                text1 = pg.TextItem("a")
                                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                                if directionOfPaths[0] == "LtoR":
                                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                                if directionOfPaths[0] == "RtoL":
                                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                                text1.setParentItem(pointOnPhantomCurve)
                                                text2.setParentItem(pointOnPhantomCurve)
                                                text3.setParentItem(pointOnPhantomCurve)
                    #                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])
                                                
                                                
                                    else:
                                        if self.adjMatrix[index1,index2]>0:
                                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                                x_coord, y_coord = curve.real, curve.imag
                                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                                
                                                epsilon = 0.000000000001
                                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                                phantomCurveForAnchoringText.setZValue(1)
                                                pointOnPhantomCurve.setZValue(1)
                                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                                text1 = pg.TextItem("a")
                                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                                if directionOfPaths[0] == "LtoR":
                                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                                if directionOfPaths[0] == "RtoL":
                                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                                text1.setParentItem(pointOnPhantomCurve)
                                                text2.setParentItem(pointOnPhantomCurve)
                                                text3.setParentItem(pointOnPhantomCurve)
                    #                            pointOnPhantomCurve.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                                
                                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])      
                                                
                        for row in self.adjMatrixEnhanced:
                            for entry in row:
                                if entry != None:
                                    for edge in entry:
                                        edge[0].sigClicked.connect(self.edgeClicked)                   
                        self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
                        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
               
                        #self.quiverVertices.selectedVertices.clear()
                        
                    #print(self.adjMatrix)
                    #print(len(self.adjMatrix))
                    
                    self.quiverVertices.mypoint_index = None

                        
                def doubleClick():
                    print("double click")
                    nonlocal x
                    nonlocal y
                    if self.quiverVertices.mypoint_index == None:
                        
                        selectedVertices.clear()
                        
                        PositionsOfVertices.append({'pos':[x,y]})
                        points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                        quiverProperties = self.quiverInfo
                        self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                        self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels)
                        #print(self.quiverVertices.scatter.data.tolist())
                        
                        if len(self.adjMatrix) > 0:
                            newZeroColumn = numpy.array([[0] for l in range(len(self.adjMatrix))])
                            newZeroRow = numpy.array([[0 for l in range(len(self.adjMatrix)+1)]])
                            self.adjMatrix = numpy.hstack((self.adjMatrix,newZeroColumn))
                            self.adjMatrix = numpy.vstack((self.adjMatrix,newZeroRow))
                            self.adjMatrixEnhanced = numpy.empty((len(PositionsOfVertices),len(PositionsOfVertices)),dtype=object)
                            indexOfNewVertex = len(PositionsOfVertices)-1
                            for rowNumber in range(len(PositionsOfVertices)):
                                for columnNumber in range(len(PositionsOfVertices)):
                                    self.adjMatrixEnhanced[rowNumber,columnNumber] = []
                            self.graphicsView_QuiverCanvas.clear()
                            self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
                            for vertex1 in self.quiverVertices.vertexPositions:
                                index1 = self.quiverVertices.vertexPositions.index(vertex1)
                                print("index1="+str(index1))
                                for vertex2 in self.quiverVertices.vertexPositions:
                                    index2 = self.quiverVertices.vertexPositions.index(vertex2)
                                    print("index2="+str(index2))
                                    if index1 != index2:
                                        print("A="+str(self.adjMatrix))
                                        if self.adjMatrix[index1,index2]>0:
                                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                                
                                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                                x_coord, y_coord = curve.real, curve.imag
                                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                                
                                                epsilon = 0.000000000001
                                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                                phantomCurveForAnchoringText.setZValue(1)
                                                pointOnPhantomCurve.setZValue(1)
                                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                                text1 = pg.TextItem("a")
                                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                                if directionOfPaths[0] == "LtoR":
                                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                                if directionOfPaths[0] == "RtoL":
                                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                                text1.setParentItem(pointOnPhantomCurve)
                                                text2.setParentItem(pointOnPhantomCurve)
                                                text3.setParentItem(pointOnPhantomCurve)
                    #                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])
                                                
                                                
                                    else:
                                        if self.adjMatrix[index1,index2]>0:
                                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                                x_coord, y_coord = curve.real, curve.imag
                                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                                
                                                epsilon = 0.000000000001
                                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                                phantomCurveForAnchoringText.setZValue(1)
                                                pointOnPhantomCurve.setZValue(1)
                                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                                text1 = pg.TextItem("a")
                                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                                if directionOfPaths[0] == "LtoR":
                                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                                if directionOfPaths[0] == "RtoL":
                                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                                text1.setParentItem(pointOnPhantomCurve)
                                                text2.setParentItem(pointOnPhantomCurve)
                                                text3.setParentItem(pointOnPhantomCurve)
                    #                            pointOnPhantomCurve.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                                
                                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])      
                                                
                            for row in self.adjMatrixEnhanced:
                                for entry in row:
                                    if entry != None:
                                        for edge in entry:
                                            edge[0].sigClicked.connect(self.edgeClicked)                   
                            self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
                            self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
                   
                            #self.quiverVertices.selectedVertices.clear()
                            
                        #print(self.adjMatrix)
                        #print(len(self.adjMatrix))
                        
                            

                                    
                        if len(self.adjMatrix)==0:
                            self.adjMatrix = numpy.array([[0]])
                            self.adjMatrixEnhanced = None
                            
                    #self.quiverVertices.mypoint_index = None

                        self.quiverVertices.mypoint_index = None
                
                if ev.double() == False:
                    QtCore.QTimer.singleShot(QtWidgets.QApplication.instance().doubleClickInterval(),singleClick)
                    
                else:
                    self.numOfClicks = 2
                    doubleClick()                    
                
                
                    
            
                                         
                
                
                
                                     
                                     
        
            #     if ev.double() == False:
                    
                    
                    

                        
                        
    
            
    def edgeClicked(self,edge):
        if self.radioButton_DrawQuiver.isChecked() == True:
            self.selectedEdges.clear()
            for i in range(len(self.adjMatrixEnhanced)):
                        for j in range(len(self.adjMatrixEnhanced)):
                            for e in self.adjMatrixEnhanced[i,j]:
                                if e[0] is edge:
                                    e[0].setPen('c',width=10)
                                    e[3].setStyle(brush='c',pen='c')
                                    self.selectedEdges[e[0]] = [i,j,self.adjMatrixEnhanced[i,j].index(e)]
                                else:
                                    e[0].setPen(self.quiverVertices.arrowPen)
                                    e[3].setStyle(brush='r',pen='r')
        if self.radioButton_RecordPathsAndRelations.isChecked() == True:
            self.quiverVertices.selectedVertices.clear()
            #selectedEdges.clear()
            for i in range(len(self.adjMatrixEnhanced)):
                        for j in range(len(self.adjMatrixEnhanced)):
                            for e in self.adjMatrixEnhanced[i,j]:
                                if e[0] is edge and directionOfPaths[0] == "RtoL":
                                    if len(pathBeingFormed)>0 and j !=pathBeingFormed[-1][0]:
                                        pass
                                        
                                    if len(pathBeingFormed)>0 and j ==pathBeingFormed[-1][0]:
                                        pathBeingFormed.append([i,j,self.adjMatrixEnhanced[i,j].index(e)])
                                        e[0].setPen('w',width=10)
                                        e[3].setStyle(brush='w',pen='w')
                                        #selectedEdges.append(e) 
                                        
                                    if len(pathBeingFormed)==0:
                                        pathBeingFormed.append([i,j,self.adjMatrixEnhanced[i,j].index(e)])
                                        e[0].setPen('w',width=10)
                                        e[3].setStyle(brush='w',pen='w')
                                        #selectedEdges.append(e)
                                    
                                elif e[0] is edge and directionOfPaths[0] == "LtoR":
                                    if len(pathBeingFormed)>0 and i !=pathBeingFormed[-1][1]:
                                        pass
                                        
                                    if len(pathBeingFormed)>0 and i ==pathBeingFormed[-1][1]:
                                        pathBeingFormed.append([i,j,self.adjMatrixEnhanced[i,j].index(e)])
                                        e[0].setPen('w',width=10)
                                        e[3].setStyle(brush='w',pen='w')
                                        #selectedEdges.append(e) 
                                        
                                    if len(pathBeingFormed)==0:
                                        pathBeingFormed.append([i,j,self.adjMatrixEnhanced[i,j].index(e)])
                                        e[0].setPen('w',width=10)
                                        e[3].setStyle(brush='w',pen='w')
                                        #selectedEdges.append(e)
            
                



        
        

                            
                            

            
            


    
    def moveQuiverAround(self,pt,ind):
        global PositionsOfVertices
        PositionsOfVertices[ind] = {'pos':[pt[0],pt[1]]}
        if ind < len(self.quiverVertices.vertexPositions) :
            self.quiverVertices.vertexPositions[ind] = [pt[0],pt[1]]
        for i in range(len(self.adjMatrixEnhanced)):
            for j in range(len(self.adjMatrixEnhanced)):
                for edge in self.adjMatrixEnhanced[i,j]: 
                    if i == ind or j == ind:
                        index1 = i
                        index2 = j
                        k = self.adjMatrixEnhanced[i,j].index(edge)
                
                        self.graphicsView_QuiverCanvas.removeItem(edge[3])
                        newTipPos = drawingQuivers.quiver().TipFormthArrow(PositionsOfVertices[index1]['pos'],PositionsOfVertices[index2]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))["pos"]
                        newTipAngle = drawingQuivers.quiver().TipFormthArrow(PositionsOfVertices[index1]['pos'],PositionsOfVertices[index2]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))["angle"]
                        edge[3] = pg.ArrowItem(pos = newTipPos, angle = newTipAngle, tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                        self.graphicsView_QuiverCanvas.addItem(edge[3])
                        
                        curve = drawingQuivers.quiver().CurveFormthArrow(PositionsOfVertices[i]['pos'],PositionsOfVertices[j]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))
                        x_coord, y_coord = curve.real, curve.imag
                        edge[0].setData(x_coord,y_coord,pen=self.quiverVertices.arrowPen)
                        
                        epsilon = 0.000000000001
                        vertex1 = PositionsOfVertices[i]['pos']
                        vertex2 = PositionsOfVertices[j]['pos']
                        x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                        y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                        edge[1].setData(x,y,pen=pg.mkPen(color='r', width=0.5))
                        edge[2].setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                        #edge[4].setZValue(1)
                        #edge[5].setZValue(1)

        self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
    
    
    def effectOf_pushButton_DeleteSelectedArrowsOrVertices(self):
        global PositionOfVertices
        global pathsFormedReadable
        if self.radioButton_DrawQuiver.isChecked() == True:
            if len(selectedVertices) == 1:
                j = selectedVertices[0]
                for i in range(len(self.adjMatrixEnhanced)):
                    for e in self.adjMatrixEnhanced[i,j]:
                        self.selectedEdges[e[0]] = [i,j,self.adjMatrixEnhanced[i,j].index(e)]
                    for e in self.adjMatrixEnhanced[j,i]:
                        self.selectedEdges[e[0]] = [j,i,self.adjMatrixEnhanced[j,i].index(e)]
            for graphicCurve in self.selectedEdges:
                i, j, k = self.selectedEdges[graphicCurve][0], self.selectedEdges[graphicCurve][1], self.selectedEdges[graphicCurve][2]
                for path in pathsFormed:
                    if [i, j, k] in path:
                        pathsFormed.remove(path)
                pathsFormedReadable = []
                for path in pathsFormed:
                    if directionOfPaths[0] == "LtoR":
                        pathReadableAsList = ["a"+ uni.sup(str(i)+"-"+str(j))+uni.sub(k) for edge in path]
                    if directionOfPaths[0] == "RtoL":
                        pathReadableAsList = ["a"+ uni.sup(str(j)+"-"+str(i))+uni.sub(k) for edge in path]
                    pathReadableAsString = ""
                    for arrow in pathReadableAsList:
                        if len(pathReadableAsString) == 0:
                            pathReadableAsString = pathReadableAsString + arrow
                        else:
                            pathReadableAsString = pathReadableAsString + " • " + arrow
                    #self.listWidget_RecordedPaths.addItem(pathReadableAsString)
                    pathsFormedReadable.append(pathReadableAsString)
                
                
                for ell in range(len(self.adjMatrixEnhanced[i,j])):
                    self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][0])
                    self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][1])
                    self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][2])
                    self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][3])
                
                self.adjMatrixEnhanced[i,j].clear()
                self.adjMatrix[i,j] = self.adjMatrix[i,j]-1    
                
                index1, index2 = i, j
                vertex1, vertex2 = self.quiverVertices.vertexPositions[i], self.quiverVertices.vertexPositions[j]
                if index1 != index2:
                    if self.adjMatrix[index1,index2]>0:
                        for arrowIndex in range(self.adjMatrix[index1,index2]):
                            
                            curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                            x_coord, y_coord = curve.real, curve.imag
                            drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                            arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                            self.graphicsView_QuiverCanvas.addItem(drawing)
                            self.graphicsView_QuiverCanvas.addItem(arrowTip)
                            
                            epsilon = 0.000000000001
                            x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                            y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                            phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                            pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                            phantomCurveForAnchoringText.setZValue(1)
                            pointOnPhantomCurve.setZValue(1)
                            self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                            text1 = pg.TextItem("a")
                            text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                            if directionOfPaths[0] == "LtoR":
                                text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                            if directionOfPaths[0] == "RtoL":
                                text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                            text1.setParentItem(pointOnPhantomCurve)
                            text2.setParentItem(pointOnPhantomCurve)
                            text3.setParentItem(pointOnPhantomCurve)
#                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                            self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                            self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])
                            
                                    
                else:
                    if self.adjMatrix[index1,index2]>0:
                        for arrowIndex in range(self.adjMatrix[index1,index2]):
                            curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                            x_coord, y_coord = curve.real, curve.imag
                            drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                            arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                            self.graphicsView_QuiverCanvas.addItem(drawing)
                            self.graphicsView_QuiverCanvas.addItem(arrowTip)
                            
                            epsilon = 0.000000000001
                            x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                            y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                            phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                            pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                            phantomCurveForAnchoringText.setZValue(1)
                            pointOnPhantomCurve.setZValue(1)
                            self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                            text1 = pg.TextItem("a")
                            text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                            if directionOfPaths[0] == "LtoR":
                                text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                            if directionOfPaths[0] == "RtoL":
                                text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                            text1.setParentItem(pointOnPhantomCurve)
                            text2.setParentItem(pointOnPhantomCurve)
                            text3.setParentItem(pointOnPhantomCurve)
#                            pointOnPhantomCurve.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                            self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                            
                            self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])      
                            
                for row in self.adjMatrixEnhanced:
                    for entry in row:
                        for edge in entry:
                            edge[0].sigClicked.connect(self.edgeClicked)                   
                self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
                self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        
    
    def keyPressEvent(self,event):
        global PositionsOfVertices
        global pathsFormedReadable
        if self.radioButton_DrawQuiver.isChecked() == True:
            if event.key() == 16777219:# 16777219 is the DELETE key
                print("delete key pressed")
                for graphicCurve in self.selectedEdges:
                    i, j, k = self.selectedEdges[graphicCurve][0], self.selectedEdges[graphicCurve][1], self.selectedEdges[graphicCurve][2]
                    for path in pathsFormed:
                        if [i, j, k] in path:
                            pathsFormed.remove(path)
                    pathsFormedReadable = []
                    for path in pathsFormed:
                        if directionOfPaths[0] == "LtoR":
                            pathReadableAsList = ["a"+ uni.sup(str(i)+"-"+str(j))+uni.sub(k) for edge in path]
                        if directionOfPaths[0] == "RtoL":
                            pathReadableAsList = ["a"+ uni.sup(str(j)+"-"+str(i))+uni.sub(k) for edge in path]
                        pathReadableAsString = ""
                        for arrow in pathReadableAsList:
                            if len(pathReadableAsString) == 0:
                                pathReadableAsString = pathReadableAsString + arrow
                            else:
                                pathReadableAsString = pathReadableAsString + " • " + arrow
                        #self.listWidget_RecordedPaths.addItem(pathReadableAsString)
                        pathsFormedReadable.append(pathReadableAsString)
                    
                    
                    for ell in range(len(self.adjMatrixEnhanced[i,j])):
                        self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][0])
                        self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][1])
                        self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][2])
                        self.graphicsView_QuiverCanvas.removeItem(self.adjMatrixEnhanced[i,j][ell][3])
                    
                    self.adjMatrixEnhanced[i,j].clear()
                    self.adjMatrix[i,j] = self.adjMatrix[i,j]-1    
                    
                    index1, index2 = i, j
                    vertex1, vertex2 = self.quiverVertices.vertexPositions[i], self.quiverVertices.vertexPositions[j]
                    if index1 != index2:
                        if self.adjMatrix[index1,index2]>0:
                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                
                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                x_coord, y_coord = curve.real, curve.imag
                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                
                                epsilon = 0.000000000001
                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                phantomCurveForAnchoringText.setZValue(1)
                                pointOnPhantomCurve.setZValue(1)
                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                text1 = pg.TextItem("a")
                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                if directionOfPaths[0] == "LtoR":
                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                if directionOfPaths[0] == "RtoL":
                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                text1.setParentItem(pointOnPhantomCurve)
                                text2.setParentItem(pointOnPhantomCurve)
                                text3.setParentItem(pointOnPhantomCurve)
    #                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])
                                
                                        
                    else:
                        if self.adjMatrix[index1,index2]>0:
                            for arrowIndex in range(self.adjMatrix[index1,index2]):
                                curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))
                                x_coord, y_coord = curve.real, curve.imag
                                drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                self.graphicsView_QuiverCanvas.addItem(drawing)
                                self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                
                                epsilon = 0.000000000001
                                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                pointOnPhantomCurve = pg.CurvePoint(phantomCurveForAnchoringText)
                                phantomCurveForAnchoringText.setZValue(1)
                                pointOnPhantomCurve.setZValue(1)
                                self.graphicsView_QuiverCanvas.addItem(pointOnPhantomCurve)
                                text1 = pg.TextItem("a")
                                text2 = pg.TextItem(str(arrowIndex), anchor=(-0.4, -0.4))
                                if directionOfPaths[0] == "LtoR":
                                    text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                if directionOfPaths[0] == "RtoL":
                                    text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                text1.setParentItem(pointOnPhantomCurve)
                                text2.setParentItem(pointOnPhantomCurve)
                                text3.setParentItem(pointOnPhantomCurve)
    #                            pointOnPhantomCurve.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,arrowIndex+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                
                                self.adjMatrixEnhanced[index1,index2].append([drawing,phantomCurveForAnchoringText,pointOnPhantomCurve,arrowTip])      
                                
                    for row in self.adjMatrixEnhanced:
                        for entry in row:
                            for edge in entry:
                                edge[0].sigClicked.connect(self.edgeClicked)                   
                    self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
                    self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
    

        if self.radioButton_RecordPathsAndRelations.isChecked() == True:
            if event.key() == 16777220 and len(pathBeingFormed)>0: #16777220 is the ENTER key:
                #path = [[edge[0],edge[1],edge[2]] for edge in pathBeingFormed]
                if directionOfPaths[0] == "LtoR":
                    pathReadableAsList = ["a"+ uni.sup(str(edge[0])+"-"+str(edge[1]))+uni.sub(edge[2]) for edge in pathBeingFormed]
                if directionOfPaths[0] == "RtoL":
                    pathReadableAsList = ["a"+ uni.sup(str(edge[1])+"-"+str(edge[0]))+uni.sub(edge[2]) for edge in pathBeingFormed]
                pathReadableAsString = ""
                for arrow in pathReadableAsList:
                    if len(pathReadableAsString) == 0:
                        pathReadableAsString = pathReadableAsString + arrow
                    else:
                        pathReadableAsString = pathReadableAsString + " • " + arrow
                self.listWidget_RecordedPaths.addItem(pathReadableAsString)
                pathsFormedReadable.append(pathReadableAsString)
                auxTempList = [path for path in pathBeingFormed]
                pathsFormed.append(auxTempList)
                pathBeingFormed.clear()
                for i in range(len(self.adjMatrixEnhanced)):
                    for j in range(len(self.adjMatrixEnhanced)):
                        for e in self.adjMatrixEnhanced[i,j]:
                            e[0].setPen(self.quiverVertices.arrowPen)
                            e[3].setStyle(brush='r',pen='r')
                #print("Paths formed"+str(pathsFormed))
                #print("Paths formed : "+str(pathsFormedReadable))
                
        if event.key() == 16777216: # 16777216 is the ESCAPE key
            selectedVertices.clear()
            self.selectedEdges.clear()
            pathBeingFormed.clear()
            points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
            quiverProperties = drawingQuivers.quiver()
            self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
            self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels,pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
            for i in range(len(self.adjMatrixEnhanced)):
                for j in range(len(self.adjMatrixEnhanced)):
                    for e in self.adjMatrixEnhanced[i,j]:
                        e[0].setPen(self.quiverVertices.arrowPen)
                        e[3].setStyle(brush='r',pen='r')
                
        #if event.key() == 16777249: # 16777249 is the COMMAND key in Mac, CONTROL key in Linux
         #   print("control")
        

    def effectOf_buttonGroup_radioButtons_drawQuiver_recordPathsAndRels(self):
        selectedVertices.clear()
        self.selectedEdges.clear()
        pathBeingFormed.clear()
        points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
        quiverProperties = drawingQuivers.quiver()
        self.vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
        self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=self.vertexLabels,pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
        for i in range(len(self.adjMatrixEnhanced)):
            for j in range(len(self.adjMatrixEnhanced)):
                for e in self.adjMatrixEnhanced[i,j]:
                    e[0].setPen(self.quiverVertices.arrowPen)
                    e[3].setStyle(brush='r',pen='r')
        
    
            
            
    def effectOf_pushButton_deleteSelectedRecordedPaths(self):
        for path in self.listWidget_RecordedPaths.selectedItems():
            self.listWidget_RecordedPaths.takeItem(self.listWidget_RecordedPaths.row(path))
            
        
    def effectOf_pushButton_AddPathToFormRelation(self):
        rowCountSelected = len(self.listWidget_RecordedPaths.selectedItems())
        #self.tableWidget_coeffsAndPathsForRel.setRowCount(rowCountSelected)
        data = numpy.array([("1",self.listWidget_RecordedPaths.selectedItems()[k].text()) for k in range(rowCountSelected)], dtype=[("Coeff",object),("Path",object)])
        self.tableWidget_coeffsAndPathsForRel.appendData(data)
        self.tableWidget_coeffsAndPathsForRel.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        #self.tableWidget_coeffsAndPathsForRel.setData(numpy.array([("","")],dtype=[("Coeff",object),("Path",object)]))
        self.tableWidget_coeffsAndPathsForRel.setColumnWidth(0,55)
        self.tableWidget_coeffsAndPathsForRel.setColumnWidth(1,285)
        #print("printing" + str(self.tableWidget_coeffsAndPathsForRel.item(rowCountSelected-1,1).text()))    #THIS IS HOW ONE EXTRACTS THE TEXT FROM A TABLE ITEM
        
        
        for k in range(rowCountSelected):
            item = self.tableWidget_coeffsAndPathsForRel.item(self.tableWidget_coeffsAndPathsForRel.rowCount()-(k+1),0)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            
            
        
            
            
    def effectOf_pushButton_deleteSelectedRowInRelationBeingFormed(self):
        for selectedRow in self.tableWidget_coeffsAndPathsForRel.selectedItems():
            self.tableWidget_coeffsAndPathsForRel.removeRow(selectedRow.row())
        
            


## The following fixes the "has no attribute 'setCentralWidget' error

#if __name__ == "__main__":
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())


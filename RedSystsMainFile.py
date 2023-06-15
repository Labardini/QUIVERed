#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:52:02 2022

@author: caesar
"""


from PyQt5 import QtGui, QtWidgets
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
import sys

import numpy


import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

from pyqtgraph.ptime import time

#### FOR 3D drawings
#import pyqtgraph.opengl as gl
####





import GUI_Window
import draggableDots as dD
import drawingQuivers
import unicodeEncoding as uni



PositionsOfVertices = [] # members of this list will have the form {'pos'=[x,y]} 
edgesDrawn = []
selectedVertices = []
selectedEdges = []
pathBeingFormed = []
pathsFormed = []
pathsFormedReadable = []
directionOfPaths = []

storageRoom = [PositionsOfVertices,edgesDrawn,selectedEdges,pathBeingFormed,pathsFormed]


class appMainWindow(QtWidgets.QDialog, GUI_Window.Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(appMainWindow,self).__init__(parent)
        self.setupUi(self)
        
        
        self.timer = None # in some animations it will become QtCore.QTimer(self)
        
        self.quiverInfo = drawingQuivers.quiver()
        self.adjMatrix = numpy.array([])
        
        
        
        #self.graphicsView_QuiverCanvas.setYRange(-1,1)
        
        self.graphicsView_QuiverCanvas.setLimits(xMin=-5,xMax=5,yMin=-5,yMax=5)
        self.graphicsView_QuiverCanvas.disableAutoRange()
#        self.graphicsView_2.setYRange(self.CP_ylim_down,self.CP_ylim_up)
        self.graphicsView_QuiverCanvas.setAspectLocked(1.0)
        #self.graphicsView_QuiverCanvas.hideAxis("left")
        #self.graphicsView_QuiverCanvas.hideAxis("bottom")
        
        
        self.quiverVertices = dD.draggableDot()
        self.quiverVertices.setData(pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        
        self.pushButton_PathsLeftToRight.clicked.connect(self.effectOf_pushButton_PathsLeftToRight)
        self.pushButton_PathsRightToLeft.clicked.connect(self.effectOf_pushButton_PathsRightToLeft)
        self.pushButton_deleteSelectedRecordedPaths.clicked.connect(self.effectOf_pushButton_deleteSelectedRecordedPaths)
        self.pushButton_AddPathToFormRelation.clicked.connect(self.effectOf_pushButton_AddPathToFormRelation)
        self.pushButton_deleteSelectedRowInRelationBeingFormed.clicked.connect(self.effectOf_pushButton_deleteSelectedRowInRelationBeingFormed)

        
        
        
        
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
        self.quiverVertices.setData(pos=numpy.array([[0,-100]]))
        self.graphicsView_QuiverCanvas.clear()
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        for infoStored in storageRoom:
            infoStored.clear()
        self.adjMatrix = numpy.array([])
        
        
        
    def vertexIsHovered(self,ev):
        print("indeed")
        
    def quiverConstruction(self,ev):
        global PositionsOfVertices
        global edgesDrawn
        global selectedVertices
        global selectedEdges
        global directionOfPaths
        if len(directionOfPaths) == 0:
            pass
        else:
            if self.radioButton_DrawQuiver.isChecked() == True:
            
                x = self.graphicsView_QuiverCanvas.plotItem.vb.mapSceneToView(ev.scenePos()).x()
                y = self.graphicsView_QuiverCanvas.plotItem.vb.mapSceneToView(ev.scenePos()).y()
                
                
                if ev.double() == True:
                    selectedVertices.clear()
                    
                    if len(self.adjMatrix) > 0:
                        newZeroColumn = numpy.array([[0] for l in range(len(self.adjMatrix))])
                        newZeroRow = numpy.array([[0 for l in range(len(self.adjMatrix)+1)]])
                        self.adjMatrix = numpy.hstack((self.adjMatrix,newZeroColumn))
                        self.adjMatrix = numpy.vstack((self.adjMatrix,newZeroRow))
                    if len(self.adjMatrix)==0:
                        self.adjMatrix = numpy.array([[0]])
        
                    
                    PositionsOfVertices.append({'pos':[x,y]})
                    points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                    quiverProperties = drawingQuivers.quiver()
                    vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                    self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=vertexLabels)
                    #print(self.quiverVertices.scatter.data.tolist())
                
                
                
                if len(selectedVertices) < 2 and self.quiverVertices.mypoint_index != None:
                    selectedVertices.append(self.quiverVertices.mypoint_index)
                    symbolBrushs = [None] * len(self.quiverVertices.vertexPositions)
                    print(selectedVertices)
                    for vertex in selectedVertices: 
                        symbolBrushs[vertex] = pg.mkBrush(color='c')#pg.mkBrush(color=(255, 0, 0))
                    vertexLabels = ["%d" % i for i in range(len(self.quiverVertices.mydata_list))]
                    self.quiverVertices.setData(pos=self.quiverVertices.newPos, symbolBrush=symbolBrushs,text=vertexLabels)
                    print(selectedVertices)
                
                roundedVertexPositions = [[round(vertex[0],1),round(vertex[1],1)] for vertex in self.quiverVertices.vertexPositions]  # 1=one decimal digit accuracy
                roundedxy = [round(x,1),round(y,1)]
                if len(selectedVertices) == 1 and self.quiverVertices.mypoint_index != None and roundedxy not in roundedVertexPositions :
                    selectedVertices.clear()
                    points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                    quiverProperties = drawingQuivers.quiver()
                    vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                    self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=vertexLabels,pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
                   
                if len(selectedVertices) == 2 and self.quiverVertices.mypoint_index != None:
                    i = selectedVertices[0]
                    j = selectedVertices[1]
                    self.adjMatrix[i,j] = self.adjMatrix[i,j]+1
                    for edge in edgesDrawn:
                        self.graphicsView_QuiverCanvas.removeItem(edge[3])
                        self.graphicsView_QuiverCanvas.removeItem(edge[4])
                        self.graphicsView_QuiverCanvas.removeItem(edge[5])
                        self.graphicsView_QuiverCanvas.removeItem(edge[6])
                    edgesDrawn.clear()
                    
                    for vertex1 in self.quiverVertices.vertexPositions:
                        index1 = self.quiverVertices.vertexPositions.index(vertex1)
                        for vertex2 in self.quiverVertices.vertexPositions:
                            index2 = self.quiverVertices.vertexPositions.index(vertex2)
                            if index1 != index2:
                                if self.adjMatrix[index1,index2]>0:
                                    for k in range(self.adjMatrix[index1,index2]):
                                        
                                        curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))
                                        x_coord, y_coord = curve.real, curve.imag
                                        drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                        arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                        self.graphicsView_QuiverCanvas.addItem(drawing)
                                        self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                        
                                        epsilon = 0.000000000001
                                        x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                        y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                        phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                        curvePoint = pg.CurvePoint(phantomCurveForAnchoringText)
                                        phantomCurveForAnchoringText.setZValue(1)
                                        curvePoint.setZValue(1)
                                        self.graphicsView_QuiverCanvas.addItem(curvePoint)
                                        text1 = pg.TextItem("a")
                                        text2 = pg.TextItem(str(k), anchor=(-0.4, -0.4))
                                        if directionOfPaths[0] == "LtoR":
                                            text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                        if directionOfPaths[0] == "RtoL":
                                            text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                        text1.setParentItem(curvePoint)
                                        text2.setParentItem(curvePoint)
                                        text3.setParentItem(curvePoint)
            #                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                        self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                        
                                        edgesDrawn.append([index1,index2,k,drawing,phantomCurveForAnchoringText,curvePoint,arrowTip])
                                        
                                        
                            else:
                                if self.adjMatrix[index1,index2]>0:
                                    for k in range(self.adjMatrix[index1,index2]):
                                        
                                        curve = drawingQuivers.quiver().CurveFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))
                                        x_coord, y_coord = curve.real, curve.imag
                                        drawing = pg.PlotCurveItem(x_coord,y_coord,pen=self.quiverVertices.arrowPen,clickable=True)
                                        arrowTip = pg.ArrowItem(pos = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"], angle = drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["angle"], tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                                        self.graphicsView_QuiverCanvas.addItem(drawing)
                                        self.graphicsView_QuiverCanvas.addItem(arrowTip)
                                        
                                        epsilon = 0.000000000001
                                        x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                                        y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                                        phantomCurveForAnchoringText = pg.PlotCurveItem(x,y,pen=pg.mkPen(color='r', width=0.5))
                                        curvePoint = pg.CurvePoint(phantomCurveForAnchoringText)
                                        phantomCurveForAnchoringText.setZValue(1)
                                        curvePoint.setZValue(1)
                                        self.graphicsView_QuiverCanvas.addItem(curvePoint)
                                        text1 = pg.TextItem("a")
                                        text2 = pg.TextItem(str(k), anchor=(-0.4, -0.4))
                                        if directionOfPaths[0] == "LtoR":
                                            text3 = pg.TextItem("("+str(index1)+","+str(index2)+")",anchor=(-0.15, 0.4))
                                        if directionOfPaths[0] == "RtoL":
                                            text3 = pg.TextItem("("+str(index2)+","+str(index1)+")",anchor=(-0.15, 0.4))
                                        text1.setParentItem(curvePoint)
                                        text2.setParentItem(curvePoint)
                                        text3.setParentItem(curvePoint)
            #                            curvePoint.setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                                        self.graphicsView_QuiverCanvas.addItem(phantomCurveForAnchoringText)
                                        
                                        edgesDrawn.append([index1,index2,k,drawing,phantomCurveForAnchoringText,curvePoint,arrowTip])
                                        
                                        
                                        
                    for edge in edgesDrawn:
                        edge[3].sigClicked.connect(self.edgeClicked)                   
                    self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
                    self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
                    selectedVertices.clear()
            
                    #self.quiverVertices.selectedVertices.clear()
                    
                #print(self.adjMatrix)
                #print(len(self.adjMatrix))
                    
                    def update():
                        points = numpy.array([[PositionsOfVertices[k]['pos'][0],PositionsOfVertices[k]['pos'][1]] for k in range(len(PositionsOfVertices))],dtype=float)
                        quiverProperties = drawingQuivers.quiver()
                        vertexLabels = ["%d" % i for i in range(len(PositionsOfVertices))]
                        print("done waiting")
                        self.quiverVertices.setData(pos=points, size=quiverProperties.vertexRadius, pxMode=True, text=vertexLabels,pen =self.quiverVertices.vertexPen, brush=self.quiverVertices.vertexBrush)
                        self.timer.stop()
                        
                    if self.timer:
                        self.timer.stop()
                        self.timer.deleteLater()
                    self.timer = QtCore.QTimer(self)
                    self.timer.timeout.connect(update)
                    self.timer.start(500)
            
    def edgeClicked(self,edge):
        if self.radioButton_DrawQuiver.isChecked() == True:
            selectedEdges.clear()
            for e in edgesDrawn:
                if e[3] is edge:
                    e[3].setPen('c',width=10)
                    e[6].setStyle(brush='c',pen='c')
                    selectedEdges.append(e)
                else:
                    e[3].setPen(self.quiverVertices.arrowPen)
                    e[6].setStyle(brush='r',pen='r')
        if self.radioButton_RecordPathsAndRelations.isChecked() == True:
            self.quiverVertices.selectedVertices.clear()
            #selectedEdges.clear()
            for e in edgesDrawn:
                if e[3] is edge and directionOfPaths[0] == "RtoL":
                    if len(pathBeingFormed)>0 and e[1]!=pathBeingFormed[-1][0]:
                        pass
                        
                    if len(pathBeingFormed)>0 and e[1]==pathBeingFormed[-1][0]:
                        pathBeingFormed.append(e)
                        e[3].setPen('w',width=10)
                        e[6].setStyle(brush='w',pen='w')
                        #selectedEdges.append(e) 
                        
                    if len(pathBeingFormed)==0:
                        pathBeingFormed.append(e)
                        e[3].setPen('w',width=10)
                        e[6].setStyle(brush='w',pen='w')
                        #selectedEdges.append(e)
                    
                elif e[3] is edge and directionOfPaths[0] == "LtoR":
                    if len(pathBeingFormed)>0 and e[0]!=pathBeingFormed[-1][1]:
                        pass
                        
                    if len(pathBeingFormed)>0 and e[0]==pathBeingFormed[-1][1]:
                        pathBeingFormed.append(e)
                        e[3].setPen('w',width=10)
                        e[6].setStyle(brush='w',pen='w')
                        #selectedEdges.append(e) 
                        
                    if len(pathBeingFormed)==0:
                        pathBeingFormed.append(e)
                        e[3].setPen('w',width=10)
                        e[6].setStyle(brush='w',pen='w')
                        #selectedEdges.append(e)
            
                



        
        

                            
                            

            
            


    
    def moveQuiverAround(self,pt,ind):
        global PositionsOfVertices
        global edgesDrawn
        PositionsOfVertices[ind] = {'pos':[pt[0],pt[1]]}
        if ind < len(self.quiverVertices.vertexPositions) :
            self.quiverVertices.vertexPositions[ind] = [pt[0],pt[1]]
        for edge in edgesDrawn:
            if edge[0] == ind or edge[1] == ind:
                index1 = edge[0]
                index2 = edge[1]
                k = edge[2]
        
                self.graphicsView_QuiverCanvas.removeItem(edge[6])
                newTipPos = drawingQuivers.quiver().TipFormthArrow(PositionsOfVertices[index1]['pos'],PositionsOfVertices[index2]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))["pos"]
                newTipAngle = drawingQuivers.quiver().TipFormthArrow(PositionsOfVertices[index1]['pos'],PositionsOfVertices[index2]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))["angle"]
                edge[6] = pg.ArrowItem(pos = newTipPos, angle = newTipAngle, tipAngle = drawingQuivers.quiver().tipAngle, baseAngle = drawingQuivers.quiver().baseAngle, headLen = drawingQuivers.quiver().headLen, tailLen = drawingQuivers.quiver().tailLen, tailWidth = None, pen =self.quiverVertices.arrowPen, brush = 'r')
                self.graphicsView_QuiverCanvas.addItem(edge[6])
                
                curve = drawingQuivers.quiver().CurveFormthArrow(PositionsOfVertices[edge[0]]['pos'],PositionsOfVertices[edge[1]]['pos'],k+numpy.sign(self.adjMatrix[index2,index1]))
                x_coord, y_coord = curve.real, curve.imag
                edge[3].setData(x_coord,y_coord,pen=self.quiverVertices.arrowPen)
                
                epsilon = 0.000000000001
                vertex1 = PositionsOfVertices[edge[0]]['pos']
                vertex2 = PositionsOfVertices[edge[1]]['pos']
                x = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][0]+epsilon]
                y = [drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1],drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1]+epsilon]
                edge[4].setData(x,y,pen=pg.mkPen(color='r', width=0.5))
                edge[5].setPos(drawingQuivers.quiver().TipFormthArrow(vertex1,vertex2,k+numpy.sign(self.adjMatrix[index2,index1]))["pos"][1])
                #edge[4].setZValue(1)
                #edge[5].setZValue(1)

        self.graphicsView_QuiverCanvas.removeItem(self.quiverVertices)
        self.graphicsView_QuiverCanvas.addItem(self.quiverVertices)
        
    def keyPressEvent(self,event):
        global PositionsOfVertices
        if self.radioButton_DrawQuiver.isChecked() == True:
            if event.key() == 16777219:# 16777219 is the DELETE key
                for edge in selectedEdges:
                    i, j = edge[0], edge[1]
                    for arrow in edgesDrawn:
                        if arrow[0] == i and arrow[1] == j and arrow[2] == self.adjMatrix[i,j]-1:
                            self.graphicsView_QuiverCanvas.removeItem(arrow[3])
                            self.graphicsView_QuiverCanvas.removeItem(arrow[4])
                            self.graphicsView_QuiverCanvas.removeItem(arrow[5])
                            self.graphicsView_QuiverCanvas.removeItem(arrow[6])
                            edgesDrawn.remove(arrow)
                    
                    edge[3].setPen(self.quiverVertices.arrowPen)
                    edge[6].setStyle(brush='r',pen='r')
                    self.adjMatrix[i,j] = self.adjMatrix[i,j]-1    
                    selectedEdges.remove(edge)
    

        if self.radioButton_RecordPathsAndRelations.isChecked() == True:
            if event.key() == 16777220 and len(pathBeingFormed)>0: #16777220 is the ENTER key:
                path = [[edge[0],edge[1],edge[2]] for edge in pathBeingFormed]
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
                pathsFormed.append(path)
                pathBeingFormed.clear()
                for e in edgesDrawn:
                    e[3].setPen(self.quiverVertices.arrowPen)
                    e[6].setStyle(brush='r',pen='r')
                #print("Paths formed"+str(pathsFormed))
                print("Paths formed : "+str(pathsFormedReadable))
            
    def effectOf_pushButton_deleteSelectedRecordedPaths(self):
        for path in self.listWidget_RecordedPaths.selectedItems():
            self.listWidget_RecordedPaths.takeItem(self.listWidget_RecordedPaths.row(path))
            
        
    def effectOf_pushButton_AddPathToFormRelation(self):
        for path in self.listWidget_RecordedPaths.selectedItems():
            self.listWidget_Path.addItem(path.text())
            item = QtWidgets.QListWidgetItem("1")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.listWidget_Coefficient.addItem(item)
            ##self.listWidget_Coefficient.setEditTriggers(QtWidgets.QAbstractItemView.SelectedClicked)
            #item = self.listWidget_Coefficient.setCurrentRow(len(self.listWidget_Coefficient))
            
    def effectOf_pushButton_deleteSelectedRowInRelationBeingFormed(self):
        for path in self.listWidget_Path.selectedItems():
            self.listWidget_Coefficient.takeItem(self.listWidget_Path.row(path))
            self.listWidget_Path.takeItem(self.listWidget_Path.row(path))
            
        
            
            

        
        
          
        
            
                       
        
        
app = QtWidgets.QApplication(sys.argv)
form = appMainWindow()
form.show()
app.exec_()

#if __name__ == "__main__":            
#    app = QtWidgets.QApplication(sys.argv)
#    form = appMainWindow()
#    form.show()
#    app.exec_()
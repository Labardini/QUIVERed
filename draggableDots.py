#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 18:46:31 2018

@author: daniellabardini
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy




class DotDragSignal(QtCore.QObject):
    moved = QtCore.pyqtSignal(object,int)

    def __init__(self, pt, ind):
        QtCore.QObject.__init__(self)
        self._pt = pt
        self._ind = ind

    @property
    def pt(self):
        return self._pt
    
    @property
    def ind(self):
        return self._ind

    
    @pt.setter
    def pt(self, new_pt):
        self._pt = new_pt
        self.moved.emit(new_pt,self.ind)
        
    @ind.setter
    def ind(self, new_ind):
        self._ind = new_ind





class draggableDot(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.Dot = DotDragSignal([0,0],-1)
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)
        self.selectedVertices = []
        self.vertexPositions = []
        #self.arrows=[]
        self.arrowPen = pg.mkPen(color='r', width=3)
        self.vertexBrush = pg.mkBrush(color='r')
        self.vertexPen = pg.mkPen(color='r')
        self.mypoint_index = None
        self.mydata_list = None
        self.newPos = None
        
    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = numpy.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = numpy.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()
        #print(self.scatter.data.tolist())
        
    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t, anchor=(0.5, 0.5))
            self.textItems.append(item)
            item.setParentItem(self)
        
    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        
        
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])
        
        
    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return
        
        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first 
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.Dot.ind = ind
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return
        
        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.Dot.pt = self.data['pos'][ind]
        self.updateGraph()
        ev.accept()
        
#    def clicked(self, pts):
#        print("clicked: %s" % pts)



    def clicked(self, scatter, pts):
        data_list = scatter.data.tolist()
        self.mydata_list = data_list
        mypoint = [tup for tup in data_list if pts[0] in tup][0]
        self.mypoint_index = data_list.index(mypoint)

 
#        mypoint_edges = [tup for tup in self.data['adj'] if mypoint_index in tup]
    
        data = scatter.getData()
        
        self.newPos = numpy.vstack([data[0],data[1]]).transpose()
        self.vertexPositions = [[position[0],position[1]] for position in self.newPos]
        
 #       newLines = lines.copy()

     #   if len(self.selectedVertices) == 2:
      #      self.arrows.append([self.selectedVertices[0],self.selectedVertices[1]])
        #print(self.arrows)
        #adj = numpy.array([pair for pair in self.arrows if len(self.arrows)>0])
        #print(adj)
        
            
#        for i in range(len(mypoint_edges)):
 #           for j in range(len(adj)):
  #              if numpy.array_equal(adj[j], mypoint_edges[i]):
   #                 break
    #        index = j
     #       newLines.itemset(index, (255,0,0,255,1))
#        g.setData(pos=newPos, adj=adj, pen=newLines, size=1, symbol=symbols, pxMode=False, text=texts, symbolBrush=symbolBrushs)

      #  if len(self.arrows)>0:
            #self.setData(pos=newPos, symbolBrush=symbolBrushs,text=vertexLabels, adj=adj, pen=self.arrowPen)
       #     self.setData(pos=newPos, symbolBrush=symbolBrushs,text=vertexLabels, pen=self.arrowPen)
        self.updateGraph()
        

                        












#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:32:29 2022

@author: daniellabardini
"""

import numpy as np

class planeGeometry:
    
    def __init__(self):
        pass
    
    def coordsR2ToC(self,listWithTwoRealNumbers): # the input is an ordered list of two real numbers
        x, y = listWithTwoRealNumbers[0], listWithTwoRealNumbers[1]
        return x+(y*(1j))
    
    def coordsCToR2(self,complexNumber):
        return [complexNumber.real,complexNumber.imag]
    
    
    def angleRadiansToDegrees(self,complexNumber):
        return np.angle(complexNumber)*180/np.pi
         
    
 

class quiver:
    
    
    def __init__(self):
        self.Plane = planeGeometry()
        self.vertexRadius = 40
        self.vertexShape = 'o'
        self.tipAngle = 40
        self.baseAngle = 10
        self.headLen = 20
        self.tailLen = None
        self.arrows=[]

    
    
    def CurveFormthArrowAsAFunction(self,initPt,finalPt,m): #the inputs are pairs (length-2 lists) of real numbers, and a non-negative integer
        z0, z1 = self.Plane.coordsR2ToC(initPt), self.Plane.coordsR2ToC(finalPt)
        midPoint = (z0+z1)/2
        halfdifference =(z0-z1)/2
        if m == 0:
            def paramCurve(t):
                return z0 + t*(z1-z0)/np.pi
        elif m >0 :
            def paramCurve(t):
                adHocParam = 1/5
                return midPoint + halfdifference * np.cos(t) + (m) * halfdifference *(1j) * adHocParam * np.sin(t)
        return paramCurve
        
    
    def CurveFormthArrow(self,initPt,finalPt,m): #the inputs are pairs (length-2 lists) of real numbers, and a non-negative integer
        interval = np.linspace(0,np.pi,50)
        curveAsFunction = self.CurveFormthArrowAsAFunction(initPt,finalPt,m)
        return curveAsFunction(interval)
        
        
        
        
        
        
        
        
    
    def TipFormthArrow(self,initPt,finalPt,m): # the inputs are pairs (length-2 lists) of real numbers, and a non-negative integers
        z0, z1 = self.Plane.coordsR2ToC(initPt), self.Plane.coordsR2ToC(finalPt)
        evaluationPointForTip = 0.525*np.pi #in the interval 0-pi
        if m == 0:
            position = [(z0 + evaluationPointForTip*(z1-z0)/np.pi).real, (z0 + evaluationPointForTip*(z1-z0)/np.pi).imag]
            angle = 180 - self.Plane.angleRadiansToDegrees(z1-z0)
        elif m >0 :
            position = [self.CurveFormthArrowAsAFunction(initPt,finalPt,m)(evaluationPointForTip).real,self.CurveFormthArrowAsAFunction(initPt,finalPt,m)(evaluationPointForTip).imag]
            halfdifference =(z0-z1)/2
            adHocParam = 1/3
            tangentVector = (halfdifference * (-np.sin(evaluationPointForTip))) + (m * halfdifference *(1j) * adHocParam * np.cos(evaluationPointForTip))
            angle = 180-self.Plane.angleRadiansToDegrees(tangentVector)
        dictionary = {"pos":position,"angle":angle}
        return dictionary
        
        
        
        
        
    
    
    # def arrowTip(self,initPt,finalPt): #the inputs are pairs (length-2 lists) of real numbers, the output is in degrees
    #     z0, z1 = self.Plane.coordsR2ToC(initPt), self.Plane.coordsR2ToC(finalPt)
    #     angle = self.Plane.angleRadiansToDegrees(z1-z0)
    #     position = z1-(np.cos(np.angle(z1-z0))+(np.sin(np.angle(z1-z0))*(1j)))*self.vertexRadius
    #     return [angle, position]
    
    # def arrow(self,initPt,finalPt): #the inputs are pairs (length-2 lists) of real numbers
    #     dictionary = {"source":initPt,"target":finalPt,"arrowTip":self.arrowTip(initPt,finalPt)}
    #     self.arrows.append(dictionary)
        
    
        
        
        
    
    
 
    

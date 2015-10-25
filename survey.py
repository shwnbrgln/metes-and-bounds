# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 20:38:01 2014

@author: SB
"""
from __future__ import print_function
from __future__ import division

from math import *
import simplekml
import declination


class Survey:
    
    M_DEG_LAT = 111091.0 #constant meters per degree of latidute
    RADIUS_M = 6356752.3 #constant earth radius in meters (~for poles)
    FEET_M = 3.28083989    
    
    M_deg_lon = 81637.0 # meters per degree of longitude a fn(latitude)    
    latitude = 0
    longitude = 0
    dd = 0 #decimal degrees
    declination = 0
    history = []  #a list of tuples; appended with coordinates of points when pen is down
    penDownState = False    
    
    
    def __init__(self,longitude,latitude,year,anglefudge=0):
        self.latitude = latitude
        self.longitude = longitude
        try:        
            self.declination = declination.calc_declination(longitude,latitude,2013)
        except:
            print ("WARNING: using 0 degrees as the delination value: ",self.declination)            
        
        #print (self.declination)
        self.declination += anglefudge
        self.kml = simplekml.Kml()  
        #self.M_deg_lon = self.lengthPerDegLon(self.latitude)
        
    def newPoint(self,longitude,latitude):
        self.latitude = latitude
        self.longitude = longitude
        if self.penDownState: self.storePoint()
    
    def lengthPerDegLon(self,latitude):
        circumatlat = cos(radians(latitude))*self.RADIUS_M*2.0*pi #this is cicumfrance
        # meters at the latitude given
        return circumatlat/360.0

    def storePoint(self):
        print(self.latitude, ",", self.longitude) 
        self.history.append((self.longitude,self.latitude))
        #print(self.v, self.degslat, self.minslat, self.secslat)
        #print(self.h, self.degslon, self.minslon, self.secslon)
        
    #def okml(self,okmlname):
        #print(self.latitude, ",", self.longitude) 
       # self.kml.newpoint(name=okmlname, Surveys=[(self.longitude,self.latitude)])
        #print(self.v, self.degslat, self.minslat, self.secslat)
        #print(self.h, self.degslon, self.minslon, self.secslon)        
    
        
    def decimalDegrees(self,d,minutes,s,quadrant):
        self.dd = d + minutes/60.0 + s/3600.0                
        if quadrant == "wn":
            self.dd += 90 - self.declination
        if quadrant == "ws":
            self.dd = 270 - self.dd - self.declination
        if quadrant == "es":
            self.dd += 270 - self.declination
        if quadrant == "en":
            self.dd = 90 - self.dd - self.declination   
            
        if quadrant not in ["wn","ws","es","en"]: 
            print("ERROR in quadrant")
            return 0
        return self.dd
        
    def dms(self,dd):
        return int(dd),(int(dd*60)%60),((dd*3600)%60)

    def move(self,dd,m):
        print("move:",self.m_to_ft(m), "ft",dd, "deg")
        y = sin(radians(dd))*m
        x = cos(radians(dd))*m
        self.latitude += (y / self.M_DEG_LAT)          
        self.longitude += (x / self.M_deg_lon)
        if self.penDownState: self.storePoint()
            #print(self.latitude, ",", self.longitude) 
        return self.longitude,self.latitude 
     
    def m_to_ft(self,m): return m*self.FEET_M

    def ft_to_m(self,ft): return ft/self.FEET_M     

    def writekml(self,filename):
        #self.kml.newlinestring(name="Pathway", description="A path round the yard",
                        #Surveys=self.history)        
        #self.history
        self.kml.save(filename)
    
    def penUp(self,namestring, linetype = 0):
        print("pen up")        
        self.lin = self.kml.newlinestring(name=("path"+namestring), description=namestring,
                        coords=self.history)        
        if linetype == 0:
            self.lin.style.linestyle.color = simplekml.Color.lightyellow
            self.lin.style.linestyle.width = 2
            #self.lin.style.linestyle.dashed
        if linetype == 1:
            self.lin.style.linestyle.color = simplekml.Color.darkgray
            self.lin.style.linestyle.width = .25
            
        self.history[:] = []
        #self.history
        #self.kml.save(filename)    
        self.penDownState = False
        
    def penDown(self):
        print ("pen down")
        self.storePoint()
        self.penDownState = True

    def markPoint(self,label):
        print ("ok")
        self.pnt = self.kml.newpoint(name=label, coords=[(self.longitude,self.latitude)])
 

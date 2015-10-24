# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 21:11:52 2014

@author: SB


###############################################################################
This function gets the declination using webservices hosted  
by the National Oceanic and Atmospheric Administration (NOAA)

Declination is a function of latitude and longitude and date
There are some limits on the numbers of times you can use the webservice per
second etc.
###############################################################################
"""

import requests
from xml.etree import ElementTree

def calc_declination(longitude, latitude, year):

    longitude = "%.4f"%longitude
    latitude = "%.4f"%latitude
    startYear = "%.4f"%year

    URL = "http://www.ngdc.noaa.gov/geomag-web/calculators/calculate\
Declination?lat1=" + latitude + "&lon1=" + longitude + "&startYear=" + startYear + "&resultFormat=xml"

    XMLresponse = requests.get(URL)
    declination = ElementTree.fromstring(XMLresponse.content)[0][4].text
    return float(declination)
    
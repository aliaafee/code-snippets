#!/usr/bin/python

from math import *

def rad(deg):
	return deg/180.0*pi

def deg(rad):
	return rad/pi*180.0

def julianDate(second,minute,hour,day,month,year):
	# day, month, year of gregorian calender
	# method: http://en.wikipedia.org/wiki/Julian_Day
	a = (14 - month)/12
	y = year + 4800 - a
	m = month + (12 * a) - 3
	julianDateNumber = day + ((153*m+2)/5) + (365*y) + (y/4) - (y/100) + (y/400) - 32045
	julianDate = julianDateNumber + ((hour-12.0)/24.0) + (minute/1440.0) + (second/86400.0)
	return float(julianDate)
	
def julianCycle(day,month,year,longitudeWest):
	#longitudeWest-> west=+,east=-
	n1 = julianDate(0,0,12,day,month,year) - 2451545 - 0.0009 + (longitudeWest/360)
	julianCycle = round(n1)
	return julianCycle
	
def apporximateSolarNoon(longitudeWest,julianCycle):
	return 2451545 + 0.0009 + longitudeWest/360 + julianCycle
	
def solarMeanAnomaly(approximateSolarNoon):
	return rad((357.5291 + 0.98560028*(approximateSolarNoon-2451545))%360)
	
def equationOfCenter(solarMeanAnomaly):
	return (1.9148*sin(solarMeanAnomaly))+(0.02*sin(2*solarMeanAnomaly))+(0.0003*sin(3*solarMeanAnomaly))
	
def eclipticLongitude(solarMeanAnomaly,equationOfCenter):
	return rad((deg(solarMeanAnomaly)+102.9372+equationOfCenter+180)%360.0)

def solarTransit(julianCycle,solarMeanAnomaly,eclipticLongitude):
	return julianCycle+(0.0053*sin(solarMeanAnomaly))-(0.0069*sin(2*eclipticLongitude))
	
def declinationOfSun(eclipticLongitude):
	return asin(sin(eclipticLongitude)*sin(rad(23.45)))
	
def hourAngle(declinationOfSun,latitude):
	#latitude->north=+,south=-
	latitude = rad(latitude)
	return (sin(rad(-0.83))-(sin(latitude)*sin(declinationOfSun)))/(cos(latitude)*cos(declinationOfSun))

def getSunset(day,month,year,latitude,longitude):
	longitudeWest = -1 * longitude
	julianCycle_ = julianCycle(day,month,year,longitudeWest)
	approximateSolarNoon_ = apporximateSolarNoon(longitudeWest,0)
	solarMeanAnomaly_ = solarMeanAnomaly(approximateSolarNoon_)
	equationOfCenter_ = equationOfCenter(solarMeanAnomaly_)
	eclipticLongitude_ = eclipticLongitude(solarMeanAnomaly_,equationOfCenter_)
	declinationOfSun_ = declinationOfSun(eclipticLongitude_)
	hourAngle_ = hourAngle(declinationOfSun_,latitude)
	
	return 2451545+0.0009+(deg(hourAngle_)+longitudeWest)/360+julianCycle_+(0.0053*sin(solarMeanAnomaly_))-(0.0069*sin(2*eclipticLongitude_))


if __name__ == '__main__':
    print getSunset(6,9,2009,85.366669,27.700001)

#!/usr/bin/python2.7
import string
from lib.url_maker import UrlMaker
from lib.requester import Requester
from lib.analyser import Analyser
from lib.proxy import Proxy
from lib.data_model import DataModel

objProxy = Proxy()
objUrlMaker = UrlMaker()
objRequester = Requester()
objAnalyser = Analyser()
objDataModel = DataModel()

def getProxyPath():
	'''Get the Proxie info into the object proxy'''
	global objProxy
	while not objProxy.getProxieList():
		proxiePath = raw_input('Please enter the proxie info path / URL:\n')
		if proxiePath == '':
			proxiePath = './source/proxie'
		objProxy.setProxiePath(proxiePath)
	else:
		count = len(objProxy.getProxieList())
		print 'Get proxie info list success! There are %s proxie info find!'%(count)

def setCity():
	'''Set the city'''
	global objUrlMaker
	global objRequester
	global objProxy

	cityName = raw_input('Please enter the city name: ')
	objRequester.setProxy(objProxy.getAvailableProxy())
	objRequester.request(objUrlMaker.makeUrlByCityName(cityName))
	objAnalyser.analysisJson(objRequester.getData())
	cityList = objAnalyser.analysisList()
	count = 1
	for i in cityList:
		print '#%d'%count
		count += 1
		print 'Area name: ', i['address']
		'''
		startLongitude = i['lat_lon_box']['north']
		endLongitude = i['lat_lon_box']['south']
		startLatitude = i['lat_lon_box']['east']
		endLatitude = i['lat_lon_box']['west']
		'''
		startLatitude = i['lat_lon_box']['north']
		endLatitude = i['lat_lon_box']['south']
		startLongitude = i['lat_lon_box']['east']
		endLongitude = i['lat_lon_box']['west']
		print 'North range: ', startLongitude
		print 'South range: ', endLongitude
		print 'East range: ', startLatitude
		print 'West range: ', endLatitude
		print 'The area is about %f km2'%((startLongitude - endLongitude) * 111 + (startLatitude - endLatitude) * 111)
		print '-' * 60

	cityId = raw_input('Please chose the number of the city: ')
	index = string.atoi(cityId) - 1
	print 'You chose the city: %s'%(
		cityList[index]['address']
	)
	initDatabase(
		#startLongitude,
		cityList[index]['lat_lon_box']['west'],
		#startLatitude,
		cityList[index]['lat_lon_box']['north'],
		#endLongitude,
		cityList[index]['lat_lon_box']['east'],
		#endLatitude,
		cityList[index]['lat_lon_box']['south'],
		#startLongitude,
		cityList[index]['lat_lon_box']['west'],
		#startLatitude
		cityList[index]['lat_lon_box']['north']
	)
	return True

def initDatabase(
	startLongitude,
	startLatitude,
	endLongitude,
	endLatitude, 
	nowLongitude,
	nowLatitude
):
	global objDataModel
	objDataModel.initDatabase(
		startLongitude,
		startLatitude,
		endLongitude,
		endLatitude,
		nowLongitude,
		nowLatitude
	)

def main():
	global objProxy

	getProxyPath()
	if setCity():
		print 'Init success!'


if __name__ == '__main__':
	main()
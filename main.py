#!/usr/lib/python2.7
from lib.url_maker import UrlMaker
from lib.requester import Requester
from lib.analyser import Analyser
from lib.proxy import Proxy
from lib.data_model import DataModel
from lib.controller import Controller

objProxy = Proxy()
objUrlMaker = UrlMaker()
objRequester = Requester()
objAnalyser = Analyser()
objDataModel = DataModel()
objController = Controller()

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

def getConfig():
	'''Get the longitude and latitude config into
	the object DataModel.'''
	global objDataModel
	objDataModel.connectDatabase()
	return objDataModel.getConfig()

def getUsefullProxy(switch = False):
	'''Get the usefull proxy info. And set the proxy into the object requester.'''
	global objProxy
	global objRequester
	global objUrlMaker
	global objAnalyser

	foo = True
	while foo == True:
		if switch == True:
			switch = False
			objProxy.getNextProxy()
		proxy = objProxy.getAvailableProxy()
		print 'Check proxy: %s'%(proxy)
		objRequester.setProxy(proxy)
		objRequester.request(objUrlMaker.getTestUrl())
		if objRequester.getStatus() != 200:
			continue
		objAnalyser.analysisJson(objRequester.getData())
		if objAnalyser.analysisData():
			foo = False
	return proxy

def main():
	global objUrlMaker
	global objController
	global objRequester
	global objAnalyser
	global objDataModel

	# Get the proxie list into the object proxy
	getProxyPath()

	# Get usefull proxy
	proxy = getUsefullProxy()
	print proxy
	configList = getConfig()
	objController.init(
		configList[1],
		configList[2],
		configList[3],
		configList[4],
		configList[5],
		configList[6]
	)

	toBecontinue = True
	done = False
	errorTimes = 0
	while toBecontinue:
		if done == True:
			break
		if objController.checkIfFinished():
			done = True

		print '-'*50
		url = objUrlMaker.makeUrlByPointList(objController.getPoint())
		print 'Fetching url: %s'%(url)
		objRequester.request(url)
		print 'HTTP status: %s'%(objRequester.getStatus())
		if objRequester.getStatus() != 200:
			if errorTimes >= 5:
				errorTimes = 0
				proxy = getUsefullProxy()
				continue
			errorTimes += 1
			continue

		rate = objController.getRate()
		print "Longitude rate: %s Latitude rate: %s"%(rate['longitude'], rate['latitude'])
		objAnalyser.analysisJson(objRequester.getData())
		if not objAnalyser.analysisData():
			print 'Analysis data error'
			if errorTimes >= 5:
				errorTimes = 0
				objController.move()
				continue
			errorTimes += 1
			continue

		if not objDataModel.checkIfDiff(objAnalyser.getDataList()):
			# There is the same data in the database.
			print 'There is the same data in the database.'
			objDataModel.savePoint(objController.getPoint())
			objController.move()
			continue

		objDataModel.addData(objAnalyser.getDataList())
		objDataModel.savePoint(objController.getPoint())
		print '###############################'
		print '###### Add a new address ######'
		print '###############################'
		objController.move()

#--------------------------------------------------------------------- The entry
if __name__ == '__main__':
	main()
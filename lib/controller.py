#!/usr/bin/python2.7
class Controller:
	__startLongitude = False
	__startLatitude = False
	__endLongitude = False
	__endLatitude = False
	__nowLongitude = False
	__nowLatitude = False
	__i = 0.0001
	__forwardLongitude = 1
	__forwardLatitude = 1

	def init(
		self,
		startLongitude,
		startLatitude,
		endLongitude,
		endLatitude,
		nowLongitude,
		nowLatitude
	):
		self.__startLongitude = startLongitude
		self.__startLatitude = startLatitude
		self.__endLongitude = endLongitude
		self.__endLatitude = endLatitude
		self.__nowLongitude = nowLongitude
		self.__nowLatitude = nowLatitude
		self.__analysisRate()

	def __analysisRate(self):
		self.__forwardLongitude = self.__analysisForward(
			self.__startLongitude,
			self.__endLongitude
		)
		self.__forwardLatitude = self.__analysisForward(
			self.__startLatitude,
			self.__endLatitude
		)

	def __analysisForward(self, start, end):
		result = end - start
		if result < 0:
			return -1
		else:
			return 1

	def getPoint(self):
		nowPointList = ["%3.4f"%self.__nowLongitude, "%3.4f"%self.__nowLatitude]
		return nowPointList

	def move(self):
		if "%3.4f"%self.__nowLongitude == "%3.4f"%self.__endLongitude:
			self.__nowLongitude = self.__startLongitude
			self.__moveToNextLatitude()
		else:
			self.__moveToNextLongitude()

	def checkIfFinished(self):
		if (self.__startLatitude - self.__nowLatitude) > (self.__startLatitude - self.__endLatitude):
			return True
		else:
			return False

	def getRate(self):
		longitudeRate = '%3.2f%%'%(
			(1 - (self.__endLongitude - self.__nowLongitude) /
				 (self.__endLongitude - self.__startLongitude)
			)*100
		)
		latitudeRate = '%3.2f%%'%(
			(1 - (self.__endLatitude - self.__nowLatitude) /
				 (self.__endLatitude - self.__startLatitude)
			)*100
		)
		return {'longitude': longitudeRate, 'latitude': latitudeRate}

	def __moveToNextLongitude(self):
		self.__nowLongitude += self.__forwardLongitude * self.__i

	def __moveToNextLatitude(self):
		self.__nowLatitude += self.__forwardLatitude * self.__i
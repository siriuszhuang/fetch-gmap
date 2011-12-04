class UrlMaker:
	__baseUrl = 'http://maps.google.com/maps/geo?'
	__output = 'json'
	__key = 'abcdefg'
	__testUrl = 'http://maps.google.com/maps/geo?q=30.6352010,104.0888760&output=json&key=abcdefg'

	def getTestUrl(self):
		return self.__testUrl

	def makeUrlByPointList(self, pointList):
		return "%sq=%s,%s&output=%s"%(
			self.__baseUrl,
			pointList[1],
			pointList[0],
			self.__output
		)

	def makeUrlByCityName(self, cityName):
		return "%sq=%s"%(
			self.__baseUrl,
			cityName
		)
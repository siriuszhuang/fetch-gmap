#!/usr/bin/python2.7
import httplib

class Requester:
	__proxy = False
	__url = False
	__headers = {"Accept-Language": "zh-cn"}
	__data = False
	__status = False

	def setProxy(self, proxy):
		self.__proxy = proxy

	def __initResult(self):
		self.__data = False
		self.__status = False

	def request(self, url):
		self.__url = url
		self.__initResult()
		if not self.__request():
			return False
		return True

	def getStatus(self):
		return self.__status

	def __request(self):
		http = httplib.HTTPConnection(
			self.__proxy,
			timeout = 5
		)
		try:
			http.request(
				'get',
				self.__url,
				headers = self.__headers
			)
			result = http.getresponse()
			self.__status = result.status
			self.__data = result.read()
		except:
			print 'Failed request!'
			return False

	def getData(self):
		return self.__data
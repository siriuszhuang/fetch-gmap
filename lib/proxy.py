#!/usr/lib/python2.7
import re
import httplib

class Proxy:
	__proxiePath = ''
	__proxieList = []
	__proxieIndex = 0
	__proxieUrlRe = '[a-zA-z]+://[^\s]*'
	__proxiePathRe = '^[\.]{0,2}[/w-]+'
	__proxyRe = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
	__headers = {"Accept-Language": "zh-cn"}

	def setProxiePath(self, path):
		self.__proxiePath = path

	def getProxieList(self):
		if self.__proxieList:
			return self.__proxieList
		if self.__proxiePath:
			if self.__analysisProxie():
				return self.__proxieList
		return False

	def __analysisProxie(self):
		if re.search(self.__proxieUrlRe, self.__proxiePath):
			pass
		elif re.search(self.__proxiePathRe, self.__proxiePath):
			self.__loadProxieFile()
		else:
			return False
		return True

	def __loadProxieFile(self):
		try:
			fileHandle = open(self.__proxiePath, 'r')
			content = fileHandle.read()
		except:
			return False
		fileHandle.close()
		self.__analysisText(content)

	def __analysisText(self, text):
		match = re.compile(self.__proxyRe)
		list = match.findall(text)
		for v in list:
			self.__proxieList.append(v)

	def getAvailableProxy(self):
		proxy = self.__getProxy()
		while not self.__testConnection(proxy):
			self.getNextProxy()
			proxy = self.__getProxy()
		else:
			return proxy

	def getNextProxy(self):
		if self.__proxieIndex == len(self.__proxieList):
			self.__proxieIndex = 0
		else:
			self.__proxieIndex += 1

	def __getProxy(self):
		if self.__proxieIndex == len(self.__proxieList):
			self.__proxieIndex = 0
		return self.__proxieList[self.__proxieIndex]

	def __testConnection(self, proxy):
		http = httplib.HTTPConnection(
			proxy,
			timeout = 5
		)
		try:
			http.request(
				'get',
				'http://maps.google.com/maps/geo?q=30.6352010,104.0888760&output=json&key=abcdefg',
				headers = self.__headers
			)
			response = http.getresponse()
		except:
			return False

		status = response.status
		if status == 200:
			return True
		else:
			return False
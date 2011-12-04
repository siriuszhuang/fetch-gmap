#!/usr/bin/python2.7
import MySQLdb

class DataModel:
	__dbHost = '127.0.0.1'
	__dbPort = 3306
	__dbUser = 'root'
	__dbPassword = 'zsrzsr1989'
	__dbDatabase = 'gmap_data'
	__dbTable = 'gmap_data'
	__dbConfTable = 'gmap_config'
	__dbLink = False
	__dbCursor = False

	def __init__(self):
		return

	def __createDatabase(self):
		self.__dbLink = MySQLdb.connect(
			host = self.__dbHost,
			user = self.__dbUser,
			passwd = self.__dbPassword
		)
		try:
			self.__dbCursor = self.__dbLink.cursor()
			self.__dbCursor.execute('CREATE DATABASE IF NOT EXISTS`%s`'%(self.__dbDatabase))
		except:
			print 'Database create faild.'
			exit()
		return True

	def __createTable(self):
		self.__dbLink.select_db(self.__dbDatabase)
		try:
			self.__dbCursor.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
	`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`address` varchar(255) CHARACTER SET utf8 NOT NULL,
	`administrative_area_name` varchar(255) CHARACTER SET utf8 NOT NULL,
	`locality_name` varchar(255) CHARACTER SET utf8 NOT NULL,
	`dependent_locality_name` varchar(255) CHARACTER SET utf8 NOT NULL,
	`thoroughfare_name` varchar(255) CHARACTER SET utf8 NOT NULL,
	`longitude` float(8,4) NOT NULL,
	`latitude` float(8,4) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `address` (`address`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;'''%(self.__dbTable))
			self.__dbCursor.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
	`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`start_longitude` float(8,4) NOT NULL,
	`start_latitude` float(8,4) NOT NULL,
	`end_longitude` float(8,4) NOT NULL,
	`end_latitude` float(8,4) NOT NULL,
	`now_longitude` float(8,4) NOT NULL,
	`now_latitude` float(8,4) NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;'''%(self.__dbConfTable))
		except:
			print 'Table create faild.'
			exit()
		return

	def initDatabase(
		self,
		startLongitude,
		startLatitude,
		endLongitude,
		endLatitude,
		nowLongitude,
		nowLatitude
	):
		self.__createDatabase()
		self.__createTable()
		try:
			self.__dbCursor.execute('''INSERT INTO `%s`
(`start_longitude`, `start_latitude`, `end_longitude`, `end_latitude`, `now_longitude`, `now_latitude`)
VALUES
("%s", "%s", "%s", "%s", "%s", "%s")'''%(
					self.__dbConfTable,
					startLongitude,
					startLatitude,
					endLongitude,
					endLatitude,
					nowLongitude,
					nowLatitude
				)
			)
		except:
			print 'Insert init config data error.'
			exit()

	def connectDatabase(self):
		'''	Connect MySQL. And choose the database'''
		self.__dbLink = MySQLdb.connect(
			host = self.__dbHost,
			user = self.__dbUser,
			passwd = self.__dbPassword,
			db = self.__dbDatabase,
			port = self.__dbPort
		)
		try:
			self.__dbCursor = self.__dbLink.cursor()
			self.__dbCursor.execute('SET NAMES utf8')
		except:
			print 'Database connect error.'
			exit()

	def getConfig(self):
		query = 'SELECT * FROM `%s` WHERE `id` = 1'%(self.__dbConfTable)
		query = query.encode('utf8')
		self.__dbCursor.execute(query)
		return self.__dbCursor.fetchone()

	def addData(self, dataList):
		query = '''INSERT INTO `%s`
(`%s`, `%s`, `%s`, `%s`, `%s`, `%s`, `%s`)
VALUES
("%s", "%s", "%s", "%s", "%s", "%s", "%s")'''%(
			self.__dbTable,
			'address',
			'administrative_area_name',
			'locality_name',
			'dependent_locality_name',
			'thoroughfare_name',
			'longitude',
			'latitude',
			dataList['address'],
			dataList['administrative_area_name'],
			dataList['locality_name'],
			dataList['dependent_locality_name'],
			dataList['thoroughfare_name'],
			dataList['longitude'],
			dataList['latitude']
		)
		query = query.encode('utf8')
		try:
			self.__dbCursor.execute(query)
		except:
			return False
		return True

	def savePoint(self, pointList):
		query = '''UPDATE `%s` SET `now_longitude` = "%s", `now_latitude` = "%s"'''%(
			self.__dbConfTable,
			pointList[0],
			pointList[1]
		)
		query = query.encode('utf8')
		try:
			self.__dbCursor.execute(query)
		except:
			return False
		return True

	def checkIfDiff(self, dataList):
		'''	Return true if there is not the same
		address in the database.'''

		query = 'SELECT `id` FROM `%s` WHERE `address` = "%s"'%(
			self.__dbDatabase,
			dataList['address']
		)
		query = query.encode('utf8')
		n = self.__dbCursor.execute(query)
		if n == 0:
			return True
		else:
			return False

	def __del__(self):
		if self.__dbCursor:
			self.__dbCursor.close()
		if self.__dbLink:
			self.__dbLink.close()
		print 'Database link is closed.'
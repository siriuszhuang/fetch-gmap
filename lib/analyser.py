#!/usr/bin/pytohn2.7
import json

class Analyser:
	__data = False
	__dataList = False
	__dataStatus = 0
	__placeList = []

	def analysisJson(self, result):
		try:
			self.__data = json.loads(result)
		except:
			return False
		return True

	def analysisList(self):
		if self.__checkDataType():
			if self.__checkDataStatus():
				if self.__checkHasPlaceMark():
					return self.__analysisPlaceList()
		return False

	def __analysisPlaceList(self):
		for i in self.__placemark:
			self.__analysisData(i)
			self.__placeList.append(self.__dataList)
		return self.__placeList

	def analysisData(self):
		if self.__checkDataType():
			if self.__checkDataStatus():
				print 'Data status: %d'%(self.__dataStatus)
				if self.__checkHasPlaceMark():
					return self.__analysisData(self.__placemark[0])
		return False

	def getDataList(self):
		return self.__dataList

	def __checkDataStatus(self):
		self.__dataStatus = self.__data['Status']['code']
		if self.__dataStatus == 200:
			return True
		return False

	def getDataStatus(self):
		return self.__dataStatus;

	def __checkDataType(self):
		if type(self.__data) == type({}):
			return True
		return False

	def __checkHasPlaceMark(self):
		if self.__data.has_key('Placemark'):
			self.__placemark = self.__data['Placemark']
			return True
		return False

	def __analysisData(self, placemark):
		self.__dataList = []
		address = '{<unknown>}'
		longitude = '{<unknown>}'
		latitude = '{<unknown>}'
		administrativeAreaName = '{<unknown>}'
		localityName = '{<unknown>}'
		dependentLocalityName = '{<unknown>}'
		thoroughfareName = '{<unknown>}'
		latLonBox = []

		if placemark.has_key('address'):
			# address
			address = placemark['address']
			if placemark.has_key('Point'):
				if placemark['Point'].has_key('coordinates'):
					point = placemark['Point']['coordinates']
					# longitude
					longitude = point[0]
					# latitude
					latitude = point[1]
			if placemark.has_key('ExtendedData'):
				if placemark['ExtendedData'].has_key('LatLonBox'):
					northRange = placemark['ExtendedData']['LatLonBox']['north']
					southRange = placemark['ExtendedData']['LatLonBox']['south']
					eastRange = placemark['ExtendedData']['LatLonBox']['east']
					westRange = placemark['ExtendedData']['LatLonBox']['west']
					latLonBox = {
						'north': northRange,
						'south': southRange,
						'east': eastRange,
						'west': westRange
					}

			if placemark.has_key('AddressDetails'):
				addressDetails = placemark['AddressDetails']
				if (addressDetails.has_key('Country') and
					addressDetails['Country'].has_key('AdministrativeArea')
				):
					# administrativeAreaName
					administrativeAreaName = addressDetails['Country']['AdministrativeArea']['AdministrativeAreaName']
					if (addressDetails['Country']['AdministrativeArea'].has_key('Locality') and
						addressDetails['Country']['AdministrativeArea']['Locality'].has_key('LocalityName')
					):
						# localityName
						localityName = addressDetails['Country']['AdministrativeArea']['Locality']['LocalityName']
						if (addressDetails['Country']['AdministrativeArea']['Locality'].has_key('DependentLocality') and
							addressDetails['Country']['AdministrativeArea']['Locality']['DependentLocality'].has_key('DependentLocalityName')
						):
							# dependentLocalityName
							dependentLocalityName = addressDetails['Country']['AdministrativeArea']['Locality']['DependentLocality']['DependentLocalityName']
							if (addressDetails['Country']['AdministrativeArea']['Locality']['DependentLocality'].has_key('Thoroughfare') and
								addressDetails['Country']['AdministrativeArea']['Locality']['DependentLocality']['Thoroughfare'].has_key('ThoroughfareName')
							):
								# thoroughfareName
								thoroughfareName = addressDetails['Country']['AdministrativeArea']['Locality']['DependentLocality']['Thoroughfare']['ThoroughfareName']

			self.__dataList = {
				'address': address,
				'longitude': longitude,
				'latitude': latitude,
				'administrative_area_name': administrativeAreaName,
				'locality_name': localityName,
				'dependent_locality_name': dependentLocalityName,
				'thoroughfare_name': thoroughfareName,
				'lat_lon_box': latLonBox
			}
			return True
		return False
from urllib3 import (PoolManager,)
from json import (dumps,)


class Network(object,):
	def __init__(self,):
		self.__request = PoolManager()

	def post(self, url, data = None, json = None, headers = None,):
		if data and headers != None:
			return self.__request.request(method = 'POST', url = url, data = data.encode('utf-8'), headers = headers)

		elif json and headers != None:
			return self.__request.request('POST', str(url), body = dumps(json).encode('utf-8'), headers = headers)

		elif json != None:
			return self.__request.request(method = 'POST', url = url, headers = {'Content-Type': 'application/json'}, body = dumps(json).encode())

		elif data != None:
			return self.__request.urlopen(method = 'POST', url = url, data = data.encode('utf-8'),)

	def get(self, url, headers = None,):
		if headers != None:
			return self.__request.urlopen(method = 'GET', url = url, headers = headers,)

		else:
			return self.__request.urlopen(method = 'GET', url = url,)
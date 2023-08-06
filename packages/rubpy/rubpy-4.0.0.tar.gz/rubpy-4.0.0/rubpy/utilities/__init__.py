from ..network import (Network,)
from ..crypto import (Encryption,)
from json import (loads, dumps,)
from random import (choice,)


web = {'app_name': 'Main', 'app_version': '4.0.8', 'platform': 'Web', 'package': 'web.rubika.ir', 'lang_code': 'fa'}
android = {'app_name': 'Main', 'app_version': '2.9.8', 'platform': 'Android', 'package': 'app.rbmain.a', 'lang_code': 'fa'}


class Maker(object,):
	def __init__(self, auth,):
		self.__auth = auth
		self.__url_results = []
		self.__net = Network()
		__result_url = loads(self.__net.get('https://getdcmess.iranlms.ir/').data.decode('utf-8')).get('data')
		for url in __result_url.get('API').keys():
			self.__url_results.append(str(__result_url.get('API').get(url)) + '/')
		del __result_url
		self.__enc = Encryption(auth,)

	def method(self, method_name, method_data, custom_client = None, method_type = None,):
		if method_type == None:
			return loads(self.__enc.decrypt(loads(self.__net.post(url = self.__url(), json = {
				'api_version': '5',
				'auth': self.__auth,
				'data_enc': self.__enc.encrypt(dumps({
					'method': method_name,
					'input': method_data,
					'client': web if custom_client == None else android,
				}))}).data.decode('utf-8')).get('data_enc')))

		elif method_type == 4:
			return loads(self.__enc.decrypt(loads(self.__net.post(url = self.__url(), json = {
			"api_version" : "4",
			"auth" : self.__auth,
			"client" : android if custom_client == None else web,
			"method" : method_name,
			"data_enc" : self.__enc.encrypt(dumps(method_data)
			)}).data.decode('utf-8')).get('data_enc')))

	def __url(self,):
		return str(choice(self.__url_results))
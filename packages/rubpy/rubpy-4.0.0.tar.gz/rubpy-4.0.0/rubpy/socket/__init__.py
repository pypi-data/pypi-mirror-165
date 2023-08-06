from websocket import (create_connection,)
from ..crypto import (Encryption,)
from json import (loads, dumps,)
from ..network import Network
from random import (choice,)
from ..rubika import (RubikaClient,)


_data = '{"api_version": "4", "auth": "replace", "data_enc": "", "method": "handShake"}'


class _Socket(object,):
	def __init__(self, auth,):
		self.__enc = Encryption(auth,)
		self.__net = Network()
		self.__auth = auth
		self.rubika = RubikaClient(auth,)
		self.__url_results = []
		while True:
			try:
				__result_url = loads(self.__net.get('https://getdcmess.iranlms.ir/').data.decode('utf-8')).get('data')
				for url in __result_url.get('socket').keys():
					self.__url_results.append(str(__result_url.get('socket').get(url)) + '/')
				del __result_url, url
				break
			except: continue

	def handSnake(self,):
		ws = create_connection(self.__url())
		ws.send(_data.replace('replace', self.__auth))
		if loads(ws.recv()).get('status') == 'OK':
			print('connect to the web socket...')
		while True:
			try:
				recv = loads(ws.recv())
				if recv.get('type') == 'messenger':
					recv = loads(self.__enc.decrypt(recv.get('data_enc')))
					if not recv.get('show_activities'):
						yield recv
				else:
					continue
			except:
				del ws
				ws = create_connection(self.__url())
				ws.send(_data.replace('replace', self.__auth))
				continue

	def handler(self,):
		__data_get = self.handSnake()
		for recv in __data_get:
			updates = recv.get('message_updates')
			if updates == None:
				continue
			for update in updates:
				yield update

	def __url(self,):
		return choice(self.__url_results)

	def message_id(self, data,):
		return data.get('message_id')

	def object_guid(self, data,):
		return data.get('object_guid')

	def guid_type(self, data,):
		return data.get('type')

	def action(self, data,):
		return data.get('action')

	def text(self, data,):
		return data.get('message').get('text')

	def message_type(self, data,):
		return data.get('message').get('type')

	def author_object_guid(self, data,):
		return data.get('message').get('author_object_guid')

	def set_action(self, data,):
		if self.action(data,) == 'New':
			return True

	def set_filter(self, data, filter_type):
		filter_type = filter_type.lower()
		if filter_type == 'double':
			if self.guid_type(data,) == 'Group' or self.guid_type(data,) == 'User':
				return True

		elif filter_type == 'users':
			if self.guid_type(data,) == 'User':
				return True

		elif filter_type == 'group':
			if self.guid_type(data,) == 'Group':
				return True

		elif filter_type == 'channel':
			if self.guid_type(data,) == 'Channel':
				return True
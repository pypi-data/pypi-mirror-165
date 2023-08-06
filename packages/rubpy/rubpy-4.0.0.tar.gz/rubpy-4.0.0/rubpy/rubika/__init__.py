from ..utilities import (Maker,)
from time import (time,)
from json.decoder import (JSONDecodeError,)
from random import (randint,)
from ..tools import (Tools,)
from socket import (gaierror,)
from urllib3.exceptions import (MaxRetryError,)


class RubikaClient(object,):
	def __init__(self, auth,):
		#self.__auth = auth
		self.__maker = Maker(auth,)
		self.__tools = Tools()

	def getChatsUpdates(self,):
		while True:
			try:
				result = self.__maker.method('getChatsUpdates', {'state': str(round(time()) - 200),}).get('data').get('chats')
				if result == []:
					return None
				else:
					return result
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def sendMessage(self, chat_id, text, reply_to_message_id = None,):
		while True:
			try:
				Input = {
					'object_guid' : chat_id,
					'rnd' : f'{randint(100000,999999999)}',
					'text' : text,
					'reply_to_message_id' : reply_to_message_id
				}

				modes = ['**' , '__' , '``',]
				for check in modes:
					if check in text:
						metadata = self.__tools.textAnalysis(text,)
						Input['metadata'] = {'meta_data_parts': metadata[0]}
						Input['text'] = metadata[1]
				return self.__maker.method('sendMessage', Input,)
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getChats(self, start_id = None,):
		while True:
			try:
				return self.__maker.method('getChats', {'start_id': start_id}).get('data').get('chats')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getUserInfo(self, user_guid,):
		while True:
			try:
				return self.__maker.method('getUserInfo', {'user_guid': user_guid}).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getLinkFromAppUrl(self, app_url,):
		while True:
			try:
				return self.__maker.method('getLinkFromAppUrl', {'app_url': app_url}).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getBannedGroupMembers(self, group_guid,):
		while True:
			try:
				return self.__maker.method('getBannedGroupMembers', {'group_guid': group_guid}, custom_client = 'android').get('data').get('in_chat_members')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getGroupAdmins(self, group_guid,):
		while True:
			try:
				return self.__maker.method('getGroupAdminMembers', {'group_guid': group_guid},).get('data').get('in_chat_members')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def deleteMessages(self, chat_id, messages_id, delete_type = 'Global'):
		while True:
			try:
				return self.__maker.method('deleteMessages',
				{'object_guid': chat_id,
					'message_ids': list(messages_id),
					'type': delete_type},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def sendGroupVoiceChatActivity(self, group_guid, voice_chat_id):
		pass

	def requestSendFile(self, name, size, mime,):
		while True:
			try:
				return self.__maker.method('requestSendFile', {
				'file_name': name,
				'size': size,
				'mime': mime
				,},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def editMessage(self, chat_id, message_id, new_text,):
		while True:
			try:
				Input = {
					'message_id': message_id,
					'object_guid': chat_id,
					'text': new_text,
				}

				modes = ['**' , '__' , '``',]
				for check in modes:
					if check in new_text:
						metadata = self.__tools.textAnalysis(new_text,)
						Input['metadata'] = {'meta_data_parts': metadata[0]}
						Input['text'] = metadata[1]
				return self.__maker.method('editMessage', Input,)
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def banGroupMember(self, group_guid, user_guid, action = 'Set'):
		while True:
			try:
				return self.__maker.method('banGroupMember', {
					'action': action,
					'group_guid': group_guid,
					'member_guid': user_guid
				},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def searchInChannelMembers(self, channel_guid, search_text,):
		while True:
			try:
				return self.__maker.method('getChannelAllMembers', {
					'channel_guid' : channel_guid,
					'search_text' : search_text
				},).get('data').get('in_chat_members')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getChannelAllMembers(self, channel_guid):
		while True:
			try:
				return self.__maker.method('getChannelAllMembers', {
				'channel_guid' : channel_guid,
				'search_text' : None,
				'start_id' : None
				},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def checkMemberInChannel(self, channel_guid, search_text, member_username,):
		for check in self.searchInChannelMembers(channel_guid, search_text):
			if check['username'] != '':
				if check['username'] == member_username.replace('@', ''):
					return True

				return None

	def getMessagesUpdates(self, chat_id):
		while True:
			try:
				return self.__maker.method('getMessagesUpdates', {
					'object_guid': chat_id,
					'state': str(round(time() - 200))
				},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def forwardMessages(self, from_guid, messages_id, to_guid):
		while True:
			try:
				return self.__maker.method('forwardMessages', {
					'from_object_guid': from_guid,
					'message_ids': messages_id,
					'rnd': f'{randint(100000,999999999)}',
					'to_object_guid': to_guid
				},).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getGroupInfo(self, group_guid, last_message_id = False):
		json = {'group_guid': group_guid}
		while True:
			try:
				if last_message_id:
					return self.__maker.method('getGroupInfo', json).get('data').get('chat').get('last_message_id')
				return self.__maker.method('getGroupInfo', json).get('data').get('group')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getChannelInfo(self, channel_guid, last_message_id = False):
		json = {'channel_guid': channel_guid}
		while True:
			try:
				if last_message_id:
					return self.__maker.method('getChannelInfo', json).get('data').get('chat').get('last_message_id')
				return self.__maker.method('getChannelInfo', json).get('data').get('channel')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getMessagesInterval(self, chat_id, middle_message_id):
		json = {
			'object_guid' : chat_id,
			'middle_message_id' : middle_message_id
			}
		while True:
			try:
				return self.__maker.method('getMessagesInterval', json).get('data').get('messages')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getInfoByUsername(self, username):
		json = {
			'username': username.replace('@', '')
		}
		while True:
			try:
				return self.__maker.method('getObjectByUsername', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getGroupLink(self, group_guid):
		json = {'group_guid': group_guid}
		while True:
			try:
				return self.__maker.method('getGroupLink', json).get('data').get('join_link')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def addGroupMembers(self, group_guid, member_guids):
		json = {
			'member_guids': list(member_guids),
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('addGroupMembers', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def addChannelMembers(self, channel_guid, member_guids):
		json = {
			'member_guids': list(member_guids),
			'channel_guid': channel_guid
		}
		while True:
			try:
				return self.__maker.method('addChannelMembers', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getMessagesInfo(self, chat_id, message_ids):
		json = {
			'object_guid': chat_id,
			'message_ids': message_ids
		}
		while True:
			try:
				return self.__maker.method('getMessagesByID', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setMembersAccess(self, group_guid, accessies):
		json = {
			'access_list': list(accessies),
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('setGroupDefaultAccess', json, custom_client = 4).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getGroupAllMembers(self, group_guid, start_id = None):
		json = {
			'start_id': start_id,
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('getGroupAllMembers', json).get('data').get('in_chat_members')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setGroupLink(self, group_guid):
		json = {
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('setGroupLink', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setGroupTimer(self, group_guid, Time):
		json = {
			'group_guid' : group_guid,
			'slow_mode' : Time,
			'updated_parameters' : ['slow_mode']
		}
		while True:
			try:
				return self.__maker.method('editGroupInfo', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setGroupAdmin(self, group_guid, user_guid, accessies, action = 'SetAdmin'):
		json = {
			'group_guid': group_guid,
			'access_list': list(accessies),
			'action': action,
			'member_guid': user_guid
		}
		while True:
			try:
				return self.__maker.method('setGroupAdmin', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def deleteGroupAdmin(self, group_guid, user_guid):
		json = {
			'group_guid': group_guid,
			'action': 'UnsetAdmin',
			'member_guid': user_guid
		}
		while True:
			try:
				return self.__maker.method('setGroupAdmin', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def logout(self,):
		while True:
			try:
				return self.__maker.method('logout', {}).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def seenChats(self, seen_list):
		while True:
			try:
				return self.__maker.method('seenChats', {'seen_list': seen_list}).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def sendChatActivity(self, chat_id, action,):
		json = {
			'activity': action,
			'object_guid': chat_id
			}
		while True:
			try:
				return self.__maker.method('sendChatActivity', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setPinMessage(self, chat_id, message_id, action = 'Pin'):
		json = {
			'action': action,
			'message_id': message_id,
			'object_guid': chat_id
		}
		while True:
			try:
				return self.__maker.method('setPinMessage', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def joinGroup(self, group_link):
		json = {
			'hash_link': group_link.split('/')[-1]
		}
		while True:
			try:
				return self.__maker.method('joinGroup', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def groupPreviewByJoinLink(self, group_link):
		json = {
			'hash_link': group_link.split('/')[-1]
		}
		while True:
			try:
				return self.__maker.method('groupPreviewByJoinLink', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def leaveGroup(self, group_guid):
		json = {
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('leaveGroup', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getGroupMentionList(self, group_guid):
		json = {
			'group_guid': group_guid
		}
		while True:
			try:
				return self.__maker.method('getGroupMentionList', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def setBlockUser(self, user_guid, action = 'Block'):
		json = {
			'action' : action,
			'user_guid' : user_guid
		}
		while True:
			try:
				return self.__maker.method('setBlockUser', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getMyStickerSets(self,):
		while True:
			try:
				return self.__maker.method('getMyStickerSets', {}).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def createGroupVoiceChat(self, chat_id,):
		json = {'chat_guid': chat_id}
		while True:
			try:
				return self.__maker.method('createGroupVoiceChat', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def discardGroupVoiceChat(self, chat_id, voice_chat_id):
		json = {
			'chat_guid': chat_id,
			'voice_chat_id': voice_chat_id
		}
		while True:
			try:
				return self.__maker.method('discardGroupVoiceChat', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getChannelLink(self, channel_guid):
		json = {'channel_guid': channel_guid}
		while True:
			try:
				return self.__maker.method('getChannelLink', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getAvatars(self, chat_id):
		json = {'object_guid': chat_id}
		while True:
			try:
				return self.__maker.method('getAvatars', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def deleteAvatar(self, chat_id, avatar_id):
		json = {
			'object_guid' : chat_id,
			'avatar_id' : avatar_id
			}
		while True:
			try:
				return self.__maker.method('deleteAvatar', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def deleteChatHistory(self, chat_id, last_message_id):
		json = {
			'object_guid': chat_id,
			'last_message_id': str(last_message_id)
		}
		while True:
			try:
				return self.__maker.method('deleteChatHistory', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def searchGlobalObjects(self, search_text):
		json = {'search_text': search_text}
		while True:
			try:
				return self.__maker.method('searchGlobalObjects', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue

	def getPollStatus(self, poll_id):
		json = {'poll': poll_id}
		while True:
			try:
				return self.__maker.method('getPollStatus', json).get('data')
			except JSONDecodeError:
				continue
			except gaierror:
				continue
			except MaxRetryError:
				continue
			except KeyError:
				continue
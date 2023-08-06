from Crypto.Cipher import (AES,)
from Crypto.Util.Padding import (pad, unpad,)
from base64 import (b64encode , urlsafe_b64decode,)


class Tools(object,):
	def __init__(self,):
		pass

	def replaceCharAt(self, text1, text2, text3):
		return text1[0:text2] + text3 + text1[text2 + len(text3):]

	def secret(self, text,):
		result = text[16:24] + text[0:8] + text[24:32] + text[8:16]
		counter = 0
		while counter < len(result):
			text = result[counter]
			if text >= '0' and text <= '9':
				result = self.replaceCharAt(result, counter, chr((ord(text[0]) - ord('0') + 5) % 10 + ord('0')))
			else:
				result = self.replaceCharAt(result, counter, chr((ord(text[0]) - ord('a') + 9) % 26 + ord('a')))
			counter += 1

		return result


class Encryption:
    def __init__(self, auth,):
        tools = Tools()
        self.key = bytearray(tools.secret(auth), "utf-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def encrypt(self, text):
        return b64encode(AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(pad(text.encode('utf-8'), 16))).decode('utf-8')

    def decrypt(self, text):
        return unpad(AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(urlsafe_b64decode(text.encode('utf-8'))), 16).decode('utf-8')
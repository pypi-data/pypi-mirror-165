import hashlib

class pwdcrk:
	def getCharPower(self, stringLength, charRange):
		self.charpowers = []
		for x in range(0, stringLength):
			self.charpowers.append(len(charRange)**(stringLength - x - 1))
		return self.charpowers

	def Generator(self, stringLength, charRange):
		self.workbench = []
		self.results = []
		self.charpowers = self.getCharPower(stringLength, charRange)
		for x in range(0, stringLength):
			while len(self.workbench) < len(charRange)**stringLength:
				for char in charRange:
					for z in range(0, self.charpowers[x]):
						self.workbench.append(char)
			self.results.append(self.workbench)
			self.workbench = []
		self.results = ["".join(result) for result in list(zip(*self.results))]
		return self.results
	
	def alphabetchoice(self, level):
		if level == ("123"):
			return [char for char in "0123456789"]
		elif level == ("abc"):
			return [char for char in "abcdefghijklmnopqrstuvwxyz"]
		elif level == ("abc123"):
			return [char for char in "abcdefghijklmnopqrstuvwxyz0123456789"]
		elif level == ("ABC"):
			return [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
		elif level == ("ABC123"):
			return [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
		elif level == ("ABCabc"):
			return [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"]
		elif level == ("ABCabc123"):
			return [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"]
		elif level == ("!!!"):
			return [char for char in "!?.,<>/@':;#~{}[]\"£$%^&*()|\\`¬"]
		elif level == ("123!!!"):
			return [char for char in "0123456789!?.,<>/@':;#~{}[]\"£$%^&*()|\\`¬"]
		elif level == ("abc!!!"):
			return [char for char in "abcdefghijklmnopqrstuvwxyz!?.,<>/@':;#~{}[]\"£$%^&*()|\\`¬"]
		elif level == ("abc123!!!"):
			return [char for char in "abcdefghijklmnopqrstuvwxyz0123456789!?.,<>/@':;#~{}[]\"£$%^&*()|\\`¬"]
		elif level == ("ABCabc123!!!"):
			return [char for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?.,<>/@':;#~{}[]\"£$%^&*()|\\`¬"]
		else:
			return level

	def crack(self, hash, password, level):
		alphabet = self.alphabetchoice(level)
		known_char = "".join([char for char in password if char != ("*")])
		unknown_char = len([char for char in password if char == ("*")])
		for passwords in [known_char+combo.strip() for combo in self.Generator(unknown_char, alphabet)]:
			if getattr(hashlib, self.hashtype)(bytes(passwords, 'utf-8')).hexdigest() == hash:
				return {"Cracked" : passwords}
		return {"Result" : "NULL"}

	def crack_md5(self, hash, password, level):
		self.hashtype = ("md5")
		return self.crack(hash, password, level)

	def crack_sha1(self, hash, password, level):
		self.hashtype = ("sha1")
		return self.crack(hash, password, level)

	def crack_sha256(self, hash, password, level):
		self.hashtype = ("sha256")
		return self.crack(hash, password, level)
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

	
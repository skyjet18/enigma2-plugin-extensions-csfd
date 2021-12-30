# -*- coding: utf-8 -*-

from enigma import eTimer
from Components.Language import language
from CSFDSettings1 import CSFDGlobalVar

class CSFDNumericalTextInput:

	def __init__(self, nextFunc=None, handleTimeout=True, search=False):
		self.mapping = []
		self.lang = language.getLanguage()
		self.useableChars = None
		self.nextFunction = nextFunc
		if handleTimeout:
			self.timer_conn = None
			self.timer = None
			self.timer = eTimer()
			if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
				self.timer.callback.append(self.timeout)
				self.timer_conn = None
			else:
				self.timer_conn = self.timer.timeout.connect(self.timeout)
		else:
			self.timer_conn = None
			self.timer = None
		self.lastKey = -1
		self.pos = -1
		if search:
			if isinstance(search, basestring):
				self.mapping.append(unicode(search) + '0')
			else:
				self.mapping.append('%_0')
			self.mapping.append(' 1')
			self.mapping.append('abc2')
			self.mapping.append('def3')
			self.mapping.append('ghi4')
			self.mapping.append('jkl5')
			self.mapping.append('mno6')
			self.mapping.append('pqrs7')
			self.mapping.append('tuv8')
			self.mapping.append('wxyz9')
			return
		else:
			if self.lang == 'de_DE':
				self.mapping.append('0,?!&@=*\'+"()$~')
				self.mapping.append(' 1.:/-_')
				self.mapping.append('abcä2ABCÄ')
				self.mapping.append('def3DEF')
				self.mapping.append('ghi4GHI')
				self.mapping.append('jkl5JKL')
				self.mapping.append('mnoö6MNOÖ')
				self.mapping.append('pqrsß7PQRSß')
				self.mapping.append('tuvü8TUVÜ')
				self.mapping.append('wxyz9WXYZ')
			elif self.lang == 'es_ES':
				self.mapping.append('0,?!&@=*\'+"()$~')
				self.mapping.append(' 1.:/-_')
				self.mapping.append('abcáà2ABCÁÀ')
				self.mapping.append('deéèf3DEFÉÈ')
				self.mapping.append('ghiíì4GHIÍÌ')
				self.mapping.append('jkl5JKL')
				self.mapping.append('mnñoóò6MNÑOÓÒ')
				self.mapping.append('pqrs7PQRS')
				self.mapping.append('tuvúù8TUVÚÙ')
				self.mapping.append('wxyz9WXYZ')
			if self.lang in ('sv_SE', 'fi_FI'):
				self.mapping.append('0,?!&@=*\'+"()$~')
				self.mapping.append(' 1.:/-_')
				self.mapping.append('abcåä2ABCÅÄ')
				self.mapping.append('defé3DEFÉ')
				self.mapping.append('ghi4GHI')
				self.mapping.append('jkl5JKL')
				self.mapping.append('mnoö6MNOÖ')
				self.mapping.append('pqrs7PQRS')
				self.mapping.append('tuv8TUV')
				self.mapping.append('wxyz9WXYZ')
			elif self.lang in ('cs_CZ', 'sk_SK'):
				self.mapping.append('0,?\'+"()@$!=&*')
				self.mapping.append(' 1.:/-_')
				self.mapping.append('abc2áäčABCÁÄČ')
				self.mapping.append('def3ďéěDEFĎÉĚ')
				self.mapping.append('ghi4íGHIÍ')
				self.mapping.append('jkl5ľĺJKLĽĹ')
				self.mapping.append('mno6ňóöôMNOŇÓÖÔ')
				self.mapping.append('pqrs7řŕšPQRSŘŔŠ')
				self.mapping.append('tuv8ťúůüTUVŤÚŮÜ')
				self.mapping.append('wxyz9ýžWXYZÝŽ')
			else:
				self.mapping.append('0,?!&@=*\'+"()$~')
				self.mapping.append(' 1.:/-_')
				self.mapping.append('abc2ABC')
				self.mapping.append('def3DEF')
				self.mapping.append('ghi4GHI')
				self.mapping.append('jkl5JKL')
				self.mapping.append('mno6MNO')
				self.mapping.append('pqrs7PQRS')
				self.mapping.append('tuv8TUV')
				self.mapping.append('wxyz9WXYZ')
			return

	def setUseableChars(self, useable):
		self.useableChars = unicode(useable)

	def getKey(self, num):
		cnt = 0
		if self.lastKey != num:
			if self.lastKey != -1:
				self.nextChar()
			self.lastKey = num
			self.pos = -1
		if self.timer is not None:
			self.timer.start(1000, True)
		while True:
			self.pos += 1
			if len(self.mapping[num]) <= self.pos:
				self.pos = 0
			if self.useableChars:
				pos = self.useableChars.find(self.mapping[num][self.pos])
				if pos == -1:
					cnt += 1
					if cnt < len(self.mapping[num]):
						continue
					else:
						return
			break

		return self.mapping[num][self.pos]

	def nextKey(self):
		if self.timer is not None:
			self.timer.stop()
		self.lastKey = -1
		return

	def nextChar(self):
		self.nextKey()
		if self.nextFunction:
			self.nextFunction()

	def timeout(self):
		if self.lastKey != -1:
			self.nextChar()

# -*- coding: utf-8 -*-

from Components.config import config, ConfigText, ConfigSubsection, ConfigYesNo, ConfigSelection
from datetime import datetime
from os import path as os_path, remove as os_remove, rename as os_rename, fsync

class CSFDLog:

	def __init__(self):
		print('[CSFD] CSFDLog Init - Start')
		self.level = -1
		self.max_level = 10
		self.key_word_start = 'ZACATEK'
		self.len_key_word_start = len(self.key_word_start)
		self.key_word_end = 'KONEC'
		self.len_key_word_end = len(self.key_word_end)
		self.separator = ' '
		self.len_separator = 3
		config.misc.CSFD = ConfigSubsection()
		config.misc.CSFD.Log = ConfigYesNo(default=True)
		config.misc.CSFD.LogConsole = ConfigYesNo(default=False)
		config.misc.CSFD.LogConsoleTime = ConfigYesNo(default=False)
		config.misc.CSFD.DirectoryTMP = ConfigText('/tmp/', fixed_size=False)
		config.misc.CSFD.LogMaxSize = ConfigSelection(choices=[('50000', '50kB'), ('100000', '100kB'), ('200000', '200kB'), ('300000', '300kB'), ('400000', '400kB'), ('500000', '500kB'), ('1000000', '1MB')], default='300000')
		self.LoadDefaults()
		print('[CSFD] CSFDLog Init - End')

	def LoadDefaults(self):
		self.Log = config.misc.CSFD.Log.getValue()
		self.LogConsole = config.misc.CSFD.LogConsole.getValue()
		self.LogConsoleTime = config.misc.CSFD.LogConsoleTime.getValue()
		self.DirectoryTMP = config.misc.CSFD.DirectoryTMP.getValue()
		self.MaxLogSize = int(config.misc.CSFD.LogMaxSize.getValue())
		if os_path.exists(self.DirectoryTMP):
			adresarTMP = self.DirectoryTMP
		else:
			adresarTMP = '/tmp/'
		self.CSFDLogFile = adresarTMP + 'CSFDlog.txt'
		if self.Log:
			if not os_path.exists(self.CSFDLogFile):
				self.CreateEmptyLog()
			self.CheckAndEmptyLog()

	def CreateEmptyLog(self):
		if self.Log:
			soubor = file(self.CSFDLogFile, 'w')
			soubor.close()

	def VerifyLogSize(self):
		vel = os_path.getsize(self.CSFDLogFile)
		return vel

	def CheckAndEmptyLog(self):
		if self.Log:
			if self.VerifyLogSize() > self.MaxLogSize:
				oldCSFDLogFile = self.CSFDLogFile + '_old'
				if os_path.exists(oldCSFDLogFile):
					os_remove(oldCSFDLogFile)
				os_rename(self.CSFDLogFile, oldCSFDLogFile)
				self.CreateEmptyLog()

	def SetOffset(self, vlakno):
		if vlakno == 0:
			return ('').ljust(self.level * self.len_separator, self.separator)
		else:
			return '[VL' + str(vlakno).rjust(2, '0') + ']'

	def CheckKeyWordStart(self, string, vlakno):
		if vlakno == 0 and string.rstrip()[-self.len_key_word_start:].upper() == self.key_word_start:
			self.level += 1
			if self.level > self.max_level:
				self.level = self.max_level

	def CheckKeyWordEnd(self, string, vlakno):
		if vlakno == 0 and string.rstrip()[-self.len_key_word_end:].upper() == self.key_word_end:
			self.level -= 1
			if self.level < -1:
				self.level = -1

	def WriteToFile(self, string, vlakno=0):
		self.CheckKeyWordStart(string, vlakno)
		if self.Log:
			soubor = file(self.CSFDLogFile, 'a')
			scctime = datetime.now().strftime('%Y%m%d %H:%M:%S.%f')
			if isinstance(string, str):
				soubor.write(scctime + ' ' + self.SetOffset(vlakno) + string)
			else:
				soubor.write(scctime + ' ' + self.SetOffset(vlakno) + str(string.encode('utf8')))
			soubor.flush()
			fsync(soubor.fileno())
			soubor.close()
			self.VerifyLogSize()
		if self.LogConsole:
			if self.LogConsoleTime:
				scctime = datetime.now().strftime('%Y%m%d %H:%M:%S.%f')
				print(scctime + '  ' + string)
			else:
				print(string)
		self.CheckKeyWordEnd(string, vlakno)

	def WriteToFileWithoutTime(self, string):
		if self.Log:
			soubor = file(self.CSFDLogFile, 'a')
			if isinstance(string, str):
				soubor.write(string)
			else:
				soubor.write(str(string.encode('utf8')))
			soubor.flush()
			fsync(soubor.fileno())
			soubor.close()
		if self.LogConsole:
			print(string)


LogCSFD = CSFDLog()

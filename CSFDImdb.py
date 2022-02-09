# -*- coding: utf-8 -*-

from .CSFDLog import LogCSFD
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import _, config
from .CSFDTools import Uni8

try:
	from twisted.web.client import downloadPage
except:
	def downloadPage(self, *a, **kw):
		pass

import traceback
LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB import - zacatek\n')
try:
	from Plugins.Extensions.IMDb.plugin import IMDB
	from Plugins.Extensions.IMDb.plugin import IMDB as puvIMDB
	import Plugins.Extensions.IMDb.plugin
	if 'getIMDB' in dir(IMDB):
		CSFDGlobalVar.setIMDBexist(True)
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB import - OK\n')
	else:
		CSFDGlobalVar.setIMDBexist(False)
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB import - nenastaven\n')
except:
	CSFDGlobalVar.setIMDBexist(False)
	from .CSFDTools import EmptyClass as puvIMDB
	err = traceback.format_exc()
	LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB import - nezdarilo se\n')

LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB import - konec\n')

class CSFD_IMDBcalls(puvIMDB):
	try:
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls1 - init - zacatek\n')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			from .CSFDSkinLoader import Screen_CSFDIMDB_SD
			skin = Screen_CSFDIMDB_SD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			from .CSFDSkinLoader import Screen_CSFDIMDB_HD
			skin = Screen_CSFDIMDB_HD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
		else:
			from .CSFDSkinLoader import Screen_CSFDIMDB_FullHD
			skin = Screen_CSFDIMDB_FullHD % (config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeight.getValue())
	except:
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 init skin 1 - chyba - konec\n')
		LogCSFD.WriteToFile(err)

	if CSFDGlobalVar.getIMDBexist():
		try:
			config.plugins.imdb.language.setValue('en-us')
		except:
			err = traceback.format_exc()

	LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls1 - init - konec\n')
	try:

		def __init__(self, session, eventName, callbackNeeded=False, moviepath='', *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 - init - zacatek\n')
			try:
				self.CSFDmoviepath = moviepath
				if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
					from .CSFDSkinLoader import Screen_CSFDIMDB_SD
					self.skin = Screen_CSFDIMDB_SD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
					from .CSFDSkinLoader import Screen_CSFDIMDB_HD
					self.skin = Screen_CSFDIMDB_HD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
				else:
					from .CSFDSkinLoader import Screen_CSFDIMDB_FullHD
					self.skin = Screen_CSFDIMDB_FullHD % (config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeight.getValue())
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 - init skin 2 - chyba - konec\n')
				LogCSFD.WriteToFile(err)

			try:
				puvIMDB.__init__(self, session, eventName, callbackNeeded=callbackNeeded, *args, **kwargs)
				LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 - init puvIMDB\n')
				if config.misc.CSFD.Skinxml.getValue():
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						self.skinName = [
						 'CSFDIMDB_SD', 'CSFDIMDB']
					elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
						self.skinName = [
						 'CSFDIMDB_HD', 'CSFDIMDB']
					else:
						self.skinName = [
						 'CSFDIMDB_FullHD', 'CSFDIMDB']
				else:
					self.skinName = 'CSFDIMDB__'
				LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 - init - konec\n')
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDBcalls2 init - chyba - konec\n')
				LogCSFD.WriteToFile(err)

	except:
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - __init__ - chyba\n')
		LogCSFD.WriteToFile(err)

	def getIMDB(self, *args, **kwargs):
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - getIMDB - zacatek\n')
		try:
			if self.CSFDmoviepath != '':
				moviepath = self.CSFDmoviepath
				self.CSFDmoviepath = ''
				self.directOpenMovie(self.eventName, moviepath)
			else:
				super(CSFD_IMDBcalls, self).getIMDB(*args, **kwargs)
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - getIMDB - chyba\n')
			LogCSFD.WriteToFile(err)

		LogCSFD.WriteToFile('[CSFD] CSFDImdb - getIMDB - konec\n')

	def fetchFailedIMDB(self, string, url):
		LogCSFD.WriteToFile('[CSFD] fetchFailedIMDB - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - url: ' + Uni8(url) + '\n')
		chyba = string.getErrorMessage()
		self['statusbar'].setText(_('Error during downloading'))
		ss2 = chyba.replace("'", '').strip().lower()
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - ss2: ' + Uni8(ss2) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedIMDB - konec\n')

	def directOpenMovie(self, evName='', moviepath=''):
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - directOpenMovie - zacatek\n')
		try:
			self.resetLabels()
			self.eventName = evName
			self['statusbar'].setText(_('Direct query IMDb'))
			localfile = '/tmp/imdbquery2.html'
			fetchurl = moviepath
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - stahuji z url ' + fetchurl + ' do ' + localfile + '\n')
			downloadPage(fetchurl, localfile).addCallback(self.IMDBquery2).addErrback(self.fetchFailedIMDB, fetchurl)
			self['menu'].hide()
			self.resetLabels()
			self.Page = 1
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - directOpenMovie - chyba\n')
			LogCSFD.WriteToFile(err)

		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - directOpenMovie - konec\n')


def InitIMDBchanges():
	try:
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - hlavni nahrazeni - zacatek\n')
		if config.misc.CSFD.CSFDreplaceIMDB.getValue() and CSFDGlobalVar.getIMDBexist():
			from .CSFD import CSFDClass
			Plugins.Extensions.IMDb.plugin.IMDB = CSFDClass
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - hlavni nahrazeni - OK\n')
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - hlavni nahrazeni - nenastaveno\n')
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - hlavni nahrazeni se nezdarilo - chyba\n')

	LogCSFD.WriteToFile('[CSFD] CSFDImdb - IMDB - hlavni nahrazeni - konec\n')

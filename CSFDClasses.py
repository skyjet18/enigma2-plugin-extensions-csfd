# -*- coding: utf-8 -*-

from enigma import gRGB, gFont, iPlayableService, RT_HALIGN_LEFT, RT_WRAP, RT_VALIGN_TOP
from enigma import eTimer, eSize, iServiceInformation, eServiceReference
from .CSFDLog import LogCSFD
from .CSFDTools import requestCSFD, internet_on, ItemListTypeSpecial, strUni, Uni8
from Screens.Screen import Screen
from Screens.InfoBarGenerics import InfoBarNotifications, InfoBarSubtitleSupport
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.ChannelSelection import SimpleChannelSelection
from Screens.EpgSelection import EPGSelection
from .CSFDHelpMenu import CSFDHelpableScreen1
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Pixmap import Pixmap, MultiPixmap
from Components.Label import Label
from .CSFDSubtitles import SubsSupport
from Components.Button import Button
from Components.MultiContent import MultiContentEntryText
from Components.ServiceEventTracker import ServiceEventTracker
from Components.config import getConfigListEntry
from Components.config import configfile
from .CSFDConfigList import CSFDConfigListScreen
from .CSFDConfigText import CSFDConfigText, CSFDConfigPassword
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import _, const_www_csfd, std_login_header, std_tv_post_header, std_login_header_UL2, std_tv_post_header_UL2, std_headers_UL2
from .CSFDSettings2 import config
from .CSFDMovieCache import TVMovieCache
from .CSFDParser import GetCSFDNumberFromChannel, ParserTVCSFD, ParserOstCSFD
from .CSFDSkinLoader import *
import time, traceback

try:
	from urllib.parse import urlencode
except:
	from urllib import urlencode


def LoginToCSFD():
	LogCSFD.WriteToFile('[CSFD] LoginToCSFD - zacatek\n', 1)
#	if not config.misc.CSFD.LoginToCSFD.getValue():
	if True:		
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - neprihlasovat do CSFD\n', 1)
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - konec\n', 1)
		return
	if int(time.time()) - config.misc.CSFD.LastLoginError.getValue() < config.misc.CSFD.LoginErrorWaiting.getValue() * 60:
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - jeste nevyprsel casovy limit z duvodu login chyby\n', 1)
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - konec\n', 1)
		return
	if not internet_on():
		config.misc.CSFD.LastLoginError.setValue(int(time.time()))
		config.misc.CSFD.LastLoginError.save()
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - neni funkcni internet\n', 1)
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - konec\n', 1)
		return

	def LogToWeb():
		LogCSFD.WriteToFile('[CSFD] LogToWeb - zacatek\n', 1)
		url = CSFDGlobalVar.getHTTP() + const_www_csfd + '/prihlaseni/'
		page = ''
		try:
			raise NameError('#1 Login do csfd nie je podporovany')
		
#			page = requestCSFD(url, headers=std_login_header_UL2, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue(), saveCookie=True)
		except:
			LogCSFD.WriteToFile('[CSFD] LogToWeb - get token - chyba - konec\n', 1)
			config.misc.CSFD.LastLoginError.setValue(int(time.time()))
			config.misc.CSFD.LastLoginError.save()
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

		LogCSFD.WriteToFile('[CSFD] LogToWeb 1a0\n', 1)
		ParserOstCSFD.setHTML2utf8(page)
		token = ParserOstCSFD.parserTokenLogin('')
		if token is None or token == '':
			token = ''
			LogCSFD.WriteToFile('[CSFD] LogToWeb - token neni na strance - chyba\n', 1)
			config.misc.CSFD.LastLoginError.setValue(int(time.time()))
			config.misc.CSFD.LastLoginError.save()
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)
		else:
			LogCSFD.WriteToFile('[CSFD] LogToWeb - token OK\n', 1)
			LogCSFD.WriteToFile('[CSFD] LogToWeb - token: ' + token + '\n', 1)
			url_login = ParserOstCSFD.parserURLLogin('')
			if url_login is None or url_login == '':
				url_login = ''
				LogCSFD.WriteToFile('[CSFD] LogToWeb - url pro login neni na strance - chyba\n', 1)
				config.misc.CSFD.LastLoginError.setValue(int(time.time()))
				config.misc.CSFD.LastLoginError.save()
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
			else:
				LogCSFD.WriteToFile('[CSFD] LogToWeb - url pro login OK\n', 1)
				page = ''
				try:
					values = {'username': config.misc.CSFD.UserNameCSFD.getValue(), 'password': config.misc.CSFD.PasswordCSFD.getValue(), 
					   'permanent': 'on', 
					   'send': 'Přihlásit+se', 
					   '_token_': token, 
					   '_do': 'form-submit'}
					data = urlencode(values)
					url = url_login
					raise NameError('#2 Login do csfd nie je podporovany')
#					page = requestCSFD(url, headers=std_login_header_UL2, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue(), data=data, redirect=False, saveCookie=True)
#					url = 'https://www.csfd.cz/'
#					page = requestCSFD(url, headers=std_headers_UL2, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue())
				except:
					LogCSFD.WriteToFile('[CSFD] LogToWeb - login - chyba - konec\n', 1)
					config.misc.CSFD.LastLoginError.setValue(int(time.time()))
					config.misc.CSFD.LastLoginError.save()
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)

				ParserOstCSFD.setHTML2utf8(page)
				page = ParserOstCSFD.getParserHTML()
				if page.find('prihlaseni/odhlaseni') >= 0:
					LogCSFD.WriteToFile('[CSFD] LogToWeb - prihlaseni OK\n', 1)
				else:
					LogCSFD.WriteToFile('[CSFD] LogToWeb - prihlaseni ERR\n', 1)
					config.misc.CSFD.LastLoginError.setValue(int(time.time()))
					config.misc.CSFD.LastLoginError.save()
		LogCSFD.WriteToFile('[CSFD] LogToWeb - konec\n', 1)
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - konec\n', 1)
		return

	LogCSFD.WriteToFile('[CSFD] LoginToCSFD - LogToWeb\n', 1)
	try:
		LogToWeb()
	except:
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - LogToWeb - chyba\n', 1)
		config.misc.CSFD.LastLoginError.setValue(int(time.time()))
		config.misc.CSFD.LastLoginError.save()
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		LogCSFD.WriteToFile('[CSFD] LoginToCSFD - konec\n', 1)


isFirstGetMovies = True

def GetMoviesForTVChannels(t_channName, t_typechannName=0, t_downlTimeout=3, t_ignoreNetErr=False):
	global isFirstGetMovies
	channName = t_channName
	typechannName = t_typechannName
	downlTimeout = t_downlTimeout
	ignoreNetErr = t_ignoreNetErr
	LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - zacatek\n', 20)
	LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - channName: ' + channName + '\n', 20)
	if isFirstGetMovies:
		isFirstGetMovies = False
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - prvni nacteni se ignoruje\n', 20)
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - konec\n', 20)
		return
	if channName == '':
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - neni kanal\n', 20)
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - konec\n', 20)
		return
	if not ignoreNetErr and int(time.time()) - config.misc.CSFD.LastLanError.getValue() < config.misc.CSFD.LanErrorWaiting.getValue() * 60:
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - jeste nevyprsel casovy limit z duvodu lan chyby\n', 20)
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - konec\n', 20)
		return

	def GetMovies(s_channName, s_typechannName=0, s_downlTimeout=3, s_ignoreNetErr=False):
		channName = s_channName
		typechannName = s_typechannName
		downlTimeout = s_downlTimeout
		ignoreNetErr = s_ignoreNetErr
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - zacatek\n', 20)
		stations = ''
		if typechannName == 0:
			channels = GetCSFDNumberFromChannel(channName)
			for channel in channels:
				if stations == '':
					stations += channel
				else:
					stations += '%2C' + channel

		else:
			stations = channName
		if stations != '':
			LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - stations: ' + stations + '\n', 20)
			t_stations = stations
			if not TVMovieCache.IsChannelInCache(t_stations):
				page = ''
				page_tomm = ''
				page_yest = ''
				cookies1 = CSFDGlobalVar.getCSFDCookies()
				cookies_addvalues = {'tv_types': 'films%2Cseries%2Cothers', 'tv_stations': t_stations}
				LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - cookies_addvalues: ' + str(cookies_addvalues) + '\n', 20)
				cookies1.update(cookies_addvalues)
				cookies1 = cookies_addvalues
				LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - cookies: ' + str(cookies1) + '\n', 20)
				chyba = False
				general_chyba = chyba
				if not chyba:
					try:
						raise NameError('#1 Ziskavanie TV tipov pre stanicu nie je podporovane')
#						page = requestCSFD(CSFDGlobalVar.getHTTP() + const_www_csfd + '/televize/?day=0', headers=std_tv_post_header_UL2, timeout=downlTimeout)
					except:
						page = ''
						chyba = True
						general_chyba = True
						config.misc.CSFD.LastLanError.setValue(int(time.time()))
						config.misc.CSFD.LastLanError.save()
						err = traceback.format_exc()
						LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies today - chyba - konec\n', 20)
						LogCSFD.WriteToFile(err)

				if not chyba:
					try:
						raise NameError('#2 Ziskavanie TV tipov pre stanicu nie je podporovane')
					
#						page_tomm = requestCSFD(CSFDGlobalVar.getHTTP() + const_www_csfd + '/televize/?day=1', headers=std_tv_post_header_UL2, timeout=downlTimeout)
					except:
						page_tomm = ''
						chyba = True
						general_chyba = True
						config.misc.CSFD.LastLanError.setValue(int(time.time()))
						config.misc.CSFD.LastLanError.save()
						err = traceback.format_exc()
						LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies tommorow - chyba - konec\n', 20)
						LogCSFD.WriteToFile(err)

				if not chyba:
					try:
						raise NameError('#3 Ziskavanie TV tipov pre stanicu nie je podporovane')
#						page_yest = requestCSFD(CSFDGlobalVar.getHTTP() + const_www_csfd + '/televize/?day=-1', headers=std_tv_post_header_UL2, timeout=downlTimeout)
					except:
						page_yest = ''
						chyba = True
						general_chyba = True
						config.misc.CSFD.LastLanError.setValue(int(time.time()))
						config.misc.CSFD.LastLanError.save()
						err = traceback.format_exc()
						LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies yesterday - chyba - konec\n', 20)
						LogCSFD.WriteToFile(err)

				if not chyba:
					page = page + page_tomm + page_yest
					ParserTVCSFD.setHTML2utf8(page)
					searchresults = ParserTVCSFD.parserListOfTVMovies(True)
					ParserTVCSFD.setParserHTML('')
					if len(searchresults) > 0:
						TVMovieCache.addMovieToCache(t_stations, searchresults)
					else:
						TVMovieCache.delChannelFromMovieCache(t_stations)
				elif general_chyba:
					LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - zapis LastLanError\n', 20)
					config.misc.CSFD.LastLanError.setValue(int(time.time()))
					config.misc.CSFD.LastLanError.save()
				else:
					LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - vynulovani LastLanError\n', 20)
					config.misc.CSFD.LastLanError.setValue(int(0))
					config.misc.CSFD.LastLanError.save()
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - GetMovies - konec\n', 20)

	try:
		GetMovies(channName, typechannName, downlTimeout, ignoreNetErr)
	except:
		LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] GetMoviesForTVChannels - konec\n', 20)


class CSFDChannelSelection(SimpleChannelSelection):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDSimpleChannelSelectionSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDSimpleChannelSelectionHD
	else:
		skin = Screen_CSFDSimpleChannelSelectionFullHD

	def __init__(self, session, openPlugin=False):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDSimpleChannelSelectionSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDSimpleChannelSelectionHD
		else:
			self.skin = Screen_CSFDSimpleChannelSelectionFullHD
		SimpleChannelSelection.__init__(self, session, _('Výběr kanálu'))
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDSimpleChannelSelectionSD', 'SimpleChannelSelection']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDSimpleChannelSelectionHD', 'SimpleChannelSelection']
			else:
				self.skinName = [
				 'CSFDSimpleChannelSelectionFullHD', 'SimpleChannelSelection']
		else:
			self.skinName = 'CSFDSimpleChannelSelection__'
		self['ChannelSelectEPGActions'] = ActionMap(['ChannelSelectEPGActions'], {'showEPGList': self.channelSelected})
		self.openPlugin = openPlugin
		CSFDGlobalVar.setCSFDcur(1)
		CSFDGlobalVar.setCSFDeventID_EPG(0)
		CSFDGlobalVar.setCSFDeventID_REF('')
		LogCSFD.WriteToFile('[CSFD] ChannelSelection - init - openPlugin ' + str(self.openPlugin) + '\n')

	def channelSelected(self):
		ref = self.getCurrentSelection()
		if ref.flags & 7 == 7:
			self.enterPath(ref)
		elif not ref.flags & eServiceReference.isMarker:
			LogCSFD.WriteToFile('[CSFD] ChannelSelection - callback - openPlugin ' + str(self.openPlugin) + '\n')
			self.session.openWithCallback(self.epgClosed, CSFDEPGSelection, ref, self.openPlugin)

	def epgClosed(self, ret=None, retEPG=None, retDVBchannel=None):
		if ret is not None and ret != '':
			self.close(ret, retEPG, retDVBchannel)
		return


class CSFDEPGSelection(EPGSelection):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDEPGSelectionSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDEPGSelectionHD
	else:
		skin = Screen_CSFDEPGSelectionFullHD

	def __init__(self, session, ref, openPlugin=True):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDEPGSelectionSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDEPGSelectionHD
		else:
			self.skin = Screen_CSFDEPGSelectionFullHD
		EPGSelection.__init__(self, session, ref)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDEPGSelectionSD', 'EPGSelection']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDEPGSelectionHD', 'EPGSelection']
			else:
				self.skinName = [
				 'CSFDEPGSelectionFullHD', 'EPGSelection']
		else:
			self.skinName = 'CSFDEPGSelection__'
		CSFDGlobalVar.setCSFDeventID_REF(ref)
		self['actions'] = ActionMap(['EPGSelectActions', 'OkCancelActions'], {'cancel': self.closeScreen, 
		   'ok': self.KeyBlue, 
		   'timerAdd': self.timerAdd, 
		   'yellow': self.yellowButtonPressed, 
		   'blue': self.KeyBlue, 
		   'info': self.infoKeyPressed, 
		   'input_date_time': self.enterDateTime, 
		   'nextBouquet': self.nextBouquet, 
		   'prevBouquet': self.prevBouquet, 
		   'nextService': self.nextService, 
		   'prevService': self.prevService, 
		   'red': self.KeyRed}, -1)
		self['key_blue'].setText(_('CSFD'))
		self['key_red'].setText(_('Výběr kanálu'))
		self.openPlugin = openPlugin
		self.onLayoutFinish.append(self.layoutFinished)
		LogCSFD.WriteToFile('[CSFD] EPGSelection - init - openPlugin ' + str(self.openPlugin) + '\n')

	def layoutFinished(self):
		LogCSFD.WriteToFile('[CSFD] EPGSelection - cur:' + str(CSFDGlobalVar.getCSFDcur()) + '\n')
		self['key_blue'].setText(_('CSFD'))
		self['key_red'].setText(_('Výběr kanálu'))
		if not CSFDGlobalVar.getCSFDcur() == 1:
			LogCSFD.WriteToFile('[CSFD] EPGSelection - nastavuji CSFDeventID_EPG\n')
			try:
				self['list'].moveToEventId(CSFDGlobalVar.getCSFDeventID_EPG())
			except:
				LogCSFD.WriteToFile('[CSFD] EPGSelection - chyba - nelze nastavit CSFDeventID_EPG\n')

			LogCSFD.WriteToFile('[CSFD] EPGSelection - nastavuji CSFDeventID_EPG - konec\n')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		try:
			self['list'].l.setItemHeight(h1)
			if 'setFont' in dir(self['list'].l):
				self['list'].l.setFont(0, gFont('Regular', h))
				self['list'].l.setFont(1, gFont('Regular', h - 4))
			else:
				LogCSFD.WriteToFile('[CSFD] EPGSelection - nelze nastavit velikost fontu v menu EPG (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] EPGSelection - chyba - nelze nastavit velikost fontu v menu EPG (stara verze enigma2)\n')

	def KeyRed(self):
		LogCSFD.WriteToFile('[CSFD] EPGSelection - init - KeyRed ' + str(self.openPlugin) + '\n')
		self.session.openWithCallback(self.KeyRedBack, CSFDChannelSelection, self.openPlugin)

	def KeyRedBack(self, ret=None, retEPG=None, retDVBchannel=None):
		if ret is not None and ret != '':
			self.close(ret, retEPG, retDVBchannel)
		return

	def closeScreen(self):
		self.close(None, None, None)
		return

	def infoKeyPressed(self):
		self.KeyBlue()

	def KeyBlue(self):
		cur = self['list'].getCurrent()
		evt = cur[0]
		serviceref = cur[1]
		LogCSFD.WriteToFile('[CSFD] EPGSelection - cur:' + str(CSFDGlobalVar.getCSFDcur()) + '\n')
		CSFDGlobalVar.setCSFDcur(2)
		LogCSFD.WriteToFile('[CSFD] EPGSelection - cur:' + str(CSFDGlobalVar.getCSFDcur()) + '\n')
		CSFDGlobalVar.setCSFDeventID_EPG(self['list'].getSelectedEventId())
		if evt is None:
			return
		else:
			LogCSFD.WriteToFile('[CSFD] EPGSelection - init - openPlugin ' + str(self.openPlugin) + '\n')
			eventName = evt.getEventName()
			short = evt.getShortDescription()
			ext = evt.getExtendedDescription()
			EPG = ''
			DVBchannel = serviceref.getServiceName()
			if short is not None and short != eventName:
				EPG = short
			if ext is not None:
				EPG += ext
			if EPG != '':
				EPG = eventName + ' - ' + EPG
			if self.openPlugin:
				from .CSFD import CSFDClass
				self.session.open(CSFDClass, eventName, False, EPG, True, DVBchannel)
				self.close(eventName, EPG, DVBchannel)
			else:
				self.close(eventName, EPG, DVBchannel)
			return

	def onSelectionChanged(self):
		pass


class CSFDLCDSummary(Screen):
	LogCSFD.WriteToFile('[CSFD] CSFDLCDSummary - zacatek\n')
	if CSFDGlobalVar.getCSFDImageCompatibility() < 11:
		if CSFDGlobalVar.getCSFDBoxType()[1] == '8000' or CSFDGlobalVar.getCSFDBoxType()[1] == '7020hd' or CSFDGlobalVar.getCSFDBoxType()[1] == '7080':
			skin = Screen_CSFDLCDSummary8000_7020hd
		elif CSFDGlobalVar.getCSFDBoxType()[1] == '800se':
			skin = Screen_CSFDLCDSummary800SE
		elif CSFDGlobalVar.getCSFDBoxType()[1] == '900':
			skin = Screen_CSFDLCDSummary900
		elif CSFDGlobalVar.getCSFDBoxType()[1] == '800':
			skin = Screen_CSFDLCDSummary800
		else:
			skin = Screen_CSFDLCDSummaryElseDMM
	else:
		skin = Screen_CSFDLCDSummaryElse
	LogCSFD.WriteToFile('[CSFD] CSFDLCDSummary - konec\n')

	def __init__(self, session, parent):
		Screen.__init__(self, session)
		LogCSFD.WriteToFile('[CSFD] CSFDLCDSummary - Init - zacatek\n')
		if config.misc.CSFD.SkinOLEDxml.getValue():
			if CSFDGlobalVar.getCSFDImageCompatibility() < 11:
				if CSFDGlobalVar.getCSFDBoxType()[1] == '8000' or CSFDGlobalVar.getCSFDBoxType()[1] == '7020hd' or CSFDGlobalVar.getCSFDBoxType()[1] == '7080':
					self.skinName = [
					 'CSFDLCDSummary8000_7020hd', 'CSFDLCDSummary']
				elif CSFDGlobalVar.getCSFDBoxType()[1] == '800se':
					self.skinName = [
					 'CSFDLCDSummary800SE', 'CSFDLCDSummary']
				elif CSFDGlobalVar.getCSFDBoxType()[1] == '900':
					self.skinName = [
					 'CSFDLCDSummary900', 'CSFDLCDSummary']
				elif CSFDGlobalVar.getCSFDBoxType()[1] == '800':
					self.skinName = [
					 'CSFDLCDSummary800', 'CSFDLCDSummary']
				else:
					self.skinName = [
					 'CSFDLCDSummaryElseDMM', 'CSFDLCDSummary']
			else:
				self.skinName = [
				 'CSFDLCDSummaryElse', 'CSFDLCDSummary']
		else:
			self.skinName = 'CSFDLCDSummary__'
		LogCSFD.WriteToFile('[CSFD] CSFDLCDSummary - Init - konec\n')
		self['headline'] = Label(_('CSFD.cz :'))
		self['infomovie'] = Label('')
		self.ColorLCD = 0
		if (CSFDGlobalVar.getCSFDBoxType()[1] == '800se' or CSFDGlobalVar.getCSFDBoxType()[1] == '900') and CSFDGlobalVar.getCSFDImageCompatibility() < 11:
			self.ColorLCD = 1

	def setText(self, text, detail):
		if self.ColorLCD == 1:
			if detail == 0:
				self['infomovie'].instance.setForegroundColor(gRGB(CSFDratingColor_Nothing))
			elif detail == 1:
				self['infomovie'].instance.setForegroundColor(gRGB(CSFDratingColor_100))
			elif detail == 2:
				self['infomovie'].instance.setForegroundColor(gRGB(CSFDratingColor_50))
			elif detail == 3:
				self['infomovie'].instance.setForegroundColor(gRGB(CSFDratingColor_0))
			else:
				self['infomovie'].instance.setForegroundColor(gRGB(16777215))
		self['infomovie'].setText(text)


def RefreshPlugins():
	LogCSFD.WriteToFile('[CSFD] RefreshPlugins - zacatek\n')
	from Components.PluginComponent import plugins
	from .CSFDTools import InitCSFDTools
	from .CSFDSettings2 import PathTMPInit, localeInit, InitParamsLangImpact
	LogCSFD.LoadDefaults()
	PathTMPInit()
	localeInit()
	LoginToCSFD()
	InitParamsLangImpact()
	InitCSFDTools()
	plugins.clearPluginList()
	plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
	LogCSFD.WriteToFile('[CSFD] RefreshPlugins - konec\n')


class CSFDSetup(Screen, CSFDConfigListScreen, CSFDHelpableScreen1):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDSetupSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDSetupHD
	else:
		skin = Screen_CSFDSetupFullHD

	def __init__(self, session, procTestLogin=None, procRepair=None, procResetParam=None):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDSetupSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDSetupHD
		else:
			self.skin = Screen_CSFDSetupFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDSetupSD', 'CSFDSetup']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDSetupHD', 'CSFDSetup']
			else:
				self.skinName = [
				 'CSFDSetupFullHD', 'CSFDSetup']
		else:
			self.skinName = 'CSFDSetup__'
		self.setup_title = _('CSFD Nastavení')
		self.TestLogin = procTestLogin
		self.Repair = procRepair
		self.ResetParam = procResetParam
		CSFDHelpableScreen1.__init__(self)
		self['CSFDSetupActions'] = HelpableActionMap(self, 'CSFDSetupActions', {'keyMenu': (
					 self.keyMenu, _('Zobrazí další možnosti v Nastaveních')), 
		   'ok': (
				self.keySave, _('Uloží nastavení')), 
		   'save': (
				  self.keySave, _('Uloží nastavení')), 
		   'cancel': (
					self.keyCancelCan, _('Ukončení nastavování - bez uložení')), 
		   'keyRed': (
					self.keyCancelRed, _('Ukončení nastavování - bez uložení')), 
		   'keyGreen': (
					  self.keySaveGreen, _('Uloží nastavení')), 
		   'keyBlue': (
					 self.keyNext, _('Přepne na další záložku')), 
		   'keyYellow': (
					   self.keyYellow, _('Otestuje přihlášení do CSFD')), 
		   'keyInfo': (
					 self.keyInfo, _('Pokusí se opravit/doinstalovat potřebné moduly')), 
		   'tabPrev': (
					 self.keyPrevious, _('Přepne na předchozí záložku')), 
		   'tabNext': (
					 self.keyNext, _('Přepne na další záložku'))}, -1)
		self['config0'] = Label('')
		self['config1'] = Label('')
		self['config2'] = Label('')
		self['key_red'] = Button(_('Zrušit'))
		self['key_green'] = Button(_('OK'))
		self['key_blue'] = Button(_('Další'))
		self['info_icon'] = Pixmap()
		self['info_epg'] = Pixmap()
		if self.Repair is not None:
			self['key_info'] = Button(_('Opravit/Reinstalovat potřebné knihovny'))
			self['info_icon'].show()
			self['info_epg'].show()
		else:
			self['key_info'] = Button('')
			self['info_icon'].hide()
			self['info_epg'].hide()
		if self.TestLogin is not None:
			self['key_yellow'] = Button(_('Test login'))
		else:
			self['key_yellow'] = Button('')
		self['info'] = Label(_('Po některých změnách je nutné znovu spustit plugin nebo restartartovat GUI!'))
		self['key_menu'] = Button(_('Menu'))
		self['info_menu'] = Pixmap()
		self['info_menu'].show()
		self['tabbar'] = MultiPixmap()
		self['config0'].setText(_('Ovládání'))
		self['config1'].setText(_('Design'))
		self['config2'].setText(_('Různé'))
		self.delay_timerHide = eTimer()
		self.delay_timerShow = eTimer()
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.delay_timerHide.callback.append(self.hideInputHelp)
			self.delay_timerHideConn = None
			self.delay_timerShow.callback.append(self.showInputHelp)
			self.delay_timerShowConn = None
		else:
			self.delay_timerHideConn = self.delay_timerHide.timeout.connect(self.hideInputHelp)
			self.delay_timerShowConn = self.delay_timerShow.timeout.connect(self.showInputHelp)
		self['VKeyText'] = Pixmap()
		self['VKeyText'].hide()
		self['VKeyIcon'] = Pixmap()
		self['VKeyIcon'].hide()
		self.selectedList = 0
		self.onChangedEntry = []
		self.session = session
		self.positionInConfig0 = 0
		self.positionInConfig1 = 0
		self.positionInConfig2 = 0
		self.list = []
		self.list0 = []
		self.list1 = []
		self.list2 = []
		CSFDConfigListScreen.__init__(self, self.list, session=self.session)
		self['config'].list = self.list
		self['config'].l.setList(self.list)
		self.createLists()
		self.updateList()
		self.onLayoutFinish.append(self.layoutFinished)
		return

	def layoutFinished(self):
		self.updateTabColour()
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		self['config'].instance.setItemHeight(h1)
		try:
			if 'setFont' in dir(self['config'].instance):
				self['config'].instance.setFont(gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDSetup - nelze nastavit velikost fontu v menu 1 (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDSetup - chyba - nelze nastavit velikost fontu v menu 1 (stara verze enigma2)\n')

		try:
			if 'setFont' in dir(self['config'].l):
				self['config'].l.setFont(gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDSetup - nelze nastavit velikost fontu v menu 2 (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDSetup - chyba - nelze nastavit velikost fontu v menu 2 (stara verze enigma2)\n')

	def updatePos(self):
		aktpos = self['config'].getCurrentIndex()
		if self.selectedList == 0:
			self.positionInConfig0 = aktpos
			self.list0 = self['config'].getList()
		elif self.selectedList == 1:
			self.positionInConfig1 = aktpos
			self.list1 = self['config'].getList()
		else:
			self.positionInConfig2 = aktpos
			self.list2 = self['config'].getList()

	def previous(self):
		self.updatePos()
		self.selectedList -= 1
		if self.selectedList < 0:
			self.selectedList = 2
		self.updateList()
		self.updateTabColour()

	def next(self):
		self.updatePos()
		self.selectedList += 1
		if self.selectedList > 2:
			self.selectedList = 0
		self.updateList()
		self.updateTabColour()

	def createLists(self):
		self.list0 = []
		self.list0.append(getConfigListEntry(_('Při dlouhém stisku tlačítka INFO(EPG)'), config.misc.CSFD.Info_EPG))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v menu Pluginů?'), config.misc.CSFD.ShowInPluginMenu))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v menu INFO(EPG)?'), config.misc.CSFD.ShowInEventInfoMenu))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v menu Extension?'), config.misc.CSFD.ShowInExtensionMenu))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v Hlavním menu?'), config.misc.CSFD.ShowInMenuStart))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v EPG SubMenu v PLI?'), config.misc.CSFD.ShowInEPGSubMenu))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v EPG místo MultiEPG?'), config.misc.CSFD.ShowEPGMulti))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v EPG výběru?'), config.misc.CSFD.ShowInEPGList))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v EPG výběru - modré tlačítko?'), config.misc.CSFD.ShowInEPGListBlueButton))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v EPG detailu?'), config.misc.CSFD.ShowInEPGDetail))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD v openATV/VIX imagích?'), config.misc.CSFD.ShowInATV))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD ve výběru nahraných pořadů?'), config.misc.CSFD.ShowInMovieSelection))
		self.list0.append(getConfigListEntry(_('Zobrazit CSFD informace při změně pořadu?'), config.misc.CSFD.ShowSimpleInfo))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 4'), config.misc.CSFD.HotKey4))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 5'), config.misc.CSFD.HotKey5))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 6'), config.misc.CSFD.HotKey6))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 7'), config.misc.CSFD.HotKey7))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 8'), config.misc.CSFD.HotKey8))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 9'), config.misc.CSFD.HotKey9))
		self.list0.append(getConfigListEntry(_('Akce pro klávesu 0'), config.misc.CSFD.HotKey0))
		self.list0.append(getConfigListEntry(_('Akce pro dlouhý stisk červeného tlačítka'), config.misc.CSFD.HotKeyLR))
		self.list0.append(getConfigListEntry(_('Akce pro dlouhý stisk zeleného tlačítka'), config.misc.CSFD.HotKeyLG))
		self.list0.append(getConfigListEntry(_('Akce pro dlouhý stisk modrého tlačítka'), config.misc.CSFD.HotKeyLB))
		self.list0.append(getConfigListEntry(_('Akce pro dlouhý stisk žlutého tlačítka'), config.misc.CSFD.HotKeyLY))
		self.list0.append(getConfigListEntry(_('Položka 01 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet1))
		self.list0.append(getConfigListEntry(_('Položka 02 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet2))
		self.list0.append(getConfigListEntry(_('Položka 03 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet3))
		self.list0.append(getConfigListEntry(_('Položka 04 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet4))
		self.list0.append(getConfigListEntry(_('Položka 05 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet5))
		self.list0.append(getConfigListEntry(_('Položka 06 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet6))
		self.list0.append(getConfigListEntry(_('Položka 07 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet7))
		self.list0.append(getConfigListEntry(_('Položka 08 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet8))
		self.list0.append(getConfigListEntry(_('Položka 09 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet9))
		self.list0.append(getConfigListEntry(_('Položka 10 pro rotaci v BOUQUETech'), config.misc.CSFD.Bouquet10))
		self.list1 = []
		self.list1.append(getConfigListEntry(_('Rozlišení'), config.misc.CSFD.Resolution))
		self.list1.append(getConfigListEntry(_('Povolit změnit CSFD ve skinu'), config.misc.CSFD.Skinxml))
		self.list1.append(getConfigListEntry(_('Povolit změnit OLED displej ve skinu'), config.misc.CSFD.SkinOLEDxml))
		self.list1.append(getConfigListEntry(_('Design CSFD obrazovek'), config.misc.CSFD.Design))
		self.list1.append(getConfigListEntry(_('Velikost fontu pro SD a HD rozlišení'), config.misc.CSFD.FontHeight))
		self.list1.append(getConfigListEntry(_('Velikost fontu pro FullHD rozlišení'), config.misc.CSFD.FontHeightFullHD))
		self.list1.append(getConfigListEntry(_('Maximální kvalita stahovaných posterů'), config.misc.CSFD.QualityPoster))
		self.list1.append(getConfigListEntry(_('Maximální kvalita stahovaných fotek z filmů'), config.misc.CSFD.QualityGallery))
		self.list1.append(getConfigListEntry(_('Maximální kvalita stahovaných fotek z videí'), config.misc.CSFD.QualityVideoPoster))
		self.list1.append(getConfigListEntry(_('Oddělovač tisíců'), config.misc.CSFD.ThousandsSeparator))
		self.list1.append(getConfigListEntry(_('Preferované rozlišení videa?'), config.misc.CSFD.VideoResolution))
		self.list1.append(getConfigListEntry(_('Načítat poster?'), config.misc.CSFD.PosterBasic))
		self.list1.append(getConfigListEntry(_('Povolit slideshow pro poster v základu?'), config.misc.CSFD.PosterBasicSlide))
		self.list1.append(getConfigListEntry(_('Změna posteru při slideshow v základu') + _('-def.10 (02 až 50)*0,5s'), config.misc.CSFD.PosterBasicSlideTime))
		self.list1.append(getConfigListEntry(_('Poster slideshow včetně fotek z galerie v základu?'), config.misc.CSFD.PosterBasicSlideInclGallery))
		self.list1.append(getConfigListEntry(_('Povolit slideshow pro galerii v detailu?'), config.misc.CSFD.GallerySlide))
		self.list1.append(getConfigListEntry(_('Změna galerie při slideshow v detailu') + _('-def.10 (02 až 50)*0,5s'), config.misc.CSFD.GallerySlideTime))
		self.list1.append(getConfigListEntry(_('Povolit slideshow pro poster v detailu?'), config.misc.CSFD.PosterSlide))
		self.list1.append(getConfigListEntry(_('Změna posteru při slideshow v detailu') + _('-def.10 (02 až 50)*0,5s'), config.misc.CSFD.PosterSlideTime))
		self.list1.append(getConfigListEntry(_('Zobrazit oddělovací linku v detailu?'), config.misc.CSFD.ShowLine))
		self.list1.append(getConfigListEntry(_('Zobrazovat tipy?'), config.misc.CSFD.TipsShow))
		self.list1.append(getConfigListEntry(_('Změna zobrazovaných tipů') + _('-def.15 (02 až 50)*0,5s'), config.misc.CSFD.TipsTime))
		self.list1.append(getConfigListEntry(_('Rotovat ratingy?'), config.misc.CSFD.RatingRotation))
		self.list1.append(getConfigListEntry(_('Změna jednotlivých ratingů') + _('-def.15 (02 až 50)*0,5s'), config.misc.CSFD.RatingRotationTime))
		self.list2 = []
#		self.list2.append(getConfigListEntry(_('Přihlásit se do CSFD?'), config.misc.CSFD.LoginToCSFD))
#		self.list2.append(getConfigListEntry(_('Uživatelské jméno pro CSFD:'), config.misc.CSFD.UserNameCSFD))
#		self.list2.append(getConfigListEntry(_('Heslo pro CSFD:'), config.misc.CSFD.PasswordCSFD))
#		self.list2.append(getConfigListEntry(_('Jak dlouho se nepřihlašovat po chybě') + _(' - def.10min.(1 až 240)'), config.misc.CSFD.LoginErrorWaiting))
		self.list2.append(getConfigListEntry(_('Při plné shodě ihned načíst detail?'), config.misc.CSFD.Detail100))
		self.list2.append(getConfigListEntry(_('Vyhledané výsledky třídit defaultně podle'), config.misc.CSFD.Default_Sort))
		self.list2.append(getConfigListEntry(_('Vyhledat defaultně všechny podobné pořady?'), config.misc.CSFD.FindAllItems))
		self.list2.append(getConfigListEntry(_('Vyhledávat včetně roku natáčení?'), config.misc.CSFD.FindInclYear))
		self.list2.append(getConfigListEntry(_('Porovnávat včetně roku natáčení?'), config.misc.CSFD.CompareInclYear))
		self.list2.append(getConfigListEntry(_('Načíst detail na základě skóre podobnosti?'), config.misc.CSFD.ReadDetailBasedOnScore))
		self.list2.append(getConfigListEntry(_('Vyhledávat včetně diakritiky pro pořady z EPG?'), config.misc.CSFD.FindInclDiacrEPG))
		self.list2.append(getConfigListEntry(_('Vyhledávat včetně diakritiky pro pořady z ostatních zdrojů?'), config.misc.CSFD.FindInclDiacrOth))
		self.list2.append(getConfigListEntry(_('Načíst další názvy z detailu kolika filmů?') + _(' def.2 (0 až 4)'), config.misc.CSFD.NumberOfReadMovieNameFromDetail))
#		self.list2.append(getConfigListEntry(_('Načíst seznam pořadů z CSFD pro daný kanál do cache?'), config.misc.CSFD.TVCache))
#		self.list2.append(getConfigListEntry(_('Jak dlouho nenačítat cache po net chybě') + _(' - def.10min.(1 až 240)'), config.misc.CSFD.LanErrorWaiting))
#		self.list2.append(getConfigListEntry(_('Třídící algoritmus pro vyhledané položky?'), config.misc.CSFD.SortFindItems))
		self.list2.append(getConfigListEntry(_('Zadávání znaků'), config.misc.CSFD.Input_Type))
		self.list2.append(getConfigListEntry(_('Při zadávání předvyplnit poslední hledaný pořad?'), config.misc.CSFD.SaveSearch))
		self.list2.append(getConfigListEntry(_('Volat místo IMDB plugin CSFD?'), config.misc.CSFD.CSFDreplaceIMDB))
		self.list2.append(getConfigListEntry(_('Při volání IMDB odstranit diakritiku?'), config.misc.CSFD.IMDBCharsConversion))
		self.list2.append(getConfigListEntry(_('Automaticky kontrolovat nové verze pluginu?'), config.misc.CSFD.AutomaticVersionCheck))
		self.list2.append(getConfigListEntry(_('Automaticky kontrolovat nové beta verze pluginu?'), config.misc.CSFD.AutomaticBetaVersionCheck))
		self.list2.append(getConfigListEntry(_('Instalaci nové verze provádět pomocí příkazu?'), config.misc.CSFD.InstallCommand))
		self.list2.append(getConfigListEntry(_('Zachovat zpětnou kompatibilitu volání CSFD?'), config.misc.CSFD.BackCSFDCompatibility))
		self.list2.append(getConfigListEntry(_('Jazyk pro menu'), config.misc.CSFD.Language))
		self.list2.append(getConfigListEntry(_('Komentáře'), config.misc.CSFD.Comment_Sort))
		self.list2.append(getConfigListEntry(_('Priorita pluginu v menu') + _(' - def.100 (000 až 200)'), config.misc.CSFD.PriorityInMenu))
		self.list2.append(getConfigListEntry(_('Posun u titulků + v ms') + _(' - def.0 ms (0 až +60000=60s)'), config.misc.CSFD.PlayerSubtDelayPlus))
		self.list2.append(getConfigListEntry(_('Posun u titulků - v ms') + _(' - def.0 ms (0 až -60000=60s)'), config.misc.CSFD.PlayerSubtDelayMinus))
		self.list2.append(getConfigListEntry(_('Testovat funkčnost internetu?'), config.misc.CSFD.InternetTest))
		self.list2.append(getConfigListEntry(_('Timeout pro stahování') + _(' - def.15 (5 až 120)'), config.misc.CSFD.DownloadTimeOut))
		self.list2.append(getConfigListEntry(_('Ochrana před kompletním "zamrznutím" aplikace?'), config.misc.CSFD.AntiFreeze))
		self.list2.append(getConfigListEntry(_('Za jak dlouho se má ochrana aktivovat') + _(' - def.30s (20 až 60s)'), config.misc.CSFD.AntiFreezeLimit))
		self.list2.append(getConfigListEntry(_('Třídit EPG podle CZ&SK abecedy?'), config.misc.CSFD.SortEPG_CZ_SK))
		self.list2.append(getConfigListEntry(_('Logovat do systémové konzole?'), config.misc.CSFD.LogConsole))
		self.list2.append(getConfigListEntry(_('Logovat do konzole i čas?'), config.misc.CSFD.LogConsoleTime))
		self.list2.append(getConfigListEntry(_('Logovat do <adr.>CSFDlog.txt ?'), config.misc.CSFD.Log))
		self.list2.append(getConfigListEntry(_('Maximální velikost logu?'), config.misc.CSFD.LogMaxSize))
		self.list2.append(getConfigListEntry(_('Cesta <adr.> pro dočasné soubory a logy (def.: /tmp/ ) '), config.misc.CSFD.DirectoryTMP))
		self.list2.append(getConfigListEntry(_('Cesta <adr.> pro download videa (def.: /hdd/movie/ ) '), config.misc.CSFD.DirectoryVideoDownload))

	def updateTabColour(self):
		if self.selectedList == 0:
			self['config0'].instance.setForegroundColor(gRGB(CSFDColor_Sel_Tab))
			self['config1'].instance.setForegroundColor(gRGB(CSFDColor_Tab))
			self['config2'].instance.setForegroundColor(gRGB(CSFDColor_Tab))
		elif self.selectedList == 1:
			self['config1'].instance.setForegroundColor(gRGB(CSFDColor_Sel_Tab))
			self['config0'].instance.setForegroundColor(gRGB(CSFDColor_Tab))
			self['config2'].instance.setForegroundColor(gRGB(CSFDColor_Tab))
		else:
			self['config2'].instance.setForegroundColor(gRGB(CSFDColor_Sel_Tab))
			self['config0'].instance.setForegroundColor(gRGB(CSFDColor_Tab))
			self['config1'].instance.setForegroundColor(gRGB(CSFDColor_Tab))

	def updateList(self):
		self.list = []
		if self.selectedList == 0:
			self.list = self.list0
		elif self.selectedList == 1:
			self.list = self.list1
		else:
			self.list = self.list2
		self['config'].list = self.list
		self['config'].l.setList(self.list)
		if self.selectedList == 0:
			self['config'].setCurrentIndex(self.positionInConfig0)
		elif self.selectedList == 1:
			self['config'].setCurrentIndex(self.positionInConfig1)
		else:
			self['config'].setCurrentIndex(self.positionInConfig2)
		self['tabbar'].setPixmapNum(self.selectedList)

	def isChanged(self):
		is_changed = False
		for x in self.list0:
			is_changed |= x[1].isChanged()

		for x in self.list1:
			is_changed |= x[1].isChanged()

		for x in self.list2:
			is_changed |= x[1].isChanged()

		return is_changed

	def keySave(self):
		if self.isChanged():
			for x in self.list0:
				x[1].save()

			for x in self.list1:
				x[1].save()

			for x in self.list2:
				x[1].save()

			configfile.save()
			RefreshPlugins()
		self.close()

	def cancelConfirm(self, result):
		if not result:
			self.showInputHelp()
			return
		else:
			for x in self.list0:
				x[1].cancel()

			for x in self.list1:
				x[1].cancel()

			for x in self.list2:
				x[1].cancel()

			self.delay_timerHideConn = None
			del self.delay_timerHideConn
			self.delay_timerHide = None
			self.delay_timerShowConn = None
			del self.delay_timerShowConn
			self.delay_timerShow = None
			self.close()
			return

	def hideInputHelp(self):
		if isinstance(self['config'].getCurrent()[1], CSFDConfigText) or isinstance(self['config'].getCurrent()[1], CSFDConfigPassword):
			current = self['config'].getCurrent()
			if current[1].help_window.instance is not None:
				current[1].help_window.instance.hide()
		return

	def showInputHelp(self):
		if isinstance(self['config'].getCurrent()[1], CSFDConfigText) or isinstance(self['config'].getCurrent()[1], CSFDConfigPassword):
			current = self['config'].getCurrent()
			if current[1].help_window.instance is not None:
				current[1].help_window.instance.show()
		return

	def showInputHelpExt(self):
		self.delay_timerShow.start(0, 1)

	def keyCancel(self):
		if self.isChanged():
			self.delay_timerHide.start(0, 1)
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving settings?'))
		else:
			self.delay_timerHideConn = None
			del self.delay_timerHideConn
			self.delay_timerHide = None
			self.delay_timerShowConn = None
			del self.delay_timerShowConn
			self.delay_timerShow = None
			self.close()
		return

	def keyCancelCan(self):
		self.updatePos()
		self.keyCancel()
		self.updateList()

	def keySaveGreen(self):
		self.keySave()

	def keyCancelRed(self):
		self.keyCancelCan()

	def keyInfo(self):
		if self.Repair:
			self.delay_timerHide.start(0, 1)
			self.Repair(self)

	def keyNext(self):
		self.next()

	def keyPrevious(self):
		self.previous()

	def keyYellow(self):
		if self.TestLogin:
			self.delay_timerHide.start(0, 1)
			self.TestLogin(self)

	def updateAllPars(self):
		self.selectedList = 0
		self.createLists()
		self.updateList()
		self.updateTabColour()

	def ResetPars(self):
		if self.ResetParam:
			self.delay_timerHide.start(0, 1)
			self.ResetParam(self)

	def keyMenu(self):
		LogCSFD.WriteToFile('[CSFD] CSFDSetup - keyMenu - zacatek\n')
		self.delay_timerHide.start(0, 1)
		listP = ((_('Přejít na předchozí záložku'), 'tabPrev'), (_('Přejít na další záložku'), 'tabNext'))
		if self.Repair is not None:
			listP = listP + ((_('Opravit/Reinstalovat potřebné knihovny'), 'repair'),)
		if self.TestLogin is not None:
			listP = listP + ((_('Test přihlášení do CSFD'), 'testlogin'),)
		if self.ResetParam is not None:
			listP = listP + ((_('Resetování všech parametrů'), 'reset'),)
		listP = listP + ((_('Zpět'), 'end'),)
		self.session.openWithCallback(self.leaveKeyMenu, ChoiceBox, title=_('Menu'), list=listP)
		LogCSFD.WriteToFile('[CSFD] CSFDSetup - keyMenu - konec\n')
		return

	def leaveKeyMenu(self, answer):
		LogCSFD.WriteToFile('[CSFD] CSFDSetup - leaveKeyMenu - zacatek\n')
		answer = answer and answer[1]
		if answer == 'end':
			self.delay_timerShow.start(0, 1)
		elif answer == 'tabPrev':
			self.previous()
		elif answer == 'tabNext':
			self.next()
		elif answer == 'repair':
			self.Repair(self)
		elif answer == 'testlogin':
			self.TestLogin(self)
		elif answer == 'reset':
			self.ResetPars()
		answer = None
		LogCSFD.WriteToFile('[CSFD] CSFDSetup - leaveKeyMenu - konec\n')
		return


class CSFDInputText(Screen, CSFDConfigListScreen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDInputTextSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDInputTextHD
	else:
		skin = Screen_CSFDInputTextFullHD

	def __init__(self, session, args=None):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDInputTextSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDInputTextHD
		else:
			self.skin = Screen_CSFDInputTextFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDInputTextSD', 'CSFDInputText']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDInputTextHD', 'CSFDInputText']
			else:
				self.skinName = [
				 'CSFDInputTextFullHD', 'CSFDInputText']
		else:
			self.skinName = 'CSFDInputText__'
		self.setup_title = _('CSFD')
		self['actions'] = ActionMap(['SetupActions'], {'ok': self.keyOK, 
		   'save': self.keySave, 
		   'cancel': self.keyCancel, 
		   'red': self.keyCancel, 
		   'green': self.keySave}, -1)
		self.onChangedEntry = []
		self.session = session
		self.list = []
		CSFDConfigListScreen.__init__(self, self.list, session=self.session)
		self.createSetup()
		self.onLayoutFinish.append(self.layoutFinished1)

	def layoutFinished1(self):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		try:
			self['config'].instance.setItemHeight(h1)
			if 'setFont' in dir(self['config'].instance):
				self['config'].instance.setFont(gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDInputText - nelze nastavit velikost fontu v menu (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDInputText - chyba - nelze nastavit velikost fontu v menu (stara verze enigma2)\n')
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_('Zadej název hledaného pořadu:'), config.misc.CSFD.InputSearch))
		self['config'].list = self.list
		self['config'].l.setList(self.list)

	def keyOK(self):
		self.close(config.misc.CSFD.InputSearch.getValue())

	def keySave(self):
		self.close(config.misc.CSFD.InputSearch.getValue())

	def keyCancel(self):
		self.close(None)
		return


class CSFDAbout(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDAboutSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDAboutHD
	else:
		skin = Screen_CSFDAboutFullHD

	def __init__(self, session, verze, datum_verze):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDAboutSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDAboutHD
		else:
			self.skin = Screen_CSFDAboutFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDAboutSD', 'CSFDAbout']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDAboutHD', 'CSFDAbout']
			else:
				self.skinName = [
				 'CSFDAboutFullHD', 'CSFDAbout']
		else:
			self.skinName = 'CSFDAbout__'
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.keyOK, 
		   'cancel': self.keyCancel, 
		   'green': self.keyOK, 
		   'red': self.keyCancel}, -1)
		self.onLayoutFinish.append(self.layoutFinished)
		self['oktext'] = Label(_('OK'))
		self['label1'] = Label('Plugin CSFD	 (2010 - 2017)	www.TVplugins.cz')
		self['label2'] = Label(_('(prohlížeč stránek CSFD.cz na platformě Enigma2)'))
		self['label3'] = Label('')
		self['label4'] = Label(_('Verze: ') + str(verze) + ' (' + str(datum_verze) + ')')
		self['label5'] = Label('© Autor pluginu: petrkl12	  email: petrkl12@tvplugins.cz')
		self['label6'] = Label('')
		self['label7'] = Label(_('Nápady na zlepšení, připomínky a chyby'))
		self['label8'] = Label(_('posílejte na můj email. Díky.'))
		self['label9'] = Label('')
		self['label10'] = Label('© ' + _('Název, grafické logo') + ' "CSFD - Česko-Slovenská filmová')
		self['label11'] = Label('databáze" ' + _('i obsahová část jsou vlastnictvím společnosti'))
		self['label12'] = Label('POMO Media Group s.r.o.')
		self['label13'] = Label('')
		self.session = session

	def layoutFinished(self):
		sss = _('Informace o pluginu CSFD')
		self.setTitle(sss)

	def keyOK(self):
		self.close()

	def keyCancel(self):
		self.close()


class CalcSizeText():

	def __init__(self, calc_label=None, velRadku=22):
		self.calc_text = calc_label
		self.textCallback = None
		self.velRadku = velRadku
		puvFont = self.calc_text.instance.getFont()
		try:
			if 'setFont' in dir(self.calc_text.instance):
				self.calc_text.instance.setFont(gFont(puvFont.family, self.velRadku))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDClasses - CalcSizeText - nelze nastavit velikost fontu (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDClasses - chyba - CalcSizeText - nelze nastavit velikost fontu (stara verze enigma2)\n')

		vel_calc_text = self.calc_text.instance.size()
		self.vely_calcText = vel_calc_text.height()
		self.MaxCharInRow = 40
		self.AutoAdjustMaxCharInRow = True
		self.SetTextField(vel_calc_text.width())
		return

	def setSizeRow(self, velRadku):
		self.velRadku = velRadku
		puvFont = self.calc_text.instance.getFont()
		try:
			if 'setFont' in dir(self.calc_text.instance):
				self.calc_text.instance.setFont(gFont(puvFont.family, self.velRadku))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDClasses - setSizeRow - nelze nastavit velikost fontu (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDClasses - chyba - setSizeRow - nelze nastavit velikost fontu (stara verze enigma2)\n')

		self.calc_text.setText('TESTICEK')
		text_height = self.calc_text.instance.calculateSize().height()
		if text_height > self.velRadku:
			self.velRadku = text_height

	def getSizeRow(self):
		return self.velRadku

	def setMaxCharInRow(self, maxCharInRow, autoAdjust=False):
		self.MaxCharInRow = maxCharInRow
		self.AutoAdjustMaxCharInRow = autoAdjust

	def getMaxCharInRow(self):
		return self.MaxCharInRow

	def SetTextField(self, velx):
		vel_calc_text = self.calc_text.instance.size()
		self.vely_calcText = vel_calc_text.height()
		self.calc_text.instance.resize(eSize(velx, self.vely_calcText))

	def SetTextCallback(self, textCallback=None):
		self.textCallback = textCallback

	def SetRowChar(self, text='', vel=0):
		text = text.rstrip('\n')
		if text == '' or vel == 0:
			return text
		if isinstance(text, str):
			text = Uni8(text)
		self.calc_text.setText(strUni(text))
		text_width = self.calc_text.instance.calculateSize().width()
		oldtext_width = -2
		newtext = text
		while text_width < vel:
			newtext += text
			self.calc_text.setText(strUni(newtext))
			text_width = self.calc_text.instance.calculateSize().width()
			if text_width == oldtext_width:
				break
			else:
				oldtext_width = text_width

		return newtext

	def DivideText(self, radek='', barva=0, zapis=True):
		radek = radek.rstrip()
		radek = radek.rstrip('\n')
		if isinstance(radek, str):
			radek = Uni8(radek)
		ss = radek
		self.calc_text.setText(strUni(ss))
		text_height = self.calc_text.instance.calculateSize().height()
		while text_height > self.velRadku:
			oddel = ' '
			poz_mezera = 0
			text_height = -2
			pamat_poz_r = -2
			while text_height <= self.velRadku:
				poz_r = ss.find(oddel, poz_mezera + 1)
				if poz_r < 0:
					poz_r = len(radek)
					if poz_mezera == 0:
						pamat_poz_r = -2
						poz_r = 0
						if oddel == ' ':
							oddel = ','
						elif oddel == ',':
							oddel = '.'
						elif oddel == '.':
							oddel = '-'
						else:
							poz_mezera = self.MaxCharInRow
							break
					else:
						break
				if pamat_poz_r == poz_r:
					pamat_poz_r = -2
					if poz_mezera == 0:
						poz_r = 0
						if oddel == ' ':
							oddel = ','
						elif oddel == ',':
							oddel = '.'
						elif oddel == '.':
							oddel = '-'
						else:
							poz_mezera = self.MaxCharInRow
							break
				else:
					pamat_poz_r = poz_r
				ss_r = ss[0:poz_r]
				self.calc_text.setText(strUni(ss_r))
				text_height = self.calc_text.instance.calculateSize().height()
				if text_height <= self.velRadku:
					poz_mezera = poz_r
				else:
					test_r = ss[0:poz_mezera].rstrip()
					self.calc_text.setText(strUni(test_r))
					test_height = self.calc_text.instance.calculateSize().height()
					if test_height > self.velRadku or poz_mezera == 0:
						poz_mezera = 0
						text_height = -2
						pamat_poz_r = -2
						poz_r = 0
						if oddel == ' ':
							oddel = ','
						elif oddel == ',':
							oddel = '.'
						elif oddel == '.':
							oddel = '-'
						else:
							poz_mezera = self.MaxCharInRow
							break

			radek = ss[0:poz_mezera].rstrip()
			if zapis:
				self.textCallback(radek, barva)
			if self.AutoAdjustMaxCharInRow:
				ii = int(round(float(len(radek)) / 100 * 85, 0))
				if ii > self.MaxCharInRow:
					self.MaxCharInRow = ii
			ss = ss[poz_mezera:len(ss)]
			self.calc_text.setText(strUni(ss))
			text_height = self.calc_text.instance.calculateSize().height()

		radek = ss.rstrip()
		text_width = self.calc_text.instance.calculateSize().width()
		if zapis:
			self.textCallback(radek, barva)
		return text_width


class CSFDHistory(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDHistorySD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDHistoryHD
	else:
		skin = Screen_CSFDHistoryFullHD

	def __init__(self, session):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDHistorySD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDHistoryHD
		else:
			self.skin = Screen_CSFDHistoryFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDHistorySD', 'CSFDHistory']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDHistoryHD', 'CSFDHistory']
			else:
				self.skinName = [
				 'CSFDHistoryFullHD', 'CSFDHistory']
		else:
			self.skinName = 'CSFDHistory__'
		self['CSFDHistoryActions'] = ActionMap(['CSFDHistoryActions'], {'ok': self.keyOK, 
		   'cancel': self.keyCancel, 
		   'green': self.keyOK, 
		   'red': self.keyCancel, 
		   'up': self.keyUp, 
		   'down': self.keyDown}, -1)
		self.onLayoutFinish.append(self.layoutFinished)
		self['oktext'] = Label(_('OK'))
		self['text'] = ItemListTypeSpecial([])
		self['calc_text'] = Label('')
		self['calc_text'].hide()
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.velRadku = int(config.misc.CSFD.FontHeight.getValue())
			self.meziRadky = 2
		else:
			self.velRadku = int(config.misc.CSFD.FontHeightFullHD.getValue())
			self.meziRadky = 3
		self.list = []
		self.velx = 0
		self.session = session
		self.CalcSizeText = None
		return

	def layoutFinished(self):
		sss = _('Historie změn v pluginu CSFD')
		self.setTitle(sss)
		self.velx = self['text'].instance.size().width()
		self.CalcSizeText = CalcSizeText(self['calc_text'], self.velRadku)
		self.CalcSizeText.SetTextField(self.velx - 30)
		self.CalcSizeText.setSizeRow(self.velRadku)
		self.CalcSizeText.SetTextCallback(self.createListofItems)
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.CalcSizeText.setMaxCharInRow(50, True)
		else:
			self.CalcSizeText.setMaxCharInRow(100, True)
		self.ReadHistoryFromFile()

	def keyUp(self):
		self['text'].instance.moveSelection(self['text'].instance.pageUp)

	def keyDown(self):
		self['text'].instance.moveSelection(self['text'].instance.pageDown)

	def createListofItems(self, radek='', barva=0):
		res = [['']]
		res.append(MultiContentEntryText(pos=(0, 0), size=(self.velx, self.velRadku + self.meziRadky), font=0, flags=RT_HALIGN_LEFT | RT_WRAP | RT_VALIGN_TOP, text=strUni(radek), color=barva, color_sel=barva))
		self.list.append(res)

	def GetRowColour(self, radek='', cislo_r=0):
		if isinstance(radek, str):
			radek = Uni8(radek)
		rad_barva = CSFDratingColor_Nothing
		if cislo_r < 2:
			rad_barva = CSFDColor_Titel
		j = radek.find('Díky za pomoc')
		if j == 0:
			rad_barva = CSFDColor_Highlight
		j = radek.find('Verze ')
		if j == 0:
			rad_barva = CSFDColor_Titel
		j = radek.find('----')
		if j == 0:
			rad_barva = CSFDColor_Titel
		j = radek.find('¯¯¯¯')
		if j == 0:
			rad_barva = CSFDColor_Titel
		j = radek.find('____')
		if j == 0:
			rad_barva = CSFDColor_Titel
		return rad_barva

	def ReadHistoryFromFile(self):
		self.list = []
		filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/CSFD_history.txt')
		file_h = file(filename, 'r')
		cisloRadku = 0
		pamatradek = ''
		rad_barva = CSFDratingColor_Nothing
		for radek in file_h:
			if pamatradek != '':
				velikost = self.CalcSizeText.DivideText(radek, rad_barva, False)
				pamatradek = self.CalcSizeText.SetRowChar(pamatradek, velikost)
				rad_barva = self.GetRowColour(pamatradek, cisloRadku - 1)
				oldvelikost = self.CalcSizeText.DivideText(pamatradek, rad_barva, True)
				pamatradek = ''
			j = radek.find('$$$A')
			if j == 0:
				radek = radek[4:]
				radek = self.CalcSizeText.SetRowChar(radek, oldvelikost)
			j = radek.find('$$$B')
			if j == 0:
				pamatradek = radek[4:]
			else:
				rad_barva = self.GetRowColour(radek, cisloRadku)
				oldvelikost = self.CalcSizeText.DivideText(radek, rad_barva, True)
			cisloRadku = cisloRadku + 1

		file_h.close()
		self['text'].selectionEnabled(False)
		self['text'].l.setList(self.list)
		self['text'].instance.moveSelectionTo(0)
		self['text'].show

	def keyOK(self):
		self.close()

	def keyCancel(self):
		self.close()


class CSFDVideoInfoScreen(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDVideoInfoScreenSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDVideoInfoScreenHD
	else:
		skin = Screen_CSFDVideoInfoScreenFullHD

	def __init__(self, session, aktvideo, video_url='', titulky_url='', eventNameLocal='', colorOLED=10):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDVideoInfoScreenSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDVideoInfoScreenHD
		else:
			self.skin = Screen_CSFDVideoInfoScreenFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDVideoInfoScreenSD', 'CSFDVideoInfoScreen']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDVideoInfoScreenHD', 'CSFDVideoInfoScreen']
			else:
				self.skinName = [
				 'CSFDVideoInfoScreenFullHD', 'CSFDVideoInfoScreen']
		else:
			self.skinName = 'CSFDVideoInfoScreen__'
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.keyOK, 
		   'cancel': self.keyCancel, 
		   'green': self.keyOK, 
		   'red': self.keyCancel}, -1)
		self.aktvideo = aktvideo
		self.eventNameLocal = eventNameLocal
		self.colorOLED = colorOLED
		self.summaries.setText(self.eventNameLocal + ' - ' + self.aktvideo[2], self.colorOLED)
		self.onLayoutFinish.append(self.layoutFinished)
		self['oktext'] = Label(_('OK'))
		self['label1'] = Label(_('Informace o přehrávaném videu:'))
		self['label2'] = Label(eventNameLocal)
		self['label3'] = Label('')
		self['label4'] = Label(_('Název: ') + aktvideo[2])
		ss = video_url.rsplit('/', 2)
		self['label5'] = Label('(' + ss[1] + '_' + ss[2] + ')')
		self['label6'] = Label('')
		if titulky_url == '':
			ss = _('Ne')
			self['label7'] = Label(_('Titulky: ') + ss)
			self['label8'] = Label('')
		else:
			ss = _('Ano')
			self['label7'] = Label(_('Titulky: ') + ss)
			ss = titulky_url.rsplit('/', 2)
			self['label8'] = Label('(' + ss[1] + '_' + ss[2] + ')')
		self.onLayoutFinish.append(self.layoutFinished)
		self.session = session

	def layoutFinished(self):
		sss = _('Video - CSFD')
		self.setTitle(sss)
		self.summaries.setText(self.eventNameLocal + ' - ' + self.aktvideo[2], self.colorOLED)

	def keyOK(self):
		self.close()

	def keyCancel(self):
		self.close()

	def createSummary(self):
		return CSFDLCDSummary


class CSFDPlayer(Screen, SubsSupport, InfoBarNotifications, InfoBarSubtitleSupport):
	LogCSFD.WriteToFile('[CSFD] CSFDPlayer - zacatek\n')
	STATE_IDLE = 0
	STATE_PLAYING = 1
	STATE_PAUSED = 2
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDPlayerSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDPlayerHD
	else:
		skin = Screen_CSFDPlayerFullHD
	LogCSFD.WriteToFile('[CSFD] CSFDPlayer - konec\n')

	def __init__(self, session, service, lastservice, subtitles, infoCallback=None, nextCallback=None, prevCallback=None, exitCallback=None, existPrevOrNextCallback=None, downloadVideo=None, colorOLED=10):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - Init - zacatek\n')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDPlayerSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDPlayerHD
		else:
			self.skin = Screen_CSFDPlayerFullHD
		Screen.__init__(self, session)
		InfoBarNotifications.__init__(self)
		InfoBarSubtitleSupport.__init__(self)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDPlayerSD', 'CSFDPlayer']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDPlayerHD', 'CSFDPlayer']
			else:
				self.skinName = [
				 'CSFDPlayerFullHD', 'CSFDPlayer']
		else:
			self.skinName = 'CSFDPlayer__'
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitles ' + Uni8(subtitles) + '\n')
		self.subtitles = subtitles
		SubsSupport.__init__(self, subPath=self.subtitles, defaultPath='/tmp', forceDefaultPath=True, subclassOfScreen=False)
		SubsSupport.setPlayerDelay(self, config.misc.CSFD.PlayerSubtDelayPlus.getValue() - config.misc.CSFD.PlayerSubtDelayMinus.getValue())
		self.lastservice = lastservice
		self.session = session
		self.service = service
		self.infoCallback = infoCallback
		self.nextCallback = nextCallback
		self.prevCallback = prevCallback
		self.exitCallback = exitCallback
		self.existPrevOrNextCallback = existPrevOrNextCallback
		self.downloadVideo = downloadVideo
		self.screen_timeout = 5000
		self.download_timeout = 1500
		self.nextservice = None
		self.colorOLED = colorOLED
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - evEOF\n')
		self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged, 
		   iPlayableService.evStart: self.__serviceStarted, 
		   iPlayableService.evEOF: self.__evEOF})

		class CSFDSeekActionMap(ActionMap):

			def __init__(self, screen, seekProc, *args, **kwargs):
				ActionMap.__init__(self, screen, *args, **kwargs)
				self.screen = screen
				self.seekProc = seekProc

			def action(self, contexts, action):
				if action[:5] == 'seek:':
					time = int(action[5:])
					self.seekProc(time * 90000)
					return 1
				else:
					if action[:8] == 'seekdef:':
						key = int(action[8:])
						time = (-config.seek.selfdefined_13.getValue(), False, config.seek.selfdefined_13.getValue(),
						 -config.seek.selfdefined_46.getValue(), False, config.seek.selfdefined_46.getValue(),
						 -config.seek.selfdefined_79.getValue(), False, config.seek.selfdefined_79.getValue())[(key - 1)]
						self.seekProc(time * 90000)
						time = None
						return 1
					else:
						return ActionMap.action(self, contexts, action)

					return

		self['actions'] = CSFDSeekActionMap(['CSFDPlayerActions'], self.doSeekRelative, {'ok': self.ok, 
		   'cancel': self.leavePlayer, 
		   'stop': self.leavePlayer, 
		   'menu': self.leavePlayer, 
		   'play': self.unPauseService, 
		   'pause': self.pauseService, 
		   'playpause': self.playpauseService, 
		   'next': self.playNextFile, 
		   'previous': self.playPrevFile, 
		   'record': self.downloadMovie, 
		   'videoInfo': self.showVideoInfo, 
		   'subtitles': self.subtitlesSetup}, -2)
		self.hidetimer = eTimer()
		self.hidetimerConn = None
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.hidetimer.timeout.get().append(self.ok)
		else:
			self.hidetimerConn = self.hidetimer.timeout.connect(self.ok)
		self.returning = False
		self.state = self.STATE_PLAYING
		self.lastseekstate = self.STATE_PLAYING
		self.onPlayStateChanged = []
		self.__seekableStatusChanged()
		self.onClose.append(self.__onClose)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - Init - konec\n')
		self.play()
		return

	def subtitlesSetup(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitlesSetup - zacatek\n')
		SubsSupport.subsMenu(self)
		SubsSupport.resumeSubs(self)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitlesSetup - konec\n')

	def __onClose(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __onClose - zacatek\n')
		if self.hidetimer.isActive():
			self.hidetimer.stop()
		self.session.nav.stopService()
		self.session.nav.playService(self.lastservice)
		self.exitCallback()
		SubsSupport.exitSubs(self)
		InfoBarNotifications = None
		InfoBarSubtitleSupport = None
		self.__event_tracker = None
		self.hidetimerConn = None
		self.hidetimer = None
		self.infoCallback = None
		self.nextCallback = None
		self.prevCallback = None
		self.exitCallback = None
		self.existPrevOrNextCallback = None
		self.downloadVideo = None
		self.screen_timeout = None
		self.download_timeout = None
		self.colorOLED = None
		self.onPlayStateChanged = []
		del self.nextservice
		del self.hidetimerConn
		del self.hidetimer
		del self.__event_tracker
		del self.lastservice
		del self.service
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __onClose - konec\n')
		return

	def __evEOF(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evEOF - zacatek\n')
		self.close()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evEOF - konec\n')

	def __evAudioDecodeError(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evAudioDecodeError - zacatek\n')
		currPlay = self.session.nav.getCurrentService()
		sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evAudioDecodeError: ' + sTagAudioCodec + '\n')
		self.session.open(MessageBox, _('Tento box nemůže dekódovat audiostream: %s') % sTagAudioCodec, type=MessageBox.TYPE_ERROR, timeout=20)
		sTagAudioCodec = None
		currPlay = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evAudioDecodeError - konec\n')
		return

	def __evVideoDecodeError(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evVideoDecodeError - zacatek\n')
		currPlay = self.session.nav.getCurrentService()
		sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evVideoDecodeError: ' + sTagVideoCodec + '\n')
		self.session.open(MessageBox, _('Tento box nemmůže dekódovat videostream: %s') % sTagVideoCodec, type=MessageBox.TYPE_ERROR, timeout=20)
		sTagVideoCodec = None
		currPlay = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evVideoDecodeError - konec\n')
		return

	def __evPluginError(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError - zacatek\n')
		currPlay = self.session.nav.getCurrentService()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError - zacatek1\n')
		message = currPlay.info().getInfoString(iServiceInformation.sUser + 12)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError - zacatek2\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError: ' + message + '\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError - zacatek3\n')
		self.session.open(MessageBox, message, type=MessageBox.TYPE_ERROR, timeout=20)
		message = None
		currPlay = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evPluginError - konec\n')
		return

	def __evStreamingSrcError(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evStreamingSrcError - zacatek\n')
		currPlay = self.session.nav.getCurrentService()
		message = currPlay.info().getInfoString(iServiceInformation.sUser + 12)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evStreamingSrcError: ' + message + '\n')
		self.session.open(MessageBox, _('Chyba streamování: %s') % message, type=MessageBox.TYPE_ERROR, timeout=20)
		message = None
		currPlay = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __evStreamingSrcError - konec\n')
		return

	def __setHideTimer(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __setHideTimer - zacatek\n')
		if self.hidetimer.isActive():
			self.hidetimer.stop()
		self.hidetimer.start(self.screen_timeout)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __setHideTimer - konec\n')

	def showInfobar(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - showInfobar - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		self.show()
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if self.state == self.STATE_PLAYING:
			self.__setHideTimer()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - showInfobar - konec\n')

	def subtitleSelection(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitleSelection - zacatek\n')
		if CSFDGlobalVar.getAudioSelectionexist():
			from Screens.AudioSelection import SubtitleSelection
			self.session.open(SubtitleSelection, self)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitleSelection - nenalezeno\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - subtitleSelection - konec\n')

	def hideInfobar(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - hideInfobar - zacatek\n')
		self.hide()
		if self.hidetimer.isActive():
			self.hidetimer.stop()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - hideInfobar - konec\n')

	def ok(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - ok - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if self.shown:
			self.hideInfobar()
		else:
			self.showInfobar()
		self.summaries.setText(self.service.getName(), self.colorOLED)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - ok - konec\n')

	def showVideoInfo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - showVideoInfo - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if self.shown:
			self.hideInfobar()
		if self.infoCallback is not None:
			self.infoCallback()
		self.summaries.setText(self.service.getName(), self.colorOLED)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - showVideoInfo - konec\n')
		return

	def playNextFile(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playNextFile - zacatek\n')
		nextservice, self.subtitles, error = self.nextCallback()
		if nextservice is None:
			self.handleLeave(error)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playNextFile: ' + nextservice.getName() + '\n')
			self.playService(nextservice)
			self.showInfobar()
			nextservice = None
		error = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playNextFile - konec\n')
		return

	def playPrevFile(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playPrevFile - zacatek\n')
		prevservice, self.subtitles, error = self.prevCallback()
		if prevservice is None:
			self.handleLeave(error)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playPrevFile: ' + prevservice.getName() + '\n')
			self.playService(prevservice)
			self.showInfobar()
			prevservice = None
		error = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playPrevFile - konec\n')
		return

	def playagain(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playagain - zacatek\n')
		if self.state != self.STATE_IDLE:
			self.stopCurrent()
		self.play()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playagain - konec\n')

	def playService(self, newservice):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playService - zacatek\n')
		if self.state != self.STATE_IDLE:
			self.stopCurrent()
		self.service = newservice
		self.play()
		newservice = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playService - konec\n')
		return

	def play(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - play - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if self.state == self.STATE_PAUSED:
			if self.shown:
				self.__setHideTimer()
		self.state = self.STATE_PLAYING
		SubsSupport.resetSubs(self, True)
		self.session.nav.playService(self.service)
		SubsSupport.loadSubs(self, self.subtitles)
		SubsSupport.startSubs(self, 2000)
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if self.shown:
			self.__setHideTimer()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - play - konec\n')

	def stopCurrent(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - stopCurrent - zacatek\n')
		self.session.nav.stopService()
		self.state = self.STATE_IDLE
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - stopCurrent - konec\n')

	def playpauseService(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playpauseService - zacatek\n')
		if self.state == self.STATE_PLAYING:
			self.pauseService()
		elif self.state == self.STATE_PAUSED:
			self.unPauseService()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - playpauseService - konec\n')

	def pauseService(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - pauseService - zacatek\n')
		if self.state == self.STATE_PLAYING:
			self.setSeekState(self.STATE_PAUSED)
			SubsSupport.pauseSubs(self)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - pauseService - konec\n')

	def unPauseService(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - unpauseService - zacatek\n')
		if self.state == self.STATE_PAUSED:
			self.setSeekState(self.STATE_PLAYING)
			SubsSupport.resumeSubs(self)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - unpauseService - konec\n')

	def getSeek(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - getSeek - zacatek\n')
		service = self.session.nav.getCurrentService()
		if service is None:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - getSeek - Service - None - konec\n')
			return
		else:
			seek = service.seek()
			if seek is None or not seek.isCurrentlySeekable():
				LogCSFD.WriteToFile('[CSFD] CSFDPlayer - getSeek - Seek - None - konec\n')
				service = None
				return
			service = None
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - getSeek - konec\n')
			return seek

	def isSeekable(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - isSeekable - zacatek\n')
		if self.getSeek() is None:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - isSeekable - False - konec\n')
			return False
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - isSeekable - True - konec\n')
			return True

	def doSeekRelative(self, pts):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doSeekRelative - zacatek\n')
		seekable = self.getSeek()
		if seekable is None:
			return
		else:
			prevstate = self.state
			if self.state == self.STATE_IDLE:
				if prevstate == self.STATE_PAUSED:
					self.setSeekState(self.STATE_PAUSED)
				else:
					self.setSeekState(self.STATE_PLAYING)
			seekable.seekRelative(pts < 0 and -1 or 1, abs(pts))
			if abs(pts) > 100 and config.usage.show_infobar_on_skip.getValue():
				self.ok()
			SubsSupport.playAfterSeek(self)
			seekable = None
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doSeekRelative - konec\n')
			return

	def __seekableStatusChanged(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __seekableStatusChanged - zacatek\n')
		if not self.isSeekable():
			self.setSeekState(self.STATE_PLAYING)
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - not seekable\n')
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - seekable\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __seekableStatusChanged - konec\n')

	def __serviceStarted(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __serviceStarted - zacatek\n')
		self.state = self.STATE_PLAYING
		self.__seekableStatusChanged()
		SubsSupport.resumeSubs(self)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - __serviceStarted - konec\n')

	def setSeekState(self, wantstate):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - setSeekState - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		if wantstate == self.STATE_PAUSED:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - trying to switch to pause - state:' + str(self.STATE_PAUSED) + '\n')
		elif wantstate == self.STATE_PLAYING:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - trying to switch to playing - state:' + str(self.STATE_PLAYING) + '\n')
		service = self.session.nav.getCurrentService()
		if service is None:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - No Service found\n')
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - setSeekState - konec\n')
			return False
		else:
			pauseable = service.pause()
			if pauseable is None:
				LogCSFD.WriteToFile('[CSFD] CSFDPlayer - not pauseable\n')
				self.state = self.STATE_PLAYING
			if pauseable is not None:
				LogCSFD.WriteToFile('[CSFD] CSFDPlayer - service is pauseable\n')
				if wantstate == self.STATE_PAUSED:
					LogCSFD.WriteToFile('[CSFD] CSFDPlayer - want to pause\n')
					pauseable.pause()
					self.state = self.STATE_PAUSED
					if not self.shown:
						self.hidetimer.stop()
						self.show()
				elif wantstate == self.STATE_PLAYING:
					LogCSFD.WriteToFile('[CSFD] CSFDPlayer - want to play\n')
					pauseable.unpause()
					self.state = self.STATE_PLAYING
					if self.shown:
						self.__setHideTimer()
			for c in self.onPlayStateChanged:
				c(self.state)

			service = None
			pauseable = None
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - setSeekState True - konec\n')
			return True

	def handleLeave(self, error=False):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - handleLeave - zacatek\n')
		self.summaries.setText(self.service.getName(), self.colorOLED)
		prevS, nextS = self.existPrevOrNextCallback()
		listP = ((_('Ano'), 'quit'), (_('Ne, ale přehrát video znovu'), 'playagain'))
		if nextS:
			listP = listP + ((_('Ano, ale přehrát další video'), 'playnext'),)
		if prevS:
			listP = listP + ((_('Ano, ale přehrát předchozí video'), 'playprev'),)
		listP = listP + ((_('Uložit video'), 'downloadmovie'),)
		if error:
			self.session.openWithCallback(self.leavePlayerConfirmed, ChoiceBox, title=_('Nenalezeno video! Zastavit přehrávání?'), list=listP)
		else:
			self.session.openWithCallback(self.leavePlayerConfirmed, ChoiceBox, title=_('Zastavit přehrávání tohoto videa?'), list=listP)
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - handleLeave - konec\n')

	def leavePlayer(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - leavePlayer - zacatek\n')
		self.handleLeave()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - leavePlayer - konec\n')

	def downloadMovie(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - downloadMovie - zacatek\n')
		self.downloadVideo()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - downloadMovie - konec\n')

	def leavePlayerConfirmed(self, answer):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - leavePlayerConfirmed - zacatek\n')
		answer = answer and answer[1]
		if answer == 'quit':
			self.close()
		elif answer == 'playnext':
			self.playNextFile()
		elif answer == 'playprev':
			self.playPrevFile()
		elif answer == 'playagain':
			self.playagain()
		elif answer == 'downloadmovie':
			self.downloadMovie()
		answer = None
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - leavePlayerConfirmed - konec\n')
		return

	def doEofInternal(self, playing):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doEofInternal - zacatek\n')
		if not self.execing:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doEofInternal - not execing - konec\n')
			return
		if not playing:
			LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doEofInternal - not playing - konec\n')
			return
		self.handleLeave()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayer - doEofInternal - konec\n')

	def createSummary(self):
		return CSFDLCDSummary

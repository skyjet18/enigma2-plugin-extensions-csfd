# -*- coding: utf-8 -*-

from enigma import eTimer, ePicLoad, eServiceCenter, eServiceReference, eConsoleAppContainer, gPixmapPtr, gRGB, RT_HALIGN_LEFT, RT_VALIGN_CENTER
from .CSFDLog import LogCSFD
from .CSFDTools import ItemList, ItemListServiceMenu, TextSimilarityBigram, TextSimilarityLD, TextCompare, max_positions, request, requestFileCSFD, internet_on, fromRomanStr, StrtoRoman
from .CSFDTools import intWithSeparator, char2Diacritic, char2DiacriticSort, char2Allowchar, char2AllowcharNumbers, strUni, Uni8, deletetmpfiles, OdstranitDuplicityRadku, loadPixmapCSFD, picStartDecodeCSFD
from .CSFDMenu import CSFDIconMenu
from .CSFDParser import ParserCSFD, ParserOstCSFD, ParserVideoCSFD, GetItemColourRateN, GetItemColourRateC, GetItemColourN, NameMovieCorrections, NameMovieCorrectionsForCompare, GetCSFDNumberFromChannel, NameMovieCorrectionsForCTChannels, NameMovieCorrectionExtensions
from .CSFDClasses import GetMoviesForTVChannels, CSFDChannelSelection, CSFDEPGSelection, CSFDLCDSummary, CSFDSetup, CSFDInputText, CSFDAbout, CSFDHistory, CSFDVideoInfoScreen, CSFDPlayer, RefreshPlugins
from .CSFDMovieCache import TVMovieCache
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import _, localeInit, CSFDActionDict, std_media_header, MainUpdateUrl, MainUpdateUrlIpk, const_www_csfd, const_csfd_http_film, const_quick_page, ResetParams
from .CSFDSettings2 import config
from .CSFDSkinSelect import CSFDSkinSelect
from .CSFDSkinLoader import *
from .CSFDImdb import CSFD_IMDBcalls
from .CSFDHelpMenu import CSFDHelpableScreen
from .CSFDVirtualKeyBoard import CSFDVirtualKeyBoard
from .CSFDScrollColorLabel import CSFDScrollColorLabel
from .CSFDConsole import CSFDConsole
from .CSFDCache import movieCSFDCache
from .IMDBParser import ParserIMDB
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Standby import TryQuitMainloop
from ServiceReference import ServiceReference
from Components.ActionMap import HelpableActionMap
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Button import Button
from Components.AVSwitch import AVSwitch
from Components.ProgressBar import ProgressBar
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from Components.config import configfile
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import path as os_path
from random import randint, seed
import time, traceback

try:
	from urllib.parse import urlencode
	from urllib.parse import quote
except:
	from urllib import urlencode
	from urllib import quote

from .CSFDAndroidClient import csfdAndroidClient, CreateCSFDAndroidClient

LogCSFD.WriteToFile('[CSFD] Iniciace modulu CSFD.py* - zacatek\n')
deletetmpfiles()

class CSFDClass(Screen, CSFDHelpableScreen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFD_SD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFD_HD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
	else:
		skin = Screen_CSFD_FullHD % (config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue())

	def __init__(self, session, eventName='', callbackNeeded=False, EPG='', sourceEPG=False, DVBchannel='', *args, **kwargs):
		LogCSFD.WriteToFile('[CSFD] CSFDClass - init - zacatek\n')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFD_SD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFD_HD % (config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue(), config.misc.CSFD.FontHeight.getValue())
		else:
			self.skin = Screen_CSFD_FullHD % (config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue(), config.misc.CSFD.FontHeightFullHD.getValue())
		Screen.__init__(self, session)
		CSFDHelpableScreen.__init__(self, session, self.getHelpKeyDescr)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFD_SD', 'CSFD']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFD_HD', 'CSFD']
			else:
				self.skinName = [
				 'CSFD_FullHD', 'CSFD']
		else:
			self.skinName = 'CSFD__'
		localeInit()
		self.session = session
		self.LoggedUser = ''
		self.versionCSFD = config.misc.CSFD.Version.getValue()
		self.versionCSFDdate = config.misc.CSFD.VersionData.getValue()
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		if eventName is not None:
			self.eventName = eventName
		else:
			self.eventName = ''
		self.eventNameSecond = ''
		self.eventNameLocal = ''
		self.ActName = ''
		self.ChannelsCSFD = []
		if EPG is not None:
			self.EPG = EPG
		else:
			self.EPG = ''
		if DVBchannel is not None:
			self.DVBchannel = DVBchannel
		else:
			self.DVBchannel = ''
		if sourceEPG is not None:
			self.eventMovieSourceOfDataEPG = sourceEPG
		else:
			self.eventMovieSourceOfDataEPG = False
		self.Detail100Akce = True
		self.Detail100Exit = False
		self.Detail100Pozice = 0
		self.callbackNeeded = callbackNeeded
		self.callbackData = ''
		self.callbackGenre = ''
		self.IMDBpath = ''
		self.CSFDratingUsers = ''
		self.stahnutoCSFD2 = ''
		self.stahnutoCSFDImage = ''
		self.NacistNazevPoradu = False
		self.querySpecAkce = 'UserComments'
		self.eventMovieYears = []
		self.eventMovieNameYears = ''
		self.automaticUpdate = True
		self.container_output = ''
		self.container = eConsoleAppContainer()
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.container.dataAvail.append(self.consoleAppContainer_avail)
			self.dataAvail_conn = None
		else:
			self.dataAvail_conn = self.container.dataAvail.connect(self.consoleAppContainer_avail)
		self.workingConfig = None
		self.linkGlobal = ''
		self.selectedMenuRow = None
		self.linkSpec = ''
		self.LastDownloadedMovieUrl = ''
		self.linkComment = config.misc.CSFD.Comment_Sort.getValue()
		self.linkExtra = ''
		self.PageSpec = 1
		self.FunctionExists = []
		self.VideoIsNotFullyRead = True
		self.VideoDwnlIsNotStarted = True
		self.PosterIsNotFullyRead = True
		self.GalleryIsNotFullyRead = True
		self.ServiceMenuFlag = 0
		self['servicemenuBackG'] = Pixmap()
		self['servicemenuBackG'].hide()
		self['servicemenuTop'] = Label('M E N U')
		self['servicemenuTop'].hide()
		self['poster'] = Pixmap()
		self.picload = ePicLoad()
		self.PosterBasicSlideShowTimer = eTimer()
		self.NewVersionTimer = eTimer()
		self.LoadIMDBTimer = eTimer()
		self.GalleryDownloadTimer = eTimer()
		self.PosterDownloadTimer = eTimer()
		self.AntiFreezeTimer = eTimer()
		self.PosterSlideShowTimer = eTimer()
		self.GallerySlideShowTimer = eTimer()
		self.TipsTimer = eTimer()
		self.RatingTimer = eTimer()
		self.DownloadTimer = eTimer()
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.PosterBasicSlideShowTimer.callback.append(self.CSFDPosterBasicSlideShowEvent)
			self.NewVersionTimer.callback.append(self.NewVersionTimerEvent)
			self.LoadIMDBTimer.callback.append(self.LoadIMDBTimerEvent)
			self.GalleryDownloadTimer.callback.append(self.GalleryDownloadTimerEvent)
			self.PosterDownloadTimer.callback.append(self.PosterDownloadTimerEvent)
			self.AntiFreezeTimer.callback.append(self.AntiFreezeEvent)
			self.PosterSlideShowTimer.callback.append(self.CSFDPosterSlideShowEvent)
			self.GallerySlideShowTimer.callback.append(self.CSFDGallerySlideShowEvent)
			self.TipsTimer.callback.append(self.CSFDTipsTimerEvent)
			self.RatingTimer.callback.append(self.RatingTimerEvent)
			self.DownloadTimer.callback.append(self.DownloadParalel)
			self.PosterBasicSlideShowTimerConn = None
			self.NewVersionTimerConn = None
			self.LoadIMDBTimerConn = None
			self.GalleryDownloadTimerConn = None
			self.PosterDownloadTimerConn = None
			self.AntiFreezeTimerConn = None
			self.PosterSlideShowTimerConn = None
			self.GallerySlideShowTimerConn = None
			self.TipsTimerConn = None
			self.RatingTimerConn = None
			self.DownloadTimerConn = None
		else:
			self.PosterBasicSlideShowTimerConn = self.PosterBasicSlideShowTimer.timeout.connect(self.CSFDPosterBasicSlideShowEvent)
			self.NewVersionTimerConn = self.NewVersionTimer.timeout.connect(self.NewVersionTimerEvent)
			self.LoadIMDBTimerConn = self.LoadIMDBTimer.timeout.connect(self.LoadIMDBTimerEvent)
			self.GalleryDownloadTimerConn = self.GalleryDownloadTimer.timeout.connect(self.GalleryDownloadTimerEvent)
			self.PosterDownloadTimerConn = self.PosterDownloadTimer.timeout.connect(self.PosterDownloadTimerEvent)
			self.AntiFreezeTimerConn = self.AntiFreezeTimer.timeout.connect(self.AntiFreezeEvent)
			self.PosterSlideShowTimerConn = self.PosterSlideShowTimer.timeout.connect(self.CSFDPosterSlideShowEvent)
			self.GallerySlideShowTimerConn = self.GallerySlideShowTimer.timeout.connect(self.CSFDGallerySlideShowEvent)
			self.TipsTimerConn = self.TipsTimer.timeout.connect(self.CSFDTipsTimerEvent)
			self.RatingTimerConn = self.RatingTimer.timeout.connect(self.RatingTimerEvent)
			self.DownloadTimerConn = self.DownloadTimer.timeout.connect(self.DownloadParalel)
		self.PosterBasicCountPixAllP = -1
		self.PosterBasicCountPixAllG = -1
		self.PosterBasicCountPix = 0
		self.PosterBasicSlideStop = True
		self.PosterBasicActIdx = 0
		self.PosterBasicSlideList = []
		self.AntiFreezeTimerCounter = 0
		self.AntiFreezeTimerWorking = True
		self.PosterCountPix = 0
		self.PosterSlideStop = True
		self.PosterActIdx = 0
		self.PosterSlideList = []
		self.GalleryCountPix = 0
		self.GallerySlideStop = True
		self.GalleryActIdx = 0
		self.GallerySlideList = []
		self.GalleryPocFinished = 0
		self.videoklipurl = ''
		self.videotitulkyurl = ''
		self.KeyFlag = ''
		self.KeyPressLong = False
		self.VideoCountPix = 0
		self.VideoActIdx = 0
		self.VideoSlideList = []
		self.VideoPocFinished = 0
		self.UpdateUrl = ''
		self.UpdateFile = ''
		self.FindAllItems = config.misc.CSFD.FindAllItems.getValue()
		self['pagebg'] = Pixmap()
		self['pagebg'].hide()
		self['pageb1'] = Pixmap()
		self['pageb1'].hide()
		self['pageb3'] = Pixmap()
		self['pageb3'].hide()
		self['paget1'] = Pixmap()
		self['paget1'].hide()
		self['paget3'] = Pixmap()
		self['paget3'].hide()
		self['page'] = Label('')
		self['page'].hide()
		self['stars'] = ProgressBar()
		self['starsbg'] = Pixmap()
		self['starsmt'] = ProgressBar()
		self['starsmtbg'] = Pixmap()
		self['stars0'] = ProgressBar()
		self['starsbg0'] = Pixmap()
		self['stars50'] = ProgressBar()
		self['starsbg50'] = Pixmap()
		self['stars100'] = ProgressBar()
		self['starsbg100'] = Pixmap()
		self['stars'].hide()
		self['starsbg'].hide()
		self['starsmt'].hide()
		self['starsmtbg'].hide()
		self['stars0'].hide()
		self['starsbg0'].hide()
		self['stars50'].hide()
		self['starsbg50'].hide()
		self['stars100'].hide()
		self['starsbg100'].hide()
		self.ratingcount = 0
		self.ratingstars = -1
		self.ratingstarsIMDB = -1
		self.ratingstarsMetacritic = -1
		self.ratingtext = ''
		self.ratingtextIMDB = ''
		self.ratingtextMetacritic = ''
		self.myreference = None
		self['titellabel'] = Label(_('Filmová databáze CSFD.cz'))
		self['sortlabel'] = Label('')
		self['detailslabel'] = CSFDScrollColorLabel('')
		self['contentlabel'] = CSFDScrollColorLabel('')
		self['extralabel'] = CSFDScrollColorLabel('')
		self['photolabel'] = Pixmap()
		self['playbutton'] = Pixmap()
		self['line'] = Pixmap()
		self.posterload = ePicLoad()
		self.galleryload = ePicLoad()
		self.videoload = ePicLoad()
		self['statusbar'] = Label('')
		self['ratinglabel'] = Label('')
		self.resultlist = []
		self['key_red'] = Button(_('Zpět'))
		self['key_green'] = Button('')
		self['key_yellow'] = Button('')
		self['key_blue'] = Button('')
		self['tips_label'] = Label('')
		self['tips_label'].hide()
		self['tips_detail'] = Label('')
		self['tips_detail'].hide()
		self['tips_icon'] = Pixmap()
		self['tips_icon'].hide()
		self.tipsiconload = ePicLoad()
		if 'connect' in dir(self.tipsiconload.PictureData):
			self.tipsiconload_conn = None
			self.tipsiconload_conn = self.tipsiconload.PictureData.connect(self.paintTipsIcon)
		else:
			self.tipsiconload_conn = True
			self.tipsiconload.PictureData.get().append(self.paintTipsIcon)
		self.Tips = []
		self.saveKeyBlue = self['key_blue'].getText()
		self.saveKeyYellow = self['key_yellow'].getText()
		self.saveKeyGreen = self['key_green'].getText()
		self.saveKeyRed = self['key_red'].getText()
		self.saveStrana = self['page'].getText()
		self.Page = 0
		self.SortType = 0
		self.SortType = int(config.misc.CSFD.Default_Sort.getValue())
		self.SortTypeText = []
		self.SortTypeText.append(_('vhodnosti názvu'))
		self.SortTypeText.append(_('CSFD.cz'))
		self.SortTypeText.append(_('data vydání'))
		self.SortTypeText.append(_('abecedy'))
		self.BouquetIndex = -1
		self.BouquetMenuRot = []
		if config.misc.CSFD.Bouquet1.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet1.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet1.getValue())
		if config.misc.CSFD.Bouquet2.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet2.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet2.getValue())
		if config.misc.CSFD.Bouquet3.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet3.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet3.getValue())
		if config.misc.CSFD.Bouquet4.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet4.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet4.getValue())
		if config.misc.CSFD.Bouquet5.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet5.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet5.getValue())
		if config.misc.CSFD.Bouquet6.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet6.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet6.getValue())
		if config.misc.CSFD.Bouquet7.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet7.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet7.getValue())
		if config.misc.CSFD.Bouquet8.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet8.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet8.getValue())
		if config.misc.CSFD.Bouquet9.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet9.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet9.getValue())
		if config.misc.CSFD.Bouquet10.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet10.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet10.getValue())
		if config.misc.CSFD.Bouquet11.getValue() != 'nic' and not self.DuplBouquet(config.misc.CSFD.Bouquet11.getValue()):
			self.BouquetMenuRot.append(config.misc.CSFD.Bouquet11.getValue())
			
		self['CSFDActions'] = HelpableActionMap(self,
			'CSFDActions', {
				'CSFDOK': self.KeyOK, 
				'CSFDOKLong': self.KeyOK, 
				'CSFDExit': (self.KeyExit, 'key_exit'), 
				'CSFDExitLong': self.KeyExitLong, 
				'CSFDEsc': self.KeyEsc, 
				'CSFDEscLong': self.KeyEscLong, 
				'CSFDRight': self.pageExtraDown, 
				'CSFDRightRepeated': self.pageExtraDown, 
				'CSFDLeft': self.pageExtraUp, 
				'CSFDLeftRepeated': self.pageExtraUp, 
				'CSFDDown': self.pageDown, 
				'CSFDDownRepeated': self.pageDown, 
				'CSFDUp': self.pageUp, 
				'CSFDUpRepeated': self.pageUp, 
				'CSFDS1Red': (self.KeyRedButton, 'key_s_red'), 
				'CSFDS1RedLong': (self.keyLR, 'key_s_red_l'), 
				'CSFDS2Green': (self.KeyGreenButton, 'key_s_green'), 
				'CSFDS2GreenLong': (self.keyLG, 'key_s_green_l'), 
				'CSFDS3Yellow': (self.KeyYellowButton, 'key_s_yellow'), 
				'CSFDS3YellowLong': (self.keyLY, 'key_s_yellow_l'), 
				'CSFDS4Blue': (self.KeyBlueButton, 'key_s_blue'), 
				'CSFDS4BlueLong': (self.keyLB, 'key_s_blue_l'), 
				'CSFDMenu': (self.KeyMainMenu, 'key_menu'), 
				'CSFDSetUp': (self.KeySetUp, 'key_text'), 
				'CSFDInfo': (self.KeyshowEventInfo, 'key_info'), 
				'CSFDInfoLong': self.KeyshowEventInfo, 
				'CSFDKeyForward': (self.keyNumber3, 'key_right'), 
				'CSFDKeyBackward': (self.keyNumber1, 'key_left'), 
				'CSFDVideo': (self.KeyVideoButton, 'key_video'), 
				'CSFDbqNext': (self.KeybqNext, 'key_bq_up'), 
				'CSFDbqPrev': (self.KeybqPrev, 'key_bq_down'), 
				'0': (self.keyNumber0, 'key_0'), 
				'1': (self.keyNumber1, 'key_1'), 
#				'2': (self.KeyExtraMenu, 'key_2'), #used for sorting in comments and change types of interests 
				'3': (self.keyNumber3, 'key_3'), 
				'4': (self.keyNumber4, 'key_4'), 
				'5': (self.keyNumber5, 'key_5'), 
				'6': (self.keyNumber6, 'key_6'), 
				'7': (self.keyNumber7, 'key_7'), 
				'8': (self.keyNumber8, 'key_8'), 
				'9': (self.keyNumber9, 'key_9'), 
				'CSFDplay': (self.keyPlay, 'key_play'), 
				'CSFDpause': (self.keyPause, 'key_playpause'), 
				'CSFDplaypause': (self.keyPlayPause, 'key_playpause'), 
				'CSFDtestkey': self.keyTestMenu
				},
			-2 )
		self.CSFDTipsLoad()
		self.OldKeyHelp = self.helpList
		self.getHelpKeyDescr()
		self['menu'] = ItemList([])
		self['menu'].hide()
		self['menu'].onSelectionChanged.append(self.MovieMenuRowChanged)
		self['servicemenu'] = ItemListServiceMenu([])
		self['servicemenu'].hide()
		self.onLayoutFinish.append(self.layoutFinished)
		SKIN_Setup()
		
		LogCSFD.WriteToFile('[CSFD] CSFDClass - init - konec\n')
		return

	def layoutFinished(self):
		sss = _('Filmová databáze CSFD') + '  -  ' + _('Verze: ') + str(self.versionCSFD)
		self.setTitle(sss)
		sc = AVSwitch().getFramebufferScale()
		if self.tipsiconload is not None and self.tipsiconload_conn is not None:
			self.tipsiconload.setPara((self['tips_icon'].instance.size().width(), self['tips_icon'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		if config.misc.CSFD.TipsShow.getValue():
			self.TipsTimer.start(100, True)
		if config.misc.CSFD.RatingRotation.getValue():
			self.RatingTimer.start(100, True)
		if config.misc.CSFD.AntiFreeze.getValue():
			self.AntiFreezeTimer.start(2000, True)
		self.getCSFD()
		return

	def GetVersion(self):
		return self.versionCSFD

	def GetVersionDate(self):
		return self.versionCSFDdate

	def MovieMenuRowChanged(self):
		if self['menu'] is not None and len(self['menu'].list) > 0:
			self.selectedMenuRow = self['menu'].getCurrent()[0]
		else:
			self.selectedMenuRow = None
		return

	def getCookies(self):
		cookies = CSFDGlobalVar.getCSFDCookiesUL2()
		LogCSFD.WriteToFile('[CSFD] Cookies: ' + str(cookies) + '\n')
		return cookies

	def AntiFreezeEvent(self):
		if self.AntiFreezeTimer is not None:
			if self.AntiFreezeTimer.isActive():
				self.AntiFreezeTimer.stop()
		if self['key_red'].getText() == '' and self.ServiceMenuFlag == 0 and self.AntiFreezeTimerWorking:
			LogCSFD.WriteToFile('[CSFD] AntiFreezeEvent - zacatek\n')
			self.AntiFreezeTimerCounter += 1
			if self.AntiFreezeTimerCounter >= config.misc.CSFD.AntiFreezeLimit.getValue() / 2:
				LogCSFD.WriteToFile('[CSFD] AntiFreezeEvent - akce\n')
				self.AntiFreezeTimerCounter = 0
				self.resetLabels()
				self.Page = 0
				self.resultlist = []
				self.summaries.setText('', 10)
				self['statusbar'].show()
				self['statusbar'].setText(_('Chyba - zamrznutí pluginu'))
				self.session.open(MessageBox, _('Byla aktivována ochrana proti "zamrznutí"!\nTento stav mohl nastat z důvodu dlouhého stahování nebo došlo k nějaké chybě v programu\nZkuste zadat nebo vybrat z EPG pořad znovu'), type=MessageBox.TYPE_ERROR, timeout=20)
				self['detailslabel'].setText('')
				self['sortlabel'].setText('')
				self['key_green'].setText(_('Výběr z EPG'))
				self['key_yellow'].setText('')
				self['key_blue'].setText(_('Zadej pořad'))
				self['key_red'].setText(_('Zpět'))
				self['line'].hide()
				self['pagebg'].hide()
				self['pageb1'].hide()
				self['pageb3'].hide()
				self['paget1'].hide()
				self['paget3'].hide()
				self['page'].setText('')
				self['page'].hide()
				self['stars'].hide()
				self['starsbg'].hide()
				self['starsmt'].hide()
				self['starsmtbg'].hide()
				self['stars0'].hide()
				self['starsbg0'].hide()
				self['stars50'].hide()
				self['starsbg50'].hide()
				self['stars100'].hide()
				self['starsbg100'].hide()
				self['ratinglabel'].hide()
				self['contentlabel'].hide()
				self['detailslabel'].hide()
				self['poster'].hide()
				self['menu'].hide()
				self['servicemenu'].hide()
				self['servicemenuTop'].hide()
				self['servicemenuBackG'].hide()
			LogCSFD.WriteToFile('[CSFD] AntiFreezeEvent - konec\n')
		else:
			self.AntiFreezeTimerCounter = 0
		if config.misc.CSFD.AntiFreeze.getValue():
			self.AntiFreezeTimer.start(2000, True)
		return

	def KeyExit(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			LogCSFD.WriteToFile('[CSFD] KeyExit - zacatek\n')
			self.KeyPressLong = False
			self.KeyFlag = 'Exit'
			self.user_exit()
			LogCSFD.WriteToFile('[CSFD] KeyExit - konec\n')

	def KeyExitLong(self):
		LogCSFD.WriteToFile('[CSFD] KeyExitLong - zacatek\n')
		self.KeyPressLong = True
		self.KeyFlag = 'ExitLong'
		self.user_exit()
		LogCSFD.WriteToFile('[CSFD] KeyExitLong - konec\n')

	def KeyEsc(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			LogCSFD.WriteToFile('[CSFD] KeyEsc - zacatek\n')
			self.KeyPressLong = False
			self.KeyFlag = 'Esc'
			self.user_exit()
			LogCSFD.WriteToFile('[CSFD] KeyEsc - konec\n')

	def KeyEscLong(self):
		LogCSFD.WriteToFile('[CSFD] KeyEscLong - zacatek\n')
		self.KeyPressLong = True
		self.KeyFlag = 'EscLong'
		self.user_exit()
		LogCSFD.WriteToFile('[CSFD] KeyEscLong - konec\n')

	def user_exit(self):
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				if (self.Page is 1 or self.Page is 2) and self.resultlist is not None and len(self.resultlist) > 0:
					if self.Page == 2:
						self.showDetails()
					elif len(self.resultlist) > 0:
						if not self.Detail100Exit:
							self.showMenu()
						elif not CSFDGlobalVar.getCSFDcur() == 1:
							LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF\n')
							ref = CSFDGlobalVar.getCSFDeventID_REF()
							LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF - konec\n')
							self.session.openWithCallback(self.channelSelectionClosedExit, CSFDEPGSelection, ref, openPlugin=False)
						else:
							config.misc.CSFD.LastLoginError.setValue(int(0))
							config.misc.CSFD.LastLoginError.save()
							config.misc.CSFD.LastLanError.setValue(int(0))
							config.misc.CSFD.LastLanError.save()
							movieCSFDCache.deleteOldItemsFromCache()
							self.exit()
					elif not CSFDGlobalVar.getCSFDcur() == 1:
						LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF\n')
						ref = CSFDGlobalVar.getCSFDeventID_REF()
						LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF - konec\n')
						self.session.openWithCallback(self.channelSelectionClosedExit, CSFDEPGSelection, ref, openPlugin=False)
					else:
						config.misc.CSFD.LastLoginError.setValue(int(0))
						config.misc.CSFD.LastLoginError.save()
						config.misc.CSFD.LastLanError.setValue(int(0))
						config.misc.CSFD.LastLanError.save()
						movieCSFDCache.deleteOldItemsFromCache()
						self.exit()
				elif not CSFDGlobalVar.getCSFDcur() == 1:
					LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF\n')
					ref = CSFDGlobalVar.getCSFDeventID_REF()
					LogCSFD.WriteToFile('[CSFD] Exit - nastavuji CSFDeventID_REF - konec\n')
					self.session.openWithCallback(self.channelSelectionClosedExit, CSFDEPGSelection, ref, openPlugin=False)
				else:
					config.misc.CSFD.LastLoginError.setValue(int(0))
					config.misc.CSFD.LastLoginError.save()
					config.misc.CSFD.LastLanError.setValue(int(0))
					config.misc.CSFD.LastLanError.save()
					movieCSFDCache.deleteOldItemsFromCache()
					self.exit()
		else:
			self.exitServiceMenu()
		return

	def channelSelectionClosedExit(self, ret=None, retEPG=None, retDVBchannel=None):
		if ret is not None and ret != '':
			self.eventName = ret
			if retEPG is not None and retEPG != '':
				self.EPG = retEPG
			if retDVBchannel is not None and retDVBchannel != '':
				self.DVBchannel = retDVBchannel
			self.ResetAndRunCSFD()
		else:
			self.exit()
		return

	def CSFDEmptyTimer(self):
		pass

	def exit(self):
		try:
			if self.GalleryDownloadTimer is not None:
				if self.GalleryDownloadTimer.isActive():
					self.GalleryDownloadTimer.stop()
			if self.PosterDownloadTimer is not None:
				if self.PosterDownloadTimer.isActive():
					self.PosterDownloadTimer.stop()
			if self.NewVersionTimer is not None:
				if self.NewVersionTimer.isActive():
					self.NewVersionTimer.stop()
			if self.LoadIMDBTimer is not None:
				if self.LoadIMDBTimer.isActive():
					self.LoadIMDBTimer.stop()
			if self.GallerySlideShowTimer is not None:
				if self.GallerySlideShowTimer.isActive():
					self.GallerySlideShowTimer.stop()
			if self.PosterSlideShowTimer is not None:
				if self.PosterSlideShowTimer.isActive():
					self.PosterSlideShowTimer.stop()
			if self.PosterBasicSlideShowTimer is not None:
				if self.PosterBasicSlideShowTimer.isActive():
					self.PosterBasicSlideShowTimer.stop()
			if self.TipsTimer is not None:
				if self.TipsTimer.isActive():
					self.TipsTimer.stop()
			if self.RatingTimer is not None:
				if self.RatingTimer.isActive():
					self.RatingTimer.stop()
			if self.AntiFreezeTimer is not None:
				if self.AntiFreezeTimer.isActive():
					self.AntiFreezeTimer.stop()
			if self.DownloadTimer is not None:
				if self.DownloadTimer.isActive():
					self.DownloadTimer.stop()
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] exit - chyba - konec\n')
			LogCSFD.WriteToFile(err)

		if CSFDGlobalVar.getCSFDEnigmaVersion() >= '4':
			self.GalleryDownloadTimerConn = None
			del self.GalleryDownloadTimerConn
			self.PosterDownloadTimerConn = None
			del self.PosterDownloadTimerConn
			self.NewVersionTimerConn = None
			del self.NewVersionTimerConn
			self.LoadIMDBTimerConn = None
			del self.LoadIMDBTimerConn
			self.GallerySlideShowTimerConn = None
			del self.GallerySlideShowTimerConn
			self.PosterSlideShowTimerConn = None
			del self.PosterSlideShowTimerConn
			self.PosterBasicSlideShowTimerConn = None
			del self.PosterBasicSlideShowTimerConn
			self.TipsTimerConn = None
			del self.TipsTimerConn
			self.RatingTimerConn = None
			del self.RatingTimerConn
			self.AntiFreezeTimerConn = None
			del self.AntiFreezeTimerConn
			self.DownloadTimerConn = None
			del self.DownloadTimerConn
		self.GalleryDownloadTimer = None
		del self.GalleryDownloadTimer
		self.PosterDownloadTimer = None
		del self.PosterDownloadTimer
		self.NewVersionTimer = None
		del self.NewVersionTimer
		self.LoadIMDBTimer = None
		del self.LoadIMDBTimer
		self.GallerySlideShowTimer = None
		del self.GallerySlideShowTimer
		self.PosterSlideShowTimer = None
		del self.PosterSlideShowTimer
		self.PosterBasicSlideShowTimer = None
		del self.PosterBasicSlideShowTimer
		self.TipsTimer = None
		del self.TipsTimer
		self.RatingTimer = None
		del self.RatingTimer
		self.AntiFreezeTimer = None
		del self.AntiFreezeTimer
		self.DownloadTimer = None
		del self.DownloadTimer
		ParserCSFD.resetValues()
		ParserOstCSFD.resetValues()
		ParserVideoCSFD.resetValues()
		ParserIMDB.resetValues()
		deletetmpfiles()
		self.PosterBasicSlideList = []
		self.PosterSlideList = []
		self.VideoSlideList = []
		self.FunctionExists = []
		self.resultlist = []
		self.Tips = []
		self.SortTypeText = []
		self.container = None
		self.dataAvail_conn = None
		self.appClosed_conn = None
		if self.callbackNeeded:
			LogCSFD.WriteToFile('[CSFD] exit - CLOSE - callbackNeeded\n')
			self.close([self.callbackData, self.callbackGenre])
		else:
			LogCSFD.WriteToFile('[CSFD] exit - CLOSE\n')
			self.close()
		return

	def getServiceMenuList(self):
		ar = ' '
		internet = internet_on()
		velx = self['servicemenu'].instance.size().width()
		if CSFDGlobalVar.getBTParameters():
			from enigma import BT_SCALE, BT_KEEP_ASPECT_RATIO
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue()) + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue()) + 3
		mainServiceMenu = []
		if config.misc.CSFD.TestVersion.getValue():
			mainServiceMenu.append((ar + _('Testovací položka'), 'test'))
		if self.Page == 0:
			if not self.FindAllItems and internet:
				mainServiceMenu.append((ar + _('Vyhledat všechny položky'), 'findall'))
			if self.resultlist is not None and len(self.resultlist) > 0:
				mainServiceMenu.append((ar + _('Setřídit položky podle CSFD'), 'sortbyCSFD'))
				mainServiceMenu.append((ar + _('Setřídit položky podle vhodnosti názvu'), 'sortbyscore'))
				mainServiceMenu.append((ar + _('Setřídit položky podle data vydání'), 'sortbydate'))
				mainServiceMenu.append((ar + _('Setřídit položky podle abecedy'), 'sortbyabc'))

		mainServiceMenu.append((ar + _('Výběr pořadu z EPG akt.programu'), 'aktEPG'))
		mainServiceMenu.append((ar + _('Výběr pořadu ze všech kanálů'), 'vyberEPG'))
		mainServiceMenu.append((ar + _('Zadání pořadu'), 'zadejporad'))
		
		if CSFDGlobalVar.getIMDBexist() and internet:
			mainServiceMenu.append((ar + _('Vyhledat pořad v IMDB'), 'spustitIMDB'))
			
		if self.Page > 0 and self.stahnutoCSFD2 != '':
			if 'serie' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Řady v seriálu'), 'serie'))
			if 'epizody' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Epizody v seriálu'), 'epizody'))
			if 'souvisejici' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Související pořady'), 'souvisejici'))
			if 'podobne' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Podobné pořady'), 'podobne'))
			if 'ownrating' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zadat/změnit hodnocení'), 'ownrating'))
			if 'komentare' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit komentáře'), 'komentare'))
			if 'diskuze' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit diskuzi'), 'diskuze'))
			if 'zajimavosti' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit zajímavosti'), 'zajimavosti'))
			if 'oceneni' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit ocenění'), 'oceneni'))
			if 'galerie' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit galerii'), 'galerie'))
			if 'postery' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit postery'), 'postery'))
			if 'video' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit videa'), 'video'))
			if 'premiery' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit premiéry'), 'premiery'))
			if 'hodnoceni' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit hodnocení uživatelů'), 'hodnoceni'))
			if 'fanousci' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit fanoušky pořadu'), 'fanousci'))
			if 'ext.recenze' not in self.FunctionExists:
				mainServiceMenu.append((ar + _('Zobrazit ext.recenze'), 'ext.recenze'))
			if self.Page == 2 and self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				mainServiceMenu.append((ar + _('Uložit video'), 'ulozvideo'))
				mainServiceMenu.append((ar + _('Spustit video ukázku'), 'spustitvideo'))
		mainServiceMenu.append((ar + _('Nastavení'), 'nastaveni'))
		if csfdAndroidClient.is_logged():
			mainServiceMenu.append((ar + _('Odhlásit se z ČSFD'), 'logout'))
		mainServiceMenu.append((ar + _('Stáhnout novou verzi pluginu'), 'novaverze'))
		mainServiceMenu.append((ar + _('Změna skinu'), 'skin'))
		mainServiceMenu.append((ar + _('Historie změn v pluginu'), 'historie'))
		mainServiceMenu.append((ar + _('O pluginu'), 'about'))
		mainServiceMenu.append((ar + _('Nápověda'), 'help'))
		mainServiceMenu.append((ar + _('Zpět'), 'zpet'))
		mainServiceMenuNew = []
		for x in mainServiceMenu:
			png_type = None
			pol0 = x[0]
			pol1 = x[1]
			if x[1] == config.misc.CSFD.HotKey4.getValue():
				png_type = loadPixmapCSFD('key_4.png')
			if x[1] == config.misc.CSFD.HotKey5.getValue():
				png_type = loadPixmapCSFD('key_5.png')
			if x[1] == config.misc.CSFD.HotKey6.getValue():
				png_type = loadPixmapCSFD('key_6.png')
			if x[1] == config.misc.CSFD.HotKey7.getValue():
				png_type = loadPixmapCSFD('key_7.png')
			if x[1] == config.misc.CSFD.HotKey8.getValue():
				png_type = loadPixmapCSFD('key_8.png')
			if x[1] == config.misc.CSFD.HotKey9.getValue():
				png_type = loadPixmapCSFD('key_9.png')
			if x[1] == config.misc.CSFD.HotKey0.getValue():
				png_type = loadPixmapCSFD('key_0.png')
			if x[1] == config.misc.CSFD.HotKeyLR.getValue():
				png_type = loadPixmapCSFD('key_s_red_l.png')
			if x[1] == config.misc.CSFD.HotKeyLG.getValue():
				png_type = loadPixmapCSFD('key_s_green_l.png')
			if x[1] == config.misc.CSFD.HotKeyLB.getValue():
				png_type = loadPixmapCSFD('key_s_blue_l.png')
			if x[1] == config.misc.CSFD.HotKeyLY.getValue():
				png_type = loadPixmapCSFD('key_s_yellow_l.png')
			if x[1] == 'video':
				png_type = loadPixmapCSFD('key_video.png')
			if x[1] == 'nastaveni':
				png_type = loadPixmapCSFD('key_text.png')
			if x[1] == 'help':
				png_type = loadPixmapCSFD('key_help.png')
			if x[1] == 'zpet':
				png_type = loadPixmapCSFD('key_exit.png')
			res = [
			 (
			  pol0, pol1)]
			if png_type is None:
				res.append(MultiContentEntryText(pos=(0, 0), size=(45, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text='			 '))
				res.append(MultiContentEntryText(pos=(45, 0), size=(velx - 45, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text=pol0))
			else:
				res.append(MultiContentEntryText(pos=(0, 0), size=(45, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text='			 '))
				if CSFDGlobalVar.getBTParameters():
					res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(35, h), backcolor=0, png=png_type, flags=BT_SCALE | BT_KEEP_ASPECT_RATIO))
				else:
					res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(35, h), backcolor=0, png=png_type))
				res.append(MultiContentEntryText(pos=(45, 0), size=(velx - 45, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text=pol0))
			mainServiceMenuNew.append(res)

		mainServiceMenu = mainServiceMenuNew
		return mainServiceMenu

	def getSortCommentMenuList(self):
		ar = ' '
		velx = self['servicemenu'].instance.size().width()
		mainServiceMenu = []
		mainServiceMenu.append((ar + _('podle počtu bodů uživatele'), 'sortCommentPoints'))
		mainServiceMenu.append((ar + _('od nejnovějších po nejstarší'), 'sortCommentDate'))
		mainServiceMenu.append((ar + _('podle hodnocení'), 'sortCommentRating'))
		mainServiceMenu.append((ar + _('zpět'), 'zpet'))
		mainServiceMenuNew = []
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue()) + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue()) + 3
		for x in mainServiceMenu:
			pol0 = x[0]
			pol1 = x[1]
			res = [(pol0, pol1)]
			res.append(MultiContentEntryText(pos=(0, 0), size=(velx, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text=pol0))
			mainServiceMenuNew.append(res)

		mainServiceMenu = mainServiceMenuNew
		return mainServiceMenu

	def getInterestTypesMenuList(self):
		ar = ' '
		velx = self['servicemenu'].instance.size().width()
		mainServiceMenu = []
		results = ParserCSFD.parserInterestTypesAndNumbers()
		if results is not None:
			for x in results:
				mainServiceMenu.append((ar + x[1] + ' ' + x[2], 'typeInterest', x[0], x[1], x[2]))

		mainServiceMenu.append((ar + _('Zpět'), 'zpet', None, None, None))
		mainServiceMenuNew = []
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue()) + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue()) + 3
		for x in mainServiceMenu:
			res = [
			 (
			  x[0], x[1], x[2], x[3], x[4])]
			res.append(MultiContentEntryText(pos=(0, 0), size=(velx, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, backcolor=0, text=x[0]))
			mainServiceMenuNew.append(res)

		mainServiceMenu = mainServiceMenuNew
		return mainServiceMenu

	def RunKey(self, akce, extraParams=None):
		LogCSFD.WriteToFile('[CSFD] RunKey - zacatek\n')
		if self.PosterSlideShowTimer.isActive():
			self.PosterSlideShowTimer.stop()
		if self.GallerySlideShowTimer.isActive():
			self.GallerySlideShowTimer.stop()
		if akce == 'aktEPG':
			LogCSFD.WriteToFile('[CSFD] RunKey - aktEPG zacatek\n')
			self.openAktChannelSelection()
			LogCSFD.WriteToFile('[CSFD] RunKey - aktEPG konec\n')
		elif akce == 'vyberEPG':
			LogCSFD.WriteToFile('[CSFD] RunKey - EPG zacatek\n')
			self.openChannelSelection()
			LogCSFD.WriteToFile('[CSFD] RunKey - EPG konec\n')
		elif akce == 'test':
			LogCSFD.WriteToFile('[CSFD] RunKey - Test - zacatek\n')
			self.KeyTesting()
			LogCSFD.WriteToFile('[CSFD] RunKey - Test - konec\n')
		elif akce == 'findall':
			LogCSFD.WriteToFile('[CSFD] RunKey - Vyhledat vsechny polozky - zacatek\n')
			self.KeyFindAll()
			LogCSFD.WriteToFile('[CSFD] RunKey - Vyhledat vsechny polozky - konec\n')
		elif akce == 'sortbyscore':
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle vhodnosti - zacatek\n')
			self.KeySortItemInMenu(0)
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle vhodnosti - konec\n')
		elif akce == 'sortbyCSFD':
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle CSFD - zacatek\n')
			self.KeySortItemInMenu(1)
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle CSFD - konec\n')
		elif akce == 'sortbydate':
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle data vydani - zacatek\n')
			self.KeySortItemInMenu(2)
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle data vydani - konec\n')
		elif akce == 'sortbyabc':
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle abecedy - zacatek\n')
			self.KeySortItemInMenu(3)
			LogCSFD.WriteToFile('[CSFD] RunKey - Setridit podle abecedy - konec\n')
		elif akce == 'zadejporad':
			LogCSFD.WriteToFile('[CSFD] RunKey - ZadaniPoradu - zacatek\n')
			self.KeyText()
			LogCSFD.WriteToFile('[CSFD] RunKey - ZadaniPoradu - konec\n')
		elif akce == 'spustitIMDB':
			LogCSFD.WriteToFile('[CSFD] RunKey - SpustitIMDB - zacatek\n')
			if CSFDGlobalVar.getIMDBexist():
				self.KeySpustitIMDB()
			LogCSFD.WriteToFile('[CSFD] RunKey - SpustitIMDB - konec\n')
		elif akce == 'komentare':
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyKomentare()
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - konec\n')
		elif akce == 'ext.recenze':
			LogCSFD.WriteToFile('[CSFD] RunKey - Ext.recenze - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyExtRecenze()
			LogCSFD.WriteToFile('[CSFD] RunKey - Ext.recenze - konec\n')
		elif akce == 'ownrating':
			LogCSFD.WriteToFile('[CSFD] RunKey - OwnRating - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyOwnRating()
			LogCSFD.WriteToFile('[CSFD] RunKey - OwnRating - konec\n')
		elif akce == 'diskuze':
			LogCSFD.WriteToFile('[CSFD] RunKey - Diskuze - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyDiskuze()
			LogCSFD.WriteToFile('[CSFD] RunKey - Diskuze - konec\n')
		elif akce == 'zajimavosti':
			LogCSFD.WriteToFile('[CSFD] RunKey - Zajimavosti - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyZajimavosti()
			LogCSFD.WriteToFile('[CSFD] RunKey - Zajimavosti - konec\n')
		elif akce == 'oceneni':
			LogCSFD.WriteToFile('[CSFD] RunKey - Oceneni - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyOceneni()
			LogCSFD.WriteToFile('[CSFD] RunKey - Oceneni - konec\n')
		elif akce == 'souvisejici':
			LogCSFD.WriteToFile('[CSFD] RunKey - Souvisejici - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeySouvisejici()
			LogCSFD.WriteToFile('[CSFD] RunKey - Souvisejici - konec\n')
		elif akce == 'podobne':
			LogCSFD.WriteToFile('[CSFD] RunKey - Podobne - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyPodobne()
			LogCSFD.WriteToFile('[CSFD] RunKey - Podobne - konec\n')
		elif akce == 'serie':
			LogCSFD.WriteToFile('[CSFD] RunKey - Serie - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeySerie()
			LogCSFD.WriteToFile('[CSFD] RunKey - Serie - konec\n')
		elif akce == 'epizody':
			LogCSFD.WriteToFile('[CSFD] RunKey - Epizody - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyEpizody()
			LogCSFD.WriteToFile('[CSFD] RunKey - Epizody - konec\n')
		elif akce == 'hodnoceni':
			LogCSFD.WriteToFile('[CSFD] RunKey - Hodnoceni - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyHodnoceni()
			LogCSFD.WriteToFile('[CSFD] RunKey - Hodnoceni - konec\n')
		elif akce == 'premiery':
			LogCSFD.WriteToFile('[CSFD] RunKey - Premiery - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyPremiery()
			LogCSFD.WriteToFile('[CSFD] RunKey - Premiery - konec\n')
		elif akce == 'galerie':
			LogCSFD.WriteToFile('[CSFD] RunKey - Galerie - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyGalerie()
			LogCSFD.WriteToFile('[CSFD] RunKey - Galerie - konec\n')
		elif akce == 'postery':
			LogCSFD.WriteToFile('[CSFD] RunKey - Postery - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyPostery()
			LogCSFD.WriteToFile('[CSFD] RunKey - Postery - konec\n')
		elif akce == 'video':
			LogCSFD.WriteToFile('[CSFD] RunKey - Video - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyVideo()
			LogCSFD.WriteToFile('[CSFD] RunKey - Video - konec\n')
		elif akce == 'ulozvideo':
			LogCSFD.WriteToFile('[CSFD] RunKey - UlozVideo - zacatek\n')
			if self.Page == 2 and self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				self.KeyUlozVideo()
			LogCSFD.WriteToFile('[CSFD] RunKey - UlozVideo - konec\n')
		elif akce == 'spustitvideo':
			LogCSFD.WriteToFile('[CSFD] RunKey - SpustitVideo - zacatek\n')
			if self.Page == 2 and self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				self.KeySpustitVideo()
			LogCSFD.WriteToFile('[CSFD] RunKey - SpustitVideo - konec\n')
		elif akce == 'fanousci':
			LogCSFD.WriteToFile('[CSFD] RunKey - Fanousci - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				self.KeyFanousci()
			LogCSFD.WriteToFile('[CSFD] RunKey - Fanousci - konec\n')
		elif akce == 'nastaveni':
			LogCSFD.WriteToFile('[CSFD] RunKey - Nastaveni - zacatek\n')
			self.showSetupScreen()
			LogCSFD.WriteToFile('[CSFD] RunKey - Nastaveni - konec\n')
		elif akce == 'about':
			LogCSFD.WriteToFile('[CSFD] RunKey - O pluginu - zacatek\n')
			self.showScreenAbout()
			LogCSFD.WriteToFile('[CSFD] RunKey - O pluginu - konec\n')
		elif akce == 'help':
			LogCSFD.WriteToFile('[CSFD] RunKey - Napoveda - zacatek\n')
			self.KeyHelp()
			LogCSFD.WriteToFile('[CSFD] RunKey - Napoveda - konec\n')
		elif akce == 'skin':
			LogCSFD.WriteToFile('[CSFD] RunKey - Zmena skinu - zacatek\n')
			self.showScreenSkin()
			LogCSFD.WriteToFile('[CSFD] RunKey - Zmena skinu - konec\n')
		elif akce == 'historie':
			LogCSFD.WriteToFile('[CSFD] RunKey - Zmeny v pluginu - zacatek\n')
			self.showScreenHistory()
			LogCSFD.WriteToFile('[CSFD] RunKey - Zmeny v pluginu - konec\n')
		elif akce == 'logout':
			LogCSFD.WriteToFile('[CSFD] RunKey - Odhlasit se - zacatek\n')
			self.showLogout()
			LogCSFD.WriteToFile('[CSFD] RunKey - Odhlasit se - konec\n')
		elif akce == 'novaverze':
			LogCSFD.WriteToFile('[CSFD] RunKey - Nova verze - zacatek\n')
			self.showNewVersion()
			LogCSFD.WriteToFile('[CSFD] RunKey - Nova verze - konec\n')
		elif akce == 'sortCommentPoints':
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle bodu - zacatek\n')
			self.linkComment = ''
			self.KeyKomentare()
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle bodu - konec\n')
		elif akce == 'sortCommentDate':
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle data - zacatek\n')
			self.linkComment = 'podle-datetime/'
			self.KeyKomentare()
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle data - konec\n')
		elif akce == 'sortCommentRating':
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle hodnoceni - zacatek\n')
			self.linkComment = 'podle-rating/'
			self.KeyKomentare()
			LogCSFD.WriteToFile('[CSFD] RunKey - Komentare - Trideni podle hodnoceni - konec\n')
		elif akce == 'typeInterest':
			LogCSFD.WriteToFile('[CSFD] RunKey - Zajimavosti - Vyber typu zajimavosti - zacatek\n')
			if self.Page > 0 and self.stahnutoCSFD2 != '' and extraParams is not None:
				sss = extraParams[2].split('?')
				if len(sss) > 1:
					self.linkExtra = '?' + str(sss[1])
				else:
					self.linkExtra = ''
				self.KeyZajimavosti()
			LogCSFD.WriteToFile('[CSFD] RunKey - Zajimavosti - Vyber typu zajimavosti - konec\n')
		LogCSFD.WriteToFile('[CSFD] RunKey - konec\n')
		return

	def KeyOK(self):
		self.KeyPressLong = False
		self.KeyFlag = 'OK'
		extraAkceParams = None
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '' and self['key_yellow'].getText() != '':
				self.showDetails()
		else:
			LogCSFD.WriteToFile('[CSFD] KeyOK - zacatek\n')
			akce = self['servicemenu'].getCurrent()[0][1].strip()
			extraAkceParams = self['servicemenu'].getCurrent()[0]
			if akce == '' or akce == 'zpet':
				self.exitServiceMenu()
				LogCSFD.WriteToFile('[CSFD] KeyOK - konec - akce konec\n')
				return
			if akce not in ['aktEPG', 'vyberEPG', 'zadejporad', 'nastaveni', 'about', 'help', 'historie', 'skin', 'novaverze']:
#			if not (akce == 'aktEPG' or akce == 'vyberEPG' or akce == 'zadejporad' or akce == 'nastaveni' or akce == 'about' or akce == 'help' or akce == 'historie' or akce == 'skin' or akce == 'novaverze'):
				self.exitServiceMenu()
			self.RunKey(akce, extraAkceParams)
			LogCSFD.WriteToFile('[CSFD] KeyOK - konec\n')
		return

	def KeyMainMenu(self):
		self['servicemenuTop'].setText('M E N U')
		self['servicemenuTop'].hide()
		self.KeyContextMenu('0')

	def KeyExtraMenu(self):
		self.KeyPressLong = False
		self.KeyFlag = '2'
		if self.querySpecAkce == 'UserComments' and self.Page == 2:
			self['servicemenuTop'].setText(_('Komentáře uživatelů třídit:'))
			self['servicemenuTop'].hide()
			self.KeyContextMenu('1')
		elif self.querySpecAkce == 'UserInteresting' and self.Page == 2:
			self['servicemenuTop'].setText(_('Vyberte typ zajímavostí:'))
			self['servicemenuTop'].hide()
			self.KeyContextMenu('2')

	def KeySortItemInMenu(self, sorttyp=0):
		self.KeyPressLong = False
		self.KeyFlag = 'SortMenu'
		if self.Page == 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeySortItemInMenu - zacatek\n')
					self.SortTypeChange(change_s=True, back=True, directTypeSort=sorttyp)
					self.Detail100Exit = False
					self.showMenu()
					LogCSFD.WriteToFile('[CSFD] KeySortItemInMenu - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeySortItemInMenu - zacatek\n')
				self.exitServiceMenu()
				self.SortTypeChange(change_s=True, back=True, directTypeSort=sorttyp)
				self.Detail100Exit = False
				self.showMenu()
				LogCSFD.WriteToFile('[CSFD] KeySortItemInMenu - konec\n')

	def KeyContextMenu(self, typ='0'):
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				self.saveKeyRed = self['key_red'].getText()
				self['key_red'].setText('')
				self.ServiceMenuFlag = 1
				self.saveKeyBlue = self['key_blue'].getText()
				self.saveKeyYellow = self['key_yellow'].getText()
				self.saveKeyGreen = self['key_green'].getText()
				self.saveStrana = self['page'].getText()
				self['pagebg'].hide()
				self['pageb1'].hide()
				self['pageb3'].hide()
				self['paget1'].hide()
				self['paget3'].hide()
				self['page'].setText('')
				self['page'].hide()
				self['key_blue'].setText('')
				self['key_yellow'].setText('')
				self['key_green'].setText('')
				self['tips_label'].hide()
				self['tips_icon'].hide()
				self['tips_detail'].hide()
				self['servicemenuBackG'].show()
				self['servicemenuTop'].show()
				if typ == '0':
					self['servicemenu'].setList(self.getServiceMenuList())
				elif typ == '1':
					self['servicemenu'].setList(self.getSortCommentMenuList())
				elif typ == '2':
					self['servicemenu'].setList(self.getInterestTypesMenuList())
				else:
					self['servicemenu'].setList(self.getServiceMenuList())
				self['servicemenu'].moveToIndex(0)
				self['servicemenu'].show()
				self.summaries.setText(self['servicemenu'].getCurrent()[0][0], 10)
		else:
			self.exitServiceMenu()

	def exitServiceMenu(self):
		self.ServiceMenuFlag = 0
		self['key_blue'].setText(self.saveKeyBlue)
		self['key_yellow'].setText(self.saveKeyYellow)
		self['key_green'].setText(self.saveKeyGreen)
		self['key_red'].setText(self.saveKeyRed)
		self['page'].setText(self.saveStrana)
		if self.saveStrana != '':
			self['pagebg'].show()
			self['pageb1'].show()
			self['pageb3'].show()
			self['paget1'].show()
			self['paget3'].show()
			self['page'].show()
		self['servicemenu'].hide()
		self['servicemenuTop'].hide()
		self['servicemenuBackG'].hide()
		if self.Page == 0:
			if self.selectedMenuRow is not None:
				self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
			else:
				self.summaries.setText(' ', 10)
		else:
			try:
				if self['titellabel'] is not None and self.ratingstars is not None:
					ss12 = self['titellabel'].getText()
					self.summaries.setText(ss12, GetItemColourRateN(self.ratingstars))
				else:
					self.summaries.setText(' ', 10)
			except:
				self.summaries.setText(' ', 10)
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] exitServiceMenu - chyba\n')
				LogCSFD.WriteToFile(err)

		return

	def showSetupScreen(self):
		LogCSFD.WriteToFile('[CSFD] ScreenSetupShow\n')
		self.AntiFreezeTimerWorking = False
		self.workingConfig = None
		self.session.openWithCallback(self.onSetupScreenClose, CSFDSetup, self.TestLoginToCSFD, self.ResetAllCSFDParams)
		return

	def onSetupScreenClose(self):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] ScreenSetupClose\n')

	def showScreenAbout(self):
		LogCSFD.WriteToFile('[CSFD] ScreenAboutShow\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.closeScreenAbout, CSFDAbout, self.versionCSFD, self.versionCSFDdate)

	def closeScreenAbout(self):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] ScreenAboutClose\n')

	def showLogout(self):
		LogCSFD.WriteToFile('[CSFD] ScreenLogoutShow\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.closeLogout, MessageBox, (_('Opravdu se odhlásit z ČSFD?') + '\n' + _('Opětovné přihlášení budete muset povolit v nastaveních.')+ '\n'), MessageBox.TYPE_YESNO)

	def closeLogout(self, answer):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] ScreenLogoutClose - zacatek\n')
		if answer == True:
			csfdAndroidClient.logout()
			config.misc.CSFD.TokenCSFD.setValue('')
			config.misc.CSFD.TokenCSFD.save()
			config.misc.CSFD.LoginToCSFD.setValue(False)
			config.misc.CSFD.LoginToCSFD.save()

		LogCSFD.WriteToFile('[CSFD] ScreenLogoutClose - konec\n')
		

	def showScreenHelp(self):
		LogCSFD.WriteToFile('[CSFD] ScreenHelpShow\n')
		self.AntiFreezeTimerWorking = False
		inst = CSFDHelpableScreen()
		inst.setAttrHelp(self.session, self.getHelpKeyDescr)
		inst.showHelp()
		self.AntiFreezeTimerWorking = True

	def showNewVersion(self):
		LogCSFD.WriteToFile('[CSFD] showNewVersion - zacatek\n')
		self.automaticUpdate = False
		self.CheckForUpdate()
		LogCSFD.WriteToFile('[CSFD] showNewVersion - konec\n')

	def showScreenSkin(self):
		LogCSFD.WriteToFile('[CSFD] ScreenSkinShow\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.closeScreenSkin, CSFDSkinSelect)

	def closeScreenSkin(self, zmenaSkinu=0):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] ScreenSkinClose\n')
		if zmenaSkinu == 1:
			LogCSFD.WriteToFile('[CSFD] ScreenSkinClose - změna skinu - ANO\n')
			self.session.openWithCallback(self.restartGUI, MessageBox, _('Změna skinu se projeví po restartu GUI.') + '\n' + _('Chcete nyní provést restart GUI?'), MessageBox.TYPE_YESNO)
		elif zmenaSkinu == 2:
			LogCSFD.WriteToFile('[CSFD] ScreenSkinClose - reset skinu - ANO\n')
			self.session.openWithCallback(self.restartGUI, MessageBox, _('Reset skinu se projeví po restartu GUI.') + '\n' + _('Chcete nyní provést restart GUI?'), MessageBox.TYPE_YESNO)

	def showScreenHistory(self):
		LogCSFD.WriteToFile('[CSFD] ScreenHistoryShow\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.closeScreenHistory, CSFDHistory)

	def closeScreenHistory(self):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] ScreenHistoryClose\n')

	def UlozitVideo(self):
		LogCSFD.WriteToFile('[CSFD] UlozitVideo - zacatek\n')
		if os_path.exists(config.misc.CSFD.DirectoryVideoDownload.getValue()):
			self.videoklipurl = self.VideoSlideList[self.VideoActIdx][4]
			self.videotitulkyurl = self.VideoSlideList[self.VideoActIdx][5]
			LogCSFD.WriteToFile('[CSFD] UlozitVideo - video file: ' + self.videoklipurl + '\n')
			LogCSFD.WriteToFile('[CSFD] UlozitVideo - video titulky: ' + self.videotitulkyurl + '\n')
			if self.videoklipurl != '':
				LogCSFD.WriteToFile('[CSFD] UlozitVideo - spouteni downloadu\n')
				self.UlozitVideoDownload(self.ActName, self.videoklipurl, self.videotitulkyurl)
		else:
			self.session.open(MessageBox, _('Adresář pro stažení videa není dostupný: %s') % config.misc.CSFD.DirectoryVideoDownload.getValue(), type=MessageBox.TYPE_ERROR, timeout=10)
		LogCSFD.WriteToFile('[CSFD] UlozitVideo - konec\n')

	def UlozitVideoDownload(self, nazev='', videourl='', titulkyurl=''):
		LogCSFD.WriteToFile('[CSFD] UlozitVideoDownload - zacatek\n')
		ss = videourl.rsplit('/', 2)
		nazevvideo = strUni(char2Diacritic(nazev)).replace(' ', '_').replace('.', '_').replace(':', '_').replace('?', '_').replace('/', '_').replace('\\', '_') + '_' + ss[1] + '_' + ss[2]
		localfilevideo = config.misc.CSFD.DirectoryVideoDownload.getValue() + nazevvideo
		LogCSFD.WriteToFile('[CSFD] UlozitVideoDownload - stahuji z url ' + videourl + ' do ' + localfilevideo + '\n')
		self.session.open(MessageBox, _('Video bude staženo do : %s') % localfilevideo, type=MessageBox.TYPE_INFO, timeout=10)
		
		requestFileCSFD(videourl, localfilevideo)
		self.closeUlozitVideo('')
		
		if titulkyurl != '':
			ss = titulkyurl.rsplit('.', 1)
			ss1 = nazevvideo.rsplit('.', 1)
			nazevtitulky = ss1[0] + '.' + ss[1]
			localfiletitulky = config.misc.CSFD.DirectoryVideoDownload.getValue() + nazevtitulky
			LogCSFD.WriteToFile('[CSFD] UlozitVideoDownload - stahuji z url ' + titulkyurl + ' do ' + localfiletitulky + '\n')
			requestFileCSFD(titulkyurl, localfiletitulky )
			self.closeUlozitTitulky('')
			
		LogCSFD.WriteToFile('[CSFD] UlozitVideoDownload - konec\n')

	def closeUlozitVideo(self, string):
		LogCSFD.WriteToFile('[CSFD] closeUlozitVideo - zacatek\n')
		self.session.open(MessageBox, _('Video bylo staženo'), type=MessageBox.TYPE_INFO, timeout=5)
		LogCSFD.WriteToFile('[CSFD] closeUlozitVideo - konec\n')

	def closeUlozitTitulky(self, string):
		LogCSFD.WriteToFile('[CSFD] closeUlozitTitulky - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] closeUlozitTitulky - konec\n')

	def CSFDopenVideoDownload(self):
		LogCSFD.WriteToFile('[CSFD] openVideoDownload - zacatek\n')
		self.UlozitVideoDownload(self.ActName, self.videoklipurl, self.videotitulkyurl)
		LogCSFD.WriteToFile('[CSFD] openVideoDownload - konec\n')

	def fetchFailedDwnlVideo(self, string, url, localfile):
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani videa\n')
		err = string.getErrorMessage()
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani videa: ' + Uni8(err) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani videa - url: ' + Uni8(url) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani videa - localfile: ' + Uni8(localfile) + '\n')
		self.session.open(MessageBox, _('Chyba při stahování videa: %s') % err, type=MessageBox.TYPE_ERROR, timeout=10)

	def fetchFailedDwnlTitulky(self, string, url, localfile):
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani titulku\n')
		err = string.getErrorMessage()
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani titulku: ' + Uni8(err) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani titulku - url: ' + Uni8(url) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani titulku - localfile: ' + Uni8(localfile) + '\n')
		self.session.open(MessageBox, _('Chyba při stahování titulků: %s') % err, type=MessageBox.TYPE_ERROR, timeout=10)

	def resetLabels(self):
		self['detailslabel'].setText('')
		self['ratinglabel'].setText('')
		self['titellabel'].setText('')
		self['sortlabel'].setText('')
		self['contentlabel'].setText('')
		self['extralabel'].setText('')
		self['photolabel'].hide()
		self['playbutton'].hide()
		self['line'].hide()
		self['pagebg'].hide()
		self['pageb1'].hide()
		self['pageb3'].hide()
		self['paget1'].hide()
		self['paget3'].hide()
		self['page'].setText('')
		self['page'].hide()
		self.ratingcount = 0
		self.ratingstars = -1
		self.ratingstarsIMDB = -1
		self.ratingstarsMetacritic = -1
		self.ratingtext = ''
		self.ratingtextIMDB = ''
		self.ratingtextMetacritic = ''
		self.PageSpec = 1
		self.PosterBasicActIdx = 0
		self.querySpecAkce = 'UserComments'
		self.IMDBpath = ''
		self.CSFDratingUsers = ''

	def doNothing(self):
		pass

	def KeyRedButton(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			self.KeyFlag = 'Red'
			if self['key_red'].getText() != '':
				self.user_exit()

	def KeyGreenButton(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			self.KeyFlag = 'Green'
			if self['key_green'].getText() != '':
				if self.Page == 0:
					self.openAktChannelSelection()
				else:
					self.Detail100Exit = False
					self.showMenu()

	def KeyBlueButton(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			self.KeyFlag = 'Blue'
			self.BlueButton()

	def BlueButton(self):
		if self['key_blue'].getText() != '':
			if self.Page > 0 and self.querySpecAkce == 'Nothing' and self.stahnutoCSFD2 != '':
				self.KeyKomentare()
			else:
				self.showExtras()

	def KeyYellowButton(self):
		if self.KeyPressLong:
			self.KeyPressLong = False
		else:
			self.KeyFlag = 'Yellow'
			if self['key_yellow'].getText() != '':
				self.showDetails()

	def KeyshowEventInfo(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Info'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '' and self['key_yellow'].getText() != '':
				self.showDetails()

	def pageExtraUp(self):
		self.KeyPressLong = False
		self.KeyFlag = 'ExtraUp'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				if self.Page == 0:
					self['menu'].pageUp()
					if self.selectedMenuRow is not None:
						self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
					else:
						self.summaries.setText(' ', 10)
				if self.Page == 1:
					self['contentlabel'].pageUp()
					self['detailslabel'].pageUp()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx += -1
							if self.GalleryActIdx < 0:
								self.GalleryActIdx = 0
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx += -1
							if self.PosterActIdx < 0:
								self.PosterActIdx = 0
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx += -1
							if self.VideoActIdx < 0:
								self.VideoActIdx = 0
							self.CSFDshowSpec()
					else:
						self['extralabel'].pageUp()
		else:
			self['servicemenu'].pageUp()
			self.summaries.setText(self['servicemenu'].getCurrent()[0][0], 10)
		return

	def pageExtraDown(self):
		self.KeyPressLong = False
		self.KeyFlag = 'ExtraDown'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				if self.Page == 0:
					self['menu'].pageDown()
					if self.selectedMenuRow is not None:
						self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
					else:
						self.summaries.setText(' ', 10)
				if self.Page == 1:
					self['contentlabel'].pageDown()
					self['detailslabel'].pageDown()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx += 1
							if self.GalleryActIdx >= self.GalleryCountPix:
								self.GalleryActIdx = self.GalleryCountPix - 1
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx += 1
							if self.PosterActIdx >= self.PosterCountPix:
								self.PosterActIdx = self.PosterCountPix - 1
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx += 1
							if self.VideoActIdx >= self.VideoCountPix:
								self.VideoActIdx = self.VideoCountPix - 1
							self.CSFDshowSpec()
					else:
						self['extralabel'].pageDown()
		else:
			self['servicemenu'].pageDown()
			self.summaries.setText(self['servicemenu'].getCurrent()[0][0], 10)
		return

	def pageUp(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Up'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				if self.Page == 0:
					self['menu'].up()
					if self.selectedMenuRow is not None:
						self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
					else:
						self.summaries.setText(' ', 10)
				if self.Page == 1:
					self['contentlabel'].Up()
					self['detailslabel'].Up()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx = self.GalleryCountPix - 1
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx = self.PosterCountPix - 1
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx = self.VideoCountPix - 1
							self.CSFDshowSpec()
					else:
						self['extralabel'].Up()
		else:
			self['servicemenu'].up()
			self.summaries.setText(self['servicemenu'].getCurrent()[0][0], 10)
		return

	def pageDown(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Down'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				if self.Page == 0:
					self['menu'].down()
					if self.selectedMenuRow is not None:
						self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
					else:
						self.summaries.setText(' ', 10)
				if self.Page == 1:
					self['contentlabel'].Down()
					self['detailslabel'].Down()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx = 0
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx = 0
							self.CSFDshowSpec()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx = 0
							self.CSFDshowSpec()
					else:
						self['extralabel'].Down()
		else:
			self['servicemenu'].down()
			self.summaries.setText(self['servicemenu'].getCurrent()[0][0], 10)
		return

	def KeyText(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Text'
		LogCSFD.WriteToFile('[CSFD] KeyText - zacatek\n')
		if config.misc.CSFD.SaveSearch.getValue() == True:
			config.misc.CSFD.InputSearch.setValue(self.eventNameLocal)
		else:
			config.misc.CSFD.InputSearch.setValue('')
		config.misc.CSFD.InputSearch.save()
		CSFDGlobalVar.setCSFDcur(1)
		CSFDGlobalVar.setCSFDeventID_EPG(0)
		CSFDGlobalVar.setCSFDeventID_REF('')
		self.AntiFreezeTimerWorking = False
		if config.misc.CSFD.Input_Type.getValue() == '0':
			self.session.openWithCallback(self.InputKeyCallback, CSFDVirtualKeyBoard, text=config.misc.CSFD.InputSearch.getValue(), title=_('Zadej název hledaného pořadu:'))
		else:
			self.session.openWithCallback(self.InputKeyCallback, CSFDInputText)
		LogCSFD.WriteToFile('[CSFD] KeyText - konec\n')

	def KeyFindAll(self):
		self.KeyPressLong = False
		self.KeyFlag = 'FindAll'
		if self.Page == 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeyFindAll - zacatek\n')
					self.FindAllItems = True
					if self.eventMovieNameYears != '':
						self.eventName = self.eventMovieNameYears
					CSFDGlobalVar.setCSFDcur(1)
					self.ResetAndRunCSFD()
					LogCSFD.WriteToFile('[CSFD] KeyFindAll - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeyFindAll - zacatek\n')
				self.exitServiceMenu()
				self.FindAllItems = True
				if self.eventMovieNameYears != '':
					self.eventName = self.eventMovieNameYears
				CSFDGlobalVar.setCSFDcur(1)
				self.ResetAndRunCSFD()
				LogCSFD.WriteToFile('[CSFD] KeyFindAll - konec\n')

	def KeyOwnRating(self):
		self.KeyPressLong = False
		self.KeyFlag = 'OwnRating'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeyOwnRating - zacatek\n')
					self.CSFDChangeOwnRating()
					LogCSFD.WriteToFile('[CSFD] KeyOwnRating - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeyOwnRating - zacatek\n')
				self.exitServiceMenu()
				self.CSFDChangeOwnRating()
				LogCSFD.WriteToFile('[CSFD] KeyOwnRating - konec\n')

	def KeyKomentare(self):
		LogCSFD.WriteToFile('[CSFD] KeyKomentare - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Komentáře'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserComments'
		self.BlueButton()
		self.KeyFlag = 'Komentare'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyKomentare - konec\n')

	def KeyExtRecenze(self):
		LogCSFD.WriteToFile('[CSFD] KeyExtRecenze - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Ext.recenze'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserExtReviews'
		self.BlueButton()
		self.KeyFlag = 'ExtRecenze'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyExtRecenze - konec\n')

	def KeyDiskuze(self):
		LogCSFD.WriteToFile('[CSFD] KeyDiskuze - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Diskuze'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserDiscussion'
		self.BlueButton()
		self.KeyFlag = 'Diskuze'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyDiskuze - konec\n')

	def KeyZajimavosti(self):
		LogCSFD.WriteToFile('[CSFD] KeyZajimavosti - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Zajímavosti'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserInteresting'
		self.BlueButton()
		self.KeyFlag = 'Zajimavosti'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyZajimavosti - konec\n')

	def KeyOceneni(self):
		LogCSFD.WriteToFile('[CSFD] KeyOceneni - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Ocenění'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserAwards'
		self.BlueButton()
		self.KeyFlag = 'Oceneni'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyOceneni - konec\n')

	def KeySouvisejici(self):
		LogCSFD.WriteToFile('[CSFD] KeySouvisejici - zacatek\n')
		self.KeyPressLong = False
		self.KeyFlag = 'Souvisejici'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() == '':
					LogCSFD.WriteToFile('[CSFD] KeySouvisejici - key_red\n')
					LogCSFD.WriteToFile('[CSFD] KeySouvisejici - konec\n')
					return
			else:
				self.exitServiceMenu()
			searchresults = ParserCSFD.parserListOfRelatedMovies()
			if len(searchresults) > 0:
				self.Detail100Exit = False
				self.Detail100Pozice = 0
				self.selectedMenuRow = None
				self.NacistNazevPoradu = False
				self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True, False)
				self.ItemsLoad()
				self['menu'].moveToIndex(0)
				self.showMenu()
			else:
				LogCSFD.WriteToFile('[CSFD] KeySouvisejici - nejsou zaznamy\n')
		LogCSFD.WriteToFile('[CSFD] KeySouvisejici - konec\n')
		return

	def KeyPodobne(self):
		LogCSFD.WriteToFile('[CSFD] KeyPodobne - zacatek\n')
		self.KeyPressLong = False
		self.KeyFlag = 'Podobne'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() == '':
					LogCSFD.WriteToFile('[CSFD] KeyPodobne - key_red\n')
					LogCSFD.WriteToFile('[CSFD] KeyPodobne - konec\n')
					return
			else:
				self.exitServiceMenu()
			searchresults = ParserCSFD.parserListOfSimilarMovies()
			if len(searchresults) > 0:
				self.Detail100Exit = False
				self.Detail100Pozice = 0
				self.selectedMenuRow = None
				self.NacistNazevPoradu = False
				self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True, False)
				self.ItemsLoad()
				self['menu'].moveToIndex(0)
				self.showMenu()
			else:
				LogCSFD.WriteToFile('[CSFD] KeyPodobne - nejsou zaznamy\n')
		LogCSFD.WriteToFile('[CSFD] KeyPodobne - konec\n')
		return

	def KeySerie(self):
		LogCSFD.WriteToFile('[CSFD] KeySerie - zacatek\n')
		self.KeyPressLong = False
		self.KeyFlag = 'Serie'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() == '':
					LogCSFD.WriteToFile('[CSFD] KeySerie - key_red\n')
					LogCSFD.WriteToFile('[CSFD] KeySerie - konec\n')
					return
			else:
				self.exitServiceMenu()
			searchresults = ParserCSFD.parserListOfSeries()
			if len(searchresults) > 0:
				self.Detail100Exit = False
				self.Detail100Pozice = 0
				self.selectedMenuRow = None
				self.NacistNazevPoradu = False
				self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True, False)
				self.ItemsLoad()
				self['menu'].moveToIndex(0)
				self.showMenu()
			else:
				LogCSFD.WriteToFile('[CSFD] KeySerie - nejsou zaznamy\n')
		LogCSFD.WriteToFile('[CSFD] KeySerie - konec\n')
		return

	def KeyEpizody(self):
		LogCSFD.WriteToFile('[CSFD] KeyEpizody - zacatek\n')
		self.KeyPressLong = False
		self.KeyFlag = 'Epizody'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() == '':
					LogCSFD.WriteToFile('[CSFD] KeyEpizody - key_red\n')
					LogCSFD.WriteToFile('[CSFD] KeyEpizody - konec\n')
					return
			else:
				self.exitServiceMenu()
			searchresults = ParserCSFD.parserListOfEpisodes()
			if len(searchresults) > 0:
				self.Detail100Exit = False
				self.Detail100Pozice = 0
				self.selectedMenuRow = None
				self.NacistNazevPoradu = False
				self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True, False)
				self.ItemsLoad()
				self['menu'].moveToIndex(0)
				self.showMenu()
			else:
				LogCSFD.WriteToFile('[CSFD] KeyEpizody - nejsou zaznamy\n')
		LogCSFD.WriteToFile('[CSFD] KeyEpizody - konec\n')
		return

	def KeyHodnoceni(self):
		LogCSFD.WriteToFile('[CSFD] KeyHodnoceni - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Hodnocení'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserReviews'
		self.BlueButton()
		self.KeyFlag = 'Hodnoceni'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyHodnoceni - konec\n')

	def KeyPremiery(self):
		LogCSFD.WriteToFile('[CSFD] KeyPremiery - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Premiéry'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserPremiery'
		self.BlueButton()
		self.KeyFlag = 'Premiery'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyPremiery - konec\n')

	def KeyGalerie(self):
		LogCSFD.WriteToFile('[CSFD] KeyGalerie - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Galerie'))
		self.PageSpec = 1
		self.GalleryActIdx = 0
		self.querySpecAkce = 'UserGallery'
		self.BlueButton()
		self.KeyFlag = 'Galerie'
		if self.PosterSlideShowTimer.isActive():
			self.PosterSlideShowTimer.stop()
		self.CSFDshowSpec()
		if config.misc.CSFD.GallerySlide.getValue():
			self.CSFDGallerySlideShowStart()
		LogCSFD.WriteToFile('[CSFD] KeyGalerie - konec\n')

	def KeyPostery(self):
		LogCSFD.WriteToFile('[CSFD] KeyPostery - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Poster'))
		self.PageSpec = 1
		self.PosterActIdx = 0
		self.querySpecAkce = 'UserPoster'
		self.BlueButton()
		self.KeyFlag = 'Postery'
		if self.GallerySlideShowTimer.isActive():
			self.GallerySlideShowTimer.stop()
		self.CSFDshowSpec()
		if config.misc.CSFD.PosterSlide.getValue():
			self.CSFDPosterSlideShowStart()
		LogCSFD.WriteToFile('[CSFD] KeyPostery - konec\n')

	def KeyVideoButton(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Video'
		if self.Page > 0 and self.stahnutoCSFD2 != '':
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeyVideoButton - zacatek\n')
					self.KeyVideo()
					LogCSFD.WriteToFile('[CSFD] KeyVideoButton - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeyVideoButton - zacatek\n')
				self.exitServiceMenu()
				self.KeyVideo()
				LogCSFD.WriteToFile('[CSFD] KeyVideoButton - konec\n')

	def DuplBouquet(self, pol):
		dupl = False
		for x in self.BouquetMenuRot:
			if x == pol:
				dupl = True
				break

		return dupl

	def CallBouquet(self, nextP=True):
		LogCSFD.WriteToFile('[CSFD] CallBouquet - zacatek\n')
		poc = 0
		if len(self.BouquetMenuRot) < 1:
			return
		if self.Page == 1:
			self.BouquetIndex = -1
		else:
			nasel = False
			for x in CSFDActionDict:
				if x[1] == self.querySpecAkce:
					nasel = True
					break

			if nasel:
				if x[0] != self.BouquetMenuRot[self.BouquetIndex]:
					for cislo_pol in range(len(self.BouquetMenuRot)):
						if self.BouquetMenuRot[cislo_pol] == x[0]:
							self.BouquetIndex = cislo_pol
							break

			else:
				self.BouquetIndex = -1
				
		oldIndex = self.BouquetIndex
		poc = 0
		prac = True
		while prac:
			poc += 1
			if poc > 20:
				break
			if nextP:
				self.BouquetIndex += 1
				if self.BouquetIndex >= len(self.BouquetMenuRot):
					self.BouquetIndex = 0
			else:
				self.BouquetIndex -= 1
				if self.BouquetIndex < 0:
					self.BouquetIndex = len(self.BouquetMenuRot) - 1
			typ = self.BouquetMenuRot[self.BouquetIndex]
			if typ == 'nic' or typ in self.FunctionExists:
				prac = True
			else:
				prac = False

		if poc < 20 and oldIndex != self.BouquetIndex:
			self.RunKey(typ)
		LogCSFD.WriteToFile('[CSFD] CallBouquet - konec\n')

	def KeybqNext(self):
		self.KeyPressLong = False
		self.KeyFlag = 'bqNext'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeybqNext - zacatek\n')
					self.CallBouquet(True)
					LogCSFD.WriteToFile('[CSFD] KeybqNext - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeybqNext - zacatek\n')
				self.exitServiceMenu()
				self.CallBouquet(True)
				LogCSFD.WriteToFile('[CSFD] KeybqNext - konec\n')

	def KeybqPrev(self):
		self.KeyPressLong = False
		self.KeyFlag = 'bqPrev'
		if self.Page > 0:
			if self.ServiceMenuFlag == 0:
				if self['key_red'].getText() != '':
					LogCSFD.WriteToFile('[CSFD] KeybqPrev - zacatek\n')
					self.CallBouquet(False)
					LogCSFD.WriteToFile('[CSFD] KeybqPrev - konec\n')
			else:
				LogCSFD.WriteToFile('[CSFD] KeybqPrev - zacatek\n')
				self.exitServiceMenu()
				self.CallBouquet(False)
				LogCSFD.WriteToFile('[CSFD] KeybqPrev - konec\n')

	def KeyVideo(self):
		LogCSFD.WriteToFile('[CSFD] KeyVideo - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Videa'))
		self.PageSpec = 1
		self.KeyPressLong = False
		self.KeyFlag = ''
		self.VideoActIdx = 0
		self.querySpecAkce = 'UserVideo'
		self.BlueButton()
		self.KeyFlag = 'Video'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyVideo - konec\n')

	def KeyUlozVideo(self):
		self.KeyPressLong = False
		self.KeyFlag = 'UlozVideo'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyUlozVideo - zacatek\n')
				self.UlozitVideo()
				LogCSFD.WriteToFile('[CSFD] KeyUlozVideo - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyUlozVideo - zacatek\n')
			self.exitServiceMenu()
			self.UlozitVideo()
			LogCSFD.WriteToFile('[CSFD] KeyUlozVideo - konec\n')

	def KeySpustitVideo(self):
		self.KeyPressLong = False
		self.KeyFlag = 'SpustitVideo'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeySpustitVideo - zacatek\n')
				self.CSFDgetEntryVideo()
				self.CSFDRefreshVideoInformation()
				LogCSFD.WriteToFile('[CSFD] KeySpustitVideo - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeySpustitVideo - zacatek\n')
			self.exitServiceMenu()
			self.CSFDgetEntryVideo()
			self.CSFDRefreshVideoInformation()
			LogCSFD.WriteToFile('[CSFD] KeySpustitVideo - konec\n')

	def KeyFanousci(self):
		LogCSFD.WriteToFile('[CSFD] KeyFanousci - zacatek\n')
		self['extralabel'].setText('')
		self['key_blue'].setText(_('Fanoušci'))
		self.PageSpec = 1
		self.querySpecAkce = 'UserFans'
		self.BlueButton()
		self.KeyFlag = 'Fanousci'
		self.CSFDshowSpec()
		LogCSFD.WriteToFile('[CSFD] KeyFanousci - konec\n')

	def ResetAndRunCSFD(self):
		if self.ServiceMenuFlag > 0:
			self.exitServiceMenu()
		self.Page = 0
		self.resultlist = []
		self['menu'].hide()
		self['ratinglabel'].show()
		self['contentlabel'].show()
		self['detailslabel'].show()
		if config.misc.CSFD.ShowLine.getValue():
			self['line'].show()
		self['statusbar'].show()
		self['poster'].hide()
		self['stars'].hide()
		self['starsbg'].hide()
		self['starsmt'].hide()
		self['starsmtbg'].hide()
		self['stars0'].hide()
		self['starsbg0'].hide()
		self['stars50'].hide()
		self['starsbg50'].hide()
		self['stars100'].hide()
		self['starsbg100'].hide()
		self.getCSFD()

	def InputKeyCallback(self, ret):
		LogCSFD.WriteToFile('[CSFD] InputKeyCallback - zacatek\n')
		self.AntiFreezeTimerWorking = True
		if ret is not None and ret != '':
			ret = ret.strip()
			if len(ret) > 0:
				LogCSFD.WriteToFile('[CSFD] InputKeyCallback - eventName - OK\n')
				self.eventName = Uni8(ret)
				LogCSFD.WriteToFile('[CSFD] InputKeyCallback - eventName ' + self.eventName + '\n')
				self.EPG = ''
				self.DVBchannel = ''
				self.ChannelsCSFD = []
				self.eventMovieSourceOfDataEPG = False
				CSFDGlobalVar.setCSFDcur(1)
				self.ResetAndRunCSFD()
		LogCSFD.WriteToFile('[CSFD] InputKeyCallback - konec\n')
		return

	def KeyHelp(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Help'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyHelp - zacatek\n')
				self.showScreenHelp()
				LogCSFD.WriteToFile('[CSFD] KeyHelp - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyHelp - zacatek\n')
			self.exitServiceMenu()
			self.showScreenHelp()
			LogCSFD.WriteToFile('[CSFD] KeyHelp - konec\n')

	def KeySetUp(self):
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeySetUp - zacatek\n')
				self.showSetupScreen()
				LogCSFD.WriteToFile('[CSFD] KeySetUp - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeySetUp - zacatek\n')
			self.exitServiceMenu()
			self.showSetupScreen()
			LogCSFD.WriteToFile('[CSFD] KeySetUp - konec\n')

	def keyNumber1(self):
		self.KeyPressLong = False
		self.KeyFlag = '1'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber1 - zacatek\n')
				if self.Page == 0 and self.resultlist is not None and len(self.resultlist) > 0:
					self.SortTypeChange(change_s=True, back=True)
					self.Detail100Exit = False
					self.showMenu()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx += -1
							if self.GalleryActIdx < 0:
								self.GalleryActIdx = 0
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx += -1
							if self.PosterActIdx < 0:
								self.PosterActIdx = 0
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx += -1
							if self.VideoActIdx < 0:
								self.VideoActIdx = 0
					else:
						self.PageSpec += -1
						if self.PageSpec < 1:
							self.PageSpec = 1
					self.CSFDshowSpec()
				LogCSFD.WriteToFile('[CSFD] KeyNumber1 - konec\n')
		return

	def keyNumber3(self):
		self.KeyPressLong = False
		self.KeyFlag = '3'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber3 - zacatek\n')
				if self.Page == 0 and self.resultlist is not None and len(self.resultlist) > 0:
					self.SortTypeChange(change_s=True, back=False)
					self.Detail100Exit = False
					self.showMenu()
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GallerySlideShowTimer.isActive():
							self.GallerySlideShowTimer.stop()
						if self.GalleryCountPix > 0:
							self.GalleryActIdx += 1
							if self.GalleryActIdx >= self.GalleryCountPix:
								self.GalleryActIdx = self.GalleryCountPix - 1
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterSlideShowTimer.isActive():
							self.PosterSlideShowTimer.stop()
						if self.PosterCountPix > 0:
							self.PosterActIdx += 1
							if self.PosterActIdx >= self.PosterCountPix:
								self.PosterActIdx = self.PosterCountPix - 1
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.VideoActIdx += 1
							if self.VideoActIdx >= self.VideoCountPix:
								self.VideoActIdx = self.VideoCountPix - 1
					else:
						self.PageSpec += 1
					self.CSFDshowSpec()
				LogCSFD.WriteToFile('[CSFD] KeyNumber3 - konec\n')
		return

	def keyNumber0(self):
		self.KeyPressLong = False
		self.KeyFlag = '0'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber0 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey0.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber0 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber0 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey0.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber0 - konec\n')

	def keyNumber2(self):
		self.KeyPressLong = False
		self.KeyFlag = '2'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber2 - zacatek\n')
				self.showSetupScreen()
				LogCSFD.WriteToFile('[CSFD] KeyNumber2 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber2 - zacatek\n')
			self.exitServiceMenu()
			self.showSetupScreen()
			LogCSFD.WriteToFile('[CSFD] KeyNumber2 - konec\n')

	def keyNumber4(self):
		self.KeyPressLong = False
		self.KeyFlag = '4'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber4 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey4.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber4 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber4 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey4.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber4 - konec\n')

	def keyNumber5(self):
		self.KeyPressLong = False
		self.KeyFlag = '5'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber5 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey5.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber5 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber5 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey5.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber5 - konec\n')

	def keyNumber6(self):
		self.KeyPressLong = False
		self.KeyFlag = '6'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber6 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey6.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber6 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber6 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey6.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber6 - konec\n')

	def keyNumber7(self):
		self.KeyPressLong = False
		self.KeyFlag = '7'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber7 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey7.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber7 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber7 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey7.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber7 - konec\n')

	def keyNumber8(self):
		self.KeyPressLong = False
		self.KeyFlag = '8'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber8 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey8.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber8 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber8 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey8.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber8 - konec\n')

	def keyNumber9(self):
		self.KeyPressLong = False
		self.KeyFlag = '9'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyNumber9 - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKey9.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyNumber9 - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyNumber9 - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKey9.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyNumber9 - konec\n')

	def keyTestMenu(self):
		LogCSFD.WriteToFile('[CSFD] keyTestMenu\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.closeCSFDIconMenu, CSFDIconMenu)

	def closeCSFDIconMenu(self):
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] closeCSFDIconMenu\n')

	def keyPlayPause(self):
		self.KeyPressLong = False
		self.KeyFlag = 'PlayPause'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] keyPlayPause - zacatek\n')
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GalleryCountPix > 0:
							if self.GallerySlideShowTimer.isActive():
								self.GallerySlideShowTimer.stop()
								self.CSFDGalleryShow()
							else:
								self.CSFDGallerySlideShowStart()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterCountPix > 0:
							if self.PosterSlideShowTimer.isActive():
								self.PosterSlideShowTimer.stop()
								self.CSFDPosterShow()
							else:
								self.CSFDPosterSlideShowStart()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.CSFDgetEntryVideo()
							self.CSFDRefreshVideoInformation()
				LogCSFD.WriteToFile('[CSFD] keyPlayPause - konec\n')

	def keyPlay(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Play'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] keyPlay - zacatek\n')
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GalleryCountPix > 0:
							if not self.GallerySlideShowTimer.isActive():
								self.CSFDGallerySlideShowStart()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterCountPix > 0:
							if not self.PosterSlideShowTimer.isActive():
								self.CSFDPosterSlideShowStart()
					elif self.querySpecAkce == 'UserVideo':
						if self.VideoCountPix > 0:
							self.CSFDgetEntryVideo()
							self.CSFDRefreshVideoInformation()
				LogCSFD.WriteToFile('[CSFD] keyPlay - konec\n')

	def keyPause(self):
		self.KeyPressLong = False
		self.KeyFlag = 'Pause'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] keyPause - zacatek\n')
				if self.Page == 2:
					if self.querySpecAkce == 'UserGallery':
						if self.GalleryCountPix > 0:
							if self.GallerySlideShowTimer.isActive():
								self.GallerySlideShowTimer.stop()
								self.CSFDGalleryShow()
					elif self.querySpecAkce == 'UserPoster':
						if self.PosterCountPix > 0:
							if self.PosterSlideShowTimer.isActive():
								self.PosterSlideShowTimer.stop()
								self.CSFDPosterShow()
				LogCSFD.WriteToFile('[CSFD] keyPause - konec\n')

	def keyLR(self):
		self.KeyPressLong = True
		self.KeyFlag = 'LR'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyLR - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKeyLR.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyLR - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyLR - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKeyLR.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyLR - konec\n')

	def keyLB(self):
		self.KeyPressLong = True
		self.KeyFlag = 'LB'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyLB - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKeyLB.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyLB - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyLB - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKeyLB.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyLB - konec\n')

	def keyLG(self):
		self.KeyPressLong = True
		self.KeyFlag = 'LG'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyLG - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKeyLG.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyLG - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyLG - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKeyLG.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyLG - konec\n')

	def keyLY(self):
		self.KeyPressLong = True
		self.KeyFlag = 'LY'
		if self.ServiceMenuFlag == 0:
			if self['key_red'].getText() != '':
				LogCSFD.WriteToFile('[CSFD] KeyLY - zacatek\n')
				self.RunKey(config.misc.CSFD.HotKeyLY.getValue())
				LogCSFD.WriteToFile('[CSFD] KeyLY - konec\n')
		else:
			LogCSFD.WriteToFile('[CSFD] KeyLY - zacatek\n')
			self.exitServiceMenu()
			self.RunKey(config.misc.CSFD.HotKeyLY.getValue())
			LogCSFD.WriteToFile('[CSFD] KeyLY - konec\n')

	def GetItemColourRateB(self, rate=-1):
		if rate >= 70:
			barva = CSFDratingColor_100
		elif rate >= 30:
			barva = CSFDratingColor_50
		elif rate >= 0:
			barva = CSFDratingColor_0
		else:
			barva = CSFDratingColor_Nothing
		return barva

	def GetItemColour(self, typ=''):
		if typ == 'c0':
			barva = CSFDratingColor_Nothing
		elif typ == 'c1':
			barva = CSFDratingColor_100
		elif typ == 'c2':
			barva = CSFDratingColor_50
		elif typ == 'c3':
			barva = CSFDratingColor_0
		else:
			barva = CSFDratingColor_Nothing
			typ = 'c0'
		return (
		 barva, typ)

	def ItemsLoad(self):
		LogCSFD.WriteToFile('[CSFD] ItemsLoad - zacatek\n')
		listP = []
		velx = self['menu'].instance.size().width()
		pic_c0 = loadPixmapCSFD('csfd_c0.png')
		pic_c1 = loadPixmapCSFD('csfd_c1.png')
		pic_c2 = loadPixmapCSFD('csfd_c2.png')
		pic_c3 = loadPixmapCSFD('csfd_c3.png')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue()) + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue()) + 3
		h1 = (h - 10) // 2
		for item in self.resultlist:
			res = [
			 item]
			barva, typ = self.GetItemColour(item[8])
			if typ == 'c0':
				png_type = pic_c0
			elif typ == 'c1':
				png_type = pic_c1
			elif typ == 'c2':
				png_type = pic_c2
			elif typ == 'c3':
				png_type = pic_c3
			else:
				png_type = pic_c0
			if config.misc.CSFD.Design.getValue() == '1' or config.misc.CSFD.Design.getValue() == '2':
				barva = CSFDratingColor_Nothing
				res.append(MultiContentEntryText(pos=(0, 0), size=(velx - 15, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=item[0], color=barva, color_sel=barva))
			else:
				res.append(MultiContentEntryPixmap(pos=(0, h1), size=(10, 10), png=png_type))
				res.append(MultiContentEntryText(pos=(15, 0), size=(velx - 15, h), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=item[0], color=barva, color_sel=barva))
			listP.append(res)

		self['menu'].setList(listP)
		self['menu'].moveToIndex(0)
		LogCSFD.WriteToFile('[CSFD] ItemsLoad - konec\n')

	def SortTypeSetUpIndex(self, id_polozky=0):
		LogCSFD.WriteToFile('[CSFD] SortTypeSetUpIndex - zacatek\n')
		kk = 0
		for x in self.resultlist:
			if x[5] == id_polozky:
				LogCSFD.WriteToFile('[CSFD] SortTypeSetUpIndex - id nalezeno na pozici ' + str(kk) + '\n')
				self['menu'].moveToIndex(kk)
				LogCSFD.WriteToFile('[CSFD] SortTypeSetUpIndex - id menu nastaveno\n')
				break
			kk += 1

		LogCSFD.WriteToFile('[CSFD] SortTypeSetUpIndex - konec\n')

	def SortTypeChange(self, change_s=True, back=False, directTypeSort=-1):
		LogCSFD.WriteToFile('[CSFD] SortTypeChange - zacatek\n')
		if self.resultlist is None or len(self.resultlist) == 0:
			LogCSFD.WriteToFile('[CSFD] SortTypeChange - neni seznam\n')
			LogCSFD.WriteToFile('[CSFD] SortTypeChange - konec\n')
			return
		else:
			vybrany_prvek_id = 0
			if change_s:
				if self.selectedMenuRow is not None:
					vybrany_prvek_id = self.selectedMenuRow[5]
				LogCSFD.WriteToFile('[CSFD] SortTypeChange - vybrany prvek ' + str(vybrany_prvek_id) + '\n')
				if directTypeSort == -1:
					if back:
						self.SortType = self.SortType - 1
						if self.SortType < 0:
							self.SortType = 3
					else:
						self.SortType = self.SortType + 1
						if self.SortType > 3:
							self.SortType = 0
				else:
					self.SortType = directTypeSort
			if self.SortType == 0:
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 0 - zacatek\n')
				self.resultlist.sort(key=lambda z: z[0], reverse=True)
				self.resultlist.sort(key=lambda z: z[2])
				self.resultlist.sort(key=lambda z: z[4], reverse=True)
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 0 - konec\n')
			elif self.SortType == 1:
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 1 - zacatek\n')
				self.resultlist.sort(key=lambda z: z[5])
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 1 - konec\n')
			elif self.SortType == 2:
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 2 - zacatek\n')
				self.resultlist.sort(key=lambda z: z[0], reverse=True)
				self.resultlist.sort(key=lambda z: z[2])
				self.resultlist.sort(key=lambda z: z[9], reverse=True)
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 2 - konec\n')
			elif self.SortType == 3:
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 3 - zacatek\n')
				self.resultlist.sort(key=lambda z: z[2])
				LogCSFD.WriteToFile('[CSFD] SortTypeChange 3 - konec\n')
			self.ItemsLoad()
			if change_s:
				self.SortTypeSetUpIndex(id_polozky=vybrany_prvek_id)
			sss = _('Setříděno podle ') + self.SortTypeText[self.SortType]
			self['sortlabel'].setText(sss)
			self['sortlabel'].show()
			LogCSFD.WriteToFile('[CSFD] SortTypeChange - konec\n')
			return

	def showMenu(self):
		if (self.Page is 1 or self.Page is 2) and self.resultlist is not None:
			if len(self.resultlist) > 0:
				self.Page = 0
				self.IMDBpath = ''
				self.CSFDratingUsers = ''
				LogCSFD.WriteToFile('[CSFD] showMenu - zacatek\n')
				self['statusbar'].setText(_('Autor pluginu: ') + 'petrkl12@tvplugins.cz')
				if self.selectedMenuRow is not None:
					self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
				else:
					self.summaries.setText(' ', 10)
				self['titellabel'].instance.setForegroundColor(gRGB(CSFDColor_Titel))
				self['menu'].show()
				self['stars'].hide()
				self['starsbg'].hide()
				self['starsmt'].hide()
				self['starsmtbg'].hide()
				self['stars0'].hide()
				self['starsbg0'].hide()
				self['stars50'].hide()
				self['starsbg50'].hide()
				self['stars100'].hide()
				self['starsbg100'].hide()
				self['ratinglabel'].hide()
				self['contentlabel'].hide()
				self['extralabel'].hide()
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				self['photolabel'].hide()
				self['playbutton'].hide()
				self['line'].hide()
				self['poster'].hide()
				self['pagebg'].hide()
				self['pageb1'].hide()
				self['pageb3'].hide()
				self['paget1'].hide()
				self['paget3'].hide()
				self['page'].setText('')
				self['page'].hide()
				if self.KeyFlag == 'Podobne':
					sss = Uni8(self.ActName)
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						if len(sss) > 25:
							sss = sss[0:25] + ' ...'
						self['titellabel'].setText(strUni(char2Allowchar(sss)))
					else:
						if len(sss) > 50:
							sss = sss[0:50] + ' ...'
						self['titellabel'].setText(_('Pořad: ') + strUni(char2Allowchar(sss)))
					LogCSFD.WriteToFile('[CSFD] showMenu - podobne k filmu: ' + sss + '\n')
					self['titellabel'].show()
					sss = _('Zobrazeny podobné pořady')
					self['sortlabel'].setText(sss)
					self['sortlabel'].show()
				elif self.KeyFlag == 'Souvisejici':
					sss = Uni8(self.ActName)
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						if len(sss) > 25:
							sss = sss[0:25] + ' ...'
						self['titellabel'].setText(strUni(char2Allowchar(sss)))
					else:
						if len(sss) > 50:
							sss = sss[0:50] + ' ...'
						self['titellabel'].setText(_('Pořad: ') + strUni(char2Allowchar(sss)))
					LogCSFD.WriteToFile('[CSFD] showMenu - souvisejici k filmu: ' + sss + '\n')
					self['titellabel'].show()
					sss = _('Zobrazeny související pořady')
					self['sortlabel'].setText(sss)
					self['sortlabel'].show()
				elif self.KeyFlag == 'Serie':
					sss = Uni8(self.ActName)
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						if len(sss) > 25:
							sss = sss[0:25] + ' ...'
						self['titellabel'].setText(strUni(char2Allowchar(sss)))
					else:
						if len(sss) > 50:
							sss = sss[0:50] + ' ...'
						self['titellabel'].setText(_('Seriál: ') + strUni(char2Allowchar(sss)))
					LogCSFD.WriteToFile('[CSFD] showMenu - serie k serialu: ' + sss + '\n')
					self['titellabel'].show()
					sss = _('Zobrazeny řady seriálu')
					self['sortlabel'].setText(sss)
					self['sortlabel'].show()
				elif self.KeyFlag == 'Epizody':
					sss = Uni8(self.ActName)
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						if len(sss) > 25:
							sss = sss[0:25] + ' ...'
						self['titellabel'].setText(strUni(char2Allowchar(sss)))
					else:
						if len(sss) > 50:
							sss = sss[0:50] + ' ...'
						self['titellabel'].setText(_('Seriál: ') + strUni(char2Allowchar(sss)))
					LogCSFD.WriteToFile('[CSFD] showMenu - epizody k serialu: ' + sss + '\n')
					self['titellabel'].show()
					sss = _('Zobrazeny epizody seriálu')
					self['sortlabel'].setText(sss)
					self['sortlabel'].show()
				else:
					sss = Uni8(self.eventNameLocal)
					if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
						if len(sss) > 25:
							sss = sss[0:25] + ' ...'
						self['titellabel'].setText(strUni(char2Allowchar(sss)))
					else:
						if len(sss) > 50:
							sss = sss[0:50] + ' ...'
						self['titellabel'].setText(_('Hledaný film: ') + strUni(char2Allowchar(sss)))
					LogCSFD.WriteToFile('[CSFD] showMenu - film: ' + sss + '\n')
					self['titellabel'].show()
					sss = _('Setříděno podle ') + self.SortTypeText[self.SortType]
					self['sortlabel'].setText(sss)
					self['sortlabel'].show()
				self['detailslabel'].setText('')
				self['detailslabel'].hide()
				self['line'].hide()
				self['key_blue'].setText(_('Zadej pořad'))
				self['key_yellow'].setText(_('Detaily'))
				self['key_green'].setText(_('Výběr z EPG'))
				self['key_red'].setText(_('Zpět'))
				self['pagebg'].hide()
				self['pageb1'].hide()
				self['pageb3'].hide()
				self['paget1'].hide()
				self['paget3'].hide()
				self['page'].setText('')
				self['page'].hide()
				if self.selectedMenuRow is not None:
					self.summaries.setText(self.selectedMenuRow[0], GetItemColourN(self.selectedMenuRow[8]))
				else:
					self.summaries.setText(' ', 10)
				LogCSFD.WriteToFile('[CSFD] showMenu - konec\n')
		return

	def DownloadDetailMovie(self):

		def SetNotFind(textInfo='', textStatus=''):
			self.Page = 0
			self.summaries.setText(textInfo + self.eventNameLocal, 10)
			self['detailslabel'].setText(textInfo + self.eventNameLocal)
			self['statusbar'].setText(textStatus)
			self['sortlabel'].setText('')
			self['key_green'].setText(_('Výběr z EPG'))
			self['key_yellow'].setText('')
			self['key_red'].setText(_('Zpět'))
			self['key_blue'].setText(_('Zadej pořad'))
			self['pagebg'].hide()
			self['pageb1'].hide()
			self['pageb3'].hide()
			self['paget1'].hide()
			self['paget3'].hide()
			self['page'].setText('')
			self['page'].hide()

		LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie - zacatek\n', 2)
		LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie - linkGlobal ' + self.linkGlobal + '\n', 2)
		
		fetchurl = self.linkGlobal
		data = csfdAndroidClient.get_json_by_uri( fetchurl )
		ParserCSFD.setJson( data )
		
#		page = requestCSFD(fetchurl, headers=std_headers_UL2, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
#		ParserCSFD.setHTML2utf8(page)

		if ParserCSFD.testJson():

			try:
				self.CSFDparseUser()
			except:
				LogCSFD.WriteToFile('[CSFD] CSFDparseUser - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
			else:
				self['statusbar'].setText(_('CSFD stahování detailu dokončeno'))
				self.stahnutoCSFD2 = fetchurl
				if self.NacistNazevPoradu:
					self.CSFDparseName()
					self.SortTypeChange(change_s=False)
					self.NacistNazevPoradu = False
					if config.misc.CSFD.Detail100.getValue() == True and self.Detail100Akce == True and self.Search100shoda() == 1:
						LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie - Detail 100%\n', 2)
						self.Detail100Exit = True
						self['menu'].moveToIndex(self.Detail100Pozice)
						self.Page = 0
						try:
							self.showDetails()
						except:
							LogCSFD.WriteToFile('[CSFD] showDetails - chyba\n')
							err = traceback.format_exc()
							LogCSFD.WriteToFile(err)

					else:
						LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie - neni detail 100%\n', 2)
						self.Detail100Exit = False
						self.Page = 1
						self['statusbar'].setText(_('Autor pluginu: ') + 'petrkl12@tvplugins.cz')
						try:
							self.showMenu()
						except:
							LogCSFD.WriteToFile('[CSFD] showMenu - chyba\n')
							err = traceback.format_exc()
							LogCSFD.WriteToFile(err)

				else:
					self.LastDownloadedMovieUrl = fetchurl
					try:
						self.CSFDparse()
					except:
						LogCSFD.WriteToFile('[CSFD] CSFDparse - chyba\n')
						err = traceback.format_exc()
						LogCSFD.WriteToFile(err)

		else:
			LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie -  chyba dotazu!\n')
			ParserCSFD.printHTML()
			SetNotFind(_('CSFD - chyba dotazu!!! - film: '), '')
		LogCSFD.WriteToFile('[CSFD] DownloadDetailMovie - konec\n', 2)
		return

	def ReDownloadMovieAndParseMainPart(self):
		LogCSFD.WriteToFile('[CSFD] ReDownloadMovieAndParseMainPart - zacatek\n', 3)
		LogCSFD.WriteToFile('[CSFD] ReDownloadMovieAndParseMainPart - stahuji z url ' + self.LastDownloadedMovieUrl + '\n', 3)
		
#		page = requestCSFD(self.LastDownloadedMovieUrl, headers=std_headers_UL2, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
#		ParserCSFD.setHTML2utf8(page)

		data = csfdAndroidClient.get_json_by_uri( self.LastDownloadedMovieUrl )
		ParserCSFD.setJson( data )

		self.CSFDParseMainPart()
		LogCSFD.WriteToFile('[CSFD] ReDownloadMovieAndParseMainPart - konec\n', 3)

	def refreshRating(self):
		self['stars'].hide()
		self['starsbg'].hide()
		self['starsmt'].hide()
		self['starsmtbg'].hide()
		self['stars0'].hide()
		self['starsbg0'].hide()
		self['stars50'].hide()
		self['starsbg50'].hide()
		self['stars100'].hide()
		self['starsbg100'].hide()
		if self.ratingcount == 0:
			if self.ratingstars >= 0:
				if config.misc.CSFD.Design.getValue() == '1' or config.misc.CSFD.Design.getValue() == '2':
					self['stars'].setValue(self.ratingstars)
					self['stars'].show()
					self['starsbg'].show()
				elif self.ratingstars >= 70:
					self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_100))
					self['stars100'].setValue(self.ratingstars)
					self['stars100'].show()
					self['starsbg100'].show()
				elif self.ratingstars >= 30:
					self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_50))
					self['stars50'].setValue(self.ratingstars)
					self['stars50'].show()
					self['starsbg50'].show()
				elif self.ratingstars >= 0:
					self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_0))
					self['stars0'].setValue(self.ratingstars)
					self['stars0'].show()
					self['starsbg0'].show()
				else:
					self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_Nothing))
			else:
				self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_Nothing))
			self['ratinglabel'].setText(self.ratingtext)
			if config.misc.CSFD.Design.getValue() == '1':
				self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDColor_Titel))
			elif config.misc.CSFD.Design.getValue() == '2':
				self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDratingColor_HighlightKeyWords))
		elif self.ratingcount == 1:
			self['stars'].setValue(self.ratingstarsIMDB)
			self['stars'].show()
			self['starsbg'].show()
			self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDColor_IMDB))
			self['ratinglabel'].setText(self.ratingtextIMDB)
		elif self.ratingcount == 2:
			self['starsmt'].setValue(self.ratingstarsMetacritic)
			self['starsmt'].show()
			self['starsmtbg'].show()
			self['ratinglabel'].instance.setForegroundColor(gRGB(CSFDColor_Metacritic))
			self['ratinglabel'].setText(self.ratingtextMetacritic)

	def showDetails(self):
		akce = False
		self.Detail100Akce = False
		if self.resultlist is not None and len(self.resultlist) > 0 and self.Page == 0:
			self['ratinglabel'].show()
			self['contentlabel'].show()
			self['detailslabel'].show()
			if config.misc.CSFD.ShowLine.getValue():
				self['line'].show()
			self['statusbar'].show()
			akce = True
			self.Page = 1
			self['key_red'].setText('')
			self['key_green'].setText('')
			self['key_blue'].setText('')
			self['key_yellow'].setText('')
			self['pagebg'].hide()
			self['pageb1'].hide()
			self['pageb3'].hide()
			self['paget1'].hide()
			self['paget3'].hide()
			self['page'].setText('')
			self['page'].hide()
			self.selectedMenuRow = self['menu'].getCurrent()[0]
			self.linkGlobal = self.selectedMenuRow[1].strip()
			self['statusbar'].setText(_('CSFD - stahování detailu probíhá ...'))
			self['menu'].hide()
			self.resetLabels()
			self.DownloadDetailMovie()
		if self.Page == 2:
			akce = True
			if self.querySpecAkce == 'UserVideo' and self.KeyFlag == 'OK' and self.VideoCountPix > 0:
				self.CSFDgetEntryVideo()
				self.CSFDRefreshVideoInformation()
			else:
				self.Page = 1
				self['ratinglabel'].show()
				self['contentlabel'].show()
				self['detailslabel'].show()
				if config.misc.CSFD.ShowLine.getValue():
					self['line'].show()
				self['statusbar'].show()
				self['extralabel'].hide()
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				self['photolabel'].hide()
				self['playbutton'].hide()
				self['pagebg'].hide()
				self['pageb1'].hide()
				self['pageb3'].hide()
				self['paget1'].hide()
				self['paget3'].hide()
				self['page'].setText('')
				self['page'].hide()
				self['ratinglabel'].show()
				self['contentlabel'].show()
				self['detailslabel'].show()
				if config.misc.CSFD.ShowLine.getValue():
					self['line'].show()
				self['statusbar'].setText(_('Autor pluginu: ') + 'petrkl12@tvplugins.cz')
				self['statusbar'].show()
				self['poster'].show()
				self.refreshRating()
		if not akce:
			self['contentlabel'].show()
			self['detailslabel'].show()
			if config.misc.CSFD.ShowLine.getValue():
				self['line'].show()
			self['statusbar'].show()
		if self.Page == 1 and not akce and self.KeyFlag == 'OK':
			self.BlueButton()
		self.KeyFlag = ''
		self.KeyPressLong = False
		return

	def fetchFailedDownloadDetailMovie(self, string, url):
		LogCSFD.WriteToFile('[CSFD] fetchFailedDownloadDetailMovie - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - url: ' + Uni8(url) + '\n')
		chyba = string.getErrorMessage()
		ss2 = chyba.replace("'", '').strip().lower()
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - ss2: ' + Uni8(ss2) + '\n')
		if self.linkComment == '':
			LogCSFD.WriteToFile('[CSFD] fetchFailedDownloadDetailMovie - zkousim znovu pri chybe\n')
			self.Page = 0
			self.stahnutoCSFD2 = ''
			self.linkComment = 'podle-datetime/'
			self.showDetails()
		else:
			self.stahnutoCSFD2 = ''
			self.stahnutoCSFDImage = ''
			self['statusbar'].setText(_('CSFD - Chyba při stahování'))
			self['key_red'].setText(_('Zpět'))
		LogCSFD.WriteToFile('[CSFD] fetchFailedDownloadDetailMovie - konec\n')

	def fetchFailedReDownloadDetailMovie(self, string, url):
		LogCSFD.WriteToFile('[CSFD] fetchFailedReDownloadDetailMovie - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - url: ' + Uni8(url) + '\n')
		chyba = string.getErrorMessage()
		ss2 = chyba.replace("'", '').strip().lower()
		LogCSFD.WriteToFile('[CSFD] Chyba pri stahovani - ss2: ' + Uni8(ss2) + '\n')
		self['statusbar'].setText(_('CSFD - Chyba při stahování'))
		LogCSFD.WriteToFile('[CSFD] fetchFailedReDownloadDetailMovie - konec\n')

	def ReadDetailName(self):
		LogCSFD.WriteToFile('[CSFD] ReadDetailName - zacatek\n')
		self.Detail100Exit = False
		if self.resultlist is not None and len(self.resultlist) > 0:
			self.selectedMenuRow = self['menu'].getCurrent()[0]
			link = self.selectedMenuRow[1].strip()
			self.linkGlobal = link
			self.DownloadDetailMovie()
		LogCSFD.WriteToFile('[CSFD] ReadDetailName - konec\n')
		return

	def showExtras(self):
		if self.Page == 0:
			self.KeyText()
		if self.Page == 2:
			if self.querySpecAkce == 'UserGallery' and self.GalleryCountPix > 0:
				if config.misc.CSFD.GallerySlide.getValue():
					if self.GallerySlideShowTimer.isActive():
						self.GallerySlideShowTimer.stop()
						self.CSFDGalleryShow()
					else:
						self.CSFDGallerySlideShowStart()
			elif self.querySpecAkce == 'UserPoster' and self.PosterCountPix > 0:
				if config.misc.CSFD.PosterSlide.getValue():
					if self.PosterSlideShowTimer.isActive():
						self.PosterSlideShowTimer.stop()
						self.CSFDPosterShow()
					else:
						self.CSFDPosterSlideShowStart()
			elif self.querySpecAkce == 'UserVideo' and self.KeyFlag == 'OK' and self.VideoCountPix > 0:
				self.CSFDgetEntryVideo()
				self.CSFDRefreshVideoInformation()
		if self.Page == 1:
			self.Page = 2
			self['detailslabel'].hide()
			self['contentlabel'].hide()
			self['line'].hide()
			self['poster'].hide()
			if self.querySpecAkce == 'UserGallery' and self.GalleryCountPix > 0:
				if self.PosterSlideShowTimer.isActive():
					self.PosterSlideShowTimer.stop()
				self['extralabel'].hide()
				self['playbutton'].hide()
				self['photolabel'].show()
				self.CSFDGalleryShow()
				sss = str(self.GalleryActIdx + 1) + '/' + str(self.GalleryCountPix) + '	 ' + strUni(self.GallerySlideList[self.GalleryActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
				if config.misc.CSFD.GallerySlide.getValue():
					if not self.GallerySlideShowTimer.isActive():
						self.CSFDGallerySlideShowStart()
			elif self.querySpecAkce == 'UserPoster' and self.PosterCountPix > 0:
				if self.GallerySlideShowTimer.isActive():
					self.GallerySlideShowTimer.stop()
				self['extralabel'].hide()
				self['playbutton'].hide()
				self['photolabel'].show()
				self.CSFDPosterShow()
				sss = str(self.PosterActIdx + 1) + '/' + str(self.PosterCountPix) + '  ' + strUni(self.PosterSlideList[self.PosterActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
				if config.misc.CSFD.PosterSlide.getValue():
					if not self.PosterSlideShowTimer.isActive():
						self.CSFDPosterSlideShowStart()
			elif self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				if self.PosterSlideShowTimer.isActive():
					self.PosterSlideShowTimer.stop()
				if self.GallerySlideShowTimer.isActive():
					self.GallerySlideShowTimer.stop()
				self['extralabel'].hide()
				self['photolabel'].show()
				self['playbutton'].show()
				sss = str(self.VideoActIdx + 1) + '/' + str(self.VideoCountPix) + '	 ' + strUni(self.VideoSlideList[self.VideoActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
				self.CSFDRefreshVideoInformation()
			else:
				if self.PosterSlideShowTimer.isActive():
					self.PosterSlideShowTimer.stop()
				if self.GallerySlideShowTimer.isActive():
					self.GallerySlideShowTimer.stop()
				self['statusbar'].hide()
				self['statusbar'].setText('')
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				self['photolabel'].hide()
				self['playbutton'].hide()
				self['extralabel'].show()
			self['pagebg'].show()
			self['pageb1'].show()
			self['pageb3'].show()
			self['paget1'].show()
			self['paget3'].show()
			if self.querySpecAkce == 'UserGallery' and self.GalleryCountPix > 0:
				sss = str(self.GalleryActIdx + 1)
				self['page'].setText(_('Galerie č.%s' % sss))
				sss = str(self.GalleryActIdx + 1) + '/' + str(self.GalleryCountPix) + '	 ' + strUni(self.GallerySlideList[self.GalleryActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
			elif self.querySpecAkce == 'UserPoster' and self.PosterCountPix > 0:
				sss = str(self.PosterActIdx + 1)
				self['page'].setText(_('Poster č.%s' % sss))
				sss = str(self.PosterActIdx + 1) + '/' + str(self.PosterCountPix) + '  ' + strUni(self.PosterSlideList[self.PosterActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
			elif self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				sss = str(self.VideoActIdx + 1)
				self['page'].setText(_('Video č.%s' % sss))
				sss = str(self.VideoActIdx + 1) + '/' + str(self.VideoCountPix) + '	 ' + strUni(self.VideoSlideList[self.VideoActIdx][2])
				self['statusbar'].setText(sss)
				self['statusbar'].show()
			else:
				sss = str(self.PageSpec)
				self['page'].setText(_('Strana č.%s' % sss))
			self['page'].show()

	def KeyTesting(self):
		LogCSFD.WriteToFile('[CSFD] KeyTesting - zacatek\n')
		self.AntiFreezeTimerWorking = False
		from CSFDSimpleInfo import CSFDFindMovie
		CSFDFindMovie.FindMovieBasedOnName(self.eventName)
		self.AntiFreezeTimerWorking = True
		LogCSFD.WriteToFile('[CSFD] KeyTesting - konec\n')

	def openChannelSelection(self):
		CSFDGlobalVar.setCSFDcur(1)
		CSFDGlobalVar.setCSFDeventID_EPG(0)
		CSFDGlobalVar.setCSFDeventID_REF('')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.channelSelectionClosed, CSFDChannelSelection)

	def openAktChannelSelection(self):
		ref = self.session.nav.getCurrentlyPlayingServiceReference()
		if not CSFDGlobalVar.getCSFDcur() == 1:
			LogCSFD.WriteToFile('[CSFD] EPGSelection - nastavuji CSFDeventID_REF\n')
			ref = CSFDGlobalVar.getCSFDeventID_REF()
			LogCSFD.WriteToFile('[CSFD] EPGSelection - nastavuji CSFDeventID_REF - konec\n')
		self.AntiFreezeTimerWorking = False
		self.session.openWithCallback(self.channelSelectionClosed, CSFDEPGSelection, ref, openPlugin=False)

	def channelSelectionClosed(self, ret=None, retEPG=None, retDVBchannel=None):
		self.AntiFreezeTimerWorking = True
		if ret is not None and ret != '':
			self.eventName = ret
			if retEPG is not None and retEPG != '':
				self.EPG = retEPG
			if retDVBchannel is not None and retDVBchannel != '':
				self.DVBchannel = retDVBchannel
			self.ResetAndRunCSFD()
		return

	def KeySpustitIMDB(self):
		LogCSFD.WriteToFile('[CSFD] KeySpustitIMDB - zacatek\n')
		if config.misc.CSFD.IMDBCharsConversion.getValue():
			if self.Page == 0:
				evname = strUni(char2Diacritic(self.eventName))
			else:
				evname = strUni(char2Diacritic(self.ActName))
		elif self.Page == 0:
			evname = strUni(self.eventName)
		else:
			evname = strUni(self.ActName)
		self.AntiFreezeTimerWorking = False
		if self.IMDBpath == '':
			self.session.openWithCallback(self.IMDBClosed, CSFD_IMDBcalls, evname)
		else:
			self.session.openWithCallback(self.IMDBClosed, CSFD_IMDBcalls, evname, False, self.IMDBpath)
		LogCSFD.WriteToFile('[CSFD] KeySpustitIMDB - konec\n')

	def IMDBClosed(self):
		LogCSFD.WriteToFile('[CSFD] IMDBClosed - zacatek\n')
		self.AntiFreezeTimerWorking = True
		if self.ServiceMenuFlag > 0:
			self.exitServiceMenu()
		LogCSFD.WriteToFile('[CSFD] IMDBClosed - konec\n')

	def getCSFD(self):
		LogCSFD.CheckAndEmptyLog()
		LogCSFD.WriteToFile('[CSFD] getCSFD - zacatek\n')
		self['key_red'].setText('')
		self['key_blue'].setText('')
		self['key_green'].setText('')
		self['key_yellow'].setText('')
		self['pagebg'].hide()
		self['pageb1'].hide()
		self['pageb3'].hide()
		self['paget1'].hide()
		self['paget3'].hide()
		self['page'].setText('')
		self['page'].hide()
		self.ServiceMenuFlag = 0
		self.SortType = int(config.misc.CSFD.Default_Sort.getValue())
		self.resetLabels()
		self.Detail100Akce = True
		self.Detail100Exit = False
		self.PageSpec = 1
		self.FunctionExists = []
		self.linkComment = config.misc.CSFD.Comment_Sort.getValue()
		self.linkExtra = ''
		self.querySpecAkce = 'UserComments'
		self.AntiFreezeTimerWorking = True
		self.workingConfig = None
		self.IMDBpath = ''
		self.myreference = None
		self.CSFDratingUsers = ''
		self.PosterBasicCountPixAllP = -1
		self.PosterBasicCountPixAllG = -1
		self.PosterBasicCountPix = 0
		self.PosterBasicSlideStop = True
		self.PosterBasicActIdx = 0
		self.GalleryCountPix = 0
		self.GallerySlideStop = True
		self.GalleryActIdx = 0
		self.PosterCountPix = 0
		self.PosterSlideStop = True
		self.PosterActIdx = 0
		self.VideoCountPix = 0
		self.VideoActIdx = 0
		self.videoklipurl = ''
		self.videotitulkyurl = ''
		self.NacistNazevPoradu = False
		self.Detail100Pozice = 0
		self.PosterBasicSlideList = []
		self.ActName = ''
		self.KeyPressLong = False
		self.BouquetIndex = -1
		self.LastDownloadedMovieUrl = ''
		self.eventMovieYears = []
		self.eventMovieNameYears = ''
		self.selectedMenuRow = None
		self.ChannelsCSFD = []
		if self.KeyFlag == 'FindAll':
			self.FindAllItems = True
			self.Detail100Akce = False
			self.KeyFlag = ''
		else:
			self.FindAllItems = config.misc.CSFD.FindAllItems.getValue()
			self.KeyFlag = ''
		if not self.eventName:
			self.eventName = ''
		self.eventNameSecond = ''
		if not self.EPG:
			self.EPG = ''
		if not self.DVBchannel:
			self.DVBchannel = ''
		if not self.eventMovieSourceOfDataEPG:
			self.eventMovieSourceOfDataEPG = False
		if self.eventName is '':
			CSFDGlobalVar.setCSFDcur(1)
			CSFDGlobalVar.setCSFDeventID_EPG(0)
			CSFDGlobalVar.setCSFDeventID_REF('')
			self.EPG = ''
			self.DVBchannel = ''
			self.ChannelsCSFD = []
			self.eventMovieSourceOfDataEPG = False
			LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - zacatek\n')
			try:
				serviceref = self.session.nav.getCurrentlyPlayingServiceReference()
				if serviceref is not None:
					serviceHandler = eServiceCenter.getInstance()
					info = serviceHandler.info(serviceref)
					event = info.getEvent(serviceref)
					if event is not None:
						self.eventName = event.getEventName()
						short = event.getShortDescription()
						ext = event.getExtendedDescription()
						if short and short != self.eventName:
							self.EPG = short
						if ext:
							self.EPG += ext
						if self.EPG != '':
							self.EPG = self.eventName + ' - ' + self.EPG
						self.eventMovieSourceOfDataEPG = True
					self.DVBchannel = ServiceReference(serviceref).getServiceName()
			except:
				self.eventName = ''
				self.eventNameSecond = ''
				self.EPG = ''
				self.DVBchannel = ''
				self.ChannelsCSFD = []
				self.eventMovieSourceOfDataEPG = False
				LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)

			LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - konec\n')
			if self.eventName == '':
				LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - pokus2 - zacatek\n')
				try:
					service = self.session.nav.getCurrentService()
					if service is not None:
						info = service and service.info()
						if info is not None:
							event = info and info.getEvent(0)
							if event is not None:
								self.eventName = event.getEventName()
								short = event.getShortDescription()
								ext = event.getExtendedDescription()
								if short and short != self.eventName:
									self.EPG = short
								if ext is not None:
									self.EPG += ext
								if self.EPG != '':
									self.EPG = self.eventName + ' - ' + self.EPG
								self.eventMovieSourceOfDataEPG = True
							name = info.getName()
							if name is not None and name != '':
								self.DVBchannel = name
				except:
					self.eventName = ''
					self.eventNameSecond = ''
					self.EPG = ''
					self.DVBchannel = ''
					self.ChannelsCSFD = []
					self.eventMovieSourceOfDataEPG = False
					LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - pokus2 - chyba\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)

				LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - pokus2 - konec\n')
		is_Internet_OK = internet_on()
		
		if self.eventName is not '' and is_Internet_OK:
			LogCSFD.WriteToFile('[CSFD] getCSFD - eventName - zacatek\n')
			if isinstance(self.eventName, str):
				self.eventName = Uni8(self.eventName)
			if isinstance(self.EPG, str):
				self.EPG = Uni8(self.EPG)
			if isinstance(self.DVBchannel, str):
				self.DVBchannel = Uni8(self.DVBchannel)
			self.eventMovieNameYears = self.eventName
			if self.EPG != '':
				self.eventMovieYears = ParserCSFD.parserGetYears(self.EPG)
				self.eventMovieSourceOfDataEPG = True
			else:
				for yr in ParserCSFD.parserGetYears(self.eventName):
					pos = self.eventName.find(' (' + yr + ')')
					if pos >= 0:
						self.eventMovieYears.append(yr)
					pos = self.eventName.find(' [' + yr + ']')
					if pos >= 0:
						self.eventMovieYears.append(yr)

			if self.DVBchannel != '':
				self.ChannelsCSFD = GetCSFDNumberFromChannel(self.DVBchannel)
			else:
				self.ChannelsCSFD = []
			LogCSFD.WriteToFile('[CSFD] getCSFD - DVBchannel - ' + self.DVBchannel + '\n')
			LogCSFD.WriteToFile('[CSFD] getCSFD - ChannelsCSFD - ' + (' ').join(x for x in self.ChannelsCSFD) + '\n')
			self.eventNameSecond = ''
			for channel in self.ChannelsCSFD:
				if channel == '4' or channel == '5' or channel == '64' or channel == '65':
					LogCSFD.WriteToFile('[CSFD] getCSFD - CT puvodni nazev - ' + self.eventName + '\n')
					self.eventName, self.eventNameSecond = NameMovieCorrectionsForCTChannels(self.eventName)
					sss = char2Allowchar(self.eventNameSecond).strip()
					sss = NameMovieCorrections(sss)
					self.eventNameSecond = sss
					LogCSFD.WriteToFile('[CSFD] getCSFD - CT korekce nazvu - eventName: ' + self.eventName + '\n')
					LogCSFD.WriteToFile('[CSFD] getCSFD - CT korekce nazvu - eventNameSecond: ' + self.eventNameSecond + '\n')
					break

			sss = char2Allowchar(self.eventName).strip()
			sss = NameMovieCorrections(sss)
			self.eventName = sss
			self.eventNameLocal = strUni(sss)
			if self.eventName == self.eventNameSecond:
				self.eventNameSecond = ''
				LogCSFD.WriteToFile('[CSFD] getCSFD - eventNameSecond - zruseno\n')
			LogCSFD.WriteToFile('[CSFD] getCSFD - hledany film - upraveno ' + self.eventName + '\n')
			LogCSFD.WriteToFile('[CSFD] getCSFD - hledany film - upraveno Local ' + self.eventNameLocal + '\n')
			LogCSFD.WriteToFile('[CSFD] getCSFD - eventName - konec\n')
			self['statusbar'].setText(_('Probíhá vyhledávání v TV databázi CSFD ... (') + self.eventNameLocal + ')')
			if self.FindAllItems or not self.CSFDqueryTV():
				self['statusbar'].setText(_('Probíhá vyhledávání v databázi CSFD ... (') + self.eventNameLocal + ')')
				try:
					eventNameUrllib = quote(self.eventNameLocal)
					LogCSFD.WriteToFile('[CSFD] getCSFD - OK\n')
				except:
					LogCSFD.WriteToFile('[CSFD] getCSFD - chyba\n')
					eventNameUrllib = quote(strUni(char2Diacritic(char2Allowchar(self.eventName)).strip()))
					LogCSFD.WriteToFile('[CSFD] getCSFD - hledany film - chyba ' + eventNameUrllib + '\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)

#				if self.FindAllItems:
#					fetchurl = CSFDGlobalVar.getHTTP() + const_www_csfd + '/hledat/complete-films/?q=' + eventNameUrllib
#				elif self.eventMovieSourceOfDataEPG == False and len(self.eventMovieYears) == 1 and config.misc.CSFD.FindInclYear.getValue():
#					yr = quote(strUni(' (' + str(self.eventMovieYears[0]) + ')'))
#					fetchurl = CSFDGlobalVar.getHTTP() + const_www_csfd + '/hledat/?q=' + eventNameUrllib + yr
#				else:
#					fetchurl = CSFDGlobalVar.getHTTP() + const_www_csfd + '/hledat/?q=' + eventNameUrllib

				if self.FindAllItems:
					fetchurl = '#search_movie#' + eventNameUrllib
#				elif self.eventMovieSourceOfDataEPG == False and len(self.eventMovieYears) == 1 and config.misc.CSFD.FindInclYear.getValue():
				elif len(self.eventMovieYears) == 1 and config.misc.CSFD.FindInclYear.getValue():
					yr = ' (' + str(self.eventMovieYears[0]) + ')'
					fetchurl = '#search_movie#' + eventNameUrllib + yr
				else:
					fetchurl = '#search_movie#' + eventNameUrllib

				LogCSFD.WriteToFile('[CSFD] getCSFD - stahuji z url ' + fetchurl + '\n')
				
#				page = requestCSFD(fetchurl, headers=std_headers_UL2, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
				page = csfdAndroidClient.get_json_by_uri( fetchurl )	
				CSFDGlobalVar.setParalelDownload(self.CSFDquery, page)
				self.DownloadTimer.start(10, True)
				
				LogCSFD.WriteToFile('[CSFD] getCSFD - stahnuto\n')
		else:
			if not is_Internet_OK:
				LogCSFD.WriteToFile('[CSFD] getCSFD - chyba - Neni funkcni internet\n')
				self.summaries.setText(_('Není funkční internet!'), 10)
				self['statusbar'].setText(_('Není funkční internet!'))
				self['detailslabel'].setText(_('Není funkční internet!'))
				self['key_green'].setText('')
				self['key_blue'].setText('')
			elif self.eventName == '':
				LogCSFD.WriteToFile('[CSFD] getCSFD - Nemuzu nacist nazev poradu\n')
				self.summaries.setText(_('Nemůžu načíst název pořadu'), 10)
				self['statusbar'].setText(_('Nemůžu načíst název pořadu'))
				self['detailslabel'].setText(_('Nemůžu načíst název pořadu'))
				self['key_green'].setText(_('Výběr z EPG'))
				self['key_blue'].setText(_('Zadej pořad'))
			else:
				LogCSFD.WriteToFile('[CSFD] getCSFD - chyba - Neznama chyba (Chyba v pluginu!)\n')
				self.summaries.setText(_('Chyba v pluginu!'), 10)
				self['statusbar'].setText(_('Chyba v pluginu!'))
				self['detailslabel'].setText(_('Chyba v pluginu!'))
				self['key_green'].setText('')
				self['key_blue'].setText('')
			self['key_yellow'].setText('')
			self['sortlabel'].setText('')
			self['key_red'].setText(_('Zpět'))
			self['pagebg'].hide()
			self['pageb1'].hide()
			self['pageb3'].hide()
			self['paget1'].hide()
			self['paget3'].hide()
			self['page'].setText('')
			self['page'].hide()
		return

	def fetchFailed(self, string, url):
		LogCSFD.WriteToFile('[CSFD] fetchFailed - Chyba pri stahovani\n')
		print( 'CSFD fetchFailed - Error: ' + str(string) )
		LogCSFD.WriteToFile('[CSFD] fetchFailed - Chyba pri stahovani: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailed - Chyba pri stahovani - url: ' + Uni8(url) + '\n')
		self.stahnutoCSFD2 = ''
		self.stahnutoCSFDImage = ''
		self['statusbar'].setText(_('CSFD fetchFailed - Chyba při stahování'))
		self['key_red'].setText(_('Zpět'))

	def fetchFailedOst(self, string, url):
		LogCSFD.WriteToFile('[CSFD] fetchFailedOst - Chyba pri stahovani\n')
		print( 'CSFD fetchFailedOst - Error: ' + str(string) )
		LogCSFD.WriteToFile('[CSFD] fetchFailedOst - Chyba pri stahovani: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedOst - Chyba pri stahovani - url: ' + Uni8(url) + '\n')

	def fetchFailedPoster(self, string, url, localfile):
		LogCSFD.WriteToFile('[CSFD] fetchFailedPoster - Chyba pri stahovani posteru\n')
		print( 'CSFD fetchFailedPoster - Erorr: ' + str(string) )
		LogCSFD.WriteToFile('[CSFD] fetchFailedPoster - Chyba pri stahovani posteru: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedPoster - Chyba pri stahovani posteru - url: ' + Uni8(url) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedPoster - Chyba pri stahovani posteru - localfile: ' + Uni8(localfile) + '\n')

	def fetchFailedVideoPoster(self, string, url, localfile):
		LogCSFD.WriteToFile('[CSFD] fetchFailedVideoPoster - Chyba pri stahovani video posteru\n')
		print( 'CSFD fetchFailedVideoPoster - Erorr: ' + str(string) )
		LogCSFD.WriteToFile('[CSFD] fetchFailedVideoPoster - Chyba pri stahovani video posteru: ' + Uni8(string.getErrorMessage()) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedVideoPoster - Chyba pri stahovani video posteru - url: ' + Uni8(url) + '\n')
		LogCSFD.WriteToFile('[CSFD] fetchFailedVideoPoster - Chyba pri stahovani video posteru - localfile: ' + Uni8(localfile) + '\n')

	def SearchDuplicity(self, listOfResult, nazev='', cesta=''):
		finded = False
		nazev = Uni8(nazev)
		for x in listOfResult:
			if Uni8(x[0]) == nazev and x[1] == cesta:
				finded = True
				break

		return finded

	def CompareMovieYears(self, year=''):
		percent = 0
		shoda = False
		if not config.misc.CSFD.CompareInclYear.getValue() or len(self.eventMovieYears) == 0:
			return (percent, shoda)
		if len(year) == 6:
			year = year[1:-1]
			v_year = int(year)
		else:
			if len(year) == 4:
				v_year = int(year)
			else:
				return (
				 percent, shoda)
			for yr in self.eventMovieYears:
				m_year = int(yr)
				if m_year == v_year:
					shoda = True
				if abs(m_year - v_year) < 6:
					per = (200 - float(abs(m_year - v_year))) / 200 * 100
					if per > percent:
						percent = per

		percent = percent / len(self.eventMovieYears)
		return (percent, shoda)

	def Search100shoda(self):

		def key(x):
			return x[6]

		max_value, pozice = max_positions(self.resultlist, key)
		if max_value:
			if max_value == '00' or max_value == '01':
				pocet = 0
				self.Detail100Pozice = 0
			else:
				pocet = len(pozice)
				self.Detail100Pozice = pozice[0]
				if config.misc.CSFD.ReadDetailBasedOnScore.getValue() and pocet > 1:
					poc = 0
					score = -1
					mv_url = ''
					for pol in pozice:
						if self.resultlist[pol][4] > score:
							score = self.resultlist[pol][4]
							mv_url = self.resultlist[pol][1]
							self.Detail100Pozice = pol
							poc = 1
						elif self.resultlist[pol][4] == score:
							if self.resultlist[pol][1] != mv_url:
								poc += 1

					pocet = poc
		else:
			pocet = 0
			self.Detail100Pozice = 0
		return pocet

	def CSFDMenuPreparation(self, eventName, searchresults, simpleSearch=False, addTVscore=True, acceptance=0):
		LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - zacatek\n')
		resultlist = []
		res_shoda = False
		TV_shoda = False
		if searchresults is None or len(searchresults) == 0:
			LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - zadny seznam\n')
			LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - konec\n')
			return (
			 resultlist, res_shoda, TV_shoda)
		else:
			lastRoman = False
			lastNumber = False
			const_shoda_100 = 99.9
			y = 0
			vst_eventName = Uni8(eventName)
			vst_eventName_Corrected_Diacr = NameMovieCorrectionsForCompare(vst_eventName)
			vst_eventName_Corrected_Diacr_WO_Roman = vst_eventName_Corrected_Diacr
			vst_eventName_Corrected_WO_Diacr = char2Diacritic(vst_eventName_Corrected_Diacr).upper()
			vst_eventName_Corrected_WO_Diacr_WO_Roman = vst_eventName_Corrected_WO_Diacr
			vst_eventName_Corrected_WO_Diacr_CorrNumber = vst_eventName_Corrected_WO_Diacr
			TVMovies = None
			if addTVscore:
				LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - VYHLEDAVANI ZE SEZNAMU TV\n')
				if config.misc.CSFD.TVCache.getValue():
					stations = ''
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - ChannelsCSFD: ' + str(self.ChannelsCSFD) + '\n')
					for channel in self.ChannelsCSFD:
						if stations == '':
							stations += channel
						else:
							stations += '%2C' + channel

					if stations != '':
						TVMovies = TVMovieCache.getMoviesFromCache(stations)
						if TVMovies is not None:
							LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TVMovies - existuje\n')
						else:
							LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TVMovies - nenalezen - 1\n')
					else:
						LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TVMovies - nenalezen - 2\n')
			if simpleSearch:
				porovnejTexty = TextCompare
				LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TextCompare\n')
			else:
				if config.misc.CSFD.SortFindItems.getValue() == '0':
					porovnejTexty = TextSimilarityLD
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TextSimilarityLD\n')
				elif config.misc.CSFD.SortFindItems.getValue() == '1':
					porovnejTexty = TextSimilarityBigram
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TextSimilarityBigram\n')
				else:
					porovnejTexty = TextCompare
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TextCompare\n')
					
			zohlednitDiacr = False
			if self.eventMovieSourceOfDataEPG == True and config.misc.CSFD.FindInclDiacrEPG.getValue():
				zohlednitDiacr = True
			if self.eventMovieSourceOfDataEPG == False and config.misc.CSFD.FindInclDiacrOth.getValue():
				zohlednitDiacr = True
			pp = ParserCSFD.parserGetRomanNumbers(vst_eventName_Corrected_Diacr)
			pocet_pp = len(pp)
			if pocet_pp > 0:
				dodat = pp[(pocet_pp - 1)]
				dodat1 = ' ' + dodat
				vv = -1 * len(dodat1)
				if vst_eventName_Corrected_WO_Diacr[vv:].upper() == dodat1:
					if dodat == 'I':
						vst_eventName_Corrected_Diacr = vst_eventName_Corrected_Diacr[:vv].strip()
						vst_eventName_Corrected_Diacr_WO_Roman = vst_eventName_Corrected_Diacr_WO_Roman[:vv].strip()
						vst_eventName_Corrected_WO_Diacr = char2Diacritic(vst_eventName_Corrected_Diacr).upper()
						vst_eventName_Corrected_WO_Diacr_WO_Roman = vst_eventName_Corrected_WO_Diacr
					else:
						vst_eventName_Corrected_WO_Diacr_WO_Roman = vst_eventName_Corrected_WO_Diacr[:vv].strip()
						vst_eventName_Corrected_Diacr_WO_Roman = vst_eventName_Corrected_Diacr[:vv].strip()
					vst_eventName_Corrected_WO_Diacr_CorrNumber = vst_eventName_Corrected_WO_Diacr_WO_Roman + ' ' + fromRomanStr(dodat)
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - korekce1 ' + vst_eventName_Corrected_WO_Diacr_CorrNumber + '\n')
					lastRoman = True
			if not lastRoman:
				pp = ParserCSFD.parserGetNumbers(vst_eventName_Corrected_Diacr)
				pocet_pp = len(pp)
				if pocet_pp > 0:
					dodat = pp[(pocet_pp - 1)]
					dodat1 = ' ' + dodat
					vv = -1 * len(dodat1)
					if vst_eventName_Corrected_WO_Diacr[vv:].upper() == dodat1:
						if dodat == '1':
							vst_eventName_Corrected_Diacr = vst_eventName_Corrected_Diacr[:vv].strip()
							vst_eventName_Corrected_Diacr_WO_Roman = vst_eventName_Corrected_Diacr_WO_Roman[:vv].strip()
							vst_eventName_Corrected_WO_Diacr = char2Diacritic(vst_eventName_Corrected_Diacr).upper()
							vst_eventName_Corrected_WO_Diacr_WO_Roman = vst_eventName_Corrected_WO_Diacr
						else:
							vst_eventName_Corrected_WO_Diacr_WO_Roman = vst_eventName_Corrected_WO_Diacr[:vv].strip()
							vst_eventName_Corrected_Diacr_WO_Roman = vst_eventName_Corrected_Diacr[:vv].strip()
						vst_eventName_Corrected_WO_Diacr_CorrNumber = vst_eventName_Corrected_WO_Diacr_WO_Roman + ' ' + StrtoRoman(dodat)
						LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - korekce2 ' + vst_eventName_Corrected_WO_Diacr_CorrNumber + '\n')
						lastNumber = True
			LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - hledany film: ' + vst_eventName + '\n')
			for x in searchresults:
				res_Name_Orig = char2Allowchar(ParserCSFD.delHTMLtags(x[1]))
				nameMovies = res_Name_Orig + '#$' + vst_eventName + '#$' + str(simpleSearch)
				res_Name = NameMovieCorrections(res_Name_Orig)
				res_Name_Corrected_Diacr = NameMovieCorrectionsForCompare(res_Name)
				res_Name_Corrected_WO_Diacr = char2Diacritic(res_Name_Corrected_Diacr).upper()
				res_Name_Corrected_Diacr_WO_Roman = res_Name_Corrected_Diacr
				res_Name_Corrected_WO_Diacr_WO_Roman = res_Name_Corrected_WO_Diacr
				if movieCSFDCache.AreMovieNamesInScoreCache(nameMovies):
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - nacteno z cache\n')
					celkem_bodu, shoda100 = movieCSFDCache.getScoreForMovieNamesFromCache(nameMovies)
				else:
					pp = ParserCSFD.parserGetRomanNumbers(res_Name_Corrected_WO_Diacr)
					pocet_pp = len(pp)
					if pocet_pp > 0:
						dodat = pp[(pocet_pp - 1)]
						dodat1 = ' ' + dodat
						vv = -1 * len(dodat1)
						if res_Name_Corrected_WO_Diacr[vv:].upper() == dodat1:
							res_Name_Corrected_WO_Diacr_WO_Roman = res_Name_Corrected_WO_Diacr[:vv].strip()
							res_Name_Corrected_Diacr_WO_Roman = res_Name_Corrected_Diacr[:vv].strip()
					else:
						pp = ParserCSFD.parserGetNumbers(res_Name_Corrected_WO_Diacr)
						pocet_pp = len(pp)
						if pocet_pp > 0:
							dodat = pp[(pocet_pp - 1)]
							dodat1 = ' ' + dodat
							vv = -1 * len(dodat1)
							if res_Name_Corrected_WO_Diacr[vv:].upper() == dodat1:
								res_Name_Corrected_WO_Diacr_WO_Roman = res_Name_Corrected_WO_Diacr[:vv].strip()
								res_Name_Corrected_Diacr_WO_Roman = res_Name_Corrected_Diacr[:vv].strip()
					podobnost_Name_Corrected_WO_Diacr_WO_Roman = porovnejTexty(res_Name_Corrected_WO_Diacr_WO_Roman, vst_eventName_Corrected_WO_Diacr_WO_Roman)
					celkem_bodu = podobnost_Name_Corrected_WO_Diacr_WO_Roman
					shoda100 = '0'
					if podobnost_Name_Corrected_WO_Diacr_WO_Roman > const_shoda_100:
						shoda100 = '1'
						podobnost_Name_Corrected_WO_Diacr = porovnejTexty(res_Name_Corrected_WO_Diacr, vst_eventName_Corrected_WO_Diacr)
						celkem_bodu += podobnost_Name_Corrected_WO_Diacr
						if podobnost_Name_Corrected_WO_Diacr > const_shoda_100:
							shoda100 = '2'
							if zohlednitDiacr:
								podobnost_Name_Corrected_Diacr = porovnejTexty(res_Name_Corrected_Diacr, vst_eventName_Corrected_Diacr)
								celkem_bodu += podobnost_Name_Corrected_Diacr
								if podobnost_Name_Corrected_Diacr > const_shoda_100:
									shoda100 = '3'
									podobnost_Name = porovnejTexty(res_Name, vst_eventName)
									celkem_bodu += podobnost_Name
									if podobnost_Name > const_shoda_100:
										shoda100 = '4'
						elif lastNumber or lastRoman:
							podobnost_Name_Corrected_WO_DiacrCorrNumber = porovnejTexty(res_Name_Corrected_WO_Diacr, vst_eventName_Corrected_WO_Diacr_CorrNumber)
							if podobnost_Name_Corrected_WO_DiacrCorrNumber > const_shoda_100:
								celkem_bodu += podobnost_Name_Corrected_WO_DiacrCorrNumber
								shoda100 = '2'
					if shoda100 == '1':
						podobnost_Name_Corrected_Diacr_WO_Roman = porovnejTexty(res_Name_Corrected_Diacr_WO_Roman, vst_eventName_Corrected_Diacr_WO_Roman)
						celkem_bodu += podobnost_Name_Corrected_Diacr_WO_Roman
						if podobnost_Name_Corrected_Diacr_WO_Roman > const_shoda_100:
							shoda100 = '2'
					movieCSFDCache.addMovieNamesToScoreCache(nameMovies, celkem_bodu, shoda100)
				if addTVscore and TVMovies is not None:
					LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TV test - ano\n')
					for movie in TVMovies:
						if movie[0] == x[0]:
							LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TV test - x[0]: ' + x[0] + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TV test - movie[0]: ' + movie[0] + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - TV test - shoda\n')
							celkem_bodu += 1000
							TV_shoda = True
							if shoda100 == '0':
								shoda100 = '1'

				if addTVscore and TVMovies is not None and x[2] is not None:
					y_body, y_shoda = self.CompareMovieYears(x[2])
					if y_shoda:
						shoda100 += '1'
					else:
						shoda100 += '0'
					celkem_bodu += y_body
				else:
					shoda100 += '0'
				if celkem_bodu >= acceptance:
					if not res_shoda and shoda100 > '01':
						res_shoda = True
					if x[2] is not None:
						spoj = strUni(res_Name_Orig + ' ' + char2Allowchar(x[2]))
					else:
						spoj = strUni(res_Name_Orig)
					if not self.SearchDuplicity(resultlist, spoj, x[0]):
						if len(res_Name_Corrected_WO_Diacr) > 0:
							res_Name_Corrected_WO_DiacrSort = char2DiacriticSort(res_Name)
							if x[2] is not None:
								resultlist.append((spoj, x[0], res_Name_Corrected_WO_DiacrSort, res_Name_Corrected_WO_Diacr, celkem_bodu, y, shoda100, res_Name_Orig, x[3], x[2]))
							else:
								resultlist.append((spoj, x[0], res_Name_Corrected_WO_DiacrSort, res_Name_Corrected_WO_Diacr, celkem_bodu, y, shoda100, res_Name_Orig, x[3], ''))
							y += 1

			LogCSFD.WriteToFile('[CSFD] CSFDMenuPreparation - konec\n')
			return (resultlist, res_shoda, TV_shoda)

	def GetOtherMovieNamesFromDetail(self, searchresults):
		LogCSFD.WriteToFile('[CSFD] GetOtherMovieNamesFromDetail - zacatek\n')
		searchresultsAdd = []
		if searchresults is not None and len(searchresults) > 0:
			try:
				pocet = int(config.misc.CSFD.NumberOfReadMovieNameFromDetail.getValue())
			except ValueError:
				LogCSFD.WriteToFile('[CSFD] GetOtherMovieNamesFromDetail - number - chyba\n')
				pocet = 1

			stahnuto = []
			index = 0
			nacteno = 0
			while nacteno < pocet:
				if index >= len(searchresults):
					break
				pol = searchresults[index]
				link = pol[0]
				if link not in stahnuto:
					stahnuto.append(link)

					fetchurl = link
					LogCSFD.WriteToFile('[CSFD] GetOtherMovieNamesFromDetail - stahuji z url ' + Uni8(fetchurl) + '\n')

					res = csfdAndroidClient.get_json_by_uri( fetchurl )
					ParserOstCSFD.setJson( res)
					res_name = ParserOstCSFD.parserOrigMovieTitle()
					if res_name is not None:
						searchresults.append((pol[0], res_name, pol[2], pol[3]))
						searchresultsAdd.append((pol[0], res_name, pol[2], pol[3]))

					nacteno += 1
				index += 1


			ParserOstCSFD.setJson( {} )
		LogCSFD.WriteToFile('[CSFD] GetOtherMovieNamesFromDetail - konec\n')
		return (searchresults, searchresultsAdd)

	def CSFDTestingTV(self):
		TVtesting = False
		stations = ''
		for channel in self.ChannelsCSFD:
			if stations == '':
				stations += channel
			else:
				stations += '%2C' + channel

		if stations != '':
			if TVMovieCache.IsChannelInCache(stations):
				searchresults = TVMovieCache.getMoviesFromCache(stations)
				if searchresults is not None and len(searchresults) > 0:
					TVtesting = True
		return TVtesting

	def CSFDquery(self, string=''):
		LogCSFD.WriteToFile('[CSFD] CSFDquery - zacatek\n')

		def SetNotFind(textInfo='', textStatus=''):
			self.summaries.setText(textInfo + self.eventNameLocal, 10)
			self['detailslabel'].setText(textInfo + self.eventNameLocal)
			self['statusbar'].setText(textStatus)
			self['sortlabel'].setText('')
			self['key_green'].setText(_('Výběr z EPG'))
			self['key_yellow'].setText('')
			self['key_red'].setText(_('Zpět'))
			self['key_blue'].setText(_('Zadej pořad'))
			self['pagebg'].hide()
			self['pageb1'].hide()
			self['pageb3'].hide()
			self['paget1'].hide()
			self['paget3'].hide()
			self['page'].setText('')
			self['page'].hide()

		LogCSFD.WriteToFile('[CSFD] CSFDquery - hledany film3 ' + self.eventNameLocal + '\n')
#		ParserCSFD.setHTML2utf8(string)
		ParserCSFD.setJson(string)
		self.CSFDparseUser()
		self.resultlist = []
		self.SortType = int(config.misc.CSFD.Default_Sort.getValue())

		if ParserCSFD.testJson():
			if ParserCSFD.parserMoviesFound():
				if self.FindAllItems:
					LogCSFD.WriteToFile('[CSFD] CSFDquery - parsuji cely seznam vyhledanych filmu\n')
					searchresults = ParserCSFD.parserListOfMovies(0)
					searchresults, searchresultsAdd = self.GetOtherMovieNamesFromDetail(searchresults)
					self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults)
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDquery - parsuji prvni skupinu vyhledanych filmu\n')
					searchresultsOrig = ParserCSFD.parserListOfMovies(1)
					searchresults, searchresultsAdd = self.GetOtherMovieNamesFromDetail(searchresultsOrig)
					self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True)
					
					if not shoda or not TVshoda and self.CSFDTestingTV():
						LogCSFD.WriteToFile('[CSFD] CSFDquery - parsuji zbytek nazvu filmu\n')
						searchresults1 = ParserCSFD.parserListOfMovies(0)
						if searchresultsOrig != searchresults1:
							LogCSFD.WriteToFile('[CSFD] CSFDquery - seznamy jsou ruzne\n')
							searchresults1 = searchresults1 + searchresultsAdd
							self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults1, True)
							if not shoda:
								LogCSFD.WriteToFile('[CSFD] CSFDquery - seznamy jsou ruzne 1\n')
								self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults1)
						else:
							LogCSFD.WriteToFile('[CSFD] CSFDquery - seznamy jsou ruzne 2\n')
							searchresults1 = searchresults1 + searchresultsAdd
							self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults1)
				
				LogCSFD.WriteToFile('[CSFD] CSFDquery - konec upravy seznamu\n')
				self.SortTypeChange(change_s=False)
				
				if len(self.resultlist) > 0:
					LogCSFD.WriteToFile('[CSFD] CSFDquery - vyhledano vice zaznamu nez 0\n')
					self['menu'].moveToIndex(0)
					self.NacistNazevPoradu = False
					if config.misc.CSFD.Detail100.getValue() == True and self.Detail100Akce == True and self.Search100shoda() == 1:
						LogCSFD.WriteToFile('[CSFD] CSFDquery - Detail 100%\n')
						self.Detail100Exit = True
						self['menu'].moveToIndex(self.Detail100Pozice)
						self.Page = 0
						self.showDetails()
					else:
						LogCSFD.WriteToFile('[CSFD] CSFDquery - neni detail 100%\n')
						self.Detail100Exit = False
						self.Page = 1
						self.showMenu()
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDquery - Redirecttext1 - nenacteno\n')
					SetNotFind(_('Žádná shoda na CSFD pro film: '), _('Žádná shoda na CSFD.'))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDquery - Redirecttext2 - nenacteno\n')
				SetNotFind(_('Žádná shoda na CSFD pro film: '), _('Žádná shoda na CSFD.'))
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDquery -	 chyba dotazu!\n')
			SetNotFind(_('CSFD - chyba dotazu! - film: '), '')
			
		LogCSFD.WriteToFile('[CSFD] CSFDquery - konec\n')
		return

	def CSFDqueryTV(self):
		shoda = False
		if config.misc.CSFD.TVCache.getValue():
			LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - zacatek\n')
			stations = ''
			for channel in self.ChannelsCSFD:
				if stations == '':
					stations += channel
				else:
					stations += '%2C' + channel

			if stations != '':
				if not TVMovieCache.IsChannelInCache(stations):
					LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - pridavam kanal do cache\n')
					GetMoviesForTVChannels(stations, 1, 10, True)
				searchresults = TVMovieCache.getMoviesFromCache(stations)
				if searchresults is not None and len(searchresults) > 0:
					LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - cast1\n')
					self.resultlist = []
					self.SortType = int(config.misc.CSFD.Default_Sort.getValue())
					self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True, False, 90)
					if shoda:
						self.SortTypeChange(change_s=False)
						if len(self.resultlist) > 0:
							LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 1 - vyhledano vice zaznamu nez 0\n')
							self['menu'].moveToIndex(0)
							self.NacistNazevPoradu = False
							if config.misc.CSFD.Detail100.getValue() == True and self.Detail100Akce == True and self.Search100shoda() == 1:
								LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 1 - Detail 100%\n')
								self.Detail100Exit = True
								self['menu'].moveToIndex(self.Detail100Pozice)
								self.Page = 0
								self.showDetails()
							else:
								LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 1 - neni detail 100%\n')
								self.Detail100Exit = False
								self.Page = 1
								self.showMenu()
					elif self.eventNameSecond is not None and self.eventNameSecond != '':
						LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - cast2\n')
						self.resultlist = []
						self.SortType = int(config.misc.CSFD.Default_Sort.getValue())
						self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameSecond, searchresults, True, False, 90)
						if shoda:
							self.SortTypeChange(change_s=False)
							if len(self.resultlist) > 0:
								LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 2 - vyhledano vice zaznamu nez 0\n')
								self['menu'].moveToIndex(0)
								self.NacistNazevPoradu = False
								if config.misc.CSFD.Detail100.getValue() == True and self.Detail100Akce == True and self.Search100shoda() == 1:
									LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 2 - Detail 100%\n')
									self.Detail100Exit = True
									self['menu'].moveToIndex(self.Detail100Pozice)
									self.Page = 0
									self.showDetails()
								else:
									LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - 2 - neni detail 100%\n')
									self.Detail100Exit = False
									self.Page = 1
									self.showMenu()
			LogCSFD.WriteToFile('[CSFD] CSFDqueryTV - konec\n')
		return shoda

	def CSFDparseName(self):
		LogCSFD.WriteToFile('[CSFD] ParseName -	 zacatek\n')
		self.PageSpec = 1
		self.querySpecAkce = 'UserComments'
		Titeltext = '???'
		self.NacistNazevPoradu = False
		LogCSFD.WriteToFile('[CSFD] ParseName - rating1\n')
		ccrate = GetItemColourRateC(ParserCSFD.parserRatingStars())
		LogCSFD.WriteToFile('[CSFD] ParseName - rating2: ' + ccrate + '\n')
		Titel = ParserCSFD.parserMovieTitleInclYear()
		if Titel is not None and Titel != '':
			Titeltext = Titel
			LogCSFD.WriteToFile('[CSFD] ParseName - Titeltext\n')
			LogCSFD.WriteToFile(Titeltext)
			LogCSFD.WriteToFile('\n')
			if len(self.resultlist) == 1:
				if self.resultlist[0][6] == '91':
					LogCSFD.WriteToFile('[CSFD] ParseName - OK\n')
					pol = self.resultlist[0]
					self.resultlist = []
					searchresults = []
					filmdate = ''
					res = ParserCSFD.parserGetYears(Titeltext[-6:])
					if res is not None and len(res) > 0:
						LogCSFD.WriteToFile('[CSFD] ParseName - filmdate - ')
						filmdate = '(' + res[0] + ')'
						LogCSFD.WriteToFile(filmdate + '\n')
					LogCSFD.WriteToFile('[CSFD] ParseName - Jmeno\n')
					jmeno = ParserCSFD.parserMovieTitle()
					if jmeno is not None and jmeno != '':
						searchresults.append((pol[1], jmeno, filmdate, ccrate))
					LogCSFD.WriteToFile('[CSFD] ParseName - Ostatni jmena\n')
					ostjmenaresult = ParserCSFD.parserOtherMovieTitleWOCountry()
					if ostjmenaresult is not None:
						for x in ostjmenaresult:
							if x != '':
								searchresults.append((pol[1], x, filmdate, ccrate))

					self.resultlist, shoda, TVshoda = self.CSFDMenuPreparation(self.eventNameLocal, searchresults, True)
					self.Detail100Pozice = 0
					self.ItemsLoad()
					self['menu'].moveToIndex(0)
		LogCSFD.WriteToFile('[CSFD] ParseName - konec\n')
		return

	def CSFDparseUser(self):
		LogCSFD.WriteToFile('[CSFD] parseUser - zacatek\n')
		resultText = csfdAndroidClient.get_logged_user()[0]
		if resultText is not None and resultText != '':
			LogCSFD.WriteToFile('[CSFD] parseUser - Logged User: ' + Uni8(resultText) + '\n')
			self.LoggedUser = resultText
			sss = _('Filmová databáze CSFD') + '  -  ' + _('Verze: ') + ' ' + strUni(self.versionCSFD) + '  -  ' + _('Přihlášen jako:') + ' ' + strUni(self.LoggedUser)
			self.setTitle(sss)
		else:
			if config.misc.CSFD.LoginToCSFD.getValue():
				CreateCSFDAndroidClient()
			self.LoggedUser = ''
			sss = _('Filmová databáze CSFD') + '  -  ' + _('Verze: ') + ' ' + strUni(self.versionCSFD)
			self.setTitle(sss)
		LogCSFD.WriteToFile('[CSFD] parseUser - konec\n')
		return

	def CSFDParseMainPart(self):
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - Nazev\n')
		Titeltext = '???'
		PridejText = ''
		
		resultText = ParserCSFD.parserMovieTitleInclYear()
		if resultText is not None and resultText is not '':
			Titeltext = char2Allowchar(resultText)
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				if len(Titeltext) > 25:
					PridejText = Titeltext
					Titeltext = Titeltext[0:25] + ' ...'
			elif len(Titeltext) > 60:
				PridejText = Titeltext
				Titeltext = Titeltext[0:60] + ' ...'
				
		self['titellabel'].setText(strUni(char2Allowchar(Titeltext)))
		self['sortlabel'].setText('')
		
		Detailstext = ''
		if PridejText != '':
			jme = PridejText.split(' / ', 1)
			Detailstext = strUni(char2Allowchar(NameMovieCorrectionExtensions(jme[0].strip()))) + '\n'
			if len(jme) > 1:
				Detailstext += strUni(char2Allowchar(NameMovieCorrectionExtensions(jme[1].strip()))) + '\n'
		
		ss = self.selectedMenuRow[7].strip()
		if ss is not None and ss is not '':
			jme = ss.split(' / ', 1)
			Detailstext = strUni(char2Allowchar(NameMovieCorrectionExtensions(jme[0].strip()))) + '\n'
			if len(jme) > 1:
				Detailstext += strUni(char2Allowchar(NameMovieCorrectionExtensions(jme[1].strip()))) + '\n'
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - Jmeno\n')
		
		resultText = ParserCSFD.parserMovieTitle()
		if resultText is not None and resultText is not '':
			self.ActName = char2Allowchar(NameMovieCorrectionExtensions(resultText))
			Detailstext += strUni(resultText + '\n')
		if self.ActName == '':
			ss = Titeltext.split(' / ', 1)
			self.ActName = char2Allowchar(ss[0].strip())
			
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - ActName: ' + self.ActName + '\n')
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - Jmeno serialu v epizode\n')
		resultText = ParserCSFD.parserSeriesNameInEpisode()
		if resultText is not None and resultText is not '':
			Detailstext += strUni(char2Allowchar(resultText))
			
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - Ostatni jmena\n')
		
		resultText = ParserCSFD.parserOtherMovieTitle()
		if resultText is not None and resultText is not '':
			Detailstext += strUni(char2Allowchar(resultText))
			
		Detailstext = OdstranitDuplicityRadku(Detailstext)
		textCol1 = self['detailslabel'].AddRowIntoText(Detailstext, '')
		textCol = Detailstext
		Detailstext = textCol1
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - typ poradu\n')
		resultText = ParserCSFD.parserTypeOfMovie()
		if resultText is not None and resultText is not '':
			Detailstext += resultText + '\n'
			
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - zanr\n')
		resultText = ParserCSFD.parserGenre()
		if resultText is not None and resultText is not '':
			Detailstext += resultText + '\n'
			self.callbackGenre = resultText
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - origin\n')
		resultText = ParserCSFD.parserOrigin()
		if resultText is not None and resultText is not '':
			delim = ', '
			Detailstext += resultText
		else:
			delim = ''

		LogCSFD.WriteToFile('[CSFD] ParseMainPart - length\n')
		resultText = ParserCSFD.parserMovieDuration()
		if resultText is not None and resultText is not '':
			Detailstext += delim + resultText + '\n'
		elif delim != '':
			Detailstext += '\n'
			
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - zebricky\n')
		resultText = ParserCSFD.parserCSFDRankings()
		if resultText is not None and resultText is not '':
			Detailstext += resultText
			
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - info, kde film bezi\n')
		resultText = ParserCSFD.parserWherePlaying()
		if resultText is not None and resultText is not '':
			Detailstext += resultText + '\n'
			
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - vlastni hodnoceni\n')
		resultText = ParserCSFD.parserOwnRating()[0]
		if resultText is not None and resultText is not '':
			ss = ParserCSFD.parserDateOwnRating()
			if ss is not None and ss is not '':
				resultText += '	 (' + ss + ')'
			coltextpart = _('Vlastní hodnocení: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - soukroma poznamka\n')
#		resultText = ParserCSFD.parserPrivateComment()
		resultText = None
		if resultText is not None and resultText is not '':
			coltextpart = _('Soukromá poznámka: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - rezije\n')
		resultText = ParserCSFD.parserDirector()
		if resultText is not None and resultText is not '':
			coltextpart = _('Režie: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - predloha\n')
		resultText = ParserCSFD.parserDraft()
		if resultText is not None and resultText is not '':
			coltextpart = _('Předloha: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - scenar\n')
		resultText = ParserCSFD.parserScenario()
		if resultText is not None and resultText is not '':
			coltextpart = _('Scénář: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - kamera\n')
		resultText = ParserCSFD.parserCamera()
		if resultText is not None and resultText is not '':
			coltextpart = _('Kamera: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - hudba\n')
		resultText = ParserCSFD.parserMusic()
		if resultText is not None and resultText is not '':
			coltextpart = _('Hudba: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - produkce\n')
		resultText = ParserCSFD.parserProduction()
		if resultText is not None and resultText is not '':
			coltextpart = _('Produkce: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - strih\n')
		resultText = ParserCSFD.parserCutting()
		if resultText is not None and resultText is not '':
			coltextpart = _('Střih: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - zvuk\n')
		resultText = ParserCSFD.parserSound()
		if resultText is not None and resultText is not '':
			coltextpart = _('Zvuk: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - scenografie\n')
		resultText = ParserCSFD.parserScenography()
		if resultText is not None and resultText is not '':
			coltextpart = _('Scénografie: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - masky\n')
		resultText = ParserCSFD.parserMakeUp()
		if resultText is not None and resultText is not '':
			coltextpart = _('Masky: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - kostymy\n')
		resultText = ParserCSFD.parserCostumes()
		if resultText is not None and resultText is not '':
			coltextpart = _('Kostýmy: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - hraji\n')
		resultText = ParserCSFD.parserCasting()
		if resultText is not None and resultText is not '':
			coltextpart = _('Hrají: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		textCol = self['detailslabel'].AddRowIntoText(Detailstext, textCol)
		
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - tagy\n')
#		resultText = ParserCSFD.parserTags()
		resultText = None
		if resultText is not None and resultText is not '':
			coltextpart = _('Tagy: ')
			textCol = textCol + coltextpart + '\n'
			coltextspace = self['detailslabel'].CalculateSizeInSpace(coltextpart)[0]
			Detailstext += coltextspace
			Detailstext += resultText + '\n'
		
		Detailstext = char2Allowchar(Detailstext)
		self.callbackData += Detailstext
		
		self['detailslabel'].setText(strUni(Detailstext))
		self['detailslabel'].setTextCol(textCol)
		LogCSFD.WriteToFile('[CSFD] ParseMainPart - konec\n')
		return Titeltext

	def CSFDparse(self):
		LogCSFD.WriteToFile('[CSFD] Parse - zacatek\n')
		self['key_red'].setText('')
		self['key_green'].setText('')
		self['key_blue'].setText('')
		self['key_yellow'].setText('')
		self['pagebg'].hide()
		self['pageb1'].hide()
		self['pageb3'].hide()
		self['paget1'].hide()
		self['paget3'].hide()
		self['page'].setText('')
		self['page'].hide()
		self.Page = 1
		self.PageSpec = 1
		self.FunctionExists = []
		self.querySpecAkce = 'UserComments'
		self.callbackData = ''
		self.callbackGenre = ''
		self.CSFDratingUsers = ''
		self.VideoDwnlIsNotStarted = True
		self.VideoIsNotFullyRead = True
		self.PosterIsNotFullyRead = True
		self.GalleryIsNotFullyRead = True
		self['statusbar'].setText(_('CSFD detaily se načítají ...'))
		self.PosterSlideList = []
		self.PosterCountPix = 0
		self.PosterSlideStop = True
		self.PosterActIdx = 0
		self.GallerySlideList = []
		self.GalleryCountPix = 0
		self.GallerySlideStop = True
		self.GalleryActIdx = 0
		self.PosterBasicSlideList = []
		self.PosterBasicCountPixAllP = -1
		self.PosterBasicCountPixAllG = -1
		self.PosterBasicCountPix = 0
		self.PosterBasicSlideStop = True
		self.PosterBasicActIdx = 0
		self.VideoSlideList = []
		self.VideoCountPix = 0
		self.VideoActIdx = 0
		self.KeyPressLong = False
		self.KeyFlag = ''
		self.ActName = ''
		sc = AVSwitch().getFramebufferScale()
		self.picload.setPara((self['poster'].instance.size().width(), self['poster'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		self.posterload.setPara((self['photolabel'].instance.size().width(), self['photolabel'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		self.galleryload.setPara((self['photolabel'].instance.size().width(), self['photolabel'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		self.videoload.setPara((self['photolabel'].instance.size().width(), self['photolabel'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		LogCSFD.WriteToFile('[CSFD] Parse - Functions\n')
		self.FunctionExists = ParserCSFD.parserFunctionExists()
		if 'video' in self.FunctionExists:
			self.VideoIsNotFullyRead = False
		adTime = 0
		LogCSFD.WriteToFile('[CSFD] Parse - Existuji fotky v galerii a postery\n')
		if 'postery' in self.FunctionExists and 'galerie' in self.FunctionExists:
			filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')
			self.paintPosterBasicPixmap(filename)
			LogCSFD.WriteToFile('[CSFD] Parse - Existuji fotky v galerii a postery - NE\n')
		else:
			self['poster'].instance.setPixmap(gPixmapPtr())
			if 'postery' not in self.FunctionExists:
				LogCSFD.WriteToFile('[CSFD] Parse - Existuji postery - ANO\n')
				adTime += 20
				pocetPaG = ParserCSFD.parserPostersNumber()
				if pocetPaG is not None:
					LogCSFD.WriteToFile('[CSFD] Parse - pocet posteru: ' + str(pocetPaG) + '\n')
					self.PosterBasicCountPixAllP = pocetPaG
				else:
					self.PosterBasicCountPixAllP = 0
				self.CSFDPosterBasicStart()
				self.PosterDownloadTimer.start(adTime, True)
			else:
				LogCSFD.WriteToFile('[CSFD] Parse - Existuji postery - NE\n')
				self.PosterBasicCountPixAllP = 0
				self.PosterIsNotFullyRead = False

			if 'galerie' not in self.FunctionExists:
				LogCSFD.WriteToFile('[CSFD] Parse - Existuji fotky v galerii - ANO\n')
				if adTime > 0:
					adTime += 500
				else:
					adTime += 20
				self.GalleryDownloadTimer.start(adTime, True)
			else:
				LogCSFD.WriteToFile('[CSFD] Parse - Existuji fotky v galerii - NE\n')
				self.PosterBasicCountPixAllG = 0
				self.GalleryIsNotFullyRead = False
		if (config.misc.CSFD.AutomaticVersionCheck.getValue() or config.misc.CSFD.AutomaticBetaVersionCheck.getValue()) and self.IsTimeForNewVersionCheck():
			self.NewVersionTimer.start(10000, True)
		self['statusbar'].setText(_('CSFD detaily se načítají ...'))
		self.CSFDparseUser()
		Titeltext = self.CSFDParseMainPart()
		LogCSFD.WriteToFile('[CSFD] Parse - obsah\n')
		Obsahtext = ParserCSFD.parserContent()
		if Obsahtext != '':
			LogCSFD.WriteToFile('[CSFD] Parse - obsah1: ' + Obsahtext + '\n')
			Obsahtext = char2Allowchar(Obsahtext)
			LogCSFD.WriteToFile('[CSFD] Parse - obsah2: ' + Obsahtext + '\n')
			coltext = _('Obsah: ')
			coltextspace = self['contentlabel'].CalculateSizeInSpace(coltext)[0]
			coltextspace = Uni8(coltextspace)
			Obsahtext = coltextspace + Obsahtext + '\n'
			if self.EPG != '' and self.selectedMenuRow is not None:
				if self.selectedMenuRow[6] >= '10':
					Obsahtext += ' \n'
					coltext1 = _('Info z EPG: ')
					coltextspace = self['contentlabel'].CalculateSizeInSpace(coltext1)[0]
					coltextspace = Uni8(coltextspace)
					coltext = self['contentlabel'].AddRowIntoText(strUni(Obsahtext), coltext)
					coltext += coltext1
					Obsahtext += coltextspace + self.EPG
			Obsahtext = strUni(Obsahtext)
			self['contentlabel'].setTextCol(coltext)
			self.callbackData += Uni8(Obsahtext)
		elif self.EPG != '' and self.selectedMenuRow is not None:
			if self.selectedMenuRow[6] >= '10':
				coltext = _('Info z EPG: ')
				coltextspace = self['contentlabel'].CalculateSizeInSpace(coltext)[0]
				coltextspace = Uni8(coltextspace)
				Obsahtext = coltextspace + self.EPG
				Obsahtext = strUni(Obsahtext)
				coltext += '\n'
				self['contentlabel'].setTextCol(coltext)
		else:
			LogCSFD.WriteToFile('[CSFD] Parse - neni obsah\n')
			self['contentlabel'].setTextCol(' ')
			Obsahtext = ' '
		self['contentlabel'].setText(Obsahtext)
		LogCSFD.WriteToFile('[CSFD] Parse - imdb link\n')
		self.IMDBpath = ParserCSFD.parserIMDBlink()
		if self.IMDBpath != '':
			self.LoadIMDBTimer.start(150, True)
		LogCSFD.WriteToFile('[CSFD] Parse - pocet hodnoceni\n')
		pocet_hodnoceni = ParserCSFD.parserRatingNumber()
		if pocet_hodnoceni is not None:
			self.CSFDratingUsers = '(' + intWithSeparator(pocet_hodnoceni) + ')'
		else:
			self.CSFDratingUsers = ''
		if config.misc.CSFD.ShowLine.getValue():
			self['line'].show()
		self['photolabel'].instance.setPixmap(gPixmapPtr())
		self['photolabel'].hide()
		self['playbutton'].hide()
		self['extralabel'].hide()
		self.querySpecAkce = 'Nothing'
		self['extralabel'].hide()
		LogCSFD.WriteToFile('[CSFD] Parse - rating\n')
		self.ratingstars = ParserCSFD.parserRatingStars()
		if self.ratingstars >= 0:
			self.ratingtext = _('CSFD:') + ' ' + str(self.ratingstars) + '% ' + self.CSFDratingUsers
		else:
			self.ratingtext = _('CSFD:') + ' ' + _('žádné hodnocení')
		self.refreshRating()
		if self.ratingstars >= 0:
			if config.misc.CSFD.Design.getValue() == '0':
				if self.ratingstars >= 70:
					self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_100))
					self['detailslabel'].SetColColor(CSFDratingColor_100)
					self['contentlabel'].SetColColor(CSFDratingColor_100)
					self['extralabel'].SetColColor(CSFDratingColor_100)
				elif self.ratingstars >= 30:
					self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_50))
					self['detailslabel'].SetColColor(CSFDratingColor_50)
					self['contentlabel'].SetColColor(CSFDratingColor_50)
					self['extralabel'].SetColColor(CSFDratingColor_50)
				elif self.ratingstars >= 0:
					self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_0))
					self['detailslabel'].SetColColor(CSFDratingColor_0)
					self['contentlabel'].SetColColor(CSFDratingColor_0)
					self['extralabel'].SetColColor(CSFDratingColor_0)
				else:
					self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_Nothing))
					self['detailslabel'].SetColColor(CSFDratingColor_Nothing)
					self['contentlabel'].SetColColor(CSFDratingColor_Nothing)
					self['extralabel'].SetColColor(CSFDratingColor_Nothing)
		else:
			self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_Nothing))
			self['detailslabel'].SetColColor(CSFDratingColor_Nothing)
			self['contentlabel'].SetColColor(CSFDratingColor_Nothing)
			self['extralabel'].SetColColor(CSFDratingColor_Nothing)
		self['extralabel'].SetHeadColor(CSFDColor_Titel)
		if config.misc.CSFD.Design.getValue() == '1':
			self['titellabel'].instance.setForegroundColor(gRGB(CSFDColor_Titel))
			self['detailslabel'].SetColColor(CSFDratingColor_Nothing)
			self['contentlabel'].SetColColor(CSFDratingColor_Nothing)
			self['extralabel'].SetColColor(CSFDratingColor_Nothing)
			self['extralabel'].SetHeadColor(CSFDratingColor_Nothing)
		elif config.misc.CSFD.Design.getValue() == '2':
			self['titellabel'].instance.setForegroundColor(gRGB(CSFDratingColor_HighlightKeyWords))
			self['detailslabel'].SetColColor(CSFDratingColor_HighlightKeyWords)
			self['contentlabel'].SetColColor(CSFDratingColor_HighlightKeyWords)
			self['extralabel'].SetColColor(CSFDratingColor_HighlightKeyWords)
			self['extralabel'].SetHeadColor(CSFDratingColor_HighlightKeyWords)
		LogCSFD.WriteToFile('[CSFD] Parse - titulok: ' + Titeltext + '\n')
		self.summaries.setText(strUni(char2Allowchar(Titeltext)), GetItemColourRateN(self.ratingstars))
		self['statusbar'].setText(_('Autor pluginu: ') + 'petrkl12@tvplugins.cz')
		self['key_red'].setText(_('Zpět'))
		self['key_green'].setText(_('Menu pořadů'))
		self['key_yellow'].setText(_('Detaily'))
		self['key_blue'].setText(_('Komentáře'))
		if config.misc.CSFD.PosterBasic.getValue():
			self.CSFDPosterBasicSlideShowStart()
		LogCSFD.WriteToFile('[CSFD] Parse - konec\n')
		return

	def CSFDshowSpec(self):
		LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - zacatek\n')
		
		movie_id = self.linkGlobal[7:]
		
		self['statusbar'].setText('')
		if self.querySpecAkce == 'UserGallery' or self.querySpecAkce == 'UserPoster' or self.querySpecAkce == 'UserVideo':
			self.CSFDquerySpec('')
		else:
			if CSFDGlobalVar.getCSFDDesktopWidth() > 1250:
				self['statusbar'].setText(_('CSFD - stahování dalších informací probíhá ...'))
				self['statusbar'].show()
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - nadpis NE\n')
				self['statusbar'].setText('')
			sss = str(self.PageSpec)
			if self.querySpecAkce == 'UserComments':
#				self.linkComment obsahuje sposob ako zoradit komentare
				self.linkSpec = '#movie_comments#' +  movie_id
			elif self.querySpecAkce == 'UserExtReviews':
				self.linkSpec = 'recenze/strana-%s/' % sss
			elif self.querySpecAkce == 'UserPremiery':
#				self.linkSpec = self.linkComment
				self.linkSpec = '#movie_premiere#'
			elif self.querySpecAkce == 'UserDiscussion':
				self.linkSpec = 'diskuze/strana-%s/' % sss
			elif self.querySpecAkce == 'UserInteresting':
				self.linkSpec = '#movie_trivia#' +  movie_id
			elif self.querySpecAkce == 'UserAwards':
				self.linkSpec = 'oceneni/strana-%s/' % sss
			elif self.querySpecAkce == 'UserReviews':
				self.linkSpec = const_quick_page + '?expandUserList=1&ratings-page=%s' % sss
			elif self.querySpecAkce == 'UserFans':
				self.linkSpec = const_quick_page + '?expandUserList=1&fanclub-page=%s' % sss
			fetchurl = CSFDGlobalVar.getHTTP() + const_csfd_http_film + self.linkGlobal + self.linkSpec
			LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - stahuji z url ' + fetchurl + '\n')
			LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - linkGlobal ' + self.linkGlobal + '\n')
			LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - linkSpec ' + self.linkSpec + '\n')
			
#			page = requestCSFD(fetchurl, headers=std_headers_UL2, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
#			CSFDGlobalVar.setParalelDownload(self.CSFDquerySpec, page)
#			self.DownloadTimer.start(10, True)

			if self.linkSpec.startswith('#'):
				page = csfdAndroidClient.get_json_by_uri(self.linkSpec, self.PageSpec )
				self.CSFDquerySpec(page)
		LogCSFD.WriteToFile('[CSFD] CSFDshowSpec - konec\n')

	def CSFDquerySpec(self, string):
		LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - zacatek\n')
		try:
			if self.querySpecAkce == 'UserGallery':
				ok = True
		except AttributeError:
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - ukonceni pluginu\n', 5)
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - konec\n')
			return

		if self.querySpecAkce == 'UserGallery':
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - Galerie\n')
			sss = str(self.GalleryActIdx + 1)
			if not self['statusbar'].instance.isVisible():
				self['statusbar'].show()
			self['page'].setText(_('Galerie č.%s' % sss))
			if self.GalleryCountPix > 0:
				if self['extralabel'].instance.isVisible():
					self['extralabel'].hide()
				if self['playbutton'].instance.isVisible():
					self['playbutton'].hide()
				if not self['photolabel'].instance.isVisible():
					self['photolabel'].show()
				self.CSFDGalleryShow()
			else:
				if not self['extralabel'].instance.isVisible():
					self['extralabel'].show()
				if self['playbutton'].instance.isVisible():
					self['playbutton'].hide()
				if self['photolabel'].instance.isVisible():
					self['photolabel'].instance.setPixmap(gPixmapPtr())
					self['photolabel'].hide()
				self.CSFDGalleryShowNothing()
		elif self.querySpecAkce == 'UserPoster':
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - Poster\n')
			sss = str(self.PosterActIdx + 1)
			if not self['statusbar'].instance.isVisible():
				self['statusbar'].show()
			self['page'].setText(_('Poster č.%s' % sss))
			if self.PosterCountPix > 0:
				if self['extralabel'].instance.isVisible():
					self['extralabel'].hide()
				if self['playbutton'].instance.isVisible():
					self['playbutton'].hide()
				if not self['photolabel'].instance.isVisible():
					self['photolabel'].show()
				self.CSFDPosterShow()
			else:
				if not self['extralabel'].instance.isVisible():
					self['extralabel'].show()
				if self['playbutton'].instance.isVisible():
					self['playbutton'].hide()
				if self['photolabel'].instance.isVisible():
					self['photolabel'].instance.setPixmap(gPixmapPtr())
					self['photolabel'].hide()
				self.CSFDPosterShowNothing()
		elif self.querySpecAkce == 'UserVideo':
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - Video\n')
			if self.VideoDwnlIsNotStarted:
				self.CSFDAllVideoDownload()
			sss = str(self.VideoActIdx + 1)
			if not self['statusbar'].instance.isVisible():
				self['statusbar'].show()
			self['page'].setText(_('Video č.%s' % sss))
			if self.VideoCountPix > 0:
				if self['extralabel'].instance.isVisible():
					self['extralabel'].hide()
				if not self['playbutton'].instance.isVisible():
					self['playbutton'].show()
				if not self['photolabel'].instance.isVisible():
					self['photolabel'].show()
				self.CSFDVideoShow()
			else:
				if not self['extralabel'].instance.isVisible():
					self['extralabel'].show()
				if self['playbutton'].instance.isVisible():
					self['playbutton'].hide()
				if self['photolabel'].instance.isVisible():
					self['photolabel'].instance.setPixmap(gPixmapPtr())
					self['photolabel'].hide()
				self.CSFDVideoShowNothing()
		else:
			if not self['extralabel'].instance.isVisible():
				self['extralabel'].show()
			if self['playbutton'].instance.isVisible():
				self['playbutton'].hide()
			if self['photolabel'].instance.isVisible():
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				self['photolabel'].hide()
			if not self['statusbar'].instance.isVisible():
				self['statusbar'].show()
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - html2utf8\n')
#			ParserCSFD.setHTML2utf8(string)
			self.CSFDparseUser()
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - pred parse' + '\n')
			if CSFDGlobalVar.getCSFDDesktopWidth() > 1250:
				self['statusbar'].setText(_('CSFD stahování dalších informací dokončeno'))
			else:
				self['statusbar'].setText('')
			LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - querySpecAkce - ' + self.querySpecAkce + '\n')
			if self.querySpecAkce == 'UserComments':
				self.CSFDParseUserComments( string )
			elif self.querySpecAkce == 'UserExtReviews':
				self.CSFDParseUserExtReviews()
			elif self.querySpecAkce == 'UserPremiery':
				self.CSFDParseUserPremiery()
			elif self.querySpecAkce == 'UserDiscussion':
				self.CSFDParseUserDiscussion()
			elif self.querySpecAkce == 'UserInteresting':
				self.CSFDParseUserInteresting( string )
			elif self.querySpecAkce == 'UserAwards':
				self.CSFDParseUserAwards()
			elif self.querySpecAkce == 'UserReviews':
				self.CSFDParseUserReviews()
			elif self.querySpecAkce == 'UserFans':
				self.CSFDParseUserFans()
			sss = str(self.PageSpec)
			self['page'].setText(_('Strana č.%s' % sss))
		LogCSFD.WriteToFile('[CSFD] CSFDquerySpec - konec\n')

	def CSFDParseUserComments(self, data ):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserComments - zacatek\n')
		Extratext = ''
		ExtratextCol = ''
		coltextUzivatel = _('Uživatel: ')
		coltextspaceUzivatel = self['extralabel'].CalculateSizeInSpace(coltextUzivatel)[0]
		coltextHodnoceni = '\t ' + _('Hodnocení:')
		coltextspaceHodnoceni = self['extralabel'].CalculateSizeInSpace(coltextHodnoceni)[0]
		extraresult = ParserCSFD.parserUserComments( data )
		if extraresult is not None:
			for x in extraresult:
				uzivtext = self['extralabel'].CalculateSizeAddSpaceDiff(x[0], 'AAAAAAAAAAAA')
				
				Extratext += coltextspaceUzivatel + uzivtext + coltextspaceHodnoceni + '\t' + x[1] + '	 ' + x[2] + ' \n' + strUni(char2Allowchar(x[3] + '\n' + '\n'))
				ExtratextCol += coltextUzivatel + self['extralabel'].CalculateSizeInSpaceSimple(uzivtext) + coltextHodnoceni + ' \n'
				ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)

#		if Extratext == '':
#			if self.PageSpec > 1:
#				Extratext = '\n' + _('Žádné další komentáře v databázi.')
#			else:
#				Extratext = '\n' + _('Žádné komentáře v databázi.')
#		if self.linkComment == 'podle-datetime/':
#			cc = _('seřazené od nejnovějších po nejstarší')
#		elif self.linkComment == 'podle-rating/':
#			cc = _('seřazené podle hodnocení')
#		else:
#			cc = _('seřazené podle počtu bodů uživatele')
#		Extradopln = _('Komentáře uživatelů ')
#		pocet = ParserCSFD.parserUserCommentsNumber()
#		if pocet is not None:
#			Extradopln += cc + ' (' + _('počet komentářů:') + ' ' + intWithSeparator(pocet) + ')\n'
#		else:
#			Extradopln += cc + ' :\n'
#		Extradopln += _('(změnit třídění komentářů můžete pomocí klávesy 2)') + '\n\n'
		pocet = ParserCSFD.parserUserCommentsNumber()
		if pocet is not None:
			Extradopln = _('Celkový počet komentářů:') + ' ' + intWithSeparator(pocet) + '\n\n'
		else:
			Extradopln = ''
			
		textFree = self['extralabel'].AddRowIntoText(Extradopln, '')
		self['extralabel'].setTextHead(Extradopln)
		Extratext = textFree + Extratext
		ExtratextCol = textFree + ExtratextCol
		self['extralabel'].setTextCol(ExtratextCol)
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserComments - konec\n')
		return

	def CSFDParseUserExtReviews(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserExtReviews - zacatek\n')
		Extratext = ''
		ExtratextCol = ''
		coltextUzivatel = _('Recenze od: ')
		coltextspaceUzivatel = self['extralabel'].CalculateSizeInSpace(coltextUzivatel)[0]
		coltextHodnoceni = _('Hodnocení: ')
		coltextspaceHodnoceni = self['extralabel'].CalculateSizeInSpace(coltextHodnoceni)[0]
		if self.PageSpec == 1:
			extraresult = ParserCSFD.parserUserExtReviews()
			if extraresult is not None:
				for x in extraresult:
					Extratext += coltextspaceUzivatel + x[0] + ' \n' + coltextspaceHodnoceni + x[1] + ' \n' + x[2] + '\n\n'
					ExtratextCol += coltextUzivatel + self['extralabel'].CalculateSizeInSpaceSimple(x[0]) + ' \n' + coltextHodnoceni + ' \n'
					ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)

		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádné další externí recenze v databázi.')
			else:
				Extratext = '\n' + _('Žádné externí recenze v databázi.')
		Extradopln = _('Externí recenze ')
		pocet = ParserCSFD.parserUserExtReviewsNumber()
		if pocet is not None:
			Extradopln += ' (' + _('počet externích recenzí:') + ' ' + intWithSeparator(pocet) + ')\n\n'
		else:
			Extradopln += ' :\n\n'
		textFree = self['extralabel'].AddRowIntoText(Extradopln, '')
		self['extralabel'].setTextHead(Extradopln)
		Extratext = textFree + Extratext
		ExtratextCol = textFree + ExtratextCol
		self['extralabel'].setTextCol(ExtratextCol)
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserExtReviews - konec\n')
		return

	def CSFDParseUserDiscussion(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserDiscussion - zacatek\n')
		Extratext = ''
		ExtratextCol = ''
		coltextUzivatel = _('Uživatel: ')
		coltextspaceUzivatel = self['extralabel'].CalculateSizeInSpace(coltextUzivatel)[0]
		coltextUzivatel += '\n'
		extraresult = ParserCSFD.parserUserDiscussion()
		if extraresult is not None:
			for x in extraresult:
				Extratext += coltextspaceUzivatel + x[1] + '  ' + x[0] + '\n' + strUni(char2Allowchar(x[2] + '\n' + '\n'))
				ExtratextCol += coltextUzivatel
				ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)

		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádné další diskuzní příspěvky v databázi.')
			else:
				Extratext = '\n' + _('Žádné diskuzní příspěvky v databázi.')
		Extradopln = _('Diskuze ')
		pocet = ParserCSFD.parserUserDiscussionNumber()
		if pocet is not None:
			Extradopln += '(' + _('počet diskuzních příspěvků:') + ' ' + intWithSeparator(pocet) + ')' + '\n\n'
		else:
			Extradopln += ':\n\n'
		textFree = self['extralabel'].AddRowIntoText(Extradopln, '')
		self['extralabel'].setTextHead(Extradopln)
		Extratext = textFree + Extratext
		ExtratextCol = textFree + ExtratextCol
		self['extralabel'].setTextCol(ExtratextCol)
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserDiscussion - konec\n')
		return

	def CSFDParseUserInteresting(self, data):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserInteresting - zacatek\n')
		Extratext = ''
		ExtratextCol = ''
		coltextUzivatel = _('Uživatel: ')
		coltextspaceUzivatel = self['extralabel'].CalculateSizeInSpace(coltextUzivatel)[0]
		coltextUzivatel += '\n'
		extraresult = ParserCSFD.parserInterest( data )
		if extraresult is not None:
			for x in extraresult:
				Extratext += coltextspaceUzivatel + x[1] + '\n' + strUni(char2Allowchar(x[0] + '\n' + '\n'))
				ExtratextCol += coltextUzivatel
				ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)

		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádné další zajímavosti pro tento typ.')
			else:
				Extratext = '\n' + _('Žádné zajímavosti v databázi.')
		urlInt, nameInt, pocInt_s = ParserCSFD.parserInterestSelectedTypeAndNumber()
		try:
			pocInt = int(pocInt_s)
		except ValueError:
			pocInt = 0
			LogCSFD.WriteToFile('[CSFD] CSFDParseUserInteresting - chyba - int\n')

		Extradopln = _('Zajímavosti ')
		pocet = ParserCSFD.parserInterestNumber()
		if pocet is not None:
			Extradopln += '(' + _('celkový počet zajímavostí:') + ' ' + intWithSeparator(pocet) + ')'
			if urlInt is not None:
				Extradopln += '	 -	' + _('typ') + ' ' + nameInt + ' (' + intWithSeparator(pocInt) + ')'
			Extradopln += '\n'
		else:
			Extradopln += ':\n'
#		Extradopln += _('(změnit typ zajímavostí můžete pomocí klávesy 2)') + '\n\n'
		Extradopln += '\n'
		textFree = self['extralabel'].AddRowIntoText(Extradopln, '')
		self['extralabel'].setTextHead(Extradopln)
		Extratext = textFree + Extratext
		ExtratextCol = textFree + ExtratextCol
		self['extralabel'].setTextCol(ExtratextCol)
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserInteresting - konec\n')
		return

	def CSFDParseUserAwards(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserAwards - zacatek\n')
		Extratext = ''
		ExtratextCol = ''
		ExtratextHead = _('Ocenění') + ' :' + '\n\n'
		typ_oceneni = 'blablab'
		if self.PageSpec == 1:
			extraresult = ParserCSFD.parserAwards()
			if extraresult is not None:
				Extratext = self['extralabel'].AddRowIntoText(ExtratextHead, Extratext)
				ExtratextCol = self['extralabel'].AddRowIntoText(ExtratextHead, ExtratextCol)
				for x in extraresult:
					if typ_oceneni != x[0]:
						ExtratextHead = self['extralabel'].AddRowIntoText(Extratext, ExtratextHead)
						ExtratextHead += x[0] + '\n'
						typ_oceneni = x[0]
						Extratext = self['extralabel'].AddRowIntoText(ExtratextHead, Extratext)
						ExtratextCol = self['extralabel'].AddRowIntoText(ExtratextHead, ExtratextCol)
					if x[1] == 'winner':
						ExtratextCol += _('Vítěz:') + ' ' + x[2] + ' \n'
						Extratext = self['extralabel'].AddRowIntoText(ExtratextCol, Extratext)
					elif x[1] == 'nominated':
						Extratext += _('Nominován:') + ' ' + x[2] + ' \n'
						ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)
					else:
						Extratext += x[1] + ' ' + x[2] + ' \n'
						ExtratextCol = self['extralabel'].AddRowIntoText(Extratext, ExtratextCol)

		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n\n\n' + _('Žádné další ocenění v databázi.')
			else:
				Extratext = '\n\n\n' + _('Žádná ocenění v databázi.')
		elif self.PageSpec > 1:
			Extratext = '\n\n\n' + _('Žádné další ocenění v databázi.')
		self['extralabel'].setTextHead(ExtratextHead)
		self['extralabel'].setTextCol(ExtratextCol)
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserAwards - konec\n')
		return

	def CSFDParseUserReviews(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserReviews - zacatek\n')
		Extratext = ''
		coltextFormatUziv = 'AAAAAAAAAAAAAAA'
		extraresult = ParserCSFD.parserUserRating()
		if extraresult is not None:
			for x in extraresult:
				Extratext += self['extralabel'].CalculateSizeAddSpaceDiff(x[0], coltextFormatUziv) + x[1] + '\n'

		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádné další hodnocení v databázi.')
			else:
				Extratext = '\n' + _('Žádné hodnocení v databázi.')
		Extradopln = _('Hodnocení uživatelů') + ' '
		pocet = ParserCSFD.parserRatingNumber()
		if pocet is not None:
			Extradopln += '(' + _('počet hodnocení:') + ' ' + intWithSeparator(pocet) + ')' + '\n\n'
		else:
			Extradopln += ':\n\n'
		self['extralabel'].setTextHead(Extradopln)
		Extratext = self['extralabel'].AddRowIntoText(Extradopln, '') + Extratext
		self['extralabel'].setTextCol('')
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserReviews - konec\n')
		return

	def CSFDParseUserPremiery(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserPremiery - zacatek\n')
		Extratext, Pristupnost = ParserCSFD.parserPremiere()
		if Pristupnost != '':
			Extratext = Pristupnost + '\n\n' + Extratext
		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádné další premiéry v databázi.')
			else:
				Extratext = '\n' + _('Žádné premiéry v databázi.')
		elif self.PageSpec > 1:
			Extratext = '\n' + _('Žádné další premiéry v databázi.')
		Extradopln = _('Premiéry') + ' :' + '\n\n'
		self['extralabel'].setTextHead(Extradopln)
		Extratext = self['extralabel'].AddRowIntoText(Extradopln, '') + strUni(char2Allowchar(Extratext))
		self['extralabel'].setTextCol('')
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserPremiery - konec\n')

	def CSFDParseUserFans(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserFans - zacatek\n')
		Extratext = ParserCSFD.parserUserFans()
		if Extratext == '':
			if self.PageSpec > 1:
				Extratext = '\n' + _('Žádní další fanoušci v databázi.')
			else:
				Extratext = '\n' + _('Žádní fanoušci v databázi.')
		Extradopln = _('Fanclub pořadu') + ' '
		pocet = ParserCSFD.parserUserFansNumber()
		if pocet is not None:
			Extradopln += '(' + _('počet fanoušků:') + ' ' + intWithSeparator(pocet) + ')' + '\n\n'
		else:
			Extradopln += ':\n\n'
		self['extralabel'].setTextHead(Extradopln)
		Extratext = self['extralabel'].AddRowIntoText(Extradopln, '') + strUni(char2Allowchar(Extratext))
		self['extralabel'].setTextCol('')
		self['extralabel'].setText(Extratext)
		LogCSFD.WriteToFile('[CSFD] CSFDParseUserFans - konec\n')
		return

	def CSFDAllVideoDownload(self):
		self.VideoDwnlIsNotStarted = False
		LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - zacatek\n')
		video_res = config.misc.CSFD.VideoResolution.getValue()
		
		try:
			id_filmu = self.linkGlobal
				
			if id_filmu.startswith('#movie#') == False:
				raise ValueError("Nespravny format ID filmu")
				
			id_filmu = id_filmu[7:]
		except:
			id_filmu = ''
			LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - chyba self.linkGlobal - konec\n', 5)
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err, 5)
			return

		porVF = 0
		
		LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - stahuji z url ' + id_filmu + '\n')
		result = csfdAndroidClient.get_json_by_uri( '#movie_videos#' + id_filmu )

		ParserVideoCSFD.setJson(result)
		results = ParserVideoCSFD.parserVideoDetail(config.misc.CSFD.QualityVideoPoster.getValue())
		LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - parserVideoDetail\n')
		if results is not None:
			for x in results:
				if video_res == 'hd':
					videoklipurl = x[1] or x[0]
				else:
					videoklipurl = x[0] or x[1]
				if CSFDGlobalVar.getCSFDlang() == 'sk':
					videotitulkyurl = x[3] or x[2]
				else:
					videotitulkyurl = x[2] or x[3]
				if videoklipurl != '':
					ss = strUni(char2Allowchar(x[4]))
					porVF += 1
					s_video = 'V' + str(porVF).zfill(7)
					localfile = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDVPoster' + str(porVF).zfill(7) + '_' + str(randint(1, 99999)) + '.jpg'
					LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - videoposter: ' + x[5] + '\n')
					downloaded = False
					url = ""
					self.VideoSlideList.append([url, porVF, ss, s_video, videoklipurl, videotitulkyurl, x[5], char2DiacriticSort(ss), localfile, downloaded])
					self.VideoCountPix += 1

			LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - VideoCountPix ' + str(self.VideoCountPix) + '\n')
			if self.Page == 2 and self.querySpecAkce == 'UserVideo':
				self.VideoSlideList.sort(key=lambda z: z[7])
				if self.VideoIsNotFullyRead:
					self.VideoIsNotFullyRead = False
					if self['extralabel'].instance.isVisible():
						self['extralabel'].hide()
					if not self['playbutton'].instance.isVisible():
						self['playbutton'].show()
					if not self['photolabel'].instance.isVisible():
						self['photolabel'].show()
					self.CSFDVideoShow()
				else:
					idx = self.VideoActIdx
					ss = str(idx + 1) + '/' + str(self.VideoCountPix) + '  ' + strUni(self.VideoSlideList[idx][2])
					self['statusbar'].setText(ss)

		self.VideoSlideList.sort(key=lambda z: z[7])
		self.VideoIsNotFullyRead = False
		ParserVideoCSFD.setJson({})
		LogCSFD.WriteToFile('[CSFD] CSFDAllVideoDownload - konec\n')
		return

	def CSFDPlayerExit(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPlayerExit - zacatek\n')
		self.AntiFreezeTimerWorking = True
		self.myreference = None
		self.CSFDRefreshVideoInformation()
		LogCSFD.WriteToFile('[CSFD] CSFDPlayerExit - konec\n')
		return

	def CSFDgetEntryVideo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - zacatek\n')
		self.videoklipurl = self.VideoSlideList[self.VideoActIdx][4]
		self.videotitulkyurl = self.VideoSlideList[self.VideoActIdx][5]
		LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - video file: ' + self.videoklipurl + '\n')
		LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - video titulky: ' + self.videotitulkyurl + '\n')
		if self.videoklipurl != '':
			LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - spouteni playeru\n')
			self.AntiFreezeTimerWorking = False
			acname = strUni(self.ActName)
			self.myreference = eServiceReference(4097, 0, str(self.videoklipurl))
			self.myreference.setName(acname + ' - ' + self.VideoSlideList[self.VideoActIdx][2])
			self.session.open(CSFDPlayer, self.myreference, self.lastservice, str(self.videotitulkyurl), infoCallback=self.CSFDshowVideoInfo, nextCallback=self.CSFDgetNextEntryVideo, prevCallback=self.CSFDgetPrevEntryVideo, exitCallback=self.CSFDPlayerExit, existPrevOrNextCallback=self.CSFDexistPrevOrNextVideo, downloadVideo=self.CSFDopenVideoDownload, colorOLED=GetItemColourRateN(self.ratingstars))
			sss = str(self.VideoActIdx + 1)
			self['page'].setText(_('Video č.%s' % sss))
			sss = sss + '/' + str(self.VideoCountPix) + '  ' + strUni(self.VideoSlideList[self.VideoActIdx][2])
			self['statusbar'].setText(sss)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - video neni dostupne\n')
			self.session.open(MessageBox, _('Video není bohužel dostupné!'), MessageBox.TYPE_ERROR, timeout=10)
		LogCSFD.WriteToFile('[CSFD] CSFDgetEntryVideo - konec\n')

	def CSFDRefreshVideoInformation(self):
		LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - zacatek\n')
		idx = self.VideoActIdx
		pol = self.VideoSlideList[idx]
		LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - video: ' + pol[6] + '\n')
		videoposterfile = pol[6]
		znovu = False
		if videoposterfile[:4].upper() == 'HTTP':
			localfile = pol[8]
			LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - video poster - localfile: ' + localfile + '\n')
			LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - video poster - url: ' + videoposterfile + '\n')

			idx1 = idx
			if requestFileCSFD(videoposterfile, localfile ) == True:
				if videoposterfile == self.VideoSlideList[idx1][6]:
					self.VideoSlideList[idx1][6] = localfile
					videoposterfile = localfile
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - spatne prirazeny stahnuty video poster - zkousim znovu\n')
					znovu = True
					videoposterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')
				idx = idx1
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - chyba - download video posteru\n')
				LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - Chyba pri stahovani video posteru - url: ' + Uni8(videoposterfile) + '\n')
				LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - Chyba pri stahovani video posteru - localfile: ' + Uni8(localfile) + '\n')
				videoposterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')

		sss = str(idx + 1)
		self['page'].setText(_('Video č.%s' % sss))
		self.paintVideoPixmap(videoposterfile)
		sss = str(idx + 1) + '/' + str(self.VideoCountPix) + '	' + strUni(self.VideoSlideList[idx][2])
		self['statusbar'].setText(sss)
		if znovu:
			self.CSFDRefreshVideoInformation()
		LogCSFD.WriteToFile('[CSFD] CSFDRefreshVideoInformation - konec\n')

	def CSFDexistPrevOrNextVideo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDexistPrevOrNextVideo - zacatek\n')
		nextVideo = True
		prevVideo = True
		if self.VideoActIdx + 1 >= self.VideoCountPix:
			nextVideo = False
		if self.VideoActIdx <= 0:
			prevVideo = False
		LogCSFD.WriteToFile('[CSFD] CSFDexistPrevOrNextVideo - konec\n')
		return (prevVideo, nextVideo)

	def CSFDgetNextEntryVideo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDgetNextEntryVideo - zacatek\n')
		self.VideoActIdx += 1
		if self.VideoActIdx >= self.VideoCountPix:
			self.VideoActIdx = self.VideoCountPix - 1
			LogCSFD.WriteToFile('[CSFD] CSFDgetNextEntryVideo - None a False (konec seznamu u next) - konec\n')
			return (
			 None, None, False)
		else:
			self.videoklipurl = self.VideoSlideList[self.VideoActIdx][4]
			self.videotitulkyurl = self.VideoSlideList[self.VideoActIdx][5]
			if self.videoklipurl != '':
				self.myreference = eServiceReference(4097, 0, str(self.videoklipurl))
				self.myreference.setName(self.eventNameLocal + ' - ' + self.VideoSlideList[self.VideoActIdx][2])
				LogCSFD.WriteToFile('[CSFD] CSFDgetNextEntryVideo - ' + self.videoklipurl + ' a False - konec\n')
				return (
				 self.myreference, self.videotitulkyurl, False)
			LogCSFD.WriteToFile('[CSFD] CSFDgetNextEntryVideo - None a True - konec\n')
			return (None, None, True)
			return

	def CSFDgetPrevEntryVideo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDgetPrevEntryVideo - zacatek\n')
		self.VideoActIdx += -1
		if self.VideoActIdx < 0:
			self.VideoActIdx = 0
			LogCSFD.WriteToFile('[CSFD] CSFDgetPrevEntryVideo - None a False (konec seznamu u prev) - konec\n')
			return (
			 None, None, False)
		else:
			self.videoklipurl = self.VideoSlideList[self.VideoActIdx][4]
			self.videotitulkyurl = self.VideoSlideList[self.VideoActIdx][5]
			if self.videoklipurl != '':
				self.myreference = eServiceReference(4097, 0, str(self.videoklipurl))
				self.myreference.setName(self.eventNameLocal + ' - ' + self.VideoSlideList[self.VideoActIdx][2])
				LogCSFD.WriteToFile('[CSFD] CSFDgetPrevEntryVideo - ' + self.videoklipurl + ' a False - konec\n')
				return (
				 self.myreference, self.videotitulkyurl, False)
			LogCSFD.WriteToFile('[CSFD] CSFDgetPrevEntryVideo - None a True - konec\n')
			return (None, None, True)
			return

	def CSFDAllGalleryDownload(self):
		LogCSFD.WriteToFile('[CSFD] CSFDAllGalleryDownload - zacatek\n', 5)

		def GalleryFiles():
			LogCSFD.WriteToFile('[CSFD] GalleryFiles - zacatek\n', 5)
			
			porGF = 0
			porGFtyp = 0
			try:
				id_filmu = self.linkGlobal
				
				if id_filmu.startswith('#movie#') == False:
					raise ValueError("Nespravny format ID filmu")
				
				id_filmu = id_filmu[7:]
			except:
				id_filmu = ''
				LogCSFD.WriteToFile('[CSFD] GalleryFiles - chyba self.linkGlobal - konec\n', 5)
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err, 5)
				return

#			timeoutGall = config.misc.CSFD.DownloadTimeOut.getValue()
			
			result = csfdAndroidClient.get_json_by_uri( '#movie_photos#' + id_filmu )
			
			if self.PosterBasicCountPixAllG < 0:
				self.PosterBasicCountPixAllG = len(result["photos"])

			for photo in result["photos"]:
				photo_url = photo["url"]
				
#				qidx = photo_url.rfind('?w')
#				if qidx != -1:
#					photo_url = photo_url[:qidx]
				
				porGF += 1
				porGFtyp += 1
				s_porGF = str(porGF)
				popis_gal = str(porGFtyp)

				localfile = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDGallery' + str(porGF).zfill(7) + '_' + str(randint(1, 99999)) + '.jpg'
				sort_gallery = 'B' + s_porGF.zfill(7)
				popis_gal = _('Galerie: ') + "Fotky" + ' - ' + popis_gal

				self.PosterBasicSlideList.append([photo_url, porGF, popis_gal, sort_gallery, localfile])
				self.PosterBasicSlideList.sort(key=lambda z: z[3])
				self.GallerySlideList.append([photo_url, porGF, popis_gal, sort_gallery, localfile])
				self.GallerySlideList.sort(key=lambda z: z[3])
				self.PosterBasicCountPix += 1

				if self.PosterBasicCountPix > 0:
					if self.PosterBasicSlideStop == True:
						self.PosterBasicSlideStop = False
						
				LogCSFD.WriteToFile('[CSFD] GalleryFiles - PosterBasicsList: ' + localfile + ' - ' + str(porGF) + ' - ' + Uni8(popis_gal) + ' - ' + sort_gallery + '\n', 5)
				self.GalleryCountPix += 1
				if self.GalleryCountPix > 0:
					if self.GallerySlideStop == True:
						self.GallerySlideStop = False
					if self.GalleryCountPix == 1 and 'postery' in self.FunctionExists and self.Page == 1:
						self['poster'].show()
						self.CSFDPosterBasicSlideShowEvent()
				LogCSFD.WriteToFile('[CSFD] GalleryFiles - GalleryList: ' + localfile + ' - ' + str(porGF) + ' - ' + Uni8(popis_gal) + ' - ' + sort_gallery + '\n', 5)


			self.GalleryIsNotFullyRead = False
			LogCSFD.WriteToFile('[CSFD] GalleryFiles - konec\n', 5)
			LogCSFD.WriteToFile('[CSFD] CSFDAllGalleryDownload - konec\n', 5)
			return

		GalleryFiles()

	def GalleryDownloadTimerEvent(self):
		if self.GalleryDownloadTimer is not None:
			if self.GalleryDownloadTimer.isActive():
				self.GalleryDownloadTimer.stop()
		self.CSFDAllGalleryDownload()
		return

	def CSFDPosterBasic(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - zacatek\n', 6)
		try:
			id_filmu = self.linkGlobal
		except:
			id_filmu = ''
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - chyba self.linkGlobal - konec\n', 6)
			LogCSFD.WriteToFile(err, 6)
			return

		readmainposter = False
		filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')
		if config.misc.CSFD.PosterBasic.getValue() == True:
			self['statusbar'].setText(_('CSFD Poster'))
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - parse poster\n', 6)
			resultText = ParserCSFD.parserMainPosterUrl(config.misc.CSFD.QualityPoster.getValue())
			if resultText is not None and resultText is not '':
				LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - Parse - resultText\n', 6)
				filename = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDPoster.jpg'
				readmainposter = True
				if self.stahnutoCSFDImage == resultText:
					LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - poster - neni nutne znovu stahovat poster\n', 6)
				else:
					self['statusbar'].setText(str( _('Stahuji obal k filmu: ') + resultText) )
					LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - download main poster: ' + resultText + '\n', 6)

					if requestFileCSFD(resultText, filename ) == True:
						self.stahnutoCSFDImage = resultText
					else:
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - chyba - download\n', 6)
						readmainposter = False
						filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')

					if id_filmu != self.linkGlobal:
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - zruseno - nacitani jineho poradu\n', 6)
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - konec\n', 6)
						return
				if ParserCSFD.parserPostersNumber() is None and readmainposter:
					sort_poster = ('A1').zfill(7)
					self.AddPoster(filename, filename, 1, sort_poster)
		if id_filmu != self.linkGlobal:
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - zruseno - nacitani jineho poradu\n', 6)
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - konec\n', 6)
			return
		else:
			if readmainposter:
				self.paintPosterBasicPixmap(filename)
			elif 'galerie' in self.FunctionExists:
				self.paintPosterBasicPixmap(filename)
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasic - konec\n', 6)
			self['statusbar'].setText(_('Autor pluginu: ') + 'petrkl12@tvplugins.cz')
			return

	def CSFDPosterBasicStart(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicStart - zacatek\n')
		self.CSFDPosterBasic()
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicStart - konec\n')

	def CSFDAllPostersDownload(self):
		LogCSFD.WriteToFile('[CSFD] CSFDAllPostersDownload - zacatek\n', 7)
		try:
			id_filmu = self.linkGlobal
		except:
			id_filmu = ''
			LogCSFD.WriteToFile('[CSFD] CSFDAllPostersDownload - chyba self.linkGlobal - konec\n', 7)
			LogCSFD.WriteToFile(err, 7)
			return

		porPF = 0
		result = ParserCSFD.parserAllPostersUrl(config.misc.CSFD.QualityPoster.getValue())
		if result is not None:
			for posterfile in result:
				porPF += 1
				localfile = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDPoster' + str(porPF).zfill(7) + '_' + str(randint(1, 99999)) + '.jpg'
				if id_filmu != self.linkGlobal:
					LogCSFD.WriteToFile('[CSFD] CSFDAllPostersDownload - zruseno - nacitani jineho poradu\n', 7)
					LogCSFD.WriteToFile('[CSFD] CSFDAllPostersDownload - konec\n', 7)
					return
				sort_poster = 'A' + str(porPF).zfill(7)
				self.AddPoster(posterfile, localfile, porPF, sort_poster)

		self.PosterIsNotFullyRead = False
		LogCSFD.WriteToFile('[CSFD] CSFDAllPostersDownload - konec\n', 7)
		return

	def AddPoster(self, posterfile, localfile, porPF, sort_poster):
		LogCSFD.WriteToFile('[CSFD] AddPoster - zacatek %s\n' % posterfile, 7)
		s_poster = _('Poster: ') + str(porPF)
		self.PosterBasicSlideList.append([posterfile, porPF, s_poster, sort_poster, localfile])
		self.PosterBasicSlideList.sort(key=lambda z: z[3])
		self.PosterSlideList.append([posterfile, porPF, s_poster, sort_poster, localfile])
		self.PosterSlideList.sort(key=lambda z: z[3])
		self.PosterBasicCountPix += 1
		if self.PosterBasicCountPix > 0:
			if self.PosterBasicSlideStop == True:
				self.PosterBasicSlideStop = False
		LogCSFD.WriteToFile('[CSFD] AddPoster - PosterBasicsList: ' + localfile + ' - ' + str(porPF) + ' - ' + Uni8(s_poster) + ' - ' + sort_poster + '\n', 7)
		self.PosterCountPix += 1
		if self.PosterCountPix > 0:
			if self.PosterSlideStop == True:
				self.PosterSlideStop = False
		LogCSFD.WriteToFile('[CSFD] AddPoster - PosterList: ' + localfile + ' - ' + str(porPF) + ' - ' + Uni8(s_poster) + ' - ' + sort_poster + '\n', 7)
		LogCSFD.WriteToFile('[CSFD] AddPoster - konec\n', 7)

	def PosterDownloadTimerEvent(self):
		if self.PosterDownloadTimer is not None:
			if self.PosterDownloadTimer.isActive():
				self.PosterDownloadTimer.stop()
		self.CSFDAllPostersDownload()
		return

	def paintPosterBasicPixmap(self, image_path=''):
		if self.Page == 1:
			LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - showing poster file: ' + Uni8(image_path) + '\n')
			try:
				self['poster'].instance.setPixmap(gPixmapPtr())
				if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
					if self.picload.startDecode(str(image_path), 0, 0, False) == 0:
						ptr = self.picload.getData()
						if ptr is not None:
							self['poster'].instance.setPixmap(ptr)
							self['poster'].show()
						else:
							LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
							self['poster'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
						self['poster'].show()
				elif self.picload.startDecode(str(image_path), False) == 0:
					ptr = self.picload.getData()
					if ptr is not None:
						self['poster'].instance.setPixmap(ptr)
						self['poster'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
						self['poster'].show()
				else:
					LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
					self['poster'].show()
			except:
				LogCSFD.WriteToFile('[CSFD] paintPosterBasicPixmap - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
				self['poster'].show()

		return

	def paintPosterPixmap(self, image_path=''):
		if self.Page == 2 and self.querySpecAkce == 'UserPoster':
			try:
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
					if self.posterload.startDecode(str(image_path), 0, 0, False) == 0:
						ptr = self.posterload.getData()
						if ptr is not None:
							self['photolabel'].instance.setPixmap(ptr)
							self['photolabel'].show()
						else:
							LogCSFD.WriteToFile('[CSFD] paintPosterPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
							self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintPosterPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				elif self.posterload.startDecode(str(image_path), False) == 0:
					ptr = self.posterload.getData()
					if ptr is not None:
						self['photolabel'].instance.setPixmap(ptr)
						self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintPosterPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				else:
					LogCSFD.WriteToFile('[CSFD] paintPosterPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
					self['photolabel'].show()
			except:
				LogCSFD.WriteToFile('[CSFD] paintPosterPixmap - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
				self['photolabel'].show()

		return

	def paintGalleryPixmap(self, image_path=''):
		if self.Page == 2 and self.querySpecAkce == 'UserGallery':
			try:
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
					if self.galleryload.startDecode(str(image_path), 0, 0, False) == 0:
						ptr = self.galleryload.getData()
						if ptr is not None:
							self['photolabel'].instance.setPixmap(ptr)
							self['photolabel'].show()
						else:
							LogCSFD.WriteToFile('[CSFD] paintGalleryPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
							self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintGalleryPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				elif self.galleryload.startDecode(str(image_path), False) == 0:
					ptr = self.galleryload.getData()
					if ptr is not None:
						self['photolabel'].instance.setPixmap(ptr)
						self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintGalleryPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				else:
					LogCSFD.WriteToFile('[CSFD] paintGalleryPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
					self['photolabel'].show()
			except:
				LogCSFD.WriteToFile('[CSFD] paintGalleryPixmap - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
				self['photolabel'].show()

		return

	def paintVideoPixmap(self, image_path=''):
		if self.Page == 2 and self.querySpecAkce == 'UserVideo':
			try:
				self['photolabel'].instance.setPixmap(gPixmapPtr())
				if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
					if self.videoload.startDecode(str(image_path), 0, 0, False) == 0:
						ptr = self.videoload.getData()
						if ptr is not None:
							self['photolabel'].instance.setPixmap(ptr)
							self['photolabel'].show()
						else:
							LogCSFD.WriteToFile('[CSFD] paintVideoPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
							self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintVideoPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				elif self.videoload.startDecode(str(image_path), False) == 0:
					ptr = self.videoload.getData()
					if ptr is not None:
						self['photolabel'].instance.setPixmap(ptr)
						self['photolabel'].show()
					else:
						LogCSFD.WriteToFile('[CSFD] paintVideoPixmap - ptr nenalezeno: ' + Uni8(image_path) + '\n')
						self['photolabel'].show()
				else:
					LogCSFD.WriteToFile('[CSFD] paintVideoPixmap - decode nenalezeno: ' + Uni8(image_path) + '\n')
					self['photolabel'].show()
			except:
				LogCSFD.WriteToFile('[CSFD] paintVideoPixmap - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
				self['photolabel'].show()

		return

	def paintTipsIcon(self, picInfo=None):
		if self.tipsiconload and self.tipsiconload_conn:
			try:
				ptr = self.tipsiconload.getData()
				if ptr is not None:
					self['tips_icon'].instance.setPixmap(ptr)
			except:
				LogCSFD.WriteToFile('[CSFD] paintTipsIcon - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)

		return

	def CSFDChangeOwnRating(self):
		LogCSFD.WriteToFile('[CSFD] CSFDChangeOwnRating - zacatek\n', 8)
		linkG = self.linkGlobal

		def reloadMovieAfterRating(result):
			LogCSFD.WriteToFile('[CSFD] reloadMovieAfterRating - zacatek\n', 8)
			if result:
				self.ReDownloadMovieAndParseMainPart()
			LogCSFD.WriteToFile('[CSFD] reloadMovieAfterRating - konec\n', 8)

		def DeleteRatingOnWeb():
			LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - zacatek\n', 8)
			try:
#				url = CSFDGlobalVar.getHTTP() + const_csfd_http_film + linkG
#				page = requestCSFD(url, headers=std_headers_UL2, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue())
#				ParserOstCSFD.setHTML2utf8(page)
#				del_url = ParserOstCSFD.parserDeleteRatingUrl()
				del_url = None
			except:
				LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - reload url - chyba\n', 8)
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err, 8)
				self.session.open(MessageBox, _('Chyba při mazání hodnocení'), type=MessageBox.TYPE_ERROR, timeout=10)

			if del_url is not None and del_url != '':
				try:
#					del_url = CSFDGlobalVar.getHTTP() + const_www_csfd + del_url
#					LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - url: %s \n' % del_url, 8)
					
#					page = requestCSFD(del_url, headers=std_headers_UL2, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue())
					
					if linkG == self.linkGlobal:
						reloadMovieAfterRating(True)
					else:
						self.session.open(MessageBox, _('Hodnocení smazáno'), type=MessageBox.TYPE_INFO, timeout=5)
				except:
					LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - chyba\n', 8)
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err, 8)
					self.session.open(MessageBox, _('Chyba při mazání hodnocení'), type=MessageBox.TYPE_ERROR, timeout=10)

			else:
				LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - nenalezeno url pro smazani hodnoceni\n', 8)
				self.session.open(MessageBox, _('Nenalezena možnost pro smazaní'), type=MessageBox.TYPE_ERROR, timeout=10)
			LogCSFD.WriteToFile('[CSFD] DeleteRatingOnWeb - konec\n', 8)
			return

		def SaveRatingOnWeb(value_rating):
			LogCSFD.WriteToFile('[CSFD] SaveRatingOnWeb - zacatek\n', 8)
			if csfdAndroidClient.set_movie_rating( linkG, value_rating ) != None:
				if linkG == self.linkGlobal:
					reloadMovieAfterRating(True)
				else:
					self.session.open(MessageBox, _('Hodnocení uloženo'), type=MessageBox.TYPE_INFO, timeout=5)
			else:
				LogCSFD.WriteToFile('[CSFD] SaveRatingOnWeb - chyba\n', 8)
				self.session.open(MessageBox, _('Chyba při ukládání hodnocení'), type=MessageBox.TYPE_ERROR, timeout=10)

			LogCSFD.WriteToFile('[CSFD] SaveRatingOnWeb - konec\n', 8)
			return

		def leaveChoiceBoxRating(answer):
			LogCSFD.WriteToFile('[CSFD] - leaveChoiceBoxRating - zacatek\n', 8)
			answer = answer and answer[1]
			if answer == '100' or answer == '80' or answer == '60' or answer == '40' or answer == '20' or answer == '0':
				SaveRatingOnWeb(answer)
			elif answer == 'smazat':
				DeleteRatingOnWeb()
			LogCSFD.WriteToFile('[CSFD] - leaveChoiceBoxRating - konec\n', 8)

		ss, ss1 = ParserCSFD.parserOwnRating()
		if ss is not None and ss is not '':
			akt_rating = ss
			select = int((ss1 / 20 - 5) * -1)
		else:
			akt_rating = _('ještě nehodnoceno')
			select = 0
#		token = ParserCSFD.parserTokenRating()
#		if token is not None and token != '':
		if ParserCSFD.parserRatingAllowed() == True:
			listP = (
				('100%	* * * * *', '100'),
				('80% 	  * * * *', '80'),
				('60% 	    * * *', '60'),
				('40% 	      * *', '40'),
				('20% 	        *', '20'),
				('0%  	   odpad!', '0')
			)
			
			if ParserCSFD.parserDeleteRatingUrl():
				listP = listP + ((_('smazat hodnocení'), 'smazat'),)
			listP = listP + ((_('ukončit'), 'exit'),)
			self.session.openWithCallback(leaveChoiceBoxRating, ChoiceBox, title=_('Zadejte hodnocení pro:') + '\n' + strUni(self.ActName) + '\n' + _('(Aktuální hodnocení: %s)') % akt_rating, list=listP, selection=select)
		LogCSFD.WriteToFile('[CSFD] ChangeOwnRating - konec\n', 8)
		return

	def getHelpKeyDescr(self):
		seznamOld = self.OldKeyHelp[0][2]
		seznamNew = []
		for x in seznamOld:
			if x is None or x[1] is None:
				continue
			for tip_cislo in range(len(self.Tips)):
				tip = self.Tips[tip_cislo]
				if x[1] + '.png' == tip[0]:
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_4' and tip[1] == config.misc.CSFD.HotKey4.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_5' and tip[1] == config.misc.CSFD.HotKey5.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_6' and tip[1] == config.misc.CSFD.HotKey6.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_7' and tip[1] == config.misc.CSFD.HotKey7.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_8' and tip[1] == config.misc.CSFD.HotKey8.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_9' and tip[1] == config.misc.CSFD.HotKey9.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_0' and tip[1] == config.misc.CSFD.HotKey0.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_s_red_l' and tip[1] == config.misc.CSFD.HotKeyLR.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_s_green_l' and tip[1] == config.misc.CSFD.HotKeyLG.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_s_blue_l' and tip[1] == config.misc.CSFD.HotKeyLB.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))
				if x[1] == 'key_s_yellow_l' and tip[1] == config.misc.CSFD.HotKeyLY.getValue():
					if not self.CSFDTipsOmezeni(tip_cislo):
						seznamNew.append((x[0], tip[2]))

		seznamNew.sort(key=lambda z: z[0])
		self.helpList = []
		self.helpList.append((self.OldKeyHelp[0][0], self.OldKeyHelp[0][1], seznamNew))
		return self.helpList

	def CSFDTipsLoad(self):
		LogCSFD.WriteToFile('[CSFD] CSFDTipsLoad - zacatek\n')
		self.Tips = [
			('key_menu.png', '', _('zobrazí menu s aktuálně dostupnými akcemi'), '', ''),
			('HOTKEY', 'aktEPG', _('výběr hledaného pořadu z EPG aktuálního kanálu'), _('v menu můžete provést výběr hledaného pořadu z EPG aktuálního kanálu'), ''),
			('HOTKEY', 'vyberEPG', _('výběr hledaného pořadu ze všech kanálů'), _('v menu můžete provést výběr hledaného pořadu ze všech kanálů'), ''),
			('HOTKEY', 'zadejporad', _('manuální zadání hledaného pořadu'), _('v menu můžete provést manuální zadání hledaného pořadu'), ''),
			('HOTKEY', 'spustitIMDB', _('vyhledání aktuálního pořadu v mezinárodní filmové databázi IMDB'), _('v menu můžete vyhledat aktuální pořad v mezinárodní filmové databázi IMDB'), 'IMDBexist'),
			('HOTKEY', 'komentare', _('zobrazí komentáře uživatelů k pořadu'), _('v menu můžete zobrazit komentáře uživatelů k pořadu'), 'Page>0'),
			('HOTKEY', 'ext.recenze', _('zobrazí externí recenze k pořadu'), _('v menu můžete zobrazit externí recenze k pořadu'), 'Page>0'),
			('HOTKEY', 'ownrating', _('máte možnost ohodnotit vyhledaný pořad'), _('v menu můžete ohodnotit vyhledaný pořad'), 'Page>0'),
			('HOTKEY', 'diskuze', _('zobrazí diskuzi uživatelů k pořadu'), _('v menu můžete zobrazit diskuzi uživatelů k pořadu'), 'Page>0'),
			('HOTKEY', 'zajimavosti', _('zobrazí zajímavosti o pořadu'), _('v menu můžete zobrazit zajímavosti o pořadu'), 'Page>0'),
			('HOTKEY', 'oceneni', _('zobrazí získaná ocenění'), _('v menu můžete zobrazit získaná ocenění'), 'Page>0'),
			('HOTKEY', 'souvisejici', _('zobrazí související filmy'), _('v menu můžete zobrazit související filmy'), 'Page>0'),
			('HOTKEY', 'serie', _('zobrazí řady seriálu'), _('v menu můžete zobrazit řady seriálu'), 'Page>0'),
			('HOTKEY', 'epizody', _('zobrazí epizody seriálu'), _('v menu můžete zobrazit epizody seriálu'), 'Page>0'),
			('HOTKEY', 'galerie', _('zobrazí galerii fotek z pořadu'), _('v menu můžete zobrazit galerii fotek z pořadu'), 'Page>0'),
			('HOTKEY', 'postery', _('zobrazí postery (filmové plakáty) k pořadu'), _('v menu můžete zobrazit postery (filmové plakáty) k pořadu'), 'Page>0'),
			('HOTKEY', 'ulozvideo', _('uloží video ukázku do definovaného adresáře'), _('v menu můžete uložit video ukázku do definovaného adresáře'), 'Page=2 and UserVideo and pocetV>0'),
			('HOTKEY', 'spustitvideo', _('spustí aktuální video ukázku'), _('v menu můžete spustit aktuální video ukázku'), 'Page=2 and UserVideo and pocetV>0'),
			('HOTKEY', 'premiery', _('zobrazí premiéry pořadu'), _('v menu můžete zobrazit premiéry pořadu'), 'Page>0'),
			('HOTKEY', 'hodnoceni', _('zobrazí detailní hodnocení pořadu'), _('v menu můžete zobrazit detailní hodnocení pořadu'), 'Page>0'),
			('HOTKEY', 'fanousci', _('zobrazí fanoušky pořadu'), _('v menu můžete zobrazit fanoušky pořadu'), 'Page>0'),
			('HOTKEY', 'skin', _('možnost změny skinu'), _('v menu můžete změnit skin'), ''),
			('HOTKEY', 'historie', _('zobrazí historii změn v pluginu'), _('v menu můžete zobrazit historii změn v pluginu'), ''),
			('HOTKEY', 'novaverze', _('zobrazí informaci, zda je k dostupná nová verze'), _('v menu můžete zjistit, zda je dostupná nová verze pluginu'), ''),
			('', '', _('v menu můžete setřídit vyhledané položky podle pořadí na CSFD'), '', 'Page=0'),
			('', '', _('v menu můžete setřídit vyhledané položky podle vhodnosti názvu'), '', 'Page=0'),
			('', '', _('v menu můžete setřídit vyhledané položky podle abecedy'), '', 'Page=0'),
			('', '', _('v menu můžete vyhledat všechny podobné názvy k danému pořadu'), '', 'Page=0 and not(FindAllItems)'),
			('key_video.png', '', _('zobrazí video ukázky z pořadu'), '', 'Page>0'),
			('key_text.png', '', _('možnost změny nastavení různých parametrů pluginu'), '', ''),
			('key_help.png', '', _('zobrazí nápovědu k jednotlivým tlačítkům v pluginu'), '', ''),
			('key_exit.png', '', _('zpět v jednotlivých položkách nebo ukončení pluginu'), '', ''),
			('key_s_red.png', '', _('zpět v jednotlivých položkách nebo ukončení pluginu'), '', ''),
			('key_s_green.png', '', _('zobrazí seznam vyhledaných pořadů'), '', 'Page>0'),
			('key_s_green.png', '', _('výběr hledaného pořadu z EPG aktuálního kanálu'), '', 'Page=0'),
			('key_s_yellow.png', '', _('zobrazí detaily o pořadu'), '', ''),
			('key_info.png', '', _('zobrazí detaily o pořadu'), '', ''),
			('key_epg.png', '', _('zobrazí detaily o pořadu'), '', ''),
			('key_s_blue.png', '', _('manuální zadání hledaného pořadu'), '', 'Page=0'),
			('key_s_blue.png', '', _('zobrazí další detaily o pořadu dle aktuálního kontextu'), '', 'Page>0'),
			('key_2.png', '', _('můžete setřídit komentáře podle počtu bodů uživatele'), '', 'komentare'),
			('key_2.png', '', _('můžete setřídit komentáře od nejnovějších po nejstarší'), '', 'komentare'),
			('key_2.png', '', _('můžete setřídit komentáře podle hodnocení uživatelů'), '', 'komentare'),
			('key_1.png', '', _('posun na předchozí stránku nebo položku'), '', 'Page=2'),
			('key_3.png', '', _('posun na následující stránku nebo položku'), '', 'Page=2'),
			('key_1.png', '', _('změna třídění vyhledaných pořadů'), '', 'Page=0'),
			('key_3.png', '', _('změna třídění vyhledaných pořadů'), '', 'Page=0'),
			('key_left.png', '', _('posun na předchozí stránku nebo položku'), '', 'Page=2'),
			('key_right.png', '', _('posun na následující stránku nebo položku'), '', 'Page=2'),
			('key_left.png', '', _('změna třídění vyhledaných pořadů'), '', 'Page=0'),
			('key_right.png', '', _('změna třídění vyhledaných pořadů'), '', 'Page=0'),
			('key_bq_up.png', '', _('rotace po jednotlivých informacích o pořadu'), '', 'Page>0'),
			('key_bq_down.png', '', _('rotace po jednotlivých informacích o pořadu'), '', 'Page>0'),
			('key_play.png', '', _('spustí aktuální video ukázku'), '', 'Page=2 and UserVideo and pocetV>0'),
			('key_ok.png', '', _('spustí aktuální video ukázku'), '', 'Page=2 and UserVideo and pocetV>0'),
			('key_play.png', '', _('spustí slideshow'), '', 'galerie or postery'),
			('key_pause.png', '', _('zastaví slideshow'), '', 'galerie or postery')
		]
		seed()
		self['tips_label'].setText(_('Tipy:'))
		LogCSFD.WriteToFile('[CSFD] CSFDTipsLoad - konec\n')

	def CSFDTipsOmezeni(self, tip_cislo):
		omezeni = True
		if self.Tips[tip_cislo][4] == '':
			omezeni = False
		elif self.Tips[tip_cislo][4] == 'Page=0':
			if self.Page == 0:
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'Page=2':
			if self.Page == 2:
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'Page>0':
			if self.Page > 0 and self.stahnutoCSFD2 != '':
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'komentare':
			if self.Page == 2 and self.querySpecAkce == 'UserComments':
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'IMDBexist':
			if CSFDGlobalVar.getIMDBexist():
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'Page=0 and not(FindAllItems)':
			if self.Page == 0 and not self.FindAllItems:
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'Page=2 and UserVideo and pocetV>0':
			if self.Page == 2 and self.querySpecAkce == 'UserVideo' and self.VideoCountPix > 0:
				omezeni = False
		elif self.Tips[tip_cislo][4] == 'galerie or postery':
			if self.Page == 2:
				if self.querySpecAkce == 'UserGallery' and self.GalleryCountPix > 0 or self.querySpecAkce == 'UserPoster' and self.PosterCountPix > 0:
					omezeni = False
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDTipsOmezeni - nedefinovany typ omezeni!!!\n')
		return omezeni

	def CSFDTipsTimerEvent(self):
		if self.TipsTimer is not None:
			if self.TipsTimer.isActive():
				self.TipsTimer.stop()
		if config.misc.CSFD.TipsShow.getValue():
			iconshow = False
			poc = 0
			omezeni = True
			while omezeni:
				poc += 1
				if poc > 10:
					tip_cislo = 0
					break
				tip_cislo = randint(0, len(self.Tips) - 1)
				omezeni = self.CSFDTipsOmezeni(tip_cislo)

			if self.Tips[tip_cislo][0] == '':
				mezery = ''
				self['tips_detail'].setText(mezery + self.Tips[tip_cislo][2])
			elif self.Tips[tip_cislo][0] == 'HOTKEY':
				png_type = ''
				if self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey4.getValue():
					png_type = 'key_4.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey5.getValue():
					png_type = 'key_5.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey6.getValue():
					png_type = 'key_6.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey7.getValue():
					png_type = 'key_7.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey8.getValue():
					png_type = 'key_8.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey9.getValue():
					png_type = 'key_9.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKey0.getValue():
					png_type = 'key_0.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKeyLR.getValue():
					png_type = 'key_s_red_l.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKeyLG.getValue():
					png_type = 'key_s_green_l.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKeyLB.getValue():
					png_type = 'key_s_blue_l.png'
				elif self.Tips[tip_cislo][1] == config.misc.CSFD.HotKeyLY.getValue():
					png_type = 'key_s_yellow_l.png'
				if png_type == '':
					mezery = ''
					self['tips_detail'].setText(mezery + self.Tips[tip_cislo][3])
				else:
					if picStartDecodeCSFD(self.tipsiconload, png_type):
						mezery = '		   '
						iconshow = True
					else:
						mezery = ''
						iconshow = False
						LogCSFD.WriteToFile('[CSFD] CSFDTipsTimerEvent - decode nenalezeno: ' + Uni8(png_type) + '\n')
					self['tips_detail'].setText(mezery + self.Tips[tip_cislo][2])
			else:
				if picStartDecodeCSFD(self.tipsiconload, self.Tips[tip_cislo][0]):
					mezery = '		   '
					iconshow = True
				else:
					mezery = ''
					iconshow = False
					LogCSFD.WriteToFile('[CSFD] CSFDTipsTimerEvent - decode nenalezeno: ' + Uni8(self.Tips[tip_cislo][0]) + '\n')
				self['tips_detail'].setText(mezery + self.Tips[tip_cislo][2])
			if self['key_red'].getText() != '':
				self['tips_label'].show()
				self['tips_detail'].show()
				if iconshow:
					ptr = self.tipsiconload.getData()
					if ptr is not None:
						self['tips_icon'].instance.setPixmap(ptr)
						self['tips_icon'].show()
					else:
						self['tips_icon'].hide()
				else:
					self['tips_icon'].hide()
			else:
				self['tips_label'].hide()
				self['tips_icon'].hide()
				self['tips_detail'].hide()
			self.TipsTimer.start(config.misc.CSFD.TipsTime.getValue() * 500, True)
		else:
			self['tips_label'].hide()
			self['tips_icon'].hide()
			self['tips_detail'].hide()
		return

	def RatingTimerEvent(self):
		if self.RatingTimer is not None:
			if self.RatingTimer.isActive():
				self.RatingTimer.stop()
		if config.misc.CSFD.RatingRotation.getValue():
			if self.Page != 0:
				oldratingcount = self.ratingcount
				self.ratingcount += 1
				if self.ratingcount > 2:
					self.ratingcount = 0
				if self.ratingcount == 1 and self.ratingstarsIMDB < 0:
					self.ratingcount = 2
				if self.ratingcount == 2 and self.ratingstarsMetacritic < 0:
					self.ratingcount = 0
				if self.ratingcount == oldratingcount:
					self.RatingTimer.start(config.misc.CSFD.RatingRotationTime.getValue() * 500, True)
					return
				self.refreshRating()
			self.RatingTimer.start(config.misc.CSFD.RatingRotationTime.getValue() * 500, True)
		return

	def CSFDPosterBasicSlideShowStart(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowStart - zacatek\n')
		if self.PosterBasicSlideShowTimer is not None:
			if self.PosterBasicSlideShowTimer.isActive():
				self.PosterBasicSlideShowTimer.stop()
		if config.misc.CSFD.PosterBasicSlide.getValue():
			self.PosterBasicActIdx = 0
			self.PosterBasicSlideShowTimer.start(config.misc.CSFD.PosterBasicSlideTime.getValue() * 500, True)
			LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowStart - start: ' + str(config.misc.CSFD.PosterBasicSlideTime.getValue() * 500) + 'ms\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowStart - konec\n')
		return

	def CSFDPosterBasicSlideShowEvent(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - zacatek\n')
		if self.PosterBasicSlideShowTimer is not None:
			if self.PosterBasicSlideShowTimer.isActive():
				self.PosterBasicSlideShowTimer.stop()
		if self.PosterBasicCountPixAllP > 0 or self.PosterBasicCountPixAllG > 0 or self.PosterBasicCountPixAllP == -1 or self.PosterBasicCountPixAllG == -1:
			noRotation = False
			if self.PosterBasicSlideList is not None:
				if not self.PosterBasicSlideStop:
					if self['poster'].instance.isVisible():
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent1 - zacatek\n')
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - poster visible: Ano\n')
						if self.PosterBasicCountPix > 0:
							LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - poster - file: ' + self.PosterBasicSlideList[self.PosterBasicActIdx][0] + '\n')
							idx = self.PosterBasicActIdx
							posterfile = self.PosterBasicSlideList[idx][0]
							chyba = False
							if posterfile[:4].upper() == 'HTTP':
								localfile = self.PosterBasicSlideList[idx][4]
								LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - poster - localfile: ' + localfile + '\n')
								if os_path.isfile(localfile):
									LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - poster - exist - localfile: ' + localfile + '\n')
									self.PosterBasicSlideList[idx][0] = self.PosterBasicSlideList[idx][4]
									posterfile = self.PosterBasicSlideList[idx][0]
								else:

									if requestFileCSFD(posterfile, localfile ) == True:
										try:
											self.PosterBasicSlideList[idx][0] = self.PosterBasicSlideList[idx][4]
											posterfile = self.PosterBasicSlideList[idx][0]
										except AttributeError:
											return
									else:
										LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - chyba - downloadposter\n')
										LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - Chyba pri stahovani posteru - url: ' + Uni8(posterfile) + '\n')
										LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - Chyba pri stahovani posteru - localfile: ' + Uni8(localfile) + '\n')
										posterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')
										chyba = True

							self.paintPosterBasicPixmap(posterfile)
							if chyba:
								if self.PosterBasicCountPixAllP != -1 and self.PosterBasicCountPixAllG != -1:
									ss = str(idx + 1) + '/' + str(self.PosterBasicCountPixAllP + self.PosterBasicCountPixAllG) + '	'
								else:
									ss = str(idx + 1) + '/' + str(self.PosterBasicCountPix) + '	 '
							elif self.PosterBasicCountPixAllP != -1 and self.PosterBasicCountPixAllG != -1:
								ss = str(idx + 1) + '/' + str(self.PosterBasicCountPixAllP + self.PosterBasicCountPixAllG) + '	' + strUni(self.PosterBasicSlideList[idx][2])
							else:
								ss = str(idx + 1) + '/' + str(self.PosterBasicCountPix) + '	 ' + strUni(self.PosterBasicSlideList[idx][2])
							self['statusbar'].setText(ss)
							self.PosterBasicActIdx += 1
							if self.PosterBasicActIdx >= self.PosterBasicCountPix:
								self.PosterBasicActIdx = 0
								if self.PosterBasicCountPixAllP != -1 and self.PosterBasicCountPixAllG != -1 and not chyba:
									cel = self.PosterBasicCountPixAllP + self.PosterBasicCountPixAllG
									if cel <= 1 and self.PosterBasicCountPix == cel:
										LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - zastavena slideshow - pouze 1 nebo zadny snimek\n')
										noRotation = True
						LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent1 - konec\n')
			if not noRotation:
				self.PosterBasicSlideShowTimer.start(config.misc.CSFD.PosterBasicSlideTime.getValue() * 500, True)
		LogCSFD.WriteToFile('[CSFD] CSFDPosterBasicSlideShowEvent - konec\n')
		return

	def CSFDGallerySlideShowStart(self):
		LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - zacatek\n')
		if self.PosterSlideShowTimer.isActive():
			self.PosterSlideShowTimer.stop()
		if self.GallerySlideShowTimer.isActive():
			self.GallerySlideShowTimer.stop()
		if config.misc.CSFD.GallerySlide.getValue():
			if self.GalleryCountPix > 0:
				idx = self.GalleryActIdx
				pol = self.GallerySlideList[idx]
				gallfile = pol[0]
				if gallfile[:4].upper() == 'HTTP':
					localfile = pol[4]
					LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - gallery - localfile: ' + localfile + '\n')
					LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - gallery - url: ' + gallfile + '\n')
					if os_path.isfile(localfile):
						LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - gallery - localfile - exist: ' + localfile + '\n')
						self.GallerySlideList[idx][0] = pol[4]
						pol = self.GallerySlideList[idx]
						gallfile = pol[0]
					else:
						if requestFileCSFD(gallfile, localfile ) == True:
							self.GallerySlideList[idx][0] = pol[4]
							pol = self.GallerySlideList[idx]
							gallfile = pol[0]
						else:
							LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - chyba - download gallerie\n')
							LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - Chyba pri stahovani gallerie - url: ' + Uni8(gallfile) + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - Chyba pri stahovani gallerie - localfile: ' + Uni8(localfile) + '\n')
							gallfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')

				self.paintGalleryPixmap(gallfile)
				ss = strUni(char2Allowchar(_('Slideshow - ')))
				ss = ss + str(idx + 1) + '/' + str(self.GalleryCountPix) + '  ' + strUni(pol[2])
				self['statusbar'].setText(ss)
				ss = str(idx + 1)
				self['page'].setText(_('Galerie č.%s' % ss))
				LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - galerie: ' + pol[0] + '\n')
				self.GallerySlideShowTimer.start(config.misc.CSFD.GallerySlideTime.getValue() * 500, True)
		LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowStart - konec\n')

	def CSFDGallerySlideShowEvent(self):
		LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - zacatek\n')
		if self.GallerySlideShowTimer is not None:
			if self.GallerySlideShowTimer.isActive():
				self.GallerySlideShowTimer.stop()
		if self.querySpecAkce == 'UserGallery':
			if not self.GallerySlideStop:
				if self['photolabel'].instance.isVisible():
					LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - gallery visible: Ano\n')
					if self.GalleryCountPix > 0:
						self.GalleryActIdx += 1
						if self.GalleryActIdx >= self.GalleryCountPix:
							self.GalleryActIdx = 0
						idx = self.GalleryActIdx
						pol = self.GallerySlideList[idx]
						gallfile = pol[0]
						if gallfile[:4].upper() == 'HTTP':
							localfile = pol[4]
							LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - gallery - localfile: ' + localfile + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - gallery - url: ' + gallfile + '\n')
							if os_path.isfile(localfile):
								LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - gallery - localfile - exist: ' + localfile + '\n')
								self.GallerySlideList[idx][0] = pol[4]
								pol = self.GallerySlideList[idx]
								gallfile = pol[0]
							else:
								if requestFileCSFD(gallfile, localfile ) == True:
									self.GallerySlideList[idx][0] = pol[4]
									pol = self.GallerySlideList[idx]
									gallfile = pol[0]
								else:
									LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - chyba - download gallerie\n')
									LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - Chyba pri stahovani gallerie - url: ' + Uni8(gallfile) + '\n')
									LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - Chyba pri stahovani gallerie - localfile: ' + Uni8(localfile) + '\n')
									gallfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')

						self.paintGalleryPixmap(gallfile)
						ss = strUni(char2Allowchar(_('Slideshow - ')))
						ss = ss + str(idx + 1) + '/' + str(self.GalleryCountPix) + '  ' + strUni(pol[2])
						self['statusbar'].setText(ss)
						ss = str(idx + 1)
						self['page'].setText(_('Galerie č.%s' % ss))
						LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - galerie: ' + pol[0] + '\n')
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - galerie visible: Ne\n')
			self.GallerySlideShowTimer.start(config.misc.CSFD.GallerySlideTime.getValue() * 500, True)
		LogCSFD.WriteToFile('[CSFD] CSFDGallerySlideShowEvent - konec\n')
		return

	def CSFDGalleryShow(self):
		LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - zacatek\n')
		if not self.GallerySlideStop:
			if self['photolabel'].instance.isVisible():
				LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - gallery visible: Ano\n')
				if self.GalleryCountPix > 0:
					idx = self.GalleryActIdx
					LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - galerie: ' + self.GallerySlideList[idx][0] + '\n')
					pol = self.GallerySlideList[idx]
					gallfile = pol[0]
					if gallfile[:4].upper() == 'HTTP':
						localfile = pol[4]
						LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - gallery - localfile: ' + localfile + '\n')
						LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - gallery - url: ' + gallfile + '\n')
						if os_path.isfile(localfile):
							LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - gallery - localfile - exist: ' + localfile + '\n')
							self.GallerySlideList[idx][0] = pol[4]
							pol = self.GallerySlideList[idx]
							gallfile = pol[0]
						else:
							if requestFileCSFD(gallfile, localfile) == True:
								self.GallerySlideList[idx][0] = pol[4]
								pol = self.GallerySlideList[idx]
								gallfile = pol[0]
							else:
								LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - chyba - download gallerie\n')
								LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - Chyba pri stahovani gallerie - url: ' + Uni8(gallfile) + '\n')
								LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - Chyba pri stahovani gallerie - localfile: ' + Uni8(localfile) + '\n')
								gallfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')

					self.paintGalleryPixmap(gallfile)
					ss = str(idx + 1) + '/' + str(self.GalleryCountPix) + '	 ' + strUni(pol[2])
					self['statusbar'].setText(ss)
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - galerie visible: Ne\n')
		LogCSFD.WriteToFile('[CSFD] CSFDGalleryShow - konec\n')

	def CSFDGalleryShowNothing(self):
		LogCSFD.WriteToFile('[CSFD] CSFDGalleryShowNothing - zacatek\n')
		if self.GallerySlideShowTimer.isActive():
			self.GallerySlideShowTimer.stop()
		Extratext = _('Galerie pořadu') + ':' + '\n\n'
		textFree = self['extralabel'].AddRowIntoText(Extratext, '')
		self['extralabel'].setTextHead(Extratext)
		Extratext = textFree
		if self.GalleryIsNotFullyRead:
			Extratext = Extratext + '\n' + _('Načítání galerie ještě probíhá. Zkuste spustit galerii za chvíli.')
		else:
			Extratext = Extratext + '\n' + _('Žádná galerie v databázi.')
		self['extralabel'].setText(Extratext)
		self['statusbar'].setText('')
		LogCSFD.WriteToFile('[CSFD] CSFDGalleryShowNothing - konec\n')

	def CSFDPosterSlideShowStart(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - zacatek\n')
		if self.GallerySlideShowTimer.isActive():
			self.GallerySlideShowTimer.stop()
		if self.PosterSlideShowTimer.isActive():
			self.PosterSlideShowTimer.stop()
		if config.misc.CSFD.PosterSlide.getValue():
			if self.PosterCountPix > 0:
				idx = self.PosterActIdx
				pol = self.PosterSlideList[idx]
				posterfile = pol[0]
				if posterfile[:4].upper() == 'HTTP':
					localfile = pol[4]
					LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - poster - localfile: ' + localfile + '\n')
					LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - poster - url: ' + posterfile + '\n')
					if os_path.isfile(localfile):
						LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - poster - localfile - exist: ' + localfile + '\n')
						self.PosterSlideList[idx][0] = pol[4]
						pol = self.PosterSlideList[idx]
						posterfile = pol[0]
					else:
						if requestFileCSFD(posterfile, localfile) == True:
							self.PosterSlideList[idx][0] = pol[4]
							pol = self.PosterSlideList[idx]
							posterfile = pol[0]
						else:
							LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - chyba - downloadposter\n')
							LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - Chyba pri stahovani posteru - url: ' + Uni8(posterfile) + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - Chyba pri stahovani posteru - localfile: ' + Uni8(localfile) + '\n')
							posterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')

				self.paintPosterPixmap(posterfile)
				ss = strUni(char2Allowchar(_('Slideshow - ')))
				ss = ss + str(idx + 1) + '/' + str(self.PosterCountPix) + '	 ' + strUni(pol[2])
				self['statusbar'].setText(ss)
				ss = str(idx + 1)
				self['page'].setText(_('Poster č.%s' % ss))
				LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - poster: ' + pol[0] + '\n')
				self.PosterSlideShowTimer.start(config.misc.CSFD.PosterSlideTime.getValue() * 500, True)
		LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowStart - konec\n')

	def CSFDPosterSlideShowEvent(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - zacatek\n')
		if self.PosterSlideShowTimer is not None:
			if self.PosterSlideShowTimer.isActive():
				self.PosterSlideShowTimer.stop()
		if self.querySpecAkce == 'UserPoster':
			if not self.PosterSlideStop:
				if self['photolabel'].instance.isVisible():
					LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster visible: Ano\n')
					if self.PosterCountPix > 0:
						self.PosterActIdx += 1
						if self.PosterActIdx >= self.PosterCountPix:
							self.PosterActIdx = 0
						idx = self.PosterActIdx
						pol = self.PosterSlideList[idx]
						posterfile = pol[0]
						if posterfile[:4].upper() == 'HTTP':
							localfile = pol[4]
							LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster - localfile: ' + localfile + '\n')
							LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster - url: ' + posterfile + '\n')
							if os_path.isfile(localfile):
								LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster - localfile - exist: ' + localfile + '\n')
								self.PosterSlideList[idx][0] = pol[4]
								pol = self.PosterSlideList[idx]
								posterfile = pol[0]
							else:
								if requestFileCSFD(posterfile, localfile) == True:
									self.PosterSlideList[idx][0] = pol[4]
									pol = self.PosterSlideList[idx]
									posterfile = pol[0]
								else:
									LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - chyba - downloadposter\n')
									LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - Chyba pri stahovani posteru - url: ' + Uni8(posterfile) + '\n')
									LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - Chyba pri stahovani posteru - localfile: ' + Uni8(localfile) + '\n')
									posterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')
									err = traceback.format_exc()
									LogCSFD.WriteToFile(err)

						self.paintPosterPixmap(posterfile)
						ss = strUni(char2Allowchar(_('Slideshow - ')))
						ss = ss + str(idx + 1) + '/' + str(self.PosterCountPix) + '	 ' + strUni(pol[2])
						self['statusbar'].setText(ss)
						ss = str(idx + 1)
						self['page'].setText(_('Poster č.%s' % ss))
						LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster: ' + pol[0] + '\n')
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - poster visible: Ne\n')
			self.PosterSlideShowTimer.start(config.misc.CSFD.PosterSlideTime.getValue() * 500, True)
		LogCSFD.WriteToFile('[CSFD] CSFDPosterSlideShowEvent - konec\n')
		return

	def CSFDPosterShow(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - zacatek\n')
		if not self.PosterSlideStop:
			if self['photolabel'].instance.isVisible():
				LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster visible: Ano\n')
				if self.PosterCountPix > 0:
					idx = self.PosterActIdx
					LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster: ' + self.PosterSlideList[idx][0] + '\n')
					pol = self.PosterSlideList[idx]
					posterfile = pol[0]
					if posterfile[:4].upper() == 'HTTP':
						localfile = pol[4]
						LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster - localfile: ' + localfile + '\n')
						LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster - url: ' + posterfile + '\n')
						if os_path.isfile(localfile):
							LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster - localfile - exist: ' + localfile + '\n')
							self.PosterSlideList[idx][0] = pol[4]
							pol = self.PosterSlideList[idx]
							posterfile = pol[0]
						else:
							if requestFileCSFD(posterfile, localfile) == True:
								self.PosterSlideList[idx][0] = pol[4]
								pol = self.PosterSlideList[idx]
								posterfile = pol[0]
							else:
								LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - chyba - downloadposter\n')
								LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - Chyba pri stahovani posteru - url: ' + Uni8(posterfile) + '\n')
								LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - Chyba pri stahovani posteru - localfile: ' + Uni8(localfile) + '\n')
								posterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/no_poster.png')

					self.paintPosterPixmap(posterfile)
					ss = str(idx + 1) + '/' + str(self.PosterCountPix) + '	' + strUni(pol[2])
					self['statusbar'].setText(ss)
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - poster visible: Ne\n')
		LogCSFD.WriteToFile('[CSFD] CSFDPosterShow - konec\n')

	def CSFDPosterShowNothing(self):
		LogCSFD.WriteToFile('[CSFD] CSFDPosterShowNothing - zacatek\n')
		if self.PosterSlideShowTimer.isActive():
			self.PosterSlideShowTimer.stop()
		Extratext = _('Postery pořadu') + ':' + '\n\n'
		textFree = self['extralabel'].AddRowIntoText(Extratext, '')
		self['extralabel'].setTextHead(Extratext)
		Extratext = textFree
		if self.PosterIsNotFullyRead:
			Extratext = Extratext + '\n' + _('Načítání posterů ještě probíhá. Zkuste spustit postery za chvíli.')
		else:
			Extratext = Extratext + '\n' + _('Žádná postery v databázi.')
		self['extralabel'].setText(Extratext)
		self['statusbar'].setText('')
		LogCSFD.WriteToFile('[CSFD] CSFDPosterShowNothing - konec\n')

	def CSFDVideoShow(self):
		LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - zacatek\n')
		if self['photolabel'].instance.isVisible():
			LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - video visible: Ano\n')
			if self.VideoCountPix > 0:
				idx = self.VideoActIdx
				pol = self.VideoSlideList[idx]
				LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - video: ' + pol[6] + '\n')
				videoposterfile = pol[6]
				znovu = False
				if videoposterfile[:4].upper() == 'HTTP':
					localfile = pol[8]
					LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - video poster - localfile: ' + localfile + '\n')
					LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - video poster - url: ' + videoposterfile + '\n')

					idx1 = idx
					if requestFileCSFD(videoposterfile, localfile) == True:
						if videoposterfile == self.VideoSlideList[idx1][6]:
							self.VideoSlideList[idx1][6] = localfile
							videoposterfile = localfile
						else:
							LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - spatne prirazeny stahnuty video poster - zkousim znovu\n')
							znovu = True
							videoposterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')
						idx = idx1
					else:
						LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - chyba - download video posteru\n')
						LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - Chyba pri stahovani video posteru - url: ' + Uni8(videoposterfile) + '\n')
						LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - Chyba pri stahovani video posteru - localfile: ' + Uni8(localfile) + '\n')
						videoposterfile = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/csfdnothing.png')

				self.paintVideoPixmap(videoposterfile)
				ss = str(idx + 1) + '/' + str(self.VideoCountPix) + '  ' + strUni(self.VideoSlideList[idx][2])
				self['statusbar'].setText(ss)
				if znovu:
					self.CSFDVideoShow()
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - video visible: Ne\n')
		LogCSFD.WriteToFile('[CSFD] CSFDVideoShow - konec\n')

	def CSFDVideoShowNothing(self):
		LogCSFD.WriteToFile('[CSFD] CSFDVideoShowNothing - zacatek\n')
		Extratext = _('Videa v pořadu') + ':' + '\n\n'
		textFree = self['extralabel'].AddRowIntoText(Extratext, '')
		self['extralabel'].setTextHead(Extratext)
		Extratext = textFree
		if self.VideoIsNotFullyRead:
			Extratext = Extratext + '\n' + _('Načítání videí ještě probíhá...')
		else:
			Extratext = Extratext + '\n' + _('Žádná videa v databázi.')
		self['extralabel'].setText(Extratext)
		self['statusbar'].setText('')
		LogCSFD.WriteToFile('[CSFD] CSFDVideoShowNothing - konec\n')

	def CSFDshowVideoInfo(self):
		LogCSFD.WriteToFile('[CSFD] CSFDshowVideoInfo - zacatek\n')
		self.CSFDopenVideoInfoScreen()
		LogCSFD.WriteToFile('[CSFD] CSFDshowVideoInfo - konec\n')

	def CSFDopenVideoInfoScreen(self):
		LogCSFD.WriteToFile('[CSFD] CSFDopenInfoScreen - zacatek\n')
		acname = strUni(self.ActName)
		self.session.open(CSFDVideoInfoScreen, self.VideoSlideList[self.VideoActIdx], self.videoklipurl, self.videotitulkyurl, acname, GetItemColourRateN(self.ratingstars))
		LogCSFD.WriteToFile('[CSFD] CSFDopenInfoScreen - konec\n')

	def DownloadParalel(self):
		LogCSFD.WriteToFile('[CSFD] DownloadParalel - zacatek\n')
		if self.DownloadTimer is not None:
			if self.DownloadTimer.isActive():
				self.DownloadTimer.stop()
		runProc, runPage = CSFDGlobalVar.getParalelDownload()
		if runProc is not None:
			runProc(runPage)
		LogCSFD.WriteToFile('[CSFD] DownloadParalel - konec\n')
		return

	def TestLoginToCSFD(self, workingConfig=None):
		LogCSFD.WriteToFile('[CSFD] TestLoginToCSFD - zacatek\n', 9)

		self.workingConfig = workingConfig
		self.session.openWithCallback(self.finishedTestLoginToCSFD, CSFDConsole, title=_('Test přihlášení na CSFD.cz ...'), cmdlist=None, startCallback=self.TestLoginToCSFD1, closeOnSuccess=False, startNow=False, startText=_('Test přihlášení na CSFD.cz - ZAČÁTEK'), endText=_('Test přihlášení na CSFD.cz - KONEC'))
		LogCSFD.WriteToFile('[CSFD] TestLoginToCSFD - konec\n', 9)
		return

	def TestLoginToCSFD1(self, console=None):
		LogCSFD.WriteToFile('[CSFD] TestLoginToCSFD1 - zacatek\n', 9)
		
		txt = _('Je povoleno přihlašování do CSFD v Nastaveních')
		if not config.misc.CSFD.LoginToCSFD.getValue():
			txt += ' ..... ERR\n'
		else:
			txt += ' ..... OK\n'
		console.addText(text=txt, typeText=0)
		LogCSFD.WriteToFile(txt, 9)

		txt = _('Je vyplněno uživatelské jméno v Nastaveních')
		ss = config.misc.CSFD.UserNameCSFD.getValue()
		if ss is not None and ss != '':
			txt += ' ..... OK\n'
			txt += _('Uživatel: ') + strUni(ss) + '\n'
		else:
			txt += ' ..... ERR\n'
		console.addText(text=txt, typeText=0)
		LogCSFD.WriteToFile(txt, 9)

		txt = _('Je vyplněno heslo v Nastaveních')
		ss = config.misc.CSFD.PasswordCSFD.getValue()
		if ss is not None and ss != '':
			txt += ' ..... OK\n'
			console.addText(text=txt, typeText=0)
			LogCSFD.WriteToFile(txt, 9)
			txt += _('Heslo: ') + strUni(ss) + '\n'
		else:
			txt += ' ..... ERR\n'
			console.addText(text=txt, typeText=0)
			LogCSFD.WriteToFile(txt, 9)

		txt = _('Je funkční internet')
		if internet_on():
			txt += ' ..... OK\n'
		else:
			txt += ' ..... ERR\n'
		console.addText(text=txt, typeText=0)
		LogCSFD.WriteToFile(txt, 9)

		txt = _('Zkouším funkčnost přihlášení')
		if csfdAndroidClient.is_logged():
			txt += ' ..... OK\n'
			console.addText(text=txt, typeText=0)
			LogCSFD.WriteToFile(txt, 9)
		else:
			txt += ' ..... ERR\n'
			console.addText(text=txt, typeText=0)
			LogCSFD.WriteToFile(txt, 9)

			txt = _('Zkouším se zalogovat na stránky CSFD')
			CreateCSFDAndroidClient( True )
			
			if csfdAndroidClient.is_logged():
				txt += ' ..... OK\n'
			else:
				txt += ' ..... ERR\n'
	
			console.addText(text=txt, typeText=0)
			LogCSFD.WriteToFile(txt, 9)
		
		txt = _('Ověřuji přihlášení na CSFD')
		if csfdAndroidClient.get_user_identity() != None:
			txt += ' ..... OK\n'
		else:
			txt += ' ..... ERR\n'
			txt += _('Resetuju přihlašovací token - zkuste spustit tenhle test ješte jednou') + '\n'
			csfdAndroidClient.logout()
			config.misc.CSFD.TokenCSFD.setValue('')
			config.misc.CSFD.TokenCSFD.save()
			
		console.addText(text=txt, typeText=0)
		LogCSFD.WriteToFile(txt, 9)

		txt = _('Zjišťuji zalogovaného uživatele na CSFD')
		loggedUser = False
		user = csfdAndroidClient.get_logged_user()[0]
		if user is not None and user != '':
			loggedUser = True
			txt += ' ..... OK\n'
			txt += _('Zalogovaný uživatel je: ') + strUni(user) + '\n'
		else:
			txt += ' ..... ERR\n'
		console.addText(text=txt, typeText=0)
		LogCSFD.WriteToFile(txt, 9)

		if loggedUser:
			txt = '\n' + _('TEST PROBĚHL ÚSPĚŠNĚ') + '\n' + _('Můžete hodnotit filmy na CSFD')
			if not config.misc.CSFD.LoginToCSFD.getValue():
				txt += ' - ' + _('pokud to povolíte v Nastaveních')
			txt += '\n'
			console.addText(text=txt, typeText=2)
			console.setReturnValue(0)
			LogCSFD.WriteToFile(txt, 9)

			config.misc.CSFD.LastLoginError.setValue(int(0))
			config.misc.CSFD.LastLanError.setValue(int(0))
			config.misc.CSFD.LastLanError.save()
		else:
			txt = '\n' + _('TEST BOHUŽEL NEPROBĚHL ÚSPĚŠNĚ') + '\n' + _('opravte nalezené chyby !!!') + '\n'
			console.addText(text=txt, typeText=2)
			console.setReturnValue(1)
			LogCSFD.WriteToFile(txt, 9)

			config.misc.CSFD.LastLoginError.setValue(int(time.time()))
		config.misc.CSFD.LastLoginError.save()
		configfile.save()
		console.startRun()
		LogCSFD.WriteToFile('[CSFD] TestLoginToCSFD1 - konec\n', 9)
		return

	def finishedTestLoginToCSFD(self, retval=0):
		LogCSFD.WriteToFile('[CSFD] finishedTestLoginToCSFD - zacatek\n', 9)
		LogCSFD.WriteToFile('[CSFD] finishedTestLoginToCSFD - retval: %s\n' % str(retval), 9)
		if retval == 0:
			LogCSFD.WriteToFile('[CSFD] finishedTestLoginToCSFD - OK\n', 9)
		else:
			LogCSFD.WriteToFile('[CSFD] finishedTestLoginToCSFD - chyba\n', 9)
		if self.workingConfig is not None:
			self.workingConfig.showInputHelp()
			self.workingConfig = None
		LogCSFD.WriteToFile('[CSFD] finishedTestLoginToCSFD - konec\n', 9)
		return

	def LoadIMDBTimerEvent(self):
		LogCSFD.WriteToFile('[CSFD] LoadIMDBTimerEvent - zacatek\n', 10)
		if self.LoadIMDBTimer is not None:
			if self.LoadIMDBTimer.isActive():
				self.LoadIMDBTimer.stop()
		if self.IMDBpath != '':
			downl_timeout = config.misc.CSFD.DownloadTimeOut.getValue()
			LogCSFD.WriteToFile('[CSFD] LoadIMDBTimerEvent - stahuji z url ' + Uni8(self.IMDBpath) + '\n')
			try:
				result = request(self.IMDBpath, headers=std_media_header, timeout=downl_timeout)
				LogCSFD.WriteToFile('[CSFD] LoadIMDBTimerEvent - OK\n', 8)
			except:
				result = ''
				LogCSFD.WriteToFile('[CSFD] LoadIMDBTimerEvent - chyba\n', 8)
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err, 8)

			if result != '':
				ParserIMDB.setHTML2utf8(result)
				self.ratingstarsIMDB = ParserIMDB.parserIMDBRatingStars()
				self.ratingtextIMDB = _('IMDb:') + ' '
				if self.ratingstarsIMDB >= 0:
					self.ratingtextIMDB += str(self.ratingstarsIMDB) + '% '
				self.ratingstarsMetacritic = ParserIMDB.parserMetacriticRatingStars()
				self.ratingtextMetacritic = _('Metacritic:') + ' '
				if self.ratingstarsMetacritic >= 0:
					self.ratingtextMetacritic += str(self.ratingstarsMetacritic) + '% '
				vv = ParserIMDB.parserIMDBRatingNumber()
				if vv is not None:
					self.ratingtextIMDB += '(' + intWithSeparator(vv) + ')'
				vv = ParserIMDB.parserMetacriticRatingNumber()
				if vv is not None:
					self.ratingtextMetacritic += '(' + intWithSeparator(vv) + ')'
				else:
					self.ratingtextMetacritic += '	   '
				ParserIMDB.resetValues()
			else:
				self.ratingstarsIMDB = -1
				self.ratingtextIMDB = ''
		else:
			self.ratingstarsIMDB = -1
			self.ratingtextIMDB = ''
		LogCSFD.WriteToFile('[CSFD] LoadIMDBTimerEvent - konec\n', 10)
		return

	def NewVersionTimerEvent(self):
		LogCSFD.WriteToFile('[CSFD] NewVersionTimerEvent - zacatek\n', 10)
		if self.NewVersionTimer is not None:
			if self.NewVersionTimer.isActive():
				self.NewVersionTimer.stop()
		self.automaticUpdate = True
		self.CheckForUpdate()
		LogCSFD.WriteToFile('[CSFD] NewVersionTimerEvent - konec\n', 10)
		return

	def IsTimeForNewVersionCheck(self):
		LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck - zacatek\n', 10)
		check = False
		if int(time.time()) - config.misc.CSFD.LastLanError.getValue() < config.misc.CSFD.LanErrorWaiting.getValue() * 60:
			LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck: Ne - jeste nevyprsel casovy limit z duvodu lan chyby\n', 10)
			LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck - konec\n', 10)
			return check
		last = config.misc.CSFD.LastVersionCheck.getValue()
		now = int(time.time())
		if now - last > 86400:
			check = True
			LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck: Ano\n', 10)
			config.misc.CSFD.LastVersionCheck.setValue(int(time.time()))
			config.misc.CSFD.LastVersionCheck.save()
		else:
			check = False
			LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck: Ne\n', 10)
		LogCSFD.WriteToFile('[CSFD] IsTimeForNewVersionCheck - konec\n', 10)
		return check

	def CheckForUpdate(self):
		LogCSFD.WriteToFile('[CSFD] CheckForUpdate - zacatek\n', 10)

		config.misc.CSFD.LastVersionCheck.setValue(int(time.time()))
		config.misc.CSFD.LastVersionCheck.save()
		self.UpdateViaCURL()
		LogCSFD.WriteToFile('[CSFD] CheckForUpdate - konec\n', 10)

	def UpdateViaCURL(self):
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURL - zacatek\n', 10)
		if config.misc.CSFD.AutomaticBetaVersionCheck.getValue():
			LogCSFD.WriteToFile('[CSFD] UpdateViaCURL - aktualizace beta verzi - zapnuta\n', 10)
			url = MainUpdateUrl + 'versionbeta.txt'
			output = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDversionbeta.txt'
		else:
			url = MainUpdateUrl + 'version.txt'
			output = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDversion.txt'
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURL - stahuji soubor verzi ' + url + ' do ' + output + '\n', 10)
		self.container_output = ''
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.container.appClosed.append(self.UpdateViaCURLfinished)
			self.appClosed_conn = None
		else:
			self.appClosed_conn = self.container.appClosed.connect(self.UpdateViaCURLfinished)
		exc = 'curl -m 10 -k -L -o ' + output + ' ' + url
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURL - instalacni prikaz: ' + exc + '\n', 10)
		LogCSFD.WriteToFileWithoutTime(exc + '\n')
		self.container.execute(exc)
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURL - konec\n', 10)
		return

	def UpdateViaCURLfinished(self, retval):
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - zacatek\n', 10)
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - retval: %s\n' % str(retval), 10)
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - container_output:\n', 10)
		LogCSFD.WriteToFileWithoutTime(self.container_output)
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.container.appClosed.remove(self.UpdateViaCURLfinished)
			self.appClosed_conn = None
		else:
			self.appClosed_conn = None
		if retval == 0:
			LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - OK - pri stahovani souboru verzi\n', 10)
			self.ReadUpdateInformation()
		else:
			LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - chyba - pri stahovani souboru verzi\n', 10)
			if not self.automaticUpdate:
				self.session.open(MessageBox, _('Informace o nové verzi není momentálně dostupná nebo došlo k síťové chybě (curl)'), type=MessageBox.TYPE_INFO, timeout=10)
		LogCSFD.WriteToFile('[CSFD] UpdateViaCURLfinished - konec\n', 10)
		return

	def ReadUpdateInformation(self):
		LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - zacatek\n', 10)
		chyba = False
		if config.misc.CSFD.AutomaticBetaVersionCheck.getValue():
			LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - aktualizace beta verzi - zapnuta\n', 10)
			file_ver = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDversionbeta.txt'
		else:
			file_ver = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDversion.txt'
		try:
			text_file = open(file_ver, 'r')
			tmp_infolines = text_file.readlines()
			text_file.close()
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - chyba - pri praci se souborem - ' + file_ver + '\n', 10)
			LogCSFD.WriteToFile(err, 10)
			chyba = True

		if chyba:
			self.session.open(MessageBox, _('Při aktualizaci došlo k chybě'), type=MessageBox.TYPE_INFO, timeout=10)
		else:
			remoteversion = char2AllowcharNumbers(tmp_infolines[0]).strip()
			nameUpdateFile = char2Allowchar(tmp_infolines[1]).strip()
			if remoteversion == '' or nameUpdateFile == '':
				self.session.open(MessageBox, _('Při aktualizaci došlo k chybě'), type=MessageBox.TYPE_INFO, timeout=10)
			else:
				if nameUpdateFile.rfind('.ipk') >= 0:
					if CSFDGlobalVar.getCSFDInstallCommand() == 'dpkg':
						nameUpdateFile = nameUpdateFile.replace('.ipk', '.deb')
				else:
					if nameUpdateFile.rfind('.deb') >= 0:
						if CSFDGlobalVar.getCSFDInstallCommand() != 'dpkg':
							nameUpdateFile = nameUpdateFile.replace('.deb', '.ipk')
					elif CSFDGlobalVar.getCSFDInstallCommand() == 'dpkg':
						nameUpdateFile += '.deb'
					else:
						nameUpdateFile += '.ipk'
					
				self.UpdateUrl = str(MainUpdateUrlIpk + 'v' + remoteversion + '/'  + nameUpdateFile.strip())
				self.UpdateFile = str(CSFDGlobalVar.getCSFDadresarTMP() + nameUpdateFile.strip())
				popis = ''
				for index, value in enumerate(tmp_infolines):
					if index > 1:
						popis += char2Allowchar(value).strip() + '\n'

				old_V = Uni8(config.misc.CSFD.Version.getValue()).rjust(10, '0')
				new_V = Uni8(remoteversion).rjust(10, '0')
				LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - akt. verze: %s\n' % old_V, 10)
				LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - nova verze: %s\n' % new_V, 10)
				LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - UpdateUrl %s\n' % Uni8(self.UpdateUrl), 10)
				LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - UpdateFile %s\n' % Uni8(self.UpdateFile), 10)
				if old_V < new_V:
					self.session.openWithCallback(self.startPluginUpdateCallback, MessageBox, (_('Je dostupná nová verze CSFD pluginu %s na githubu') + '\n(' + strUni(config.misc.CSFD.Version.getValue()) + ' --> ' + strUni(remoteversion) + ')\n' + strUni(popis) + '\n' + _('Chcete ji stáhnout a nainstalovat?')) % strUni(remoteversion), MessageBox.TYPE_YESNO)
				elif not self.automaticUpdate:
					if old_V == new_V:
						self.session.openWithCallback(self.startPluginUpdateCallback, MessageBox, _('Máte nainstalovanou aktuální verzi pluginu!') + '\n' + _('Chcete plugin přesto znovu stáhnout a nainstalovat?') + '\n(' + _('verze:') + ' ' + strUni(remoteversion) + ')', MessageBox.TYPE_YESNO, default=False)
					elif old_V > new_V:
						self.session.openWithCallback(self.startPluginUpdateCallback, MessageBox, _('Máte nainstalovanou novější verzi pluginu než je aktuálně online dostupná!') + '\n' + _('Chcete přesto stáhnout a nainstalovat tuto starší verzi?') + '\n' + _('Stahovaná verze:') + ' ' + strUni(remoteversion) + '\n' + _('Vaše verze:') + ' ' + strUni(config.misc.CSFD.Version.getValue()), MessageBox.TYPE_YESNO, default=False)
		LogCSFD.WriteToFile('[CSFD] ReadUpdateInformation - konec\n', 10)

	def startPluginUpdateCallback(self, answer):
		LogCSFD.WriteToFile('[CSFD] startPluginUpdateCallback - zacatek\n', 10)
		if answer is True:
			self.startPluginDownloadAndUpdate()
		LogCSFD.WriteToFile('[CSFD] startPluginUpdateCallback - konec\n', 10)

	def startPluginDownloadAndUpdate(self):
		LogCSFD.WriteToFile('[CSFD] startPluginDownloadAndUpdate - zacatek\n', 10)
		cmd = []

		cmd.append('curl -k -L -o ' + self.UpdateFile + ' ' + self.UpdateUrl)
		if CSFDGlobalVar.getCSFDInstallCommand() == 'dpkg':
			cmd.append(CSFDGlobalVar.getCSFDInstallCommand() + ' --install --force-all ' + str(self.UpdateFile) + ' && apt-get -y update && apt-get -f -y install')
		else:
			cmd.append(CSFDGlobalVar.getCSFDInstallCommand() + ' install --force-overwrite --force-depends --force-downgrade ' + str(self.UpdateFile))
		self.session.openWithCallback(self.finishedPluginDownloadAndUpdate, CSFDConsole, title=_('Online update pluginu ...'), cmdlist=cmd, closeOnSuccess=False, startText=_('Stažení a instalace nové verze pluginu - ZAČÁTEK'), endText=_('Stažení a instalace nové verze pluginu - KONEC'))
		
		LogCSFD.WriteToFile('[CSFD] startPluginDownloadAndUpdate - konec\n', 10)

	def finishedPluginDownloadAndUpdate(self, retval=0):
		LogCSFD.WriteToFile('[CSFD] finishedPluginDownloadAndUpdate - zacatek\n', 10)
		LogCSFD.WriteToFile('[CSFD] finishedPluginDownloadAndUpdate - retval: %s\n' % str(retval), 10)
		if retval == 0:
			LogCSFD.WriteToFile('[CSFD] finishedPluginDownloadAndUpdate - OK - pri instalaci nove verze\n', 10)
			self.session.openWithCallback(self.restartGUI, MessageBox, _('Nová verze byla úspěšně nainstalována!') + '\n' + _('Chcete nyní provést restart GUI?'), MessageBox.TYPE_YESNO)
		else:
			LogCSFD.WriteToFile('[CSFD] finishedPluginDownloadAndUpdate - chyba - pri instalaci nove verze\n', 10)
			self.session.openWithCallback(self.restartGUI, MessageBox, (_('Instalace skončila s kódem (%s)!') + '\n' + _('Chcete nyní provést restart GUI?')) % str(retval), MessageBox.TYPE_YESNO)
		LogCSFD.WriteToFile('[CSFD] finishedPluginDownloadAndUpdate - konec\n', 10)

	def restartGUI(self, answer):
		LogCSFD.WriteToFile('[CSFD] restartGUI - zacatek\n')
		if answer is True:
			LogCSFD.WriteToFile('[CSFD] restartGUI - ano\n')
			LogCSFD.WriteToFile('[CSFD] restartGUI - konec\n')
			self.session.open(TryQuitMainloop, 3)
		else:
			LogCSFD.WriteToFile('[CSFD] restartGUI - konec\n')

	def consoleAppContainer_avail(self, string):
		self.container_output += string.decode("utf-8")

	def ResetAllCSFDParams(self, workingConfig=None):
		LogCSFD.WriteToFile('[CSFD] ResetAllCSFDParams - zacatek\n')
		self.workingConfig = workingConfig
		self.session.openWithCallback(self.answerResetAllCSFDParams, MessageBox, _('Chcete nastavit všechny parametry na přednastavené (default) hodnoty?'), MessageBox.TYPE_YESNO)
		LogCSFD.WriteToFile('[CSFD] ResetAllCSFDParams - konec\n')

	def answerResetAllCSFDParams(self, answer):
		LogCSFD.WriteToFile('[CSFD] answerResetAllCSFDParams - zacatek\n')
		if answer is True:
			self.runResetAllCSFDParams()
		elif self.workingConfig is not None:
			self.workingConfig.showInputHelp()
			self.workingConfig = None
		LogCSFD.WriteToFile('[CSFD] answerResetAllCSFDParams - konec\n')
		return

	def runResetAllCSFDParams(self):
		LogCSFD.WriteToFile('[CSFD] runResetAllCSFDParams - zacatek\n')
		ResetParams()
		RefreshPlugins()
		self.session.openWithCallback(self.finalResetAllCSFDParams, MessageBox, _('Všechny parametry byly nastaveny na přednastavené hodnoty!\nSpusťte znovu plugin!'), type=MessageBox.TYPE_INFO, timeout=10)
		LogCSFD.WriteToFile('[CSFD] runResetAllCSFDParams - konec\n')

	def finalResetAllCSFDParams(self, answer=None):
		LogCSFD.WriteToFile('[CSFD] finalResetAllCSFDParams - zacatek\n')
		if self.workingConfig is not None:
			self.workingConfig.updateAllPars()
			self.workingConfig = None
		LogCSFD.WriteToFile('[CSFD] finalResetAllCSFDParams - konec\n')
		return

	def createSummary(self):
		return CSFDLCDSummary


LogCSFD.WriteToFile('[CSFD] Iniciace modulu CSFD.py* - konec\n')

# -*- coding: utf-8 -*-

from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigSelection, ConfigInteger, configfile, NoSave
from CSFDConfigText import CSFDConfigText, CSFDConfigPassword
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import environ as os_environ, path as os_path
from datetime import datetime
from CSFDLog import LogCSFD
from CSFDSettings1 import CSFDGlobalVar
import gettext, locale
CSFDVersion='15.00'
CSFDVersionData='05.01.2022'
config.misc.CSFD = ConfigSubsection()
config.misc.CSFD.Log = ConfigYesNo(default=True)
config.misc.CSFD.LogConsole = ConfigYesNo(default=False)
config.misc.CSFD.LogConsoleTime = ConfigYesNo(default=False)
config.misc.CSFD.LogMaxSize = ConfigSelection(choices=[('50000', '50kB'), ('100000', '100kB'), ('200000', '200kB'), ('300000', '300kB'), ('400000', '400kB'), ('500000', '500kB'), ('1000000', '1MB')], default='300000')
config.misc.CSFD.Language = ConfigSelection(choices=[('0', _('automaticky')), ('1', _('česky')), ('2', _('slovensky'))], default='0')
config.misc.CSFD.Resolution = ConfigSelection(choices=[('0', _('automaticky')), ('720', _('720')), ('1280', _('1280')), ('1920', _('1920'))], default='0')
config.misc.CSFD.DirectoryTMP = CSFDConfigText('/tmp/', fixed_size=False)
config.misc.CSFD.LastVersionCheck = ConfigInteger(default=0, limits=(0, 99999999999))
config.misc.CSFD.LastLanError = ConfigInteger(default=0, limits=(0, 99999999999))
config.misc.CSFD.LastLoginError = ConfigInteger(default=0, limits=(0, 99999999999))
config.misc.CSFD.LanErrorWaiting = ConfigInteger(default=10, limits=(1, 240))
config.misc.CSFD.LoginErrorWaiting = ConfigInteger(default=10, limits=(1, 240))
config.misc.CSFD.AutomaticVersionCheck = ConfigYesNo(default=True)
config.misc.CSFD.AutomaticBetaVersionCheck = ConfigYesNo(default=False)
config.misc.CSFD.TestVersion = ConfigYesNo(default=False)
config.misc.CSFD.CurrentSkin = CSFDConfigText('Default', fixed_size=False)
config.misc.CSFD.Version = NoSave(CSFDConfigText(default=CSFDVersion))
config.misc.CSFD.VersionData = NoSave(CSFDConfigText(default=CSFDVersionData))
const_www_csfd = '://www.csfd.cz'
const_csfd_http_film = '://www.csfd.cz/film/'
const_quick_page = 'komentare/strana-300/'
std_headers = {'Host': 'www.csfd.cz', 
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0', 
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
   'Accept-Language': 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3', 
   'Accept-Encoding': 'gzip', 
   'DNT': '1', 
   'Referer': 'https://www.csfd.cz/', 
   'Connection': 'keep-alive'}
std_headers_UL2 = [
 ('Host', 'www.csfd.cz'),
 ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'),
 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
 ('Accept-Language', 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3'),
 ('Accept-Encoding', 'gzip'),
 ('DNT', '1'),
 ('Referer', 'https://www.csfd.cz/'),
 ('Connection', 'keep-alive')]
std_media_header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
std_media_header_UL2 = [
 ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0')]
std_post_header = {'Host': 'www.csfd.cz', 
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0', 
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
   'Accept-Language': 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3', 
   'Accept-Encoding': 'gzip', 
   'DNT': '1', 
   'Referer': 'https://www.csfd.cz/', 
   'Connection': 'keep-alive', 
   'Content-Type': 'application/x-www-form-urlencoded', 
   'Content-Length': '75'}
std_post_header_UL2 = [
 ('Host', 'www.csfd.cz'),
 ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'),
 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
 ('Accept-Language', 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3'),
 ('Accept-Encoding', 'gzip'),
 ('DNT', '1'),
 ('Referer', 'https://www.csfd.cz/'),
 ('Connection', 'keep-alive'),
 ('Content-Type', 'application/x-www-form-urlencoded'),
 ('Content-Length', '75')]
std_tv_post_header = {'Host': 'www.csfd.cz', 
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0', 
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
   'Accept-Language': 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3', 
   'Accept-Encoding': 'gzip', 
   'DNT': '1', 
   'Referer': 'https://www.csfd.cz/televize/', 
   'Connection': 'keep-alive', 
   'Content-Type': 'application/x-www-form-urlencoded'}
std_tv_post_header_UL2 = [
 ('Host', 'www.csfd.cz'),
 ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'),
 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
 ('Accept-Language', 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3'),
 ('Accept-Encoding', 'gzip'),
 ('DNT', '1'),
 ('Referer', 'https://www.csfd.cz/televize/'),
 ('Connection', 'keep-alive'),
 ('Content-Type', 'application/x-www-form-urlencoded')]
std_login_header = {'Host': 'www.csfd.cz', 
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0', 
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
   'Accept-Language': 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3', 
   'Accept-Encoding': 'gzip', 
   'DNT': '1', 
   'Referer': 'https://www.csfd.cz/prihlaseni/', 
   'Connection': 'keep-alive', 
   'Content-Type': 'application/x-www-form-urlencoded'}
std_login_header_UL2 = [
 ('Host', 'www.csfd.cz'),
 ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'),
 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
 ('Accept-Language', 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3'),
 ('Accept-Encoding', 'gzip'),
 ('DNT', '1'),
 ('Referer', 'https://www.csfd.cz/prihlaseni/'),
 ('Connection', 'keep-alive'),
 ('Content-Type', 'application/x-www-form-urlencoded')]

# MainUpdateUrl = 'http://downloads.tvplugins.cz/csfd/'
MainUpdateUrl = 'https://raw.githubusercontent.com/skyjet18/enigma2-plugin-extensions-csfd/master/'
MainUpdateUrlIpk = 'https://github.com/skyjet18/enigma2-plugin-extensions-csfd/releases/download/'

def PathTMPInit():
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - PathTMPInit - zacatek\n')
	if os_path.exists(config.misc.CSFD.DirectoryTMP.getValue()):
		CSFDGlobalVar.setCSFDadresarTMP(config.misc.CSFD.DirectoryTMP.getValue())
	else:
		CSFDGlobalVar.setCSFDadresarTMP('/tmp/')
		config.misc.CSFD.DirectoryTMP.setValue('/tmp/')
		config.misc.CSFD.DirectoryTMP.save()
		configfile.save()
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - PathTMPInit - konec\n')


PathTMPInit()

def localeInit():
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - zacatek\n')
	if config.misc.CSFD.Language.getValue() == '0':
		lang = language.getLanguage()[:2]
		LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - automaticky ' + lang + '\n')
	else:
		if config.misc.CSFD.Language.getValue() == '2':
			lang = 'sk'
			LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - volba ' + lang + '\n')
		else:
			lang = 'cs'
			LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - volba ' + lang + '\n')
		os_environ['LANGUAGE'] = lang
		gettext.bindtextdomain('CSFD', resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/locale'))
		CSFDGlobalVar.setCSFDlang(lang)
		try:
			if lang == 'cs':
				locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')
				LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - LC_ALL nastaveno na cs_CZ.UTF-8\n')
				print(datetime.now().strftime('CSFD Init - Dnes je %A %d. %B %Y'))
				LogCSFD.WriteToFile(datetime.now().strftime('CSFD Init - Dnes je %A %d. %B %Y') + '\\u')
			elif lang == 'sk':
				locale.setlocale(locale.LC_ALL, 'sk_SK.UTF-8')
				LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - LC_ALL nastaveno na sk_SK.UTF-8\n')
				print(datetime.now().strftime('CSFD Init - Dnes je %A %d. %B %Y'))
				LogCSFD.WriteToFile(datetime.now().strftime('CSFD Init - Dnes je %A %d. %B %Y') + '\\u')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - nepodarilo se nastavit LC_ALL\n')

	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - nastaveno ' + lang + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - localeInit - konec\n')


if CSFDGlobalVar.getCSFDlang() is None:
	localeInit()
	language.addCallback(localeInit)

def _(txt):
	t = gettext.dgettext('CSFD', txt.decode('utf-8'))
	if t == txt:
		t = t.encode('utf-8')
	t = str(t)
	return t


config.misc.CSFD.Detail100 = ConfigYesNo(default=True)
config.misc.CSFD.PosterBasic = ConfigYesNo(default=True)
config.misc.CSFD.SaveSearch = ConfigYesNo(default=False)
config.misc.CSFD.InputSearch = CSFDConfigText('', fixed_size=False)
config.misc.CSFD.ShowInMenuStart = ConfigYesNo(default=False)
config.misc.CSFD.ShowInEPGSubMenu = ConfigYesNo(default=False)
config.misc.CSFD.ShowInPluginMenu = ConfigYesNo(default=True)
config.misc.CSFD.ShowInEventInfoMenu = ConfigYesNo(default=True)
config.misc.CSFD.ShowInExtensionMenu = ConfigYesNo(default=True)
config.misc.CSFD.ShowInATV = ConfigYesNo(default=True)
config.misc.CSFD.ShowInInfoBar = ConfigYesNo(default=True)
config.misc.CSFD.FindAllItems = ConfigYesNo(default=False)
config.misc.CSFD.FindInclYear = ConfigYesNo(default=True)
config.misc.CSFD.CompareInclYear = ConfigYesNo(default=True)
config.misc.CSFD.ReadDetailBasedOnScore = ConfigYesNo(default=True)
config.misc.CSFD.FindInclDiacrEPG = ConfigYesNo(default=True)
config.misc.CSFD.FindInclDiacrOth = ConfigYesNo(default=False)
config.misc.CSFD.ShowEPGMulti = ConfigYesNo(default=True)
config.misc.CSFD.ShowInEPGList = ConfigYesNo(default=True)
config.misc.CSFD.ShowInEPGListBlueButton = ConfigYesNo(default=False)
config.misc.CSFD.ShowInEPGDetail = ConfigYesNo(default=True)
config.misc.CSFD.ShowInMovieSelection = ConfigYesNo(default=True)
config.misc.CSFD.ShowSimpleInfo = ConfigYesNo(default=True)
config.misc.CSFD.CSFDreplaceIMDB = ConfigYesNo(default=True)
config.misc.CSFD.SortEPG_CZ_SK = ConfigYesNo(default=True)
config.misc.CSFD.PriorityInMenu = ConfigInteger(default=50, limits=(0, 200))
config.misc.CSFD.PosterBasicSlide = ConfigYesNo(default=True)
config.misc.CSFD.PosterBasicSlideTime = ConfigInteger(default=10, limits=(2, 50))
config.misc.CSFD.PosterBasicSlideInclGallery = ConfigYesNo(default=True)
config.misc.CSFD.GallerySlide = ConfigYesNo(default=True)
config.misc.CSFD.GallerySlideTime = ConfigInteger(default=10, limits=(2, 50))
config.misc.CSFD.PosterSlide = ConfigYesNo(default=True)
config.misc.CSFD.PosterSlideTime = ConfigInteger(default=10, limits=(2, 50))
config.misc.CSFD.TipsShow = ConfigYesNo(default=True)
config.misc.CSFD.TipsTime = ConfigInteger(default=15, limits=(2, 50))
config.misc.CSFD.RatingRotation = ConfigYesNo(default=True)
config.misc.CSFD.RatingRotationTime = ConfigInteger(default=15, limits=(2, 50))
config.misc.CSFD.IMDBCharsConversion = ConfigYesNo(default=True)
config.misc.CSFD.ShowLine = ConfigYesNo(default=True)
config.misc.CSFD.LoginToCSFD = ConfigYesNo(default=False)
config.misc.CSFD.UserNameCSFD = CSFDConfigText('', fixed_size=False)
config.misc.CSFD.PasswordCSFD = CSFDConfigPassword('', fixed_size=False)
config.misc.CSFD.DownloadTimeOut = ConfigInteger(default=25, limits=(5, 120))
config.misc.CSFD.TechnicalDownloadTimeOut = ConfigInteger(default=10, limits=(5, 120))
config.misc.CSFD.InternetTest = ConfigYesNo(default=True)
config.misc.CSFD.AntiFreeze = ConfigYesNo(default=True)
config.misc.CSFD.AntiFreezeLimit = ConfigInteger(default=30, limits=(20, 60))
config.misc.CSFD.PlayerSubtDelayPlus = ConfigInteger(default=0, limits=(0, 60000))
config.misc.CSFD.PlayerSubtDelayMinus = ConfigInteger(default=0, limits=(0, 60000))
config.misc.CSFD.BackCSFDCompatibility = ConfigYesNo(default=True)
config.misc.CSFD.TVCache = ConfigYesNo(default=False)
config.misc.CSFD.DirectoryVideoDownload = CSFDConfigText('/hdd/movie/', fixed_size=False)
config.misc.CSFD.Skinxml = ConfigYesNo(default=False)
config.misc.CSFD.SkinOLEDxml = ConfigYesNo(default=True)
config.misc.CSFD.QualityPoster = ConfigYesNo(default=False)
config.misc.CSFD.QualityGallery = ConfigYesNo(default=False)
config.misc.CSFD.QualityVideoPoster = ConfigYesNo(default=False)
CSFDActionDict = [
 ('komentare', 'UserComments'),
 ('ext.recenze', 'UserExtReviews'),
 ('diskuze', 'UserDiscussion'),
 ('zajimavosti', 'UserInteresting'),
 ('oceneni', 'UserAwards'),
 ('premiery', 'UserPremiery'),
 ('hodnoceni', 'UserReviews'),
 ('fanousci', 'UserFans'),
 ('galerie', 'UserGallery'),
 ('postery', 'UserPoster'),
 ('video', 'UserVideo')]

def ResetParams():
	config.misc.CSFD.Log.saved_value = None
	config.misc.CSFD.LogConsole.saved_value = None
	config.misc.CSFD.LogConsoleTime.saved_value = None
	config.misc.CSFD.LogMaxSize.saved_value = None
	config.misc.CSFD.Language.saved_value = None
	config.misc.CSFD.Resolution.saved_value = None
	config.misc.CSFD.DirectoryTMP.saved_value = None
	config.misc.CSFD.LastVersionCheck.saved_value = None
	config.misc.CSFD.LastLanError.saved_value = None
	config.misc.CSFD.LastLoginError.saved_value = None
	config.misc.CSFD.LanErrorWaiting.saved_value = None
	config.misc.CSFD.LoginErrorWaiting.saved_value = None
	config.misc.CSFD.AutomaticVersionCheck.saved_value = None
	config.misc.CSFD.AutomaticBetaVersionCheck.saved_value = None
	config.misc.CSFD.TestVersion.saved_value = None
	config.misc.CSFD.CurrentSkin.saved_value = None
	config.misc.CSFD.Detail100.saved_value = None
	config.misc.CSFD.PosterBasic.saved_value = None
	config.misc.CSFD.SaveSearch.saved_value = None
	config.misc.CSFD.InputSearch.saved_value = None
	config.misc.CSFD.ShowInMenuStart.saved_value = None
	config.misc.CSFD.ShowInEPGSubMenu.saved_value = None
	config.misc.CSFD.ShowInPluginMenu.saved_value = None
	config.misc.CSFD.ShowInEventInfoMenu.saved_value = None
	config.misc.CSFD.ShowInExtensionMenu.saved_value = None
	config.misc.CSFD.ShowInATV.saved_value = None
	config.misc.CSFD.ShowInInfoBar.saved_value = None
	config.misc.CSFD.FindAllItems.saved_value = None
	config.misc.CSFD.FindInclYear.saved_value = None
	config.misc.CSFD.CompareInclYear.saved_value = None
	config.misc.CSFD.ReadDetailBasedOnScore.saved_value = None
	config.misc.CSFD.FindInclDiacrEPG.saved_value = None
	config.misc.CSFD.FindInclDiacrOth.saved_value = None
	config.misc.CSFD.ShowEPGMulti.saved_value = None
	config.misc.CSFD.ShowInEPGList.saved_value = None
	config.misc.CSFD.ShowInEPGListBlueButton.saved_value = None
	config.misc.CSFD.ShowInEPGDetail.saved_value = None
	config.misc.CSFD.ShowInMovieSelection.saved_value = None
	config.misc.CSFD.ShowSimpleInfo.saved_value = None
	config.misc.CSFD.CSFDreplaceIMDB.saved_value = None
	config.misc.CSFD.SortEPG_CZ_SK.saved_value = None
	config.misc.CSFD.PriorityInMenu.saved_value = None
	config.misc.CSFD.PosterBasicSlide.saved_value = None
	config.misc.CSFD.PosterBasicSlideTime.saved_value = None
	config.misc.CSFD.PosterBasicSlideInclGallery.saved_value = None
	config.misc.CSFD.GallerySlide.saved_value = None
	config.misc.CSFD.GallerySlideTime.saved_value = None
	config.misc.CSFD.PosterSlide.saved_value = None
	config.misc.CSFD.PosterSlideTime.saved_value = None
	config.misc.CSFD.TipsShow.saved_value = None
	config.misc.CSFD.TipsTime.saved_value = None
	config.misc.CSFD.RatingRotation.saved_value = None
	config.misc.CSFD.RatingRotationTime.saved_value = None
	config.misc.CSFD.IMDBCharsConversion.saved_value = None
	config.misc.CSFD.ShowLine.saved_value = None
	config.misc.CSFD.DownloadTimeOut.saved_value = None
	config.misc.CSFD.TechnicalDownloadTimeOut.saved_value = None
	config.misc.CSFD.InternetTest.saved_value = None
	config.misc.CSFD.AntiFreeze.saved_value = None
	config.misc.CSFD.AntiFreezeLimit.saved_value = None
	config.misc.CSFD.PlayerSubtDelayPlus.saved_value = None
	config.misc.CSFD.PlayerSubtDelayMinus.saved_value = None
	config.misc.CSFD.BackCSFDCompatibility.saved_value = None
	config.misc.CSFD.TVCache.saved_value = None
	config.misc.CSFD.DirectoryVideoDownload.saved_value = None
	config.misc.CSFD.Skinxml.saved_value = None
	config.misc.CSFD.SkinOLEDxml.saved_value = None
	config.misc.CSFD.QualityPoster.saved_value = None
	config.misc.CSFD.QualityGallery.saved_value = None
	config.misc.CSFD.QualityVideoPoster.saved_value = None
	config.misc.CSFD.VideoResolution.saved_value = None
	config.misc.CSFD.SortFindItems.saved_value = None
	config.misc.CSFD.NumberOfReadMovieNameFromDetail.saved_value = None
	config.misc.CSFD.Info_EPG.saved_value = None
	config.misc.CSFD.Default_Sort.saved_value = None
	config.misc.CSFD.Input_Type.saved_value = None
	config.misc.CSFD.Design.saved_value = None
	config.misc.CSFD.Comment_Sort.saved_value = None
	config.misc.CSFD.FontHeight.saved_value = None
	config.misc.CSFD.FontHeightFullHD.saved_value = None
	config.misc.CSFD.ThousandsSeparator.saved_value = None
	config.misc.CSFD.InstallCommand.saved_value = None
	config.misc.CSFD.HotKey4.saved_value = None
	config.misc.CSFD.HotKey5.saved_value = None
	config.misc.CSFD.HotKey6.saved_value = None
	config.misc.CSFD.HotKey7.saved_value = None
	config.misc.CSFD.HotKey8.saved_value = None
	config.misc.CSFD.HotKey9.saved_value = None
	config.misc.CSFD.HotKey0.saved_value = None
	config.misc.CSFD.HotKeyLR.saved_value = None
	config.misc.CSFD.HotKeyLG.saved_value = None
	config.misc.CSFD.HotKeyLB.saved_value = None
	config.misc.CSFD.HotKeyLY.saved_value = None
	config.misc.CSFD.Bouquet1.saved_value = None
	config.misc.CSFD.Bouquet2.saved_value = None
	config.misc.CSFD.Bouquet3.saved_value = None
	config.misc.CSFD.Bouquet4.saved_value = None
	config.misc.CSFD.Bouquet5.saved_value = None
	config.misc.CSFD.Bouquet6.saved_value = None
	config.misc.CSFD.Bouquet7.saved_value = None
	config.misc.CSFD.Bouquet8.saved_value = None
	config.misc.CSFD.Bouquet9.saved_value = None
	config.misc.CSFD.Bouquet10.saved_value = None
	config.misc.CSFD.Bouquet11.saved_value = None
	config.misc.CSFD.Log.load()
	config.misc.CSFD.LogConsole.load()
	config.misc.CSFD.LogConsoleTime.load()
	config.misc.CSFD.LogMaxSize.load()
	config.misc.CSFD.Language.load()
	config.misc.CSFD.Resolution.load()
	config.misc.CSFD.DirectoryTMP.load()
	config.misc.CSFD.LastVersionCheck.load()
	config.misc.CSFD.LastLanError.load()
	config.misc.CSFD.LastLoginError.load()
	config.misc.CSFD.LanErrorWaiting.load()
	config.misc.CSFD.LoginErrorWaiting.load()
	config.misc.CSFD.AutomaticVersionCheck.load()
	config.misc.CSFD.AutomaticBetaVersionCheck.load()
	config.misc.CSFD.TestVersion.load()
	config.misc.CSFD.CurrentSkin.load()
	config.misc.CSFD.Detail100.load()
	config.misc.CSFD.PosterBasic.load()
	config.misc.CSFD.SaveSearch.load()
	config.misc.CSFD.InputSearch.load()
	config.misc.CSFD.ShowInMenuStart.load()
	config.misc.CSFD.ShowInEPGSubMenu.load()
	config.misc.CSFD.ShowInPluginMenu.load()
	config.misc.CSFD.ShowInEventInfoMenu.load()
	config.misc.CSFD.ShowInExtensionMenu.load()
	config.misc.CSFD.ShowInATV.load()
	config.misc.CSFD.ShowInInfoBar.load()
	config.misc.CSFD.FindAllItems.load()
	config.misc.CSFD.FindInclYear.load()
	config.misc.CSFD.CompareInclYear.load()
	config.misc.CSFD.ReadDetailBasedOnScore.load()
	config.misc.CSFD.FindInclDiacrEPG.load()
	config.misc.CSFD.FindInclDiacrOth.load()
	config.misc.CSFD.ShowEPGMulti.load()
	config.misc.CSFD.ShowInEPGList.load()
	config.misc.CSFD.ShowInEPGListBlueButton.load()
	config.misc.CSFD.ShowInEPGDetail.load()
	config.misc.CSFD.ShowInMovieSelection.load()
	config.misc.CSFD.ShowSimpleInfo.load()
	config.misc.CSFD.CSFDreplaceIMDB.load()
	config.misc.CSFD.SortEPG_CZ_SK.load()
	config.misc.CSFD.PriorityInMenu.load()
	config.misc.CSFD.PosterBasicSlide.load()
	config.misc.CSFD.PosterBasicSlideTime.load()
	config.misc.CSFD.PosterBasicSlideInclGallery.load()
	config.misc.CSFD.GallerySlide.load()
	config.misc.CSFD.GallerySlideTime.load()
	config.misc.CSFD.PosterSlide.load()
	config.misc.CSFD.PosterSlideTime.load()
	config.misc.CSFD.TipsShow.load()
	config.misc.CSFD.TipsTime.load()
	config.misc.CSFD.RatingRotation.load()
	config.misc.CSFD.RatingRotationTime.load()
	config.misc.CSFD.IMDBCharsConversion.load()
	config.misc.CSFD.ShowLine.load()
	config.misc.CSFD.DownloadTimeOut.load()
	config.misc.CSFD.TechnicalDownloadTimeOut.load()
	config.misc.CSFD.InternetTest.load()
	config.misc.CSFD.AntiFreeze.load()
	config.misc.CSFD.AntiFreezeLimit.load()
	config.misc.CSFD.PlayerSubtDelayPlus.load()
	config.misc.CSFD.PlayerSubtDelayMinus.load()
	config.misc.CSFD.BackCSFDCompatibility.load()
	config.misc.CSFD.TVCache.load()
	config.misc.CSFD.DirectoryVideoDownload.load()
	config.misc.CSFD.Skinxml.load()
	config.misc.CSFD.SkinOLEDxml.load()
	config.misc.CSFD.QualityPoster.load()
	config.misc.CSFD.QualityGallery.load()
	config.misc.CSFD.QualityVideoPoster.load()
	config.misc.CSFD.VideoResolution.load()
	config.misc.CSFD.SortFindItems.load()
	config.misc.CSFD.NumberOfReadMovieNameFromDetail.load()
	config.misc.CSFD.Info_EPG.load()
	config.misc.CSFD.Default_Sort.load()
	config.misc.CSFD.Input_Type.load()
	config.misc.CSFD.Design.load()
	config.misc.CSFD.Comment_Sort.load()
	config.misc.CSFD.FontHeight.load()
	config.misc.CSFD.FontHeightFullHD.load()
	config.misc.CSFD.ThousandsSeparator.load()
	config.misc.CSFD.InstallCommand.load()
	config.misc.CSFD.HotKey4.load()
	config.misc.CSFD.HotKey5.load()
	config.misc.CSFD.HotKey6.load()
	config.misc.CSFD.HotKey7.load()
	config.misc.CSFD.HotKey8.load()
	config.misc.CSFD.HotKey9.load()
	config.misc.CSFD.HotKey0.load()
	config.misc.CSFD.HotKeyLR.load()
	config.misc.CSFD.HotKeyLG.load()
	config.misc.CSFD.HotKeyLB.load()
	config.misc.CSFD.HotKeyLY.load()
	config.misc.CSFD.Bouquet1.load()
	config.misc.CSFD.Bouquet2.load()
	config.misc.CSFD.Bouquet3.load()
	config.misc.CSFD.Bouquet4.load()
	config.misc.CSFD.Bouquet5.load()
	config.misc.CSFD.Bouquet6.load()
	config.misc.CSFD.Bouquet7.load()
	config.misc.CSFD.Bouquet8.load()
	config.misc.CSFD.Bouquet9.load()
	config.misc.CSFD.Bouquet10.load()
	config.misc.CSFD.Bouquet11.load()
	from CSFDSubtitles import ResetSubtitleParams
	ResetSubtitleParams()
	configfile.save()
	return


def InitParamsLangImpact():
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - InitParamsLangImpact - zacatek\n')
	config.misc.CSFD.Language = ConfigSelection(choices=[('0', _('automaticky')), ('1', _('česky')), ('2', _('slovensky'))], default='0')
	config.misc.CSFD.Resolution = ConfigSelection(choices=[('0', _('automaticky')), ('720', _('720')), ('1280', _('1280')), ('1920', _('1920'))], default='0')
	config.misc.CSFD.VideoResolution = ConfigSelection(choices=[('sd', _('SD')), ('hd', _('HD'))], default='sd')
	config.misc.CSFD.SortFindItems = ConfigSelection(choices=[('0', _('metoda 1 - Levenshtein')), ('1', _('metoda 2 - Bigram')), ('2', _('metoda 3 - Jen porovnat'))], default='0')
	config.misc.CSFD.NumberOfReadMovieNameFromDetail = ConfigSelection(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='2')
	config.misc.CSFD.Info_EPG = ConfigSelection(choices=[('0', _('rovnou vyhledat aktuální pořad')), ('1', _('zobrazit EPG aktuálního kanálu')), ('2', _('zobrazit seznam kanálů'))], default='0')
	config.misc.CSFD.Default_Sort = ConfigSelection(choices=[('0', _('vhodnosti názvu')), ('1', _('CSFD.cz')), ('2', _('data vydání')), ('3', _('abecedy'))], default='0')
	config.misc.CSFD.Input_Type = ConfigSelection(choices=[('0', _('pomocí virtuální klávesnice')), ('1', _('výběrem znaků opakovaným stiskem klávesy'))], default='0')
	config.misc.CSFD.Design = ConfigSelection(choices=[('0', _('barva textu dle hodnocení')), ('1', _('barvy stejné bez ohledu na hodnocení')), ('2', _('barvy stejné + zvýraznění kategorií'))], default='0')
	config.misc.CSFD.Comment_Sort = ConfigSelection(choices=[('', _('seřadit podle počtu bodů uživatele')), ('podle-datetime/', _('seřadit od nejnovějších po nejstarší')), ('podle-rating/', _('seřadit podle hodnocení'))], default='')
	config.misc.CSFD.FontHeight = ConfigSelection(choices=[('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37')], default='22')
	config.misc.CSFD.FontHeightFullHD = ConfigSelection(choices=[('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56')], default='28')
	config.misc.CSFD.ThousandsSeparator = ConfigSelection(choices=[('', _('žádný')), (' ', _('mezera')), ('.', _('tečka')), (',', _('čárka'))], default=' ')
	config.misc.CSFD.InstallCommand = ConfigSelection(choices=[('default', 'default'), ('ipkg', 'ipkg'), ('opkg', 'opkg'), ('dpkg', 'dpkg')], default='default')
	HotKeysMenu = [
	 (
	  'nic', _('Bez akce')),
	 (
	  'aktEPG', _('Výběr pořadu z EPG akt.programu')),
	 (
	  'vyberEPG', _('Výběr pořadu ze všech kanálů')),
	 (
	  'zadejporad', _('Zadání pořadu')),
	 (
	  'spustitIMDB', _('Vyhledat pořad v IMDB')),
	 (
	  'souvisejici', _('Zobrazit související pořady')),
	 (
	  'podobne', _('Zobrazit podobné pořady')),
	 (
	  'serie', _('Zobrazit řady seriálu')),
	 (
	  'epizody', _('Zobrazit epizody seriálu')),
	 (
	  'komentare', _('Zobrazit komentáře')),
	 (
	  'ext.recenze', _('Zobrazit ext.recenze')),
	 (
	  'diskuze', _('Zobrazit diskuzi')),
	 (
	  'zajimavosti', _('Zobrazit zajímavosti')),
	 (
	  'oceneni', _('Zobrazit ocenění')),
	 (
	  'galerie', _('Zobrazit galerii')),
	 (
	  'postery', _('Zobrazit postery')),
	 (
	  'video', _('Zobrazit videa')),
	 (
	  'ulozvideo', _('Uložit video')),
	 (
	  'spustitvideo', _('Spustit video ukázku')),
	 (
	  'premiery', _('Zobrazit premiéry')),
	 (
	  'hodnoceni', _('Zobrazit hodnocení uživatelů')),
	 (
	  'fanousci', _('Zobrazit fanoušky pořadu')),
	 (
	  'ownrating', _('Zadat/změnit hodnocení')),
	 (
	  'nastaveni', _('Nastavení')),
	 (
	  'novaverze', _('Stáhnout novou verzi pluginu')),
	 (
	  'historie', _('Historie změn v pluginu')),
	 (
	  'skin', _('Změna skinu')),
	 (
	  'about', _('O pluginu'))]
	BouquetMenu = [
	 (
	  'nic', _('Bez akce')),
	 (
	  'komentare', _('Zobrazit komentáře')),
	 (
	  'ext.recenze', _('Zobrazit ext.recenze')),
	 (
	  'diskuze', _('Zobrazit diskuzi')),
	 (
	  'zajimavosti', _('Zobrazit zajímavosti')),
	 (
	  'oceneni', _('Zobrazit ocenění')),
	 (
	  'premiery', _('Zobrazit premiéry')),
	 (
	  'hodnoceni', _('Zobrazit hodnocení uživatelů')),
	 (
	  'fanousci', _('Zobrazit fanoušky pořadu')),
	 (
	  'galerie', _('Zobrazit galerii')),
	 (
	  'postery', _('Zobrazit postery')),
	 (
	  'video', _('Zobrazit videa'))]
	config.misc.CSFD.HotKey4 = ConfigSelection(choices=HotKeysMenu, default='aktEPG')
	config.misc.CSFD.HotKey5 = ConfigSelection(choices=HotKeysMenu, default='oceneni')
	config.misc.CSFD.HotKey6 = ConfigSelection(choices=HotKeysMenu, default='komentare')
	config.misc.CSFD.HotKey7 = ConfigSelection(choices=HotKeysMenu, default='zajimavosti')
	config.misc.CSFD.HotKey8 = ConfigSelection(choices=HotKeysMenu, default='galerie')
	config.misc.CSFD.HotKey9 = ConfigSelection(choices=HotKeysMenu, default='postery')
	config.misc.CSFD.HotKey0 = ConfigSelection(choices=HotKeysMenu, default='video')
	config.misc.CSFD.HotKeyLR = ConfigSelection(choices=HotKeysMenu, default='diskuze')
	config.misc.CSFD.HotKeyLG = ConfigSelection(choices=HotKeysMenu, default='postery')
	config.misc.CSFD.HotKeyLB = ConfigSelection(choices=HotKeysMenu, default='premiery')
	config.misc.CSFD.HotKeyLY = ConfigSelection(choices=HotKeysMenu, default='ownrating')
	config.misc.CSFD.Bouquet1 = ConfigSelection(choices=BouquetMenu, default='komentare')
	config.misc.CSFD.Bouquet2 = ConfigSelection(choices=BouquetMenu, default='diskuze')
	config.misc.CSFD.Bouquet3 = ConfigSelection(choices=BouquetMenu, default='zajimavosti')
	config.misc.CSFD.Bouquet4 = ConfigSelection(choices=BouquetMenu, default='oceneni')
	config.misc.CSFD.Bouquet5 = ConfigSelection(choices=BouquetMenu, default='premiery')
	config.misc.CSFD.Bouquet6 = ConfigSelection(choices=BouquetMenu, default='hodnoceni')
	config.misc.CSFD.Bouquet7 = ConfigSelection(choices=BouquetMenu, default='fanousci')
	config.misc.CSFD.Bouquet8 = ConfigSelection(choices=BouquetMenu, default='galerie')
	config.misc.CSFD.Bouquet9 = ConfigSelection(choices=BouquetMenu, default='postery')
	config.misc.CSFD.Bouquet10 = ConfigSelection(choices=BouquetMenu, default='video')
	config.misc.CSFD.Bouquet11 = ConfigSelection(choices=BouquetMenu, default='ext.recenze')
	config.misc.CSFD.LastLoginError.setValue(int(0))
	config.misc.CSFD.LastLoginError.save()
	config.misc.CSFD.LastLanError.setValue(int(0))
	config.misc.CSFD.LastLanError.save()
	LogCSFD.WriteToFile('[CSFD] CSFDSettings2 - InitParamsLangImpact - konec\n')


InitParamsLangImpact()

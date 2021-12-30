# -*- coding: utf-8 -*-

from CSFDLog import LogCSFD
from enigma import getDesktop, eListboxPythonMultiContent, eListboxPythonStringContent, gFont
from os import remove as os_remove, listdir as os_listdir, path as os_path
from CSFDSettings1 import CSFDGlobalVar
from CSFDSettings2 import config, std_media_header, std_login_header, std_headers
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from CSFDMenuList import CSFDMenuList
import urllib, urllib2, cookielib, re, sys, operator, traceback
cj = cookielib.CookieJar()
handlersUL2 = [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cj)]
openerUL2 = urllib2.build_opener(*handlersUL2)

class NoRedirection(urllib2.HTTPErrorProcessor):

	def http_response(self, request, response):
		return response

	https_response = http_response


openerUL2NoRedirect = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
try:
	import ssl
	contextSSL = hasattr(ssl, '_create_unverified_context') and ssl._create_unverified_context() or None
	if contextSSL is not None:
		ssl._create_default_https_context = ssl._create_unverified_context
		CSFDGlobalVar.setOpenSSLcontext(True)
		LogCSFD.WriteToFile('[CSFD] CSFDTools - import ssl - context OK\n')
	else:
		CSFDGlobalVar.setOpenSSLcontext(False)
		LogCSFD.WriteToFile('[CSFD] CSFDTools - import ssl - context ERR\n')
	CSFDGlobalVar.setOpenSSLexist(True)
	LogCSFD.WriteToFile('[CSFD] CSFDTools - import ssl - OK\n')
except:
	CSFDGlobalVar.setOpenSSLexist(False)
	CSFDGlobalVar.setOpenSSLcontext(False)
	err = traceback.format_exc()
	LogCSFD.WriteToFile('[CSFD] CSFDTools - import ssl - chyba\n')
	LogCSFD.WriteToFile(err)

google_URL = 'http://google.cz'
csfd_URL_https = 'https://www.csfd.cz/'
try:
	import socket
	google_IP = 'http://' + socket.gethostbyname('google.cz')
except:
	google_IP = google_URL

LogCSFD.WriteToFile('[CSFD] CSFDTools - google_IP: ' + google_IP + '\n')
if CSFDGlobalVar.getOpenSSLexist():
	try:
		if CSFDGlobalVar.getOpenSSLcontext():
			from twisted.internet.ssl import ClientContextFactory
			from OpenSSL import SSL
			LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - vytvarim\n')

			class CSFDClientContextFactory(ClientContextFactory):
				LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - class\n')

				def __init__(self):
					LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - init\n')
					self.privateKeyFileName = '/etc/enigma2/key.pem'
					self.certificateFileName = '/etc/enigma2/cert.pem'
					self.method = SSL.SSLv23_METHOD
					self.sslmethod = SSL.SSLv23_METHOD

				def getContext(self):
					LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - getContext\n')
					ctx = ClientContextFactory.getContext(self)
					ctx.set_options(SSL.OP_ALL)
					return ctx


			ClientContextFactoryCSFD = CSFDClientContextFactory()
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFDClientContextFactory - None\n')
			ClientContextFactory = object
			ClientContextFactoryCSFD = None
			CSFDGlobalVar.setOpenSSLcontext(False)
	except:
		ClientContextFactory = object
		ClientContextFactoryCSFD = None
		CSFDGlobalVar.setOpenSSLcontext(False)
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFDClientContextFactory - chyba\n')
		LogCSFD.WriteToFile(err)
		LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - None\n')

else:
	LogCSFD.WriteToFile('[CSFD] CSFDClientContextFactory - None\n')
	ClientContextFactory = object
	ClientContextFactoryCSFD = None
try:
	from twisted.web.client import downloadPage, getPage, HTTPClientFactory
	from twisted.internet import defer
	from twisted.internet.defer import DeferredSemaphore
	from twisted.python.log import startLogging
	twistedwebExist = True
	old_HTTPClientFactory_gotHeaders = HTTPClientFactory.gotHeaders

	def CSFD_HTTPClientFactory_gotHeaders(self, headers):
		LogCSFD.WriteToFile('[CSFD] CSFD_HTTPClientFactory_gotHeaders - zacatek\n')
		old_HTTPClientFactory_gotHeaders(self, headers)
		LogCSFD.WriteToFile('[CSFD] CSFD_HTTPClientFactory_gotHeaders - response headers: ' + str(headers) + '\n')
		if headers.has_key('set-cookie'):
			cookies = CSFDGlobalVar.getCSFDCookies()
			LogCSFD.WriteToFile('[CSFD] Cookies - pred zmenou : ' + str(cookies) + '\n')
			cookies.update(self.cookies)
			LogCSFD.WriteToFile('[CSFD] Cookies - po zmene	  : ' + str(cookies) + '\n')
			CSFDGlobalVar.setCSFDCookies(cookies)
		LogCSFD.WriteToFile('[CSFD] CSFD_HTTPClientFactory_gotHeaders - konec\n')


	HTTPClientFactory.gotHeaders = CSFD_HTTPClientFactory_gotHeaders
except:
	twistedwebExist = False

	def downloadPage(self, *a, **kw):
		pass


	def getPage(self, *a, **kw):
		pass


	class c_defer():

		def inlineCallbacks(self, f):
			pass


	defer = c_defer()

	def DeferredSemaphore(self, *a, **kw):
		pass


try:
	import unicodedata
	unicodedataExist = True
except:
	unicodedataExist = False

class LimitedDownloader():

	def __init__(self, howMany):
		self._semaphore = DeferredSemaphore(howMany)

	def downloadPage(self, *a, **kw):
		return self._semaphore.run(downloadPage, *a, **kw)

	def getPage(self, *a, **kw):
		return self._semaphore.run(getPage, *a, **kw)


class ItemList(MenuList):

	def __init__(self, items, enableWrapAround=False):
		MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		try:
			self.l.setItemHeight(h1)
			if 'setFont' in dir(self.l):
				self.l.setFont(0, gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDTools - ItemList - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDTools - chyba - ItemList - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')


class ItemListServiceMenu(MenuList):

	def __init__(self, items, enableWrapAround=False):
		MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		try:
			self.l.setItemHeight(h1)
			if 'setFont' in dir(self.l):
				self.l.setFont(0, gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDTools - ItemListServiceMenu - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDTools - chyba - ItemListServiceMenu - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')


class ItemListTypeSpecial(CSFDMenuList):

	def __init__(self, items, enableWrapAround=False):
		CSFDMenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		try:
			self.l.setItemHeight(h1)
			if 'setFont' in dir(self.l):
				self.l.setFont(0, gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDTools - ItemListTypeSpecial - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDTools - chyba - ItemListTypeSpecial - nelze nastavit velikost fontu v menu eListboxPythonMultiContent (stara verze enigma2)\n')


class ItemListString(MenuList):

	def __init__(self, items, enableWrapAround=False, content=eListboxPythonStringContent):
		MenuList.__init__(self, items, enableWrapAround, content)


class EmptyClass():

	def __init__(self):
		pass


def loadPixmapCSFD(name):
	pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/%s' % name))
	if pixmap is None:
		pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/%s' % name))
	return pixmap


def picStartDecodeCSFD(pic, name):
	OK = False
	filename = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/%s' % name)
	if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
		if pic.startDecode(filename, 0, 0, False) == 0:
			OK = True
	elif pic.startDecode(filename, False) == 0:
		OK = True
	if not OK:
		filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/%s' % name)
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			if pic.startDecode(filename, 0, 0, False) == 0:
				OK = True
		elif pic.startDecode(filename, False) == 0:
			OK = True
	return OK


def strUni(mystring):
	if not isinstance(mystring, str):
		return str(mystring.encode('utf-8'))
	else:
		return mystring


def Uni8(mystring):
	if isinstance(mystring, str):
		return unicode(mystring, 'utf-8')
	else:
		return mystring


def ExtractNumbers(mystring):
	return re.findall('\\b\\d+\\b', mystring)


def request(url, headers={}, timeout=None):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - url: %s\n' % Uni8(url))
	try:
		r = urllib2.Request(url, headers=headers)
		if timeout is None:
			response = openerUL2.open(r)
		else:
			response = openerUL2.open(r, timeout=timeout)
		data = response.read()
		response.close()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - request - OK\n')
	except:
		data = ''
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - request - chyba\n')
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - konec\n')
	return data


def requestCSFD(url, headers=[], timeout=None, data=None, redirect=True, saveCookie=False):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestCSFD - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestCSFD - url: %s\n' % Uni8(url))
	try:
		if redirect:
			op = openerUL2
		else:
			op = openerUL2NoRedirect
		op.addheaders = headers
		if timeout is None and data is None:
			response = op.open(url)
		elif timeout is not None and data is not None:
			response = op.open(url, timeout=timeout, data=data)
		elif timeout is not None:
			response = op.open(url, timeout=timeout)
		elif data is not None:
			response = op.open(url, data=data)
		else:
			response = op.open(url)
		data = response.read()
		if saveCookie:
			cookieUL2 = response.headers.getheader('Set-Cookie')
			if cookieUL2 is not None:
				CSFDGlobalVar.setCSFDCookiesUL2(cookieUL2)
			LogCSFD.WriteToFile('Cookies response UL2: ' + str(cookieUL2) + '\n')
		response.close()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestCSFD - OK\n')
	except:
		data = ''
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestCSFD - chyba\n')
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestCSFD - konec\n')
	return data


def requestFileCSFD(url='', fileout='', file_mode='wb', headers=[], timeout=None, errHandling=True, saveCookie=False):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - url: %s\n' % Uni8(url))
	if fileout == '':
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - Neni co stahovat\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - konec\n')
		return
	else:
		if errHandling:
			try:
				openerUL2.addheaders = headers
				if timeout is not None:
					response = openerUL2.open(url, timeout=timeout)
				else:
					response = openerUL2.open(url)
				local_file = open(fileout, file_mode)
				local_file.write(response.read())
				local_file.close()
				if saveCookie:
					cookieUL2 = response.headers.getheader('Set-Cookie')
					if cookieUL2 is not None:
						CSFDGlobalVar.setCSFDCookiesUL2(cookieUL2)
					LogCSFD.WriteToFile('Cookies response UL2: ' + str(cookieUL2) + '\n')
				response.close()
				LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - OK\n')
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - chyba\n')
				LogCSFD.WriteToFile(err)

		else:
			openerUL2.addheaders = headers
			if timeout is not None:
				response = openerUL2.open(url, timeout=timeout)
			else:
				response = openerUL2.open(url)
			local_file = open(fileout, file_mode)
			local_file.write(response.read())
			local_file.close()
			if saveCookie:
				cookieUL2 = response.headers.getheader('Set-Cookie')
				if cookieUL2 is not None:
					CSFDGlobalVar.setCSFDCookiesUL2(cookieUL2)
				LogCSFD.WriteToFile('Cookies response UL2: ' + str(cookieUL2) + '\n')
			response.close()
			LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - OK\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - konec\n')
		return


class CSFDHelpableActionMapChng(ActionMap):

	def __init__(self, parent, context, actions=None, prio=0):
		if actions is None:
			actions = {}
		alist = []
		adict = {}
		for action, funchelp in actions.iteritems():
			if isinstance(funchelp, tuple):
				alist.append((action, funchelp[1]))
				adict[action] = funchelp[0]
			else:
				adict[action] = funchelp

		ActionMap.__init__(self, [context], adict, prio)
		for index, value in enumerate(parent.helpList):
			if parent.helpList[index][1] == context:
				for index1, value1 in enumerate(parent.helpList[index][2]):
					for xx, val in enumerate(alist):
						if alist[xx][1] is not None:
							if parent.helpList[index][2][index1][0] == alist[xx][0]:
								parent.helpList[index][2][index1] = list(parent.helpList[index][2][index1])
								parent.helpList[index][2][index1][1] = alist[xx][1]
								parent.helpList[index][2][index1] = tuple(parent.helpList[index][2][index1])
								break

				break

		return


def requestInclErr(url, headers={}):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - url: %s\n' % Uni8(url))
	chyba = False
	try:
		r = urllib2.Request(url, headers=headers)
		response = urllib2.urlopen(r)
		data = response.read()
		response.close()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - OK\n')
	except:
		chyba = True
		data = ''
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - chyba\n')
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - OK\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestInclErr - konec\n')
	return (data, chyba)


def internet_on(timeout_s=1):
	if not config.misc.CSFD.InternetTest.getValue():
		return True
	OK = False
	try:
		urllib2.urlopen(google_IP, timeout=timeout_s)
		OK = True
	except:
		OK = False
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - internet_on - chyba\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - internet_on - google_IP: ' + google_IP + '\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - internet_on - timeout_s: ' + str(timeout_s) + '\n')
		LogCSFD.WriteToFile(err)

	if not OK and timeout_s < 3:
		timeout_s += 3
		OK = internet_on(timeout_s)
	return OK


std_header_UA = 'Mozilla/6.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.5) Gecko/2008092417 Firefox/3.0.3)'

def post(url, data):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - post - zacatek\n')
	try:
		postdata = urllib.urlencode(data)
		req = urllib2.Request(url, postdata)
		req.add_header('User-Agent', std_header_UA)
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - post - OK\n')
	except:
		data = ''
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - post - chyba\n')
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] CSFDTools - post - konec\n')
	return data


def substr(data, start, end):
	i1 = data.find(start)
	i2 = data.find(end, i1)
	return data[i1:i2]


def GetInstallCommand():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand - zacatek\n')
	inst_c = 'ipkg'
	err = False
	try:
		fileP = open('/usr/bin/opkg', 'r')
	except:
		err = True

	if not err:
		inst_c = 'opkg'
		fileP.close()
	err = False
	try:
		fileP = open('/usr/bin/dpkg', 'r')
	except:
		err = True

	if not err:
		inst_c = 'dpkg'
		fileP.close()
	if config.misc.CSFD.InstallCommand.getValue() != 'default':
		inst_c = config.misc.CSFD.InstallCommand.getValue()
	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand: %s\n' % Uni8(inst_c))
	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand - konec\n')
	return inst_c


def getBoxtypeCSFD():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxTypeCSFD - zacatek\n')
	success = False
	try:
		filePointer = open('/proc/stb/info/vumodel')
		success = True
	except:
		try:
			filePointer = open('/proc/stb/info/model')
			success = True
		except:
			try:
				filePointer = open('/proc/stb/info/azmodel')
				success = True
			except:
				try:
					filePointer = open('/hdd/model')
					success = True
				except:
					pass

	manu = 'Unknown'
	model = 'Unknown'
	arch = 'unk'
	if success:
		box = filePointer.readline().strip()
		filePointer.close()
		if box == 'ufs910':
			manu = 'Kathrein'
			model = 'UFS-910'
			arch = 'sh4'
		elif box == 'ufs912':
			manu = 'Kathrein'
			model = 'UFS-912'
			arch = 'sh4'
		elif box == 'ufs922':
			manu = 'Kathrein'
			model = 'UFS-922'
			arch = 'sh4'
		elif box == 'solo':
			manu = 'VU+'
			model = 'Solo'
			arch = 'mipsel'
		elif box == 'duo':
			manu = 'VU+'
			model = 'Duo'
			arch = 'mipsel'
		elif box == 'solo2':
			manu = 'VU+'
			model = 'Solo2'
			arch = 'mipsel'
		elif box == 'duo2':
			manu = 'VU+'
			model = 'Duo2'
			arch = 'mipsel'
		elif box == 'ultimo':
			manu = 'VU+'
			model = 'Ultimo'
			arch = 'mipsel'
		elif box == 'tf7700hdpvr':
			manu = 'Topfield'
			model = 'HDPVR-7700'
			arch = 'sh4'
		elif box == 'dm800':
			manu = 'Dreambox'
			model = '800'
			arch = 'mipsel'
		elif box == 'dm800se':
			manu = 'Dreambox'
			model = '800se'
			arch = 'mipsel'
		elif box == 'dm820hd' or box == 'dm820':
			manu = 'Dreambox'
			model = '820'
			arch = 'mipsel'
		elif box == 'dm8000':
			manu = 'Dreambox'
			model = '8000'
			arch = 'mipsel'
		elif box == 'dm500hd' or box == 'dm500':
			manu = 'Dreambox'
			model = '500hd'
			arch = 'mipsel'
		elif box == 'dm520hd' or box == 'dm520':
			manu = 'Dreambox'
			model = '520'
			arch = 'mipsel'
		elif box == 'dm900hd' or box == 'dm900':
			manu = 'Dreambox'
			model = '900'
			arch = 'mipsel'
		elif box == 'dm7025':
			manu = 'Dreambox'
			model = '7025'
			arch = 'mipsel'
		elif box == 'dm7020hd':
			manu = 'Dreambox'
			model = '7020hd'
			arch = 'mipsel'
		elif box == 'dm7080':
			manu = 'Dreambox'
			model = '7080'
			arch = 'mipsel'
		elif box == 'dm7080hd':
			manu = 'Dreambox'
			model = '7080'
			arch = 'mipsel'
		elif box == 'elite':
			manu = 'Azbox'
			model = 'Elite'
			arch = 'mipsel'
		elif box == 'premium':
			manu = 'Azbox'
			model = 'Premium'
			arch = 'mipsel'
		elif box == 'premium+':
			manu = 'Azbox'
			model = 'Premium+'
			arch = 'mipsel'
		elif box == 'cuberevo-mini':
			manu = 'Cubarevo'
			model = 'Mini'
			arch = 'sh4'
		elif box == 'hdbox':
			manu = 'Fortis'
			model = 'HdBox'
			arch = 'sh4'
		elif box == 'gbquad':
			manu = 'Gigablue'
			model = 'Quad'
			arch = 'mipsel'
		elif box == 'gbquadplus':
			manu = 'Gigablue'
			model = 'QuadPlus'
			arch = 'mipsel'
		elif box == 'gb800seplus':
			manu = 'Gigablue'
			model = '800SEPlus'
			arch = 'mipsel'
		elif box == 'gb800ueplus':
			manu = 'Gigablue'
			model = '800UEPlus'
			arch = 'mipsel'
		elif box == 'et8000':
			manu = 'Xtrend'
			model = '8000'
			arch = 'mipsel'
		elif box == 'et10000':
			manu = 'Xtrend'
			model = '10000'
			arch = 'mipsel'
		elif box == 'maram9':
			manu = 'Odin'
			model = 'M9'
			arch = 'mipsel'
	version, enigma = Uni8(getBoxArch())
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - box=' + box + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - Vyrobce=' + manu + '; Model=' + model + '; Arch=' + arch + '; Image=' + version + '; Enigma=' + enigma + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - konec\n')
	return (manu, model, arch, version, enigma)


def getBoxArch():
	ARCH = 'unknown'
	enigma = '2'
	if sys.version_info < (2, 6, 9) and sys.version_info > (2, 6, 6):
		ARCH = 'oe16'
		enigma = '2'
	if sys.version_info > (2, 7, 0):
		ARCH = 'oe20'
		enigma = '3'
	try:
		fileP = open('/usr/bin/dpkg', 'r')
		ARCH = 'oe22'
	except:
		pass

	try:
		from enigma import eMediaDatabase
		ARCH = 'oe22'
		enigma = '4'
	except:
		pass

	return (
	 ARCH, enigma)


def getImagetype():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - zacatek\n')
	result = ''
	success = False
	try:
		filePointer = open('/etc/issue')
		success = True
	except:
		pass

	text = ''
	if success:
		tt = filePointer.readlines()
		filePointer.close()
		for index, value in enumerate(tt):
			text += value.lower()

	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - typ image-issue: ' + text + '\n')
	success = False
	try:
		filePointer = open('/etc/image-version')
		success = True
	except:
		pass

	text1 = ''
	if success:
		tt = filePointer.readlines()
		filePointer.close()
		for index, value in enumerate(tt):
			text1 += value.lower()

	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - typ image-version: ' + text1 + '\n')
	compatibility = 255
	if text.find('openpli') >= 0 or text1.find('openpli') >= 0:
		result = 'openpli'
		compatibility = 20
	elif text.find('openatv') >= 0 or text1.find('openatv') >= 0:
		result = 'openatv'
		compatibility = 30
	elif text.find('openvix') >= 0 or text1.find('openvix') >= 0:
		result = 'openvix'
		compatibility = 30
	elif text.find('merlin') >= 0 or text1.find('merlin') >= 0:
		result = 'merlin'
		compatibility = 10
	elif text.find('newnigma') >= 0 or text1.find('newnigma') >= 0:
		result = 'newnigma'
		compatibility = 10
	elif text.find('dream-elite') >= 0 or text1.find('dream-elite') >= 0:
		result = 'dreamelite'
		compatibility = 10
	elif text.find('oozoon') >= 0 or text1.find('oozoon') >= 0:
		result = 'oozoon'
		compatibility = 10
	elif text.find('opendreambox') >= 0 or text1.find('opendreambox') >= 0:
		result = 'dmm'
		compatibility = 1
	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - typ image: ' + result + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - image compatibility: ' + str(compatibility) + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - getImagetype - konec\n')
	return (result, compatibility)


def intWithSeparator(x):
	if x < 0:
		return '-' + intWithSeparator(-x)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = config.misc.CSFD.ThousandsSeparator.getValue() + '%03d%s' % (r, result)

	return '%d%s' % (x, result)


dictonaryDiacritic = {'Á': 'A', 'Ä': 'A', 'Ą': 'A', 'À': 'A', 'Â': 'A', 'Č': 'C', 'Ć': 'C', 'Ç': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Ë': 'E', 'Ę': 'E', 'È': 'E', 'Ê': 'E', 'Í': 'I', 'Ï': 'I', 'Î': 'I', 'Ĺ': 'L', 'Ľ': 'L', 'Ł': 'L', 'Ň': 'N', 'Ń': 'N', 'Ó': 'O', 'Ô': 'O', 'Ö': 'O', 'Ő': 'O', 'Œ': 'O', 'Ŕ': 'R', 'Ř': 'R', 'Š': 'S', 
   'Ś': 'S', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ü': 'U', 'Ű': 'U', 'Ù': 'U', 'Û': 'U', 'Ý': 'Y', 'Ÿ': 'Y', 'Ž': 'Z', 'Ż': 'Z', 'Ź': 'Z', 'á': 'a', 'ä': 'a', 'ą': 'a', 'à': 'a', 'â': 'a', 'č': 'c', 'ć': 'c', 'ç': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'ë': 'e', 'ę': 'e', 'è': 'e', 'ê': 'e', 'í': 'i', 'ï': 'i', 'î': 'i', 'ĺ': 'l', 'ľ': 'l', 'ł': 'l', 'ň': 'n', 'ń': 'n', 'ó': 'o', 
   'ö': 'o', 'ô': 'o', 'ő': 'o', 'œ': 'o', 'ř': 'r', 'ŕ': 'r', 'š': 's', 'ś': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ü': 'u', 'ű': 'u', 'ù': 'u', 'û': 'u', 'ý': 'y', 'ÿ': 'y', 'ž': 'z', 'ż': 'z', 'ź': 'z'}

def char2Diacritic(line):
	if isinstance(line, str):
		line = unicode(line, 'utf-8')
	if unicodedataExist:
		line = unicodedata.normalize('NFKD', line)
		output = ''
		for c in line:
			if not unicodedata.combining(c):
				output += c

	else:
		for i, j in dictonaryDiacritic.iteritems():
			line = line.replace(i, j)

		output = line
	return output


dictonarySortCZ = {'ch': 'h|', 'CH': 'H|', 'Ch': 'H|', 'Ch': 'h|', 'Á': 'A|', 'Ä': 'A}', 'Č': 'C|', 'Ď': 'D|', 'É': 'E|', 'Ě': 'E}', 'Ë': 'E~', 'Í': 'I|', 'Ï': 'I}', 'Ĺ': 'L|', 'Ľ': 'L}', 'Ł': 'L~', 'Ň': 'N|', 'Ó': 'O|', 
   'Ô': 'O}', 'Ö': 'O~', 'Ŕ': 'R|', 'Ř': 'R}', 'Š': 'S|', 'Ť': 'T|', 'Ú': 'U|', 'Ů': 'U}', 'Ü': 'U~', 'Ý': 'Y|', 'Ÿ': 'Y}', 'Ž': 'Z|', 'á': 'a|', 'ä': 'a}', 'č': 'c|', 'ď': 'd|', 
   'é': 'e|', 'ě': 'e}', 'ë': 'e~', 'í': 'i|', 'ï': 'i}', 'ĺ': 'l|', 'ľ': 'l}', 'ł': 'l~', 'ň': 'n|', 'ó': 'o|', 'ö': 'o}', 'ô': 'o~', 'ř': 'r|', 'ŕ': 'r}', 'š': 's|', 'ť': 't|', 'ú': 'u|', 
   'ů': 'u}', 'ü': 'u~', 'ý': 'y|', 'ÿ': 'y}', 'ž': 'z|'}

def char2DiacriticSort(text):
	if isinstance(text, str):
		text = unicode(text, 'utf-8')
	for i, j in dictonarySortCZ.iteritems():
		text = text.replace(i, j)

	return text


charAllowed = '1234567890QWERTZUIOPASDFGHJKLYXCVBNMqwertzuiopasdfghjklyxcvbnm?:./\\+ -()!@;*#$^&[]\'%|;{}",<>=»«_ÁÄĄÀÂČĆÇĎÉĚËĘÈÊÍÏÎĹĽŁŇŃÓÔÖŐŒŔŘŠŚŤÚŮÜŰÙÛÝŸŽŻŹáäąàâčćçďéěëęèêíïîĺľłňńóöôőœřŕšśťúůüűùûýÿžżź\n'

def char2Allowchar(mystring, typeControl=0):
	if True:
		return mystring
	if isinstance(mystring, str):
		mystring = unicode(mystring, 'utf-8')
	if typeControl == 1:
		mystring = mystring.replace('\xa0', ' ')
	else:
		roz = set(mystring) - set(charAllowed)
		if roz is not None:
			for i in roz:
				if i == '\xa0':
					mystring = mystring.replace(i, ' ')
				else:
					mystring = mystring.replace(i, '')

	return mystring


charAllowedNumbers = '1234567890.'

def char2AllowcharNumbers(mystring):
	if isinstance(mystring, str):
		mystring = unicode(mystring, 'utf-8')
	roz = set(mystring) - set(charAllowedNumbers)
	if roz is not None:
		for i in roz:
			if i == '\xa0':
				mystring = mystring.replace(i, ' ')
			else:
				mystring = mystring.replace(i, '')

	return mystring


bigChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÄĄÀÂČĆÇĎÉĚËĘÈÊÍÏÎĹĽŁŇŃÓÔÖŐŒŔŘŠŚŤÚŮÜŰÙÛÝŸŽŻŹ'

def isBigCharInFirst(mystring):
	result = False
	if isinstance(mystring, str):
		mystring = unicode(mystring, 'utf-8')
	mystring = mystring.strip()
	if len(mystring) > 0:
		if mystring[0] in bigChar:
			result = True
	return result


def OdstranitDuplicityRadku(text):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - DuplicityRadku - zacatek\n')
	LogCSFD.WriteToFileWithoutTime(text)
	sez = text.splitlines()
	novy_text = ''
	new_sez = []
	i = 0
	k = len(sez)
	while i < k:
		j = 0
		dupl = False
		sez[i] = sez[i].strip()
		if sez[i] != '':
			while j < k:
				if j != i:
					por = sez[j].strip()
					if sez[i] == por:
						if sez[i] in new_sez:
							dupl = True
							break
					elif len(sez[i]) < len(por):
						vel = -1 * len(sez[i])
						if sez[i] == por[vel:]:
							dupl = True
							break
				j += 1

			if not dupl:
				novy_text += sez[i] + '\n'
				new_sez.append(sez[i])
		i += 1

	LogCSFD.WriteToFile('[CSFD] CSFDTools - DuplicityRadku - konec\n')
	LogCSFD.WriteToFileWithoutTime(novy_text)
	return novy_text


def CSFD_Desktop_Width():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFD_Desktop_Width - zacatek\n')
	tt = 720
	if config.misc.CSFD.Resolution.getValue() == '0':
		tt = getDesktop(0).size().width()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFD_Desktop_Width_system: ' + str(tt) + '\n')
	else:
		try:
			tt = int(config.misc.CSFD.Resolution.getValue())
			if tt < 720:
				tt = 720
			if tt > 720 and tt < 1280:
				tt = 1280
			if tt > 1280:
				tt = 1920
		except:
			tt = getDesktop(0).size().width()

	if tt is not None:
		if tt < 720:
			tt = 720
		if tt > 720 and tt < 1280:
			tt = 1280
		if tt > 1280:
			tt = 1920
	else:
		tt = 720
	LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFD_Desktop_Width: ' + str(tt) + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - CSFD_Desktop_Width - konec\n')
	return tt


def grem(path, pattern):
	pattern = re.compile(pattern)
	for each in os_listdir(path):
		if pattern.search(each) is not None:
			name = os_path.join(path, each)
			try:
				LogCSFD.WriteToFile('[CSFD] CSFDTools - mazu docasny soubor: ' + Uni8(name) + '\n')
				os_remove(name)
			except:
				LogCSFD.WriteToFile('[CSFD] CSFDTools - chyba - behem mazani docasnych souboru: ' + Uni8(name) + '\n')

	return


def deletetmpfiles():
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDQuery.*?html')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDGallPoc.html')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDVideo.*?html')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDVPoster.*?jpg')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDPoster.*?jpg')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDGallery.*?jpg')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDversion.*?txt')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDtest.*?txt')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'poster.jpg')
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'imdbquery.*?html')


def TextCompare(s, t):
	if s == t:
		return float(100)
	else:
		return float(0)


def TextSimilarityLD(s, t):
	if s == t:
		return float(100)
	vel = len(s)
	vel1 = len(t)
	if vel1 > vel:
		vel = vel1
	if vel == 0:
		return float(100)
	s = ' ' + s
	t = ' ' + t
	d = {}
	S = len(s)
	T = len(t)
	for i in range(S):
		d[(i, 0)] = i

	for j in range(T):
		d[(0, j)] = j

	for j in range(1, T):
		for i in range(1, S):
			if s[i] == t[j]:
				d[(i, j)] = d[(i - 1, j - 1)]
			else:
				d[(i, j)] = min(d[(i - 1, j)] + 1, d[(i, j - 1)] + 1, d[(i - 1, j - 1)] + 1)

	diff = d[(S - 1, T - 1)]
	return 100 - float(diff) / float(vel) * 100


def TextSimilarityBigram(str1, str2):

	def get_bigrams(string):
		s = string.lower()
		return [ s[i:i + 2] for i in xrange(len(s) - 1) ]

	if str1 == str2:
		return float(100)
	pairs1 = get_bigrams(str1.rjust(len(str2)))
	pairs2 = get_bigrams(str2.rjust(len(str1)))
	union = len(pairs1) + len(pairs2)
	hit_count = 0
	for x in pairs1:
		for y in pairs2:
			if x == y:
				hit_count += 1
				break

	return 2.0 * hit_count / union * 100


def max_positions(iterable, key=None, reverse=False):
	if key is None:

		def key(x):
			return x

	if reverse:
		better = operator.lt
	else:
		better = operator.gt
	it = iter(enumerate(iterable))
	for pos, item in it:
		break
	else:
		return (None, None)

	cur_max = key(item)
	cur_pos = [pos]
	for pos, item in it:
		k = key(item)
		if better(k, cur_max):
			cur_max = k
			cur_pos = [pos]
		elif k == cur_max:
			cur_pos.append(pos)

	return (
	 cur_max, cur_pos)


def min_positions(iterable, key=None, reverse=False):
	return max_positions(iterable, key, not reverse)


romanNumeralMap = (
 (
  'M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))

def StrtoRoman(s):
	n = 0
	try:
		n = int(s)
	except ValueError:
		n = 0
		LogCSFD.WriteToFile('[CSFD] StrtoRoman - chyba - int\n')

	return toRoman(n)


def toRoman(n):
	result = ''
	if not 0 < n < 5000:
		LogCSFD.WriteToFile('[CSFD] toRoman - chyba - rozsah\n')
		return result
	if int(n) != n:
		LogCSFD.WriteToFile('[CSFD] toRoman - chyba - int\n')
		return result
	for numeral, integer in romanNumeralMap:
		while n >= integer:
			result += numeral
			n -= integer

	return result


romanNumeralPattern = re.compile("\n	^					# beginning of string\n	   M{0,4}			   # thousands - 0 to 4 M's\n	 (CM|CD|D?C{0,3})	 # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),\n						   #			or 500-800 (D, followed by 0 to 3 C's)\n	(XC|XL|L?X{0,3})	# tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),\n						   #		or 50-80 (L, followed by 0 to 3 X's)\n	  (IX|IV|V?I{0,3})	  # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),\n						  #		   or 5-8 (V, followed by 0 to 3 I's)\n	   $				   # end of string\n	", re.VERBOSE)

def fromRoman(s):
	result = 0
	if s is None:
		LogCSFD.WriteToFile('[CSFD] fromRoman - chyba - neni string\n')
		return result
	else:
		if romanNumeralPattern.search(s) is None:
			LogCSFD.WriteToFile('[CSFD] fromRoman - chyba - ' + s + '\n')
			return result
		index = 0
		for numeral, integer in romanNumeralMap:
			while s[index:index + len(numeral)] == numeral:
				result += integer
				index += len(numeral)

		return result


def fromRomanStr(s):
	return str(fromRoman(s))


def IsThereBT_Parameters():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsThereBT_Parameters - zacatek\n')
	OK = True
	try:
		from enigma import BT_SCALE, BT_KEEP_ASPECT_RATIO
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsThereBT_Parameters - Ano\n')
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsThereBT_Parameters - Ne\n')
		OK = False

	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsThereBT_Parameters - konec\n')
	return OK


@defer.inlineCallbacks
def IsHTTPSWorkingTwistedWeb():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorkingTwistedWeb - zacatek\n')
	OK = True
	url = csfd_URL_https
	try:
		r = yield getPage(url, contextFactory=ClientContextFactoryCSFD, headers=std_headers, timeout=config.misc.CSFD.TechnicalDownloadTimeOut.getValue())
	except:
		OK = False
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorkingTwistedWeb - neni funkcni stahovani HTTPS v twisted web - ' + url + '\n')
		LogCSFD.WriteToFile(err)

	CSFDGlobalVar.setHTTPSWorkingTwistedWeb(OK)
	if OK:
		CSFDGlobalVar.setHTTP('https')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorkingTwistedWeb - OK - ' + url + '\n')
	else:
		CSFDGlobalVar.setHTTP('http')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorkingTwistedWeb - NOT OK - ' + url + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorkingTwistedWeb - konec\n')


def IsHTTPSWorking(testTwisted=True):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorking - zacatek\n')
	if testTwisted:
		IsHTTPSWorkingTwistedWeb()
	OK = True
	url = csfd_URL_https
	try:
		r = urllib2.Request(url, headers=std_media_header)
		response = urllib2.urlopen(r)
		response.read()
		response.close()
	except:
		OK = False
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorking - neni funkcni stahovani HTTPS v urllib2 - ' + url + '\n')
		LogCSFD.WriteToFile(err)

	if not OK and testTwisted:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorking - nastavuji vysledek podle IsHTTPSWorkingTwistedWeb\n')
		OK = CSFDGlobalVar.getHTTPSWorkingTwistedWeb()
	if OK:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorking - OK - ' + url + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsHTTPSWorking - konec\n')
	return OK


def closeIsTwistedFollowRedirect(string):
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDtest.*?txt')


def IsTwistedFollowRedirect():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedFollowRedirect - zacatek\n')
	OK = True
	url = google_URL
	output = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDtest.txt'
	try:
		downloadPage(url, output, followRedirect=True, headers=std_media_header).addCallback(closeIsTwistedFollowRedirect)
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedFollowRedirect - neni funkcni redirect pro twisted web - ' + url + '\n')
		OK = False

	if OK:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedFollowRedirect - OK - ' + url + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedFollowRedirect - konec\n')
	return OK


def closeIsTwistedUseCookies(string):
	grem(CSFDGlobalVar.getCSFDadresarTMP(), 'CSFDtest.*?txt')


def IsTwistedUseCookies():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedUseCookies - zacatek\n')
	OK = True
	url = google_URL
	output = CSFDGlobalVar.getCSFDadresarTMP() + 'CSFDtest.txt'
	cookies = CSFDGlobalVar.getCSFDCookies()
	try:
		downloadPage(url, output, headers=std_media_header, cookies=cookies).addCallback(closeIsTwistedUseCookies)
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedUseCookies - neni funkcni parametr cookies pro twisted web - ' + url + '\n')
		OK = False

	if OK:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedUseCookies - OK - ' + url + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - IsTwistedUseCookies - konec\n')
	return OK


CSFDdownloader = LimitedDownloader(4)

def InitSetDownloadType():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - zacatek\n')
	if config.misc.CSFD.DownloadType.getValue() == '0':
		if twistedwebExist and CSFDGlobalVar.getOpenSSLexist() and CSFDGlobalVar.getOpenSSLcontext():
			LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - Auto WebDownload TwistedWeb\n')
			CSFDGlobalVar.setWebDownload(0)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - Auto WebDownload Urllib2\n')
			CSFDGlobalVar.setWebDownload(1)
	elif config.misc.CSFD.DownloadType.getValue() == '1':
		LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - WebDownload TwistedWeb\n')
		CSFDGlobalVar.setWebDownload(0)
	elif config.misc.CSFD.DownloadType.getValue() == '2':
		LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - WebDownload Urllib2\n')
		CSFDGlobalVar.setWebDownload(1)
	elif twistedwebExist and CSFDGlobalVar.getOpenSSLexist() and CSFDGlobalVar.getOpenSSLcontext():
		LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - Nedef. WebDownload TwistedWeb\n')
		CSFDGlobalVar.setWebDownload(0)
	else:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - Nedef. WebDownload Urllib2\n')
		CSFDGlobalVar.setWebDownload(1)
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitSetDownloadType - konec\n')


def InitCSFDTools():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools - zacatek\n')
	if twistedwebExist and config.misc.CSFD.LogTwistedWeb.getValue():
		sb = file(LogCSFD.GetNameTwistedLog(), 'w')
		sb.close()
		startLogging(file(LogCSFD.GetNameTwistedLog(), 'w'), setStdout=0)
	CSFDGlobalVar.setCSFDBoxType(getBoxtypeCSFD())
	ImageType, ImageCompatibility = getImagetype()
	CSFDGlobalVar.setCSFDImageType(ImageType)
	CSFDGlobalVar.setCSFDImageCompatibility(ImageCompatibility)
	CSFDGlobalVar.setCSFDDesktopWidth(CSFD_Desktop_Width())
	CSFDGlobalVar.setCSFDoeVersion(CSFDGlobalVar.getCSFDBoxType()[3])
	CSFDGlobalVar.setCSFDEnigmaVersion(CSFDGlobalVar.getCSFDBoxType()[4])
	CSFDGlobalVar.setCSFDInstallCommand(GetInstallCommand())
	CSFDGlobalVar.setBTParameters(IsThereBT_Parameters())
	CSFDGlobalVar.setIsTwistedWithCookies(IsTwistedUseCookies())
	InitSetDownloadType()
	if CSFDGlobalVar.getWebDownload() == 0:
		try:
			IsHTTPSWorkingTwistedWeb()
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools  - IsHTTPSWorkingTwistedWeb - neni funkcni - ERR - chyba\n')
			LogCSFD.WriteToFile(err)
			CSFDGlobalVar.setHTTPSWorkingTwistedWeb(False)
			CSFDGlobalVar.setHTTP('http')

	elif IsHTTPSWorking(testTwisted=False):
		CSFDGlobalVar.setHTTP('https')
	else:
		LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools  - IsHTTPSWorking - neni funkcni - ERR - chyba\n')
		CSFDGlobalVar.setHTTP('http')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools - konec\n')


InitCSFDTools()

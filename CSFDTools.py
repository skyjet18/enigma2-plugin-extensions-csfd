# -*- coding: utf-8 -*-

from .CSFDLog import LogCSFD
from enigma import getDesktop, eListboxPythonMultiContent, eListboxPythonStringContent, gFont
from os import remove as os_remove, listdir as os_listdir, path as os_path
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import config, std_media_header
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from .CSFDMenuList import CSFDMenuList
import re, sys, operator, traceback
import requests
from .compat import ePicloadDecodeData

if sys.version_info[0] == 3:
	xrange = range
	unicode = str

csfd_session = requests.Session()

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

http_adaptor = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1))
csfd_session.mount('http://', http_adaptor)
csfd_session.mount('https://', http_adaptor)

try:
	import unicodedata
	unicodedataExist = True
except:
	unicodedataExist = False

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
	filename = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/%s' % name)
	ptr = ePicloadDecodeData( pic, filename )
	
	if ptr is None:
		filename = resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/icons/%s' % name)
		ptr = ePicloadDecodeData( pic, filename )
		
	return ptr


def strUni(mystring):
	if sys.version_info[0] < 3 and not isinstance(mystring, str):
		return str(mystring.encode('utf-8'))
	else:
		return mystring


def Uni8(mystring):
	if sys.version_info[0] < 3 and isinstance(mystring, str):
		return unicode(mystring, 'utf-8', errors='ignore')
	else:
		return mystring


def ExtractNumbers(mystring):
	return re.findall('\\b\\d+\\b', mystring)


def request(url, headers={}, timeout=None):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - url: %s\n' % Uni8(url))
	
	if timeout == None:
		timeout = config.misc.CSFD.DownloadTimeOut.getValue()
		
	try:
		data = csfd_session.get( url, headers=headers, timeout=timeout, stream=True ).raw.read()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - request - OK\n')
	except:
		data = None
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - request - chyba\n')
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] CSFDTools - request - konec\n')
	return data


def requestFileCSFD(url='', fileout='' ):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - zacatek\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - url: %s\n' % Uni8(url))

	if fileout == '':
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - Neni co stahovat\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - konec\n')
		return False
	
	timeout = config.misc.CSFD.DownloadTimeOut.getValue()
	ret = True
	
	try:
		with open(fileout, 'wb') as f:
			f.write( csfd_session.get( url, headers=std_media_header, timeout=timeout, stream=True ).raw.read() )
		
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - OK\n')
	except:
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - chyba\n')
		LogCSFD.WriteToFile(err)
		ret = False

	LogCSFD.WriteToFile('[CSFD] CSFDTools - requestFileCSFD - konec\n')
	return ret


class CSFDHelpableActionMapChng(ActionMap):

	def __init__(self, parent, context, actions=None, prio=0):
		if actions is None:
			actions = {}
		alist = []
		adict = {}
		for action, funchelp in list(actions.items()):
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


def internet_on(timeout_s=1):
	if not config.misc.CSFD.InternetTest.getValue():
		return True
	OK = False
	try:
		csfd_session.get("https://www.google.cz", timeout=timeout_s, stream=True).raw.read()
		OK = True
	except:
		OK = False
		err = traceback.format_exc()
		LogCSFD.WriteToFile('[CSFD] CSFDTools - internet_on - chyba\n')
		LogCSFD.WriteToFile('[CSFD] CSFDTools - internet_on - timeout_s: ' + str(timeout_s) + '\n')
		LogCSFD.WriteToFile(err)

	if not OK and timeout_s < 3:
		timeout_s += 3
		OK = internet_on(timeout_s)
	return OK


def substr(data, start, end):
	i1 = data.find(start)
	i2 = data.find(end, i1)
	return data[i1:i2]


def GetInstallCommand():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand - zacatek\n')

	if config.misc.CSFD.InstallCommand.getValue() == 'default':
		inst_c = config.misc.CSFD.InstallCommand.getValue()
	elif os_path.exists('/usr/bin/opkg'):
		inst_c = 'opkg'
	elif os_path.exists('/usr/bin/dpkg'):
		inst_c = 'dpkg'

	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand: %s\n' % Uni8(inst_c))
	LogCSFD.WriteToFile('[CSFD] CSFDTools - GetInstallCommand - konec\n')
	return inst_c


def getBoxtypeCSFD():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxTypeCSFD - zacatek\n')
	
	box = None
	for p in [ '/proc/stb/info/vumodel', '/proc/stb/info/model' ]:
		try:
			with open(p, 'r') as f:
				box = f.readline().strip()
			break
		except:
			pass
		
	model = 'Unknown'
	if box != None:
		if box == 'dm800':
			model = '800'
		elif box == 'dm800se':
			model = '800se'
		elif box == 'dm8000' or box == "dm7020hd" or box == "dm7080" or box == 'dm7080hd':
			model = '8000'
		elif box == 'dm900hd' or box == 'dm900':
			model = '900'

	version, enigma = Uni8(getBoxArch())
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - box=' + box + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - Model=' + model + '; Image=' + version + '; Enigma=' + enigma + '\n')
	LogCSFD.WriteToFile('[CSFD] CSFDTools - BoxType - konec\n')
	return (model, version, enigma)


def getBoxArch():
	ARCH = 'unknown'
	enigma = '2'
	if sys.version_info < (2, 6, 9) and sys.version_info > (2, 6, 6):
		ARCH = 'oe16'
		enigma = '2'
	if sys.version_info > (2, 7, 0):
		ARCH = 'oe20'
		enigma = '3'
	if os_path.exists('/usr/bin/dpkg'):
		ARCH = 'oe22'

	try:
		from enigma import eMediaDatabase
		ARCH = 'oe22'
		enigma = '4'
	except:
		pass

	return (ARCH, enigma)


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
	if sys.version_info[0] < 3 and isinstance(line, str):
		line = unicode(line, 'utf-8')
	if unicodedataExist:
		line = unicodedata.normalize('NFKD', line)
		output = ''
		for c in line:
			if not unicodedata.combining(c):
				output += c

	else:
		for i, j in list(dictonaryDiacritic.items()):
			line = line.replace(i, j)

		output = line
	return output


dictonarySortCZ = {'ch': 'h|', 'CH': 'H|', 'Ch': 'H|', 'Ch': 'h|', 'Á': 'A|', 'Ä': 'A}', 'Č': 'C|', 'Ď': 'D|', 'É': 'E|', 'Ě': 'E}', 'Ë': 'E~', 'Í': 'I|', 'Ï': 'I}', 'Ĺ': 'L|', 'Ľ': 'L}', 'Ł': 'L~', 'Ň': 'N|', 'Ó': 'O|', 
   'Ô': 'O}', 'Ö': 'O~', 'Ŕ': 'R|', 'Ř': 'R}', 'Š': 'S|', 'Ť': 'T|', 'Ú': 'U|', 'Ů': 'U}', 'Ü': 'U~', 'Ý': 'Y|', 'Ÿ': 'Y}', 'Ž': 'Z|', 'á': 'a|', 'ä': 'a}', 'č': 'c|', 'ď': 'd|', 
   'é': 'e|', 'ě': 'e}', 'ë': 'e~', 'í': 'i|', 'ï': 'i}', 'ĺ': 'l|', 'ľ': 'l}', 'ł': 'l~', 'ň': 'n|', 'ó': 'o|', 'ö': 'o}', 'ô': 'o~', 'ř': 'r|', 'ŕ': 'r}', 'š': 's|', 'ť': 't|', 'ú': 'u|', 
   'ů': 'u}', 'ü': 'u~', 'ý': 'y|', 'ÿ': 'y}', 'ž': 'z|'}

def char2DiacriticSort(text):
	if sys.version_info[0] < 3 and isinstance(text, str):
		text = unicode(text, 'utf-8')
	for i, j in list(dictonarySortCZ.items()):
		text = text.replace(i, j)

	return text


charAllowed = '1234567890QWERTZUIOPASDFGHJKLYXCVBNMqwertzuiopasdfghjklyxcvbnm?:./\\+ -()!@;*#$^&[]\'%|;{}",<>=»«_ÁÄĄÀÂČĆÇĎÉĚËĘÈÊÍÏÎĹĽŁŇŃÓÔÖŐŒŔŘŠŚŤÚŮÜŰÙÛÝŸŽŻŹáäąàâčćçďéěëęèêíïîĺľłňńóöôőœřŕšśťúůüűùûýÿžżź\n'
bigChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÄĄÀÂČĆÇĎÉĚËĘÈÊÍÏÎĹĽŁŇŃÓÔÖŐŒŔŘŠŚŤÚŮÜŰÙÛÝŸŽŻŹ'

try:
	charAllowed = charAllowed.decode('utf-8')
	bigChar = bigChar.decode('utf-8')
except:
	pass

def char2Allowchar(mystring, typeControl=0):
#	if True:
#		return mystring
	if isinstance(mystring, str):
		try:
			mystring = unicode(mystring, 'utf-8', errors='ignore')
		except:
			pass
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
	if sys.version_info[0] < 3 and isinstance(mystring, str):
		mystring = unicode(mystring, 'utf-8')
	roz = set(mystring) - set(charAllowedNumbers)
	if roz is not None:
		for i in roz:
			if i == '\xa0':
				mystring = mystring.replace(i, ' ')
			else:
				mystring = mystring.replace(i, '')

	return mystring


def isBigCharInFirst(mystring):
	result = False
	if sys.version_info[0] < 3 and isinstance(mystring, str):
		mystring = unicode(mystring, 'utf-8')
	mystring = mystring.strip()
	if len(mystring) > 0:
		if mystring[0] in bigChar:
			result = True
	return result


def OdstranitDuplicityRadku(text):
	LogCSFD.WriteToFile('[CSFD] CSFDTools - DuplicityRadku - zacatek\n')
	LogCSFD.WriteToFileWithoutTime(text + '\n')
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
	for name in [ 'CSFDVPoster.*?jpg', 'CSFDPoster.*?jpg', 'CSFDGallery.*?jpg', 'CSFDversion.*?txt', 'imdbquery.*?html' ]:
		grem(CSFDGlobalVar.getCSFDadresarTMP(), name )


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
	('M',  1000),
	('CM', 900),
	('D',  500),
	('CD', 400),
	('C',  100),
	('XC', 90),
	('L',  50),
	('XL', 40),
	('X',  10),
	('IX', 9),
	('V',  5),
	('IV', 4),
	('I',  1)
)

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

def CheckValidValue( value, value_valid = "" ):
	return str(value) if value != None else value_valid

def CreateNameSurname( data, name_key = "firstname", surname_key = "surname" ):
	try:
		ret = CheckValidValue( data[name_key] )
	except:
		ret = ""
	
	try:
		surname = data[surname_key]
		ret += " " + surname if len( ret ) > 0 else surname
	except:
		pass
	
	return ret

def CreateNameSurnameList( data ):
	return ', '.join( CreateNameSurname(x) for x in data )

def AddLine( text ):
	return text + '\n' if len(text) > 0 else ""

def CreateStrList( data, delim=', ', all_valid=False ):
	if all_valid:
		for x in data:
			if x is None or len(x) == 0:
				return ''
	return delim.join( x for x in data if x is not None and len(x) > 0 )

try:
	import unidecode
	
	def StripAccents(s):
		return unidecode.unidecode(s)
except:
	import unicodedata
	
	def StripAccents(s):
		try:
			# py2
			s = s.decode('utf-8')
		except:
			pass
		return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def InitCSFDTools():
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools - zacatek\n')
	CSFDGlobalVar.setCSFDBoxType(getBoxtypeCSFD())
	ImageType, ImageCompatibility = getImagetype()
	CSFDGlobalVar.setCSFDImageType(ImageType)
	CSFDGlobalVar.setCSFDImageCompatibility(ImageCompatibility)
	CSFDGlobalVar.setCSFDDesktopWidth(CSFD_Desktop_Width())
	CSFDGlobalVar.setCSFDoeVersion(CSFDGlobalVar.getCSFDBoxType()[1])
	CSFDGlobalVar.setCSFDEnigmaVersion(CSFDGlobalVar.getCSFDBoxType()[2])
	CSFDGlobalVar.setCSFDInstallCommand(GetInstallCommand())
	CSFDGlobalVar.setBTParameters(IsThereBT_Parameters())
	LogCSFD.WriteToFile('[CSFD] CSFDTools - InitCSFDTools - konec\n')

InitCSFDTools()

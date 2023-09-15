# -*- coding: utf-8 -*-

from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screens.Screen import Screen
from Components.Language import language
from Components.ActionMap import HelpableActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from .CSFDLog import LogCSFD
from .CSFDSettings1 import CSFDGlobalVar

try:
	# py2
	unicode
	unichr
except:
	# py3
	unicode = str
	unichr = chr
	
class VirtualKeyBoardList(MenuList):

	def __init__(self, listP, enableWrapAround=False):
		MenuList.__init__(self, listP, enableWrapAround, eListboxPythonMultiContent)
		try:
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.l.setItemHeight(45)
				if 'setFont' in dir(self.l):
					self.l.setFont(0, gFont('Regular', 28))
				else:
					LogCSFD.WriteToFile('[CSFD] VirtualKeyBoardList - nelze nastavit velikost fontu - stara verze enigma2)\n')
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
				self.l.setItemHeight(65)
				if 'setFont' in dir(self.l):
					self.l.setFont(0, gFont('Regular', 36))
				else:
					LogCSFD.WriteToFile('[CSFD] VirtualKeyBoardList - nelze nastavit velikost fontu - stara verze enigma2)\n')
			else:
				self.l.setItemHeight(87)
				if 'setFont' in dir(self.l):
					self.l.setFont(0, gFont('Regular', 48))
				else:
					LogCSFD.WriteToFile('[CSFD] VirtualKeyBoardList - nelze nastavit velikost fontu - stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] VirtualKeyBoardList - chyba - nelze nastavit velikost fontu - stara verze enigma2)\n')


def VirtualKeyBoardEntryComponent(keys, selectedKey, shiftMode=False):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		h = 45
		key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_backspace.png'))
		key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_bg.png'))
		key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_clr.png'))
		key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_esc.png'))
		key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_ok.png'))
		key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_sel.png'))
		key_shift = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift.png'))
		key_shift_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift_sel.png'))
		key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_space.png'))
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
		h = 65
		key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_backspace_fhd.png'))
		key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_bg_fhd.png'))
		key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_clr_fhd.png'))
		key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_esc_fhd.png'))
		key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_ok_fhd.png'))
		key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_sel_fhd.png'))
		key_shift = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift_fhd.png'))
		key_shift_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift_sel_fhd.png'))
		key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_space_fhd.png'))
	else:
		h = 87
		key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_backspace_fhd.png'))
		key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_bg_fhd.png'))
		key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_clr_fhd.png'))
		key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_esc_fhd.png'))
		key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_ok_fhd.png'))
		key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_sel_fhd.png'))
		key_shift = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift_fhd.png'))
		key_shift_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_shift_sel_fhd.png'))
		key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_space_fhd.png'))
	res = [
	 keys]
	x = 0
	count = 0
	if shiftMode:
		shiftkey_png = key_shift_sel
	else:
		shiftkey_png = key_shift
	for key in keys:
		width = None
		if key == 'EXIT':
			width = key_esc.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_esc))
		elif key == 'BACKSPACE':
			width = key_backspace.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_backspace))
		elif key == 'CLEAR':
			width = key_clr.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_clr))
		elif key == 'SHIFT':
			width = shiftkey_png.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=shiftkey_png))
		elif key == 'SPACE':
			width = key_space.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_space))
		elif key == 'OK':
			width = key_ok.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_ok))
		else:
			width = key_bg.size().width()
			res.extend((
			 MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_bg),
#			 MultiContentEntryText(pos=(x, 0), size=(width, h), font=0, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
			 MultiContentEntryText(pos=(x, 0), size=(width, h), font=0, text=str(key), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
		if selectedKey == count:
			width = key_sel.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=key_sel))
		if width is not None:
			x += width
		else:
			x += h
		count += 1

	return res


class CSFDVirtualKeyBoard(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardSD
		skin = Screen_CSFDVirtualKeyBoardSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardHD
		skin = Screen_CSFDVirtualKeyBoardHD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
		from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardFullHD
		skin = Screen_CSFDVirtualKeyBoardFullHD
	else:
		from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardWQHD
		skin = Screen_CSFDVirtualKeyBoardWQHD

	def __init__(self, session, title='', text=''):
		from .CSFDSettings2 import config
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardSD
			self.skin = Screen_CSFDVirtualKeyBoardSD
		else:
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardHD
				self.skin = Screen_CSFDVirtualKeyBoardHD
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
				from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardFullHD
				self.skin = Screen_CSFDVirtualKeyBoardFullHD
			else:
				from .CSFDSkinLoader import Screen_CSFDVirtualKeyBoardWQHD
				self.skin = Screen_CSFDVirtualKeyBoardWQHD
			Screen.__init__(self, session)
			if config.misc.CSFD.Skinxml.getValue():
				if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
					self.skinName = [
					 'CSFDVirtualKeyBoardSD', 'CSFDVirtualKeyBoard']
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
					self.skinName = [
					 'CSFDVirtualKeyBoardHD', 'CSFDVirtualKeyBoard']
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
					self.skinName = [
					 'CSFDVirtualKeyBoardFullHD', 'CSFDVirtualKeyBoard']
				else:
					self.skinName = [
					 'CSFDVirtualKeyBoardWQHD', 'CSFDVirtualKeyBoard']
			else:
				self.skinName = 'CSFDVirtualKeyBoard__'
			self.keys_list = []
			self.shiftkeys_list = []
			self.lang = language.getLanguage()
			self.nextLang = None
			self.shiftMode = False
			self.text = text
			self.selectedKey = 0
			self['country'] = StaticText('')
			self['countryFlag'] = Pixmap()
			self['header'] = Label(title)
			self['text'] = Label(self.text)
			self['list'] = VirtualKeyBoardList([])
			self['actions'] = HelpableActionMap(self, 'CSFDVirtualKeyboard', {'gotAsciiCode': self.keyGotAscii, 
			   'ok': self.okClicked, 
			   'cancel': self.exit, 
			   'left': self.left, 
			   'right': self.right, 
			   'up': self.up, 
			   'down': self.down, 
			   'red': self.backClicked, 
			   'green': self.ok, 
			   'yellow': self.switchLang, 
			   'deleteBackward': self.backClicked, 
			   'back': self.exit}, -2)
			self.setLang()
			try:
				self.onExecBegin.append(self.setKeyboardModeAscii)
			except:
				pass

		self.onLayoutFinish.append(self.buildVirtualKeyBoard)
		return

	def switchLang(self):
		self.lang = self.nextLang
		self.setLang()
		self.buildVirtualKeyBoard()

	def setLang(self):
		if self.lang == 'de_DE':
			self.keys_list = [['EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '@', 'ß', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', "'"],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'OK']]
			self.nextLang = 'es_ES'
		elif self.lang == 'es_ES':
			self.keys_list = [
			 [
			  'EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ú', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ó', 'á', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '@', 'Ł', 'ŕ', 'é', 'č', 'í', 'ě', 'ń', 'ň', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ú', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ó', 'Á', "'"],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'Ŕ', 'É', 'Č', 'Í', 'Ě', 'Ń', 'Ň', 'OK']]
			self.nextLang = 'fi_FI'
		elif self.lang == 'fi_FI':
			self.keys_list = [['EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'é', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '@', 'ß', 'ĺ', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'É', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', "'"],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'Ĺ', 'OK']]
			self.nextLang = 'sv_SE'
		elif self.lang == 'sv_SE':
			self.keys_list = [['EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'é', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '@', 'ß', 'ĺ', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'É', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', "'"],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'Ĺ', 'OK']]
			self.nextLang = 'sk_SK'
		elif self.lang == 'sk_SK':
			self.keys_list = [['EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ú', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ľ', '@', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', 'š', 'č', 'ž', 'ý', 'á', 'í', 'é', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'ť', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'ň', 'ď', "'"],
			 [
			  'Á', 'É', 'Ď', 'Í', 'Ý', 'Ó', 'Ú', 'Ž', 'Š', 'Č', 'Ť', 'Ň'],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'ä', 'ö', 'ü', 'ô', 'ŕ', 'ĺ', 'OK']]
			self.nextLang = 'cs_CZ'
		elif self.lang == 'cs_CZ':
			self.keys_list = [['EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ú', '+'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ů', '@', '#'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', 'ě', 'š', 'č', 'ř', 'ž', 'ý', 'á', 'í', 'é', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'ť', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'ň', 'ď', "'"],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', '?', '\\', 'Č', 'Ř', 'Š', 'Ž', 'Ú', 'Á', 'É', 'OK']]
			self.nextLang = 'en_EN'
		else:
			self.keys_list = [
			 [
			  'EXIT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BACKSPACE'],
			 [
			  'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', '+', '@'],
			 [
			  'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '#', '\\'],
			 [
			  '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', 'OK']]
			self.shiftkeys_list = [
			 [
			  'EXIT', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', 'BACKSPACE'],
			 [
			  'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', '*'],
			 [
			  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', "'", '?'],
			 [
			  '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', 'CLEAR'],
			 [
			  'SHIFT', 'SPACE', 'OK']]
			self.lang = 'en_EN'
			self.nextLang = 'de_DE'
		self['country'].setText(self.lang)
		self.max_key = 47 + len(self.keys_list[4])

	def buildVirtualKeyBoard(self, selectedKey=0):
		listP = []
		if self.shiftMode:
			self.k_list = self.shiftkeys_list
			for keys in self.k_list:
				if selectedKey < 12 and selectedKey > -1:
					listP.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
				else:
					listP.append(VirtualKeyBoardEntryComponent(keys, -1, True))
				selectedKey -= 12

		else:
			self.k_list = self.keys_list
			for keys in self.k_list:
				if selectedKey < 12 and selectedKey > -1:
					listP.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
				else:
					listP.append(VirtualKeyBoardEntryComponent(keys, -1))
				selectedKey -= 12

		self['list'].setList(listP)
		name = self.lang[3:].lower()
		self['countryFlag'].instance.setPixmapFromFile('/usr/share/enigma2/countries/' + name + '.png')

	def backClicked(self):
#		ss = unicode(self['text'].getText(), 'utf-8')
		ss = self['text'].getText()
		ss = ss[:-1]
#		self.text = str(ss.encode('utf-8'))
		self.text = str(ss)
		self['text'].setText(self.text)

	def okClicked(self):
		if self.shiftMode:
			listP = self.shiftkeys_list
		else:
			listP = self.keys_list
		selectedKey = self.selectedKey
		text = None
		for x in listP:
			if selectedKey < 12:
				if selectedKey < len(x):
					text = x[selectedKey]
				break
			else:
				selectedKey -= 12

		if text is None:
			return
		else:
#			text = text.encode('utf-8')
			if text == 'EXIT':
				self.close(None)
			elif text == 'BACKSPACE':
#				ss = unicode(self['text'].getText(), 'utf-8')
				ss = self['text'].getText()
				ss = ss[:-1]
#				self.text = str(ss.encode('utf-8'))
				self.text = str(ss)
				self['text'].setText(str(self.text))
			elif text == 'CLEAR':
				self.text = ''
				self['text'].setText(str(self.text))
			elif text == 'SHIFT':
				if self.shiftMode:
					self.shiftMode = False
				else:
					self.shiftMode = True
				self.buildVirtualKeyBoard(self.selectedKey)
			elif text == 'SPACE':
				self.text += ' '
				self['text'].setText(str(self.text))
			elif text == 'OK':
				self.close(self['text'].getText())
			else:
				self.text = self['text'].getText()
				self.text += text
				self['text'].setText(str(self.text))
			return

	def ok(self):
		self.close(self['text'].getText())

	def exit(self):
		self.close(None)
		return

	def left(self):
		self.selectedKey -= 1
		if self.selectedKey == -1:
			self.selectedKey = 11
		elif self.selectedKey == 11:
			self.selectedKey = 23
		elif self.selectedKey == 23:
			self.selectedKey = 35
		elif self.selectedKey == 35:
			self.selectedKey = 47
		elif self.selectedKey == 47:
			self.selectedKey = self.max_key
		self.showActiveKey()

	def right(self):
		self.selectedKey += 1
		if self.selectedKey == 12:
			self.selectedKey = 0
		elif self.selectedKey == 24:
			self.selectedKey = 12
		elif self.selectedKey == 36:
			self.selectedKey = 24
		elif self.selectedKey == 48:
			self.selectedKey = 36
		elif self.selectedKey > self.max_key:
			self.selectedKey = 48
		self.showActiveKey()

	def up(self):
		self.selectedKey -= 12
		if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
			self.selectedKey += 48
		elif self.selectedKey < 0:
			self.selectedKey += 60
		self.showActiveKey()

	def down(self):
		self.selectedKey += 12
		if self.selectedKey > self.max_key and self.selectedKey > 59:
			self.selectedKey -= 60
		elif self.selectedKey > self.max_key:
			self.selectedKey -= 48
		self.showActiveKey()

	def showActiveKey(self):
		self.buildVirtualKeyBoard(self.selectedKey)

	def inShiftKeyList(self, key):
		for KeyList in self.shiftkeys_list:
			for char in KeyList:
				if char == key:
					return True

		return False

	def keyGotAscii(self):
#		char = str(unichr(getPrevAsciiCode()).encode('utf-8'))
		char = str(chr(getPrevAsciiCode()))
		st_shift = self.shiftMode
		if self.inShiftKeyList(char):
			self.shiftMode = True
			listP = self.shiftkeys_list
		else:
			self.shiftMode = False
			listP = self.keys_list
		selkey = 0
		if char == ' ':
			char = 'SPACE'
			self.shiftMode = False
			listP = self.keys_list
		for keylist in listP:
			for key in keylist:
				if key == char:
					self.selectedKey = selkey
					self.okClicked()
					self.showActiveKey()
					return
				selkey += 1

		self.shiftMode = st_shift
		self.text = self['text'].getText()
		self.text += char
		self['text'].setText(self.text)

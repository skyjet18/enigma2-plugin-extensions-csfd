# -*- coding: utf-8 -*-

from .CSFDSettings2 import config
from .CSFDSettings2 import _
from .CSFDLog import LogCSFD
from Screens.Screen import Screen
from Components.config import configfile
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Button import Button
from .CSFDTools import strUni, Uni8, ItemListString
from .CSFDSkinLoader import *
from .CSFDSettings1 import CSFDGlobalVar
from enigma import ePicLoad, gPixmapPtr, gFont
from os import path as os_path, listdir as os_listdir
import traceback
from .compat import ePicloadDecodeData

class CSFDSkinSelect(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDSkinSelectSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDSkinSelectHD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
		skin = Screen_CSFDSkinSelectFullHD
	else:
		skin = Screen_CSFDSkinSelectWQHD

	def __init__(self, session):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDSkinSelectSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDSkinSelectHD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
			self.skin = Screen_CSFDSkinSelectFullHD
		else:
			self.skin = Screen_CSFDSkinSelectWQHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDSkinSelectSD', 'CSFDSkinSelect']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDSkinSelectHD', 'CSFDSkinSelect']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
				self.skinName = [
				 'CSFDSkinSelectFullHD', 'CSFDSkinSelect']
			else:
				self.skinName = [
				 'CSFDSkinSelectWQHD', 'CSFDSkinSelect']
		else:
			self.skinName = 'CSFDSkinSelect__'
		self['actions'] = ActionMap(['CSFDSkinSelection'], {'ok': self.keyOK, 
		   'cancel': self.keyCancel, 
		   'green': self.keyOK, 
		   'red': self.keyCancel, 
		   'blue': self.keyReset, 
		   'up': self.keyUp, 
		   'down': self.keyDown, 
		   'left': self.keyLeft, 
		   'right': self.keyRight}, -1)
		self.session = session
		self.onLayoutFinish.append(self.layoutFinished)
		self.resultlist = []
		self['menu'] = ItemListString([])
		self['author'] = Label(_('Autor skinu:'))
		self['email'] = Label(_('Email:'))
		self['description'] = Label('Test')
		self['preview'] = Pixmap()
		self.previewload = ePicLoad()
		self['key_red'] = Button(_('Zpět'))
		self['key_green'] = Button(_('Změnit'))
		self['key_blue'] = Button(_('Reset'))

	def layoutFinished(self):
		sss = _('Výběr skinu pro plugin CSFD')
		self.setTitle(sss)
		sc = AVSwitch().getFramebufferScale()
		self.previewload.setPara((self['preview'].instance.size().width(), self['preview'].instance.size().height(), sc[0], sc[1], False, 1, '#31000000'))
		LogCSFD.WriteToFile('[CSFD] CSFDSkinSelect - change font\n')
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
			h1 = h + 2
		if CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
			h1 = h + 3
		else:
			h = int(config.misc.CSFD.FontHeightWQHD.getValue())
			h1 = h + 4
		try:
			self['menu'].instance.setItemHeight(h1)
			if 'setFont' in dir(self['menu'].instance):
				self['menu'].instance.setFont(gFont('Regular', h))
			else:
				LogCSFD.WriteToFile('[CSFD] CSFDSkinSelect - nelze nastavit velikost fontu (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDSkinSelect - chyba - nelze nastavit velikost fontu (stara verze enigma2)\n')

		self.LoadSkins()
		self.updateInfo()

	def keyOK(self):
		LogCSFD.WriteToFile('[CSFD] SkinSelect - Zmena skinu - zacatek\n')
		newskin = self['menu'].getCurrent()[0]
		if config.misc.CSFD.CurrentSkin.getValue() == newskin:
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Zmena skinu - neni treba menit, vybrany skin je stejny - konec\n')
			self.close(0)
			return
		config.misc.CSFD.CurrentSkin.setValue(newskin)
		config.misc.CSFD.save()
		module = 'CSFDSkin_Default'
		LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - Reload Defaultniho skinu\n')
		try:
			exec('import %s.%s' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - Reload Defaultniho skinu 1\n')
			exec('reload(%s.%s)' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - Reload Defaultniho skinu 2\n')
			exec('from .%s.%s import *' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - Reload Defaultniho skinu OK\n')
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - Reload Defaultniho skinu ERR\n')
			LogCSFD.WriteToFile(err)

		module = 'CSFDSkin_' + config.misc.CSFD.CurrentSkin.getValue()
		LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena - %s\n' % module)
		try:
			exec('import %s.%s' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena 1 - %s\n' % module)
			exec('reload(%s.%s)' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena 2 - %s\n' % module)
			exec('from .%s.%s import *' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena OK - %s\n' % module)
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] SkinSelect - zmena ERR - %s\n' % module)
			LogCSFD.WriteToFile(err)

		SKIN_DefaultSetup()
		SKIN_Setup()
		config.misc.CSFD.save()
		configfile.save()
		LogCSFD.WriteToFile('[CSFD] SkinSelect - Zmena skinu - konec\n')
		self.close(1)

	def keyReset(self):
		if self['key_blue'].getText() != '':
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reset skinu - zacatek\n')
			SKIN_DefaultSetup()
			SKIN_Setup()
			config.misc.CSFD.save()
			configfile.save()
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reset skinu - konec\n')
			self.close(2)

	def keyCancel(self):
		self.close(0)

	def keyUp(self):
		self['menu'].instance.moveSelection(self['menu'].instance.moveUp)
		self.updateInfo()

	def keyDown(self):
		self['menu'].instance.moveSelection(self['menu'].instance.moveDown)
		self.updateInfo()

	def keyLeft(self):
		self['menu'].instance.moveSelection(self['menu'].instance.pageUp)
		self.updateInfo()

	def keyRight(self):
		self['menu'].instance.moveSelection(self['menu'].instance.pageDown)
		self.updateInfo()

	def updateInfo(self):
		self['author'].setText(_('Autor skinu:') + ' ' + strUni(self['menu'].getCurrent()[1]))
		self['email'].setText(_('Email:') + ' ' + strUni(self['menu'].getCurrent()[2]))
		self['description'].setText(strUni(self['menu'].getCurrent()[3]))
		self.paintPreview(self['menu'].getCurrent()[4])
		if config.misc.CSFD.CurrentSkin.getValue() == self['menu'].getCurrent()[0]:
			self['key_blue'].setText(_('Reset'))
		else:
			self['key_blue'].setText('')

	def paintPreview(self, image_path=''):
		try:
			self['preview'].instance.setPixmap(gPixmapPtr())
			ptr = ePicloadDecodeData( self.previewload, image_path )
			if ptr is not None:
				self['preview'].instance.setPixmap(ptr)
			else:
				LogCSFD.WriteToFile('[CSFD] SkinSelect - paintPreview - ptr nenalezeno: ' + Uni8(image_path) + '\n')
		except:
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Chyba v paintPreview\n')
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

		return

	def LoadSkins(self):
		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - zacatek\n')
		ar = ''
		self.resultlist = []
		index = 0
		sel_index = 0
		module = 'CSFDSkin_Default'
		LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu 1\n')
		try:
			exec('import %s.%s' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu 2\n')
			exec('reload(%s.%s)' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu 3\n')
			exec('from .%s.%s import *' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu 4\n')
			self.resultlist.append((ar + CSFD_SKIN_NAME, CSFD_SKIN_AUTHOR, CSFD_SKIN_AUTHOR_CONTACT, CSFD_SKIN_DESCRIPTION, CSFD_SKIN_PREVIEW))
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu OK\n')
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Reload Defaultniho skinu ERR\n')
			LogCSFD.WriteToFile(err)

		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - nacteni seznamu skinu - zacatek\n')
		for module in os_listdir(os_path.join(os_path.dirname(__file__), 'skins')):
			if module == '__init__.py' or module[-3:] != '.py' or module == 'CSFDSkin_Default.py' or module[0:9] != 'CSFDSkin_':
				continue
			module = module[:-3]
			LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload1 - %s\n' % module)
			try:
				exec('import %s.%s' % ('skins', module))
				LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload2 - %s\n' % module)
				exec('reload(%s.%s)' % ('skins', module))
				LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload3 - %s\n' % module)
				exec('from .%s.%s import *' % ('skins', module))
				LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload4 - %s\n' % module)
				if module == 'CSFDSkin_' + CSFD_SKIN_NAME:
					self.resultlist.append((ar + CSFD_SKIN_NAME, CSFD_SKIN_AUTHOR, CSFD_SKIN_AUTHOR_CONTACT, CSFD_SKIN_DESCRIPTION, CSFD_SKIN_PREVIEW))
					index += 1
					if module == 'CSFDSkin_' + config.misc.CSFD.CurrentSkin.getValue():
						sel_index = index
					LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload OK - %s\n' % module)
				else:
					LogCSFD.WriteToFile('[CSFD] SkinSelect - nekonzistence jmena skinu a nazvu souboru se skinem - ERR - %s\n' % module)
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] SkinSelect - import/reload ERR - %s\n' % module)
				LogCSFD.WriteToFile(err)

		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - nacteni seznamu skinu - konec\n')
		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - prenacteni zvoleneho skinu - zacatek\n')
		moduleload = False
		for module in os_listdir(os_path.join(os_path.dirname(__file__), 'skins')):
			if module == '__init__.py' or module[-3:] != '.py' or module[0:9] != 'CSFDSkin_':
				continue
			module = module[:-3]
			if module == 'CSFDSkin_' + config.misc.CSFD.CurrentSkin.getValue():
				LogCSFD.WriteToFile('[CSFD] SkinSelect - reload - %s\n' % module)
				try:
					exec('import %s.%s' % ('skins', module))
					LogCSFD.WriteToFile('[CSFD] SkinSelect - reload 1 - %s\n' % module)
					exec('reload(%s.%s)' % ('skins', module))
					LogCSFD.WriteToFile('[CSFD] SkinSelect - reload 2 - %s\n' % module)
					exec('from .%s.%s import *' % ('skins', module))
					LogCSFD.WriteToFile('[CSFD] SkinSelect - reload OK - %s\n' % module)
					moduleload = True
				except:
					err = traceback.format_exc()
					LogCSFD.WriteToFile('[CSFD] SkinSelect - reload ERR - %s\n' % module)
					LogCSFD.WriteToFile(err)

		if not moduleload:
			LogCSFD.WriteToFile('[CSFD] SkinSelect - Nebyl nacten skin podle parametru\n')
		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - prenacteni zvoleneho skinu - konec\n')
		self['menu'].l.setList(self.resultlist)
		self['menu'].moveToIndex(sel_index)
		LogCSFD.WriteToFile('[CSFD] SkinSelect - LoadSkins - konec\n')

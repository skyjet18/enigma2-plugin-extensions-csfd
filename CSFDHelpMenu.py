# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from .CSFDHelpMenuList import CSFDHelpMenuList
from .CSFDRc import CSFDRc
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import _
from .CSFDSettings2 import config
from .CSFDSkinLoader import *

class CSFDHelpMenu(Screen, CSFDRc):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDHelpMenuSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDHelpMenuHD
	else:
		skin = Screen_CSFDHelpMenuFullHD

	def __init__(self, session, listP):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDHelpMenuSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDHelpMenuHD
		else:
			self.skin = Screen_CSFDHelpMenuFullHD
		Screen.__init__(self, session)
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDHelpMenuSD', 'HelpMenu']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDHelpMenuHD', 'HelpMenu']
			else:
				self.skinName = [
				 'CSFDHelpMenuFullHD', 'HelpMenu']
		else:
			self.skinName = 'CSFDHelpMenu__'
		self.onSelChanged = []
		self.list = listP
		self.velx = 400
		self['list'] = CSFDHelpMenuList(self.list, self.close, self.velx)
		self['list'].onSelChanged.append(self.SelectionChanged)
		CSFDRc.__init__(self)
		self['long_key'] = Label('')
		self['actions'] = ActionMap(['WizardActions'], {'ok': self['list'].ok, 
		   'back': self.close}, -1)
		self.onLayoutFinish.append(self.LayoutFinished)

	def LayoutFinished(self):
		self.velx = self['list'].instance.size().width()
		self['list'].CreateNewList(self.velx)
		self['long_key'].setText(_('Long Keypress'))
		self['long_key'].hide()
		self.SelectionChanged()

	def SelectionChanged(self):
		self.clearSelectedKeys()
		selection = self['list'].getCurrent()
		if selection:
			selection = selection[3]
		self['long_key'].hide()
		if selection and len(selection) > 1:
			if selection[1] == 'SHIFT':
				self.selectKey('SHIFT')
			elif selection[1] == 'long':
				self['long_key'].show()
		if selection and len(selection) > 0:
			self.selectKey(selection[0])


class CSFDHelpableScreen:

	def __init__(self, session=None, aktListHelp=None):
		self.helpList = []
		self.aktListHelp = aktListHelp
		self.session = session
		self['helpActions'] = ActionMap(['HelpActions'], {'displayHelp': self.showHelp})

	def __setitem__(self, key, value):
		pass

	def setAttrHelp(self, session, aktListHelp):
		self.session = session
		self.aktListHelp = aktListHelp

	def showHelp(self):
		if self.aktListHelp != None:
			self.helpList = self.aktListHelp()
		self.session.openWithCallback(self.callHelpAction, CSFDHelpMenu, self.helpList)
		return

	def callHelpAction(self, *args):
		if args:
			actionmap, context, action = args
			actionmap.action(context, action)


class CSFDHelpableScreen1:

	def __init__(self):
		self['helpActions'] = ActionMap(['HelpActions'], {'displayHelp': self.showHelp})

	def showHelp(self):
		self.session.openWithCallback(self.callHelpAction, CSFDHelpMenu, self.helpList)

	def callHelpAction(self, *args):
		if args:
			actionmap, context, action = args
			actionmap.action(context, action)

# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from .CSFDSettings1 import CSFDGlobalVar

class CSFDNumericalTextInputHelpDialog(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogSD
		skin = Screen_CSFDNumericalTextInputHelpDialogSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogHD
		skin = Screen_CSFDNumericalTextInputHelpDialogHD
	else:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogFullHD
		skin = Screen_CSFDNumericalTextInputHelpDialogFullHD

	def __init__(self, session, textinput):
		from .CSFDSettings2 import config
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogSD
			self.skin = Screen_CSFDNumericalTextInputHelpDialogSD
		else:
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogHD
				self.skin = Screen_CSFDNumericalTextInputHelpDialogHD
			else:
				from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogFullHD
				self.skin = Screen_CSFDNumericalTextInputHelpDialogFullHD
			Screen.__init__(self, session)
			if config.misc.CSFD.Skinxml.getValue():
				if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogSD', 'CSFDNumericalTextInputHelpDialog']
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogHD', 'CSFDNumericalTextInputHelpDialog']
				else:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogFullHD', 'CSFDNumericalTextInputHelpDialog']
			else:
				self.skinName = 'CSFDNumericalTextInputHelpDialog__'
			self['help1'] = Label(text='<')
			self['help2'] = Label(text='>')
			for x in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0):
				self['key%d' % x] = Label(text=textinput.mapping[x].encode('utf-8'))

		self.last_marked = 0

	def update(self, textinput):
		if 0 <= self.last_marked <= 9:
			self[('key%d' % self.last_marked)].setMarkedPos(-1)
		if 0 <= textinput.lastKey <= 9:
			self[('key%d' % textinput.lastKey)].setMarkedPos(textinput.pos)
			self.last_marked = textinput.lastKey

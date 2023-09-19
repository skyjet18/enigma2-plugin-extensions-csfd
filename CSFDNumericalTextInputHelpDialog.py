# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.Label import Label
from .CSFDSettings1 import CSFDGlobalVar

try:
	unichr
	is_py2=True
except NameError:
	unichr = chr
	is_py2 = False

class CSFDNumericalTextInputHelpDialog(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogSD
		skin = Screen_CSFDNumericalTextInputHelpDialogSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogHD
		skin = Screen_CSFDNumericalTextInputHelpDialogHD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogFullHD
		skin = Screen_CSFDNumericalTextInputHelpDialogFullHD
	else:
		from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogWQHD
		skin = Screen_CSFDNumericalTextInputHelpDialogWQHD

	def __init__(self, session, textinput):
		from .CSFDSettings2 import config
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogSD
			self.skin = Screen_CSFDNumericalTextInputHelpDialogSD
		else:
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogHD
				self.skin = Screen_CSFDNumericalTextInputHelpDialogHD
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
				from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogFullHD
				self.skin = Screen_CSFDNumericalTextInputHelpDialogFullHD
			else:
				from .CSFDSkinLoader import Screen_CSFDNumericalTextInputHelpDialogWQHD
				self.skin = Screen_CSFDNumericalTextInputHelpDialogWQHD
			Screen.__init__(self, session)
			if config.misc.CSFD.Skinxml.getValue():
				if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogSD', 'CSFDNumericalTextInputHelpDialog']
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogHD', 'CSFDNumericalTextInputHelpDialog']
				elif CSFDGlobalVar.getCSFDDesktopWidth() < 2540:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogFullHD', 'CSFDNumericalTextInputHelpDialog']
				else:
					self.skinName = [
					 'CSFDNumericalTextInputHelpDialogWQHD', 'CSFDNumericalTextInputHelpDialog']
			else:
				self.skinName = 'CSFDNumericalTextInputHelpDialog__'
			self['help1'] = Label(text='<')
			self['help2'] = Label(text='>')
			for x in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0):
				if is_py2:
					self['key%d' % x] = Label(text=textinput.mapping[x].encode('utf-8'))
				else:
					self['key%d' % x] = Label(text=textinput.mapping[x])

		self.last_marked = 0

	def update(self, textinput):
		if 0 <= self.last_marked <= 9:
			self[('key%d' % self.last_marked)].setMarkedPos(-1)
		if 0 <= textinput.lastKey <= 9:
			self[('key%d' % textinput.lastKey)].setMarkedPos(textinput.pos)
			self.last_marked = textinput.lastKey

# -*- coding: utf-8 -*-

from Components.GUIComponent import GUIComponent
from enigma import eListboxPythonMultiContent, eListbox, gFont
try:
	from Tools.KeyBindings import getKeyDescription
except:
	from .CSFDKeyBindings import getKeyDescription

try:
	from Tools.KeyBindings import queryKeyBinding
except:
	from Components.ActionMap import queryKeyBinding
	
from .CSFDLog import LogCSFD
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import config

class CSFDHelpMenuList(GUIComponent):

	def __init__(self, helplist, callback, velx):
		GUIComponent.__init__(self)
		self.onSelChanged = []
		self.l = eListboxPythonMultiContent()
		self.callback = callback
		self.extendedHelp = False
		self.helplist = helplist
		self.velx = velx
		self.CreateNewList(self.velx)

	def CreateNewList(self, velx):
		self.velx = velx
		l = []
		for actionmap, context, actions in self.helplist:
			if not actionmap.enabled:
				continue
			for action, helpP in actions:
				buttons = queryKeyBinding(context, action)
				if not len(buttons):
					continue
				name = None
				flags = 0
				for n in buttons:
					name, flags = getKeyDescription(n[0]), n[1]
					if name is not None:
						break

				if flags & 8:
					name = (
					 name[0], 'long')
				entry = [(actionmap, context, action, name)]
				if isinstance(helpP, list):
					self.extendedHelp = True
					entry.extend((
					 (
					  eListboxPythonMultiContent.TYPE_TEXT, 0, 0, self.velx, 26, 0, 0, helpP[0]),
					 (
					  eListboxPythonMultiContent.TYPE_TEXT, 0, 28, self.velx, 20, 1, 0, helpP[1])))
				else:
					entry.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 0, self.velx, 28, 0, 0, helpP))
				l.append(entry)

		if CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			h = int(config.misc.CSFD.FontHeight.getValue())
		else:
			h = int(config.misc.CSFD.FontHeightFullHD.getValue())
		self.l.setList(l)
		try:
			if self.extendedHelp is True:
				self.l.setItemHeight(h + 30)
				if 'setFont' in dir(self.l):
					self.l.setFont(0, gFont('Regular', h))
					self.l.setFont(1, gFont('Regular', h - 4))
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDHelpMenuList - CreateNewList - 1 - nelze nastavit velikost fontu v seznamu (stara verze enigma2)\n')
			else:
				self.l.setItemHeight(h + 10)
				if 'setFont' in dir(self.l):
					self.l.setFont(0, gFont('Regular', h))
				else:
					LogCSFD.WriteToFile('[CSFD] CSFDHelpMenuList - CreateNewList - 2 - nelze nastavit velikost fontu v seznamu (stara verze enigma2)\n')
		except:
			LogCSFD.WriteToFile('[CSFD] CSFDHelpMenuList - chyba - CreateNewList - nelze nastavit velikost fontu v seznamu (stara verze enigma2)\n')

		return

	def ok(self):
		l = self.getCurrent()
		if l is None:
			return
		else:
			self.callback(l[0], l[1], l[2])
			return

	def getCurrent(self):
		sel = self.l.getCurrentSelection()
		return sel and sel[0]

	GUI_WIDGET = eListbox

	def postWidgetCreate(self, instance):
		instance.setContent(self.l)
		if 'connect' in dir(instance.selectionChanged):
			self.selectionChanged_conn = instance.selectionChanged.connect(self.selectionChanged)
		else:
			instance.selectionChanged.get().append(self.selectionChanged)

	def preWidgetRemove(self, instance):
		instance.setContent(None)
		if 'connect' in dir(instance.selectionChanged):
			self.selectionChanged_conn = None
		else:
			instance.selectionChanged.get().remove(self.selectionChanged)
		return

	def selectionChanged(self):
		for x in self.onSelChanged:
			x()

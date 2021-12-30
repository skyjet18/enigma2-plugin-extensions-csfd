# -*- coding: utf-8 -*-

from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
from enigma import eListboxPythonStringContent, eListbox

class CSFDMenuList(HTMLComponent, GUIComponent):

	def __init__(self, listP, enableWrapAround=False, content=eListboxPythonStringContent):
		GUIComponent.__init__(self)
		self.list = listP
		self.l = content()
		self.l.setList(self.list)
		self.onSelectionChanged = []
		self.enableWrapAround = enableWrapAround

	def getCurrent(self):
		return self.l.getCurrentSelection()

	GUI_WIDGET = eListbox

	def postWidgetCreate(self, instance):
		instance.setContent(self.l)
		if 'connect' in dir(instance.selectionChanged):
			self.selectionChanged_conn = instance.selectionChanged.connect(self.selectionChanged)
		else:
			instance.selectionChanged.get().append(self.selectionChanged)
		if self.enableWrapAround:
			self.instance.setWrapAround(True)

	def preWidgetRemove(self, instance):
		instance.setContent(None)
		if 'connect' in dir(instance.selectionChanged):
			self.selectionChanged_conn = None
		else:
			instance.selectionChanged.get().remove(self.selectionChanged)
		return

	def selectionChanged(self):
		for f in self.onSelectionChanged:
			f()

	def getSelectionIndex(self):
		return self.l.getCurrentSelectionIndex()

	def getSelectedIndex(self):
		return self.l.getCurrentSelectionIndex()

	def setList(self, listP):
		self.list = listP
		self.l.setList(self.list)

	def moveToIndex(self, idx):
		if self.instance is not None:
			self.instance.moveSelectionTo(idx)
		return

	def pageUp(self):
		if self.instance is not None:
			self.instance.moveSelection(self.instance.pageUp)
		return

	def pageDown(self):
		if self.instance is not None:
			self.instance.moveSelection(self.instance.pageDown)
		return

	def up(self):
		if self.instance is not None:
			self.instance.moveSelection(self.instance.moveUp)
		return

	def down(self):
		if self.instance is not None:
			self.instance.moveSelection(self.instance.moveDown)
		return

	def selectionEnabled(self, enabled):
		if self.instance is not None:
			self.instance.setSelectionEnable(enabled)
		return

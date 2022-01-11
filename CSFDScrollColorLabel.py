# -*- coding: utf-8 -*-

import skin
from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
from enigma import eLabel, eWidget, eSlider, fontRenderClass, ePoint, eSize, gRGB
from .CSFDLog import LogCSFD
from .CSFDSettings1 import CSFDGlobalVar

class CSFDScrollColorLabel(HTMLComponent, GUIComponent):

	def __init__(self, text=''):
		GUIComponent.__init__(self)
		self.message = text
		self.instance = None
		self.long_text = None
		self.long_textCol = None
		self.long_textHead = None
		self.long_textCalc = None
		self.scrollbar = None
		self.pages = None
		self.total = None
		self.SpaceSize = -1
		self.ASize = -1
		self.Correction = 0
		self.DefaultASize = 16
		self.DefaultSpaceSize = 7
		return

	def applySkin(self, desktop, parent):
		if self.skinAttributes is not None:
			text_attribs = []
			textCol_attribs = []
			textHead_attribs = []
			flagzPosition = False
			for attrib, value in self.skinAttributes:
				if attrib.find('zPosition') != -1:
					flagzPosition = True
					valueN = int(value)
					if CSFDGlobalVar.getCSFDEnigmaVersion() >= '4':
						if valueN < 1000:
							valueN = 1000
					text_attribs.append((attrib, str(valueN)))
					textCol_attribs.append((attrib, str(valueN + 1)))
					textHead_attribs.append((attrib, str(valueN + 2)))
				else:
					text_attribs.append((attrib, value))
					textCol_attribs.append((attrib, value))
					textHead_attribs.append((attrib, value))

			if not flagzPosition:
				attrib = 'zPosition'
				if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
					valueN = 0
				else:
					valueN = 1000
				text_attribs.append((attrib, str(valueN)))
				textCol_attribs.append((attrib, str(valueN + 1)))
				textHead_attribs.append((attrib, str(valueN + 2)))
			skin.applyAllAttributes(self.long_text, desktop, text_attribs, parent.scale)
			skin.applyAllAttributes(self.long_textCol, desktop, textCol_attribs, parent.scale)
			skin.applyAllAttributes(self.long_textHead, desktop, textHead_attribs, parent.scale)
			skin.applyAllAttributes(self.long_textCalc, desktop, text_attribs, parent.scale)
			widget_attribs = []
			scrollbar_attribs = []
			for attrib, value in self.skinAttributes:
				if attrib.find('borderColor') != -1 or attrib.find('borderWidth') != -1:
					scrollbar_attribs.append((attrib, value))
				if attrib.find('transparent') != -1 or attrib.find('backgroundColor') != -1:
					widget_attribs.append((attrib, value))

			skin.applyAllAttributes(self.instance, desktop, widget_attribs, parent.scale)
			skin.applyAllAttributes(self.scrollbar, desktop, scrollbar_attribs + widget_attribs, parent.scale)
		else:
			return False
		s = self.long_text.size()
		self.instance.move(self.long_text.position())
		self.instance.move(self.long_textCol.position())
		self.instance.move(self.long_textHead.position())
		self.instance.move(self.long_textCalc.position())
		lineheight = fontRenderClass.getInstance().getLineHeight(self.long_text.getFont())
		if not lineheight:
			lineheight = 30
		lines = int(s.height() / lineheight)
		self.pageHeight = int(lines * lineheight)
		self.rowHeight = int(lineheight)
		corr_pageHeight = -1
		self.instance.resize(eSize(s.width(), self.pageHeight + corr_pageHeight))
		if hasattr(self.scrollbar, 'updateScrollLabelProperties'):
			scrollbarwidth, scrollbarborderwidth = self.scrollbar.updateScrollLabelProperties(20, 1)
		else:
			scrollbarwidth = 20
			scrollbarborderwidth = 1
		self.scrollbar.move(ePoint(s.width() - scrollbarwidth, 0))
		self.scrollbar.resize(eSize(scrollbarwidth, self.pageHeight + corr_pageHeight))
		self.scrollbar.setOrientation(eSlider.orVertical)
		self.scrollbar.setRange(0, 100)
		self.scrollbar.setBorderWidth(scrollbarborderwidth)
		self.long_text.move(ePoint(0, 0))
		self.long_text.resize(eSize(s.width() - scrollbarwidth - 10, self.pageHeight * 2))
		self.long_textCol.move(ePoint(0, 0))
		self.long_textCol.resize(eSize(s.width() - scrollbarwidth - 10, self.pageHeight * 2))
		self.long_textHead.move(ePoint(0, 0))
		self.long_textHead.resize(eSize(s.width() - scrollbarwidth - 10, self.pageHeight * 2))
		self.long_textCalc.move(ePoint(0, 0))
		self.long_textCalc.resize(eSize(s.width() - scrollbarwidth - 10, self.pageHeight * 2))
		self.long_textCalc.hide()
		self.setText(self.message)
		self.SetSpace()
		self.SetCorrection()
		return True

	def SetSpace(self):
		self.long_textCalc.setText(' ')
		self.SpaceSize = self.long_textCalc.calculateSize().width()
		if self.SpaceSize <= 0:
			self.long_textCalc.setText('A A')
			size1 = self.long_textCalc.calculateSize().width()
			self.long_textCalc.setText('AA')
			size2 = self.long_textCalc.calculateSize().width()
			self.SpaceSize = size1 - size2
			if self.SpaceSize <= 0:
				self.SpaceSize = -1
		self.long_textCalc.setText('A')
		self.ASize = self.long_textCalc.calculateSize().width()
		if self.ASize <= 0:
			self.ASize = -1

	def setText(self, text):
		self.message = text
		numberOfRow = 0
		if self.long_text is not None and self.pageHeight:
			if text == '':
				self.setTextCol('')
				self.setTextHead('')
			self.long_text.move(ePoint(0, 0))
			self.long_textCol.move(ePoint(0, 0))
			self.long_textHead.move(ePoint(0, 0))
			self.long_text.setText(str(self.message))
			length = len(self.message)
			if length > 0:
				if self.message[(length - 1)] == '\n':
					self.long_textCalc.setText(str(self.message + 'A'))
				else:
					self.long_textCalc.setText(str(self.message + '\nA'))
			text_height = self.long_textCalc.calculateSize().height()
			if text_height < 0:
				text_height = 0
			numberOfRow, mm = divmod(text_height, self.rowHeight)
			if mm > 0:
				numberOfRow += 1
			total = self.pageHeight
			pages = 1
			while total < text_height:
				total += self.pageHeight
				pages += 1

			if pages > 1:
				s = self.long_textCalc.size()
				self.long_text.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textCol.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textHead.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textCalc.resize(eSize(s.width(), self.pageHeight * pages))
				self.scrollbar.show()
				self.total = total
				self.pages = pages
				self.updateScrollbar()
			else:
				self.scrollbar.hide()
				self.total = None
				self.pages = None
		return numberOfRow

	def setTextCol(self, text):
		if self.long_textCol is not None:
			self.long_textCol.setText(str(text))
		return

	def setTextHead(self, text):
		if self.long_textHead is not None:
			self.long_textHead.setText(str(text))
		return

	def appendText(self, text):
		old_text_height = self.long_text.calculateSize().height()
		if old_text_height < 0:
			old_text_height = 0
		text_height = old_text_height
		old_text = self.getText()
		if len(str(old_text)) > 0:
			self.message += text
		else:
			self.message = text
		if self.long_text is not None:
			self.long_text.setText(self.message)
			text_height = self.long_text.calculateSize().height()
			total = self.pageHeight
			pages = 1
			while total < text_height:
				total += self.pageHeight
				pages += 1

			if pages > 1:
				s = self.long_text.size()
				self.long_text.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textCol.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textHead.resize(eSize(s.width(), self.pageHeight * pages))
				self.long_textCalc.resize(eSize(s.width(), self.pageHeight * pages))
				self.scrollbar.show()
				self.total = total
				self.pages = pages
				self.updateScrollbar()
			else:
				self.scrollbar.hide()
				self.total = None
				self.pages = None
		if text_height < 0:
			text_height = 0
		vel = text_height - old_text_height
		numberOfRow, mm = divmod(vel, self.rowHeight)
		if mm > 0:
			numberOfRow += 1
		return numberOfRow

	def SetColColor(self, color_col):
		self.long_textCol.setForegroundColor(gRGB(color_col))

	def SetHeadColor(self, color_head):
		self.long_textHead.setForegroundColor(gRGB(color_head))

	def SetCorrection(self):
		text = 'A\nA\n'
		poc_radek1, velr1 = self.CalculateRowInText(text)
		if poc_radek1 > 2:
			self.Correction = -1
		else:
			self.Correction = 0

	def CalculateRowInText(self, text):
		length = len(text)
		if length > 0:
			text = text.replace(' \n', 'i\n')
			if text[(length - 1)] == '\n':
				self.long_textCalc.setText(str(text + 'A'))
			else:
				self.long_textCalc.setText(str(text + '\nA'))
		else:
			return (0, 0)
		text_height = self.long_textCalc.calculateSize().height()
		if text_height < 0:
			text_height = 0
		numberOfRow = divmod(text_height, self.rowHeight)[0]
		text_height -= self.rowHeight
		if text_height < 0:
			text_height = 0
			numberOfRow = 0
		return (
		 numberOfRow, text_height)

	def CalculateRowInSize(self, size):
		if size < 0:
			size = 0
		numberOfRow, mm = divmod(size, self.rowHeight)
		if mm > 0:
			numberOfRow += 1
		return numberOfRow

	def CalculateSizeInSpaceSimple(self, text):
		space = self.CalculateSizeInSpace(text)[0]
		return space

	def CalculateSizeInSpace(self, text):
		if self.ASize <= 0 or self.SpaceSize <= 0:
			self.SetSpace()
			if self.ASize <= 0:
				self.ASize = self.DefaultASize
			if self.SpaceSize <= 0:
				self.SpaceSize = self.DefaultSpaceSize
		self.long_textCalc.setText(str(text + 'A'))
		vel = self.long_textCalc.calculateSize().width() - self.ASize
		if vel < 0:
			vel = 0
		numberOfSpace, mm = divmod(vel, self.SpaceSize)
		if mm > 0:
			numberOfSpace += 1
		space = ''
		space = space.rjust(numberOfSpace, ' ')
		self.long_textCalc.setText(str(space + 'A'))
		newvel = self.long_textCalc.calculateSize().width() - self.ASize
		if newvel < 0:
			newvel = 0
		if vel > newvel:
			space += ' '
			numberOfSpace += 1
		return (space, numberOfSpace, vel)

	def CalculateSizeAddSpaceDiff(self, maintext, formattext):
		if self.ASize <= 0 or self.SpaceSize <= 0:
			self.SetSpace()
			if self.ASize <= 0:
				self.ASize = self.DefaultASize
			if self.SpaceSize <= 0:
				self.SpaceSize = self.DefaultSpaceSize
		self.long_textCalc.setText(str(maintext + 'A'))
		vel = self.long_textCalc.calculateSize().width() - self.ASize
		if vel < 0:
			vel = 0
		self.long_textCalc.setText(str(formattext + 'A'))
		vel1 = self.long_textCalc.calculateSize().width() - self.ASize
		if vel1 < 0:
			vel1 = 0
		rozdil = vel1 - vel
		if rozdil < 0:
			rozdil = 0
		numberOfSpace, mm = divmod(rozdil, self.SpaceSize)
		if mm > 0:
			numberOfSpace += 1
		space = ''
		space = space.rjust(numberOfSpace, ' ')
		space = maintext + space
		self.long_textCalc.setText(str(space + 'A'))
		newvel = self.long_textCalc.calculateSize().width() - self.ASize
		if newvel < 0:
			newvel = 0
		if vel1 > newvel:
			space += ' '
			numberOfSpace += 1
		return space

	def AddRowIntoText(self, textMain, textCol):
		poc_radek1, velr1 = self.CalculateRowInText(textMain)
		if textCol == '':
			poc_radek_roz = poc_radek1 + self.Correction
			textCol += ('').rjust(poc_radek_roz, '\n').replace('\n', ' \n')
		else:
			velr = self.CalculateRowInText(textCol)[1]
			poc_radek_roz = self.CalculateRowInSize(velr1 - velr)
			textCol += ('').rjust(poc_radek_roz, '\n').replace('\n', ' \n')
			poc_radek_f = self.CalculateRowInText(textCol)[0]
			if poc_radek_f < poc_radek1:
				textCol += ' \n'
			elif poc_radek_f > poc_radek1:
				if textCol[-2:] == ' \n':
					textCol = textCol[:-2]
				elif textCol[-1:] == '\n':
					textCol = textCol[:-1]
		return textCol

	def updateScrollbar(self):
		start = -self.long_text.position().y() * 100 / self.total
		vis = self.pageHeight * 100 / self.total
		self.scrollbar.setStartEnd(0, 0)
		self.scrollbar.setStartEnd(int(start), int(start + vis))

	def getText(self):
		return self.message

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.scrollbar = eSlider(self.instance)
		self.long_text = eLabel(self.instance)
		self.long_textCol = eLabel(self.instance)
		self.long_textHead = eLabel(self.instance)
		self.long_textCalc = eLabel(self.instance)

	def GUIdelete(self):
		self.long_textCalc = None
		self.long_textHead = None
		self.long_textCol = None
		self.long_text = None
		self.scrollbar = None
		self.instance = None
		return

	def pageUp(self):
		if self.total is not None:
			curPos = self.long_text.position()
			if curPos.y() < 0:
				poz = curPos.y() + self.pageHeight
				if poz > 0:
					poz = 0
				self.long_text.move(ePoint(curPos.x(), poz))
				self.long_textCol.move(ePoint(curPos.x(), poz))
				self.long_textHead.move(ePoint(curPos.x(), poz))
				self.updateScrollbar()
		return

	def pageDown(self):
		if self.total is not None:
			curPos = self.long_text.position()
			if self.total - self.pageHeight > abs(curPos.y()):
				poz = curPos.y() - self.pageHeight
				if self.total - self.pageHeight < abs(poz):
					poz = -1 * (self.total - self.pageHeight)
				self.long_text.move(ePoint(curPos.x(), poz))
				self.long_textCol.move(ePoint(curPos.x(), poz))
				self.long_textHead.move(ePoint(curPos.x(), poz))
				self.updateScrollbar()
		return

	def Up(self):
		if self.total is not None:
			curPos = self.long_text.position()
			if curPos.y() < 0:
				self.long_text.move(ePoint(curPos.x(), curPos.y() + self.rowHeight))
				self.long_textCol.move(ePoint(curPos.x(), curPos.y() + self.rowHeight))
				self.long_textHead.move(ePoint(curPos.x(), curPos.y() + self.rowHeight))
				self.updateScrollbar()
		return

	def Down(self):
		if self.total is not None:
			curPos = self.long_text.position()
			poz = curPos.y() - self.rowHeight
			if self.total - self.pageHeight >= abs(poz):
				self.long_text.move(ePoint(curPos.x(), poz))
				self.long_textCol.move(ePoint(curPos.x(), poz))
				self.long_textHead.move(ePoint(curPos.x(), poz))
				self.updateScrollbar()
		return

	def lastPage(self):
		i = 1
		while i < self.pages:
			self.pageDown()
			i += 1
			self.updateScrollbar()

	def produceHTML(self):
		return self.getText()


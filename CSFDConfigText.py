# -*- coding: utf-8 -*-

from enigma import eRCInput, getPrevAsciiCode
from .CSFDNumericalTextInput import CSFDNumericalTextInput
from .CSFDNumericalTextInputHelpDialog import CSFDNumericalTextInputHelpDialog
from Components.config import KEY_LEFT, KEY_RIGHT, KEY_HOME, KEY_END, KEY_DELETE, KEY_BACKSPACE, KEY_TOGGLEOW, KEY_ASCII, KEY_TIMEOUT, KEY_NUMBERS, getKeyNumber, ConfigElement
from .CSFDSettings1 import CSFDGlobalVar

try:
	unichr
except NameError:
	unichr = chr

class CSFDConfigText(ConfigElement, CSFDNumericalTextInput):

	def __init__(self, default='', fixed_size=True, visible_width=False):
		ConfigElement.__init__(self)
		CSFDNumericalTextInput.__init__(self, nextFunc=self.nextFunc, handleTimeout=False)
		self.marked_pos = 0
		self.allmarked = default != ''
		self.fixed_size = fixed_size
		self.visible_width = visible_width
		self.offset = 0
		self.overwrite = fixed_size
		self.help_window = None
		self.value = self.default = default
		self._keyboardMode = 0
		return

	def validateMarker(self):
		textlen = len(self.text)
		if self.fixed_size:
			if self.marked_pos > textlen - 1:
				self.marked_pos = textlen - 1
		elif self.marked_pos > textlen:
			self.marked_pos = textlen
		if self.marked_pos < 0:
			self.marked_pos = 0
		if self.visible_width:
			if self.marked_pos < self.offset:
				self.offset = self.marked_pos
			if self.marked_pos >= self.offset + self.visible_width:
				if self.marked_pos == textlen:
					self.offset = self.marked_pos - self.visible_width
				else:
					self.offset = self.marked_pos - self.visible_width + 1
			if self.offset > 0 and self.offset + self.visible_width > textlen:
				self.offset = max(0, textlen - self.visible_width)

	def insertChar(self, ch, pos, owr):
		if owr or self.overwrite:
			self.text = self.text[0:pos] + ch + self.text[pos + 1:]
		elif self.fixed_size:
			self.text = self.text[0:pos] + ch + self.text[pos:-1]
		else:
			self.text = self.text[0:pos] + ch + self.text[pos:]

	def deleteChar(self, pos):
		if not self.fixed_size:
			self.text = self.text[0:pos] + self.text[pos + 1:]
		elif self.overwrite:
			self.text = self.text[0:pos] + ' ' + self.text[pos + 1:]
		else:
			self.text = self.text[0:pos] + self.text[pos + 1:] + ' '

	def deleteAllChars(self):
		if self.fixed_size:
			self.text = ' ' * len(self.text)
		else:
			self.text = ''
		self.marked_pos = 0

	def handleKey(self, key):
		if key == KEY_DELETE:
			self.timeout()
			if self.allmarked:
				self.deleteAllChars()
				self.allmarked = False
			else:
				self.deleteChar(self.marked_pos)
				if self.fixed_size and self.overwrite:
					self.marked_pos += 1
		elif key == KEY_BACKSPACE:
			self.timeout()
			if self.allmarked:
				self.deleteAllChars()
				self.allmarked = False
			elif self.marked_pos > 0:
				self.deleteChar(self.marked_pos - 1)
				if not self.fixed_size and self.offset > 0:
					self.offset -= 1
				self.marked_pos -= 1
		elif key == KEY_LEFT:
			self.timeout()
			if self.allmarked:
				self.marked_pos = len(self.text)
				self.allmarked = False
			else:
				self.marked_pos -= 1
		elif key == KEY_RIGHT:
			self.timeout()
			if self.allmarked:
				self.marked_pos = 0
				self.allmarked = False
			else:
				self.marked_pos += 1
		elif key == KEY_HOME:
			self.timeout()
			self.allmarked = False
			self.marked_pos = 0
		elif key == KEY_END:
			self.timeout()
			self.allmarked = False
			self.marked_pos = len(self.text)
		elif key == KEY_TOGGLEOW:
			self.timeout()
			self.overwrite = not self.overwrite
		elif key == KEY_ASCII:
			self.timeout()
			newChar = unichr(getPrevAsciiCode())
			if not self.useableChars or newChar in self.useableChars:
				if self.allmarked:
					self.deleteAllChars()
					self.allmarked = False
				self.insertChar(newChar, self.marked_pos, False)
				self.marked_pos += 1
		elif key in KEY_NUMBERS:
			owr = self.lastKey == getKeyNumber(key)
			newChar = self.getKey(getKeyNumber(key))
			if self.allmarked:
				self.deleteAllChars()
				self.allmarked = False
			self.insertChar(newChar, self.marked_pos, owr)
		elif key == KEY_TIMEOUT:
			self.timeout()
			if self.help_window:
				self.help_window.update(self)
			return
		if self.help_window:
			self.help_window.update(self)
		self.validateMarker()
		self.changed()

	def nextFunc(self):
		self.marked_pos += 1
		self.validateMarker()
		self.changed()

	def getValue(self):
#		return self.text.encode('utf-8')
		return self.text

	def setValue(self, val):
		try:
			self.text = val.decode('utf-8')
		except AttributeError:
			self.text = str(val)
		except UnicodeDecodeError:
			self.text = val.decode('utf-8', 'ignore')
			print( 'Broken UTF8!' )

		self.changed()

	value = property(getValue, setValue)
	_value = property(getValue, setValue)

	def getText(self):
		return self.text.encode('utf-8')

	def getMulti(self, selected):
		if self.visible_width:
			if self.allmarked:
				mark = list(range(0, min(self.visible_width, len(self.text))))
			else:
				mark = [
				 self.marked_pos - self.offset]
			return ('mtext'[1 - selected:], self.text[self.offset:self.offset + self.visible_width].encode('utf-8') + ' ', mark)
		else:
			if self.allmarked:
				mark = list(range(0, len(self.text)))
			else:
				mark = [
				 self.marked_pos]
			return (
			 'mtext'[1 - selected:], self.text.encode('utf-8') + ' ', mark)

	def onSelect(self, session):
		self.allmarked = self.value != ''
		self._keyboardMode = eRCInput.getInstance().getKeyboardMode()
		eRCInput.getInstance().setKeyboardMode(eRCInput.kmAscii)
		if session is not None:
			if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
				self.help_window = session.instantiateDialog(CSFDNumericalTextInputHelpDialog, self)
			else:
				self.help_window = session.instantiateDialog(CSFDNumericalTextInputHelpDialog, self, zPosition=1000)
				self.help_window.setShowHideAnimation('simple_fade')
			self.help_window.show()
		return

	def onDeselect(self, session):
		eRCInput.getInstance().setKeyboardMode(self._keyboardMode)
		self.marked_pos = 0
		self.offset = 0
		if self.help_window:
			session.deleteDialog(self.help_window)
			self.help_window = None
		ConfigElement.onDeselect(self, session)
		return

	def getHTML(self, idP):
		return '<input type="text" name="' + idP + '" value="' + self.value + '" /><br>\n'

	def unsafeAssign(self, value):
		self.value = str(value)


class CSFDConfigPassword(CSFDConfigText):

	def __init__(self, default='', fixed_size=False, visible_width=False, censor='*'):
		CSFDConfigText.__init__(self, default=default, fixed_size=fixed_size, visible_width=visible_width)
		self.censor_char = censor
		self.hidden = True

	def getMulti(self, selected):
		mtext, text, mark = CSFDConfigText.getMulti(self, selected)
		if self.hidden:
			text = len(text) * self.censor_char
		return (
		 mtext, text, mark)

	def onSelect(self, session):
		CSFDConfigText.onSelect(self, session)
		self.hidden = False

	def onDeselect(self, session):
		CSFDConfigText.onDeselect(self, session)
		self.hidden = True

# -*- coding: utf-8 -*-

from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from .CSFDScrollColorLabel import CSFDScrollColorLabel
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDLog import LogCSFD
from .CSFDSkinLoader import *
from .compat import eConnectCallback

class CSFDConsole(Screen):
	if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
		skin = Screen_CSFDConsoleSD
	elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
		skin = Screen_CSFDConsoleHD
	else:
		skin = Screen_CSFDConsoleFullHD

	def __init__(self, session, title='CSFDConsole', cmdlist=None, finishedCallback=None, startCallback=None, closeOnSuccess=False, startText='', endText='', startNow=True):
		if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
			self.skin = Screen_CSFDConsoleSD
		elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
			self.skin = Screen_CSFDConsoleHD
		else:
			self.skin = Screen_CSFDConsoleFullHD
		Screen.__init__(self, session)
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - Init - zacatek\n')
		if config.misc.CSFD.Skinxml.getValue():
			if CSFDGlobalVar.getCSFDDesktopWidth() < 1250:
				self.skinName = [
				 'CSFDConsoleSD', 'CSFDConsole']
			elif CSFDGlobalVar.getCSFDDesktopWidth() < 1900:
				self.skinName = [
				 'CSFDConsoleHD', 'CSFDConsole']
			else:
				self.skinName = [
				 'CSFDConsoleFullHD', 'CSFDConsole']
		else:
			self.skinName = 'CSFDConsole__'
		self.finishedCallback = finishedCallback
		self.startCallback = startCallback
		self.closeOnSuccess = closeOnSuccess
		self.startNow = startNow
		self.container_output = ''
		self.container_output_all = ''
		self.textHead = ''
		self.textCol = ''
		self.retValue = 0
		self['text'] = CSFDScrollColorLabel('')
		if startText != '':
			self.startText = startText + '\n \n'
		else:
			self.startText = ''
		if endText != '':
			self.endText = endText + ' \n'
		else:
			self.endText = ''
		self['actions'] = ActionMap(['CSFDConsole'], {'ok': self.cancel, 
		   'back': self.cancel, 
		   'up': self['text'].Up, 
		   'down': self['text'].Down, 
		   'pageUp': self['text'].pageUp, 
		   'pageDown': self['text'].pageDown}, -1)
		self.cmdlist = cmdlist
		self.newtitle = title
		self.container = eConsoleAppContainer()
		self.run = 0
		self.dataAvail_conn = eConnectCallback( self.container.dataAvail, self.dataAvail )
		self.appClosed_conn = eConnectCallback( self.container.appClosed, self.runFinished )
		self.onLayoutFinish.append(self.layoutFinished)
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - Init - konec\n')
		return

	def layoutFinished(self):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - layoutFinished - zacatek\n')
		self.setTitle(self.newtitle)
		self['text'].setTextHead('')
		self['text'].setTextCol('')
		self['text'].setText('')
		self['text'].SetHeadColor(CSFDColor_Console_Titel)
		self['text'].SetColColor(CSFDColor_Console_Command)
		if self.startText != '':
			self.textHead = self.startText
			self['text'].setTextHead(self.textHead)
			self.container_output_all = self['text'].AddRowIntoText(self.textHead, '')
		if self.startCallback is not None:
			self.startCallback(self)
		if self.startNow:
			self.startRun()
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - layoutFinished - konec\n')
		return

	def startRun(self):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - startRun - zacatek\n')
		self.container_output = ''
		if self.cmdlist is not None and len(self.cmdlist) > 0:
			LogCSFD.WriteToFile('[CSFD] CSFDConsole - startRun - command: %s\n' % self.cmdlist[self.run])
			self.container_output += self.cmdlist[self.run] + '\n'
			self.textCol = self['text'].AddRowIntoText(self.container_output_all, self.textCol)
			self.textCol += self.cmdlist[self.run] + '\n'
			self.container_output_all = self['text'].AddRowIntoText(self.textCol, self.container_output_all)
			self['text'].setTextCol(self.textCol)
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
			if self.container.execute(self.cmdlist[self.run]):
				self.runFinished(-1)
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDConsole - startRun - neni co vykonavat\n')
			self.runFinished(0)
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - startRun - konec\n')
		return

	def addText(self, text='', typeText=0):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - addText - zacatek\n')
		if typeText == 0:
			self.container_output_all += text
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
		elif typeText == 1:
			self.textHead = self['text'].AddRowIntoText(self.container_output_all, self.textHead)
			self.textHead += text + '\n'
			self.container_output_all = self['text'].AddRowIntoText(self.textHead, self.container_output_all)
			self['text'].setTextHead(self.textHead)
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
		elif typeText == 2:
			self.textCol = self['text'].AddRowIntoText(self.container_output_all, self.textCol)
			self.textCol += text + '\n'
			self.container_output_all = self['text'].AddRowIntoText(self.textCol, self.container_output_all)
			self['text'].setTextCol(self.textCol)
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - addText - konec\n')

	def changeCmd(self, cmdlist=None):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - changeCmd - zacatek\n')
		self.cmdlist = cmdlist
		self.run = 0
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - changeCmd - konec\n')

	def setReturnValue(self, retval=None):
		if retval is not None:
			self.retValue = retval
		return

	def runFinished(self, retval):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - runFinished - zacatek\n')
		if self.cmdlist is not None and len(self.cmdlist) > 0:
			LogCSFD.WriteToFile('[CSFD] CSFDConsole - runFinished - command: %s\n' % self.cmdlist[self.run])
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - runFinished - retval: %s\n' % str(retval))
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - runFinished - container_output:\n')
		LogCSFD.WriteToFileWithoutTime(self.container_output)
		if retval is not None:
			if retval != 0:
				self.retValue = retval
			if self.cmdlist is not None and len(self.cmdlist) > 0:
				self.container_output_all += 'Returned value: ' + str(retval) + '\n'
		self.run += 1
		if self.cmdlist is not None and self.run < len(self.cmdlist):
			self.container_output = ''
			self.container_output += self.cmdlist[self.run] + '\n'
			self.container_output_all += ' \n'
			self.textCol = self['text'].AddRowIntoText(self.container_output_all, self.textCol)
			self.textCol += self.cmdlist[self.run] + '\n'
			self.container_output_all = self['text'].AddRowIntoText(self.textCol, self.container_output_all)
			self['text'].setTextCol(self.textCol)
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
			if self.container.execute(self.cmdlist[self.run]):
				self.runFinished(-1)
		else:
			self.container_output_all += ' \n'
			self.container_output_all += 'Final returned value: ' + str(self.retValue) + '\n'
			self.container_output_all += ' \n'
			self.textHead = self['text'].AddRowIntoText(self.container_output_all, self.textHead)
			self.textHead += self.endText
			self.container_output_all = self['text'].AddRowIntoText(self.textHead, self.container_output_all)
			self['text'].setTextHead(self.textHead)
			self['text'].setText(self.container_output_all)
			self['text'].lastPage()
			if self.finishedCallback is not None:
				self.finishedCallback(self)
			if self.retValue == 0 and self.closeOnSuccess:
				self.cancel()
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - runFinished - konec\n')
		return

	def cancel(self):
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - cancel - zacatek\n')
		if self.cmdlist is None or len(self.cmdlist) == 0 or self.run >= len(self.cmdlist):
			self.appClosed_conn = None
			self.dataAvail_conn = None
			LogCSFD.WriteToFile('[CSFD] CSFDConsole - cancel - done\n')
			LogCSFD.WriteToFile('[CSFD] CSFDConsole - cancel - konec\n')
			self.close(self.retValue)
		LogCSFD.WriteToFile('[CSFD] CSFDConsole - cancel - konec\n')
		return

	def dataAvail(self, string):
		self.container_output += string
		self.container_output_all += string
		self['text'].setText(self.container_output_all)
		self['text'].lastPage()

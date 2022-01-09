# -*- coding: utf-8 -*-

from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen
from Tools import ASCIItranslit
from Tools.Directories import fileExists
from CSFDLog import LogCSFD
from CSFDTools import downloadPage
from CSFDXmlMenu import sxml
from CSFDSettings1 import CSFDGlobalVar
from CSFDSettings2 import _
from enigma import ePicLoad, getDesktop
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape

class CSFDIconMenu(Screen):

	def __init__(self, session, feedtitle='Uvod', feedtext='CSFD'):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - Init - zacatek\n')
		size_w = getDesktop(0).size().width()
		size_h = getDesktop(0).size().height()
		if size_w == 1280:
			self.spaceTop = 75
			self.spaceLeft = 30
			self.textsize = 16
			self.spaceX = 45
			self.spaceY = self.textsize * 4 + 5
			self.picX = 118
			self.picY = 118
			size_w = 1100
			size_h = 613
		else:
			self.spaceTop = 75
			self.spaceLeft = 15
			self.textsize = 16
			self.spaceX = 45
			self.spaceY = self.textsize * 4 + 5
			self.picX = 118
			self.picY = 118
			size_w = 605
			size_h = 530
		self['titletext'] = StaticText(feedtitle)
		self['titlemessage'] = StaticText(feedtext)
		self['pageinfo'] = StaticText(_('Nacitam dalsi informace ...'))
		self.feedtitle = feedtitle
		self.feedtext = feedtext
		self.textcolor = '#F7F7F7'
		self.bgcolor = '#31000000'
		self.thumbsX = (size_w - self.spaceLeft) / (self.spaceX + self.picX)
		self.thumbsY = (size_h - self.spaceTop) / (self.spaceY + self.picY)
		self.thumbsC = self.thumbsX * self.thumbsY
		self.positionlist = []
		skincontent = ''
		posX = -1
		for x in range(self.thumbsC):
			posY = x / self.thumbsX
			posX += 1
			if posX >= self.thumbsX:
				posX = 0
			absX = self.spaceLeft + self.spaceX + posX * (self.spaceX + self.picX)
			absY = self.spaceTop + self.spaceY + posY * (self.spaceY + self.picY)
			self.positionlist.append((absX, absY))
			skincontent += '<widget source="label' + str(x) + '" render="Label" position="' + str(absX - 10) + ',' + str(absY + self.picY + 3) + '" size="' + str(self.picX + 20) + ',' + str(self.textsize * 3 + 10) + '" halign="center" valign="top" font="Regular;' + str(self.textsize) + '" zPosition="4" transparent="1" foregroundColor="' + self.textcolor + '" />'
			skincontent += '<widget name="thumb' + str(x) + '" position="' + str(absX) + ',' + str(absY) + '" size="' + str(self.picX) + ',' + str(self.picY) + '" zPosition="4" backgroundColor="black" alphatest="blend" />'

		self.skin = '<screen position="center,60" size="' + str(size_w) + ',' + str(size_h) + '" zPosition="10" backgroundColor="#31000000" title="CSFD Menu"> \t\t\t<widget source="titletext" transparent="1" render="Label" zPosition="2" valign="center" halign="center" position="10,10" size="' + str(size_w - 10) + ',30" font="Regular;26" backgroundColor="' + self.bgcolor + '" foregroundColor="' + self.textcolor + '" /> \t\t\t<widget source="titlemessage" transparent="1" render="Label" zPosition="2" valign="center" halign="center" position="10,40" size="' + str(size_w - 10) + ',25" font="Regular;18" foregroundColor="' + self.textcolor + '" /> \t\t\t<widget source="global.CurrentTime" render="Label" position="1000,20" zPosition="2" transparent="1" size="80,30" font="Regular;22" halign="right" foregroundColor="' + self.textcolor + '"> \t\t\t\t<convert type="ClockToText"></convert> \t\t\t</widget> \t\t\t<eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.bgcolor + '" /> \t\t\t<widget source="pageinfo" position="' + str(0) + ',' + str(size_h - 25) + '" transparent="1" render="Label" zPosition="2" valign="center" halign="center" size="' + str(size_w) + ',30" font="Regular;14" foregroundColor="' + self.textcolor + '" /> \t\t\t<widget name="frame" position="' + str(size_w) + ',' + str(size_h) + '" size="118,118" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/CSFDMenu_Frame.png" backgroundColor="black" zPosition="5" alphatest="blend" />' + skincontent + '</screen>'
		Screen.__init__(self, session)
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'DirectionActions', 'MovieSelectionActions'], {'cancel': self.Exit, 
		   'ok': self.key_ok, 
		   'left': self.key_left, 
		   'right': self.key_right, 
		   'up': self.key_up, 
		   'down': self.key_down}, -1)
		self.maxPage = 0
		self.maxentry = 1
		self.index = 0
		self.itemlist = False
		self['frame'] = MovingPixmap()
		for x in range(self.thumbsC):
			self['label' + str(x)] = StaticText()
			self['thumb' + str(x)] = Pixmap()

		sc = AVSwitch().getFramebufferScale()
		self.picload = ePicLoad()
		if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
			self.picload.PictureData.get().append(self.showThumbPixmap)
		else:
			self.picloadConn = self.picload.PictureData.connect(self.showThumbPixmap)
		self.picload.setPara((self.picX, self.picY, sc[0], sc[1], True, 0, '#31000000'))
		self.onLayoutFinish.append(self.layoutFinished)
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - Init - konec\n')

	def layoutFinished(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - layoutFinished - zacatek\n')
		self.gotxmlfeed(sxml)
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - layoutFinished - konec\n')

	def gotxmlfeed(self, page=''):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - gotxmlfeed - zacatek\n')
		self['pageinfo'].setText(_('Parsing XML Feeds ...'))
		xml = parseString(page)
		index = 0
		framePos = 0
		Page = 0
		self.Thumbnaillist = []
		self.itemlist = []
		self.currPage = -1
		self.maxPage = 0
		for node in xml.getElementsByTagName('ITEM'):
			typeP = str(node.getElementsByTagName('TYPE')[0].childNodes[0].data)
			name = unescape(str(node.getElementsByTagName('NAME')[0].childNodes[0].data))
			imgurl = str(node.getElementsByTagName('IMGURL')[0].childNodes[0].data)
			self.itemlist.append((index, framePos, Page, name, imgurl, typeP, 'item'))
			index += 1
			framePos += 1
			if framePos == 1:
				self.maxPage += 1
			elif framePos > self.thumbsC - 1:
				framePos = 0
				Page += 1

		self.maxentry = len(self.itemlist) - 1
		self['pageinfo'].setText('')
		self.paintFrame()
		self['frame'].show()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - gotxmlfeed - konec\n')

	def getThumbnail(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - getThumbnail - zacatek\n')
		self.thumbcount += 1
		self.thumburl = self.Thumbnaillist[self.thumbcount][2]
		if self.thumburl.startswith('http'):
			self.thumbfile = '/tmp/' + str(self.Thumbnaillist[self.thumbcount][3])
		else:
			self.thumbfile = str(self.Thumbnaillist[self.thumbcount][3])
		if fileExists(self.thumbfile, 'r'):
			self.gotThumbnail()
		else:
			UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0'
			downloadPage(self.thumburl, self.thumbfile, agent=UA).addCallback(self.gotThumbnail).addErrback(self.showThumbError)
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - getThumbnail - konec\n')

	def gotThumbnail(self, data=''):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - gotThumbnail - zacatek\n')
		imagescaler = '0'
		if imagescaler == '0':
			self.picload.startDecode(self.thumbfile)
		elif self.picload.getThumbnail(self.thumbfile) == 1:
			if self.thumbcount + 1 < len(self.Thumbnaillist):
				self.getThumbnail()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - gotThumbnail - konec\n')

	def showThumbPixmap(self, picInfo=None):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - showThumbPixmap - zacatek\n')
		ptr = self.picload.getData()
		if ptr != None:
			self[('thumb' + str(self.thumbcount))].instance.setPixmap(ptr)
			self[('thumb' + str(self.thumbcount))].show()
		if self.thumbcount + 1 < len(self.Thumbnaillist):
			self.getThumbnail()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - showThumbPixmap - konec\n')
		return

	def showThumbError(self, error):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - showThumbPixmap - zacatek\n')
		if self.thumbcount + 1 < self.thumbsC:
			self.getThumbnail()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - showThumbPixmap - konec\n')

	def paintFrame(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - paintFrame - zacatek\n')
		if self.maxentry < self.index or self.index < 0 or not self.itemlist:
			LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - paintFrame - konec\n')
			return
		pos = self.positionlist[self.itemlist[self.index][1]]
		self['frame'].moveTo(pos[0], pos[1], 1)
		self['frame'].startMoving()
		if self.currPage != self.itemlist[self.index][2]:
			self.currPage = self.itemlist[self.index][2]
			self.newPage()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - paintFrame - konec\n')

	def newPage(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - newPage - zacatek\n')
		self.Thumbnaillist = []
		if self.maxPage > 1:
			self['pageinfo'].setText(_('Page ') + str(self.currPage + 1) + _(' of ') + str(self.maxPage))
		else:
			self['pageinfo'].setText('')
		for x in range(self.thumbsC):
			self[('label' + str(x))].setText('')
			self[('thumb' + str(x))].hide()

		for x in self.itemlist:
			if x[2] == self.currPage:
				print( 'newPage: ' + x[1] )
				self[('label' + str(x[1]))].setText(x[3])
				if x[4].startswith('http'):
					self[('thumb' + str(x[1]))].instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/CSFDMenu_empty.png')
					self.Thumbnaillist.append([0, x[1], x[4], ASCIItranslit.legacyEncode(x[3] + '.' + x[4].split('.')[(-1)]).lower()])
					self[('thumb' + str(x[1]))].show()
				else:
					self[('thumb' + str(x[1]))].instance.setPixmapFromFile(x[4])
					self.Thumbnaillist.append([0, x[1], x[4], x[4]])

		self.thumbcount = -1
		self.getThumbnail()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - newPage - konec\n')

	def key_left(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_left - zacatek\n')
		self.index -= 1
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_left - konec\n')

	def key_right(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_right - zacatek\n')
		self.index += 1
		if self.index > self.maxentry:
			self.index = 0
		self.paintFrame()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_right - konec\n')

	def key_up(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_up - zacatek\n')
		self.index -= self.thumbsX
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_up - konec\n')

	def key_down(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_down - zacatek\n')
		self.index += self.thumbsX
		if self.index - self.thumbsX == self.maxentry:
			self.index = 0
		elif self.index > self.maxentry:
			self.index = self.maxentry
		self.paintFrame()
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_down - konec\n')

	def key_ok(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_ok - zacatek\n')
		if not self.itemlist:
			return
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - key_ok - konec\n')

	def Exit(self):
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - Exit - zacatek\n')
		del self.picload
		LogCSFD.WriteToFile('[CSFD] CSFDIconMenu - Exit - konec\n')
		self.close()

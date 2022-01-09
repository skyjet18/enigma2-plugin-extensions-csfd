# -*- coding: utf-8 -*-

from Components.Pixmap import MovingPixmap, MultiPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from xml.etree.ElementTree import ElementTree
from Components.config import config, ConfigInteger
from time import sleep
config.misc.rcused = ConfigInteger(default=1)

class CSFDRc:

	def __init__(self):
		self['rc'] = MultiPixmap()
		self['arrowdown'] = MovingPixmap()
		self['arrowdown2'] = MovingPixmap()
		self['arrowup'] = MovingPixmap()
		self['arrowup2'] = MovingPixmap()
		config.misc.rcused = ConfigInteger(default=1)
		self.vel_rc = 154
		self.rcheight = 500
		self.rcheighthalf = 250
		self.selectpics = []
		self.selectpics.append((self.rcheighthalf, ['arrowdown', 'arrowdown2'], (-18, -70)))
		self.selectpics.append((self.rcheight, ['arrowup', 'arrowup2'], (-18, 0)))
		self.onLayoutFinish.append(self.layoutFinished)
		self.onShown.append(self.initRc)

	def layoutFinished(self):
		self['arrowdown'].hide()
		self['arrowdown2'].hide()
		self['arrowup'].hide()
		self['arrowup2'].hide()
		self.vel_rc = self['rc'].instance.size().width()
		if self.vel_rc > 200:
			self.rcheight = 750
			self.rcheighthalf = 375
			self.selectpics = []
			self.selectpics.append((self.rcheighthalf, ['arrowdown', 'arrowdown2'], (-18, -70)))
			self.selectpics.append((self.rcheight, ['arrowup', 'arrowup2'], (-18, 0)))
		self.readPositions()
		self.clearSelectedKeys()

	def initRc(self):
		self['rc'].setPixmapNum(config.misc.rcused.value)

	def readPositions(self):
		tree = ElementTree(file=resolveFilename(SCOPE_PLUGINS, 'Extensions/CSFD/rcpositions.xml'))
		rcs = tree.getroot()
		self.rcs = {}
		for rc in rcs:
			id = int(rc.attrib['id'])
			self.rcs[id] = {}
			for key in rc:
				name = key.attrib['name']
				pos = key.attrib['pos'].split(',')
				if self.vel_rc > 200:
					self.rcs[id][name] = (
					 int(round(float(pos[0]) * 1.5, 0)), int(round(float(pos[1]) * 1.5, 0)))
				else:
					self.rcs[id][name] = (
					 int(pos[0]), int(pos[1]))

	def getSelectPic(self, pos):
		for selectPic in self.selectpics:
			if pos[1] <= selectPic[0]:
				return (selectPic[1], selectPic[2])

		return

	def hideRc(self):
		self.hideSelectPics()
		self['rc'].hide()

	def showRc(self):
		self['rc'].show()

	def selectKey(self, key):
		rc = self.rcs[config.misc.rcused.value]
		if key in rc:
			rcpos = self['rc'].getPosition()
			pos = rc[key]
			selectPics = self.getSelectPic(pos)
			selectPic = None
			for x in selectPics[0]:
				if x not in self.selectedKeys:
					selectPic = x
					break

			if selectPic is not None:
				self[selectPic].hide()
				self[selectPic].moveTo(rcpos[0] + pos[0] + selectPics[1][0], rcpos[1] + pos[1] + selectPics[1][1], 1)
				self[selectPic].startMoving()
				sleep(0.1)
				self[selectPic].show()
				self.selectedKeys.append(selectPic)
		return

	def clearSelectedKeys(self):
		self.showRc()
		self.selectedKeys = []
		self.hideSelectPics()

	def hideSelectPics(self):
		for selectPic in self.selectpics:
			for pic in selectPic[1]:
				self[pic].hide()

# -*- coding: utf-8 -*-

from CSFDLog import LogCSFD
import time

class CSFDCache:

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDCache - init - zacatek\n')
		self.cacheMovieScore = {}
		LogCSFD.WriteToFile('[CSFD] CSFDCache - init - konec\n')

	def fullResetCache(self):
		LogCSFD.WriteToFile('[CSFD] CSFDCache - fullResetCache - zacatek\n')
		self.cacheMovieScore = {}
		LogCSFD.WriteToFile('[CSFD] CSFDCache - fullResetCache - konec\n')

	def deleteOldItemsFromCache(self):
		LogCSFD.WriteToFile('[CSFD] CSFDCache - deleteOldItemsFromCache - zacatek\n')
		tmpDict = self.cacheMovieScore.copy()
		for key, value in tmpDict.iteritems():
			now = int(time.time())
			if now - value[2] > 43200:
				del self.cacheMovieScore[key]

		LogCSFD.WriteToFile('[CSFD] CSFDCache - deleteOldItemsFromCache - konec\n')

	def addMovieNamesToScoreCache(self, movienames, score, shoda100):
		now = int(time.time())
		self.cacheMovieScore[movienames] = (score, shoda100, now)

	def getScoreForMovieNamesFromCache(self, movienames):
		score, shoda100, tm = self.cacheMovieScore[movienames]
		return (
		 score, shoda100)

	def AreMovieNamesInScoreCache(self, movienames):
		if self.cacheMovieScore.has_key(movienames):
			return True
		else:
			return False

	def delMovieNameFromScoreCache(self, movienames):
		if self.cacheMovieScore.has_key(movienames):
			del self.cacheMovieScore[movienames]


movieCSFDCache = CSFDCache()

# -*- coding: utf-8 -*-

from .CSFDLog import LogCSFD
from datetime import datetime, timedelta

class CSFDMovieCache:

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - init - zacatek\n')
		self.cacheMovieList = {}
		self.cacheMovieListValidity = {}
		self.ValidityHours = 12
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - init - konec\n')

	def addMovieToCache(self, channel, Movielist):
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - addMovieToCache - zacatek\n')
		if channel is not None and channel != '':
			self.cacheMovieList[channel] = Movielist
			self.cacheMovieListValidity[channel] = datetime.now() + timedelta(hours=self.ValidityHours)
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - addMovieToCache - konec\n')
		return

	def getMoviesFromCache(self, channel):
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - getMoviesFromCache - zacatek\n')
		if channel in self.cacheMovieList and channel in self.cacheMovieListValidity:
			if self.cacheMovieListValidity[channel] > datetime.now():
				Movielist = self.cacheMovieList[channel]
				if Movielist is not None and len(Movielist) > 0:
					LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - getMoviesFromCache - OK\n')
					LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - getMoviesFromCache - konec\n')
					return Movielist
				LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - getMoviesFromCache - konec\n')
				return
			else:
				self.delChannelFromMovieCache(channel)
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - getMoviesFromCache - konec\n')
		return

	def IsChannelInCache(self, channel):
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - IsChannelInCache - zacatek\n')
		if channel in self.cacheMovieList and channel in self.cacheMovieListValidity:
			if self.cacheMovieListValidity[channel] > datetime.now():
				LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - IsChannelInCache - True\n')
				LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - IsChannelInCache - konec\n')
				return True
			self.delChannelFromMovieCache(channel)
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - IsChannelInCache - False\n')
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - IsChannelInCache - konec\n')
		return False

	def delChannelFromMovieCache(self, channel):
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - delChannelFromMovieCache - zacatek\n')
		if channel is not None and channel != '':
			if channel in self.cacheMovieList:
				del self.cacheMovieList[channel]
			if channel in self.cacheMovieListValidity:
				del self.cacheMovieListValidity[channel]
		LogCSFD.WriteToFile('[CSFD] CSFDMovieCache - delChannelFromMovieCache - konec\n')
		return


TVMovieCache = CSFDMovieCache()

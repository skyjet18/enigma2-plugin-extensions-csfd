# -*- coding: utf-8 -*-

from .CSFDLog import LogCSFD
from .CSFDTools import char2Allowchar, strUni, ExtractNumbers, isBigCharInFirst, char2Diacritic
from .CSFDSettings1 import CSFDGlobalVar
from datetime import datetime
import re, traceback

from .CSFDAndroidClient import csfdAndroidClient

try:
	# py2
	from .htmlentitydefs import name2codepoint
except:
	# py3
	from html.entities import name2codepoint
	unichr = chr
	unicode = str
	
zlib_exist = True
try:
	import zlib
except:
	zlib_exist = False
	err = traceback.format_exc()
	LogCSFD.WriteToFile('[CSFD] CSFDParser - ERR - neexistuje zlib knihovna nutna pro dekompresi dat do html - chyba\n')
	LogCSFD.WriteToFile(err)

correction_const02a = [
 ' pt1', ' part 1', ' part1', ' pt2', ' part 2', ' part2', ' pt3', ' part 3', ' part3']
correction_const02b = [', Pro pamětníky...', ', Pro pamětníky', ' Pro pamětníky', ' 1 část', ' 1. část', ' 1.část', ' 2 část', ' 2. část', ' 2.část', ' 3 část', ' 3. část', ' 3.část', ' část', ' díl']
correction_const02c = [', Pre pamätníkov...', ', Pre pamätníkov', ' Pre pamätníkov', ' 1 časť', ' 1. časť', ' 1.časť', ' 2 časť', ' 2. časť', ' 2.časť', ' 3 časť', ' 3. časť', ' 3.časť', ' časť', ' diel']
correction_const02d = [' ST W', ' W ST', ' -ST -W', ' -W -ST', ' -W', ' W', ' -ST', ' ST', ' (HD)', ' -HD', ' HD', ' -AD', ' AD', ' -CB', ' CB', " '60'", ' "60"']
correction_const03 = [('Letné kino na Dvojke: ', ''), ('FILM NA PŘÁNÍ: ', ''), ('.', ' '), ('_', ' '), ('-', ' '), ('*', ' '), ('DVDRip', ''), ('dvdrip', ''), ('dvd', ''), ('divx', ''), ('xvid', ''), ('hdtv', ''), ('HDTV', ''), ('1080p', ''), ('720p', ''), ('560p', ''), ('480p', ''), ('x264', ''), ('h264', ''), ('1080i', ''), ('AC3', ''), ('ac3', ''), ('...', ' '), ('	 ', ' '), ('  ', ' ')]
correction_const04 = ['The', 'Der', 'Die', 'Das', 'Le', 'La']
correction_const05 = ['A', 'The', 'Der', 'Die', 'Das', 'Le', 'La']
correction_const10 = [(',', ' '), (';', ' '), (':', ' '), ('-', ' '), ('"', ' '), ("'", ' '), ('(', ' '), (')', ' '), ('\\[', ' '), ('\\]', ' '), ('.', ' '), ('?', ' '), ('!', ' '), ('&', ' '), ('	  ', ' '), ('  ', ' ')]

typeOfMovie = {
	'video film': _('Video film'),
	'film': _('TV film'),
	'seriál': _('TV seriál'),
	'pořad': _('TV pořad'),
	'divadelní záznam': _('Divadelní záznam'),
	'koncert': _('Koncert'),
	'studentský film': _('Studentský film'),
	'amatérský film': _('Amatérský film'),
	'hudební videoklip': _('Hudební videoklip'),
	'série': _('Seriál - série'),
	'epizoda': _('Seriál - epizoda')
}

try:
	import unidecode
	
	def strip_accents(s):
		return unidecode.unidecode(s)
except:
	import unicodedata
	
	def strip_accents(s):
		try:
			# py2
			s = s.decode('utf-8')
		except:
			pass
		return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def channel_name_normalise( name ):
	name = strip_accents( name ).lower()

	name = name.replace("television", "tv")
	name = name.replace("(bonus)", "").strip()
	name = name.replace("eins", "1")
	
	if name.endswith(" hd"):
		name = name[:name.rfind(" hd")]

	if name.endswith(" tv"):
		name = name[:name.rfind(" tv")]
	
	if name.startswith("tv "):
		name = name[3:]

	if name.endswith(" channel"):
		name = name[:name.rfind(" channel")]

	name = name.replace("&", " and ").replace("'", "").replace(".", "").replace(" ", "")
	return name

tv_stations = {}

def load_tv_stations():
	LogCSFD.WriteToFile('[CSFD] load_tv_stations - zacatek\n')
	
	if csfdAndroidClient.is_logged():
		global tv_stations
		
		tv_stations = {}
		stations = csfdAndroidClient.get_tv_stations()
		if 'http_error' in stations or 'internal_error' in stations:
			LogCSFD.WriteToFile('[CSFD] load_tv_stations - chyba\n')
		else:
			LogCSFD.WriteToFile('[CSFD] load_tv_stations - nacteno %d stanic\n' % len( stations['stations']))
			
			for station in stations['stations']:
				tv_stations[ channel_name_normalise( station['name']) ] = str(station['id'])
			
	LogCSFD.WriteToFile('[CSFD] load_tv_stations - konec\n')
	
def GetCSFDNumberFromChannel(nameChannel=''):
	LogCSFD.WriteToFile('[CSFD] GetCSFDNumberFromChannel - zacatek\n')
	results = []
	global tv_stations
	
	if len(tv_stations) == 0:
		load_tv_stations()
	
	name = channel_name_normalise( nameChannel )
	LogCSFD.WriteToFile('[CSFD] GetCSFDNumberFromChannel - normalised name: %s\n' % name)

	try:
		results.append( tv_stations[name] )
		LogCSFD.WriteToFile('[CSFD] GetCSFDNumberFromChannel - found\n')
	except:
		pass

	LogCSFD.WriteToFile('[CSFD] GetCSFDNumberFromChannel - konec\n')
	
	return results

def GetItemColourRateN(rate=-1):
	if rate >= 70:
		typn = 1
	elif rate >= 30:
		typn = 2
	elif rate >= 0:
		typn = 3
	else:
		typn = 0
	return typn


def GetItemColourRateC(rate=-1):
	if rate >= 70:
		typc = 'c1'
	elif rate >= 30:
		typc = 'c2'
	elif rate >= 0:
		typc = 'c3'
	else:
		typc = 'c0'
	return typc


def GetItemColourN(typ=''):
	if typ == 'c0':
		typn = 0
	elif typ == 'c1':
		typn = 1
	elif typ == 'c2':
		typn = 2
	elif typ == 'c3':
		typn = 3
	else:
		typn = 0
	return typn


def NameMovieCorrectionsForCTChannels(name_s):
	name1 = name_s
	name2 = name_s
	rozdel = name_s.split(',')
	poc = 0
	for slovo in rozdel:
		poc += 1
		if poc == 1:
			name1 = slovo
		elif isBigCharInFirst(slovo.strip()):
			break
		else:
			name1 += ',' + slovo

	poc = 0
	poc_big = 0
	for slovo in rozdel:
		poc += 1
		if poc == 1:
			name2 = slovo
		elif isBigCharInFirst(slovo.strip()):
			poc_big += 1
			if poc_big >= 2:
				break
			else:
				name2 += ',' + slovo
		else:
			name2 += ',' + slovo

	return (
	 name1, name2)


def NameMovieCorrections(name_s):

	def corr1(name1):
		pos = name1.rfind(' (')
		if pos > 0 and name1[-1:] == ')':
			name1 = name1[0:pos].strip()
		pos = name1.rfind(' [')
		if pos > 0 and name1[-1:] == ']':
			name1 = name1[0:pos].strip()
		return name1

	def corr2a(name1):
		zmena = False
		for dodat in correction_const02a:
			vv = -1 * len(dodat)
			if name1[vv:] == dodat:
				name1 = name1[:vv].strip()
				zmena = True

		if zmena:
			name1 = corr2a(name1)
		return name1

	def corr2b(name1):
		zmena = False
		for dodat in correction_const02b:
			vv = -1 * len(dodat)
			if name1[vv:] == dodat:
				name1 = name1[:vv].strip()
				zmena = True

		if zmena:
			name1 = corr2b(name1)
		return name1

	def corr2c(name1):
		zmena = False
		for dodat in correction_const02c:
			vv = -1 * len(dodat)
			if name1[vv:] == dodat:
				name1 = name1[:vv].strip()
				zmena = True

		if zmena:
			name1 = corr2c(name1)
		return name1

	def corr2d(name1):
		zmena = False
		for dodat in correction_const02d:
			vv = -1 * len(dodat)
			if name1[vv:].upper() == dodat:
				name1 = name1[:vv].strip()
				zmena = True

		if zmena:
			name1 = corr2d(name1)
		return name1

	def corr3(name1):
		name1 = re.sub('\\[.*\\]', '', name1)
		for phrase, sub in correction_const03:
			name1 = name1.replace(phrase, sub).strip()

		return name1

	def corr4(name1):
		for article in correction_const04:
			vel = len(article) + 1
			if name1[:vel] == article + ' ':
				name1 = name1[vel:] + ', ' + article

		return name1

	name_s = corr1(name_s)
	name_s = corr2a(name_s)
	name_s = corr2b(name_s)
	name_s = corr2c(name_s)
	name_s = corr2d(name_s)
	name_s = corr3(name_s)
	name_s = corr1(name_s)
	name_s = corr2a(name_s)
	name_s = corr2b(name_s)
	name_s = corr2c(name_s)
	name_s = corr2d(name_s)
	name_s = corr3(name_s)
	name_s = corr4(name_s).replace('  ', ' ')
	return name_s


def NameMovieCorrectionsForCompare(name_s):
	for phrase, sub in correction_const10:
		name_s = name_s.replace(phrase, sub).strip()

	return name_s


def NameMovieCorrectionExtensions(name1=''):
	for artic in correction_const05:
		article = ', ' + artic
		vel = -1 * len(article)
		if name1[vel:] == article:
			name1 = artic + ' ' + name1[:vel].strip()

	return name1


class CSFDConstParser():

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDConstParser - init - zacatek\n')
		self.ccFindCond = re.DOTALL | re.IGNORECASE
		self.parserhtmltags = re.compile('<.*?>')
		self.parserYear = re.compile('19\\d{2}|20\\d{2}|21\\d{2}', re.DOTALL)
		self.parserYear2 = re.compile('\(19\\d{2}\)|\(20\\d{2}\)', re.DOTALL)
		self.parserDate = re.compile('\\d{2}\\.\\d{2}\\.\\d{4}', re.DOTALL)
		self.parserNumbers = re.compile(' \\d+', re.DOTALL)
		self.parserRomanNumerals = re.compile('\\b(?!LLC)(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.DOTALL)

		LogCSFD.WriteToFile('[CSFD] CSFDConstParser - init - konec\n')

	def parserGetRomanNumbers(self, name):
		searchresults = []
		results = self.parserRomanNumerals.findall(name)
		if results is not None:
			for value in results:
				vysl = value[0] + value[1] + value[2]
				searchresults.append(vysl)

		return searchresults

	def parserGetNumbers(self, name):
		searchresults = []
		results = self.parserNumbers.findall(name)
		if results is not None:
			for value in results:
				searchresults.append(value.strip())

		return searchresults

	def parserGetYears(self, name):
		LogCSFD.WriteToFile('[CSFD] parserGetYears - zacatek\n')
		searchresults = []
		results = self.parserYear2.findall(name)
		if results is not None:
			for value in results:
				LogCSFD.WriteToFile('[CSFD] parserGetYears - have year2 %s\n' % value[1:-1])
				searchresults.append(value[1:-1])
		else:
			results = self.parserYear.findall(name)
			if results is not None:
				for value in results:
					LogCSFD.WriteToFile('[CSFD] parserGetYears - have year %s\n' % value)
					searchresults.append(value)

		LogCSFD.WriteToFile('[CSFD] parserGetYears - konec\n')
		return list(set(searchresults))

	def delHTMLtags(self, string):
		return self.parserhtmltags.sub('', string)


ParserConstCSFD = CSFDConstParser()

class CSFDParser():

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - zacatek\n')
		self.inhtml = ''
		self.inhtml_script = ''
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - konec\n')


	def parserMoviesFound(self):
		LogCSFD.WriteToFile('[CSFD] parserMoviesFound - zacatek\n')
		res = False
		
		if len(self.json_data["films"]) > 0:
			res = True
		
		LogCSFD.WriteToFile('[CSFD] parserMoviesFound - False - konec\n')
		return res

	def parserListOfMovies(self, co_parsovat=0):
		LogCSFD.WriteToFile('[CSFD] parserListOfMovies - zacatek\n')
		
		searchresults = []
		
		for movie in self.json_data["films"]:
			if movie["year"] != None:
				year = '(%d)' % movie["year"]
			else:
				year = ""
			searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], year, 'c' + movie["rating_category"] ) )
			
			if movie["search_name"] != movie["name"]:
				searchresults.append( ( '#movie#%d' % movie["id" ], movie["search_name"], year, 'c' + movie["rating_category"] ) )

		LogCSFD.WriteToFile('[CSFD] parserListOfMovies - konec\n')
		return searchresults

	def parserListOfRelatedMovies(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - zacatek\n')
		searchresults = []
		
		try:
			if "related" not in self.json_data:
				self.json_data["related"] = csfdAndroidClient.get_movie_related( self.json_data["info"]["id"], 0, 50 )["related"]

			movie_info = self.json_data["related"]
			
			for movie in movie_info:
				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], '(%d)' % movie["year"], 'c' + movie["rating_category"] ) )
		except:
			LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - failed\n')

		LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - konec\n')
		return searchresults

	def parserListOfSimilarMovies(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfSimilarMovies - zacatek\n')
		searchresults = []
		
		try:
			if "similar" not in self.json_data:
				self.json_data["similar"] = csfdAndroidClient.get_movie_similar( self.json_data["info"]["id"], 0, 50 )["similar"]

			movie_info = self.json_data["similar"]
			
			for movie in movie_info:
				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], '(%d)' % movie["year"], 'c' + movie["rating_category"] ) )
		except:
			LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - failed\n')

		LogCSFD.WriteToFile('[CSFD] parserListOfSimilarMovies - konec\n')
		return searchresults

	def parserListOfSeries(self ):
		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - zacatek\n')

		searchresults = []
		type_id = self.json_data["info"]["type_id"]
		
		if (type_id == 11 or type_id == 12) and self.json_data["info"]["has_no_seasons"] == False:
			if "seasons" not in self.json_data:
				self.json_data["seasons"] = csfdAndroidClient.get_movie_episodes( self.json_data["info"]["id"], 0, 0 )["seasons"]
				
			for movie in self.json_data["seasons"]:
				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], '(%d)' % movie["year"], 'c' + movie["rating_category"] ) )

		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - konec\n')
		return searchresults

	def parserListOfEpisodes(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfEpisodes - zacatek\n')
		
		searchresults = []
		
		type_id = self.json_data["info"]["type_id"]
		if type_id == 10 or type_id == 11 or type_id == 12:
			if "seasons" not in self.json_data:
				self.json_data["seasons"] = csfdAndroidClient.get_movie_episodes( self.json_data["info"]["id"], 0, 0 )["seasons"]

			for season in self.json_data["seasons"]:
				for movie in season["episodes"]:
					if type_id == 12:
						name_prefix = movie["position_code"] + " - "
					else:
						name_prefix = ""
					searchresults.append( ( '#movie#%d' % movie["id" ], name_prefix + movie["name"], '(%d)' % movie["year"], 'c' + movie["rating_category"] ) )

		LogCSFD.WriteToFile('[CSFD] parserListOfEpisodes - konec\n')
		return searchresults

	def parserRatingStars(self):
		LogCSFD.WriteToFile('[CSFD] parserRatingStars - zacatek\n')
		try:
			ratingstars = self.json_data["info"]["rating_average"]
			
			if ratingstars == None:
				ratingstars = -1
		except:
			ratingstars = -1

		LogCSFD.WriteToFile('[CSFD] parserRatingStars - konec\n')
		return ratingstars

	def parserMovieTitleInclYear(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - zacatek\n')
		
		try:
			movie_info = self.json_data["info"]
			titelblock = '%s (%d)' % (movie_info["name"], movie_info["year"])
		except:
			LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - failed\n')
			titelblock = '' 

		LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - konec\n')
		return titelblock

	def parserMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieTitle - zacatek\n')
		try:
			movie_info = self.json_data["info"]
			
			if "root_name" in movie_info:
				jmenoblock = movie_info["root_name"] + ' - ' + movie_info["name"]
			else:
				jmenoblock = movie_info["name"]
			
			
		except:
			LogCSFD.WriteToFile('[CSFD] parserMovieTitle - failed\n')
			jmenoblock = '' 
		LogCSFD.WriteToFile('[CSFD] parserMovieTitle - konec\n')
		return jmenoblock

	def parserSeriesNameInEpisode(self):
		LogCSFD.WriteToFile('[CSFD] parserSeriesNameInEpisode - zacatek\n')
		
		movie_info = self.json_data["info"]
		
		if "root_name" in movie_info:
			name = movie_info["root_name"]
		else:
			name = None

		LogCSFD.WriteToFile('[CSFD] parserSeriesNameInEpisode - konec\n')
		return name

	def parserTypeOfMovie(self):
		LogCSFD.WriteToFile('[CSFD] parserTypeOfMovie - zacatek\n')
		
		movie_info = self.json_data["info"]
		
		try:	
			typeMovie = movie_info["type"]
			
			try:
				typeMovie = typeOfMovie[typeMovie]
			except:
				pass
			
			typeMovie += ' '
		except:
			LogCSFD.WriteToFile('[CSFD] parserTypeOfMovie - Failed\n')
			typeMovie = ''

		try:	
			typeMovie += movie_info["position_code"]
		except:
			pass
		
		LogCSFD.WriteToFile('[CSFD] parserTypeOfMovie - konec\n')
		return typeMovie

	def parserOtherMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitle - zacatek\n')
		ostjmenatext = self.parserOrigMovieTitle()
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitle - konec\n')
		return ostjmenatext

	def parserOtherMovieTitleWOCountry(self):
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitleWOCountry - zacatek\n')
		searchresults = None
		
		orig_name = self.parserOrigMovieTitle()
		
		if orig_name != None:
			searchresults = [ orig_name ]
		
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitleWOCountry - konec\n')
		return searchresults

	def parserOrigMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - zacatek\n')
		origname = None
		
		try:
			movie_info = self.json_data["info"]
			
			if "name_orig" in movie_info:
				origname = movie_info["name_orig"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - Failed\n')
			origname = None
		
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - konec\n')
		return origname

	def parserMainPosterUrl(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - zacatek\n')

		try:
			url = self.json_data["info"]["poster_url"]
			
			if url == None and "root_info" in self.json_data:
				url = self.json_data["root_info"]["poster_url"]
				
			if full_image:
				qidx = url.rfind('?h')
				if qidx != -1:
					url = url[:qidx]
		except:
			LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - failed\n')
			url = None
		
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - konec\n')
		return url

	def parserAllPostersUrl(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - zacatek\n')
		posterresult1 = None
		ret = self.parserMainPosterUrl( full_image )
		if ret != None and ret != '':
			posterresult1 = [ ret ]
		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - konec\n')
		return posterresult1

	def parserPostersNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - zacatek\n')
		
		pocet = None
		
		if self.json_data["info"]["poster_url"] != None or ("root_info" in self.json_data and self.json_data["info"]["poster_url"] != None):
			pocet = 1

		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - konec\n')
		return pocet

	def parserGenre(self):
		LogCSFD.WriteToFile('[CSFD] parserGenre - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			genre = ''
			for x in movie_info["genre"]:
				if genre == '':
					genre += x
				else:
					genre += ", " + x
		except:
			LogCSFD.WriteToFile('[CSFD] parserGenre - failed\n')
			genre = ''

		LogCSFD.WriteToFile('[CSFD] parserGenre - konec\n')
		return genre

	def parserOrigin(self):
		LogCSFD.WriteToFile('[CSFD] parserOrigin - zacatek\n')
		
		try:
			movie_info = self.json_data["info"]
			origin = ''
			for x in movie_info["origin"]:
				if origin != '':
					origin += ", "
				
				origin += x
		except:
			LogCSFD.WriteToFile('[CSFD] parserOrigin - failed\n')
			origin = ''

		LogCSFD.WriteToFile('[CSFD] parserOrigin - konec\n')
		return origin

	def parserMovieYear(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieYear - zacatek\n')
		
		try:
			movie_info = self.json_data["info"]
			year = str( movie_info["year"] )
		except:
			LogCSFD.WriteToFile('[CSFD] parserMovieYear - failed\n')
			year = ''

		LogCSFD.WriteToFile('[CSFD] parserMovieYear - konec\n')
		return year

	def parserMovieDuration(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieDuration - zacatek\n')
		delka = None
		
		try:
			movie_info = self.json_data["info"]
			delka = movie_info["length"] + ' min.'
		except:
			LogCSFD.WriteToFile('[CSFD] parserMovieDuration - failed\n')
			delka = None

		LogCSFD.WriteToFile('[CSFD] parserMovieDuration - konec\n')
		return delka

	def parserMovieDurationMin(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieDurationMin - zacatek\n')
		delka = self.parserMovieDuration()
		if delka is not None:
			delka = delka.replace('min.', '').strip()
			if delka == '':
				delka = None
		LogCSFD.WriteToFile('[CSFD] parserMovieDurationMin - konec\n')
		return delka

	def parserMovieCountry(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieCountry - zacatek\n')
		country = None
		info = self.parserOrigin()
		if info is not None:
			r_info = info.split(',')
			country = r_info[0].replace(' / ', ', ').strip()
		LogCSFD.WriteToFile('[CSFD] parserMovieCountry - konec\n')
		return country

	def parserCSFDRankings(self):
		LogCSFD.WriteToFile('[CSFD] parserCSFDRankings - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			Zebrickytext = ''
			for x in movie_info["charts"]:
				Zebrickytext += x["title"] + ' na CSFD\n'

		except:
			LogCSFD.WriteToFile('[CSFD] parserCSFDRankings - failed\n')
			Zebrickytext = ''
		
		LogCSFD.WriteToFile('[CSFD] parserCSFDRankings - konec\n')
		return Zebrickytext

	def parserWherePlaying(self):
		LogCSFD.WriteToFile('[CSFD] parserWherePlaying - zacatek\n')
		
		try:
			movie_info = self.json_data["info"]
			text = ''
			for x in movie_info["tv_schedule"]:
				if text != '':
					text += ", "

				# convert 2022-01-04 21:55:00.000000+0100 -> 04.01 21:55
				play_date = x["start_datetime"][5:16]
				play_date = play_date[3:5] + '.' + play_date[0:2] + '. ' + play_date[6:]
				text += x["station"]["name"] + ' ' + play_date
		except:
			LogCSFD.WriteToFile('[CSFD] parserWherePlaying - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserWherePlaying - konec\n')
		return text

	def parserDirector(self):
		LogCSFD.WriteToFile('[CSFD] parserDirector - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			text = ''
			for x in movie_info["directors"]:
				if text != '':
					text += ", "
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserDirector - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserDirector - konec\n')
		return text

	def parserMusic(self):
		LogCSFD.WriteToFile('[CSFD] parserMusic - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["composers"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserMusic - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserMusic - konec\n')
		return text

	def parserDraft(self):
		LogCSFD.WriteToFile('[CSFD] parserDraft - zacatek\n')
		
		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["authors"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserDraft - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserDraft - konec\n')
		return text

	def parserWriters(self):
		LogCSFD.WriteToFile('[CSFD] parserWriters - zacatek\n')
		
		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["authors"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserWriters - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserWriters - konec\n')
		return text

	def parserScenario(self):
		LogCSFD.WriteToFile('[CSFD] parserScenario - zacatek\n')
		
		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["screenwriters"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserScenario - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserScenario - konec\n')
		return text

	def parserCamera(self):
		LogCSFD.WriteToFile('[CSFD] parserCamera - zacatek\n')
		
		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["cinematographers"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserScenario - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserCamera - konec\n')
		return text

	def parserProduction(self):
		LogCSFD.WriteToFile('[CSFD] parserProduction - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["production"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserProduction - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserProduction - konec\n')
		return text

	def parserCutting(self):
		LogCSFD.WriteToFile('[CSFD] parserCutting - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["edit"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserCutting - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserCutting - konec\n')
		return text

	def parserSound(self):
		LogCSFD.WriteToFile('[CSFD] parserSound - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["sound"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserSound - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserSound - konec\n')
		return text

	def parserScenography(self):
		LogCSFD.WriteToFile('[CSFD] parserScenography - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["scenographies"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserScenography - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserScenography - konec\n')
		return text

	def parserMakeUp(self):
		LogCSFD.WriteToFile('[CSFD] parserMakeUp - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["masks"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserMakeUp - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserMakeUp - konec\n')
		return text

	def parserCostumes(self):
		LogCSFD.WriteToFile('[CSFD] parserCostumes - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["costumes"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserCostumes - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserCostumes - konec\n')
		return text

	def parserCasting(self):
		LogCSFD.WriteToFile('[CSFD] parserCasting - zacatek\n')

		try:
			movie_info = self.json_data["creators"]
			text = ''
			for x in movie_info["actors"]:
				if text != '':
					text += ', '
				
				text += x["firstname"] + " " + x["surname"]
		except:
			LogCSFD.WriteToFile('[CSFD] parserCasting - failed\n')
			text = ''

		LogCSFD.WriteToFile('[CSFD] parserCasting - konec\n')
		return text

	def parserTags(self):
		LogCSFD.WriteToFile('[CSFD] parserTags - zacatek\n')
		text = None
		LogCSFD.WriteToFile('[CSFD] parserTags - konec\n')
		return text

	def parserContent(self):
		LogCSFD.WriteToFile('[CSFD] parserContent - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			Obsahtext = ParserConstCSFD.delHTMLtags(movie_info["plot"]["text"] + '\n(' + movie_info["plot"]["source_name"] + ')' )
		except:
			LogCSFD.WriteToFile('[CSFD] parserContent - failed\n')
			Obsahtext = ''

		LogCSFD.WriteToFile('[CSFD] parserContent - konec\n')
		return Obsahtext

	def parserIMDBlink(self):
		LogCSFD.WriteToFile('[CSFD] parserIMDBlink - zacatek\n')
		result = ''
		LogCSFD.WriteToFile('[CSFD] parserIMDBlink - konec\n')
		return result

	def parserRatingNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserRatingNumber - zacatek\n')
		pocet_hodnoceni = None
		LogCSFD.WriteToFile('[CSFD] parserRatingNumber - konec\n')
		return pocet_hodnoceni

	def parserUserComments(self, data ):
		LogCSFD.WriteToFile('[CSFD] parserUserComments - zacatek\n')
		searchresults = []
		
		for comment in data["comments"]:
			comment_text = ParserConstCSFD.delHTMLtags( comment["text"] )
			if comment["rating"] == None:
				rating_stars = ""
			elif int(comment["rating"]) == 0:
				rating_stars = "odpad!"
			else:
				rating_stars = "* " * int(int(comment["rating"]) / 20)
			
			# convert 2022-01-04 21:55 -> 04.01.2022 21:55
			comment_date = comment["inserted_datetime"][:-15]
			comment_date = comment_date[8:10] + '.' + comment_date[5:7] + '.' + comment_date[0:4] + '  ' + comment_date[11:]

			searchresults.append( (comment["user"]["nick"], rating_stars , comment_date, comment_text) )

		LogCSFD.WriteToFile('[CSFD] parserUserComments - konec\n')
		if len(searchresults) == 0:
			return None
		return searchresults

	def parserUserCommentsNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserCommentsNumber - zacatek\n')
		pocet = int( self.json_data["info"]["summary"]["comment_count"] )
		LogCSFD.WriteToFile('[CSFD] parserUserCommentsNumber - konec\n')
		return pocet

	def parserUserExtReviews(self):
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviews - zacatek\n')
		
		# rating_stars = '*' - '*****' alebo odpad
		# searchresults.append( (nick, rating_stars, text) )
		searchresults = None

		LogCSFD.WriteToFile('[CSFD] parserUserExtReviews - konec\n')
		return searchresults

	def parserUserExtReviewsNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviewsNumber - zacatek\n')
		pocet = None
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviewsNumber - konec\n')
		return pocet

	def parserUserDiscussion(self):
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussion - zacatek\n')
		# searchresults.append( (date, nick, text) )
		searchresults = None

		LogCSFD.WriteToFile('[CSFD] parserUserDiscussion - konec\n')
		return searchresults

	def parserUserDiscussionNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussionNumber - zacatek\n')
		pocet = None
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussionNumber - konec\n')
		return pocet

	def parserInterest(self, data ):
		LogCSFD.WriteToFile('[CSFD] parserInterest - zacatek\n')

		searchresults = None
		movie_info = data["trivia"]
		
		if len( movie_info ) > 0:
			searchresults = []
				
			for trivia in movie_info:
				try:
					searchresults.append( ( ParserConstCSFD.delHTMLtags( trivia["text"] ), trivia["source_user"]["nick"]) )
				except:
					pass

		LogCSFD.WriteToFile('[CSFD] parserInterest - konec\n')
		return searchresults

	def parserInterestNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestNumber - zacatek\n')
		pocet = int( self.json_data["info"]["summary"]["trivia_count"] )
		LogCSFD.WriteToFile('[CSFD] parserInterestNumber - konec\n')
		return pocet

	def parserUserRating(self):
		LogCSFD.WriteToFile('[CSFD] parserUserRating - zacatek\n')
		# searchresults.append( (user, rating_stars) )
		searchresults = None
		LogCSFD.WriteToFile('[CSFD] parserUserRating - konec\n')
		return searchresults

	def parserPremiere(self):
		LogCSFD.WriteToFile('[CSFD] parserPremiere - zacatek\n')
		text = ''
		pristupnost = ''
		
		movie_info = self.json_data["info"]
		
		if "releases" in movie_info:
			if "cinema" in movie_info["releases"]:
				text += _("V kinech:") + "\n"
				for release in movie_info["releases"]["cinema"]:
					release_date = release["release_date"]
					release_date = release_date[8:10] + '.' + release_date[5:7] + '.' + release_date[0:4]
					distributor = release["distributor"] if release["distributor"] != None else ""
					text += release["country"] + '\t' + release_date + "  " + distributor + '\n'
				
				text += '\n'
				
			if "dvd" in movie_info["releases"]:
				text += _("Na DVD:") + "\n"
				for release in movie_info["releases"]["dvd"]:
					release_date = release["release_date"]
					release_date = release_date[8:10] + '.' + release_date[5:7] + '.' + release_date[0:4]
					distributor = release["distributor"] if release["distributor"] != None else ""
					text += release["country"] + '\t' + release_date + "  " + distributor + '\n'
				text += '\n'
				
			if "bluray" in movie_info["releases"]:
				text += _("Na blu-ray:") + "\n"
				for release in movie_info["releases"]["bluray"]:
					release_date = release["release_date"]
					release_date = release_date[8:10] + '.' + release_date[5:7] + '.' + release_date[0:4]
					distributor = release["distributor"] if release["distributor"] != None else ""
					text += release["country"] + '\t' + release_date + "  " + distributor + '\n'
				text += '\n'

			if "tv" in movie_info["releases"]:
				text += _("V televizi:") + "\n"
				for release in movie_info["releases"]["tv"]:
					release_date = release["release_date"]
					release_date = release_date[8:10] + '.' + release_date[5:7] + '.' + release_date[0:4]
					distributor = release["distributor"] if release["distributor"] != None else ""
					text += release["country"] + '\t' + release_date + "  " + distributor + '\n'

		LogCSFD.WriteToFile('[CSFD] parserPremiere - konec\n')
		return (text, pristupnost)

	def parserAwards(self):
		LogCSFD.WriteToFile('[CSFD] parserAwards - zacatek\n')
		searchresults = None
		LogCSFD.WriteToFile('[CSFD] parserAwards - konec\n')
		return searchresults

	def parserUserFans(self):
		LogCSFD.WriteToFile('[CSFD] parserUserFans - zacatek\n')
		text = ''
		LogCSFD.WriteToFile('[CSFD] parserUserFans - konec\n')
		return text

	def parserUserFansNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserFansNumber - zacatek\n')
		pocet = None
		LogCSFD.WriteToFile('[CSFD] parserUserFansNumber - konec\n')
		return pocet

	def parserVideoDetail(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - 0a\n')

		searchresults = None
		
		if len( self.json_data["videos"] ) > 0:
			searchresults = []
			
			for video in self.json_data["videos"]:
				if "1080" in video["video"]:
					videoklipurlHD = video["video"]["1080"]
				elif "720" in video["video"]:
					videoklipurlHD = video["video"]["720"]
				else:
					videoklipurlHD = ''

				if "480" in video["video"]:
					videoklipurlSD = video["video"]["480"]
				elif "360" in video["video"]:
					videoklipurlSD = video["video"]["360"]
				else:
					videoklipurlSD = ''
					
				videotitulkyurlCZ = ''
				videotitulkyurlSK = ''
				
				try:
					videotitulkyurlCZ = video["subtitles"]["české".decode('utf-8')]
				except:
					pass

				try:
					videotitulkyurlSK = video["subtitles"]["slovenské".decode('utf-8')]
				except:
					pass
					
				videoDescr = video["description"]
				videoPoster = video["preview_image"]["url"]
				
				if full_image and videoPoster.endswith("?w700"):
					videoPoster = videoPoster[:-5]
					
				searchresults.append((videoklipurlSD, videoklipurlHD, videotitulkyurlCZ, videotitulkyurlSK, videoDescr, videoPoster))

		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - konec\n')
		return searchresults

	def parserOwnRating(self):
		LogCSFD.WriteToFile('[CSFD] parserOwnRating - zacatek\n')
		if "rating" in self.json_data["info"] and self.json_data["info"]["rating"] != None:
			num_rating = int(self.json_data["info"]["rating"]["rating"])
			ss_rating = "* " * int(num_rating / 20)
		else:
			num_rating = None # number 0-100
			ss_rating = '' # star rating string in format '60%   * * *'
		
		LogCSFD.WriteToFile('[CSFD] parserOwnRating - konec\n')
		return (ss_rating, num_rating)

	def parserDateOwnRating(self):
		LogCSFD.WriteToFile('[CSFD] parserDateOwnRating - zacatek\n')
		if "rating" in self.json_data["info"] and self.json_data["info"]["rating"]:
			ss_date_rating = self.json_data["info"]["rating"]["inserted_datetime"][:-15]
			
			# convert 2022-01-04 21:55 -> 04.01.2022 21:55
			ss_date_rating = ss_date_rating[8:10] + '.' + ss_date_rating[5:7] + '.' + ss_date_rating[0:4] + ' ' + ss_date_rating[11:]
		else:
			ss_date_rating = None
		LogCSFD.WriteToFile('[CSFD] parserDateOwnRating - konec\n')
		return ss_date_rating

	def parserRatingAllowed(self):
		LogCSFD.WriteToFile('[CSFD] parserRatingAllowed - zacatek\n')
		if "rating_allowed" in self.json_data["info"] and self.json_data["info"]["rating_allowed"] == True:
			ret = True
		else:
			ret = False
		LogCSFD.WriteToFile('[CSFD] parserRatingAllowed - konec\n')
		return ret

	def parserTokenLogin(self, html):
		LogCSFD.WriteToFile('[CSFD] parserTokenLogin - zacatek\n')
		token = None
		LogCSFD.WriteToFile('[CSFD] parserTokenLogin - konec\n')
		return token

	def parserURLLogin(self, html):
		LogCSFD.WriteToFile('[CSFD] parserURLLogin - zacatek\n')
		url = ''
		LogCSFD.WriteToFile('[CSFD] parserURLLogin: ' + url + '\n')
		LogCSFD.WriteToFile('[CSFD] parserURLLogin - konec\n')
		return url

	def parserDeleteRatingUrl(self):
		LogCSFD.WriteToFile('[CSFD] parserDeleteRatingUrl - zacatek\n')
		url = None
		LogCSFD.WriteToFile('[CSFD] parserDeleteRatingUrl - konec\n')
		return url

	def parserFunctionExists(self):
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - zacatek\n')
		searchresults = []
		
		if int(self.json_data["info"]["summary"]["comment_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - komentare - NE\n')
			searchresults.append('komentare')

		if int(self.json_data["info"]["summary"]["trivia_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - zajimavosti - NE\n')
			searchresults.append('zajimavosti')
		
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - oceneni - NE\n')
		searchresults.append('oceneni')

		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - ext.recenze - NE\n')
		searchresults.append('ext.recenze')
		
		if int(self.json_data["info"]["summary"]["photo_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - galerie - NE\n')
			searchresults.append('galerie')
			
		if int(self.json_data["info"]["summary"]["video_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - video - NE\n')
			searchresults.append('video')
			
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - diskuze - NE\n')
		searchresults.append('diskuze')

		if self.parserRatingNumber() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - hodnoceni - NE\n')
			searchresults.append('hodnoceni')
		
		if self.parserUserFansNumber() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - fanousci - NE\n')
			searchresults.append('fanousci')
			
		if self.json_data["info"]["releases"] == False:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - premiery - NE\n')
			searchresults.append('premiery')
		
		if self.parserPostersNumber() is None and self.parserMainPosterUrl() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - postery - NE\n')
			searchresults.append('postery')
			
#		if self.parserTokenRating() is None:
		if self.parserRatingAllowed() == False:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - ownrating - NE\n')
			searchresults.append('ownrating')
			
		if int(self.json_data["info"]["summary"]["related_films_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - souvisejici - NE\n')
			searchresults.append('souvisejici')
			
		if int(self.json_data["info"]["summary"]["similar_films_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - podobne - NE\n')
			searchresults.append('podobne')

		if self.json_data["info"]["type_id"] != 12 or self.json_data["info"]["has_no_seasons"] == True:		
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - serie - NE\n')
			searchresults.append('serie')
			
		if self.json_data["info"]["type_id"] != 10 and self.json_data["info"]["type_id"] != 12:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - epizody - NE\n')
			searchresults.append('epizody')
			
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - konec\n')
		return searchresults
	
	def parserListOfTVMovies(self, deleteDuplicity=False):
		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - zacatek\n')
		searchresults = []

		for station in self.json_data["stations"]:
			LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - parsing %s\n' % station['name'])
			
			for schedule in station['schedule']:
				movie = schedule['film']
				if movie['id'] != None:
					c = movie['rating_category'] if movie['rating_category'] != None else "0"
					year = movie['year'] if movie['year'] != None else ''
					searchresults.append( ( '#movie#' + str(movie['id']), movie['name'], str(year), "c" + str(c) ) )

		# searchresults.append( (movie_id, movie_name, year, color_class) )
		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - konec\n')
		return searchresults

	def parserPrivateComment(self):
		LogCSFD.WriteToFile('[CSFD] parserPrivateComment - zacatek\n')
		comment = None
		LogCSFD.WriteToFile('[CSFD] parserPrivateComment - konec\n')
		return comment

	def resetValues(self):
		LogCSFD.WriteToFile('[CSFD] resetValues - zacatek\n')
		self.json_data = {}
		LogCSFD.WriteToFile('[CSFD] resetValues - konec\n')
		
	def setJson(self, data):
		self.json_data = data
		
	def testJson(self):
		if "http_error" in self.json_data or "internal_error" in self.json_data:
			return False
		
		return True


ParserCSFD = CSFDParser()
ParserOstCSFD = CSFDParser()
ParserVideoCSFD = CSFDParser()
ParserTVCSFD = CSFDParser()

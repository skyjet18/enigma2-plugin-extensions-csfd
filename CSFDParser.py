# -*- coding: utf-8 -*-

from .CSFDLog import LogCSFD
from .CSFDTools import char2Allowchar, strUni, ExtractNumbers, isBigCharInFirst, CheckValidValue, CreateNameSurname, CreateNameSurnameList, Uni8, StripAccents
from .CSFDSettings1 import CSFDGlobalVar
from datetime import datetime
import re, traceback
from itertools import islice

from .CSFDAndroidClient import csfdAndroidClient

try:
	# py2
	from .htmlentitydefs import name2codepoint
except:
	# py3
	from html.entities import name2codepoint
	unichr = chr
	unicode = str
	
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
	'TV film': _('TV film'),
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

class MovieType():
	UNUSED = 0
	VIDEO_MOVIE = 1
	TV_MOVIE = 2
	SERIAL = 3
	SHOW = 4
	THEATRE_RECORD = 5
	CONCERT = 6
	STUDENT_MOVIE = 7
	AMATEUR_MOVIE = 8
	MUSIC_VIDEO = 9
	SERIE = 10
	EPISODE = 11
	SERIAL_WITH_EPISODES = 12 # example: Simpsons
	SHOW_WITH_EPISODES = 13 # example: MythBusters
	VIDEO_COMPILATION = 14

	# used for translation
	movie_type_map = {
		0: "", # used also for type 1 - to not show type in text form
		1: _('Video film'),
		2: _('TV film'),
		3: _('TV seriál'),
		4: _('TV pořad'),
		5: _('Divadelní záznam'),
		6: _('Koncert'),
		7: _('Studentský film'),
		8: _('Amatérský film'),
		9: _('Hudební videoklip'),
		10: _('Seriál - série'),
		11: _('Seriál - epizoda'),
		12: _('TV seriál'), # example: Simpsons
		13: _('TV pořad'), # example: MythBusters
		14: _('Video kompilace')
	}
	
	# used for reverse mapping
	movie_type_map2 = {
		0: "", # used also for type 1 - to not show type in text form
		1: "video film",
		2: "TV film",
		3: "seriál",
		4: "pořad",
		5: "divadelní záznam",
		6: "koncert",
		7: "studentský film",
		8: "amatérský film",
		9: "hudební videoklip",
		10: "série",
		11: "epizoda",
		12: "seriál s epizodami", # example: Simpsons
		13: "pořad s epizodami", # example: MythBusters
		14: "video kompilace"
	}
	movie_type_map_rev = {}
	
	def __init__(self):
		# build reverse map
		for movie_type in self.movie_type_map2:
			self.movie_type_map_rev[ Uni8( self.movie_type_map2[movie_type] ) ] = movie_type
	
	def idToStr(self, type_id ):
		return self.movie_type_map[type_id]
	
	def strToId(self, type_str ):
		return self.movie_type_map_rev[type_str] if type_str in self.movie_type_map_rev else 0
	
	def isEpisode(self, movie_type ):
		return movie_type == self.EPISODE

	def isSeriesOrShow(self, movie_type ):
		return movie_type in (self.SERIAL, self.SERIAL_WITH_EPISODES, self.SHOW, self.SHOW_WITH_EPISODES)
	
	def isLowPriority(self, movie_type ):
		return movie_type not in ( self.UNUSED, self.VIDEO_MOVIE, self.TV_MOVIE, self.SERIAL, self.SHOW, self.SERIAL_WITH_EPISODES, self.SHOW_WITH_EPISODES )
	
movieType = MovieType()


def channel_name_normalise( name ):
	name = StripAccents( name ).lower()

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
		typc = '1'
	elif rate >= 30:
		typc = '2'
	elif rate >= 0:
		typc = '3'
	else:
		typc = '0'
	return typc


def GetItemColourN(typ=''):
	if typ == 'c0':
		typn = '0'
	elif typ == 'c1':
		typn = '1'
	elif typ == 'c2':
		typn = '2'
	elif typ == 'c3':
		typn = '3'
	else:
		typn = '0'
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


def NameMovieCorrections(name_s, corr1_enable=True):

	def corr1(name1):
		if corr1_enable == False:
			return name1
		
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
	
	# correct wrong roman numbers (1 or i at the end)
	if len(name_s) > 2 and (name_s[-1] == '1' or name_s[-1] == 'i') and name_s[-2] in ('I', 'V', 'X'):
		name_s = name_s[:-1] + 'I'
	
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
		self.parserYear3 = re.compile('\[19\\d{2}\]|\[20\\d{2}\]', re.DOTALL)
		self.parserDate = re.compile('\\d{2}\\.\\d{2}\\.\\d{4}', re.DOTALL)
		self.parserNumbers = re.compile(' \\d+', re.DOTALL)
		self.parserRomanNumerals = re.compile('\\b(?!LLC)(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.DOTALL)
		self.parserPositionCode1 = re.compile( '\(S[0-9]+E[0-9]+\)', re.DOTALL )
		self.parserPositionCode2 = re.compile( '\(S[0-9]+E[0-9]+[/-][0-9]+\)', re.DOTALL )

		self.parserEpisode = re.compile( '\(E[0-9]+\)', re.DOTALL )
		self.parserSerie = re.compile( '\(S[0-9]+\)', re.DOTALL )

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

	def parserGetYears(self, name, delim=''):
		LogCSFD.WriteToFile('[CSFD] parserGetYears - zacatek\n')
		searchresults = []
		if delim == '':
			results = self.parserYear.findall(name)
		elif delim == '(':
			results = self.parserYear2.findall(name)
		elif delim == '[':
			results = self.parserYear3.findall(name)
		else:
			return searchresults
		
		if results is not None:
			if delim == '':
				for value in results:
					LogCSFD.WriteToFile('[CSFD] parserGetYears - have year %s\n' % value[1:-1])
					searchresults.append(value)
			else:
				for value in results:
					LogCSFD.WriteToFile('[CSFD] parserGetYears - have year %s\n' % value)
					searchresults.append(value[1:-1])

		LogCSFD.WriteToFile('[CSFD] parserGetYears - konec\n')
		return list(set(searchresults))

	def delHTMLtags(self, string):
		return self.parserhtmltags.sub('', string)
	
	def parserGetPositionCode(self, name ):
		results = self.parserPositionCode1.findall(name)
		
		if results is not None and len(results) == 1:
			pc = results[0][1:-1].split('E')
			return int(pc[0][1:]), int(pc[1])

		results = self.parserPositionCode2.findall(name)
		
		if results is not None and len(results) == 1:
			pc = results[0][1:-1].split('E')
			return int(pc[0][1:]), int(pc[1].split('/')[0].pc[1].split('-')[0])

		return None, None

	def parserGetEpisode(self, name ):
		results = self.parserEpisode.findall(name)
		
		if results is not None and len(results) == 1:
			return int(results[0][2:-1])

		return None

	def parserGetSerie(self, name ):
		results = self.parserSerie.findall(name)
		
		if results is not None and len(results) == 1:
			return int(results[0][2:-1])

		return None

	def najdi(self, retezec, celytext):
		maska = re.compile(retezec, re.DOTALL)
		vysledek = maska.findall(celytext)
		vysledek = vysledek[0] if vysledek else ""
		return vysledek

	def rimskeArabske(self, vstupnirimska):
		definicecislic = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
		rimska = ""
		for rznak in vstupnirimska:
			if rznak in "IVXLCDM":
				rimska+= rznak
		arabska = 0
		for iii, ccc in enumerate(rimska):
			if (iii+1) == len(rimska) or definicecislic[ccc] >= definicecislic[rimska[iii+1]]:
				arabska += definicecislic[ccc]
			else:
				arabska -= definicecislic[ccc]
		if arabska == 0:
			return None

		return arabska

	def rozlozeniNazvu(self, upravovanytext):
		zbytecnosti = [" -HD", " -W", " -ST", " -AD"]
		for zbytecnost in zbytecnosti:
			upravovanytext = upravovanytext.replace(zbytecnost, '')
			
		serialy = self.najdi('\s+([IVX]{0,7}\.?\s?\([0-9]?[0-9]?[0-9][,-/]?\s?[0-9]?[0-9]?[0-9]?\))', upravovanytext)
		casti = self.najdi('\s+(\(?[0-9]?[0-9]?[0-9]/[0-9]?[0-9]?[0-9]\)?)(?![0-9])', upravovanytext)
		rimska_na_konci = self.najdi('\s+([IVX]{1,5}\.?)\s*$', upravovanytext)
		arabska_na_konci = self.najdi('\s+([0-9]?[0-9]?[0-9])\s*$', upravovanytext)
		kompletnazev = upravovanytext.replace(serialy, '').replace(" "+casti, ' ').replace(" "+rimska_na_konci, ' ').replace(" "+arabska_na_konci, ' ')
		rimska_na_konci = rimska_na_konci.replace(".","")
		rozlozenynazev = re.split('[:,;]', kompletnazev)
		nazev1 = rozlozenynazev[0].rstrip(' ')
		nazev2 = ""
		
		seria_num = None
		epizoda_num = None
		
		if len(rozlozenynazev) > 1:
			nazev2 = rozlozenynazev[1].lstrip(' ').rstrip(' ')
		if serialy:
#			print("X_Serialy: %s" % serialy)
			serie = self.najdi('([IVX]{1,5})', serialy)
			if serie:
				seria_num = self.rimskeArabske(serie)
				
			epizoda = self.najdi('\(([0-9]?[0-9]?[0-9])', serialy)
			epizoda_num = int(epizoda)
		elif casti:
#			print("X_Casti: %s" % casti)
			epizoda = self.najdi('([0-9]?[0-9]?[0-9])/', casti)
			epizoda_num = int(epizoda)
		elif rimska_na_konci:
#			print("X_RNK: %s" % rimska_na_konci)
			seria_num = self.rimskeArabske(rimska_na_konci)
	
		serialy = self.najdi('\s+([IVX]{0,7}\.?\s?\([0-9]?[0-9]?[0-9][,-]?\s?[0-9]?[0-9]?[0-9]?\))', nazev1)
		casti = self.najdi('\s+(\(?[0-9]?[0-9]?[0-9]/[0-9]?[0-9]?[0-9]\)?)(?![0-9])', nazev1)
		rimska_na_konci = self.najdi('([IVX]{1,5}\.?)\s*$', nazev1)
		arabska_na_konci = self.najdi('([0-9]?[0-9]?[0-9])\s*$', nazev1)
		nazev1 = nazev1.replace(serialy, '').replace(" "+casti, ' ').replace(" "+rimska_na_konci, ' ').replace(" "+arabska_na_konci, ' ')
	
		serialy = self.najdi('\s+([IVX]{0,7}\.?\s?\([0-9]?[0-9]?[0-9][,-]?\s?[0-9]?[0-9]?[0-9]?\))', nazev2)
		casti = self.najdi('\s+(\(?[0-9]?[0-9]?[0-9]/[0-9]?[0-9]?[0-9]\)?)(?![0-9])', nazev2)
		rimska_na_konci = self.najdi('([IVX]{1,5}\.?)\s*$', nazev2)
		arabska_na_konci = self.najdi('([0-9]?[0-9]?[0-9])\s*$', nazev2)
		nazev2 = nazev2.replace(serialy, '').replace(" "+casti, ' ').replace(" "+rimska_na_konci, ' ').replace(" "+arabska_na_konci, ' ')
	
		return kompletnazev, nazev1, nazev2, seria_num, epizoda_num

ParserConstCSFD = CSFDConstParser()

class CSFDParser():

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - konec\n')

	def parserMoviesFound(self):
		LogCSFD.WriteToFile('[CSFD] parserMoviesFound - zacatek\n')
		res = False
		
		if len(self.json_data["films"]) > 0:
			res = True
		
		LogCSFD.WriteToFile('[CSFD] parserMoviesFound - False - konec\n')
		return res

	def parserListOfMovies(self, low_priority=True):
		LogCSFD.WriteToFile('[CSFD] parserListOfMovies - zacatek\n')
		
		searchresults = []
		
		for movie in self.json_data["films"]:
			movie_info = {
				'id': movie['id'],
				'name': movie['name'],
				'year': CheckValidValue(movie["year"]),
				'rating_category': CheckValidValue(movie["rating_category"], "0"),
				'type': movieType.strToId( movie['type'] )
			}
			
			if low_priority == False and movieType.isLowPriority( movie_info['type'] ):
				continue
			
#			searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], year, 'c' + movie["rating_category"], movie_info ) )
			searchresults.append( movie_info )
			
			if movie.get("search_name") is not None and movie["search_name"] != movie["name"]:
				movie_info2 = movie_info.copy()
				movie_info2['name'] = movie["search_name"]
#				searchresults.append( ( '#movie#%d' % movie["id" ], movie["search_name"], year, 'c' + movie["rating_category"], movie_info ) )
				searchresults.append( movie_info2 )

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
				movie_info = {
					'id': movie['id'],
					'name': movie['name'],
					'year': CheckValidValue(movie["year"]),
					'rating_category': CheckValidValue(movie["rating_category"], "0"),
					'type': movieType.strToId( movie['type'] )
				}

#				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], CheckValidValue(movie["year"], None), 'c' + movie["rating_category"], movie_info ) )
				searchresults.append( movie_info )
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
				movie_info = {
					'id': movie['id'],
					'name': movie['name'],
					'year': CheckValidValue(movie["year"]),
					'rating_category': CheckValidValue(movie["rating_category"], "0"),
					'type': movieType.strToId( movie['type'] )
				}

#				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], CheckValidValue(movie["year"], None), 'c' + movie["rating_category"], movie_info ) )
				searchresults.append( movie_info )
		except:
			LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - failed\n')

		LogCSFD.WriteToFile('[CSFD] parserListOfSimilarMovies - konec\n')
		return searchresults

	def parserListOfSeries(self ):
		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - zacatek\n')

		searchresults = []
		type_id = self.json_data["info"]["type_id"]
		
		if type_id in (movieType.SERIAL_WITH_EPISODES, movieType.SHOW_WITH_EPISODES, movieType.EPISODE) and self.json_data["info"]["has_no_seasons"] == False:
			if "seasons" not in self.json_data:
				self.json_data["seasons"] = csfdAndroidClient.get_movie_episodes( self.json_data["info"]["id"], 0, 0 )["seasons"]
				
			for movie in self.json_data["seasons"]:
				position_code = movie['episodes'][0]['position_code']
				if 'S' in position_code:
					position_code = position_code.split('E')[0]
				else:
					position_code = 'S01'
					
				movie_info = {
					'id': movie['id'],
					'name': movie['name'],
					'year': CheckValidValue(movie["year"]),
					'rating_category': CheckValidValue(movie["rating_category"], "0"),
					'type': movieType.SERIE,
					'position_code': position_code
				}

#				searchresults.append( ( '#movie#%d' % movie["id" ], movie["name"], CheckValidValue(movie["year"], None), 'c' + movie["rating_category"], movie_info ) )
				searchresults.append( movie_info )

		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - konec\n')
		return searchresults

	def parserListOfEpisodes(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfEpisodes - zacatek\n')
		
		searchresults = []
		
		type_id = self.json_data["info"]["type_id"]
		if type_id in (movieType.SERIAL_WITH_EPISODES, movieType.SHOW_WITH_EPISODES, movieType.SERIE):
			if "seasons" not in self.json_data:
				self.json_data["seasons"] = csfdAndroidClient.get_movie_episodes( self.json_data["info"]["id"], 0, 0 )["seasons"]

			for season in self.json_data["seasons"]:
				for movie in season["episodes"]:
					movie_info = {
						'id': movie['id'],
						'name': movie['name'],
						'year': CheckValidValue(movie["year"]),
						'rating_category': CheckValidValue(movie["rating_category"], "0"),
						'type': type_id - 9,
						'position_code': movie['position_code'] if 'position_code' in movie else ''
					}

#					searchresults.append( ( '#movie#%d' % movie["id" ], movie_info["position_code"] + ' ' + movie["name"] if movie_info['position_code'] != '' else movie["name"], CheckValidValue(movie["year"], None), 'c' + movie["rating_category"], movie_info ) )
					searchresults.append( movie_info )

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
			
			titelblock = movie_info["name"]
			year = movie_info.get("year")
			
			if year != None:
				titelblock += ' (%d)' % year
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
		name = movie_info.get("root_name", "")

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

	def parserOrigMovieTitle(self, json_data = None):
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - zacatek\n')
		origname = None
		
		if json_data == None:
			json_data = self.json_data
			
		try:
			movie_info = json_data["info"]
			origname = movie_info.get("name_orig", "")
		except:
			LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - Failed\n')
			origname = ''
		
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - konec\n')
		return origname

	def getUrlByImageResolution(self, url, image_resolution='' ):
		qidx = url.rfind('?')
			
		if qidx != -1:
			url = url[:qidx]
		
		if image_resolution != '':
			url += '?' + image_resolution
			
		return url

		
	def parserMainPosterUrl(self, image_resolution=''):
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - zacatek\n')

		try:
			url = self.json_data["info"]["poster_url"]
			
			if url == None and "parent_info" in self.json_data:
				url = self.json_data["parent_info"]["poster_url"]

				if url == None and "root_info" in self.json_data:
					url = self.json_data["root_info"]["poster_url"]
			
			url = self.getUrlByImageResolution( url, image_resolution )
		except:
			LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - failed\n')
			url = None
		
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - konec\n')
		return url

	def parserAllPostersUrl(self, image_resolution=''):
		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - zacatek\n')
		result = []

		try:
			for x in ('info', 'parent_info', 'root_info'):
				if x in self.json_data:
					url = self.json_data[x]["poster_url"]
					if url != None:
						result.append( self.getUrlByImageResolution( url, image_resolution ) )
		except:
			LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - failed\n')

		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - konec\n')
		return result if len( result ) > 0 else None

	def parserPostersNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - zacatek\n')

		urls = self.parserAllPostersUrl()

		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - konec\n')
		return len(urls) if urls is not None else None

	def parserGenre(self):
		LogCSFD.WriteToFile('[CSFD] parserGenre - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			genre = ', '.join( x for x in movie_info["genre"] )
		except:
			LogCSFD.WriteToFile('[CSFD] parserGenre - failed\n')
			genre = ''

		LogCSFD.WriteToFile('[CSFD] parserGenre - konec\n')
		return genre

	def parserOrigin(self):
		LogCSFD.WriteToFile('[CSFD] parserOrigin - zacatek\n')
		
		try:
			movie_info = self.json_data["info"]
			origin = ', '.join( x for x in movie_info["origin"] )
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
			delka = ''

		LogCSFD.WriteToFile('[CSFD] parserMovieDuration - konec\n')
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
			for x in islice( movie_info["tv_schedule"], 6 ):
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

	# available creator_type:
	# 'directors', 'authors', 'screenwriters', 'cinematographers', 'composers', 'production', 'edit', 'sound',
	# 'scenographies', 'masks', 'costumes', 'actors', 'performer'
	def parserGetCreatorList(self, creator_type):
		LogCSFD.WriteToFile('[CSFD] parserGetCreatorList[%s] - zacatek\n' % creator_type )
		
		try:
			movie_info = self.json_data["creators"]
			text = CreateNameSurnameList( movie_info[creator_type] )
		except:
			LogCSFD.WriteToFile('[CSFD] parserGetCreatorList[%s] - failed\n' % creator_type )
			text = ''
		
		LogCSFD.WriteToFile('[CSFD] parserGetCreatorList[%s] - konec\n' % creator_type )
		return text

	def parserContent(self):
		LogCSFD.WriteToFile('[CSFD] parserContent - zacatek\n')

		try:
			movie_info = self.json_data["info"]
			Obsahtext = ParserConstCSFD.delHTMLtags(movie_info["plot"]["text"] + '\n(' + movie_info["plot"]["source_name"] + ')' )
		except:
			try:
				# we try to get plot from season (if available)
				movie_info = self.json_data["parent_info"]
				Obsahtext = ParserConstCSFD.delHTMLtags(movie_info["plot"]["text"] + '\n(' + movie_info["plot"]["source_name"] + ')' )
			except:
				try:
					# we try to get plot from serie (if available)
					movie_info = self.json_data["root_info"]
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
		
		movie_info = self.json_data["info"]
		
		if "releases" in movie_info:
			release_types = [
				( 'cinema', _("V kinech:") ),
				( 'dvd', _("Na DVD:") ),
				( 'bluray', _("Na blu-ray:") ),
				( 'tv', _("V televizi:") ),
				( 'internet', _("Na internetu:") ),
			]
			
			for release_type in release_types:
				if release_type[0] in movie_info["releases"]:
					text += release_type[1] + "\n"
					for release in movie_info["releases"][release_type[0]]:
						release_date = release["release_date"]
						# convert 2022-02-15 -> 15.02.2022
						release_date = release_date[8:10] + '.' + release_date[5:7] + '.' + release_date[0:4]
						country = CheckValidValue( release["country"] )
						distributor = CheckValidValue( release["distributor"] )
						text += country + ' \t' + release_date + "   " + distributor + '\n'
					
					text += '\n'

		LogCSFD.WriteToFile('[CSFD] parserPremiere - konec\n')
		return text

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

	def parserVideoDetail(self, json_data=None, video_resolution='', image_resolution=''):
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - 0a\n')

		searchresults = None
		
		if json_data == None:
			json_data = self.json_data
		
		if len( json_data["videos"] ) > 0:
			searchresults = []
			
			quality = ( '1080', '720', '480', '360' )
			try:
				# update max available quality based on settings
				quality = quality[quality.index(video_resolution):]
			except:
				pass
			
			for video in json_data["videos"]:
				
				video_url = None
				for q in quality:
					if q in video["video"]:
						video_url= video["video"][q]
						break
				
				if video_url == None:
					continue

				try:
					videotitulkyurlCZ = video["subtitles"]["české".decode('utf-8')]
				except:
					videotitulkyurlCZ = ''

				try:
					videotitulkyurlSK = video["subtitles"]["slovenské".decode('utf-8')]
				except:
					videotitulkyurlSK = ''
					
				videoDescr = video["description"]
				videoPoster = video["preview_image"]["url"]
				
				videoPoster = self.getUrlByImageResolution(videoPoster, image_resolution)
					
				searchresults.append( (video_url, videotitulkyurlCZ, videotitulkyurlSK, videoDescr, videoPoster) )

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
			ss_date_rating = ''
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
			
		if self.parserRatingAllowed() == False:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - ownrating - NE\n')
			searchresults.append('ownrating')
			
		if int(self.json_data["info"]["summary"]["related_films_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - souvisejici - NE\n')
			searchresults.append('souvisejici')
			
		if int(self.json_data["info"]["summary"]["similar_films_count"]) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - podobne - NE\n')
			searchresults.append('podobne')

		if 'has_no_seasons' not in self.json_data["info"] or self.json_data["info"]["has_no_seasons"] == True:		
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - serie - NE\n')
			searchresults.append('serie')
			
		if self.json_data["info"]["type_id"] != 10 and self.json_data["info"]["type_id"] != 12:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - epizody - NE\n')
			searchresults.append('epizody')
			
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - konec\n')
		return searchresults
	
	def parserListOfTVMovies(self, json_data=None, deleteDuplicity=False):
		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - zacatek\n')
		searchresults = []

		if json_data == None:
			json_data = self.json_data

		for station in json_data["stations"]:
			LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - parsing %s\n' % station['name'])
			
			for schedule in station['schedule']:
				movie = schedule['film']
				if movie['id'] != None:
					c = CheckValidValue(movie['rating_category'], "0")
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

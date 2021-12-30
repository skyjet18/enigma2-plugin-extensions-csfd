# -*- coding: utf-8 -*-

from CSFDLog import LogCSFD
from CSFDTools import char2Allowchar, strUni, ExtractNumbers, isBigCharInFirst, char2Diacritic
from CSFDSettings2 import const_csfd_http_film
from CSFDSettings1 import CSFDGlobalVar
from datetime import datetime
import re, traceback, htmlentitydefs
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
correction_const10 = [
 (
  ',', ' '), (';', ' '), (':', ' '), ('-', ' '), ('"', ' '), ("'", ' '), ('(', ' '), (')', ' '), ('\\[', ' '), ('\\]', ' '), ('.', ' '), ('?', ' '), ('!', ' '), ('&', ' '), ('	  ', ' '), ('  ', ' ')]
TV_stations_delete_const = [
 ' (Preladte)', ' Preladte', ' (Czech/Slovak)', ' Czech/Slovak', ' CZECH-SLOVAK', ' (Hungary/Czech)', ' Hungary/Czech', ' (International)', ' International', ' (Czechia)', ' Czechia', ' (Central Europe)', ' Central Europe', ' (Eastern Europe)', ' Eastern Europe', ' (Europe)', ' Europe', ' (Czech)', ' Czech', ' - Czech', ' CEE', ' INT', ' (CE)', ' CE', ' JM', ' SM', ' CZE', ' CZ', ' BG', ' | T2', ' +1']
typeOfMovie = [
 (
  '(video film)', _('Video film')), ('(TV film)', _('TV film')), ('(TV seriál)', _('TV seriál')), ('(TV pořad)', _('TV pořad')), ('(divadelní záznam)', _('Divadelní záznam')), ('(koncert)', _('Koncert')), ('(studentský film)', _('Studentský film')), ('(amatérský film)', _('Amatérský film')), ('(hudební videoklip)', _('Hudební videoklip')), ('(série)', _('Seriál - série')), ('(epizoda)', _('Seriál - epizoda'))]
TV_stations_menu_const = [
 (
  '1', 'HBO'), ('1', 'HBO HD'),
 (
  '2', 'Nova'), ('2', 'Nova HD'), ('2', 'TV Nova'), ('2', 'TV Nova HD'), ('2', 'Nova TV'), ('2', 'Nova TV HD'),
 (
  '3', 'Prima'), ('3', 'Prima TV'), ('3', 'Prima TV HD'), ('3', 'Prima HD'), ('3', 'TV Prima'), ('3', 'TV Prima HD'), ('3', 'FTV Prima'), ('3', 'FTV Prima HD'),
 (
  '3', 'Prima Family'), ('3', 'Prima Family HD'),
 (
  '4', 'ČT1'), ('4', 'ČT 1'),
 (
  '4', 'ČT1 HD'), ('4', 'ČT 1 HD'), ('4', 'CT 1 HD new'), ('4', 'ČT HD'),
 (
  '5', 'ČT2'), ('5', 'ČT 2'),
 (
  '5', 'ČT2 HD'), ('5', 'ČT 2 HD'), ('5', 'CT 2 HD new'),
 (
  '6', 'Markíza'), ('6', 'Markíza HD'), ('6', 'TV Markíza'), ('6', 'TV Markíza HD'), ('6', 'Markíza TV'), ('6', 'Markíza TV HD'),
 (
  '6', 'Markíza'), ('6', 'Markíza HD'), ('6', 'TV Markíza'), ('6', 'TV Markíza HD'), ('6', 'Markíza TV'), ('6', 'Markíza TV HD'),
 (
  '7', 'JOJ'), ('7', 'JOJ HD'), ('7', 'TV JOJ'), ('7', 'TV JOJ HD'), ('7', 'JOJ TV'), ('7', 'JOJ TV HD'),
 (
  '8', 'HBO2'), ('8', 'HBO 2'), ('8', 'HBO2 HD'), ('8', 'HBO 2 HD'),
 (
  '9', 'Jednotka'), ('9', 'STV1'), ('9', 'STV 1'),
 (
  '9', 'JEDNOTKA HD'), ('9', 'STV1 HD'), ('9', 'STV 1 HD'), ('9', 'STV HD'),
 (
  '10', 'Dvojka'), ('10', 'STV2'), ('10', 'STV 2'),
 (
  '10', 'Dvojka HD'), ('10', 'STV2 HD'), ('10', 'STV 2 HD'),
 (
  '12', 'AXN'), ('12', 'AXN HD'), ('12', 'AXN CS'),
 (
  '13', 'Cinemax'), ('13', 'Cinemax 1'), ('13', 'Cinemax HD'), ('13', 'Cinemax 1 HD'),
 (
  '14', 'FilmBox'),
 (
  '15', 'Film+'), ('15', 'Film +'), ('15', 'FilmPlus'), ('15', 'Film Plus'), ('15', 'Minimax/FilmPlus'),
 (
  '16', 'CSfilm'), ('16', 'CS Film'), ('16', 'CS Mini/CS Film/Horor Film'), ('16', 'CS Film/CS Mini'), ('16', 'CSFilm/CSMini'),
 (
  '17', 'MGM'), ('17', 'MGM HD'),
 (
  '18', 'HBO Comedy'), ('18', 'HBO Comedy HD'),
 (
  '19', 'Nova Cinema'), ('19', 'Nova Cinema HD'),
 (
  '20', 'FilmBox Plus'), ('20', 'FilmBox+'),
 (
  '22', 'Cinemax2'), ('22', 'Cinemax 2'), ('22', 'Cinemax2 HD'), ('22', 'Cinemax 2 HD'),
 (
  '24', 'Barrandov'), ('24', 'TV Barrandov'), ('24', 'Barrandov HD'), ('24', 'TV Barrandov HD'),
 (
  '25', 'Plus'), ('25', 'Plus HD'), ('25', 'JOJ Plus'), ('25', 'JOJ Plus HD'),
 (
  '26', 'Prima Cool'), ('26', 'Prima Cool HD'),
 (
  '27', 'Doma'), ('27', 'Doma HD'), ('27', 'TV Doma'), ('27', 'TV Doma HD'), ('27', 'Doma TV'), ('27', 'Doma TV HD'),
 (
  '28', 'Universal Channel'), ('28', 'Universal'), ('28', 'UNI CZSK'),
 (
  '30', 'Disney Channel'),
 (
  '31', 'Kino CS'), ('31', 'KinoCS'),
 (
  '32', 'Doku CS'),
 (
  '33', 'Prima Love'), ('33', 'Prima Love HD'),
 (
  '34', 'Minimax'), ('34', 'Minimax/Animax'), ('34', 'Minimax / Animax'), ('34', 'Minimax/FilmPlus'),
 (
  '37', 'Discovery Channel'), ('37', 'Discovery Channel HD'), ('37', 'Discovery'), ('37', 'Discovery HD'),
 (
  '38', 'History Channel'), ('38', 'History Chnl'), ('38', 'History channel'), ('38', 'History'), ('38', 'History Channel HD'), ('38', 'History Chnl HD'), ('38', 'History channel HD'), ('38', 'History HD'),
 (
  '39', 'Spektrum'), ('39', 'Spektrum HD'),
 (
  '40', 'Animal Planet'), ('40', 'Animal Planet HD'),
 (
  '41', 'Filmbox Family'), ('41', 'FilmBox Family'),
 (
  '42', 'Viasat Nature'),
 (
  '43', 'Viasat Explorer'), ('43', 'Viasat Explorer / Spice'), ('43', 'Viasat Explorer/Spice'),
 (
  '44', 'Viasat History'),
 (
  '45', 'Viasat HD'),
 (
  '46', 'Film Europe Channel'),
 (
  '48', 'Fanda'), ('48', 'Fanda HD'), ('48', 'Fanda TV'), ('48', 'Fanda TV HD'),
 (
  '49', 'Animax'), ('49', 'Minimax/Animax'), ('49', 'Minimax / Animax'),
 (
  '50', 'Discovery Science'), ('50', 'Discovery Science Channel'),
 (
  '51', 'Discovery World'), ('51', 'Discovery World Channel'),
 (
  '52', 'JimJam'), ('52', 'Jim Jam'),
 (
  '53', 'Spektrum Home'),
 (
  '54', 'Dajto'), ('54', 'Dajto HD'), ('54', 'TV Dajto'), ('54', 'TV Dajto HD'),
 (
  '55', 'National Geographic'), ('55', 'Nat Geo'), ('55', 'NatGeo'),
 (
  '56', 'National Geographic Wild'), ('56', 'Nat Geo Wild'), ('56', 'NatGeo Wild'), ('56', 'National Geographic Wild HD'), ('56', 'Nat Geo Wild HD'), ('56', 'NatGeo Wild HD'),
 (
  '57', 'CBS Drama'),
 (
  '58', 'Smíchov'), ('58', 'Smíchov HD'),
 (
  '60', 'Prima Zoom'), ('60', 'Prima Zoom HD'),
 (
  '61', 'Telka'),
 (
  '63', 'Wau'), ('63', 'Wau HD'),
 (
  '64', 'ČT :D'), ('64', 'ČT:D'), ('64', 'CT:D / CT art'), ('64', 'CT:D/CT art'),
 (
  '65', 'ČT art'), ('65', 'ČTart'), ('65', 'CT:D / CT art'), ('65', 'CT:D/CT art'),
 (
  '66', 'AXN Black'),
 (
  '67', 'AXN White'),
 (
  '68', 'Megamax'),
 (
  '69', 'CBS Reality'),
 (
  '70', 'Horor Film'), ('70', 'CS Mini/CS Film/Horor Film'),
 (
  '71', 'National Geographic HD'), ('71', 'Nat Geo HD'), ('71', 'NatGeo HD'),
 (
  '72', 'Travel Channel'), ('72', 'Travel Channel HD'),
 (
  '73', 'Nickelodeon'), ('73', 'Nickelodeon HD'),
 (
  '74', 'MTV CZ'), ('74', 'MTV'),
 (
  '75', 'Filmbox Extra'), ('75', 'FilmBox Extra'),
 (
  '76', 'Kino Svět'),
 (
  '77', 'ID Xtra'),
 (
  '78', 'AMC'),
 (
  '79', 'Filmbox Premium'),
 (
  '80', 'RiK'), ('80', 'TV RiK'), ('80', 'RiK TV'),
 (
  '81', 'Relax-Pohoda'), ('81', 'RELAX Pohoda'), ('81', 'RELAX - Pohoda'),
 (
  '82', 'Rebel'),
 (
  '83', 'Kino Barrandov'), ('83', 'KinoBarrandov'),
 (
  '84', 'Barrandov Plus'), ('84', 'TV Barrandov Plus'), ('84', 'Barrandov Plus HD'), ('84', 'TV Barrandov Plus HD'), ('84', 'BARRANDOV PLUS TV'),
 (
  '85', 'Discovery HD Showcase'), ('85', 'Discovery Showcase HD'),
 (
  '86', 'JOJ Cinema'), ('86', 'JOJ Cinema HD'),
 (
  '87', 'FilmBox Extra HD'),
 (
  '88', 'Prima Max'),
 (
  '89', 'Comedy Central Extra'),
 (
  '90', 'Prima Comedy Central'), ('90', 'Prima Comedy'),
 (
  '91', 'Nova International'),
 (
  '92', 'Markíza International'),
 (
  '93', 'HBO3'),
 (
  '94', 'RTL'),
 (
  '95', 'Sat.1'),
 (
  '96', 'PRO7'),
 (
  '97', 'Kabel1'),
 (
  '98', 'RTL 2'),
 (
  '99', 'VOX'),
 (
  '100', 'RTL Nitro'),
 (
  '101', 'Super RTL'),
 (
  '102', 'TELE 5'),
 (
  '103', 'Sixx'),
 (
  '104', 'ProSieben MAXX'),
 (
  '105', 'ORF 1'),
 (
  '106', 'ORF 2'),
 (
  '107', 'Das Erste'),
 (
  '108', 'Discovery Turbo Xtra'),
 (
  '109', 'ZDF'),
 (
  '110', 'ZDF Neo'),
 (
  '111', 'TLC'),
 (
  '112', 'KiKa'),
 (
  '113', '3Sat'),
 (
  '114', 'E! Entertainment'),
 (
  '115', 'arte'),
 (
  '116', 'RTL plus'),
 (
  '117', 'JOJ Family'),
 (
  '118', 'Sat.1 Gold'), ('118', 'Sat1 Gold'), ('118', 'Sat 1 Gold'),
 (
  '119', 'Kabel Eins Doku'),
 (
  '120', 'Československo HD'), ('120', 'Ceskoslovensko HD'), ('120', 'Československo'), ('120', 'Ceskoslovensko'),
 (
  '121', 'Festival HD'),
 (
  '122', 'Barrandov Family'),
 (
  '123', 'Nova Action'),
 (
  '124', 'Nova Gold'),
 (
  '125', 'Nova 2'), ('125', 'Nova2'),
 (
  '126', 'Prima Plus')]

def GetCSFDNumberFromChannel(nameChannel=''):
	results = []
	if isinstance(nameChannel, str):
		nameChannel = unicode(nameChannel, 'utf-8')
	nameChannel = nameChannel.strip()
	for dodat in TV_stations_delete_const:
		vv = -1 * len(dodat)
		if nameChannel[vv:] == dodat:
			nameChannel = nameChannel[:vv].strip()

	nameChannelP = char2Diacritic(nameChannel).upper()
	for ch, name in TV_stations_menu_const:
		if char2Diacritic(name).upper() == nameChannelP:
			if ch not in results:
				results.append(ch)

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


def NameMovieCorrectionExtensionsTwoNames(name1=''):
	sss = name1[-7:]
	res_rok = re.findall(' \\(19\\d{2}\\)| \\(20\\d{2}\\)| \\(21\\d{2}\\)', sss)
	if res_rok is not None and len(res_rok) == 1:
		rok = res_rok[0]
		name1 = name1[:-7]
	else:
		rok = ''
	seznam = name1.split(' / ', 1)
	if len(seznam) > 1:
		newname = seznam[0].strip() + ' / ' + NameMovieCorrectionExtensions(seznam[1])
	else:
		newname = NameMovieCorrectionExtensions(seznam[0].strip())
	newname += rok
	return newname


class CSFDConstParser():

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDConstParser - init - zacatek\n')
		self.ccFindCond = re.DOTALL | re.IGNORECASE
		self.parserhtmltags = re.compile('<.*?>')
		self.parserHTML2utf8_1 = re.compile('&([^#][A-Za-z]{1,5}?);')
		self.parserHTML2utf8_2 = re.compile('&#x([0-9A-Fa-f]{2,2}?);')
		self.parserHTML2utf8_3 = re.compile('&#(\\d{1,5}?);')
		self.parserYear = re.compile('19\\d{2}|20\\d{2}|21\\d{2}', re.DOTALL)
		self.parserDate = re.compile('\\d{2}\\.\\d{2}\\.\\d{4}', re.DOTALL)
		self.parserNumbers = re.compile(' \\d+', re.DOTALL)
		self.parserRomanNumerals = re.compile('\\b(?!LLC)(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.DOTALL)
		self.parserTestHTMLSearchMask = re.compile('html', self.ccFindCond)
		self.parserTestCSFDFindingSearchMask = re.compile('SFD.cz', self.ccFindCond)
		self.parserMoviesFoundSearchMask1 = re.compile('<h3 class="header">Fanklub filmu</h3>', self.ccFindCond)
		self.parserMoviesFoundLimitMask2 = re.compile('<h2 class="header">Filmy</h2>(.*?)<div class="footer">', self.ccFindCond)
		self.parserMoviesFoundSearchMask2 = re.compile('<li>(.*?)</li>', self.ccFindCond)
		self.parserListOfMoviesLimitMask1 = re.compile('<h2 class="header">Filmy</h2>(.*?)</ul>', self.ccFindCond)
		self.parserListOfMoviesSearchMask1 = re.compile('<h3 class="subject.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)</a>(.*?)<p>(.*?)</p>', self.ccFindCond)
		self.parserListOfMoviesLimitMask2 = re.compile('class="films others">(.*?)</ul>', self.ccFindCond)
		self.parserListOfMoviesSearchMask2 = re.compile('<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year".*?>(.*?)</span>(.*?)</li>', self.ccFindCond)
		self.parserListOfMoviesSearchMask1a = re.compile('class="search-name">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserListOfMainMoviesLimitMask = re.compile('<h2 class="header">Filmy</h2>(.*?)</ul>', self.ccFindCond)
		self.parserListOfMainMoviesSearchMask = re.compile('<li>.*?<img src="(.*?)".*?<h3 class="subject.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)</a>(.*?)<p>(.*?)</p>(.*?)</p>.*?</li>', self.ccFindCond)
		self.parserListOfMainMoviesSearchMask1a = re.compile('class="search-name">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserListOfMoviesRedirectMask1 = re.compile('<p class="genre">.*?<a href="/film/(.*?/)', self.ccFindCond)
		self.parserListOfMoviesRedirectMask2 = re.compile('<p class="origin">.*?<a href="/film/(.*?/)', self.ccFindCond)
		self.parserListOfMoviesRedirectMaskUrl = re.compile('<link rel="canonical" href="https://www.csfd.cz/film/(.*?/).*?"', self.ccFindCond)
		self.parserCurrentPageUrlSearchMask = re.compile('<link rel="canonical" href="(https://www.csfd.cz/film/.*?)"', self.ccFindCond)
		self.parserRedirectPageMask = re.compile(">location.replace.*?/film/(.*?/)'", self.ccFindCond)
		self.parserHiddenContentMask = re.compile('<br>Obsah:.*?font-weight:normal\'>.*?<a href=.*?(text=.*?)".*?</div>.*?</span></span>', self.ccFindCond)
		self.parserListOfRelatedMoviesLimitMask = re.compile('<h3 class="header">Souvisej.*?</h3>.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserListOfRelatedMoviesSearchMask = re.compile('<li>.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year".*?>(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserListOfSimilarMoviesLimitMask = re.compile('<h3 class="header">Podobn.*?</h3>.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserListOfSimilarMoviesSearchMask = re.compile('<li>.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year".*?>(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserListOfSeriesLimitMask = re.compile('<div class="header">.*?<h3>.*?S.*?rie.*?</h3>.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserListOfSeriesSearchMask = re.compile('<li>.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year">(.*?)</span>.*?<span>(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserListOfEpisodesLimitMask = re.compile('<div class="header">.*?<h3>.*?Epizody.*?</h3>.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserListOfEpisodesSearchMask1 = re.compile('<li>.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-position">(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserListOfEpisodesSearchMask2 = re.compile('<li>.*?<a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year">(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserRatingMask = re.compile('<div id="rating".*?average">(.*?)<', self.ccFindCond)
		self.parserMovieTitelInclYearMask1 = re.compile('<title>(.*?)\\|.*?SFD.cz</title>', self.ccFindCond)
		self.parserMovieTitelInclYearMask2 = re.compile('<title>(.*?)\\|.*?</title>', self.ccFindCond)
		self.parserMovieTitelMask = re.compile('<div class="info">.*?<h1.*?>(.*?)</h1>', re.DOTALL)
		self.parserSeriesNameTitelLimitMask = re.compile('<div class=".*?series-navigation">(.*?)</div>', re.DOTALL)
		self.parserSeriesNameTitelMask1 = re.compile('<a href="/film/(.*?)/">(.*?)</a>.*?<a href="/film/(.*?)/">(.*?)<', re.DOTALL)
		self.parserSeriesNameTitelMask2 = re.compile('<a href="/film/(.*?)/">(.*?)</a>', re.DOTALL)
		self.parserTypeOfMovieMask = re.compile('<div class="info">.*?<h1.*?class="film-type">(.*?)<', re.DOTALL)
		self.parserOtherMovieTitelLimitMask = re.compile('<ul class="names">(.*?)</ul>', self.ccFindCond)
		self.parserOtherMovieTitelSearchMask = re.compile('<li>.*?alt="(.*?)".*?<h3>(.*?)</h3>.*?</li>', self.ccFindCond)
		self.parserOtherMovieTitelWOCountryLimitMask = re.compile('<ul class="names">(.*?)</ul>', self.ccFindCond)
		self.parserOtherMovieTitelWOCountrySearchMask = re.compile('<li>.*?<h3>(.*?)</h3>.*?</li>', self.ccFindCond)
		self.parserMainPosterUrlMask = re.compile('<img src="(//img.csfd.cz/files/images/film/posters/.*?|//img.csfd.cz/posters/.*?)\\?.*?"', self.ccFindCond)
		self.parserAllPostersUrlLimitMask = re.compile('<h3>Plak.*?ty</h3>(.*?)</table>', self.ccFindCond)
		self.parserAllPostersUrlSearchMask = re.compile('style="background-image\\: url\\(\'(.*?)\\?.*?\'\\)\\;', self.ccFindCond)
		self.parserPostersNumberLimitMask = re.compile('<h3>Plak.*?ty</h3>(.*?)</table>', self.ccFindCond)
		self.parserPostersNumberSearchMask = re.compile('style="background-image\\: url\\(\'(.*?)\\?.*?\'\\)\\;', self.ccFindCond)
		self.parserGenreMask = re.compile('<p class="genre">(.*?)<', re.DOTALL)
		self.parserOriginMask = re.compile('<p class="origin">(.*?)</p>', re.DOTALL)
		self.parserCSFDRankingsLimitMask = re.compile('<div id="rating"(.*?)</div>', self.ccFindCond)
		self.parserCSFDRankingsSearchMask = re.compile('href="/zebricky/.*?">(.*?)<', self.ccFindCond)
		self.parserWherePlayingLimitMask = re.compile('<ul class="relations">(.*?)</ul>', self.ccFindCond)
		self.parserWherePlayingSearchMask = re.compile('href=".*?>(.*?)<', self.ccFindCond)
		self.parserDirectorLimitMask = re.compile('<h4>Re.*?ie:</h4>(.*?)</div>', self.ccFindCond)
		self.parserDirectorSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserMusicLimitMask = re.compile('<h4>Hudba:</h4>(.*?)</div>', self.ccFindCond)
		self.parserMusicSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserDraftLimitMask = re.compile('<h4>P.*?edloha:</h4>(.*?)</div>', self.ccFindCond)
		self.parserDraftSearchMask1 = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserDraftSearchMask2 = re.compile('</a>.*?\\((.*?)\\).*?</span>', self.ccFindCond)
		self.parserScenarioLimitMask = re.compile('<h4>Sc.*?n.*?:</h4>(.*?)</div>', self.ccFindCond)
		self.parserScenarioSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserCameraLimitMask = re.compile('<h4>Kamera:</h4>(.*?)</div>', self.ccFindCond)
		self.parserCameraSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserProductionLimitMask = re.compile('<h4>Producenti:</h4>(.*?)</div>', self.ccFindCond)
		self.parserProductionSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserCuttingLimitMask = re.compile('<h4>St.*?ih:</h4>(.*?)</div>', self.ccFindCond)
		self.parserCuttingSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserSoundLimitMask = re.compile('<h4>Zvuk:</h4>(.*?)</div>', self.ccFindCond)
		self.parserSoundSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserScenographyLimitMask = re.compile('<h4>Sc.*?nografie:</h4>(.*?)</div>', self.ccFindCond)
		self.parserScenographySearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserMakeUpLimitMask = re.compile('<h4>Masky:</h4>(.*?)</div>', self.ccFindCond)
		self.parserMakeUpSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserCostumesLimitMask = re.compile('<h4>Kost.*?my:</h4>(.*?)</div>', self.ccFindCond)
		self.parserCostumesSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserCastingLimitMask = re.compile('<h4>Hraj.*?:</h4>(.*?)</div>', self.ccFindCond)
		self.parserCastingSearchMask = re.compile('href="/tvurce/.*?>(.*?)<', self.ccFindCond)
		self.parserTagsLimitMask = re.compile('<div class="ct-related tags">.*?(<a href.*?)</div>', self.ccFindCond)
		self.parserTagsSearchMask = re.compile('href="/.*?>(.*?)</a>', self.ccFindCond)
		self.parserContentLimitMask = re.compile('<div class="header">.*?<h3>Obsah.*?</h3>.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserContentSearchMask = re.compile('<li>(.*?)</li>', self.ccFindCond)
		self.parserIMDBlinkMask = re.compile('<div id="share">.*?<ul class="links">.*?<a href="(https?\\:\\/\\/www\\.imdb.*?)".*?</ul>', re.DOTALL)
		self.parserIMDBidkMask = re.compile('<div id="share">.*?<ul class="links">.*?<a href="https?\\:\\/\\/www\\.imdb\\.com\\/title\\/(.*?)\\/combined.*?</ul>', re.DOTALL)
		self.parserRatingNumberMask = re.compile('<a id="rating-count-link".*?<br>(.*?)</', re.DOTALL)
		self.parserRatingNumberLimitMask = re.compile('<div id="ratings" class=(.*?)</ul>', self.ccFindCond)
		self.parserRatingNumberSearchMask = re.compile('<a href=.*?">(.*?)<.*?<div class="clear">', self.ccFindCond)
		self.parserUserCommentsLimitMask = re.compile('<ul class="ui-posts-list"(.*?)</ul>', self.ccFindCond)
		self.parserUserCommentsSearchMask = re.compile('<li id.*?<h5 class="author"><a href=.*?">(.*?)<(.*?)class="post">(.*?)<span.*?date desc">(.*?)<.*?</li>', self.ccFindCond)
		self.parserUserCommentsNumberMask = re.compile('<div class="header">.*?<h2>Koment.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserUserExtReviewsLimitMask = re.compile('<ul class="ui-posts-list">(.*?)</ul>', self.ccFindCond)
		self.parserUserExtReviewsSearchMask = re.compile('<li .*?<h4 class="author">(.*?)</h4>.*?<p>(.*?)</li>', self.ccFindCond)
		self.parserUserExtReviewsNumberMask = re.compile('<h2 class="header">Extern.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserUserDiscussionMask = re.compile('<li class="date">(.*?)</li>.*?h5 class="author"><a href=.*?">(.*?)<.*?<div>(.*?)</div>', self.ccFindCond)
		self.parserUserDiscussionNumberMask = re.compile('<div class="header">.*?<h2>Diskuze.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserInterestLimitMask = re.compile('<h2 class="header">.*?<ul class="ui-posts-list">(.*?)</ul>', self.ccFindCond)
		self.parserInterestSearchMask1 = re.compile('<li.*?<h5>(.*?)</h5>.*?</span></span>(.*?)<span class="author">(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserInterestSearchMask2 = re.compile('<li id="trivia.*?</span></span>(.*?)<span class="author">(.*?)</span>.*?</li>', self.ccFindCond)
		self.parserInterestTypesAndNumbersLimitMask = re.compile('<h2 class="header">.*?<div class="navigation">(.*?)</ul>', self.ccFindCond)
		self.parserInterestTypesAndNumbersSearchMask = re.compile('<li.*?<a href="(.*?)"><span>(.*?)</span>.*?"item-info">(.*?)<.*?</li>', self.ccFindCond)
		self.parserInterestSelectedTypeAndNumberLimitMask = re.compile('<h2 class="header">.*?<div class="navigation">(.*?)</ul>', self.ccFindCond)
		self.parserInterestSelectedTypeAndNumberSearchMask = re.compile('<li class="selected.*?<a href="(.*?)"><span>(.*?)</span>.*?"item-info">(.*?)<.*?</li>', self.ccFindCond)
		self.parserInterestNumberMask = re.compile('<h2 class="header">.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserUserRatingLimitMask = re.compile('<div id="ratings" class=(.*?)</ul>', self.ccFindCond)
		self.parserUserRatingSearchMask = re.compile('<a href=.*?">(.*?)<(.*?)<div class="clear">', self.ccFindCond)
		self.parserPremiereLimitMask = re.compile('<h3 class="header">Premi.*?ry.*?</h3>(.*?)</table>', self.ccFindCond)
		self.parserPremiereSearchMask = re.compile('(<tr.*?)</tr>', self.ccFindCond)
		self.parserAccessibilitySearchMask = re.compile('<p class="classification">(.*?)</p>', self.ccFindCond)
		self.parserAwardsLimitMask = re.compile('<h2 class="header">Ocen.*?</h2>(.*?)<div class="footer">', self.ccFindCond)
		self.parserAwardsSearchMask1 = re.compile('<h3>(.*?)</h3>.*?<ul class="awards-list">(.*?)</ul>', self.ccFindCond)
		self.parserAwardsSearchMask2 = re.compile('<li class="(.*?)">(.*?)</li>', self.ccFindCond)
		self.parserUserFansLimitMask = re.compile('<div id="fanclub" class=(.*?)<div class="clear">', self.ccFindCond)
		self.parserUserFansSearchMask = re.compile('<a href=.*?">(.*?)<', self.ccFindCond)
		self.parserUserFansNumberMask = re.compile('<a id="fanclub-count-link".*?>\\((.*?)\\).*?</', self.ccFindCond)
		self.parserUserFansNumberLimitMask = re.compile('<div id="fanclub" class=(.*?)<div class="clear">', self.ccFindCond)
		self.parserUserFansNumberSearchMask = re.compile('<a href=.*?">(.*?)<', self.ccFindCond)
		self.parserVideoListNextPageLimitMask = re.compile('<div class="paginator text">(.*?)</div>', self.ccFindCond)
		self.parserVideoListNextPageSearchMask = re.compile('<a class="next" href="(.*?)">', self.ccFindCond)
		self.parserVideoTypeListLimitMask = re.compile('<div class="header">.*?<h2>Vide.*?<span class="count">.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserVideoTypeListSearchMask = re.compile('<li.*?<a href="(.*?)"><span>(.*?)<.*?"item-info">(.*?)</.*?</li>', self.ccFindCond)
		self.parserVideoNumberMask = re.compile('<div class="header">.*?<h2>Vide.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserVideoDetailLimitMask = re.compile('<div class="ui-video-player">(.*?)</li>', self.ccFindCond)
		self.parserVideoDetailSearchMask = re.compile('playlist.addClip\\((.*?)\\)\\;', self.ccFindCond)
		self.parserVideoDetailClipListSearchMask = re.compile('\\{"src"\\:"(.*?)","type"\\:"video(.*?)","quality"\\:"(.*?)".*?\\}', self.ccFindCond)
		self.parserVideoDetailSubtListSearchMask = re.compile('\\}\\],.*?\\{"src"\\:"(.*?srt)","type"\\:"text.*?","lang"\\:"(.*?)","label"\\:"(.*?)"\\}', self.ccFindCond)
		self.parserVideoDetailFlagSearchMask = re.compile('<img class="flag" src="(.*?)"', self.ccFindCond)
		self.parserVideoDetailDurationSearchMask = re.compile('<span class="duration">(.*?)</span>', self.ccFindCond)
		self.parserVideoDetailDescrSearchMask = re.compile('<div class="description.*?">(.*?)</div>', self.ccFindCond)
		self.parserVideoDetailPosterSearchMask = re.compile('poster="(.*?)\\?.*?"', self.ccFindCond)
		self.parserGalleryNumberMask = re.compile('<h2 class="header">.*?<span class="count">\\((.*?)\\)</span>', self.ccFindCond)
		self.parserGalleryTypeListLimitMask = re.compile('<h2 class="header">.*?<span class="count">.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserGalleryTypeListSearchMask = re.compile('<li.*?<a href="(.*?)"><span>(.*?)<.*?"item-info">(.*?)</.*?</li>', self.ccFindCond)
		self.parserGallerySelectedTypeListLimitMask = re.compile('<h2 class="header">.*?<span class="count">.*?<ul>(.*?)</ul>', self.ccFindCond)
		self.parserGallerySelectedTypeListSearchMask = re.compile('<li class="selected.*?<a href="(.*?)"><span>(.*?)<.*?"item-info">(.*?)</.*?</li>', self.ccFindCond)
		self.parserGalleryListLimitMask = re.compile('</div><h2 class="header">.*?Galerie.*?<ul>.*?(<li>.*?class="photo".*?)</ul>', self.ccFindCond)
		self.parserGalleryListSearchMask1 = re.compile('<li>.*?class="photo".*?background-image\\: url\\(\'(.*?)\\?.*?\'\\)\\;.*?<p class="creators">(.*?)</li>', self.ccFindCond)
		self.parserGalleryListSearchMask2 = re.compile('<a href=".*?">(.*?)</a>', self.ccFindCond)
		self.parserGalleryListNextPageLimitMask = re.compile('<div class="paginator text">(.*?)</div>', self.ccFindCond)
		self.parserGalleryListNextPageSearchMask = re.compile('<a class="next" href="(.*?)">', self.ccFindCond)
		self.parserOwnRatingLimitMask = re.compile('<div id="my-rating" class(.*?)</form>', self.ccFindCond)
		self.parserOwnRatingSearchMask = re.compile(' selected>(.*?)</option>', self.ccFindCond)
		self.parserDateOwnRatingLimitMask = re.compile('<div id="my-rating" class(.*?)</form>', self.ccFindCond)
		self.parserDateOwnRatingSearchMask = re.compile('<span class="my-rating"><span title="(.*?)">', self.ccFindCond)
		self.parserLoggedUserLimitMask = re.compile('<div id="user-menu" class="logged">(.*?)</div>', self.ccFindCond)
		self.parserLoggedUserSearchMask = re.compile('<h3><a href=".*?">(.*?)</', self.ccFindCond)
		self.parserFunctionExistsLimitMask = re.compile('<div class="navigation">(.*?)</div>', self.ccFindCond)
		self.parserFunctionExistsSearchMask = re.compile('<li class="(.*?)">.*?</li>', self.ccFindCond)
		self.parserUserIDLoggedUserSearchMask = re.compile('<a href="(?P<url>/uzivatel/[^"]+)', self.ccFindCond)
		self.parserTokenRatingLimitMask = re.compile('<form action.*?id="frm-ratingForm"(.*?)</form>', self.ccFindCond)
		self.parserTokenRatingSearchMask = re.compile('name="_token_" value="(.*?)"', self.ccFindCond)
		self.parserTokenLoginLimitMask = re.compile('<form action.*?prihlaseni(.*?)</form>', self.ccFindCond)
		self.parserTokenLoginSearchMask = re.compile('name="_token_" value="(.*?)"', self.ccFindCond)
		self.parserURLLoginLimitMask = re.compile('<div class="login-wrapper">(.*?)</form>', self.ccFindCond)
		self.parserURLLoginSearchMask = re.compile('<form action="(.*?)"', self.ccFindCond)
		self.parserDeleteRatingUrlLimitMask = re.compile('<div id="my-rating"(.*?)</div>', self.ccFindCond)
		self.parserDeleteRatingUrlSearchMask = re.compile('<div class="controls">.*?<a href="(.*?myRatingDelete)".*?title="smazat', self.ccFindCond)
		self.parserListOfTVMoviesLimitMask = re.compile('<div id="box-(.*?)<div class="clear">', self.ccFindCond)
		self.parserListOfTVMoviesSearchMask = re.compile('<span class="name"><a href="/film/(.*?/)" class="film (.*?)">(.*?)<.*?class="film-year">(.*?)</span>', self.ccFindCond)
		self.parserPrivateCommentLimitMask = re.compile('<h3>Soukrom.*?mka</h3>(.*?)</form>', self.ccFindCond)
		self.parserPrivateCommentSearchMask = re.compile('class="private delete".*?<form action.*?title=".*?">(.*?)</div>', self.ccFindCond)
		LogCSFD.WriteToFile('[CSFD] CSFDConstParser - init - konec\n')


ParserConstCSFD = CSFDConstParser()

class CSFDParser():

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - zacatek\n')
		self.inhtml = ''
		self.inhtml_script = ''
		LogCSFD.WriteToFile('[CSFD] CSFDParser - init - konec\n')

	def parserTestHTML(self, test_code):
		LogCSFD.WriteToFile('[CSFD] parserTestHTML - zacatek\n')
		if test_code is None or test_code == '':
			return True
		if ParserConstCSFD.parserTestHTMLSearchMask.search(test_code) is not None:
			LogCSFD.WriteToFile('[CSFD] parserTestHTML - True\n')
			LogCSFD.WriteToFile('[CSFD] parserTestHTML - konec\n')
			return True
		else:
			LogCSFD.WriteToFile('[CSFD] parserTestHTML - False\n')
			LogCSFD.WriteToFile('[CSFD] parserTestHTML - konec\n')
			return False
			return

	def setParserHTML(self, inhtml):
		LogCSFD.WriteToFile('[CSFD] setParserHTML - zacatek\n')
		if inhtml is None or inhtml == '':
			self.inhtml = ''
		elif self.parserTestHTML(inhtml):
			self.inhtml = inhtml
		elif zlib_exist:
			LogCSFD.WriteToFile('[CSFD] setParserHTML - dekomprese dat do html\n')
			try:
				html = zlib.decompress(inhtml, 16 + zlib.MAX_WBITS)
				if self.parserTestHTML(html):
					LogCSFD.WriteToFile('[CSFD] setParserHTML - dekomprese dat do html - OK\n')
					self.inhtml = html
				else:
					LogCSFD.WriteToFile('[CSFD] setParserHTML - dekomprese dat do html - ERR - chyba\n')
					LogCSFD.WriteToFileWithoutTime(inhtml)
					self.inhtml = ''
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] setParserHTML - dekomprese dat do html - ERR 1 - chyba\n')
				LogCSFD.WriteToFile(err)
				LogCSFD.WriteToFileWithoutTime(inhtml)
				self.inhtml = ''

		else:
			LogCSFD.WriteToFile('[CSFD] setParserHTML - nelze provest dekompresi dat do html - neni knihovna zlib - ERR 2 - chyba\n')
		LogCSFD.WriteToFile('[CSFD] setParserHTML - konec\n')
		return

	def HTML_CSFD_Conversion(self, inhtml):
		LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - zacatek\n')
		if inhtml == '':
			outhtml = ''
		elif self.parserTestHTML(inhtml):
			outhtml = inhtml
		elif zlib_exist:
			LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - dekomprese dat do html\n')
			try:
				html = zlib.decompress(inhtml, 16 + zlib.MAX_WBITS)
				if self.parserTestHTML(html):
					LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - dekomprese dat do html - OK\n')
					outhtml = html
				else:
					LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - dekomprese dat do html - ERR - chyba\n')
					LogCSFD.WriteToFileWithoutTime(inhtml)
					outhtml = ''
			except:
				err = traceback.format_exc()
				LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - dekomprese dat do html - ERR 1 - chyba\n')
				LogCSFD.WriteToFile(err)
				LogCSFD.WriteToFileWithoutTime(inhtml)
				outhtml = ''

		else:
			LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - nelze provest dekompresi dat do html - neni knihovna zlib - ERR 2 - chyba\n')
		LogCSFD.WriteToFile('[CSFD] HTML_CSFD_Conversion - konec\n')
		return outhtml

	def getParserHTML(self):
		return self.inhtml

	def HTML2utf8(self, inhtml):
		if inhtml == '':
			inhtml_script = ''
		else:
			entitydict = {}
			entities1 = ParserConstCSFD.parserHTML2utf8_1.finditer(inhtml)
			if entities1 is not None:
				for x1 in entities1:
					key1 = x1.group(0)
					if key1 not in entitydict:
						try:
							entitydict[key1] = htmlentitydefs.name2codepoint[x1.group(1)]
						except KeyError:
							pass

			entities2 = ParserConstCSFD.parserHTML2utf8_2.finditer(inhtml)
			if entities2 is not None:
				for x2 in entities2:
					key2 = x2.group(0)
					if key2 not in entitydict:
						entitydict[key2] = '%d' % int(key2[3:5], 16)

			entities3 = ParserConstCSFD.parserHTML2utf8_3.finditer(inhtml)
			if entities3 is not None:
				for x3 in entities3:
					key3 = x3.group(0)
					if key3 not in entitydict:
						entitydict[key3] = x3.group(1)

			for key, codepoint in entitydict.items():
				inhtml = inhtml.replace(key, unichr(int(codepoint)).encode('utf8'))

			inhtml_script = inhtml
			inhtml = re.subn('<(script).*?</\\1>(?s)', '', inhtml)[0]
		return (
		 inhtml, inhtml_script)

	def setHTML2utf8(self, inhtml):
		self.setParserHTML(inhtml)
		self.inhtml, self.inhtml_script = self.HTML2utf8(self.inhtml)
		return (
		 self.inhtml, self.inhtml_script)

	def delHTMLtags(self, string):
		return ParserConstCSFD.parserhtmltags.sub('', string)

	def parserGetRomanNumbers(self, name):
		searchresults = []
		results = ParserConstCSFD.parserRomanNumerals.findall(name)
		if results is not None:
			for value in results:
				vysl = value[0] + value[1] + value[2]
				searchresults.append(vysl)

		return searchresults

	def parserGetNumbers(self, name):
		searchresults = []
		results = ParserConstCSFD.parserNumbers.findall(name)
		if results is not None:
			for value in results:
				searchresults.append(value.strip())

		return searchresults

	def parserGetYears(self, name):
		LogCSFD.WriteToFile('[CSFD] parserGetYears - zacatek\n')
		searchresults = []
		results = ParserConstCSFD.parserYear.findall(name)
		if results is not None:
			for value in results:
				searchresults.append(value)

		LogCSFD.WriteToFile('[CSFD] parserGetYears - konec\n')
		return searchresults

	def parserTestCSFDFinding(self):
		LogCSFD.WriteToFile('[CSFD] parserTestCSFDFinding - zacatek\n')
		if ParserConstCSFD.parserTestCSFDFindingSearchMask.search(self.inhtml) is not None:
			LogCSFD.WriteToFile('[CSFD] parserTestCSFDFinding - True - konec\n')
			return True
		else:
			LogCSFD.WriteToFile('[CSFD] parserTestCSFDFinding - False - konec\n')
			return False
			return

	def parserMoviesFound(self):
		LogCSFD.WriteToFile('[CSFD] parserMoviesFound - zacatek\n')
		if ParserConstCSFD.parserMoviesFoundSearchMask1.search(self.inhtml) is not None:
			LogCSFD.WriteToFile('[CSFD] parserMoviesFound - 1 - True - konec\n')
			return True
		else:
			omezitresults = ParserConstCSFD.parserMoviesFoundLimitMask2.search(self.inhtml)
			if omezitresults is not None:
				searchresults = ParserConstCSFD.parserMoviesFoundSearchMask2.search(omezitresults.group(1))
				if searchresults is not None:
					LogCSFD.WriteToFile('[CSFD] parserMoviesFound - 2 - True - konec\n')
					return True
			LogCSFD.WriteToFile('[CSFD] parserMoviesFound - False - konec\n')
			return False

	def parserListOfMovies(self, co_parsovat=0):
		LogCSFD.WriteToFile('[CSFD] parserListOfMovies - zacatek\n')
		searchresults = []
		searchresults1 = []
		searchresults2 = []
		searchresults1a = []
		searchresults2a = []
		omezitresults1 = ParserConstCSFD.parserListOfMoviesLimitMask1.search(self.inhtml)
		if omezitresults1 is not None:
			searchresults1 = ParserConstCSFD.parserListOfMoviesSearchMask1.finditer(omezitresults1.group(1))
		omezitresults2 = ParserConstCSFD.parserListOfMoviesLimitMask2.search(self.inhtml)
		if omezitresults2 is not None:
			searchresults2 = ParserConstCSFD.parserListOfMoviesSearchMask2.finditer(omezitresults2.group(1))
		if co_parsovat == 0 or co_parsovat == 1:
			for x in searchresults1:
				ss = ParserConstCSFD.parserhtmltags.sub('', x.group(5))
				ss = ss[-4:]
				if len(ss) == 4:
					ss = '(' + ss + ')'
				else:
					ss = ''
				searchresults.append((x.group(1), x.group(3), ss, x.group(2)))
				searchresults1a = ParserConstCSFD.parserListOfMoviesSearchMask1a.findall(x.group(4).strip())
				if searchresults1a is not None and len(searchresults1a) > 0:
					searchresults.append((x.group(1), searchresults1a[0].strip(), ss, x.group(2)))

		if co_parsovat == 0 or co_parsovat == 2:
			if searchresults2 is not None:
				for x in searchresults2:
					searchresults.append((x.group(1), x.group(3), x.group(4), x.group(2)))
					searchresults2a = ParserConstCSFD.parserListOfMoviesSearchMask1a.findall(x.group(5).strip())

			if searchresults2a is not None and len(searchresults2a) > 0:
				searchresults.append((x.group(1), searchresults2a[0].strip(), x.group(4), x.group(2)))
		LogCSFD.WriteToFile('[CSFD] parserListOfMovies - konec\n')
		return searchresults

	def parserListOfMainMovies(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfMainMovies - zacatek\n')
		searchresults = []
		searchresults1 = []
		searchresults1a = []
		omezitresults1 = ParserConstCSFD.parserListOfMainMoviesLimitMask.search(self.inhtml)
		if omezitresults1 is not None:
			searchresults1 = ParserConstCSFD.parserListOfMainMoviesSearchMask.finditer(omezitresults1.group(1))
			if searchresults1 is not None:
				for x in searchresults1:
					ss = ParserConstCSFD.parserhtmltags.sub('', x.group(6)).replace('\t', '')
					movie_info = ss.strip() + '\n' + ParserConstCSFD.parserhtmltags.sub('', x.group(7)).replace('\t', '').strip()
					ss = ss[-4:]
					if len(ss) != 4:
						ss = ''
					if x.group(1).find('poster-free') >= 0:
						poster_url = ''
					else:
						poster_url = CSFDGlobalVar.getHTTP() + ':' + x.group(1)
					movie_link = CSFDGlobalVar.getHTTP() + const_csfd_http_film + x.group(2)
					hl_rating = GetItemColourN(x.group(3))
					searchresults.append((movie_link, x.group(4), ss, hl_rating, movie_info, poster_url))
					searchresults1a = ParserConstCSFD.parserListOfMainMoviesSearchMask1a.findall(x.group(5).strip())
					if searchresults1a is not None and len(searchresults1a) > 0:
						searchresults.append((movie_link, searchresults1a[0].strip(), ss, hl_rating, movie_info, poster_url))

		elif ParserConstCSFD.parserMoviesFoundSearchMask1.search(self.inhtml) is not None:
			pass
		LogCSFD.WriteToFile('[CSFD] parserListOfMainMovies - konec\n')
		return searchresults

	def parserListOfMoviesRedirect(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfMoviesRedirect - zacatek\n')
		redirectblock = ParserConstCSFD.parserListOfMoviesRedirectMask1.search(self.inhtml)
		if redirectblock is not None:
			redirectblock = ParserConstCSFD.parserhtmltags.sub('', redirectblock.group(1).strip()).strip()
		else:
			redirectblock = ParserConstCSFD.parserListOfMoviesRedirectMask2.search(self.inhtml)
			if redirectblock is not None:
				redirectblock = ParserConstCSFD.parserhtmltags.sub('', redirectblock.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserListOfMoviesRedirect - konec\n')
		return redirectblock

	def parserListOfMoviesRedirect1(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfMoviesRedirect1 - zacatek\n')
		redirectblock = ParserConstCSFD.parserListOfMoviesRedirectMask1.search(self.inhtml)
		if redirectblock is not None:
			redirectblock = ParserConstCSFD.parserhtmltags.sub('', redirectblock.group(1).strip()).strip()
		else:
			redirectblock = ParserConstCSFD.parserListOfMoviesRedirectMask2.search(self.inhtml)
			if redirectblock is not None:
				redirectblock = ParserConstCSFD.parserhtmltags.sub('', redirectblock.group(1).strip()).strip()
		redirecturl = ParserConstCSFD.parserListOfMoviesRedirectMaskUrl.search(self.inhtml)
		if redirecturl is not None:
			redirecturl = ParserConstCSFD.parserhtmltags.sub('', redirecturl.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserListOfMoviesRedirect1 - konec\n')
		return (redirectblock, redirecturl)

	def parserCurrentPageUrl(self):
		LogCSFD.WriteToFile('[CSFD] parserCurrentPageUrl - zacatek\n')
		url = ParserConstCSFD.parserCurrentPageUrlSearchMask.search(self.inhtml)
		if url is not None:
			url = ParserConstCSFD.parserhtmltags.sub('', url.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserCurrentPageUrl - konec\n')
		return url

	def parserRedirectPage(self):
		LogCSFD.WriteToFile('[CSFD] parserRedirectPage - zacatek\n')
		redirectblock = ParserConstCSFD.parserRedirectPageMask.search(self.inhtml)
		if redirectblock is not None:
			redirectblock = ParserConstCSFD.parserhtmltags.sub('', redirectblock.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserRedirectPage - konec\n')
		return redirectblock

	def parserHiddenContent(self):
		LogCSFD.WriteToFile('[CSFD] parserHiddenContent - zacatek\n')
		hideblock = ParserConstCSFD.parserHiddenContentMask.search(self.inhtml)
		if hideblock is not None:
			hideblock = ParserConstCSFD.parserhtmltags.sub('', hideblock.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserHiddenContent - konec\n')
		return hideblock

	def parserListOfRelatedMovies(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - zacatek\n')
		searchresults = []
		searchresults1 = []
		omezitresults = ParserConstCSFD.parserListOfRelatedMoviesLimitMask.search(self.inhtml)
		if omezitresults is not None:
			searchresults1 = ParserConstCSFD.parserListOfRelatedMoviesSearchMask.finditer(omezitresults.group(1))
			if searchresults1 is not None:
				for x in searchresults1:
					if x is not None:
						searchresults.append((x.group(1), x.group(3), x.group(4), x.group(2)))

		LogCSFD.WriteToFile('[CSFD] parserListOfRelatedMovies - konec\n')
		return searchresults

	def parserListOfSimilarMovies(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfSimilarMovies - zacatek\n')
		searchresults = []
		searchresults1 = []
		omezitresults = ParserConstCSFD.parserListOfSimilarMoviesLimitMask.search(self.inhtml)
		if omezitresults is not None:
			searchresults1 = ParserConstCSFD.parserListOfSimilarMoviesSearchMask.finditer(omezitresults.group(1))
			if searchresults1 is not None:
				for x in searchresults1:
					searchresults.append((x.group(1), x.group(3), x.group(4), x.group(2)))

		LogCSFD.WriteToFile('[CSFD] parserListOfSimilarMovies - konec\n')
		return searchresults

	def parserListOfSeries(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - zacatek\n')
		searchresults = []
		searchresults1 = []
		nazev = self.parserMovieTitle()
		if nazev is None:
			nazev = ''
		elif nazev != '':
			nazev = nazev + ' - '
		omezitresults = ParserConstCSFD.parserListOfSeriesLimitMask.search(self.inhtml)
		if omezitresults is not None:
			searchresults1 = ParserConstCSFD.parserListOfSeriesSearchMask.finditer(omezitresults.group(1))
			if searchresults1 is not None:
				for x in searchresults1:
					searchresults.append((x.group(1), nazev + x.group(3) + ' ' + x.group(5), x.group(4), x.group(2)))

		LogCSFD.WriteToFile('[CSFD] parserListOfSeries - konec\n')
		return searchresults

	def parserListOfEpisodes(self):
		LogCSFD.WriteToFile('[CSFD] parserListOfEpisodes - zacatek\n')
		searchresults = []
		searchresults1 = []
		searchresults2 = []
		omezitresults = ParserConstCSFD.parserListOfEpisodesLimitMask.search(self.inhtml)
		if omezitresults is not None:
			searchresults1 = ParserConstCSFD.parserListOfEpisodesSearchMask1.finditer(omezitresults.group(1))
			if searchresults1 is not None:
				for x in searchresults1:
					searchresults.append((x.group(1), x.group(3) + ' ' + x.group(4), None, x.group(2)))

			if len(searchresults) == 0:
				searchresults2 = ParserConstCSFD.parserListOfEpisodesSearchMask2.finditer(omezitresults.group(1))
				if searchresults2 is not None:
					for x in searchresults2:
						searchresults.append((x.group(1), x.group(3), x.group(4), x.group(2)))

		LogCSFD.WriteToFile('[CSFD] parserListOfEpisodes - konec\n')
		return searchresults

	def parserRatingStars(self):
		LogCSFD.WriteToFile('[CSFD] parserRatingStars - zacatek\n')
		ratingstars = -1
		rating = ParserConstCSFD.parserRatingMask.search(self.inhtml)
		if rating is not None:
			sss = ParserConstCSFD.parserhtmltags.sub('', rating.group(1).replace('%', '').replace('\xa0', '').strip())
			if sss != '':
				try:
					ratingstars = int(10 * round(float(sss.replace(',', '.')) / 10, 1))
				except ValueError:
					ratingstars = -1

		LogCSFD.WriteToFile('[CSFD] parserRatingStars - konec\n')
		return ratingstars

	def parserMovieTitleInclYear(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - zacatek\n')
		titelblock = ParserConstCSFD.parserMovieTitelInclYearMask1.search(self.inhtml)
		if titelblock is not None:
			titelblock = ParserConstCSFD.parserhtmltags.sub('', titelblock.group(1).strip()).strip()
			for phrase, newphrase in typeOfMovie:
				titelblock = titelblock.replace(phrase, '')

			titelblock = titelblock.strip()
			titelblock = titelblock.replace('  ', ' ')
			titelblock = NameMovieCorrectionExtensionsTwoNames(titelblock)
		if titelblock is None or titelblock == '':
			LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - 2 zpusob\n')
			titelblock = ParserConstCSFD.parserMovieTitelInclYearMask2.search(self.inhtml)
			if titelblock is not None:
				titelblock = ParserConstCSFD.parserhtmltags.sub('', titelblock.group(1).strip()).strip()
				for phrase, newphrase in typeOfMovie:
					titelblock = titelblock.replace(phrase, '')

				titelblock = titelblock.strip()
				titelblock = titelblock.replace('  ', ' ')
				titelblock = NameMovieCorrectionExtensionsTwoNames(titelblock)
		LogCSFD.WriteToFile('[CSFD] parserMovieTitleInclYear - konec\n')
		return titelblock

	def parserMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieTitle - zacatek\n')
		jmenoblock = ParserConstCSFD.parserMovieTitelMask.search(self.inhtml)
		if jmenoblock is not None:
			jmenoblock = ParserConstCSFD.parserhtmltags.sub('', jmenoblock.group(1).strip())
			for phrase, newphrase in typeOfMovie:
				jmenoblock = jmenoblock.replace(phrase, '')

			jmenoblock = jmenoblock.strip()
			jmenoblock = jmenoblock.replace('  ', ' ')
			jmenoblock = NameMovieCorrectionExtensionsTwoNames(jmenoblock)
		LogCSFD.WriteToFile('[CSFD] parserMovieTitle - konec\n')
		return jmenoblock

	def parserSeriesNameInEpisode(self):
		LogCSFD.WriteToFile('[CSFD] parserSeriesNameInEpisode - zacatek\n')
		vysl = None
		limitresult = ParserConstCSFD.parserSeriesNameTitelLimitMask.search(self.inhtml)
		if limitresult is not None:
			jmenoblock = ParserConstCSFD.parserSeriesNameTitelMask1.search(limitresult.group(1))
			if jmenoblock is not None:
				vysl1 = ParserConstCSFD.parserhtmltags.sub('', jmenoblock.group(2).strip())
				vysl1 = vysl1.strip()
				vysl1 = vysl1.replace('	 ', ' ')
				vysl2 = ParserConstCSFD.parserhtmltags.sub('', jmenoblock.group(4).strip())
				vysl2 = vysl2.strip()
				vysl2 = vysl2.replace('	 ', ' ')
				vysl = vysl1 + ' - ' + vysl2
			else:
				jmenoblock = ParserConstCSFD.parserSeriesNameTitelMask2.search(limitresult.group(1))
				if jmenoblock is not None:
					vysl1 = ParserConstCSFD.parserhtmltags.sub('', jmenoblock.group(2).strip())
					vysl1 = vysl1.strip()
					vysl1 = vysl1.replace('	 ', ' ')
					vysl = vysl1
		LogCSFD.WriteToFile('[CSFD] parserSeriesNameInEpisode - konec\n')
		return vysl

	def parserTypeOfMovie(self):
		LogCSFD.WriteToFile('[CSFD] parserTypeOfMovie - zacatek\n')
		typeMovie = None
		jmenoblock = ParserConstCSFD.parserTypeOfMovieMask.search(self.inhtml)
		if jmenoblock is not None:
			jmenoblock = ParserConstCSFD.parserhtmltags.sub('', jmenoblock.group(1).strip())
			for phrase, newphrase in typeOfMovie:
				if jmenoblock.find(phrase) >= 0:
					typeMovie = strUni(newphrase)
					break

		LogCSFD.WriteToFile('[CSFD] parserTypeOfMovie - konec\n')
		return typeMovie

	def parserOtherMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitle - zacatek\n')
		searchresults = None
		ostjmenatext = ''
		ostjmenaresult = ParserConstCSFD.parserOtherMovieTitelLimitMask.search(self.inhtml)
		if ostjmenaresult is not None:
			ostjmenaresult1 = ParserConstCSFD.parserOtherMovieTitelSearchMask.findall(ostjmenaresult.group(1))
			if ostjmenaresult1 is not None:
				searchresults = []
				for value in ostjmenaresult1:
					p1 = value[0].replace(' název', '').strip()
					p2 = value[1].strip()
					p2 = NameMovieCorrectionExtensions(p2)
					searchresults.append((p1, p2))
					ostjmenatext += p1 + ': ' + p2 + '\n'

				if ostjmenatext is not '':
					ostjmenatext = ParserConstCSFD.parserhtmltags.sub('', ostjmenatext)
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitle - konec\n')
		return (searchresults, ostjmenatext)

	def parserOtherMovieTitleWOCountry(self):
		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitleWOCountry - zacatek\n')
		searchresults = None
		ostjmenaresult = ParserConstCSFD.parserOtherMovieTitelWOCountryLimitMask.search(self.inhtml)
		if ostjmenaresult is not None:
			ostjmenaresult1 = ParserConstCSFD.parserOtherMovieTitelWOCountrySearchMask.findall(ostjmenaresult.group(1))
			if ostjmenaresult1 is not None:
				searchresults = []
				for value in ostjmenaresult1:
					p1 = value.strip()
					if p1 != '':
						searchresults.append(NameMovieCorrectionExtensions(p1))

		LogCSFD.WriteToFile('[CSFD] parserOtherMovieTitleWOCountry - konec\n')
		return searchresults

	def parserOrigMovieTitle(self):
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - zacatek\n')
		origname = None
		result = self.parserOtherMovieTitleWOCountry()
		if result is not None and len(result) > 0:
			origname = result[0]
		LogCSFD.WriteToFile('[CSFD] parserOrigMovieTitle - konec\n')
		return origname

	def parserMainPosterUrl(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - zacatek\n')
		if full_image:
			image_limit = ''
		else:
			image_limit = '?h180'
		posterurl = ParserConstCSFD.parserMainPosterUrlMask.search(self.inhtml)
		if posterurl is not None and (posterurl.group(1).find('jpg') >= 0 or posterurl.group(1).find('png') >= 0):
			posterurl = CSFDGlobalVar.getHTTP() + ':' + posterurl.group(1) + image_limit
		LogCSFD.WriteToFile('[CSFD] parserMainPosterUrl - konec\n')
		return posterurl

	def parserAllPostersUrl(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - zacatek\n')
		if full_image:
			image_limit = ''
		else:
			image_limit = '?h180'
		posterresult1 = None
		posterresult = ParserConstCSFD.parserAllPostersUrlLimitMask.search(self.inhtml)
		if posterresult is not None:
			posterresult1 = ParserConstCSFD.parserAllPostersUrlSearchMask.findall(posterresult.group(1))
			if posterresult1 is not None:
				for index, value in enumerate(posterresult1):
					posterresult1[index] = CSFDGlobalVar.getHTTP() + ':' + value.replace('\\', '').strip() + image_limit

		LogCSFD.WriteToFile('[CSFD] parserAllPostersUrl - konec\n')
		return posterresult1

	def parserPostersNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - zacatek\n')
		pocet = None
		posterresult = ParserConstCSFD.parserPostersNumberLimitMask.search(self.inhtml)
		if posterresult is not None:
			posterresult1 = ParserConstCSFD.parserPostersNumberSearchMask.findall(posterresult.group(1))
			if posterresult1 is not None:
				pocet = len(posterresult1)
				if pocet <= 0:
					pocet = None
		LogCSFD.WriteToFile('[CSFD] parserPostersNumber - konec\n')
		return pocet

	def parserGenre(self):
		LogCSFD.WriteToFile('[CSFD] parserGenre - zacatek\n')
		genre = ParserConstCSFD.parserGenreMask.search(self.inhtml)
		if genre is not None:
			genre = ParserConstCSFD.parserhtmltags.sub('', genre.group(1).replace(' / ', ', ').strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserGenre - konec\n')
		return genre

	def parserOrigin(self):
		LogCSFD.WriteToFile('[CSFD] parserOrigin - zacatek\n')
		origin = ParserConstCSFD.parserOriginMask.search(self.inhtml)
		if origin is not None:
			origin = ParserConstCSFD.parserhtmltags.sub('', origin.group(1).strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserOrigin - konec\n')
		return origin

	def parserMovieYear(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieYear - zacatek\n')
		year = None
		info = self.parserOrigin()
		if info is not None:
			r_year = self.parserGetYears(info)
			if r_year is not None and len(r_year) > 0:
				year = r_year[0]
		LogCSFD.WriteToFile('[CSFD] parserMovieYear - konec\n')
		return year

	def parserMovieDuration(self):
		LogCSFD.WriteToFile('[CSFD] parserMovieDuration - zacatek\n')
		delka = None
		info = self.parserOrigin()
		if info is not None:
			info = re.sub('\\(.*\\)', '', info).strip()
			r_info = info.split(',')
			for x in r_info:
				if x.find('min') >= 0:
					delka = x.replace('	 ', ' ').strip() + '.'
					poz = delka.find('x')
					if poz >= 0:
						delka = delka[poz + 1:].strip()
					poz = delka.find('-')
					if poz >= 0:
						delka = delka[poz + 1:].strip()
					if delka == '':
						delka = None
					break

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
		Zebrickytext = None
		result = ParserConstCSFD.parserCSFDRankingsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserCSFDRankingsSearchMask.findall(result.group(1))
			if result1 is not None:
				Zebrickytext = ''
				for x in result1:
					Zebrickytext += ParserConstCSFD.parserhtmltags.sub('', x.strip()).strip() + ' na CSFD\n'

		LogCSFD.WriteToFile('[CSFD] parserCSFDRankings - konec\n')
		return Zebrickytext

	def parserWherePlaying(self):
		LogCSFD.WriteToFile('[CSFD] parserWherePlaying - zacatek\n')
		text = None
		result = ParserConstCSFD.parserWherePlayingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserWherePlayingSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserWherePlaying - konec\n')
		return text

	def parserDirector(self):
		LogCSFD.WriteToFile('[CSFD] parserDirector - zacatek\n')
		text = None
		result = ParserConstCSFD.parserDirectorLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDirectorSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not None and text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserDirector - konec\n')
		return text

	def parserMusic(self):
		LogCSFD.WriteToFile('[CSFD] parserMusic - zacatek\n')
		text = None
		result = ParserConstCSFD.parserMusicLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserMusicSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserMusic - konec\n')
		return text

	def parserDraft(self):
		LogCSFD.WriteToFile('[CSFD] parserDraft - zacatek\n')
		text = None
		result = ParserConstCSFD.parserDraftLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDraftSearchMask1.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
				result2 = ParserConstCSFD.parserDraftSearchMask2.search(result.group(1))
				if result2 is not None:
					text += ' (' + ParserConstCSFD.parserhtmltags.sub('', result2.group(1).strip()).strip() + ')'
		LogCSFD.WriteToFile('[CSFD] parserDraft - konec\n')
		return text

	def parserWriters(self):
		LogCSFD.WriteToFile('[CSFD] parserWriters - zacatek\n')
		text = None
		result = ParserConstCSFD.parserDraftLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDraftSearchMask1.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserWriters - konec\n')
		return text

	def parserScenario(self):
		LogCSFD.WriteToFile('[CSFD] parserScenario - zacatek\n')
		text = None
		result = ParserConstCSFD.parserScenarioLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserScenarioSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserScenario - konec\n')
		return text

	def parserCamera(self):
		LogCSFD.WriteToFile('[CSFD] parserCamera - zacatek\n')
		text = None
		result = ParserConstCSFD.parserCameraLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserCameraSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserCamera - konec\n')
		return text

	def parserProduction(self):
		LogCSFD.WriteToFile('[CSFD] parserProduction - zacatek\n')
		text = None
		result = ParserConstCSFD.parserProductionLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserProductionSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserProduction - konec\n')
		return text

	def parserCutting(self):
		LogCSFD.WriteToFile('[CSFD] parserCutting - zacatek\n')
		text = None
		result = ParserConstCSFD.parserCuttingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserCuttingSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserCutting - konec\n')
		return text

	def parserSound(self):
		LogCSFD.WriteToFile('[CSFD] parserSound - zacatek\n')
		text = None
		result = ParserConstCSFD.parserSoundLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserSoundSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserSound - konec\n')
		return text

	def parserScenography(self):
		LogCSFD.WriteToFile('[CSFD] parserScenography - zacatek\n')
		text = None
		result = ParserConstCSFD.parserScenographyLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserScenographySearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserScenography - konec\n')
		return text

	def parserMakeUp(self):
		LogCSFD.WriteToFile('[CSFD] parserMakeUp - zacatek\n')
		text = None
		result = ParserConstCSFD.parserMakeUpLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserMakeUpSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserMakeUp - konec\n')
		return text

	def parserCostumes(self):
		LogCSFD.WriteToFile('[CSFD] parserCostumes - zacatek\n')
		text = None
		result = ParserConstCSFD.parserCostumesLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserCostumesSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserCostumes - konec\n')
		return text

	def parserCasting(self):
		LogCSFD.WriteToFile('[CSFD] parserCasting - zacatek\n')
		text = None
		result = ParserConstCSFD.parserCastingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserCastingSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserCasting - konec\n')
		return text

	def parserTags(self):
		LogCSFD.WriteToFile('[CSFD] parserTags - zacatek\n')
		text = None
		result = ParserConstCSFD.parserTagsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserTagsSearchMask.findall(result.group(1))
			if result1 is not None:
				text = ''
				for x in result1:
					text += x.strip() + ', '

				if text is not '':
					text = text.rstrip(', ')
					text = ParserConstCSFD.parserhtmltags.sub('', text.strip()).strip()
		LogCSFD.WriteToFile('[CSFD] parserTags - konec\n')
		return text

	def parserContent(self):
		LogCSFD.WriteToFile('[CSFD] parserContent - zacatek\n')
		Obsahtext = ''
		result = ParserConstCSFD.parserContentLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserContentSearchMask.findall(result.group(1))
			if result1 is not None:
				for x in result1:
					obsah = ParserConstCSFD.parserhtmltags.sub('', x.replace('\n\n', ' ').replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip()).replace('	', ' ').replace('  ', ' ').strip()
					obsah = obsah.replace('\n\n', '\n').replace('\n \n', '\n').strip()
					if obsah != '':
						if Obsahtext == '':
							Obsahtext += obsah
						else:
							Obsahtext += '\n \n' + obsah

		LogCSFD.WriteToFile('[CSFD] parserContent - konec\n')
		return Obsahtext

	def parserIMDBlink(self):
		LogCSFD.WriteToFile('[CSFD] parserIMDBlink - zacatek\n')
		result = ParserConstCSFD.parserIMDBlinkMask.search(self.inhtml)
		if result is not None:
			result = result.group(1).replace('/combined', '').strip()
			LogCSFD.WriteToFile('[CSFD] parserIMDBlink: ' + result + '\n')
		else:
			result = ''
		LogCSFD.WriteToFile('[CSFD] parserIMDBlink - konec\n')
		return result

	def parserIMDBid(self):
		LogCSFD.WriteToFile('[CSFD] parserIMDBid - zacatek\n')
		result = ParserConstCSFD.parserIMDBidkMask.search(self.inhtml)
		if result is not None:
			result = result.group(1).strip().replace('tt', '')
			LogCSFD.WriteToFile('[CSFD] parserIMDBid: ' + result + '\n')
		else:
			result = ''
		LogCSFD.WriteToFile('[CSFD] parserIMDBid - konec\n')
		return result

	def parserNumber(self, typParser):
		pocet = None
		result = typParser.search(self.inhtml)
		if result is not None:
			result = result.group(1).replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').strip()
			try:
				pocet = int(result)
			except ValueError:
				LogCSFD.WriteToFile('[CSFD] parserNumber - chyba\n')
				pocet = None

		return pocet

	def parserRatingNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserRatingNumber - zacatek\n')
		pocet_hodnoceni = self.parserNumber(ParserConstCSFD.parserRatingNumberMask)
		if pocet_hodnoceni is None:
			result = ParserConstCSFD.parserRatingNumberLimitMask.search(self.inhtml)
			if result is not None:
				result1 = ParserConstCSFD.parserRatingNumberSearchMask.findall(result.group(1))
				if result1 is not None:
					pocet_hodnoceni = len(result1)
					if pocet_hodnoceni <= 0:
						pocet_hodnoceni = None
		LogCSFD.WriteToFile('[CSFD] parserRatingNumber - konec\n')
		return pocet_hodnoceni

	def parserUserComments(self):
		LogCSFD.WriteToFile('[CSFD] parserUserComments - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserUserCommentsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserUserCommentsSearchMask.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					if value[1].count('odpad') > 0:
						p1 = 'odpad!'
					else:
						p1 = ('').ljust(value[1].count('*'), '*').replace('*', '* ').strip()
					p0 = value[0].strip()
					p2 = value[3].strip()
					p3 = ParserConstCSFD.parserhtmltags.sub('', value[2].replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip())
					searchresults.append((p0, p1, p2, p3))

		LogCSFD.WriteToFile('[CSFD] parserUserComments - konec\n')
		return searchresults

	def parserUserCommentsNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserCommentsNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserUserCommentsNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserUserCommentsNumber - konec\n')
		return pocet

	def parserUserExtReviews(self):
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviews - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserUserExtReviewsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserUserExtReviewsSearchMask.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					if value[0].count('odpad') > 0:
						p1 = 'odpad!'
					else:
						p1 = ('').ljust(value[0].count('*'), '*').replace('*', '* ').strip()
					p0 = strUni(char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', value[0]))).replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').replace('   ', ' ').replace('  ', ' ').strip()
					p2 = strUni(char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', value[1].replace('\n', ' ').replace('…', '...').replace('<br>', '\n').replace('<br />', '\n').strip())))
					p2 = strUni(p2.replace('(více)', ''))
					searchresults.append((p0, p1, p2))

		LogCSFD.WriteToFile('[CSFD] parserUserExtReviews - konec\n')
		return searchresults

	def parserUserExtReviewsNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviewsNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserUserExtReviewsNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserUserExtReviewsNumber - konec\n')
		return pocet

	def parserUserDiscussion(self):
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussion - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserUserDiscussionMask.findall(self.inhtml)
		if result is not None:
			searchresults = []
			for value in result:
				p0 = value[0].strip()
				p1 = value[1].strip()
				p2 = ParserConstCSFD.parserhtmltags.sub('', value[2].replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip())
				searchresults.append((p0, p1, p2))

		LogCSFD.WriteToFile('[CSFD] parserUserDiscussion - konec\n')
		return searchresults

	def parserUserDiscussionNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussionNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserUserDiscussionNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserUserDiscussionNumber - konec\n')
		return pocet

	def parserInterest(self):
		LogCSFD.WriteToFile('[CSFD] parserInterest - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserInterestLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserInterestSearchMask1.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					film = ParserConstCSFD.parserhtmltags.sub('', value[0].replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip())
					p0 = film + ':\n' + ParserConstCSFD.parserhtmltags.sub('', value[1].replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip())
					p1 = ParserConstCSFD.parserhtmltags.sub('', value[2].replace('(', '').replace(')', '')).strip()
					searchresults.append((p0, p1))

			if searchresults is None or len(searchresults) == 0:
				result2 = ParserConstCSFD.parserInterestSearchMask2.findall(result.group(1))
				if result2 is not None:
					searchresults = []
					for value in result2:
						p0 = ParserConstCSFD.parserhtmltags.sub('', value[0].replace('\n', ' ').replace('<br>', '\n').replace('<br />', '\n').strip())
						p1 = ParserConstCSFD.parserhtmltags.sub('', value[1].replace('(', '').replace(')', '')).strip()
						searchresults.append((p0, p1))

		LogCSFD.WriteToFile('[CSFD] parserInterest - konec\n')
		return searchresults

	def parserInterestTypesAndNumbers(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestTypesAndNumbers - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserInterestTypesAndNumbersLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserInterestTypesAndNumbersSearchMask.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					p0 = ParserConstCSFD.parserhtmltags.sub('', value[0].strip())
					p1 = ParserConstCSFD.parserhtmltags.sub('', value[1].strip())
					p2 = ParserConstCSFD.parserhtmltags.sub('', value[2].strip())
					searchresults.append((p0, p1, p2))

		LogCSFD.WriteToFile('[CSFD] parserInterestTypesAndNumbers - konec\n')
		return searchresults

	def parserInterestSelectedTypeAndNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestSelectedTypeAndNumber - zacatek\n')
		url = None
		name = ''
		number = ''
		result = ParserConstCSFD.parserInterestSelectedTypeAndNumberLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserInterestSelectedTypeAndNumberSearchMask.search(result.group(1))
			if result1 is not None:
				url = ParserConstCSFD.parserhtmltags.sub('', result1.group(1).strip())
				name = ParserConstCSFD.parserhtmltags.sub('', result1.group(2).strip())
				number = ParserConstCSFD.parserhtmltags.sub('', result1.group(3).strip())
				number = number.replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').strip()
		LogCSFD.WriteToFile('[CSFD] parserInterestSelectedTypeAndNumber - konec\n')
		return (url, name, number)

	def parserInterestNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserInterestNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserInterestNumber - konec\n')
		return pocet

	def parserUserRating(self):
		LogCSFD.WriteToFile('[CSFD] parserUserRating - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserUserRatingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserUserRatingSearchMask.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					if value[1].count('odpad') > 0:
						p1 = 'odpad!'
					else:
						p1 = ('').ljust(value[1].count('*'), '*').replace('*', '* ').strip()
					p0 = ParserConstCSFD.parserhtmltags.sub('', value[0].strip())
					searchresults.append((p0, p1))

		LogCSFD.WriteToFile('[CSFD] parserUserRating - konec\n')
		return searchresults

	def parserPremiere(self):
		LogCSFD.WriteToFile('[CSFD] parserPremiere - zacatek\n')
		text = ''
		pristupnost = ''
		result = ParserConstCSFD.parserPremiereLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserAccessibilitySearchMask.search(result.group(1))
			if result1 is not None:
				pristupnost = ParserConstCSFD.parserhtmltags.sub('', result1.group(1).strip())
			result1 = ParserConstCSFD.parserPremiereSearchMask.findall(result.group(1))
			if result1 is not None:
				for x in result1:
					text += ParserConstCSFD.parserhtmltags.sub('', x.strip().replace('\n', '')).replace('\n', '').replace(':', ': ') + '\n'

		LogCSFD.WriteToFile('[CSFD] parserPremiere - konec\n')
		return (text, pristupnost)

	def parserAwards(self):
		LogCSFD.WriteToFile('[CSFD] parserAwards - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserAwardsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserAwardsSearchMask1.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					p0 = ParserConstCSFD.parserhtmltags.sub('', value[0].strip().replace('\n', '')).replace('\n', '')
					p0 = p0.replace('\xa0', ' ').strip()
					result2 = ParserConstCSFD.parserAwardsSearchMask2.findall(value[1])
					if result2 is not None:
						for detail in result2:
							p1 = detail[0].strip()
							p2 = ParserConstCSFD.parserhtmltags.sub('', detail[1].strip()).replace('\n', '').replace('\t', ' ')
							p2 = p2.replace('\xa0\xa0', ' ').replace('\xa0\xa0\xa0', ' ').replace('	  ', ' ').replace('	 ', ' ').strip()
							p2 = p2.replace('	', ' ').replace('  ', ' ').strip()
							searchresults.append((p0, p1, p2))

		LogCSFD.WriteToFile('[CSFD] parserAwards - konec\n')
		return searchresults

	def parserDateOfPremiere(self):
		LogCSFD.WriteToFile('[CSFD] parserDateOfPremiere - zacatek\n')
		datum = None
		datref = None
		try:
			x = '01.01.' + self.parserMovieYear()
			datref = datetime.strptime(x, '%d.%m.%Y')
		except ValueError:
			datref = None

		result = ParserConstCSFD.parserPremiereLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDate.findall(result.group(1))
			if result1 is not None:
				for x in result1:
					d1 = None
					try:
						d1 = datetime.strptime(x, '%d.%m.%Y')
					except ValueError:
						d1 = None

					if d1 is not None:
						if datum is not None:
							if d1 < datum:
								datum = d1
						else:
							datum = d1

		if datum is None:
			datum = datref
		elif datref is not None:
			diff = datum - datref
			if abs(diff.days) > 750:
				datum = datref
		LogCSFD.WriteToFile('[CSFD] parserDateOfPremiere - konec\n')
		return datum

	def parserUserFans(self):
		LogCSFD.WriteToFile('[CSFD] parserUserFans - zacatek\n')
		text = ''
		result = ParserConstCSFD.parserUserFansLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserUserFansSearchMask.findall(result.group(1))
			if result1 is not None:
				for x in result1:
					text += x.strip() + '\n'

		LogCSFD.WriteToFile('[CSFD] parserUserFans - konec\n')
		return text

	def parserUserFansNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserUserFansNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserUserFansNumberMask)
		if pocet is None:
			result = ParserConstCSFD.parserUserFansNumberLimitMask.search(self.inhtml)
			if result is not None:
				result1 = ParserConstCSFD.parserUserFansNumberSearchMask.findall(result.group(1))
				if result1 is not None:
					pocet = len(result1)
					if pocet <= 0:
						pocet = None
		LogCSFD.WriteToFile('[CSFD] parserUserFansNumber - konec\n')
		return pocet

	def parserVideoListNextPage(self):
		LogCSFD.WriteToFile('[CSFD] parserVideoListNextPage - zacatek\n')
		link = None
		result = ParserConstCSFD.parserVideoListNextPageLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserVideoListNextPageSearchMask.search(result.group(1))
			if result1 is not None:
				link = result1.group(1).strip()
		LogCSFD.WriteToFile('[CSFD] parserVideoListNextPage - konec\n')
		result = None
		result1 = None
		return link

	def parserVideoTypeList(self):
		LogCSFD.WriteToFile('[CSFD] parserVideoTypeList - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserVideoTypeListLimitMask.search(self.inhtml)
		if result is not None:
			searchresults = []
			result1 = ParserConstCSFD.parserVideoTypeListSearchMask.findall(result.group(1))
			if result1 is not None:
				for value in result1:
					p0 = value[0].strip()
					p1 = value[1].strip()
					p2 = value[2].replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').strip()
					searchresults.append((p0, p1, p2))

		result = None
		result1 = None
		LogCSFD.WriteToFile('[CSFD] parserVideoTypeList - konec\n')
		return searchresults

	def parserVideoNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserVideoNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserVideoNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserVideoNumber - konec\n')
		return pocet

	def parserVideoDetail(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - zacatek\n')
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - 0a\n')
		if full_image:
			image_limit = ''
		else:
			image_limit = '?w700'
		searchresults = None
		url_movie = self.parserCurrentPageUrl()
		typ_ukazek = ''
		if url_movie is not None and url_movie.rfind('type=') > 0:
			try:
				typ_ukazek = strUni(_('Kategorie:') + ' ' + url_movie.rsplit('=', 1)[1] + ' - ')
			except:
				typ_ukazek = strUni(_('Kategorie:') + ' 1 - ')

		else:
			typ_ukazek = strUni(_('Kategorie:') + ' 1 - ')
		result = ParserConstCSFD.parserVideoDetailLimitMask.findall(self.inhtml_script)
		if result is not None:
			searchresults = []
			for y in result:
				videoklipurlSD = ''
				videoklipurlHD = ''
				videotitulkyurlCZ = ''
				videotitulkyurlSK = ''
				videoDescr = ''
				videoPoster = ''
				result1 = ParserConstCSFD.parserVideoDetailDescrSearchMask.search(y)
				if result1 is not None:
					videoDescr = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', result1.group(1).replace('\n', ' ')).strip())
					digit = ExtractNumbers(videoDescr)
					if digit is not None:
						for cc in digit:
							cc = cc.strip()
							if len(cc) == 1:
								cc1 = cc.zfill(2)
								videoDescr = videoDescr.replace(' ' + cc, ' ' + cc1)

					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video - Descr: ' + videoDescr + '\n')
					videoDescr = strUni(videoDescr)
				result1 = ParserConstCSFD.parserVideoDetailPosterSearchMask.search(y)
				if result1 is not None:
					videoPoster = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', result1.group(1).replace('\n', ' ')).strip()) + image_limit
					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video - Poster: ' + videoPoster + '\n')
					videoPoster = strUni(videoPoster)
				result1 = ParserConstCSFD.parserVideoDetailFlagSearchMask.search(y)
				if result1 is not None:
					extra_info = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', result1.group(1).replace('\n', ' ')).strip())
					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video - urlFlag: ' + extra_info + '\n')
				result1 = ParserConstCSFD.parserVideoDetailDurationSearchMask.search(y)
				if result1 is not None:
					extra_info = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', result1.group(1).replace('\n', '')).strip())
					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video - Duration: ' + extra_info + '\n')
					if len(extra_info) > 0:
						videoDescr += strUni(' - ' + extra_info)
				videoDescr = typ_ukazek + videoDescr
				result1 = ParserConstCSFD.parserVideoDetailSearchMask.findall(y)
				if result1 is not None:
					for x in result1:
						sss = x.strip()
						if sss.find('advert') >= 0:
							LogCSFD.WriteToFile('[CSFD] parserVideoDetail - reklama: ano\n')
						else:
							LogCSFD.WriteToFile('[CSFD] parserVideoDetail - reklama: ne\n')
							resultDet = ParserConstCSFD.parserVideoDetailClipListSearchMask.findall(sss)
							if resultDet is not None:
								for xx in resultDet:
									if xx[1].replace('\\', '').replace('/', '') != 'webm':
										if xx[2] == '720p' or xx[2] == '1080i' or xx[2] == '1080p':
											videoklipurlHD = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', xx[0]).replace('\\', '').strip())
										elif xx[2] == '360p' or xx[2] == '480p':
											videoklipurlSD = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', xx[0]).replace('\\', '').strip())
										else:
											LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video file - chyba: nezname rozliseni ' + char2Allowchar(xx[2]) + '\n')

								LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video file - SD: ' + videoklipurlSD + '\n')
								videoklipurlSD = strUni(videoklipurlSD)
								LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video file - HD: ' + videoklipurlHD + '\n')
								videoklipurlHD = strUni(videoklipurlHD)
								resultDet = ParserConstCSFD.parserVideoDetailSubtListSearchMask.findall(sss)
								if resultDet is not None:
									for xx in resultDet:
										if xx[1] == 'cz' or xx[1] == 'cs':
											videotitulkyurlCZ = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', xx[0]).replace('\\', '').strip())
											videoDescr += ' ' + _('CZ titulky')
										elif xx[1] == 'sk':
											videotitulkyurlSK = char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', xx[0]).replace('\\', '').strip())
											videoDescr += ' ' + _('SK titulky')

									LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video titulky - CZ: ' + videotitulkyurlCZ + '\n')
									videotitulkyurlCZ = strUni(videotitulkyurlCZ)
									LogCSFD.WriteToFile('[CSFD] parserVideoDetail - video titulky - SK: ' + videotitulkyurlSK + '\n')
									videotitulkyurlSK = strUni(videotitulkyurlSK)

				if not (videoklipurlSD == '' and videoklipurlHD == ''):
					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - added video file\n')
					searchresults.append((videoklipurlSD, videoklipurlHD, videotitulkyurlCZ, videotitulkyurlSK, videoDescr, videoPoster))
				else:
					LogCSFD.WriteToFile('[CSFD] parserVideoDetail - NOT added video file\n')

		resultDet = None
		result = None
		result1 = None
		LogCSFD.WriteToFile('[CSFD] parserVideoDetail - konec\n')
		return searchresults

	def parserGalleryNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserGalleryNumber - zacatek\n')
		pocet = self.parserNumber(ParserConstCSFD.parserGalleryNumberMask)
		LogCSFD.WriteToFile('[CSFD] parserGalleryNumber - konec\n')
		return pocet

	def parserGalleryTypeList(self):
		LogCSFD.WriteToFile('[CSFD] parserGalleryTypeList - zacatek\n')
		searchresults = None
		result = ParserConstCSFD.parserGalleryTypeListLimitMask.search(self.inhtml)
		if result is not None:
			searchresults = []
			result1 = ParserConstCSFD.parserGalleryTypeListSearchMask.findall(result.group(1))
			if result1 is not None:
				for value in result1:
					p0 = value[0].strip()
					p1 = value[1].strip()
					p2 = value[2].replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').strip()
					searchresults.append((p0, p1, p2))

		result = None
		result1 = None
		LogCSFD.WriteToFile('[CSFD] parserGalleryTypeList - konec\n')
		return searchresults

	def parserGallerySelectedTypeList(self):
		LogCSFD.WriteToFile('[CSFD] parserGallerySelectedTypeList - zacatek\n')
		url = None
		name = ''
		number = ''
		result = ParserConstCSFD.parserGallerySelectedTypeListLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserGallerySelectedTypeListSearchMask.search(result.group(1))
			if result1 is not None:
				url = ParserConstCSFD.parserhtmltags.sub('', result1.group(1).strip())
				name = ParserConstCSFD.parserhtmltags.sub('', result1.group(2).strip())
				number = ParserConstCSFD.parserhtmltags.sub('', result1.group(3).strip())
				number = number.replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').strip()
		LogCSFD.WriteToFile('[CSFD] parserGallerySelectedTypeList - konec\n')
		return (url, name, number)

	def parserGalleryList(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserGalleryList - zacatek\n')
		if full_image:
			image_limit = ''
		else:
			image_limit = '?w700'
		searchresults = None
		result = ParserConstCSFD.parserGalleryListLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserGalleryListSearchMask1.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					popis_gal = ''
					p0 = CSFDGlobalVar.getHTTP() + ':' + value[0].replace('\\', '').strip() + image_limit
					result2 = ParserConstCSFD.parserGalleryListSearchMask2.findall(value[1].strip())
					if result2 is not None:
						for xx in result2:
							popis_gal += xx.strip() + ', '

						if popis_gal is not '':
							popis_gal = popis_gal.rstrip(', ')
					p1 = popis_gal
					searchresults.append((p0, p1))

		result = None
		result1 = None
		LogCSFD.WriteToFile('[CSFD] parserGalleryList - konec\n')
		return searchresults

	def parserGalleryListUrl(self, full_image=False):
		LogCSFD.WriteToFile('[CSFD] parserGalleryListUrl - zacatek\n')
		if full_image:
			image_limit = ''
		else:
			image_limit = '?w700'
		searchresults = None
		result = ParserConstCSFD.parserGalleryListLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserGalleryListSearchMask1.findall(result.group(1))
			if result1 is not None:
				searchresults = []
				for value in result1:
					p0 = CSFDGlobalVar.getHTTP() + ':' + value[0].replace('\\', '').strip() + image_limit
					searchresults.append(p0)

		result = None
		result1 = None
		LogCSFD.WriteToFile('[CSFD] parserGalleryListUrl - konec\n')
		return searchresults

	def parserGalleryListNextPage(self):
		LogCSFD.WriteToFile('[CSFD] parserGalleryListNextPage - zacatek\n')
		link = None
		result = ParserConstCSFD.parserGalleryListNextPageLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserGalleryListNextPageSearchMask.search(result.group(1))
			if result1 is not None:
				link = result1.group(1).strip()
		LogCSFD.WriteToFile('[CSFD] parserGalleryListNextPage - konec\n')
		return link

	def parserOwnRating(self):
		LogCSFD.WriteToFile('[CSFD] parserOwnRating - zacatek\n')
		rating = None
		num_rating = None
		ss_rating = ''
		result = ParserConstCSFD.parserOwnRatingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserOwnRatingSearchMask.search(result.group(1))
			if result1 is not None:
				ss = result1.group(1).strip()
				if ss.count('odpad') > 0:
					rating = 'odpad!'
					num_rating = 0
				else:
					num_rating = ss.count('*') * 20
					rating = ('').ljust(ss.count('*'), '*').replace('*', '* ').strip()
				ss_rating = str(num_rating) + '%  ' + rating
		LogCSFD.WriteToFile('[CSFD] parserOwnRating - konec\n')
		return (ss_rating, num_rating)

	def parserDateOwnRating(self):
		LogCSFD.WriteToFile('[CSFD] parserDateOwnRating - zacatek\n')
		ss_date_rating = ''
		result = ParserConstCSFD.parserDateOwnRatingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDateOwnRatingSearchMask.search(result.group(1))
			if result1 is not None:
				ss_date_rating = strUni(char2Allowchar(result1.group(1).strip()))
		LogCSFD.WriteToFile('[CSFD] parserDateOwnRating - konec\n')
		return ss_date_rating

	def parserLoggedUser(self):
		LogCSFD.WriteToFile('[CSFD] parserLoggedUser - zacatek\n')
		link = None
		result = ParserConstCSFD.parserLoggedUserLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserLoggedUserSearchMask.search(result.group(1))
			if result1 is not None:
				link = result1.group(1).strip()
		LogCSFD.WriteToFile('[CSFD] parserLoggedUser - konec\n')
		return link

	def parserLoggedUserOwnData(self, html):
		LogCSFD.WriteToFile('[CSFD] parserLoggedUserOwnData - zacatek\n')
		link = None
		result = ParserConstCSFD.parserLoggedUserLimitMask.search(html)
		if result is not None:
			result1 = ParserConstCSFD.parserLoggedUserSearchMask.search(result.group(1))
			if result1 is not None:
				link = result1.group(1).strip()
		LogCSFD.WriteToFile('[CSFD] parserLoggedUserOwnData - konec\n')
		return link

	def parserUserIDLoggedUser(self):
		LogCSFD.WriteToFile('[CSFD] parserUserIDLoggedUser - zacatek\n')
		userid = None
		result = ParserConstCSFD.parserUserIDLoggedUserSearchMask.search(self.inhtml)
		if result is not None:
			userid = result.group('url').strip()
		LogCSFD.WriteToFile('[CSFD] parserUserIDLoggedUser - konec\n')
		return userid

	def parserTokenRating(self):
		LogCSFD.WriteToFile('[CSFD] parserTokenRating - zacatek\n')
		token = None
		result = ParserConstCSFD.parserTokenRatingLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserTokenRatingSearchMask.search(result.group(1))
			if result1 is not None:
				token = result1.group(1)
		LogCSFD.WriteToFile('[CSFD] parserTokenRating - konec\n')
		return token

	def parserTokenLogin(self, html):
		LogCSFD.WriteToFile('[CSFD] parserTokenLogin - zacatek\n')
		token = None
		if html is None or html == '':
			inhtml = self.inhtml
		else:
			inhtml = html
		result = ParserConstCSFD.parserTokenLoginLimitMask.search(inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserTokenLoginSearchMask.search(result.group(1))
			if result1 is not None:
				token = result1.group(1)
		LogCSFD.WriteToFile('[CSFD] parserTokenLogin - konec\n')
		return token

	def parserURLLogin(self, html):
		LogCSFD.WriteToFile('[CSFD] parserURLLogin - zacatek\n')
		url = ''
		if html is None or html == '':
			inhtml = self.inhtml
		else:
			inhtml = html
		result = ParserConstCSFD.parserURLLoginLimitMask.search(inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserURLLoginSearchMask.search(result.group(1))
			if result1 is not None:
				url = result1.group(1)
		LogCSFD.WriteToFile('[CSFD] parserURLLogin: ' + url + '\n')
		LogCSFD.WriteToFile('[CSFD] parserURLLogin - konec\n')
		return url

	def parserDeleteRatingUrl(self):
		LogCSFD.WriteToFile('[CSFD] parserDeleteRatingUrl - zacatek\n')
		url = None
		result = ParserConstCSFD.parserDeleteRatingUrlLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserDeleteRatingUrlSearchMask.search(result.group(1))
			if result1 is not None:
				url = result1.group(1)
		LogCSFD.WriteToFile('[CSFD] parserDeleteRatingUrl - konec\n')
		return url

	def parserFunctionExists(self):
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - zacatek\n')
		searchresults = []
		result = ParserConstCSFD.parserFunctionExistsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserFunctionExistsSearchMask.findall(result.group(1))
			if result1 is not None:
				for value in result1:
					if value.find('comments disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - komentare - NE\n')
						searchresults.append('komentare')
					elif value.find('trivia disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - zajimavosti - NE\n')
						searchresults.append('zajimavosti')
					elif value.find('awards disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - oceneni - NE\n')
						searchresults.append('oceneni')
					elif value.find('reviews disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - ext.recenze - NE\n')
						searchresults.append('ext.recenze')
					elif value.find('photos disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - galerie - NE\n')
						searchresults.append('galerie')
					elif value.find('videos disabled') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - video - NE\n')
						searchresults.append('video')
					elif value.find('disabled forum') >= 0:
						LogCSFD.WriteToFile('[CSFD] parserFunctionExists - diskuze - NE\n')
						searchresults.append('diskuze')

		if self.parserRatingNumber() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - hodnoceni - NE\n')
			searchresults.append('hodnoceni')
		if self.parserUserFansNumber() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - fanousci - NE\n')
			searchresults.append('fanousci')
		ss = self.parserPremiere()
		if ss[0] == '' and ss[1] == '':
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - premiery - NE\n')
			searchresults.append('premiery')
		if self.parserPostersNumber() is None and self.parserMainPosterUrl() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - postery - NE\n')
			searchresults.append('postery')
		if self.parserTokenRating() is None:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - ownrating - NE\n')
			searchresults.append('ownrating')
		if len(self.parserListOfRelatedMovies()) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - souvisejici - NE\n')
			searchresults.append('souvisejici')
		if len(self.parserListOfSimilarMovies()) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - podobne - NE\n')
			searchresults.append('podobne')
		if len(self.parserListOfSeries()) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - serie - NE\n')
			searchresults.append('serie')
		if len(self.parserListOfEpisodes()) == 0:
			LogCSFD.WriteToFile('[CSFD] parserFunctionExists - epizody - NE\n')
			searchresults.append('epizody')
		LogCSFD.WriteToFile('[CSFD] parserFunctionExists - konec\n')
		return searchresults

	def parserListOfTVMovies(self, deleteDuplicity=False):
		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - zacatek\n')
		searchresults = []
		searchresults1 = ParserConstCSFD.parserListOfTVMoviesLimitMask.findall(self.inhtml)
		if searchresults1 is not None:
			for x in searchresults1:
				items = ParserConstCSFD.parserListOfTVMoviesSearchMask.search(x)
				if items is not None:
					finded = False
					if deleteDuplicity:
						for y in searchresults:
							if y[0] == items.group(1) and y[1] == items.group(3):
								finded = True
								break

					if not finded:
						searchresults.append((items.group(1), items.group(3), items.group(4), items.group(2)))

		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - konec\n')
		return searchresults

	def parserPrivateComment(self):
		LogCSFD.WriteToFile('[CSFD] parserPrivateComment - zacatek\n')
		comment = None
		result = ParserConstCSFD.parserPrivateCommentLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstCSFD.parserPrivateCommentSearchMask.search(result.group(1))
			if result1 is not None:
				comment = strUni(char2Allowchar(ParserConstCSFD.parserhtmltags.sub('', result1.group(1).replace('\n', ' ').replace('…', '...').replace('<br>', '\n').replace('<br />', '\n').strip())))
				if comment == '':
					comment = None
		LogCSFD.WriteToFile('[CSFD] parserPrivateComment - konec\n')
		return comment

	def printHTML(self):
		LogCSFD.WriteToFile('[CSFD] printHTML - zacatek\n')
		LogCSFD.WriteToFileWithoutTime(self.inhtml)
		LogCSFD.WriteToFile('[CSFD] printHTML - konec\n')

	def resetValues(self):
		LogCSFD.WriteToFile('[CSFD] resetValues - zacatek\n')
		self.inhtml = ''
		self.inhtml_script = ''
		LogCSFD.WriteToFile('[CSFD] resetValues - konec\n')


ParserCSFD = CSFDParser()
ParserOstCSFD = CSFDParser()
ParserVideoCSFD = CSFDParser()
ParserGallCSFD = CSFDParser()
ParserTVCSFD = CSFDParser()

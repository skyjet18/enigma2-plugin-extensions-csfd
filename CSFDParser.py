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
TV_stations_delete_const = [
	' (Preladte)',
	' Preladte',
	' (Czech/Slovak)',
	' Czech/Slovak',
	' CZECH-SLOVAK',
	' (Hungary/Czech)',
	' Hungary/Czech',
	' (International)',
	' International',
	' (Czechia)',
	' Czechia',
	' (Central Europe)',
	' Central Europe',
	' (Eastern Europe)',
	' Eastern Europe',
	' (Europe)',
	' Europe',
	' (Czech)',
	' Czech',
	' - Czech',
	' CEE',
	' INT',
	' (CE)',
	' CE',
	' JM',
	' SM',
	' CZE',
	' CZ',
	' BG',
	' | T2',
	' +1'
]

typeOfMovie = [
	('(video film)', _('Video film')),
	('(TV film)', _('TV film')),
	('(TV seriál)', _('TV seriál')),
	('(TV pořad)', _('TV pořad')),
	('(divadelní záznam)', _('Divadelní záznam')),
	('(koncert)', _('Koncert')),
	('(studentský film)', _('Studentský film')),
	('(amatérský film)', _('Amatérský film')),
	('(hudební videoklip)', _('Hudební videoklip')),
	('(série)', _('Seriál - série')),
	('(epizoda)', _('Seriál - epizoda'))
]

TV_stations_menu_const = [
	('1', 'HBO'), ('1', 'HBO HD'),
	('2', 'Nova'), ('2', 'Nova HD'), ('2', 'TV Nova'), ('2', 'TV Nova HD'), ('2', 'Nova TV'), ('2', 'Nova TV HD'),
	('3', 'Prima'), ('3', 'Prima TV'), ('3', 'Prima TV HD'), ('3', 'Prima HD'), ('3', 'TV Prima'), ('3', 'TV Prima HD'), ('3', 'FTV Prima'), ('3', 'FTV Prima HD'),
	('3', 'Prima Family'), ('3', 'Prima Family HD'),
	('4', 'ČT1'), ('4', 'ČT 1'),
	('4', 'ČT1 HD'), ('4', 'ČT 1 HD'), ('4', 'CT 1 HD new'), ('4', 'ČT HD'),
	('5', 'ČT2'), ('5', 'ČT 2'),
	('5', 'ČT2 HD'), ('5', 'ČT 2 HD'), ('5', 'CT 2 HD new'),
	('6', 'Markíza'), ('6', 'Markíza HD'), ('6', 'TV Markíza'), ('6', 'TV Markíza HD'), ('6', 'Markíza TV'), ('6', 'Markíza TV HD'),
	('6', 'Markíza'), ('6', 'Markíza HD'), ('6', 'TV Markíza'), ('6', 'TV Markíza HD'), ('6', 'Markíza TV'), ('6', 'Markíza TV HD'),
	('7', 'JOJ'), ('7', 'JOJ HD'), ('7', 'TV JOJ'), ('7', 'TV JOJ HD'), ('7', 'JOJ TV'), ('7', 'JOJ TV HD'),
	('8', 'HBO2'), ('8', 'HBO 2'), ('8', 'HBO2 HD'), ('8', 'HBO 2 HD'),
	('9', 'Jednotka'), ('9', 'STV1'), ('9', 'STV 1'),
	('9', 'JEDNOTKA HD'), ('9', 'STV1 HD'), ('9', 'STV 1 HD'), ('9', 'STV HD'),
	('10', 'Dvojka'), ('10', 'STV2'), ('10', 'STV 2'),
	('10', 'Dvojka HD'), ('10', 'STV2 HD'), ('10', 'STV 2 HD'),
	('12', 'AXN'), ('12', 'AXN HD'), ('12', 'AXN CS'),
	('13', 'Cinemax'), ('13', 'Cinemax 1'), ('13', 'Cinemax HD'), ('13', 'Cinemax 1 HD'),
	('14', 'FilmBox'),
	('15', 'Film+'), ('15', 'Film +'), ('15', 'FilmPlus'), ('15', 'Film Plus'), ('15', 'Minimax/FilmPlus'),
	('16', 'CSfilm'), ('16', 'CS Film'), ('16', 'CS Mini/CS Film/Horor Film'), ('16', 'CS Film/CS Mini'), ('16', 'CSFilm/CSMini'),
	('17', 'MGM'), ('17', 'MGM HD'),
	('18', 'HBO Comedy'), ('18', 'HBO Comedy HD'),
	('19', 'Nova Cinema'), ('19', 'Nova Cinema HD'),
	('20', 'FilmBox Plus'), ('20', 'FilmBox+'),
	('22', 'Cinemax2'), ('22', 'Cinemax 2'), ('22', 'Cinemax2 HD'), ('22', 'Cinemax 2 HD'),
	('24', 'Barrandov'), ('24', 'TV Barrandov'), ('24', 'Barrandov HD'), ('24', 'TV Barrandov HD'),
	('25', 'Plus'), ('25', 'Plus HD'), ('25', 'JOJ Plus'), ('25', 'JOJ Plus HD'),
	('26', 'Prima Cool'), ('26', 'Prima Cool HD'),
	('27', 'Doma'), ('27', 'Doma HD'), ('27', 'TV Doma'), ('27', 'TV Doma HD'), ('27', 'Doma TV'), ('27', 'Doma TV HD'),
	('28', 'Universal Channel'), ('28', 'Universal'), ('28', 'UNI CZSK'),
	('30', 'Disney Channel'),
	('31', 'Kino CS'), ('31', 'KinoCS'),
	('32', 'Doku CS'),
	('33', 'Prima Love'), ('33', 'Prima Love HD'),
	('34', 'Minimax'), ('34', 'Minimax/Animax'), ('34', 'Minimax / Animax'), ('34', 'Minimax/FilmPlus'),
	('37', 'Discovery Channel'), ('37', 'Discovery Channel HD'), ('37', 'Discovery'), ('37', 'Discovery HD'),
	('38', 'History Channel'), ('38', 'History Chnl'), ('38', 'History channel'), ('38', 'History'), ('38', 'History Channel HD'), ('38', 'History Chnl HD'), ('38', 'History channel HD'), ('38', 'History HD'),
	('39', 'Spektrum'), ('39', 'Spektrum HD'),
	('40', 'Animal Planet'), ('40', 'Animal Planet HD'),
	('41', 'Filmbox Family'), ('41', 'FilmBox Family'),
	('42', 'Viasat Nature'),
	('43', 'Viasat Explorer'), ('43', 'Viasat Explorer / Spice'), ('43', 'Viasat Explorer/Spice'),
	('44', 'Viasat History'),
	('45', 'Viasat HD'),
	('46', 'Film Europe Channel'),
	('48', 'Fanda'), ('48', 'Fanda HD'), ('48', 'Fanda TV'), ('48', 'Fanda TV HD'),
	('49', 'Animax'), ('49', 'Minimax/Animax'), ('49', 'Minimax / Animax'),
	('50', 'Discovery Science'), ('50', 'Discovery Science Channel'),
	('51', 'Discovery World'), ('51', 'Discovery World Channel'),
	('52', 'JimJam'), ('52', 'Jim Jam'),
	('53', 'Spektrum Home'),
	('54', 'Dajto'), ('54', 'Dajto HD'), ('54', 'TV Dajto'), ('54', 'TV Dajto HD'),
	('55', 'National Geographic'), ('55', 'Nat Geo'), ('55', 'NatGeo'),
	('56', 'National Geographic Wild'), ('56', 'Nat Geo Wild'), ('56', 'NatGeo Wild'), ('56', 'National Geographic Wild HD'), ('56', 'Nat Geo Wild HD'), ('56', 'NatGeo Wild HD'),
	('57', 'CBS Drama'),
	('58', 'Smíchov'), ('58', 'Smíchov HD'),
	('60', 'Prima Zoom'), ('60', 'Prima Zoom HD'),
	('61', 'Telka'),
	('63', 'Wau'), ('63', 'Wau HD'),
	('64', 'ČT :D'), ('64', 'ČT:D'), ('64', 'CT:D / CT art'), ('64', 'CT:D/CT art'),
	('65', 'ČT art'), ('65', 'ČTart'), ('65', 'CT:D / CT art'), ('65', 'CT:D/CT art'),
	('66', 'AXN Black'),
	('67', 'AXN White'),
	('68', 'Megamax'),
	('69', 'CBS Reality'),
	('70', 'Horor Film'), ('70', 'CS Mini/CS Film/Horor Film'),
	('71', 'National Geographic HD'), ('71', 'Nat Geo HD'), ('71', 'NatGeo HD'),
	('72', 'Travel Channel'), ('72', 'Travel Channel HD'),
	('73', 'Nickelodeon'), ('73', 'Nickelodeon HD'),
	('74', 'MTV CZ'), ('74', 'MTV'),
	('75', 'Filmbox Extra'), ('75', 'FilmBox Extra'),
	('76', 'Kino Svět'),
	('77', 'ID Xtra'),
	('78', 'AMC'),
	('79', 'Filmbox Premium'),
	('80', 'RiK'), ('80', 'TV RiK'), ('80', 'RiK TV'),
	('81', 'Relax-Pohoda'), ('81', 'RELAX Pohoda'), ('81', 'RELAX - Pohoda'),
	('82', 'Rebel'),
	('83', 'Kino Barrandov'), ('83', 'KinoBarrandov'),
	('84', 'Barrandov Plus'), ('84', 'TV Barrandov Plus'), ('84', 'Barrandov Plus HD'), ('84', 'TV Barrandov Plus HD'), ('84', 'BARRANDOV PLUS TV'),
	('85', 'Discovery HD Showcase'), ('85', 'Discovery Showcase HD'),
	('86', 'JOJ Cinema'), ('86', 'JOJ Cinema HD'),
	('87', 'FilmBox Extra HD'),
	('88', 'Prima Max'),
	('89', 'Comedy Central Extra'),
	('90', 'Prima Comedy Central'), ('90', 'Prima Comedy'),
	('91', 'Nova International'),
	('92', 'Markíza International'),
	('93', 'HBO3'),
	('94', 'RTL'),
	('95', 'Sat.1'),
	('96', 'PRO7'),
	('97', 'Kabel1'),
	('98', 'RTL 2'),
	('99', 'VOX'),
	('100', 'RTL Nitro'),
	('101', 'Super RTL'),
	('102', 'TELE 5'),
	('103', 'Sixx'),
	('104', 'ProSieben MAXX'),
	('105', 'ORF 1'),
	('106', 'ORF 2'),
	('107', 'Das Erste'),
	('108', 'Discovery Turbo Xtra'),
	('109', 'ZDF'),
	('110', 'ZDF Neo'),
	('111', 'TLC'),
	('112', 'KiKa'),
	('113', '3Sat'),
	('114', 'E! Entertainment'),
	('115', 'arte'),
	('116', 'RTL plus'),
	('117', 'JOJ Family'),
	('118', 'Sat.1 Gold'), ('118', 'Sat1 Gold'), ('118', 'Sat 1 Gold'),
	('119', 'Kabel Eins Doku'),
	('120', 'Československo HD'), ('120', 'Ceskoslovensko HD'), ('120', 'Československo'), ('120', 'Ceskoslovensko'),
	('121', 'Festival HD'),
	('122', 'Barrandov Family'),
	('123', 'Nova Action'),
	('124', 'Nova Gold'),
	('125', 'Nova 2'), ('125', 'Nova2'),
	('126', 'Prima Plus')
]

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
		self.parserYear2 = re.compile('\(19\\d{2}\)|\(20\\d{2}\)', re.DOTALL)
		self.parserDate = re.compile('\\d{2}\\.\\d{2}\\.\\d{4}', re.DOTALL)
		self.parserNumbers = re.compile(' \\d+', re.DOTALL)
		self.parserRomanNumerals = re.compile('\\b(?!LLC)(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.DOTALL)
		self.parserTestHTMLSearchMask = re.compile('html', self.ccFindCond)
		self.parserTestCSFDFindingSearchMask = re.compile('SFD.cz', self.ccFindCond)

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
							entitydict[key1] = name2codepoint[x1.group(1)]
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

			for key, codepoint in list(entitydict.items()):
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
		results = ParserConstCSFD.parserYear2.findall(name)
		if results is not None:
			for value in results:
				LogCSFD.WriteToFile('[CSFD] parserGetYears - have year2 %s\n' % value[1:-1])
				searchresults.append(value[1:-1])
		else:
			results = ParserConstCSFD.parserYear.findall(name)
			if results is not None:
				for value in results:
					LogCSFD.WriteToFile('[CSFD] parserGetYears - have year %s\n' % value)
					searchresults.append(value)

		LogCSFD.WriteToFile('[CSFD] parserGetYears - konec\n')
		return list(set(searchresults))

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
			typeMovie = movie_info["type"] + ' '
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
			Obsahtext = self.delHTMLtags(movie_info["plot"]["text"] + '\n(' + movie_info["plot"]["source_name"] + ')' )
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
		pocet_hodnoceni = None
		LogCSFD.WriteToFile('[CSFD] parserRatingNumber - konec\n')
		return pocet_hodnoceni

	def parserUserComments(self, data ):
		LogCSFD.WriteToFile('[CSFD] parserUserComments - zacatek\n')
		searchresults = []
		
		for comment in data["comments"]:
			comment_text = self.delHTMLtags( comment["text"] )
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
					searchresults.append( ( self.delHTMLtags( trivia["text"] ), trivia["source_user"]["nick"]) )
				except:
					pass

		LogCSFD.WriteToFile('[CSFD] parserInterest - konec\n')
		return searchresults

		LogCSFD.WriteToFile('[CSFD] parserInterestTypesAndNumbers - konec\n')
		return searchresults

	def parserInterestTypesAndNumbers(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestTypesAndNumbers - zacatek\n')
		# searchresults.append( (url, name, count) )
		searchresults = None
		LogCSFD.WriteToFile('[CSFD] parserInterestTypesAndNumbers - konec\n')
		return searchresults

	def parserInterestSelectedTypeAndNumber(self):
		LogCSFD.WriteToFile('[CSFD] parserInterestSelectedTypeAndNumber - zacatek\n')
		url = None
		name = ''
		number = ''
		LogCSFD.WriteToFile('[CSFD] parserInterestSelectedTypeAndNumber - konec\n')
		return (url, name, number)

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
		# searchresults.append( (movie_id, movie_name, year, color_class) )
		searchresults = []
		LogCSFD.WriteToFile('[CSFD] parserListOfTVMovies - konec\n')
		return searchresults

	def parserPrivateComment(self):
		LogCSFD.WriteToFile('[CSFD] parserPrivateComment - zacatek\n')
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
		
	def setJson(self, data):
		self.json_data = data
		
	def testJson(self):
		if "http_error" in self.json_data or "internal_error" in self.json_data:
			return False
		
		return True


ParserCSFD = CSFDParser()
ParserOstCSFD = CSFDParser()
ParserVideoCSFD = CSFDParser()
ParserGallCSFD = CSFDParser()
ParserTVCSFD = CSFDParser()

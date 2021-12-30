# -*- coding: utf-8 -*-

from CSFDLog import LogCSFD
from CSFDSettings2 import config
import re, htmlentitydefs

class IMDBConstParser:

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] IMDBConstParser - init - zacatek\n')
		self.ccFindCond = re.DOTALL | re.IGNORECASE
		self.parserhtmltags = re.compile('<.*?>')
		self.parserHTML2utf8_1 = re.compile('&([^#][A-Za-z]{1,5}?);')
		self.parserHTML2utf8_2 = re.compile('&#x([0-9A-Fa-f]{2,2}?);')
		self.parserHTML2utf8_3 = re.compile('&#(\\d{1,5}?);')
		self.parserYear = re.compile('19\\d{2}|20\\d{2}|21\\d{2}', re.DOTALL)
		self.parserDate = re.compile('\\d{2}\\.\\d{2}\\.\\d{4}', re.DOTALL)
		self.parserNumbers = re.compile(' \\d+', re.DOTALL)
		self.parserRomanNumerals = re.compile('\\b(?!LLC)(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.DOTALL)
		self.parserTestIMDBFindingSearchMask = re.compile("<meta property='og:site_name' content='IMDb' \\/>", self.ccFindCond)
		self.parserIMDBRatingStarsLimitMask = re.compile('<div class="ratingValue">(.*?)</div>', self.ccFindCond)
		self.parserIMDBRatingStarsSearchMask = re.compile('itemprop="ratingValue">(.*?)<', self.ccFindCond)
		self.parserIMDBRatingNumberLimitMask = re.compile('<div class="ratingValue">.*?</div>(.*?)</div>', self.ccFindCond)
		self.parserIMDBRatingNumberSearchMask = re.compile('itemprop="ratingCount">(.*?)<', self.ccFindCond)
		self.parserMetacriticRatingStarsLimitMask = re.compile('<div class="metacriticScore(.*?)</div>', self.ccFindCond)
		self.parserMetacriticRatingStarsSearchMask = re.compile('<span>(.*?)</span>', self.ccFindCond)
		self.parserMetacriticRatingNumberLimitMask = re.compile('<div class="star-box-details"(.*?)</div>', self.ccFindCond)
		self.parserMetacriticRatingNumberSearchMask = re.compile('Metascore: <a href="criticreviews.*?<a href="criticreviews.*?title=".*?>(.*?)<', self.ccFindCond)
		LogCSFD.WriteToFile('[CSFD] IMDBConstParser - init - konec\n')


ParserConstIMDB = IMDBConstParser()

class IMDBParser:

	def __init__(self):
		LogCSFD.WriteToFile('[CSFD] IMDBParser - init - zacatek\n')
		self.inhtml = ''
		LogCSFD.WriteToFile('[CSFD] IMDBParser - init - konec\n')

	def setParserHTML(self, inhtml):
		self.inhtml = inhtml

	def getParserHTML(self):
		return self.inhtml

	def HTML2utf8(self, inhtml, del_script=True):
		if del_script:
			inhtml = re.subn('<(script).*?</\\1>(?s)', '', inhtml)[0]
		entitydict = {}
		entities1 = ParserConstIMDB.parserHTML2utf8_1.finditer(inhtml)
		if entities1 is not None:
			for x1 in entities1:
				key1 = x1.group(0)
				if key1 not in entitydict:
					try:
						entitydict[key1] = htmlentitydefs.name2codepoint[x1.group(1)]
					except KeyError:
						pass

		entities2 = ParserConstIMDB.parserHTML2utf8_2.finditer(inhtml)
		if entities2 is not None:
			for x2 in entities2:
				key2 = x2.group(0)
				if key2 not in entitydict:
					entitydict[key2] = '%d' % int(key2[3:5], 16)

		entities3 = ParserConstIMDB.parserHTML2utf8_3.finditer(inhtml)
		if entities3 is not None:
			for x3 in entities3:
				key3 = x3.group(0)
				if key3 not in entitydict:
					entitydict[key3] = x3.group(1)

		for key, codepoint in entitydict.items():
			inhtml = inhtml.replace(key, unichr(int(codepoint)).encode('utf8'))

		return inhtml

	def setHTML2utf8(self, inhtml, del_script=True):
		self.inhtml = self.HTML2utf8(inhtml, del_script)
		return self.inhtml

	def delHTMLtags(self, string):
		return ParserConstIMDB.parserhtmltags.sub('', string)

	def parserGetRomanNumbers(self, name):
		searchresults = []
		results = ParserConstIMDB.parserRomanNumerals.findall(name)
		if results is not None:
			for value in results:
				vysl = value[0] + value[1] + value[2]
				searchresults.append(vysl)

		return searchresults

	def parserGetNumbers(self, name):
		searchresults = []
		results = ParserConstIMDB.parserNumbers.findall(name)
		if results is not None:
			for value in results:
				searchresults.append(value.strip())

		return searchresults

	def parserGetYears(self, name):
		LogCSFD.WriteToFile('[CSFD] IMDB parserGetYears - zacatek\n')
		searchresults = []
		results = ParserConstIMDB.parserYear.findall(name)
		if results is not None:
			for value in results:
				searchresults.append(value)

		LogCSFD.WriteToFile('[CSFD] IMDB parserGetYears - konec\n')
		return searchresults

	def parserTestIMDBFinding(self):
		LogCSFD.WriteToFile('[CSFD] IMDB parserTestIMDBFinding - zacatek\n')
		if ParserConstIMDB.parserTestIMDBFindingSearchMask.search(self.inhtml) is not None:
			LogCSFD.WriteToFile('[CSFD] IMDB parserTestIMDBFinding - True - konec\n')
			return True
		else:
			LogCSFD.WriteToFile('[CSFD] IMDB parserTestIMDBFinding - False - konec\n')
			return False
			return

	def parserIMDBRatingStars(self):
		LogCSFD.WriteToFile('[CSFD] IMDB parserIMDBRatingStars - zacatek\n')
		ratingstars = -1
		result = ParserConstIMDB.parserIMDBRatingStarsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstIMDB.parserIMDBRatingStarsSearchMask.search(result.group(1))
			if result1 is not None:
				sss = ParserConstIMDB.parserhtmltags.sub('', result1.group(1).replace('\xa0', '').strip())
				if sss != '':
					try:
						ratingstars = int(10 * float(sss.replace(',', '.')))
					except ValueError:
						ratingstars = -1

		LogCSFD.WriteToFile('[CSFD] IMDB parserIMDBRatingStars - konec\n')
		return ratingstars

	def parserMetacriticRatingStars(self):
		LogCSFD.WriteToFile('[CSFD] IMDB parserMetacriticRatingStars - zacatek\n')
		ratingstars = -1
		result = ParserConstIMDB.parserMetacriticRatingStarsLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstIMDB.parserMetacriticRatingStarsSearchMask.search(result.group(1))
			if result1 is not None:
				sss = ParserConstIMDB.parserhtmltags.sub('', result1.group(1).replace('\xa0', '').strip())
				if sss != '':
					try:
						ratingstars = int(10 * round(float(sss.replace(',', '.')) / 10, 1))
					except ValueError:
						ratingstars = -1

		LogCSFD.WriteToFile('[CSFD] IMDB parserMetacriticRatingStars - konec\n')
		return ratingstars

	def parserIMDBRatingNumber(self):
		LogCSFD.WriteToFile('[CSFD] IMDB parserIMDBRatingNumber - zacatek\n')
		pocet = None
		result = ParserConstIMDB.parserIMDBRatingNumberLimitMask.search(self.inhtml)
		if result is not None:
			result1 = ParserConstIMDB.parserIMDBRatingNumberSearchMask.search(result.group(1))
			if result1 is not None:
				sss = result1.group(1).replace('(', '').replace(')', '').replace('\xa0', '').replace(' ', '').replace(',', '').replace('.', '').strip()
				try:
					pocet = int(sss)
				except ValueError:
					LogCSFD.WriteToFile('[CSFD] IMDB parserIMDBRatingNumber - chyba\n')
					pocet = None

		LogCSFD.WriteToFile('[CSFD] IMDB parserIMDBRatingNumber - konec\n')
		return pocet

	def parserMetacriticRatingNumber(self):
		LogCSFD.WriteToFile('[CSFD] IMDB parserMetacriticRatingNumber - zacatek\n')
		pocet = None
		LogCSFD.WriteToFile('[CSFD] IMDB parserMetacriticRatingNumber - konec\n')
		return pocet

	def resetValues(self):
		LogCSFD.WriteToFile('[CSFD] IMDB resetValues - zacatek\n')
		self.inhtml = ''
		LogCSFD.WriteToFile('[CSFD] IMDB resetValues - konec\n')


ParserIMDB = IMDBParser()

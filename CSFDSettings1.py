# -*- coding: utf-8 -*-

defaultCSFDCookies = {'cookies-agreement': '1'}

class CSFDGlobalVarDef:

	def __init__(self):
		self.CSFDcur = 1
		self.CSFDeventID_EPG = 0
		self.CSFDeventID_REF = ''
		self.CSFDCookies = defaultCSFDCookies
		self.CSFDCookiesUL2 = ''
		self.IMDBexist = False
		self.AudioSelectionexist = False
		self.OpenSSLexist = False
		self.OpenSSLcontext = False
		self.WebDownload = 0
		self.TVTimer_channName = ''
		self.Session = None
		self.EventName = ''
		self.CallBackNeeded = False
		self.EPG = ''
		self.SourceEPG = False
		self.DVBchannel = ''
		self.CSFDDesktopWidth = 720
		self.CSFDlang = None
		self.CSFDadresarTMP = '/tmp/'
		self.CSFDBoxType = None
		self.CSFDImageType = ''
		self.CSFDImageCompatibility = 255
		self.CSFDoeVersion = 'unknown'
		self.CSFDEnigmaVersion = '3'
		self.CSFDInstallCommand = 'opkg'
		self.BTParameters = False
		self.HTTPSWorkingTwistedWeb = False
		self.HTTP = 'http'
		self.IsTwistedWithCookies = True
		self.ParalelDownloadProcedure = None
		self.ParalelDownloadPage = ''
		return

	def getTVTimer_channName(self):
		return self.TVTimer_channName

	def setTVTimer_channName(self, TVTimer_channName):
		self.TVTimer_channName = TVTimer_channName

	def getOpenSSLexist(self):
		return self.OpenSSLexist

	def setOpenSSLexist(self, OpenSSLexist):
		self.OpenSSLexist = OpenSSLexist

	def getOpenSSLcontext(self):
		return self.OpenSSLcontext

	def setOpenSSLcontext(self, OpenSSLcontext):
		self.OpenSSLcontext = OpenSSLcontext

	def getAudioSelectionexist(self):
		return self.AudioSelectionexist

	def setAudioSelectionexist(self, AudioSelectionexist):
		self.AudioSelectionexist = AudioSelectionexist

	def getIMDBexist(self):
		return self.IMDBexist

	def setIMDBexist(self, IMDBexist):
		self.IMDBexist = IMDBexist

	def getWebDownload(self):
		return self.WebDownload

	def setWebDownload(self, WebDownload):
		self.WebDownload = WebDownload

	def getCSFDCookies(self):
		return self.CSFDCookies

	def setCSFDCookies(self, CSFDCookies):
		self.CSFDCookies = CSFDCookies

	def resetCSFDCookies(self):
		self.CSFDCookies = defaultCSFDCookies

	def getCSFDCookiesUL2(self):
		return self.CSFDCookiesUL2

	def setCSFDCookiesUL2(self, CSFDCookiesUL2):
		self.CSFDCookiesUL2 = CSFDCookiesUL2

	def resetCSFDCookiesUL2(self):
		self.CSFDCookiesUL2 = ''

	def getCSFDcur(self):
		return self.CSFDcur

	def setCSFDcur(self, cur):
		self.CSFDcur = cur

	def getCSFDeventID_EPG(self):
		return self.CSFDeventID_EPG

	def setCSFDeventID_EPG(self, eventID_EPG):
		self.CSFDeventID_EPG = eventID_EPG

	def getCSFDeventID_REF(self):
		return self.CSFDeventID_REF

	def setCSFDeventID_REF(self, eventID_REF):
		self.CSFDeventID_REF = eventID_REF

	def getSession(self):
		return self.Session

	def setSession(self, Session):
		self.Session = Session

	def getEventName(self):
		return self.EventName

	def setEventName(self, EventName):
		self.EventName = EventName

	def getCallBackNeeded(self):
		return self.CallBackNeeded

	def setCallBackNeeded(self, CallBackNeeded):
		self.CallBackNeeded = CallBackNeeded

	def getEPG(self):
		return self.EPG

	def setEPG(self, EPG):
		self.EPG = EPG

	def getSourceEPG(self):
		return self.SourceEPG

	def setSourceEPG(self, SourceEPG):
		self.SourceEPG = SourceEPG

	def getDVBchannel(self):
		return self.DVBchannel

	def setDVBchannel(self, DVBchannel):
		self.DVBchannel = DVBchannel

	def getCSFDDesktopWidth(self):
		return self.CSFDDesktopWidth

	def setCSFDDesktopWidth(self, CSFDDesktopWidth):
		self.CSFDDesktopWidth = CSFDDesktopWidth

	def getCSFDlang(self):
		return self.CSFDlang

	def setCSFDlang(self, CSFDlang):
		self.CSFDlang = CSFDlang

	def getCSFDadresarTMP(self):
		return self.CSFDadresarTMP

	def setCSFDadresarTMP(self, CSFDadresarTMP):
		self.CSFDadresarTMP = CSFDadresarTMP

	def getCSFDBoxType(self):
		return self.CSFDBoxType

	def setCSFDBoxType(self, CSFDBoxType):
		self.CSFDBoxType = CSFDBoxType

	def getCSFDImageType(self):
		return self.CSFDImageType

	def setCSFDImageType(self, CSFDImageType):
		self.CSFDImageType = CSFDImageType

	def getCSFDImageCompatibility(self):
		return self.CSFDImageCompatibility

	def setCSFDImageCompatibility(self, CSFDImageCompatibility):
		self.CSFDImageCompatibility = CSFDImageCompatibility

	def getCSFDoeVersion(self):
		return self.CSFDoeVersion

	def setCSFDoeVersion(self, CSFDoeVersion):
		self.CSFDoeVersion = CSFDoeVersion

	def getCSFDEnigmaVersion(self):
		return self.CSFDEnigmaVersion

	def setCSFDEnigmaVersion(self, CSFDEnigmaVersion):
		self.CSFDEnigmaVersion = CSFDEnigmaVersion

	def getCSFDInstallCommand(self):
		return self.CSFDInstallCommand

	def setCSFDInstallCommand(self, CSFDInstallCommand):
		self.CSFDInstallCommand = CSFDInstallCommand

	def getBTParameters(self):
		return self.BTParameters

	def setBTParameters(self, BTParameters):
		self.BTParameters = BTParameters

	def getHTTPSWorkingTwistedWeb(self):
		return self.HTTPSWorkingTwistedWeb

	def setHTTPSWorkingTwistedWeb(self, HTTPSWorkingTwistedWeb):
		self.HTTPSWorkingTwistedWeb = HTTPSWorkingTwistedWeb

	def getHTTP(self):
		return self.HTTP

	def setHTTP(self, HTTP):
		self.HTTP = HTTP

	def getIsTwistedWithCookies(self):
		return self.IsTwistedWithCookies

	def setIsTwistedWithCookies(self, IsTwistedWithCookies):
		self.IsTwistedWithCookies = IsTwistedWithCookies

	def getParalelDownload(self):
		return (
		 self.ParalelDownloadProcedure, self.ParalelDownloadPage)

	def setParalelDownload(self, ParalelDownloadProcedure, ParalelDownloadPage):
		self.ParalelDownloadProcedure = ParalelDownloadProcedure
		self.ParalelDownloadPage = ParalelDownloadPage


CSFDGlobalVar = CSFDGlobalVarDef()


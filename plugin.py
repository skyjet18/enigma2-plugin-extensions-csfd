# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor
from enigma import eTimer, eEPGCache, eServiceCenter
from .CSFDLog import LogCSFD
from .CSFDSettings1 import CSFDGlobalVar
from .CSFDSettings2 import _, config
from .CSFDImdb import InitIMDBchanges
from .CSFDTools import CSFDHelpableActionMapChng
from Screens.Screen import Screen
from Screens.EpgSelection import EPGSelection
from Screens.EventView import EventViewEPGSelect, EventViewSimple
from Screens.EventView import EventViewSimple as puvEventViewSimple
from Screens.EventView import EventViewEPGSelect as puvEventViewEPGSelect
from Screens.InfoBar import InfoBar
from Screens.InfoBarGenerics import InfoBarEPG
from Screens.MovieSelection import MovieSelection
from ServiceReference import ServiceReference
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.EpgList import EPGList, EPG_TYPE_SIMILAR, EPG_TYPE_MULTI
from Components.config import configfile
from .compat import eConnectCallback
import traceback, inspect, os
LogCSFD.WriteToFile('[CSFD] Log CSFD pluginu - zacatek\n')
LogCSFD.WriteToFile('[CSFD] Log CSFD pluginu: ' + config.misc.CSFD.Version.getValue() + '  ' + config.misc.CSFD.VersionData.getValue() + '\n')
LogCSFD.WriteToFile('[CSFD] Log CSFD pluginu - konec\n')
LogCSFD.WriteToFile('[CSFD] Iniciace modulu plugin.py* - zacatek\n')
try:
	from Screens.AudioSelection import SubtitleSelection
	CSFDGlobalVar.setAudioSelectionexist(True)
except:
	CSFDGlobalVar.setAudioSelectionexist(False)

InitIMDBchanges()
if config.misc.CSFD.BackCSFDCompatibility.getValue():
	LogCSFD.WriteToFile('[CSFD] CSFD - zapnuta zpetna kompatibilita volani CSFD\n')
	from .CSFD import CSFDClass

	class CSFD(CSFDClass):

		def __init__(self, session, eventName='', callbackNeeded=False, EPG='', sourceEPG=False, DVBchannel='', *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] CSFD - puvodni volani CSFD - zacatek\n')
			CSFDClass.__init__(self, session, eventName, callbackNeeded, EPG, sourceEPG, DVBchannel, *args, **kwargs)
			LogCSFD.WriteToFile('[CSFD] CSFD - puvodni volani CSFD - konec\n')


else:
	LogCSFD.WriteToFile('[CSFD] CSFD - vypnuta zpetna kompatibilita volani CSFD\n')

	class CSFD(Screen):

		def __init__(self, session, eventName='', callbackNeeded=False, EPG='', sourceEPG=False, DVBchannel='', *args, **kwargs):
			Screen.__init__(self, session)
			LogCSFD.WriteToFile('[CSFD] CSFD - puvodni volani CSFD - zacatek\n')
			LogCSFD.WriteToFile('[CSFD] CSFD - neprovedena zadna akce - vypnuta zpetna kompatibilita\n')
			LogCSFD.WriteToFile('[CSFD] CSFD - puvodni volani CSFD - konec\n')
			self.close()


def RunCSFD(session, eventName='', callbackNeeded=False, EPG='', sourceEPG=False, DVBchannel=''):
	LogCSFD.WriteToFile('[CSFD] Spusteni CSFD - zacatek\n')
	CSFDGlobalVar.setCSFDcur(1)
	CSFDGlobalVar.setCSFDeventID_EPG(0)
	CSFDGlobalVar.setCSFDeventID_REF('')
	ret = None
	try:
		from .CSFD import CSFDClass
		ret = session.open(CSFDClass, eventName, callbackNeeded, EPG, sourceEPG, DVBchannel)
	except:
		LogCSFD.WriteToFile('[CSFD] Spusteni CSFD - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)

	LogCSFD.WriteToFile('[CSFD] Spusteni CSFD - konec\n')
	return ret


def CallCSFD(session, eventName='', callbackNeeded=False, EPG='', sourceEPG=False, DVBchannel=''):
	LogCSFD.WriteToFile('[CSFD] Externi volani CSFD pluginu - zacatek\n')
	ret = RunCSFD(session, eventName, callbackNeeded, EPG, sourceEPG, DVBchannel)
	LogCSFD.WriteToFile('[CSFD] Externi volani CSFD pluginu - konec\n')
	return ret

if CSFDGlobalVar.getCSFDImageType() == 'openatv' or CSFDGlobalVar.getCSFDImageType() == 'openvix':
	LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - ATV/VIX image\n')
	try:

		class CSFDEventViewEPGSelect(puvEventViewEPGSelect):

			def __init__(self, session, event, ref, callback=None, singleEPGCB=None, multiEPGCB=None, similarEPGCB=None, *args, **kwargs):
				try:
					puvEventViewEPGSelect.__init__(self, session, event, ref, callback=None, singleEPGCB=None, multiEPGCB=None, similarEPGCB=None, *args, **kwargs)
					self.skinName = 'EventView'
					EPG_CSFD = self.CallCSFD
					if singleEPGCB:
						self['key_red'] = Button(_('CSFD'))
						self['key_yellow'] = Button(_('Single EPG'))
						self['epgactions2'] = ActionMap(['EventViewEPGActionsATV'], {'openSingleServiceEPG': singleEPGCB, 
						   'openCSFD': EPG_CSFD})
					else:
						self['key_yellow'] = Button('')
						self['yellow'].hide()
					if multiEPGCB:
						self['key_red'] = Button(_('CSFD'))
						self['key_blue'] = Button(_('Multi EPG'))
						self['epgactions3'] = ActionMap(['EventViewEPGActionsATV'], {'openMultiServiceEPG': multiEPGCB, 
						   'openCSFD': EPG_CSFD})
					else:
						self['key_blue'] = Button('')
						self['blue'].hide()
				except:
					LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect 1 - 1 - chyba\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)
					config.misc.CSFD.ShowEPGMulti.setValue(False)
					config.misc.CSFD.ShowEPGMulti.save()
					configfile.save()

				return

			def CallCSFD(self):
				CSFDGlobalVar.setCSFDcur(1)
				CSFDGlobalVar.setCSFDeventID_EPG(0)
				CSFDGlobalVar.setCSFDeventID_REF('')
				eventName = self.event.getEventName()
				DVBchannel = self.currentService.getServiceName()
				short = self.event.getShortDescription()
				ext = self.event.getExtendedDescription()
				EPG = ''
				if short is not None and short != eventName and short != '':
					EPG = short
				if ext is not None and ext != '':
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
				RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				return


		if config.misc.CSFD.ShowInATV.getValue():
			EventViewEPGSelect = CSFDEventViewEPGSelect
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect 1 - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowEPGMulti.setValue(False)
		config.misc.CSFD.ShowEPGMulti.save()
		configfile.save()

else:
	LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - non ATV/VIX image\n')
	try:

		class CSFDEventViewEPGSelect(puvEventViewEPGSelect):

			def __init__(self, session, Event, Ref, callback=None, singleEPGCB=None, multiEPGCB=None, similarEPGCB=None, *args, **kwargs):
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - __init__ - zacatek\n')
				try:
					puvEventViewEPGSelect.__init__(self, session, Event, Ref, callback, singleEPGCB, multiEPGCB, similarEPGCB, *args, **kwargs)
					self.skinName = 'EventView'
					self['key_blue'].setText(_('CSFD'))
					EPG_CSFD = self.CallCSFD
					self['epgactions'] = ActionMap(['EventViewEPGActions'], {'openSingleServiceEPG': singleEPGCB, 
					   'openMultiServiceEPG': EPG_CSFD})
				except:
					LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect 1 - 1 - chyba\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)
					config.misc.CSFD.ShowEPGMulti.setValue(False)
					config.misc.CSFD.ShowEPGMulti.save()
					configfile.save()

				LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - __init__ - konec\n')

			def CallCSFD(self):
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - CallCSFD - zacatek\n')
				CSFDGlobalVar.setCSFDcur(1)
				CSFDGlobalVar.setCSFDeventID_EPG(0)
				CSFDGlobalVar.setCSFDeventID_REF('')
				eventName = self.event.getEventName()
				DVBchannel = self.currentService.getServiceName()
				short = self.event.getShortDescription()
				ext = self.event.getExtendedDescription()
				EPG = ''
				if short is not None and short != eventName and short != '':
					EPG = short
				if ext is not None and ext != '':
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
				RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect - CallCSFD - konec\n')
				return


		if config.misc.CSFD.ShowEPGMulti.getValue():
			EventViewEPGSelect = CSFDEventViewEPGSelect
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDEventViewEPGSelect 1 - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowEPGMulti.setValue(False)
		config.misc.CSFD.ShowEPGMulti.save()
		configfile.save()

if CSFDGlobalVar.getCSFDImageType() == 'openatv' or CSFDGlobalVar.getCSFDImageType() == 'openvix':
	LogCSFD.WriteToFile('[CSFD] CSFDopenEventView - ATV/VIX image\n')
else:
	LogCSFD.WriteToFile('[CSFD] CSFDopenEventView - non ATV/VIX image\n')
	try:
		if len(inspect.getargspec(InfoBarEPG.openEventView)[0]) == 1:
			LogCSFD.WriteToFile('[CSFD] CSFDopenEventView - funkce s 1 parametrem - nahrazeni zapnuto\n')

			def CSFDopenEventView(self):
				LogCSFD.WriteToFile('[CSFD] InfoBarEPG - CSFDopenEventView - zacatek\n')
				ref = self.session.nav.getCurrentlyPlayingServiceReference()
				self.getNowNext()
				epglist = self.epglist
				if not epglist:
					self.is_now_next = False
					epg = eEPGCache.getInstance()
					ptr = ref and ref.valid() and epg.lookupEventTime(ref, -1)
					if ptr:
						epglist.append(ptr)
						ptr = epg.lookupEventTime(ref, ptr.getBeginTime(), +1)
						if ptr:
							epglist.append(ptr)
				else:
					self.is_now_next = True
				if epglist:
					try:
						self.eventView = self.session.openWithCallback(self.closed, EventViewEPGSelect, self.epglist[0], ServiceReference(ref), self.eventViewCallback, self.openSingleServiceEPG, self.openMultiServiceEPG, self.openSimilarList)
						self.dlg_stack.append(self.eventView)
					except:
						LogCSFD.WriteToFile('[CSFD] CSFDopenEventView (ShowEPGMulti - self.eventView) - chyba\n')
						err = traceback.format_exc()
						LogCSFD.WriteToFile(err)
						config.misc.CSFD.ShowEPGMulti.setValue(False)
						config.misc.CSFD.ShowEPGMulti.save()
						configfile.save()

				else:
					print('[CSFD] no epg for the service avail.. so we show CSFD instead of eventinfo')
					serviceref = self.session.nav.getCurrentlyPlayingServiceReference()
					serviceHandler = eServiceCenter.getInstance()
					info = serviceHandler.info(serviceref)
					curevent_name = info.getName(serviceref)
					DVBchannel = ServiceReference(serviceref).getServiceName()
					EPG = ''
					eventEPG = info.getEvent(serviceref)
					if eventEPG is not None:
						short = eventEPG.getShortDescription()
						ext = eventEPG.getExtendedDescription()
						if short is not None and short != curevent_name and short != '':
							EPG = short
						if ext is not None and ext != '':
							EPG += ext
						if EPG != '':
							EPG = curevent_name + ' - ' + EPG
						RunCSFD(self.session, curevent_name, False, EPG, True, DVBchannel)
					else:
						RunCSFD(self.session, '', False, '', True, DVBchannel)
				LogCSFD.WriteToFile('[CSFD] InfoBarEPG - CSFDopenEventView - konec\n')
				return


			if config.misc.CSFD.ShowEPGMulti.getValue():
				InfoBarEPG.openEventView = CSFDopenEventView
		else:
			LogCSFD.WriteToFile('[CSFD] CSFDopenEventView - funkce s vice parametry - nahrazeni vypnuto\n')
	except:
		LogCSFD.WriteToFile('[CSFD] CSFDopenEventView (ShowEPGMulti) - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowEPGMulti.setValue(False)
		config.misc.CSFD.ShowEPGMulti.save()
		configfile.save()

	try:

		def CSFDMovieSlection_showEventInformation(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] MovieSelection - showEventInformation - zacatek\n')
			CSFDGlobalVar.setCSFDcur(1)
			CSFDGlobalVar.setCSFDeventID_EPG(0)
			CSFDGlobalVar.setCSFDeventID_REF('')
			serviceref = self.getCurrent()
			curevent_name = ''
			DVBchannel = ''
			EPG = ''
			if serviceref:
				serviceHandler = eServiceCenter.getInstance()
				info = serviceHandler.info(serviceref)
				curevent_name = info.getName(serviceref)
				DVBchannel = ServiceReference(serviceref).getServiceName()
				eventEPG = info.getEvent(serviceref)
				if eventEPG is not None:
					short = eventEPG.getShortDescription()
					ext = eventEPG.getExtendedDescription()
					if short is not None and short != curevent_name and short != '':
						EPG = short
					if ext is not None and ext != '':
						EPG += ext
					if EPG != '':
						EPG = curevent_name + ' - ' + EPG
			
			# curevent_name can be a path or file name - make some processing for better search
			if curevent_name.endswith('/'): # remove / from the end of name
				curevent_name = curevent_name[:-1]
			
			# remove path and extension from name
			curevent_name = os.path.splitext( os.path.basename( curevent_name ) )[0]
			
			# convert '.' into spaces (example: The.Simpsons.2020 -> The Simpsons 2020)
			curevent_name = curevent_name.replace('.', ' ')
			
			RunCSFD(self.session, curevent_name, False, EPG, True, DVBchannel)
			LogCSFD.WriteToFile('[CSFD] MovieSelection - showEventInformation - konec\n')
			return


		if config.misc.CSFD.ShowInMovieSelection.getValue():
			MovieSelection.showEventInformation = CSFDMovieSlection_showEventInformation
	except:
		LogCSFD.WriteToFile('[CSFD] ShowInMovieSelection - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowInMovieSelection.setValue(False)
		config.misc.CSFD.ShowInMovieSelection.save()
		configfile.save()

if CSFDGlobalVar.getCSFDImageType() == 'openatv' or CSFDGlobalVar.getCSFDImageType() == 'openvix':
	LogCSFD.WriteToFile('[CSFD] InfoBar_openIMDB - ATV/VIX image\n')
	try:

		def CSFD_InfoBarExtensions_showIMDB(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] InfoBarExtensions - showIMDB - zacatek\n')
			s = self.session.nav.getCurrentService()
			if s:
				info = s.info()
				event = info.getEvent(0)
				name = event and event.getEventName() or ''
			DVBchannel = ''
			eventName = ''
			EPG = ''
			service = self.session.nav.getCurrentService()
			if service is not None:
				info = service and service.info()
				if info is not None:
					name = info.getName()
					if name is not None and name != '':
						DVBchannel = name
					event = info and info.getEvent(0)
					if event is not None:
						eventName = event.getEventName()
						short = event.getShortDescription()
						ext = event.getExtendedDescription()
						if short is not None and short != eventName and short != '':
							EPG = short
						if ext is not None and ext != '':
							EPG += ext
						RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
					else:
						RunCSFD(self.session, '', False, '', True, DVBchannel)
			LogCSFD.WriteToFile('[CSFD] InfoBarExtensions - showIMDB - konec\n')
			return


		if config.misc.CSFD.ShowInATV.getValue():
			from Screens.InfoBarGenerics import InfoBarExtensions
			if 'showIMDB' in dir(InfoBarExtensions):
				InfoBarExtensions.showIMDB = CSFD_InfoBarExtensions_showIMDB

		def CSFD_InfoBar_openIMDB(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] InfoBar - openIMDB - zacatek\n')
			cur = self['list'].getCurrent()
			evt = cur[0]
			serviceref = cur[1]
			if not evt:
				return
			else:
				eventName = evt.getEventName()
				short = evt.getShortDescription()
				ext = evt.getExtendedDescription()
				EPG = ''
				DVBchannel = serviceref.getServiceName()
				if short is not None and short != eventName and short != '':
					EPG = short
				if ext is not None and ext != '':
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
				RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				LogCSFD.WriteToFile('[CSFD] InfoBar - openIMDB - konec\n')
				return


		if config.misc.CSFD.ShowInATV.getValue() and 'openIMDB' in dir(InfoBar):
			InfoBar.openIMDB = CSFD_InfoBar_openIMDB
	except:
		LogCSFD.WriteToFile('[CSFD] InfoBar_openIMDB - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)

else:
	LogCSFD.WriteToFile('[CSFD] CSFDEventViewSimple - non ATV/VIX image\n')
	try:

		class CSFDEventViewSimple(puvEventViewSimple):

			def __init__(self, *args, **kwargs):
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewSimple - __init__ - zacatek\n')
				try:
					puvEventViewSimple.__init__(self, *args, **kwargs)
					self.skinName = 'EventView'
					self['key_blue'].setText(_('CSFD'))
					EPG_CSFD = self.CallCSFD
					self['epgactions'] = ActionMap(['EventViewEPGActions'], {'openMultiServiceEPG': EPG_CSFD})
				except:
					LogCSFD.WriteToFile('[CSFD] ShowInEPGDetail - 1 - chyba\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)
					config.misc.CSFD.ShowInEPGDetail.setValue(False)
					config.misc.CSFD.ShowInEPGDetail.save()
					configfile.save()

				LogCSFD.WriteToFile('[CSFD] CSFDEventViewSimple - __init__ - konec\n')

			def CallCSFD(self):
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewSimple - CallCSFD - zacatek\n')
				CSFDGlobalVar.setCSFDcur(1)
				CSFDGlobalVar.setCSFDeventID_EPG(0)
				CSFDGlobalVar.setCSFDeventID_REF('')
				eventName = self.event.getEventName()
				DVBchannel = self.currentService.getServiceName()
				short = self.event.getShortDescription()
				ext = self.event.getExtendedDescription()
				EPG = ''
				if short is not None and short != eventName and short != '':
					EPG = short
				if ext is not None and ext != '':
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
				RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				LogCSFD.WriteToFile('[CSFD] CSFDEventViewSimple - CallCSFD - konec\n')
				return


		if config.misc.CSFD.ShowInEPGDetail.getValue():
			EventViewSimple = CSFDEventViewSimple
		if config.misc.CSFD.ShowInEPGDetail.getValue():
			old_EPGSelection_infoKeyPressed = EPGSelection.infoKeyPressed

		def CSFD_EPGSelection_infoKeyPressed(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] EPGSelection - infoKeyPressed - zacatek\n')
			cur = self['list'].getCurrent()
			event = cur[0]
			service = cur[1]
			if event is not None:
				if self.type != EPG_TYPE_SIMILAR:
					self.session.open(EventViewSimple, event, service, callback=self.eventViewCallback, similarEPGCB=self.openSimilarList)
				else:
					self.session.open(EventViewSimple, event, service, callback=self.eventViewCallback)
			LogCSFD.WriteToFile('[CSFD] EPGSelection - infoKeyPressed - konec\n')
			return


		if config.misc.CSFD.ShowInEPGDetail.getValue():
			EPGSelection.infoKeyPressed = CSFD_EPGSelection_infoKeyPressed
	except:
		LogCSFD.WriteToFile('[CSFD] ShowInEPGDetail - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowInEPGDetail.setValue(False)
		config.misc.CSFD.ShowInEPGDetail.save()
		configfile.save()

if CSFDGlobalVar.getCSFDImageType() == 'openatv' or CSFDGlobalVar.getCSFDImageType() == 'openvix':
	try:
		LogCSFD.WriteToFile('[CSFD] ShowInEPGList - ATV/VIX image\n')

		def CSFD_EPGSelection_openIMDb(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] EPGSelection - openIMDb - zacatek\n')
			cur = self['list'].getCurrent()
			evt = cur[0]
			serviceref = cur[1]
			if not evt:
				return
			else:
				eventName = evt.getEventName()
				short = evt.getShortDescription()
				ext = evt.getExtendedDescription()
				EPG = ''
				DVBchannel = serviceref.getServiceName()
				if short is not None and short != eventName and short != '':
					EPG = short
				if ext is not None and ext != '':
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
				RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				LogCSFD.WriteToFile('[CSFD] EPGSelection - openIMDb - konec\n')
				return


		if config.misc.CSFD.ShowInATV.getValue() and (CSFDGlobalVar.getCSFDImageType() == 'openatv' or CSFDGlobalVar.getCSFDImageType() == 'openvix'):
			if 'openIMDb' in dir(EPGSelection):
				EPGSelection.openIMDb = CSFD_EPGSelection_openIMDb
			if 'LayoutFinish' in dir(EPGSelection):
				old_EPGSelection_LayoutFinish = EPGSelection.LayoutFinish

			def CSFD_EPGSelection_LayoutFinish(self, *args, **kwargs):
				LogCSFD.WriteToFile('[CSFD] EPGSelection - LayoutFinish - zacatek\n')
				old_EPGSelection_LayoutFinish(self, *args, **kwargs)
				self['key_red'].setText(_('CSFD'))
				self['colouractions'] = CSFDHelpableActionMapChng(self, 'ColorActions',
				{
					'red': (self.redButtonPressed, _('Vyhledat akt. pořad v CSFD')), 
					'redlong': (self.redButtonPressedLong, None), 
					'green': (self.greenButtonPressed, None), 
					'greenlong': (self.greenButtonPressedLong, None), 
					'yellow': (self.yellowButtonPressed, None), 
					'blue': (self.blueButtonPressed, None), 
					'bluelong': (self.blueButtonPressedLong, None)
				}, -1)
				LogCSFD.WriteToFile('[CSFD] EPGSelection - LayoutFinish - konec\n')
				return


			if 'LayoutFinish' in dir(EPGSelection):
				EPGSelection.LayoutFinish = CSFD_EPGSelection_LayoutFinish
	except:
		LogCSFD.WriteToFile('[CSFD] ShowInEPGList - ATV/VIX image - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowInEPGList.setValue(False)
		config.misc.CSFD.ShowInEPGList.save()
		configfile.save()

else:
	try:
		LogCSFD.WriteToFile('[CSFD] ShowInEPGList - non ATV/VIX image\n')
		if config.misc.CSFD.ShowInEPGList.getValue() and 'setSortDescription' in dir(EPGSelection):
			old_EPGSelection_setSortDescription = EPGSelection.setSortDescription

		def CSFD_EPGSelection_setSortDescription(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] EPGSelection - setSortDescription - zacatek\n')
			try:
				old_EPGSelection_setSortDescription(self, *args, **kwargs)
				if not self.type == EPG_TYPE_MULTI:
					self['key_blue'].setText(_('CSFD'))
			except:
				LogCSFD.WriteToFile('[CSFD] ShowInEPGList - 1 - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)
				config.misc.CSFD.ShowInEPGList.setValue(False)
				config.misc.CSFD.ShowInEPGList.save()
				configfile.save()

			LogCSFD.WriteToFile('[CSFD] EPGSelection - setSortDescription - konec\n')


		if config.misc.CSFD.ShowInEPGList.getValue() and 'setSortDescription' in dir(EPGSelection):
			EPGSelection.setSortDescription = CSFD_EPGSelection_setSortDescription
		if (config.misc.CSFD.ShowInEPGList.getValue() or config.misc.CSFD.ShowInEPGListBlueButton.getValue()) and 'blueButtonPressed' in dir(EPGSelection):
			old_EPGSelection_blueButtonPressed = EPGSelection.blueButtonPressed

		def CSFD_EPGSelection_blueButtonPressed(self, *args, **kwargs):
			LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - zacatek\n')
			if config.misc.CSFD.ShowInEPGListBlueButton.getValue():
				LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - full blue\n')
				try:
					cur = self['list'].getCurrent()
					evt = cur[0]
					serviceref = cur[1]
					if not evt:
						LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - not evt\n')
						LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - konec\n')
						return
					eventName = evt.getEventName()
					short = evt.getShortDescription()
					ext = evt.getExtendedDescription()
					EPG = ''
					DVBchannel = serviceref.getServiceName()
					if short is not None and short != eventName and short != '':
						EPG = short
					if ext is not None and ext != '':
						EPG += ext
					if EPG != '':
						EPG = eventName + ' - ' + EPG
					RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				except:
					LogCSFD.WriteToFile('[CSFD] ShowInEPGList - non ATV/VIX image - full blue - chyba - 1\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)
					config.misc.CSFD.ShowInEPGListBlueButton.setValue(False)
					config.misc.CSFD.ShowInEPGListBlueButton.save()
					configfile.save()

			else:
				LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - not full blue\n')
				try:
					old_EPGSelection_blueButtonPressed(self, *args, **kwargs)
					if not self.type == EPG_TYPE_MULTI:
						cur = self['list'].getCurrent()
						evt = cur[0]
						serviceref = cur[1]
						if not evt:
							LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - not evt\n')
							LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - konec\n')
							return
						eventName = evt.getEventName()
						short = evt.getShortDescription()
						ext = evt.getExtendedDescription()
						EPG = ''
						DVBchannel = serviceref.getServiceName()
						if short is not None and short != eventName and short != '':
							EPG = short
						if ext is not None and ext != '':
							EPG += ext
						if EPG != '':
							EPG = eventName + ' - ' + EPG
						RunCSFD(self.session, eventName, False, EPG, True, DVBchannel)
				except:
					LogCSFD.WriteToFile('[CSFD] ShowInEPGList - non ATV/VIX image - not full blue - chyba - 1\n')
					err = traceback.format_exc()
					LogCSFD.WriteToFile(err)
					config.misc.CSFD.ShowInEPGListBlueButton.setValue(True)
					config.misc.CSFD.ShowInEPGListBlueButton.save()
					config.misc.CSFD.ShowInEPGList.setValue(False)
					config.misc.CSFD.ShowInEPGList.save()
					configfile.save()

			LogCSFD.WriteToFile('[CSFD] EPGSelection - blueButtonPressed - konec\n')
			return


		if (config.misc.CSFD.ShowInEPGList.getValue() or config.misc.CSFD.ShowInEPGListBlueButton.getValue()) and 'blueButtonPressed' in dir(EPGSelection):
			EPGSelection.blueButtonPressed = CSFD_EPGSelection_blueButtonPressed
	except:
		LogCSFD.WriteToFile('[CSFD] ShowInEPGList - non ATV/VIX image - chyba\n')
		err = traceback.format_exc()
		LogCSFD.WriteToFile(err)
		config.misc.CSFD.ShowInEPGList.setValue(False)
		config.misc.CSFD.ShowInEPGList.save()
		configfile.save()

def eventinfo(session, eventName='', **kwargs):
	LogCSFD.WriteToFile('[CSFD] eventinfo called: eventName: %s, kwargs: %s\n' %(eventName, str(kwargs)) )
	CSFDGlobalVar.setCSFDcur(1)
	CSFDGlobalVar.setCSFDeventID_EPG(0)
	CSFDGlobalVar.setCSFDeventID_REF('')
	
	if config.misc.CSFD.Info_EPG.getValue() == '0':
		EPG=''
		eventMovieSourceOfDataEPG = False
		
		try:
			event = kwargs['event']
			if event is not None:
				eventName = event.getEventName()
				short = event.getShortDescription()
				ext = event.getExtendedDescription()
				if short and short != eventName:
					EPG = short
				if ext:
					EPG += ext
				if EPG != '':
					EPG = eventName + ' - ' + EPG
					
				eventMovieSourceOfDataEPG = True
		except:
			EPG=''
			eventMovieSourceOfDataEPG = False

		try:
			DVBchannel = kwargs['service'].getServiceName()
		except:
			DVBchannel = ''
			
		RunCSFD(session, eventName, False, EPG, eventMovieSourceOfDataEPG, DVBchannel)
	elif config.misc.CSFD.Info_EPG.getValue() == '1':
		ref = session.nav.getCurrentlyPlayingServiceReference()
		from .CSFDClasses import CSFDEPGSelection
		session.open(CSFDEPGSelection, ref)
	else:
		from .CSFDClasses import CSFDChannelSelection
		session.open(CSFDChannelSelection, openPlugin=True)


def main(session, eventName='', **kwargs):
	LogCSFD.WriteToFile('[CSFD] main with eventName: %s: kwargs: %s\n' % (eventName, str(kwargs)) )
	CSFDGlobalVar.setCSFDcur(1)
	CSFDGlobalVar.setCSFDeventID_EPG(0)
	CSFDGlobalVar.setCSFDeventID_REF('')
	
	EPG = ''
	DVBchannel = ''
	eventMovieSourceOfDataEPG = False
	
	if eventName is '':
		CSFDGlobalVar.setCSFDcur(1)
		CSFDGlobalVar.setCSFDeventID_EPG(0)
		CSFDGlobalVar.setCSFDeventID_REF('')
		EPG = ''
		DVBchannel = ''
		eventMovieSourceOfDataEPG = False
		LogCSFD.WriteToFile('[CSFD] main - getServiceName\n')
		try:
			serviceref = session.nav.getCurrentlyPlayingServiceReference()
			if serviceref is not None:
				serviceHandler = eServiceCenter.getInstance()
				info = serviceHandler.info(serviceref)
				event = info.getEvent(serviceref)
				if event is not None:
					eventName = event.getEventName()
					short = event.getShortDescription()
					ext = event.getExtendedDescription()
					if short and short != eventName:
						EPG = short
					if ext:
						EPG += ext
					if EPG != '':
						EPG = eventName + ' - ' + EPG
					eventMovieSourceOfDataEPG = True
				DVBchannel = ServiceReference(serviceref).getServiceName()
		except:
			eventName = ''
			EPG = ''
			DVBchannel = ''
			eventMovieSourceOfDataEPG = False
			LogCSFD.WriteToFile('[CSFD] getCSFD - getServiceName - chyba\n')
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

	RunCSFD(session, eventName, False, EPG, eventMovieSourceOfDataEPG, DVBchannel)


def startViaMenu(menuid, **kwargs):
	if menuid == 'mainmenu':
		return [(_('Filmová databáze CSFD.cz'), main, 'csfd', 37)]
	return []


def epgfurther(session, **kwargs):
	LogCSFD.WriteToFile('[CSFD] epgfurther called\n' )
	
	try:
		selectedevent = kwargs['selectedevent']
		CSFDGlobalVar.setCSFDcur(1)
		CSFDGlobalVar.setCSFDeventID_EPG(0)
		CSFDGlobalVar.setCSFDeventID_REF('')
		eventName = selectedevent[0].getEventName()
		DVBchannel = selectedevent[1].getServiceName()
		short = selectedevent[0].getShortDescription()
		ext = selectedevent[0].getExtendedDescription()
		EPG = ''
		if short is not None and short != eventName and short != '':
			EPG = short
		if ext is not None and ext != '':
			EPG += ext
		if EPG != '':
			EPG = eventName + ' - ' + EPG
	except:
		eventName = ''
		EPG = ''
		DVBchannel = ''
		
	RunCSFD(session, eventName, False, EPG, True, DVBchannel)
	return


def Plugins(**kwargs):
	pname = 'CSFD.cz'
	pname1 = _('Vyhledat v CSFD')
	pdesc = _('Filmová databáze CSFD.cz')
	listP = []
	if config.misc.CSFD.ShowInPluginMenu.getValue():
		try:
			desc_m = PluginDescriptor(name=pname, description=pdesc, where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main, icon='csfd.png', weight=config.misc.CSFD.PriorityInMenu.getValue() - 100)
			listP.append(desc_m)
		except:
			desc_m = PluginDescriptor(name=pname, description=pdesc, where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main, icon='csfd.png')
			listP.append(desc_m)

	if config.misc.CSFD.ShowInEventInfoMenu.getValue():
		try:
			desc_m = PluginDescriptor(name=pname1, description=pdesc, where=PluginDescriptor.WHERE_EVENTINFO, fnc=eventinfo, weight=config.misc.CSFD.PriorityInMenu.getValue() - 100)
			listP.append(desc_m)
		except:
			try:
				desc_m = PluginDescriptor(name=pname1, description=pdesc, where=PluginDescriptor.WHERE_EVENTINFO, fnc=eventinfo)
				listP.append(desc_m)
			except:
				LogCSFD.WriteToFile('[CSFD] PluginDescriptor - WHERE_EVENTINFO - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)

	if config.misc.CSFD.ShowInExtensionMenu.getValue():
		try:
			desc_m = PluginDescriptor(name=pname, description=pdesc, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main, weight=config.misc.CSFD.PriorityInMenu.getValue() - 100)
			listP.append(desc_m)
		except:
			try:
				desc_m = PluginDescriptor(name=pname, description=pdesc, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)
				listP.append(desc_m)
			except:
				LogCSFD.WriteToFile('[CSFD] PluginDescriptor - WHERE_EXTENSIONSMENU - chyba\n')
				err = traceback.format_exc()
				LogCSFD.WriteToFile(err)

	if config.misc.CSFD.ShowInMenuStart.getValue():
		try:
			desc_m = PluginDescriptor(name=pname, description=pdesc, where=PluginDescriptor.WHERE_MENU, fnc=startViaMenu)
			listP.append(desc_m)
		except:
			LogCSFD.WriteToFile('[CSFD] PluginDescriptor - WHERE_MENU - chyba\n')
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

	if config.misc.CSFD.ShowInEPGSubMenu.getValue():
		try:
			desc_m = PluginDescriptor(name=pname1, description=pdesc, where=PluginDescriptor.WHERE_EVENTINFO, fnc=epgfurther)
			listP.append(desc_m)
		except:
			LogCSFD.WriteToFile('[CSFD] PluginDescriptor - WHERE_EVENTINFO - ShowInEPGSubMenu - chyba\n')
			err = traceback.format_exc()
			LogCSFD.WriteToFile(err)

	return listP


LogCSFD.WriteToFile('[CSFD] Iniciace modulu plugin.py* - konec\n')

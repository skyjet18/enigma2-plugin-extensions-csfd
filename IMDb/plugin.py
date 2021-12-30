# -*- coding: utf-8 -*-
# -*- coding: UTF-8 -*-
# emulation of IMDb plugin for calling CSFD plugin because not all plugins can call CSFD directly
# CSFD is Czech and Slovak Movie Database

from Plugins.Plugin import PluginDescriptor	 # @UnusedImport
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
import traceback

class IMDB(Screen):
	skin = """
		<screen name="IMDBemu" position="center,center" size="1,1" title="IMDB emu" >
			<widget name="key_red" position="0,0" zPosition="1" size="1,1" font="Regular;20" valign="center" halign="center" backgroundColor="#9f1313" transparent="1" />
		</screen>"""

	def __init__(self, session, eventName, callbackNeeded=False):
		Screen.__init__(self, session)
		self.session = session
		self.eventName = eventName
		self.callbackNeeded = callbackNeeded
		self.ret = None
		self["key_red"] = Button("")
		self["actions"] = ActionMap(["IMDBemu"],
		{
			"cancel": self.exit
		}, -1)
		self.onShown.append(self.CSFDemu)

	def CSFDemu(self):
		try:
			from Plugins.Extensions.CSFD.plugin import CallCSFD	 # @UnresolvedImport
			self.ret = CallCSFD(session=self.session, eventName=self.eventName, callbackNeeded=self.callbackNeeded)
		except:
			print "IMDB emulator for CSFD - error"
			err = traceback.format_exc()
			print err
			pass
		self.exit()

	def exit(self):
		if self.callbackNeeded:
			self.close(self.ret)
		else:
			self.close()

def Plugins(**kwargs):
	return []

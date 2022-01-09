# -*- coding: utf-8 -*-

from .CSFDSettings2 import config
from .CSFDLog import LogCSFD
from Components.config import configfile
from os import path as os_path, listdir as os_listdir
import traceback
LogCSFD.WriteToFile('[CSFD] SkinLoader - zacatek\n')
LogCSFD.WriteToFile('[CSFD] SkinLoader - Import Defaultniho skinu\n')
try:
	from .skins.CSFDSkin_Default import *
	LogCSFD.WriteToFile('[CSFD] SkinLoader - Import Defaultniho skinu OK\n')
except:
	err = traceback.format_exc()
	LogCSFD.WriteToFile('[CSFD] SkinLoader - Import Defaultniho skinu ERR\n')
	LogCSFD.WriteToFile(err)

moduleload = False
for module in os_listdir(os_path.join(os_path.dirname(__file__), 'skins')):
	if module == '__init__.py' or module[-3:] != '.py' or module == 'CSFDSkin_Default.py' or module[0:9] != 'CSFDSkin_':
		continue
	module = module[:-3]
	if module == 'CSFDSkin_' + config.misc.CSFD.CurrentSkin.getValue():
		LogCSFD.WriteToFile('[CSFD] SkinLoader - import - %s\n' % module)
		try:
			exec('from .%s.%s import *' % ('skins', module))
			LogCSFD.WriteToFile('[CSFD] SkinLoader - import OK - %s\n' % module)
			moduleload = True
		except:
			err = traceback.format_exc()
			LogCSFD.WriteToFile('[CSFD] SkinLoader - import ERR - %s\n' % module)
			LogCSFD.WriteToFile(err)

if not moduleload:
	LogCSFD.WriteToFile('[CSFD] SkinLoader - Nebyl nacten jiny skin nez defaultni\n')
del module
del moduleload
LogCSFD.WriteToFile('[CSFD] SKIN_Setup - zacatek\n')
try:
	SKIN_Setup()
	config.misc.CSFD.save()
	configfile.save()
except:
	err = traceback.format_exc()
	LogCSFD.WriteToFile('[CSFD] SKIN_Setup - ERR - \n')
	LogCSFD.WriteToFile(err)

LogCSFD.WriteToFile('[CSFD] SKIN_Setup - konec\n')
LogCSFD.WriteToFile('[CSFD] SkinLoader - konec\n')

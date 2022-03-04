from .CSFDSettings1 import CSFDGlobalVar

class eConnectCallbackObj:
	def __init__(self, obj=None, connectHandler=None):
		self.connectHandler = connectHandler
		self.obj = obj

	def __del__(self):
		if 'connect' not in dir(self.obj):
			if 'get' in dir(self.obj):
				self.obj.get().remove(self.connectHandler)
			else:
				self.obj.remove(self.connectHandler)
		else:
			del self.connectHandler
		self.connectHandler = None
		self.obj = None


def eConnectCallback(obj, callbackFun):
	if 'connect' in dir(obj):
		return eConnectCallbackObj(obj, obj.connect(callbackFun))
	else:
		if 'get' in dir(obj):
			obj.get().append(callbackFun)
		else:
			obj.append(callbackFun)
		return eConnectCallbackObj(obj, callbackFun)
	return eConnectCallbackObj()


def ePicloadDecodeData( ePicObj, filename ):
	if CSFDGlobalVar.getCSFDEnigmaVersion() < '4':
		if ePicObj.startDecode(str(filename), 0, 0, False) == 0:
			return ePicObj.getData()
	elif ePicObj.startDecode(str(filename), False) == 0:
		return ePicObj.getData()

	return None

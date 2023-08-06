from text2sentences import text_to_sentences
from appPublic.uniqueID import getID
import importlib

def buildDriver(tts, driverName):
	_module = importlib.import_module(driverName)
	return _module.buildDriver(tts)
	
class TTSEngine:
	"""
	Usages:
	"""
	def __init__(self, driverName):
		self.driver = buildDriver(self, driverName)
		self._connects = {}
		self._busy = False

	def setBusy(self, f):
		self._busy = f

	def connect(self, subject, func):
		if subject in ['started-sentence', 'started-word',
						'started-text', 'finished-text']:
			self._connects.update({subject:func})
	
	def disconnect(self, subject):
		if subject in ['started-sentence', 'started-word',
						'started-text', 'finished-text']:
			del self._connects[subject]
		
	def say(self, text, pos=0):
		if self.isBusy():
			print('tts is busy, do no thing')
			return
		if isinstance(text, str):
			self.current_pos = pos
			sentences = text_to_sentences(text)
		else:
			sentences = text
		self.say_sentences(sentences)

	def say_sentences(self, sentences):
		for s in sentences:
			self.driver.say(s)
		
	def notify(self, subject, *args, **kw):
		for s,f in self._connects.items():
			if s == subject:
				f(*args, **kw)

	def isBusy(self):
		return self._busy


	def stop(self):
		pass

	def pause(self):
		pass

	def resume(self):
		pass

	def startLoop(self):
		self.driver.startLoop()

	def is_in_loop(self):
		return self.driver.is_in_loop()

	def endLoop(self):
		self.driver.endLoop()
	
	def getProperty(self, name):
		return self.driver.getProperty(name)

	def setProperty(self, name, value):
		self.driver.setProperty(name, value)


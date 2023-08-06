import os
import time
from traceback import print_exc
from unitts.voice import Voice
from appPublic.background import Background
from text2sentences import text_to_sentences

class BaseDriver:
	def __init__(self, proxy):
		self._proxy = proxy
		self._tts = None
		self.sentences = []
		self.normal_voice = {}
		self.dialog_voice = {}
		self.pitch = 5
		self.language = 'zh'
		self.format = 3
		self.voice = 0
		self.cmds = []
		self._completed = True
		self.running = True
		self.task = None
		self._speaked = False
		self._speaking = False
		self.voices = self.get_voices()

	def get_voices(self):
		return []

	def set_type_voice(self, sentence):
		raise Exception('fixme')

	def backtask(self):
		print('player back task running ...')
		self.running = True
		while self.running:
			self._pump()
			time.sleep(0.01)
		print('player back task end ...')

	def is_speaking(self):
		return self._speaked

	def speak_finish(self):
		self._proxy.notify('finished-sentence')
		self._speaking = False
		self._speaked = False

	def _push(self, cmd):
		self.cmds.append(cmd)

	def isSpeaking(self):
		return self._speaked

	def _pump(self):
		if self._speaking:
			# print('tts driver is busy')
			if not self._speaked:
				self._speaked = self.isSpeaking()
			else:
				if not self.isSpeaking():
					self.speak_finish()
			return False
		if len(self.cmds) < 1:
			# print('No cmd to do')
			if self._proxy.isBusy():
				self._proxy.setBusy(False)
				self._proxy.notify('finished-text')
			return False

		self._speaking = True
		args = self.cmds.pop(0)
		print('start speak', args)
		self.command(*args)
		pos, _ = args
		self._proxy.notify('started-sentence', pos)
		return True

	def destroy(self):
		if self.task:
			self.running = False
			self.task.join()
			self.task = None
	
	def __del__(self):
		self.destroy()

	def is_in_loop(self):
		if self.task:
			return True
		return False

	def startLoop(self, *args):
		print('startLoop() called')
		self._proxy.setBusy(False)
		self.task = Background(self.backtask)
		self.task.start()

	def endLoop(self):
		print('endLoop() called')
		self.cmds = []
		self._proxy.setBusy(False)
		if self.task:
			self.running = False
			self.task.join()
			self.task = None

	def pre_command(self, sentence):
		# return sentence's start_pos and a object to use to product voice
		# self.set_type_voice(sentence)
		return sentence.start_pos, sentence.text
	
	def command(self, *args):
		raise Exception('fixme')

	def say(self, sentence):
		self._proxy.setBusy(False)
		self._completed = True
		args = self.pre_command(sentence)
		if None in args:
			return
		self._push(args)

	def stop(self):
		if self._proxy.isBusy():
			self._completed = False

	def getProperty(self, name):
		if name == 'normal_voice':
			return self.normal_voice
		if name == 'dialog_voice':
			return self.dialog_voice

		if name == 'voices':
			return Voices

		if name == 'voice':
			for v in self.voices:
				if v.id == self.voice:
					return v
			return None
		if name == 'rate':
			return self.rate
		if name == 'volume':
			return self.volume
		if name == 'pitch':
			return self.pitch
	
	def setProperty(self, name, value):
		if name == 'normal_voice':
			self.normal_voice = value
		if name == 'dialog_voice':
			self.dialog_voice = value
		if name == 'voice':
			self.voice = value
		if name == 'rate':
			self.rate = value
		if name == 'pitch':
			self.rate = value
		if name == 'language':
			self.language = value
		if name == 'volume':
			self.volume = value


import pyaudio
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivyblocks.baseWidget import HBox, VBox
import sys
import time

from .audio import Audio

class Recorder(VBox):
	input_id = 
	def __init__(self, **kw):
		super().__init__(**kw)
		self.auido = pyaudio.PyAudio()
		self.input_device_id = 
	def pause(self):
		pass

	def record(self):
		pass

	def stop(self):
		pass

	def play(self):
		pass

	def save(self):
		pass


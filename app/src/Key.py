from . import Qsys
import numpy as np
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty

class Key(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()
    measured = BooleanProperty()
    output = NumericProperty()
    sounds = ListProperty() #A reference to the KeyboardScreen's set of sounds
    system = '' #A reference to the KeyboardScreen's QSys
    
    def __init__(self, inPC, inPitches, inSys, x, y, text):
        """Initializes the key
        """
        super(Key,self).__init__(x=x,y=y,text=text)
        self.pitch_class = inPC
        self.system = inSys;
        self.playFunction = self.playSinglePitch
        self.measured = False
        self.pitches = inPitches

    def update_alpha(self, probabilities):
        self.alpha = float(np.power(probabilities[self.pitch_class], 1/1.2))
    
    def on_release(self):
        self.output = self.system.measure(self.pitch_class)
        self.playFunction()
        self.measured = True #So that the KeyboardScreen knows there's been a measurement (This is automatically reset to False by the KeyboardScreen)
    
    def playSinglePitch(self):
        pitch = self.pitches[self.output]
        if pitch.state == 'play':
            pitch.stop()
        pitch.play()

from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.logger import Logger

Builder.load_file('src/kv/OutputPitchWidget.kv')

class OutputPitchWidget(Widget):
    key = StringProperty('0')
    output = StringProperty('0')
    labelColor = ListProperty([1,1,1,0])
    
    def __init__(self,argOutput,argKey):
		super(OutputPitchWidget,self).__init__()
		self.output = str(argOutput)
		self.key = str(argKey)

    def start(self):
        self.animation = Animation(labelColor=[1,1,1,1], duration=.5) 
        self.animation &= Animation(pos=(Window.width * .3, self.y), duration=3.5) + Animation(labelColor=[1,1,1,0], duration=.1)
        self.animation.bind(on_complete = self.stop)
        self.animation.start(self)
        
    def stop(self, arg1, arg2):
		if(self.parent is not None):
			self.parent.remove_widget(self)

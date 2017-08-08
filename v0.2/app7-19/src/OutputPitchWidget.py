from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window

Builder.load_file('src/OutputPitchWidget.kv')

class OutputPitchWidget(Widget):
    key = StringProperty('0')
    output = StringProperty('0')
    labelColor = ListProperty([1,1,1,0])

    def start(self):
        self.set_keyOut()
        self.scroll()

    def set_keyOut(self):
        self.key = str(self.parent.parent.parent.parent.parent.system.lastKey)
        self.output = str(self.parent.parent.parent.parent.parent.system.lastOutput)

    def scroll(self):
        self.animation = Animation(labelColor=[1,1,1,1], duration=.5) 
        self.animation &= Animation(pos=(Window.width * .3, self.y), duration=3.5) + Animation(labelColor=[1,1,1,0], duration=.1)
        self.animation.bind(on_complete = self.stop)
        self.animation.start(self)
        
    def stop(self, arg1, arg2):
        self.parent.remove_widget(self)

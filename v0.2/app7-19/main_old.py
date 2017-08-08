from __future__ import print_function

import numpy as np
import DefaultApplication
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.base import EventLoop
from kivy.clock import Clock
import cProfile

class Key(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()

    def update_alpha(self):
        self.alpha = float(np.power((self.parent.system.get_probs()[self.pitch_class]), 1/1.5))

class MainScreenManager(ScreenManager):
    pass

class WelcomeScreen(Screen):
    pass

class DefaultApplicationScreen(Screen):
    defaultApplication = DefaultApplication.DefaultApplication()

class MainApp(App):

    def build(self):
        self.colorScheme = ColorScheme()
        self.defaultApplicationScreen = DefaultApplicationScreen(name='main')
        self.welcomeScreen = WelcomeScreen(name='welcome')
        self.screenManager = MainScreenManager()
        self.screenManager.add_widget(self.defaultApplicationScreen)
        self.screenManager.add_widget(self.welcomeScreen)
        print("Using Color Scheme : " + self.colorScheme.name)
        return self.screenManager

    def on_start(self):
#        self.profile = cProfile.Profile()
#        self.profile.enable()
        self.defaultApplicationScreen.defaultApplication.postWindowInit()
        Clock.schedule_interval(self.defaultApplicationScreen.defaultApplication.application_loop, 1 / 30.)

    def on_stop(self):
        pass
#        self.profile.disable()
#        self.profile.dump_stats('app.profile')

if __name__ == "__main__":
    #Builder.load_file('./kv/defaultApplication.kv')
    #Builder.load_file('./kv/welcome.kv')
    EventLoop.ensure_window()
    MainApp().run()

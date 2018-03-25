from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger

class EmailScreen(Screen):

class EmailInterface(BoxLayout):
    pass

class IntentButton(Button):
    email_recipient = StringProperty()
    email_subject = StringProperty()
    email_text = StringProperty()
    create_chooser = BooleanProperty()

    def send_email(self, *args):
        email.send(recipient=self.email_recipient,
                   subject=self.email_subject,
                   text=self.email_text,
                   create_chooser=self.create_chooser)

class EmailApp(App):
    def build(self):
        return EmailInterface()

    def on_pause(self):
        return True

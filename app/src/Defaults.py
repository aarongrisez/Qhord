class WinClass():
    """
    Contains information about the window size/aspect ratio, etc
    """
    def getWinClass(self,size):
        """
        This class contains information about the window created for the app
        """
        aspectRatio = size[0] / size[1]
        if aspectRatio == 4./3:
            return '4:3' 

class ColorScheme():
    """
    Setup color scheme for the application
    """
    Background = 0.03, 0.63, 1.0, 1
    ButtonFill = 1, 1, 1 
    ButtonEdge = 0.98, 0.65, 0.13, 1
    name = "default"

class WidgetDefaults(object):
    """
    Setup default sizes for widgets (this is mostly to help debugging the UI)
    """

    def __init__(self, winClass):
        
        if winClass == '4:3':
            self.KEY_WIDTH = '50dp'
            self.KEY_HEIGHT = '50dp'
        else:
            self.KEY_WIDTH = '30dp'
            self.KEY_HEIGHT = '30dp'

class Spectra():
    defaults = {
    ############
    #PENTATONIC#
    ############
    #These options are only available for n = 4
    '1-5': [.5,0,0,0,.5],
    '1-3': [.5,0,0,0,0],
    ###########
    #CHROMATIC#
    ###########
    #These options are only available for n = 11
    'Major': [.45, 0, 0, 0, .35, 0, 0, .2, 0, 0, 0, 0],
    'Minor':  [.45, 0, 0, .35, 0, 0, 0, .2, 0, 0, 0, 0],
    'Augmented': [.45, 0, 0, 0, .35, 0, 0, 0, .2, 0, 0, 0], 
    'Diminished': [.45, 0, 0, .35, 0, 0, .2, 0, 0, 0, 0, 0],
    'Tritone': [.5, 0, 0, 0, 0, 0, .5, 0, 0, 0, 0, 0]
    }

class PitchesSharps():
    pitchClasses = {'C_pentatonic': [0,2,4,5,7]}
    letters5 = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4}
    numbers5 = {'0': 'C', '1': 'D', '2': 'E', '3': 'F', '4': 'G'}
    letters = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    numbers = {'0': 'C', '1': 'C#', '2': 'D', '3': 'D#', '4': 'E', '5': 'F', '6': 'F#', '7': 'G', '8': 'G#', '9': 'A', '10': 'A#', '11': 'B'}
 

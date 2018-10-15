# qhord 

Qhord is a mobile application for interacting with a quantum mechanical system through a musical interface.

### IMPORTANT NOTE
This repo has been deprecated. In February 2018, I decided to abandon Kivy as the framework behind Qhord. The primary reason for this was the spotty success I was having with the build system for deploying to mobile devices. We have moved to the Godot engine for continued development and have separated the simulation code into a separate C++ library [qsys](https://github.com/aarongrisez/Qsys). Please email me at aaron@qhord.com if you have any questions.

![logo](app/src/assets/images/QhordLogo.png?raw=true)

Website: [qhord](http://qhord.com/)

Demo: [Youtube](https://youtu.be/WgCajz7P-M0)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run this code on your machine you will need:

* Cython version [0.23, 0.25]
```
pip install 'cython>=0.23,<0.26'
```
* [NumPY](http://www.numpy.org/)
* [SciPY](https://www.scipy.org/)
```
pip install numpy
pip install scipy
```

* [Kivy](https://kivy.org/docs/)

#### Install necessary system packages
```
sudo apt install -y \
    python-pip \
    build-essential \
    git \
    python \
    python-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

Then you can install kivy with pip:
```
pip install kivy
```


    * Mac OSX users may also need the tools 'gst-plugins-bad' and 'gst-plugins-good' in addition to the tools listed on the installation guide
```
brew install gst-plugins-bad
brew install gst-plugins-good
```

### Running

Once your dependencies are installed and clean, you can run the app with
```
python -m main
```
from the /qhord/app folder

### Files
* App - Source Code
    * main.py - code entrance
    * /src - Location of Qsys module - main quantum system
        * assets
        * kv
* iOS - XCode Project
* Android - Android builds

## Contributing

Please reach out to us at [http://qhord.com/](http://qhord.com/) or email Aaron at aaron@qhord.com for info about contributing.

## Authors

* **Aaron Grisez** - *Initial work* - [Aaron Grisez](https://github.com/aarongrisez)
* **Michael Seaman** - *Just the README* [Michael Seaman](https://github.com/michaelseaman)
* **Sam Kagan** - *Fixing a lot of things* [Sam Kagan](https://github.com/HungryJoe)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

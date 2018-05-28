# qhord 
[![Build Status: Still need Test Suite!](https://travis-ci.com/aarongrisez/qhord.svg?token=NKnMzaV57yuvZyF9zLxy&branch=master)](https://travis-ci.com/aarongrisez/qhord)

Qhord is a mobile application for interacting with a quantum mechanical system through a musical interface.

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

* kivy - Installation instructions at [kivy](https://kivy.org/docs/installation/installation.html)
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

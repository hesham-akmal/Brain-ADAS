Updated Version (2017.12.23)

**Original repository:**
https://github.com/CymatiCorp/CyKITv2

**Chat Discussion:**
https://discordapp.com/invite/gTYNWc7 <br/>
(Do not need discord app, just click for browser chat)

<img src="./git-Images/CyKITv2.png" width="25%" height="25%" />

CyKit 2.0 (2017.12)
 - for Python 2.7.6 (Windows)
 - for Python 2.7, 3.5, 3.6 (Linux)

Python Data Controller for Neural EEG headsets.


# Description

Streams EEG data to a browser for data handling.
Works with Chrome and Firefox thus far.

<img src="./git-Images/CyKITpreview.png" width="70%" height="70%" />

<img src="http://cymaticorp.com/edu/CyKITv2-/CyKITv2-example.png" width="70%" height="70%" />


# Dependencies

See [requirements.txt](./requirements.txt).
<!-- * pywinusb 0.4.2 --- https://pypi.python.org/pypi/pywinusb/  <br>
* pycrypto 2.6.1 --- https://pypi.python.org/pypi/pycrypto/2.6.1
//-->


# Installation

## Windows
* Install Python 2.7.6
* Install pycrypto
* Extract pywinusb-0.4.2
* Copy pywinusb/ folder to Python27\Lib\site-packages\

## Linux

Tested with Arch Linux so far. Feel free to contribute!

### Arch Linux

*Note: I'll outline the installation process for Python 3.6 in what follows.*

1. Install one of python 2,7, 3.5, 3.6
    `sudo pacman -S python` (for the latest python version)
2. Clone this repository and `cd` into the cloned repository
3. Install virtualenv and create it (as you like to keep your global site-packages clean)
    - `sudo pacman -Syy python-virtualenv`
    - `virtualenv ./venv`
4. Install packages into local virtualenv
    - `source ./venv/bin/activate`
    - `pip install -r requirements.txt`
5. Optionally, create missing symlinks for *.so*'s from your virtualenv to your system folder. In my case, this was:
    - `sudo ln -s path/to/venv/lib/python3.6/site-packages/hidraw.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/libhidapi-libusb.so.0`

# Usage

<img src="./git-Images/helpFile.png" width=70% height=70% >

Example 1.
`python CyKITv2.py 127.0.0.1 18675 2`

Example 2.
`python CyKITv2.py 127.0.0.1 15309 4 info`

Example 3.
`python CyKITv2.py 127.0.0.1 12991 6 info+confirm`


* Open a browser. (Firefox/Chrome)
* Open Web Document in project: /Web/CyKITv2.html
* Enter localhost and listen port used to run CyKITv2.py
* Press "Connect"

Features
--------

* Uses Python threading.
* Able to connect localy to localhost. (no need for http servers)
* Scrolling
* Able to make use of EEG data via javascript.
* EEG graphing.
* Masking (Advanced feature lets you manipulate data functions in real-time)

Note: Does not currently stream to openvibe. <br>
      Only a browser can access this data.

Beta
----

Updated 12.23.2017

Gyro Data not yet supported.  <br>
Depending on the headset, you may be able to view gyros in manual control. <br>
Epoc+ gyros will not currently be displayed. <br>
Note: Switching to Gyro-mode may cause EEG to stop displaying.  <br>
Refresh the browser if this occurs. <br>

Recordings work, however it has not been tested with importing <br>
to any application, and the headers may need some work. <br>

Todo: <br>
 Fix (All, Counter) buttons. <br>
 Add Gyros. <br>
 Add Game. <br>
 Add Epoc+ Settings change. <br>
 Fix CSV header data. <br>
 Add OpenVIBE support. <br>
 Add Generic TCP layer. <br>
 Fix Misc. visual bugs with scrolling. <br>
 
* Feel free to offer comments and suggests via Issues, for further <br>
information check our Discord server.  Submit new push requests,  <br>
if you have something to contribute. <br>

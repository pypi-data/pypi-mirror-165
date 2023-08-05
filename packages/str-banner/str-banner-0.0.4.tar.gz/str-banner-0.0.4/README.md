# STR Linux Classification Banner
## Description

Python program to display the classification of a system at the top of the screen. This project is meant to be run as a system wide installation and display the banner for all users. With the example /etc/banner.conf included below, the banner displayed will look like this on Ubuntu 20.04:

<br> 

<div align="center"><img src="config/banner.PNG" width=50% ></div>

<br>

## Prerequisites
Install tkinter and pip for python3
### Ubuntu
```
# sudo apt install python3-pip python3-tk
```

### Red Hat
```
# sudo yum install python3-pip python3-tkinter
```

<br>

## Installation

Two installation methods exist for this project:

<br>

Method 1 - Pulling source from gitlab and calling setup.py directly
```
# git clone https://gitlab.str.corp/csa0363/lab-banner.git
# sudo python3 setup.py install
```

<br>

Method 2 - Installing from PyPi using pip
```
# sudo python3 -m pip install str-banner
```
<br>

## Usage
Either installation method will create a python script in your path. You can execute it by running:
```
# /usr/local/bin/banner
```

<br>

## Configuration
Create a configuration file, /etc/banner.conf with the following settings:
```
    message     -    Banner message that will be displayed
    color       -    Hex color code for the banner background
    opacity     -    Specify how transparent the banner should be. Value between 0 (transparent) and 1 (Opaque)
    width       -    Specify what percent of the screen the banner should span. Value between 0 and 1
```

### STR Color Standards
| Color Code    | Color     | Classification    |
|---            |---        |---                |
| `#4cbb17`     |Green      | Unclassified      |
| `#ff0000`     |Red        | Secret            |
| `#ee8822`     |Orange     | Top Secret        |
| `#ffff00`     |Yellow     | Top Secret // SAR |

<br>

<br>


## Examples


### Define configuration settings in /etc/banner.conf
```
# vi /etc/banner.conf

[settings]
message = Unclassified
color = #4cbb17
opacity = 0.8
width = 0.85
```
<br>

### Automatic launch on login
An admin can set up the python script installed in /usr/local/bin/banner to run when a user logs into GNOME. Create a configuration file in /etc/xdg/autostart/

```
# vi /etc/xdg/autostart/str-banner.desktop

[Desktop Entry]
Name=Classification Banner
Exec=/usr/local/bin/banner
Comment=Display Classification Level of System
Type=Application
Encoding=UTF-8
Version=1.0
MimeType=application/python;
Categories=Utility;
X-GNOME-Autostart-enabled=true
X-KDE-autostart-phase=2
X-KDE-StartupNotify=false
StartupNotify=false
Terminal=false

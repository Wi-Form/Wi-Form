# Overview
Wi-Form is a open-source and international endeavour to map and give form to places’ WIFI signature. This is done through a reworked take on Wardriving, Warwalking, etc.

A mobile device with a GPS module and a WIFI module (with a monitor-mode capabilities) collect the WIFI probes sent by nearby devices. The data is then stored in a 3 dimensional table, where the X and Y are the latitude and longitude and the Z is the strength of the probe signal.

The data is outputted as a csv file that can be imported into a 3D program and viewed as a pointcloud. This is then processed though a surface reconstruction to get a solid mesh. More detail on this in the instruction section.

## Installation

### Requirements
1. Python 3.x, and the following libraries:
    - Scrapy
    - Csv
    - Netaddr 
    - Serial
2. Airmon-ng
3. GPS module
4. Wifi adaptor with monitor-mode capabilities
5. Mobile device running Linux (Such as a Raspberry Pi, but any mobile Linux device should work)

## 1. Setup
Download the repository, ether as a zip or clone it, and install the required python libraries. You can do this manually using pip install, or use ```Python install -r requirements``` while in the downloaded repository folder.
If you don’t have airmon-ng installed, install with the command:
``` sudo apt-get install aircrack-ng```

Then we need to get the address of the GPS module and the WIFI adaptor. (If you don’t know how to do this see below) Take the address of the GPS module and inset into the code at the top where is say “GPSPATH” <-- Implement this 

The script is thought and tested as being used with a Raspberry Pi (or other arm devices) in headless mode with a ssh connecting to a phone.

### Find the GPS&WIFI module address
#### GPS
With the GPS module unplugged open a terminal window and type ` ls /dev/ `. Then plug the module in and type ` ls /dev/ ` again. There should be a new address now – this is the module.
Typically it is at “ttyACM(x)”, x being a number between 0 and 10.

So you could utilise ` ls /dev/ | grep ttyACM ` to make the output more manageable.

#### WIFI adaptor
For the WIFI adaptor you simply use the command ` airmon-ng ` and look for your preferred adaptor. Should be something like “wlan(x)”, but this can vary from distro to distro. You can then start the WIFI adaptor in monitor mode using:
`airmon-ng start wlan(x)`


## 2. Usage
The script takes in one mandatory argument (Capture interface) and two optional arguments (log output and output path)

Args:
   - -i (Capture interface)
   - -l (Output log in realtime)
   - -o (Path to output file – Default is the same path as the script)

Example:
` python main.py -i wlan0mon -l -o /home/user/Desktop `

This command will show collection of data in realtime and save the output file on the desktop.



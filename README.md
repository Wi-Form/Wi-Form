# Wi-Form
A script to create 3D forms from collected GPS and WIFI data

# Overview
Wi-Form is a open-source and international endeavour to map and give form to places’ WIFI signature. This is done through a reworked take on Wardriving, Warwalking, etc.

A mobile device with a GPS module and a WIFI module (with a monitor-mode capabilities) collect the WIFI probes sent by nearby devices. The data is then stored in a 3 dimensional table, where the X and Y are the latitude and longitude and the Z is the strength of the probe signal.

The data is outputted as a csv file that can be imported into a 3D program and viewed as a pointcloud. This is then processed though a surface reconstruction to get a solid mesh. More detail on this in the instruction section.

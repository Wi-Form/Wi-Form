#!/usr/bin/python

from scapy.all import *
import netaddr
import time
import datetime
from threading import *
import os
import argparse
import csv

import serial
from math import sin, cos, radians, pi, atan, tan


fields = []
fieldsDebug = []
GpsStart = []


DESCRIPTION = 'Program to collect wifi probes and GPS data to make 3D models'

class packetsniff(Thread):
	# Setup of the sniffing deamon
	def __init__(self, interface):
		super(packetsniff, self).__init__()
		global fields, fieldsDebug
		fields = []
		fieldsDebug = []
		self.iface = interface
		self.deamon = True
		self.socket = None
		self.stop_sniff = Event()

	def run(self):
		# Running thread for the sniffer
		# Takes the parameters from the
		# function process_packet
		sniff(iface 	  = self.iface,
		      store 	  = 0,
		      prn 		  = self.process_packet,
		      stop_filter = self.should_stop_sniffer)


	def join(self, timeout=None):
		# Killing function for sniffer
		self.stop_sniff.set()
		print('Waiting for the sniffer to stop')
		time.sleep(timeout)

	def should_stop_sniffer(self, packet):
		# Checks if the thead should be killed
		return self.stop_sniff.isSet()
 

	def process_packet(self, packet):
		# The main packet sniffing module
		if not packet.haslayer(Dot11):
			return

		# Looks if device have been seen before
		# if not, the rssi value is added
		if packet.addr2 not in fieldsDebug:
			fields.append(packet.dBm_AntSignal)
		fieldsDebug.append(packet.addr2)
		
def convertZ(zlist):
	# Translate the collected rssi value
	# to something that is relateble with lat&long value
	netrssi = 0
	if len(zlist) == 0:
		z = float(0)
	if len(zlist) == 1:
		z = float(zlist[0]+100)/100
	else:
		for i in zlist:
			netrssi = netrssi+(i+100)
		z = float(netrssi)/100
	return z

def addConvert(lat_deg, lon_deg, rssiList, GpsStart):
	# Takes the GPS coordinates and the converted rssi value
	# and returns them as concatinated list
	x = float(lat_deg)-float(GpsStart[0])
	y = float(lon_deg)-float(GpsStart[1])
	z = convertZ(rssiList)
	return [float(x),float(y),float(z)]
	

def GPSpuller(log):
	'''
	Main function.
	Collectes GPS data and concatinates it with wifi rssi values.
	Returns list with GPS and rssi and writes to csv file 
	'''
	now = datetime.datetime.now()
	now = now.strftime('%H, %M, %S')
	gps = serial.Serial("/dev/ttyACM0", baudrate=9600) # Path to GPS module
	output = []
	GpsStart = None
	itter = 0
	while True:
		line = gps.readline()
		data = line.split(",")
		if data[2] == "A" and GpsStart == None:
			GpsStart = [data[3],data[5]]
			StartingCoor.write(str([data[3],data[5]]))
			StartingCoor.close()
			print('Starting condinates - ',GpsStart)
			if len(fields) != 0:
				del fields[0]
		if GpsStart != None:
			
			# Checks if GPS signal is valid #
			if data[0] == "$GPRMC" and data[2] == "V":
				if log:
					print('no gps connection')
					print('length of fields', len(fields))
				if len(fields)>2:
					del fields[0]		

			# If signal is valid 
			# Appends converted GPS condinates and RSSI to output list 
			# Deletes the last RSSI value to avid past devices clogging the list
			if data[0] == "$GPRMC" and data[2] == "A":
				output.append(addConvert(data[3], data[5], fields, GpsStart))
				

				if log:
					print(itter, output[-1])

				# Write output to csv file
				wr.writerow(output[-1])
				del fields[::]
				itter += 1
	
		time.sleep(0.1)





if __name__ == "__main__":

	# Setup of argumentparser #
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('-i', '--interface', help="Capture interface")
	parser.add_argument('-o', '--output', default='output.csv', help='Output name for csv file')
	parser.add_argument('-l', '--log', action='store_true', help='Write log to the consol')
	args = parser.parse_args()
	if not args.interface:
		print ("error: capture interface not given, try --help")
		sys.exit(-1)

	# Setup thread for sniffer #
	sniffer = packetsniff(args.interface)	

	# Making folder for files #
	if not os.path.exists(os.path.dirname(__file__)+'/data'):
		os.makdirs(os.path.dirname(__file__)+'/data')
	folder = os.path.dirname(__file__)+'/data/'+args.output[:-4]
	if folder == True:
		print(
			'Please choose another file name'
			'\nOne with this name already exists'
			)
		sys.exit(-1)
	os.makedirs(folder)


	# Setting up csv writer and file for starting coordinates #
	csvFile = open(folder+'/'+args.output, 'w')
	wr = csv.writer(csvFile)

	StartingCoor = open(folder+'/'+'startingCoordinates.txt', 'w')
	
	# Start the main function
	try:
		sniffer.start()
		GPSpuller(args.log)

	#Quit and shutdown deamon, when you press ctrl+c
	except KeyboardInterrupt, SystemExit:
		print ("\nKilling Thread...")
		sniffer.join(2)
		print ("Done.\nExiting.")

from math import *

'''
A script to hold the small funcitons used in the Tube mapper
'''

def angle_trunc(a):
        # Get the positive angle
        while a < 0.0:
                a += pi * 2
        return a

def get_angle(row):
        # get angle between (point, origin) and x-axis
        deltaY = row['lat_off']
        deltaX = row['lon_off']
        return angle_trunc(atan2(deltaY, deltaX))

def add_colour(line):
	# this is beyond awful, but it's the easiest way to do this. Ugh.
	if line == 'Bakerloo':
		return '#B36305'
	if line == 'Central':
		return '#E32017'
	if line == 'Circle':
		return '#FFD300'
	if line == 'District':
		return '#00782A'
	if line == 'H & C':
		return '#F3A9BB'
	if line == 'Jubilee':
		return '#A0A5A9'
	if line == 'Metropolitan':
		return '#9B0056'
	if line == 'Northern':
		return '#000000'
	if line == 'East London':
		return '#EE7C0E'
	if line == 'Piccadilly':
		return '#003688'
	if line == 'Victoria':
		return '#0098D4'
	if line == 'Waterloo & City':
		return  '#95CDBA'


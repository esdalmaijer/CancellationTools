# -*- coding: utf-8 -*-
#
# This file is part of CancellationTools
#
# CancellationTools is open-source software for running cancellation tasks,
# and directly analysing the data they produce.
#
# Copyright (C) 2014, Edwin S. Dalmaijer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

__author__ = u"Edwin Dalmaijer"

# native
import struct

# external
import numpy
import pygame


# # # # #
# HELPER FUNCTIONS

def check_colour(colour):
	
	"""Checks if the passed colour is a correct one, and returns an RGB gun of
	that colour

	arguments
	
	colour		--	any kind of colour (RGB, hex, string) to check
	
	returns
	
	rgbcol		--	a RGB list of values between 0 and 255, e.g.
					[0,255,100]
	"""
	
	rgbcol = None
	err = None
	
	# check if the passed colour is a string
	if type(colour) in [str,unicode]:
		# check if the passed colour is a hex value
		if colour[0] == '#' and len(colour) == 7:
			# try converting hex to RGB
			try:
				# note: do NOT turn 'BBB' into unicode! (will cause error)
				rgbcol = list(struct.unpack('BBB', colour[1:].decode('hex')))
			except:
				err = u"colour '%s' not recognized"	
		else:
			# check if the colour is in the PyGame colour dict
			if colour in pygame.colordict.THECOLORS.keys():
				rgbcol = list(pygame.colordict.THECOLORS[colour][:3])
			else:
				err = u"colour '%s' not recognized" % colour
	# check if the passed colour is a string or a list
	elif type(colour) in [tuple,list]:
		rgbcol = list(colour[:3])
	# if the type of colour is something else, we don't know what to do
	else:
		err = u"colour '%s' not recognized"

	# check if the colour values are valid
	if err == None:
		if not sum(map(isrgb, rgbcol)) == 3:
			err = u"colour '%s' (RGB='%s') contains an illegal value" % (colour,rgbcol)

	# return an error if necessary
	if err != None:
		return err
	# return RGB gun is there are no errors
	else:
		return rgbcol


def draw_Landolt_C(size, direction, fgc, bgc, pw, ow):
	
	"""Returns a surface with a Landolt C
	
	arguments
	
	size		-	an integer indicating both the width and height of the C
				in pixels
	direction	-	a string indicating the direction, should be one of:
				'u' (up), 'd' (down), 'l' (left), 'r' (right), or 'o' (no
				opening)
	fgc		-	a (r,g,b) tuple indicating the colour of the C
	bgc		-	a (r,g,b) tuple indicating the background colour of the C,
				or None for a transparent background
	pw		-	penwidth of the circle in pixels
	ow		-	width of the opening in pixels
	
	returns
	
	surface	-	a square surface of (size,size), containing the Landolt C
	"""
	
	# check if the background should be transparant
	if bgc == None:
		# reset the background colour to a colour with an alpha of 0
		bgc = (0,0,0,0)
		# create a Surface that supports transparancy
		surf = pygame.Surface((size,size), pygame.SRCALPHA)
	else:
		# create Surface
		surf = pygame.Surface((size,size))
	# fill the surface with the background colour
	surf.fill(bgc)
	
	# circle centre
	spos = (int(size/2),int(size/2))
	
	# first draw a filled outer circle in the foreground colour
	pygame.draw.circle(surf, fgc, spos, int(size/2), 0)
	# then draw a filled inner circle in the background colour
	# (this gives prettier results than drawing a circle with a penwidth)
	pygame.draw.circle(surf, bgc, spos, int(size/2-pw), 0)
	
	# draw an opening
	if direction != u'o':
		# up
		if direction[0] == u'u':
			epos = (int(size/2), 0)
		# down
		elif direction[0] == u'd':
			epos = (int(size/2), size)
		# left
		elif direction[0] == u'l':
			epos = (0, int(size/2))
		# right
		elif direction[0] == u'r':
			epos = (size, int(size/2))
		# draw line from centre to ending position, drawing over the circle
		pygame.draw.line(surf, bgc, spos, epos, int(ow))
	
	return surf


def intersection(line1, line2):
	
	"""Checks if the passed lines intersect, and returns the coordinates of
	the intersection, by applying Cramer's rule; NOTE: only checks for
	# intersections in the domain of each line!
	
	arguments
	
	line1		--	a list of a starting and an ending (x,y) coordinate,
					e.g. [(1,1),(5,5)
	line2		--	a list of a starting and an ending (x,y) coordinate,
					e.g. [(0,1),(3,4)
	
	returns
	intersect		--	a coordinate of the intersection, or None when there
					was no intersection
	"""
	
	# points (renaming for convenience)
	p11, p12 = line1
	p21, p22 = line2

	# coefficients of the line equations
	A = [p11[1]-p12[1], p21[1]-p22[1]]
	B = [p12[0]-p11[0], p22[0]-p21[0]]
	C = [-1 * (p11[0]*p12[1] - p12[0]*p11[1]),
		-1 * (p21[0]*p22[1] - p22[0]*p21[1])]
	
	# determinant
	D  = A[0]*B[1] - B[0]*A[1]
	Dx = C[0]*B[1] - B[0]*C[1]
	Dy = A[0]*C[1] - C[0]*A[1]
		
	# check if there is an intersection, and return None if there wasn't any
	if D != 0:
		intersect = (Dx/D, Dy/D)
	else:
		return None
	
	# check if the intersection is in the domain of both lines
	if min(p11[0],p12[0]) < intersect[0] < max(p11[0],p12[0]) \
		and min(p11[1],p12[1]) < intersect[1] < max(p11[1],p12[1]) \
	and min(p21[0],p22[0]) < intersect[0] < max(p21[0],p22[0]) \
		and min(p21[1],p22[1]) < intersect[1] < max(p21[1],p22[1]):
		return intersect
	# if the intersection was outside of the domain, return None
	else:
		return None


def isrgb(value):
	
	"""Checks if a value is between 0 and 255 (inlcuding 0 and 255)
	
	arguments
	
	value		--	a numerical value
	
	returns
	
	check		--	1 if the value is in range(0,256) or 0 if it is not
	"""
	
	if 0 <= int(value) <= 255:
		return 1
	else:
		return 0


def gaussian(x, sx, y=None, sy=None):
	
	"""Returns an array of numpy arrays (a matrix) containing values between
	1 and 0 in a 2D Gaussian distribution
	
	arguments
	x		-- width in pixels
	sx		-- width standard deviation
	
	keyword argments
	y		-- height in pixels (default = x)
	sy		-- height standard deviation (default = sx)
	"""
	
	
	# square Gaussian if only x values are passed
	if y == None:
		y = x
	if sy == None:
		sy = sx

	# MATRIX
	#(gives pixelated results; array takes more processing, but looks nicer)
	#M = 1.0/(2*numpy.pi*sx*sy) * (numpy.exp(-0.5*(x**2/sx**2 + y**2/sy**2)))

	# ARRAY
	# centers	
	xo = x/2
	yo = y/2
	# matrix of zeros
	M = numpy.zeros([y,x],dtype=float)
	# gaussian matrix
	for i in range(x):
		for j in range(y):
			M[j,i] = numpy.exp(-1.0 * (((float(i)-xo)**2/(2*sx*sx)) + ((float(j)-yo)**2/(2*sy*sy)) ) )

	return M


def pearsonr(x, y):

	"""Calculates the Pearson rank correlation; source directly from SciPy,
	to avoid having to import SciPy for just a single function; see:
	https://github.com/scipy/scipy/blob/v0.13.0/scipy/stats/stats.py#L2470
	
	arguments
	
	x			-	NumPy array
	y			-	NumPy array
	
	returns
	
	R			-	Pearson's R
	"""
	
	# x and y should have same length.
	x = numpy.asarray(x)
	y = numpy.asarray(y)
	n = len(x)
	mx = x.mean()
	my = y.mean()
	xm, ym = x-mx, y-my
	r_num = numpy.add.reduce(xm * ym)
	r_den = numpy.sqrt(numpy.sum(xm**2) * numpy.sum(ym**2))
	r = r_num / r_den

	# Presumably, if abs(r) > 1, then it is only some small artifact of floating
	# point arithmetic.
	r = max(min(r, 1.0), -1.0)
	return r
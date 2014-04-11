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

# external
import pygame


# # # # #
# DICTS

keymodsdict = {u'1':u'!',
			u'2':u'@',
			u'3':u'#',
			u'4':u'$',
			u'5':u'%',
			u'6':u'^',
			u'7':u'&',
			u'8':u'*',
			u'9':u'(',
			u'0':u')',
			u'`':u'~',
			u'-':u'_',
			u'=':u'+',
			u'[':u'{',
			u']':u'}',
			u'\\':u'|',
			u';':u':',
			u"'":u'"',
			u',':u'<',
			u'.':u'>',
			u'/':u'?'}
for letter in u'abcdefghijklmnopqrstuvwxyz':
	keymodsdict[letter] = letter.upper()


# # # # #
# FUNCTIONS

def check_click(pos, rect):
	
	"""Checks if the passed position was in the passed rect
	
	arguments
	
	pos		-	a (x,y) tuple
	rect		-	a (x,y,w,h) tuple
	
	returns
	check	-	True if pos is within rect, False if not
	"""
	
	if (rect[0] <= pos[0] <= rect[0]+rect[2]) and (rect[1] <= pos[1] <= rect[1]+rect[3]):
		return True
	else:
		return False


def check_escape():
	
	"""Checks if the Escape key is pressed
	
	arguments
	
	None
	
	returns
	
	check	-	True if Escape was pressed, False if not
	"""
	
	# check if there is a mouse click or a keypress
	for event in pygame.event.get():
		# check if there was a keypress
		if event.type == pygame.KEYDOWN:
			# check if the Escape key is pressed
			if event.key == pygame.K_ESCAPE:
				# if the Escape is pressed, return True
				return True
	# if the Escape is not pressed, return False
	return False


def check_mouseclicks():
	
	"""Checks if there was a mouseclick, and returns the clicked button, and
	position
	
	arguments
	
	None
	
	returns
	button, pos	-	button is an integer value, indicating which button
					got pressed (counting starts at 1, on the left mouse
					button); or None if no button was clicked
					pos is a (x,y) tuple, indicating where the click
					occured; or None if no button was clicked
	"""
	
	# check events
	pygame.event.get()
	# check mouse button states
	down = pygame.mouse.get_pressed()
	# if a button is clicked, return button number and position
	if sum(down) > 0:
		return down.index(1)+1, pygame.mouse.get_pos()
	else:
		return None, None


def check_space():
	
	"""Checks if the Space key is pressed
	
	arguments
	
	None
	
	returns
	
	check	-	True if Escape was pressed, False if not
	"""
	
	# check if there is a mouse click or a keypress
	for event in pygame.event.get():
		# check if there was a keypress
		if event.type == pygame.KEYDOWN:
			# check if the Escape key is pressed
			if event.key == pygame.K_SPACE:
				# if the Escape is pressed, return True
				return True
	# if the Escape is not pressed, return False
	return False


def colourpicker(settings):
	
	"""Allows a user to choose a colour, using three sliders (one for red,
	one for green, and one for blue); the interactive window will be full
	screen (taking over the display), and will restore the display to its
	state when calling colourpicker before returning
	
	arguments
	
	settings	-	the app settings dict
	
	returns
	
	input	-	list of the chosen colour, e.g. [255,100,0]
	"""
	
	# DISPLAY
	# get current display
	disp = pygame.display.get_surface()
	ds = disp.get_size()
	# copy display as it is now
	dispcopy = disp.copy()
	
	# PROPERTIES
	# current button
	button = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']]
	# current colour
	exec(u"rgb = list(%s)" % button[u'text'])
	# colour rect
	crect = [int(ds[0]/4), int(ds[1]/5), int(ds[0]/2), int(2*ds[1]/5)]
	# text position (centre)
	textrect = [int(ds[0]/4), int(3*ds[1]/5), int(3*ds[0]/8), int(ds[1]/10)]
	textpos = (int(7*ds[0]/16), int(13*ds[1]/20))
	# save button
	savetext = settings[u'font'][u'medium'][u'bold'].render(u"save", False, settings[u'fgc'])
	saverect = [int(5*ds[0]/8), int(12.5*ds[1]/20), int(ds[0]/8), int(ds[1]/20)]
	savepos = (int(saverect[0]+saverect[2]/2)-savetext.get_width()/2, int(saverect[1]+saverect[3]/2)-savetext.get_height()/2)
	# sliders
	bw = 1
	sly = [14*ds[1]/20, 16*ds[1]/20, 18*ds[1]/20]
	slrect = []
	for y in sly:
		slrect.append([int(ds[0]/4), int(y), int(ds[0]/2), int(ds[1]/20)])
	# slider button
	buttsize = (slrect[0][3]-2*bw, slrect[0][3]-2*bw)
	minx = slrect[0][0]+bw
	maxfill = (slrect[0][2]-2*bw) - buttsize[0]
	
	# DRAWING
	# fill the display with the background colour
	disp.fill(settings[u'bgc'])
	# draw colour rect
	disp.fill(rgb, crect)
	# RGB value
	rgbtext = settings[u'font'][u'medium'][u'bold'].render(unicode(rgb), False, settings[u'fgc'])
	disp.blit(rgbtext, (textpos[0]-rgbtext.get_width()/2, textpos[1]-rgbtext.get_height()/2))
	# save button
	disp.fill(settings[u'colours'][u'chameleon'][2], saverect)
	disp.blit(savetext, (savepos))
	# sliders
	for i in range(len(slrect)):
		r = slrect[i]
		# draw rect background
		pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][4], r, 0)
		# draw border
		pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][0], r, bw)
		# draw button
		x = minx + (rgb[i] / 255.0) * maxfill
		pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][0], [x, r[1]+bw, buttsize[0], buttsize[1]], 0)
	# update display
	pygame.display.flip()
	
	# INTERACTION
	saved = False
	while not saved:
		# check for clicks
		b, pos = check_mouseclicks()
		# handle input
		if b != None:
			# save button
			if check_click(pos, saverect):
				saved = True
			# any rect
			for i in range(len(slrect)):
				r = slrect[i]
				if check_click(pos, r) and (minx < pos[0] <= minx+maxfill):
					# reset button
					pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][4], r, 0)
					pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][0], r, bw)
					# draw new button
					pygame.draw.rect(disp, settings[u'colours'][u'aluminium'][0], [pos[0], r[1]+bw, buttsize[0], buttsize[1]], 0)
					# set corresponding RGB value
					rgb[i] = int(((pos[0]-minx) / float(maxfill)) * 255)
					# redraw rect
					disp.fill(rgb, crect)
					# reset and redraw text
					disp.fill(settings[u'bgc'], textrect)
					rgbtext = settings[u'font'][u'medium'][u'bold'].render(unicode(rgb), False, settings[u'fgc'])
					disp.blit(rgbtext, (textpos[0]-rgbtext.get_width()/2, textpos[1]-rgbtext.get_height()/2))
					# update display
					pygame.display.flip()

	# DISPLAY
	# reset display
	disp.blit(dispcopy,(0,0))
	pygame.display.flip()
	
	return rgb


def numfield(rect, font, settings):
	
	"""Starts interaction with a text field that only allows numerical input
	(simply calls textfield with the onlynums keyword argument passed True)
	
	arguments
	
	rect		-	a (x,y,w,h) tuple indicating where the textfield is
	font		-	a pygame.font.Font instance
	fgc		-	a (r,g,b) tuple indicating the text colour
	bgc		-	a (r,g,b) tuple indicating the background colour of the
				textfield
	settings	-	the app settings dict
	
	returns
	
	input	-	string of what was typed in
	"""
	
	return textfield(rect, font, settings, onlynums=True)


def on_off_button(button, settings, ontext=u"o", offtext=u"x"):
	
	"""Turns a button on if it is off, and off if it is on
	
	arguments
	
	button	-	key pointing to the button dict
	settings	-	the app settings dict
	
	keyword arguments
	
	ontext	-	unicode of what the text should be when the button state
				is on, e.g. u"o" (default = u"o")
	offtext	-	unicode of what the text should be when the button state
				is off, e.g. u"x" (default = u"x")
	
	returns
	
	button	-	the changed on/off buttondict, containing these keys:
						rect		-	[x,y,w,h]
						text		-	text on button
						font		-	font style (e.g. u'bold')
						colour	-	button colour (r,g,b)
						onlcick	-	function to call when clicked
									(settings need to be passed to
									this function; function will
									return updated settings and a
									Boolean indicating the experiment
									or analysis has started)
	"""
	
	# get the current button
	button = settings[u'guibuttons'][settings[u'currentscreen']][button]
	
	# change the button state
	if button[u'text'] == ontext:
		button[u'text'] = offtext
		button[u'colour'] = settings[u'onoffcol'][u"x"]
	elif button[u'text'] == offtext:
		button[u'text'] = ontext
		button[u'colour'] = settings[u'onoffcol'][u"o"]
	
	# get the display surface
	disp = pygame.display.get_surface()
	
	# colour the button
	disp.fill(button[u'colour'], button[u'rect'])
	
	# render and blit the text
	txtsurf = settings[u'font'][u'medium'][button[u'font']].render(button[u'text'], False, settings[u'fgc'])
	txtpos = [(button[u'rect'][0]+button[u'rect'][2]/2)-txtsurf.get_width()/2,
			(button[u'rect'][1]+button[u'rect'][3]/2)-txtsurf.get_height()/2]
	disp.blit(txtsurf, txtpos)
	
	# update the display
	pygame.display.flip()
	
	return button


def textfield(rect, font, settings, onlynums=False, loadtext=True):
	
	"""Starts interaction with a text field, handling keyboard input and
	updating part of the display on that input; returns when Enter is pressed
	
	arguments
	
	rect		-	a (x,y,w,h) tuple indicating where the textfield is
	font		-	a pygame.font.Font instance
	fgc		-	a (r,g,b) tuple indicating the text colour
	bgc		-	a (r,g,b) tuple indicating the background colour of the
				textfield
	settings	-	the app settings dict
	
	keyword arguments
	
	onlynums	-	Boolean indicating whether only numerical values should be
				allowed
	loadtext	-	Boolean indicating if the current text should be loaded
				(assuming the function is called via the currently active
				button!); alternatively all text is deleted when this
				function is called
	
	returns
	
	input	-	string of what was typed in
	"""
	
	# get the display surface
	disp = pygame.display.get_surface()
	
	# clip the display surface, to prevent text from spilling over
	disp.set_clip(rect)
	
	# rect centre
	textcentre = (rect[0]+rect[2]/2, rect[1]+rect[3]/2)

	# allowed characters
	if onlynums:
		allowed = u'0123456789'
	else:
		allowed = keymodsdict.keys()

	# load the current text
	if loadtext:
		text = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text']
	else:
		text = u""

	# run until Enter is pressed
	enter = False
	while not enter:
		# check if there is any event
		for event in pygame.event.get():
			# check if the event is a keypress
			if event.type == pygame.KEYDOWN:
				# convert the keyname into something readable
				key = pygame.key.name(event.key)#
				# check if the key is Enter
				if key == u'return':
					enter = True
				# remove the last index of the text if the key was backspace
				elif key == u'backspace' and len(text) > 0:
					text = text[:-1]
				# add the input to the text if the key was an allowed key
				elif key in allowed:
					# check if the Shift key is pressed (not when using nums)
					if (event.mod & pygame.KMOD_SHIFT) and not onlynums:
						# change key value accordingly
						key = keymodsdict[key]
					# append key to the text
					text += key
			# render the text
			textsurf = font.render(text, False, settings[u'fgc'])
			# text position
			textpos = (int(textcentre[0] - textsurf.get_width()/2), int(textcentre[1]-textsurf.get_height()/2))
			# reset text
			if enter:
				colour = settings[u'tfbgc']
			else:
				colour = settings[u'tfhbgc']
			disp.fill(colour, rect)
			# blit text to display
			disp.blit(textsurf, textpos)
			pygame.display.flip()
	
	# unclip display
	disp.set_clip(None)
	
	return text

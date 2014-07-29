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

# CancellationTools
from libhelper import check_colour
import libgui
import libinput

# native
import os
import sys

# external
import pygame


def run(directory, version=u"unknown", thisisandroid=False):
	
	"""Runs the application
	
	arguments
	
	directory		--	the directory of the application
	
	keyword arguments
	
	version		--	the version number as a string, e.g. '1.0.0'
					(default = u'unknown')
	thisisandroid	--	Boolean indicating if the app is running on Android
					(default = False)
	"""

	# # # # #
	# SETTINGS
	
	# if this is Windows, change the video driver environment variable to handle
	# input from touch screens better
	if os.name == u'nt':
		os.environ['SDL_VIDEODRIVER'] = u'windib'
	
	# if this is Android, import android
	if thisisandroid:
		import android
	
	# initialize pygame
	pygame.init()
	
	# the settings dict will contain the important settings, e.g. the paths to all
	# directories
	settings = {u'version':version, u'android':thisisandroid, u'ppname':None, u'newtaskname':None}
	
	
	# # # # #
	# DIRECTORY
	
	# main and lib directories
	settings[u'dir'] = {}
	settings[u'dir'][u'main'] = directory
	
	# data directory
	settings[u'dir'][u'data'] = os.path.join(settings[u'dir'][u'main'], u'data')
	settings[u'dir'][u'out'] = os.path.join(settings[u'dir'][u'data'], u'output')
	settings[u'dir'][u'rawout'] = os.path.join(settings[u'dir'][u'data'], u'raw')
	settings[u'dir'][u'onlinedata'] = os.path.join(settings[u'dir'][u'data'], u'online')
	
	# resources
	settings[u'dir'][u'res'] = os.path.join(settings[u'dir'][u'main'], u'resources')
	settings[u'dir'][u'tasks'] = os.path.join(settings[u'dir'][u'res'], u'tasks')
	settings[u'dir'][u'fonts'] = os.path.join(settings[u'dir'][u'res'], u'text', u'ubuntu-font-family-0.80')
	settings[u'dir'][u'plotfont'] = os.path.join(settings[u'dir'][u'fonts'], u'Ubuntu-R.ttf')
	settings[u'dir'][u'boldplotfont'] = os.path.join(settings[u'dir'][u'fonts'], u'Ubuntu-B.ttf')
	
	# browser
	settings[u'dir'][u'browsing'] = os.path.join(settings[u'dir'][u'res'], u'tasks')


	# # # # #
	# DISPLAY
	
	# initialize pygame.display (should have been done alread, but just for safety)
	pygame.display.init()
	
	# get the current display info
	if settings[u'android']:
		w, h = 1200, 800
	else:
		dispinfo = pygame.display.Info()
		w, h = dispinfo.current_w, dispinfo.current_h
	
	# correct the display size if it is insanely large (likely a two-screen setup)
	if w > 1920 or h > 1200:
		# get the second largets display mode
		w, h = pygame.display.list_modes()[1]
	
	# save the display size in the settings
	settings[u'dispsize'] = [w,h]
	settings[u'dispcentre'] = [w/2,h/2]
	
	# COLOURS
	# these colours are all from the Tango theme, see:
	# http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines#Color_Palette
	settings[u'colours'] = {	u'butter': 	[	u'#fce94f',
										u'#edd400',
										u'#c4a000'],
						u'orange': 	[	u'#fcaf3e',
										u'#f57900',
										u'#ce5c00'],
						u'chocolate': 	[	u'#e9b96e',
										u'#c17d11',
										u'#8f5902'],
						u'chameleon': 	[	u'#8ae234',
										u'#73d216',
										u'#4e9a06'],
						u'skyblue': 	[	u'#729fcf',
										u'#3465a4',
										u'#204a87'],
						u'plum': 		[	u'#ad7fa8',
										u'#75507b',
										u'#5c3566'],
						u'scarletred':	[	u'#ef2929',
										u'#cc0000',
										u'#a40000'],
						u'aluminium':	[	u'#eeeeec',
										u'#d3d7cf',
										u'#babdb6',
										u'#888a85',
										u'#555753',
										u'#2e3436']
									}
	# hex2rgb
	for cn in settings[u'colours'].keys():
		for i in range(len(settings[u'colours'][cn])):
			settings[u'colours'][cn][i] = check_colour(settings[u'colours'][cn][i])
	# foreground and background colours
	settings[u'fgc'] = settings[u'colours'][u'aluminium'][0]
	settings[u'bgc'] = settings[u'colours'][u'aluminium'][5]
	# text fields background and highlighted background
	settings[u'tfbgc'] = settings[u'colours'][u'aluminium'][3]
	settings[u'tfhbgc'] = settings[u'colours'][u'skyblue'][0]
	# on/off button
	settings[u'onoffcol'] = {u'o':settings[u'colours'][u'chameleon'][2],
						u'x':settings[u'colours'][u'scarletred'][2]}
	
	# FONTS
	# all fonts are from the Ubuntu font family, see: http://font.ubuntu.com/
	# rescale medium font size to display width
	mediumfontsize = int(settings[u'dispsize'][0] * (12.0 / (1920-1024)))
	# initialize pygame.font (should have been done alread, but just for safety)
	pygame.font.init()
	# create new Font instances
	settings[u'fontsize'] = {u'large':48, u'medium':mediumfontsize, u'small':12}
	settings[u'font'] = {}
	for s in settings[u'fontsize'].keys():
		settings[u'font'][s] = {	u'regular':pygame.font.Font(os.path.join(settings[u'dir'][u'fonts'],u'Ubuntu-R.ttf'), settings[u'fontsize'][s]),
							u'bold':pygame.font.Font(os.path.join(settings[u'dir'][u'fonts'],u'Ubuntu-B.ttf'), settings[u'fontsize'][s]),
							u'italic':pygame.font.Font(os.path.join(settings[u'dir'][u'fonts'],u'Ubuntu-RI.ttf'), settings[u'fontsize'][s])
							}
	
	# DISPLAY	
	# create the display
	disp = pygame.display.set_mode(settings[u'dispsize'], pygame.FULLSCREEN)
	# show a loading message
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"loading, please wait...", False, settings[u'fgc'])
	disp.blit(textsurf, (settings[u'dispcentre'][0]-textsurf.get_width()/2, settings[u'dispcentre'][1]-textsurf.get_height()/2))
	pygame.display.flip()
	
	# SOUND
	# initialize the mixer module
	pygame.mixer.init()
	# all sounds in a dict
	settings[u'sounds'] = {u'cancellation':	os.path.join(settings[u'dir'][u'res'], u'oncancellation.ogg')}
	# load all sounds
	for s in settings[u'sounds'].keys():
		settings[u'sounds'][s] = pygame.mixer.Sound(settings[u'sounds'][s])
	
	# ANDROID
	# Android specific stuff, only do this if this is the Android app
	if settings[u'android']:
		# initialize Android
		android.init()
		# map Escape function to Back key
		# TODO: is this necessary with Exit button at the ready in the
		# top-right of the display of the app?
		android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
		# wait to resume (allows Android interrupt)
		if android.check_pause():
			android.wait_for_resume()

	
	# # # # #
	# PROPERTIES
	
	# TASK
	# these settings will be overridden later on
	settings['taskproperties'] = {u'taskpath':None,
							u'visible':u'visible',
							u'ntargets':64,
							u'ndistractors':128,
							u'target':'o',
							u'distractor':['u','d'],
							u'stimsize':40,
							u'bgc':(127,127,127),
							u'fgc':(0,0,0),
							u'pw':3,
							u'ow':20,
							u'input':u'mouse',
							u'sound':u'x',
							u'clickcorrect':u'x'}
	
	# ANALYSIS
	settings[u'analysisproperties'] = {}
	settings[u'analysisproperties'][u'datapath'] = None
	settings[u'analysisproperties'][u'disthreshold'] = 50
	
	
	# # # # #
	# GUI SCREENS
	
	# top buttons
	settings[u'topbuttsize'] = (50,50)
	settings[u'topbuttons'] =  {	'quit': {	u'rect':[	settings[u'dispsize'][0]-int(1.5*settings[u'topbuttsize'][0]),
										settings[u'topbuttsize'][1]-int(0.5*settings[u'topbuttsize'][1]),
										settings[u'topbuttsize'][0],
										settings[u'topbuttsize'][0]],
									u'text':u"x",
									u'font':u'bold',
									u'colour':settings[u'colours'][u'scarletred'][2],
									u'onclick':libgui.quit_application},
							'mini': {	u'rect':[	settings[u'dispsize'][0]-int(4.5*settings[u'topbuttsize'][0]),
											settings[u'topbuttsize'][1]-int(0.5*settings[u'topbuttsize'][1]),
											settings[u'topbuttsize'][0],
											settings[u'topbuttsize'][1]],
									u'text':u"-",
									u'font':u'bold',
									u'colour':settings[u'colours'][u'skyblue'][0],
									u'onclick':libgui.minimize_application},
							'full': {	u'rect':[	settings[u'dispsize'][0]-int(3*settings[u'topbuttsize'][0]),
											settings[u'topbuttsize'][1]-int(0.5*settings[u'topbuttsize'][1]),
											settings[u'topbuttsize'][0],
											settings[u'topbuttsize'][1]],
									u'text':u"□",
									u'font':u'bold',
									u'colour':settings[u'colours'][u'skyblue'][0],
									u'onclick':libgui.toggle_fullscreen},
							'prev': {	u'rect':[	settings[u'topbuttsize'][0]-int(0.5*settings[u'topbuttsize'][0]),
											settings[u'topbuttsize'][1]-int(0.5*settings[u'topbuttsize'][1]),
											settings[u'topbuttsize'][0],
											settings[u'topbuttsize'][1]],
									u'text':u"<",
									u'font':u'bold',
									u'colour':settings[u'colours'][u'skyblue'][0],
									u'onclick':libgui.goto_previous_screen}
							}


	# empty dicts to contain all screens and buttons
	settings[u'guiscreens'] = {}
	settings[u'guibuttons'] = {}

	# starting screen (and associated buttons)
	settings[u'guiscreens'][u'start'], settings[u'guibuttons'][u'start'] = libgui.startscreen(settings)
	

	# # # # #
	# RUN GUI
	
	# set starting values
	settings[u'running'] = True
	settings[u'currentscreen'] = u'start'
	settings[u'currentbutton'] = None
	settings[u'currenttaskpage'] = 0
	settings[u'currentdatapage'] = 0
	settings[u'currentonlinedatapage'] = 0
	settings[u'currentbrowserpage'] = 0
	settings[u'screenhistory'] = [u'start']
	
	# show start screen
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	# loop until a task or an anlysis is started
	while settings[u'running']:
		# check if the Escape key is pressed
		if libinput.check_escape():
			settings[u'running'] = False
		# wait for a (left) mouseclick
		butt, pos = libinput.check_mouseclicks()
		# check if the left button got pressed
		if butt == 1:
			# loop through buttons, to check which got pressed
			for b in settings[u'guibuttons'][settings[u'currentscreen']].keys():
				# check if the current button was clicked
				if libinput.check_click(pos, settings[u'guibuttons'][settings[u'currentscreen']][b][u'rect']):
					# set new current button
					settings[u'currentbutton'] = b
					# call 'onclick' function, and wait for it to return
					settings = settings[u'guibuttons'][settings[u'currentscreen']][b][u'onclick'](settings)
					# unset current button
					settings[u'currentbutton'] = None
					# wait for a bit, to allow for unclicking
					pygame.time.wait(200)
					# break the for loop that's checking all buttons from the
					# now previous screen
					break
			# check if any of the top buttons got pressed
			for b in settings[u'topbuttons'].keys():
				# check if the current button was clicked
				if libinput.check_click(pos, settings[u'topbuttons'][b][u'rect']):
					# call 'onclick' function, and wait for it to return
					settings = settings[u'topbuttons'][b][u'onclick'](settings)
					# wait for a bit, to allow for unclicking
					pygame.time.wait(200)
					# stop checking the other buttons
					break
		# update the screen history
		if settings[u'currentscreen'] != settings[u'screenhistory'][-1]:
			settings[u'screenhistory'].append(settings[u'currentscreen'])
		# allow an Android interrupt
		if settings[u'android']:
			if android.check_pause():
				android.wait_for_resume()	

	
	# # # # #
	# SHUTDOWN
	
	pygame.display.quit()
	pygame.quit()
	sys.exit(0)

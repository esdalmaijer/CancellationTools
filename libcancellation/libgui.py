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
import libanalysis
from libhelper import draw_Landolt_C
from libinput import *
import libtask

# native
import copy
import os

# external
import pygame


# # # # #
# ONCLICKS

def after_data_selection(settings):
	
	"""Changes the current screen to the after data selection screen"""

	# make a new after task selection screen
	settings[u'guiscreens'][u'afterdataselection'], settings[u'guibuttons'][u'afterdataselection'] = afterdataselectionscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'afterdataselection'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def after_task_selection(settings):
	
	"""Changes the current screen to the after task selection screen"""
	
	# make a new after task selection screen
	settings[u'guiscreens'][u'aftertaskselection'], settings[u'guibuttons'][u'aftertaskselection'] = aftertaskselectionscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'aftertaskselection'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def back_to_start(settings):
	
	"""Changes the current screen back to the start screen"""
	
	# change the screen to the start screen
	settings[u'currentscreen'] = u'start'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()

	return settings


def browser(settings):
	
	"""Switches to the browser screen"""
	
	# change the screen to the start screen
	settings[u'currentscreen'] = u'browserscreen'
	# draw the browser screen
	settings[u'guiscreens'][u'browserscreen'], settings[u'guibuttons'][u'browserscreen'] = browserscreen(settings)
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def change_state(settings):
	
	"""Changes the state of an on/off button"""
	
	# GENERAL
	# Boolean indicating whether the button state should be changed
	changeplz = True

	# TASK SETTINGS
	if settings[u'currentscreen'] in [u'tasksettings',u'aftertaskselection']:
		# check if the button is for the input type
		if settings[u'currentbutton'] == 0:
			settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']] = on_off_button(settings[u'currentbutton'], settings, ontext=u"mouse", offtext=u"touch")
			return settings
		# check if the button is for the cancellation visibility
		if settings[u'currentbutton'] == 1:
			settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']] = on_off_button(settings[u'currentbutton'], settings, ontext=u"visible", offtext=u"invisible")
			return settings
		# check if the button is for a target
		elif settings[u'currentbutton'] in range(6,11):
			target = u'target'
		# check if the button is for a distractor
		elif settings[u'currentbutton'] in range(11,16):
			target = u'distractor'
		# any other case
		else:
			target = None
		# if the button to change is a target button, change the others too
		if target == u'target':
			# loop through all the buttons
			for b in range(6,11):
				# check if they are on
				if settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'] == u"o":
					# change the state of those that are on
					settings[u'guibuttons'][settings[u'currentscreen']][b] = on_off_button(b,settings)
			# check if the distractor for the same stimulus is on
			if settings[u'guibuttons'][settings[u'currentscreen']][range(11,16)[range(6,11).index(settings[u'currentbutton'])]][u'text'] == u"o":
				b = range(11,16)[range(6,11).index(settings[u'currentbutton'])]
				settings[u'guibuttons'][settings[u'currentscreen']][b] = on_off_button(b,settings)
		# if the button to change is a distractor button, do not change it
		# if the same stimulus type is used for the target!
		elif target == u'distractor':
			if settings[u'guibuttons'][settings[u'currentscreen']][range(6,11)[range(11,16).index(settings[u'currentbutton'])]][u'text'] == u"o":
				changeplz = False

	# CHANGE STATE
	# change the button state
	if changeplz:
		settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']] = on_off_button(settings[u'currentbutton'],settings)
	
	return settings


def data_selection(settings):
	
	"""Changes the current screen to the data selection screen"""
	
	# create a data selection screen if it doesn't exist yet
	settings[u'guiscreens'][u'dataselection'], settings[u'guibuttons'][u'dataselection'] = dataselectionscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'dataselection'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def goto_previous_screen(settings):
	
	"""Sets the current screen to the previous screen in the screen history"""
	
	if len(settings[u'screenhistory']) > 1:
		# remove the final screen from the history
		settings[u'screenhistory'].pop(-1)
		# set the current screen to the final one
		settings[u'currentscreen'] = copy.copy(settings[u'screenhistory'][-1])
		# draw current screen
		disp = pygame.display.get_surface()
		disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
		pygame.display.flip()

	return settings


def load_scan(settings):
	
	"""Starts the loading a scan procedure"""
	
	# PROBE TASK NAME
	# get display
	disp = pygame.display.get_surface()
	disp.fill(settings[u'bgc'])
	# inputrect
	inputrect = [	int(settings[u'dispcentre'][0]-settings[u'dispsize'][0]/4),
				int(settings[u'dispcentre'][1]-settings[u'dispsize'][1]/12),
				int(settings[u'dispsize'][0]/2),
				int(settings[u'dispsize'][0]/6)]
	# draw text input screen	
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"please provide a name for your new task:", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispsize'][1]/4-textsurf.get_height()/2)))
	disp.fill(settings[u'tfbgc'], inputrect)
	pygame.display.flip()
	# ask for the task name
	taskname = u""
	while not taskname:
		taskname = textfield(inputrect, settings[u'font'][u'large'][u'regular'], settings, loadtext=False)
	
	# TASK DIRECTORY
	# new task directory
	settings['taskproperties'][u'taskpath'] = os.path.join(	settings[u'dir'][u'tasks'], taskname)
	# check if the directory already exists (this is not a stupid thing to
	# do, as users might have already created a directory themselves)
	if not os.path.isdir(settings['taskproperties'][u'taskpath']):
		os.mkdir(settings['taskproperties'][u'taskpath'])
	# load the original image
	imgpath = os.path.join(settings[u'dir'][u'browsing'], settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text'])
	image = pygame.image.load(imgpath)
	# convert the image to a size that's appropriate to the current dispsize
	scale = min([settings[u'dispsize'][0] / float(image.get_width()), settings[u'dispsize'][1] / float(image.get_height())])
	newsize = (int(image.get_width() * scale), int(image.get_height() * scale))
	image = pygame.transform.scale(image, newsize)
	# use the image in a new task
	taskimg = pygame.Surface(settings[u'dispsize'])
	taskimg.fill((0,0,0))
	taskimg.blit(image, (int(settings[u'dispsize'][0]/2 - image.get_width()/2), int(settings[u'dispsize'][1]/2 - image.get_height()/2)))
	# save the new task as a PNG
	imgpath = os.path.join(settings['taskproperties'][u'taskpath'], u'task.png')
	pygame.image.save(taskimg, imgpath)
	# load PNG task image
	image = pygame.image.load(imgpath)
	
	# TARGET INPUT
	# show image
	disp.blit(image, (0,0))
	pygame.display.flip()
	# save button properties
	saverect = [	int(settings[u'dispsize'][0]-settings[u'dispsize'][0]/20),
				int(settings[u'dispsize'][1]-settings[u'dispsize'][1]/20),
				int(settings[u'dispsize'][0]/20),
				int(settings[u'dispsize'][1]/20)]
	savetext = settings[u'font'][u'medium'][u'bold'].render(u"save", False, settings[u'fgc'])
	savetextpos = (int(saverect[0]+saverect[2]/2 - savetext.get_width()/2),
				int(saverect[1]+saverect[3]/2 - savetext.get_height()/2))
	# click interaction, until Space is pressed
	targets = []
	running = True
	while running:
		# get the mouse state
		button, pos = check_mouseclicks()
		# handle the mouse input
		if button != None:
			# on a left click, append the current position
			if button == 1 and not check_click(pos, saverect):
				targets.append(pos)
			# on a left click on the save button, save the current task
			elif button == 1 and check_click(pos, saverect):
				running = False
			# on any other click, pop the last position
			else:
				targets.pop()
			# reset the screen
			disp.blit(image, (0,0))
			# draw the targets
			for i in range(len(targets)):
				# get the target position
				pos = targets[i]
				# draw a cross centered around the click position,
				# with starting and ending positions based on click
				spos = [	[int(pos[0]-20),	# top left x
						int(pos[1]-20)],	# top left y
						[int(pos[0]-20),	# bottom left x
						int(pos[1]+20)]]	# bottom left y
				epos = [	[int(pos[0]+20),	# bottom right x
						int(pos[1]+20)],	# bottom right y
						[int(pos[0]+20),	# top right x
						int(pos[1]-20)]]	# top right y
				pygame.draw.line(disp, settings[u'colours'][u'scarletred'][2], spos[0], epos[0], 3)
				pygame.draw.line(disp, settings[u'colours'][u'scarletred'][2], spos[1], epos[1], 3)
				# show save button
				disp.fill(settings[u'colours'][u'chameleon'][2], saverect)
				disp.blit(savetext, savetextpos)
			# show the screen
			pygame.display.flip()
			# wait a bit, to allow to unclick
			pygame.time.wait(200)
	
	# REMOVE DOUBLE TARGETS
	# loop through all coordinates
	for c in targets:
		# check if the coordinate occurs more than once
		if targets.count(c) > 1:
			# if the coordinate occurs more, throw it out
			i = targets.index(c)
			targets.pop(i)
	# SAVE TARGETS
	# open text file to save target locations
	tf = open(os.path.join(settings['taskproperties'][u'taskpath'], u'targets.txt'), 'w')
	# write header
	header = [u"target", u"x", u"y"]
	tf.write(u'\t'.join(header) + u"\n")
	# write the target locations
	for i in range(len(targets)):
		tf.write(u"%s\t%d\t%d\n" % (u'scan',targets[i][0],targets[i][1]))
	# close the file
	tf.close()

	# now that the task has been selected and targets have been indicated,
	# run the after task selection screen (after this, the task starts)
	
	return after_task_selection(settings)


def minimize_application(settings):
	
	"""Minimizes (iconifies) the application"""
	
	# minimize
	pygame.display.iconify()
	
	return settings


def next_browser_page(settings):
	
	"""Advances to the next browser page"""
	
	# reduce the current browser page
	settings[u'currentbrowserpage'] += 1
	# draw the task browser screen
	settings = browser(settings)
	
	return settings


def next_data_page(settings):
	
	"""Advances to the next data page"""
	
	# reduce the current data page	
	settings[u'currentdatapage'] += 1
	# draw the data selection screen
	settings = data_selection(settings)
	
	return settings


def next_task_page(settings):
	
	"""Advances to the next task page"""
	
	# reduce the current task page	
	settings[u'currenttaskpage'] += 1
	# draw the task selection screen
	settings = task_selection(settings)
	
	return settings


def one_dir_up(settings):
	
	"""Moves the browser one directory up"""
	
	# go up one directory
	settings[u'dir'][u'browsing'] = os.path.dirname(settings[u'dir'][u'browsing'])
	# reset the current browser page
	settings[u'currentbrowserpage'] = 0
	# draw the new browser screen
	settings[u'guiscreens'][u'browserscreen'], settings[u'guibuttons'][u'browserscreen'] = browserscreen(settings)
	# show the new browser screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def prev_browser_page(settings):
	
	"""Returns to the previous task page"""
	
	# reduce the current browser page	
	if settings[u'currentbrowserpage'] > 0:
		settings[u'currentbrowserpage'] -= 1
	# draw the task browser screen
	settings = browser(settings)
	
	return settings


def prev_data_page(settings):
	
	"""Returns to the previous data page"""
	
	# reduce the current data page	
	if settings[u'currentdatapage'] > 0:
		settings[u'currentdatapage'] -= 1
	# draw the data selection screen
	settings = data_selection(settings)
	
	return settings


def prev_task_page(settings):
	
	"""Returns to the previous task page"""
	
	# reduce the current task page	
	if settings[u'currenttaskpage'] > 0:
		settings[u'currenttaskpage'] -= 1
	# draw the task selection screen
	settings = task_selection(settings)
	
	return settings


def quit_application(settings):
	
	"""Sets the running setting to False, which will make the app shut down"""
	
	settings[u'running'] = False
	
	return settings


def run_colourpicker(settings):
	
	"""Runs a colour picker"""
	
	# get new colour
	rgb = tuple(colourpicker(settings))
	# adjust settings
	settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text'] = unicode(rgb)
	settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'colour'] = rgb
	# apply to current display
	disp = pygame.display.get_surface()
	bdict = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']]
	disp.fill(bdict[u'colour'], bdict[u'rect'])
	# render the new button
	txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
	txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
			(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
	disp.blit(txtsurf, txtpos)
	# update display
	pygame.display.flip()
	
	
	return settings


def run_numfield(settings):
	
	"""Runs a text field interaction"""
	
	rect = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'rect']
	font = settings[u'font'][u'medium'][u'bold']
	
	settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text'] = numfield(rect, font, settings)
	
	return settings


def run_textfield(settings):
	
	"""Runs a text field interaction"""
	
	rect = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'rect']
	font = settings[u'font'][u'medium'][u'bold']
	
	settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text'] = textfield(rect, font, settings)
	
	return settings


def same_browser_page(settings):
	
	"""Stays on the same browser page (doesn't do anything)"""
	
	return settings


def same_data_page(settings):
	
	"""Stays on the same data page (doesn't do anything)"""
	
	return settings


def same_task_page(settings):
	
	"""Stays on the same task page (doesn't do anything)"""
	
	return settings


def save_and_start_analysis(settings):
	
	"""Saves the analysis settings, and starts the analysis"""

	# loop through all buttons
	for b in settings[u'guibuttons'][settings[u'currentscreen']].keys():
		# input type
		if b == 0:
			settings[u'analysisproperties'][u'disthreshold'] = int(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
	
	# if the option for batch analysis is chosen, run a batch analysis
	if os.path.basename(settings[u'analysisproperties'][u'datapath']) == u"batch":
		libanalysis.batch_analysis(settings)
	# run the analysis (returns to starting screen after finishing)
	else:
		libanalysis.start_analysis(settings)
	
	return settings


def save_and_start_task(settings):
	
	"""Saves the task settings (after task selection), and starts the task"""

	# loop through all buttons
	for b in settings[u'guibuttons'][settings[u'currentscreen']].keys():
		# input type
		if b == 0:
			settings[u'taskproperties'][u'input'] = unicode(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# cancellation visibility
		elif b == 1:
			settings[u'taskproperties'][u'visible'] = unicode(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# FGC
		elif b == 2:
			exec("colourtuple = %s" % settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
			settings[u'taskproperties'][u'fgc'] = colourtuple
		
	return libtask.start_task(settings)


def save_task_settings(settings):
	
	"""Saves the task settings, and returns to the start screen"""

	# reset settings
	settings['taskproperties'] = {u'taskpath':None,
							u'visible':u'visible',
							u'ntargets':0,
							u'ndistractors':0,
							u'target':u"",
							u'distractor':[],
							u'stimsize':40,
							u'bgc':(127,127,127),
							u'fgc':(0,0,0),
							u'pw':3,
							u'ow':20,
							u'input':u'mouse'}

	# Landol C buttons
	lcbuttons = [u'o',u'u',u'd',u'l',u'r']

	# loop through all buttons
	for b in settings[u'guibuttons'][settings[u'currentscreen']].keys():
		# input type
		if b == 0:
			settings[u'taskproperties'][u'input'] = unicode(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# cancellation visibility
		elif b == 1:
			settings[u'taskproperties'][u'visible'] = unicode(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# Ntargets
		elif b == 2:
			settings[u'taskproperties'][u'ntargets'] = int(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# FGC
		elif b == 3:
			exec("colourtuple = %s" % settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
			settings[u'taskproperties'][u'fgc'] = colourtuple
		# Ndistracters
		elif b == 4:
			settings[u'taskproperties'][u'ndistractors'] = int(settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
		# BGC
		elif b == 5:
			exec("colourtuple = %s" % settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'])
			settings[u'taskproperties'][u'bgc'] = colourtuple
		# target type
		elif b in range(6,11):
			if settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'] == u"o":
				settings[u'taskproperties'][u'target'] = lcbuttons[range(6,11).index(b)]
		# target type
		elif b in range(11,16):
			if settings[u'guibuttons'][settings[u'currentscreen']][b][u'text'] == u"o":
				settings[u'taskproperties'][u'distractor'].append(lcbuttons[range(11,16).index(b)])
	
	# change the screen back to the start screen
	#settings = back_to_start(settings)
	
	return libtask.start_task(settings)


def select_this_dataset(settings):
	
	"""Selects the clicked dataset"""
	
	# task path
	dataname = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text']
	settings[u'analysisproperties'][u'datapath'] = os.path.join(settings[u'dir'][u'rawout'], dataname)
	# get display handle
	disp = pygame.display.get_surface()
	# render text
	if os.path.basename(settings[u'analysisproperties'][u'datapath']) == u'batch':
		text = u"you chose all datasets (click to continue)"
	else:
		text = u"you chose dataset '%s' (click to continue)" % dataname
	textsurf = settings[u'font'][u'medium'][u'regular'].render(text, False, settings[u'fgc'])
	textpos = (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2))
	# display message
	disp.fill(settings[u'bgc'])
	disp.blit(textsurf, textpos)
	pygame.display.flip()
	# wait for a click (allow time to unclick first)
	pygame.time.wait(200)
	while check_mouseclicks()[0] == None:
		pass
	
	return after_data_selection(settings)


def select_this_item(settings):
	
	"""Selects the clicked item"""
	
	# item path
	itemname = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text']
	itempath = os.path.join(settings[u'dir'][u'browsing'], itemname)
	
	# check if the item is a directory
	if os.path.isdir(itempath):
		# change the current browsing directory
		settings[u'dir'][u'browsing'] = itempath
		# reset the browsing page
		settings[u'currentbrowserpage'] = 0
		# draw the new browsing screen
		return browser(settings)
	
	# check if the item is a file
	if os.path.isfile(itempath):
		# check if the file is an image
		if os.path.splitext(itemname)[1] in [u'.jpg',u'.png',u'.gif',u'.bmp',u'.tif']:
			# load the image
			return load_scan(settings)
		# if the file is not an image, do nothing
		else:
			return settings
	# if the selected item is not a directory or a file, do nothing
	else:
		return settings


def select_this_task(settings):
	
	"""Selects the clicked task"""
	
	# task path
	taskname = settings[u'guibuttons'][settings[u'currentscreen']][settings[u'currentbutton']][u'text']
	settings['taskproperties'][u'taskpath'] = os.path.join(settings[u'dir'][u'tasks'], taskname)
	# get display handle
	disp = pygame.display.get_surface()
	# render text
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"you chose task '%s' (click to continue)" % taskname, False, settings[u'fgc'])
	textpos = (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2))
	# display message
	disp.fill(settings[u'bgc'])
	disp.blit(textsurf, textpos)
	pygame.display.flip()
	# wait for a click (allow time to unclick first)
	pygame.time.wait(200)
	while check_mouseclicks()[0] == None:
		pass
	
	return after_task_selection(settings)


def task_options(settings):
	
	"""Changes the current screen to the task options screen"""
	
	# create a task selection screen if it doesn't exist yet
	if not u'taskoptions' in settings[u'guiscreens'].keys():
		settings[u'guiscreens'][u'taskoptions'], settings[u'guibuttons'][u'taskoptions'] = taskoptionsscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'taskoptions'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def task_selection(settings):
	
	"""Changes the current screen to the task selection screen"""
	
	# create a task selection screen if it doesn't exist yet
	settings[u'guiscreens'][u'taskselection'], settings[u'guibuttons'][u'taskselection'] = taskselectionscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'taskselection'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings
			

def task_settings(settings):
	
	"""Changes the current screen to task settings"""

	# create new screen (with updated values)
	settings[u'guiscreens'][u'tasksettings'], settings[u'guibuttons'][u'tasksettings'] = tasksettingsscreen(settings)
	# change the current screen
	settings[u'currentscreen'] = u'tasksettings'
	# draw current screen
	disp = pygame.display.get_surface()
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	return settings


def toggle_fullscreen(settings):
	
	"""Toggles full screen mode"""
	
	# get the display
	disp = pygame.display.get_surface()
	olddisp = disp.copy()
	# get the display flags
	flags = disp.get_flags()
	# toggle fullscreen
	if flags & pygame.FULLSCREEN:
		flags = pygame.RESIZABLE
	else:
		flags = pygame.FULLSCREEN
	# set new display settings
	disp = pygame.display.set_mode(settings[u'dispsize'], flags)
	# blit old display to it
	disp.blit(olddisp, (0,0))
	pygame.display.flip()
	
	return settings


# # # # #
# GUI SCREENS

def aftertaskselectionscreen(settings):
	
	"""Draws the screen that is shown after task selection, which requires
	some further user input: the input type, the cancellation visibility, and
	the foreground colour (for the cancellation marks)
	
			task settings
		input type	(0) [mouse]
		cancellation	(1) [visible]
		mark colour	(2) [(0,0,0)]
			(3) [save]

	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# STARTUP VISUALS
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"task settings", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# TEXTS
	# text properties
	y = [int(2*ds[1]/6), int(3*ds[1]/6), int(4*ds[1]/6)]
	texts = [u"input",u"cancellations",u"mark colour"]
	# render and blit texts
	for i in range(len(texts)):
		textsurf = settings[u'font'][u'medium'][u'regular'].render(texts[i], False, settings[u'fgc'])
		textpos = (int(4*ds[0]/9 - textsurf.get_width()/2), int(ds[1]/20 + y[i] - textsurf.get_height()/2))
		screen.blit(textsurf, textpos)
	
	# BUTTONS
	# dict containing on/off button states
	buttdict = {}
	# input and cancellation visibility
	cd = {u'visible':u'o',u'invisible':u'x',u'mouse':u'o',u'touch':u'x'}
	buttdict[0] = cd[settings['taskproperties'][u'input']]
	buttdict[1] = cd[settings['taskproperties'][u'visible']]
	# button dict
			# input type
	buttons = {0:{	u'rect':[int(5*ds[0]/9), y[0], int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'input']),
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[0]],
				u'onclick':change_state},
			# cancellation visibility
			1:{	u'rect':[int(5*ds[0]/9), y[1], int(ds[0]/9), int(ds[1]/10)],
				u'text':u"visible",
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[1]],
				u'onclick':change_state},
			# FGC
			2:{	u'rect':[int(5*ds[0]/9), y[2], int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'fgc']),
				u'font':u'bold',
				u'colour':settings['taskproperties'][u'fgc'],
				u'onclick':run_colourpicker},
			# save button
			3:{	u'rect':[int(ds[0]/4), int(5*ds[1]/6), int(ds[0]/2), int(ds[1]/10)],
				u'text':u"start the task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][2],
				u'onclick':save_and_start_task}
			}

	# DRAW BUTTONS
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def afterdataselectionscreen(settings):
	
	"""Draws the screen that is shown after data selection, which requires
	some further user input
	
			analysis settings
		distance threshold	(0) [50]
			(3) [save]

	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# STARTUP VISUALS
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"analysis settings", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# TEXTS
	# text properties
	y = [int(2*ds[1]/6), int(3*ds[1]/6), int(4*ds[1]/6)]
	texts = [u"distance threshold"]
	# render and blit texts
	for i in range(len(texts)):
		textsurf = settings[u'font'][u'medium'][u'regular'].render(texts[i], False, settings[u'fgc'])
		textpos = (int(4*ds[0]/9 - textsurf.get_width()/2), int(ds[1]/20 + y[i] - textsurf.get_height()/2))
		screen.blit(textsurf, textpos)
	
	# BUTTONS
	# button dict
			# distance threshold
	buttons = {0:{	u'rect':[int(5*ds[0]/9), y[0], int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['analysisproperties'][u'disthreshold']),
				u'font':u'bold',
				u'colour':settings[u'tfbgc'],
				u'onclick':run_numfield},
			# save button
			3:{	u'rect':[int(ds[0]/4), int(5*ds[1]/6), int(ds[0]/2), int(ds[1]/10)],
				u'text':u"start the analysis",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'skyblue'][2],
				u'onclick':save_and_start_analysis}
			}

	# DRAW BUTTONS
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def browserscreen(settings):
	
	"""Draws the browser screen, which shows eight items in the current
	directory (buttons 1-8), a folder-up button (button 0), and two arrows to
	scroll through the tasks (buttons 9 and 10)
	
				select a folder
				[0]	[1]	[2]
		(9) [<]	[3]	[4]	[5]	(10) [>]
				[6]	[7]	[8]

	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# ITEMS
	# get the current directory contents
	itemnames = map(unicode, os.listdir(settings[u'dir'][u'browsing']))
	# only use eight
	si = settings[u'currentbrowserpage'] * 8
	itemnames = itemnames[si:]
	# add a dummy one as the first item
	itemnames.insert(0,u"dummy")
	# determine the colours to use
	itemcols = []
	for name in itemnames:
		if os.path.isdir(os.path.join(settings[u'dir'][u'browsing'], name)):
			itemcols.append(settings[u'colours'][u'butter'][1])
		elif os.path.isfile(os.path.join(settings[u'dir'][u'browsing'], name)):
			itemcols.append(settings[u'colours'][u'plum'][1])
		else:
			itemcols.append(settings[u'colours'][u'aluminium'][3])
	
	# DISPLAY
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# title space: full width, 1/3 of the height
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(os.path.basename(settings[u'dir'][u'browsing']), False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# ITEM BUTTONS
	# left margin: 2/15, interbutton margin: 1/15, right margin: 1/9,\
	# title height: 1/3, button height (*3): 1/6, margin hight (*2): 1/18
	# button specs
	start = [int(2*ds[0]/15), int(ds[1]/3)]
	margin = [int(ds[0]/15), int(ds[1]/18)]
	buttsize = [int(ds[0]/5), int(ds[1]/6)]
	# empty dict to contain the buttons
	buttons = {}
	# loop through buttons (left to right, top to bottom)
	bis = [range(0,3), range(3,6), range(6,9)]
	for r in range(3):
		for c in range(3):
			# get the button index
			bi = bis[r][c]
			# skip if the button index exceeds the amount of items, or is
			# the first (this will be the "folder-up")
			if bi >= len(itemnames) or bi == 0:
				continue
			# set the button dict
			buttons[bi] = {u'rect':[start[0]+c*buttsize[0]+c*margin[0], start[1]+r*buttsize[1]+r*margin[1], buttsize[0], buttsize[1]],
						u'text':itemnames[bi],
						u'font':u'bold',
						u'colour':itemcols[bi],
						u'onclick':select_this_item}
	
	# ONE DIR UP BUTTON
	buttons[0] = {	u'rect':[start[0], start[1], buttsize[0], buttsize[1]],
				u'text':u"^",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][2],
				u'onclick':one_dir_up}

	# ARROW BUTTONS
	# the left arrow button should only be active when the current task page
	# is higher than zero; the right arrow should only be active if the task
	# list is longer than nine
	if settings[u'currenttaskpage'] > 0:
		lcol = settings[u'colours'][u'skyblue'][2]
	else:
		lcol = settings[u'colours'][u'aluminium'][2]
	if len(itemnames) > 8:
		rcol = settings[u'colours'][u'skyblue'][2]
		ronc = next_browser_page
	else:
		rcol = settings[u'colours'][u'aluminium'][2]
		ronc = same_browser_page
	absize = int(ds[0]/15)
	buttons[9] = {	u'rect':[int(ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u"<",
				u'font':u'bold',
				u'colour':lcol,
				u'onclick':prev_browser_page}
	buttons[10] = {u'rect':[int(14*ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u">",
				u'font':u'bold',
				u'colour':rcol,
				u'onclick':ronc}
	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit a thumbnail
		if (0 < i < 9) and (os.path.splitext(itemnames[i])[1] in [u'.jpg',u'.png',u'.gif',u'.bmp',u'.tif']):
			imgpath = os.path.join(settings[u'dir'][u'browsing'], itemnames[i])
			imgsurf = pygame.transform.scale(pygame.image.load(imgpath),(bdict[u'rect'][2],bdict[u'rect'][3]))
			screen.blit(imgsurf,(bdict[u'rect'][0],bdict[u'rect'][1]))
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def dataselectionscreen(settings):
	
	"""Draws the data selection screen, which shows nine currently available
	datasets (buttons 0-8), and two arrows to scroll through the datasets
	(buttons 9 and 10)
	
				select a dataset
				[0]	[1]	[2]
		(9) [<]	[3]	[4]	[5]	(10) [>]
				[6]	[7]	[8]

	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# DATA
	# get all the data files
	datanames = map(unicode, os.listdir(settings[u'dir'][u'rawout']))
	# throw out anything that is not a folder
	for name in datanames:
		if not os.path.isdir(os.path.join(settings[u'dir'][u'rawout'], name)):
			datanames.pop(datanames.index(name))
	# only use eight
	si = settings[u'currentdatapage'] * 8
	datanames = datanames[si:]
	# insert the batch option as the first option
	datanames.insert(0,u"batch")
	
	# DISPLAY
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# title space: full width, 1/3 of the height
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"select a dataset", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# DATA BUTTONS
	# left margin: 2/15, interbutton margin: 1/15, right margin: 1/9
	# title height: 1/3, button height (*3): 1/6, margin hight (*2): 1/18
	# button specs
	start = [int(2*ds[0]/15), int(ds[1]/3)]
	margin = [int(ds[0]/15), int(ds[1]/18)]
	buttsize = [int(ds[0]/5), int(ds[1]/6)]
	# empty dict to contain the buttons
	buttons = {}
	# loop through buttons (left to right, top to bottom)
	bis = [range(0,3), range(3,6), range(6,9)]
	for r in range(3):
		for c in range(3):
			# get the button index
			bi = bis[r][c]
			# skip if the button index exceeds the amount of tasks
			if bi >= len(datanames):
				continue
			# set the button dict
			buttons[bi] = {u'rect':[start[0]+c*buttsize[0]+c*margin[0], start[1]+r*buttsize[1]+r*margin[1], buttsize[0], buttsize[1]],
						u'text':datanames[bi],
						u'font':u'bold',
						u'colour':settings[u'colours'][u'skyblue'][2],
						u'onclick':select_this_dataset}

	# ARROW BUTTONS
	# the left arrow button should only be active when the current task page
	# is higher than zero; the right arrow should only be active if the task
	# list is longer than nine
	if settings[u'currenttaskpage'] > 0:
		lcol = settings[u'colours'][u'skyblue'][2]
	else:
		lcol = settings[u'colours'][u'aluminium'][2]
	if len(datanames) > 9:
		rcol = settings[u'colours'][u'skyblue'][2]
		ronc = next_data_page
	else:
		rcol = settings[u'colours'][u'aluminium'][2]
		ronc = same_data_page
	absize = int(ds[0]/15)
	buttons[9] = {	u'rect':[int(ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u"<",
				u'font':u'bold',
				u'colour':lcol,
				u'onclick':prev_data_page}
	buttons[10] = {u'rect':[int(14*ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u">",
				u'font':u'bold',
				u'colour':rcol,
				u'onclick':ronc}
	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit a thumbnail
		if 0 < i < 9:
			imgpath = os.path.join(settings[u'dir'][u'rawout'], datanames[i], u'task.png')
			imgsurf = pygame.transform.scale(pygame.image.load(imgpath),(bdict[u'rect'][2],bdict[u'rect'][3]))
			screen.blit(imgsurf,(bdict[u'rect'][0],bdict[u'rect'][1]))
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def draw_top_buttons(settings, screen):
	
	"""Adds the top buttons to the screen; top row looks like this:
	
		[x] (0) [-] (1) [□] (2)				[<] (3)

	"""

	# DRAW BUTTONS
	for i in settings[u'topbuttons'].keys():
		# colour the button
		bdict = settings[u'topbuttons'][i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'small'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	return screen


def startscreen(settings):
	
	"""Draws the starting screen, showing the title and four buttons:
					CancellationTools
			(0) task		-	(1) task settings
			(2) analysis	-	(3) analysis settings
	
	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					starting screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	
	# create a new Surface
	screen = pygame.Surface(ds)
	
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# title space: full width, 1/3 of the height
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"CancellationTools", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# BUTTONS
	# left margin: 1/9, centre margin: 1/9, right margin: 1/9,
	# horizontal margin total: 1/3, button width (*2): 1/3
	# title height: 1/3, button height (*2): 1/6, margin hight (*2): 1/6
	# button specs
	top = int(ds[1]/3)
	margin = [int(ds[0]/9), int(ds[1]/6)]
	buttsize = [int(ds[0]/3), int(ds[1]/6)]
	buttons = {0:{	u'rect':[int(1.5*margin[0]), top, 2*buttsize[0], buttsize[1]],
				u'text':u"run task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][2],
				u'onclick':task_options}, # libtask.start_task
#			1:{	u'rect':[2*margin[0]+buttsize[0], top, buttsize[0], buttsize[1]],
#				u'text':u"task settings",
#				u'font':u'bold',
#				u'colour':settings[u'colours'][u'chameleon'][1],
#				u'onclick':task_options},
			2:{	u'rect':[int(1.5*margin[0]), top+buttsize[1]+margin[1], 2*buttsize[0], buttsize[1]], # margin[0], top+buttsize[1]+margin[1], buttsize[0], buttsize[1]
				u'text':u"run analysis",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'skyblue'][2],
				u'onclick':data_selection}
#			3:{	u'rect':[2*margin[0]+buttsize[0], top+buttsize[1]+margin[1], buttsize[0], buttsize[1]],
#				u'text':u"analysis settings",
#				u'font':u'bold',
#				u'colour':settings[u'colours'][u'skyblue'][1],
#				u'onclick':None}
				}

	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def taskoptionsscreen(settings):
	
	"""Draws the task options screen, showing three buttons: one to select
	a task, one to create a task, and one to put in a new (scanned) task
	
	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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

			(1)   [select a task]
			(2)   [create a task]
			(3) [load scanned task]
	"""
	
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	
	# create a new Surface
	screen = pygame.Surface(ds)
	
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# BUTTONS
	# three buttons, each half of the screen size wide, and a quarter of the
	# display size high; shown horizontally centered, at 1/4, 2/4 and 3/4 of
	# the display height
	margin = [int(ds[0]/4), int(ds[1]/4)]
	buttsize = [int(ds[0]/2), int(ds[1]/6)]
	top = int(ds[1]/4 - buttsize[1]/2)
	buttons = {0:{	u'rect':[margin[0], top, buttsize[0], buttsize[1]],
				u'text':u"select a task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][2],
				u'onclick':task_selection},
			1:{	u'rect':[margin[0], top+margin[1], buttsize[0], buttsize[1]],
				u'text':u"create a new task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][1],
				u'onclick':task_settings},
			2:{	u'rect':[margin[0], top+2*margin[1], buttsize[0], buttsize[1]],
				u'text':u"load scanned task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][0],
				u'onclick':browser}
				}

	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def taskselectionscreen(settings):
	
	"""Draws the task selection screen, which shows nine currently available
	tasks (buttons 0-8), and two arrows to scroll through the tasks
	(buttons 9 and 10)
	
				select a task
				[0]	[1]	[2]
		(9) [<]	[3]	[4]	[5]	(10) [>]
				[6]	[7]	[8]

	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# TASKS
	# get all the tasks
	tasknames = map(unicode, os.listdir(settings[u'dir'][u'tasks']))
	# only use nine
	si = settings[u'currenttaskpage'] * 9
	tasknames = tasknames[si:]
	
	# DISPLAY
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# title space: full width, 1/3 of the height
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"select a task", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# TASK BUTTONS
	# left margin: 2/15, interbutton margin: 1/15, right margin: 1/9,\
	# title height: 1/3, button height (*3): 1/6, margin hight (*2): 1/18
	# button specs
	start = [int(2*ds[0]/15), int(ds[1]/3)]
	margin = [int(ds[0]/15), int(ds[1]/18)]
	buttsize = [int(ds[0]/5), int(ds[1]/6)]
	# empty dict to contain the buttons
	buttons = {}
	# loop through buttons (left to right, top to bottom)
	bis = [range(0,3), range(3,6), range(6,9)]
	for r in range(3):
		for c in range(3):
			# get the button index
			bi = bis[r][c]
			# skip if the button index exceeds the amount of tasks
			if bi >= len(tasknames):
				continue
			# set the button dict
			buttons[bi] = {u'rect':[start[0]+c*buttsize[0]+c*margin[0], start[1]+r*buttsize[1]+r*margin[1], buttsize[0], buttsize[1]],
						u'text':tasknames[bi],
						u'font':u'bold',
						u'colour':settings[u'colours'][u'chameleon'][2],
						u'onclick':select_this_task}

	# ARROW BUTTONS
	# the left arrow button should only be active when the current task page
	# is higher than zero; the right arrow should only be active if the task
	# list is longer than nine
	if settings[u'currenttaskpage'] > 0:
		lcol = settings[u'colours'][u'skyblue'][2]
	else:
		lcol = settings[u'colours'][u'aluminium'][2]
	if len(tasknames) > 9:
		rcol = settings[u'colours'][u'skyblue'][2]
		ronc = next_task_page
	else:
		rcol = settings[u'colours'][u'aluminium'][2]
		ronc = same_task_page
	absize = int(ds[0]/15)
	buttons[9] = {	u'rect':[int(ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u"<",
				u'font':u'bold',
				u'colour':lcol,
				u'onclick':prev_task_page}
	buttons[10] = {u'rect':[int(14*ds[0]/15-absize/2), int(start[1]+buttsize[1]+margin[1]), absize, absize],
				u'text':u">",
				u'font':u'bold',
				u'colour':rcol,
				u'onclick':ronc}
	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit a thumbnail
		if i < 9:
			imgpath = os.path.join(settings[u'dir'][u'tasks'], tasknames[i], u'task.png')
			imgsurf = pygame.transform.scale(pygame.image.load(imgpath),(bdict[u'rect'][2],bdict[u'rect'][3]))
			screen.blit(imgsurf,(bdict[u'rect'][0],bdict[u'rect'][1]))
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons


def tasksettingsscreen(settings):
	
	"""Draws the task settings screen, showing the title and 15 buttons:
						task settings
			path				-	[..........] (0) [o x] (1)
			ntargets			-	[...] (2)
			ndistractors		-	[...] (3)
			fgc				-	[...] (4)
			bgc				-	[...] (5)

								 o	 u	 d	 l	 r			
			target type		-	(6)	(7)	(8)	(9)	(10)
			distractor types	-	(11)	(12)	(13)	(14)	(16)
			
						[SAVE CHANGES] (17)
	
	arguments
	
	settings		-	the app settings dict
	
	returns
	
	surface, dict	-	surface is a PyGame Surface instance, showing the
					task settings screen screen
					dict is a buttondict, containing the buttons above
					(see numbers in the docstring), for each with keys:
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
	
	# LOAD STIMULI
	# stimuli and corresponding buttons
	stimdict = {	u'o':[6,11],
				u'u':[7,12],
				u'd':[8,13],
				u'l':[9,14],
				u'r':[10,15]}
	# dict containing on/off button states
	buttdict = {}
	# set all buttons to off
	for i in range(6,16):
		buttdict[i] = u'x'
	# fill out on states
	buttdict[stimdict[settings['taskproperties'][u'target']][0]] = u'o'
	for d in settings['taskproperties'][u'distractor']:
		buttdict[stimdict[d][1]] = u'o'
	# input and cancellation visibility
	cd = {u'visible':u'o',u'invisible':u'x',u'mouse':u'o',u'touch':u'x'}
	buttdict[0] = cd[settings['taskproperties'][u'input']]
	buttdict[1] = cd[settings['taskproperties'][u'visible']]

	# STARTUP VISUALS
	# convenience renaming
	ds = settings[u'dispsize']
	dc = settings[u'dispcentre']
	# create a new Surface
	screen = pygame.Surface(ds)
	# fill it with the background colour
	screen.fill(settings[u'bgc'])
	
	# TITLE
	# title space: full width, 1/3 of the height
	# render title surface
	titsurf = settings[u'font'][u'large'][u'bold'].render(u"task settings", False, settings[u'fgc'])
	# title position
	titpos = [dc[0]-titsurf.get_width()/2, ds[1]/6-titsurf.get_height()/2]
	# draw the title
	screen.blit(titsurf,titpos)
	
	# TEXTS
	texts = {	u"input":(int(2*ds[0]/18), int(7*ds[1]/18)),
			u"cancellations":(int(6*ds[0]/18), int(7*ds[1]/18)),
			u"targets":(int(2*ds[0]/18), int(9*ds[1]/18)),
			u"FGC":(int(6*ds[0]/18), int(9*ds[1]/18)),
			u"distractors":(int(2*ds[0]/18), int(11*ds[1]/18)),
			u"BGC":(int(6*ds[0]/18), int(11*ds[1]/18)),
			u"target":(int(11*ds[0]/18), int(9*ds[1]/18)),
			u"distractor":(int(11*ds[0]/18), int(11*ds[1]/18))}
	for t in texts.keys():
		surf = settings[u'font'][u'medium'][u'regular'].render(t, False, settings[u'fgc'])
		blitpos = (int(texts[t][0] - surf.get_width()/2), int(texts[t][1] - surf.get_height()/2))
		screen.blit(surf, blitpos)
	
	# LANDOLT C
	# properties (also used for buttons below!)
	LCsize = int(2*ds[0]/45)
	space = int(ds[0]/45)
	sx = int(2*ds[0]/3)
	y = [int(ds[1]/3 + ((ds[1]/9)/2-LCsize/2)),	# row 1 (Landolt Cs)
		int(4*ds[1]/9 + ((ds[1]/9)/2-LCsize/2)),	# row 2 (target buttons)
		int(5*ds[1]/9 + ((ds[1]/9)/2-LCsize/2))]	# row 3 (distractor buttons)
	LCrect = {u'o':[sx, y[0], LCsize, LCsize],				# 'o'
			u'u':[sx+LCsize+space, y[0], LCsize, LCsize],		# 'u'
			u'd':[sx+2*LCsize+2*space, y[0], LCsize, LCsize],	# 'd'
			u'l':[sx+3*LCsize+3*space, y[0], LCsize, LCsize],	# 'l'
			u'r':[sx+4*LCsize+4*space, y[0], LCsize, LCsize]}	# 'r'
	# draw the Landolt Cs
	for direction in LCrect.keys():
		surf = draw_Landolt_C(LCsize, direction, settings[u'fgc'], None, int(LCsize/8), int(LCsize/3))
		screen.blit(surf, (LCrect[direction][0],LCrect[direction][1]))
	
	# BUTTONS
	# left margin: 1/9, centre margin: 1/9, right margin: 1/9,
	# horizontal margin total: 1/3, button width (*2): 1/3
	# title height: 1/3, button height (*2): 1/6, margin hight (*2): 1/6
	# button specs
			# input type
	buttons = {0:{	u'rect':[int(3*ds[0]/18), int(ds[1]/3), int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'input']),
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[0]],
				u'onclick':change_state},
			# cancellation visibility
			1:{	u'rect':[int(7*ds[0]/18), int(ds[1]/3), int(ds[0]/9), int(ds[1]/10)],
				u'text':u"visible",
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[1]],
				u'onclick':change_state},
			# ntargets
			2:{	u'rect':[int(3*ds[0]/18), int(ds[1]/3 + ds[1]/9), int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'ntargets']),
				u'font':u'bold',
				u'colour':settings[u'tfbgc'],
				u'onclick':run_numfield},
			# FGC
			3:{	u'rect':[int(7*ds[0]/18), int(ds[1]/3 + ds[1]/9), int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'fgc']),
				u'font':u'bold',
				u'colour':settings['taskproperties'][u'fgc'],
				u'onclick':run_colourpicker},
			# ndistracters
			4:{	u'rect':[int(3*ds[0]/18), int(ds[1]/3 + 2*ds[1]/9), int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'ndistractors']),
				u'font':u'bold',
				u'colour':settings[u'tfbgc'],
				u'onclick':run_numfield},
			# BGC
			5:{	u'rect':[int(7*ds[0]/18), int(ds[1]/3 + 2*ds[1]/9), int(ds[0]/9), int(ds[1]/10)],
				u'text':unicode(settings['taskproperties'][u'bgc']),
				u'font':u'bold',
				u'colour':settings['taskproperties'][u'bgc'],
				u'onclick':run_colourpicker},
			# target 'o'
			6:{	u'rect':[sx, y[1], LCsize, LCsize],
				u'text':buttdict[6],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[6]],
				u'onclick':change_state},
			# target 'u'
			7:{	u'rect':[sx+LCsize+space, y[1], LCsize, LCsize],
				u'text':buttdict[7],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[7]],
				u'onclick':change_state},
			# target 'd'
			8:{	u'rect':[sx+2*LCsize+2*space, y[1], LCsize, LCsize],
				u'text':buttdict[8],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[8]],
				u'onclick':change_state},
			# target 'l'
			9:{	u'rect':[sx+3*LCsize+3*space, y[1], LCsize, LCsize],
				u'text':buttdict[9],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[9]],
				u'onclick':change_state},
			# target 'r'
			10:{	u'rect':[sx+4*LCsize+4*space, y[1], LCsize, LCsize],
				u'text':buttdict[10],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[10]],
				u'onclick':change_state},
			# distractor 'o'
			11:{	u'rect':[sx, y[2], LCsize, LCsize],
				u'text':buttdict[11],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[11]],
				u'onclick':change_state},
			# distractor 'u'
			12:{	u'rect':[sx+LCsize+space, y[2], LCsize, LCsize],
				u'text':buttdict[12],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[12]],
				u'onclick':change_state},
			# distractor 'd'
			13:{	u'rect':[sx+2*LCsize+2*space, y[2], LCsize, LCsize],
				u'text':buttdict[13],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[13]],
				u'onclick':change_state},
			# distractor 'l'
			14:{	u'rect':[sx+3*LCsize+3*space, y[2], LCsize, LCsize],
				u'text':buttdict[14],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[14]],
				u'onclick':change_state},
			# distractor 'r'
			15:{	u'rect':[sx+4*LCsize+4*space, y[2], LCsize, LCsize],
				u'text':buttdict[15],
				u'font':u'bold',
				u'colour':settings[u'onoffcol'][buttdict[15]],
				u'onclick':change_state},
			# save changes
			16:{	u'rect':[int(ds[0]/3), int(7*ds[1]/9), int(ds[0]/3), int(ds[1]/9)],
				u'text':u"start the task",
				u'font':u'bold',
				u'colour':settings[u'colours'][u'chameleon'][2],
				u'onclick':save_task_settings}
				}
	# draw the buttons
	for i in buttons.keys():
		# colour the button
		bdict = buttons[i]
		screen.fill(bdict[u'colour'], bdict[u'rect'])
		# render and blit the text
		txtsurf = settings[u'font'][u'medium'][bdict[u'font']].render(bdict[u'text'], False, settings[u'fgc'])
		txtpos = [(bdict[u'rect'][0]+bdict[u'rect'][2]/2)-txtsurf.get_width()/2,
				(bdict[u'rect'][1]+bdict[u'rect'][3]/2)-txtsurf.get_height()/2]
		screen.blit(txtsurf, txtpos)
	
	# draw the top buttons
	screen = draw_top_buttons(settings, screen)
	
	return screen, buttons

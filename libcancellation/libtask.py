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
from libinput import check_click, check_mouseclicks, textfield
from libhelper import check_colour, draw_Landolt_C

# native
import os
import random
import time

# external
import numpy
import pygame


# # # # #
# FUNCTIONS

def start_task(settings):
	
	"""Prepares the task, and runs it (saving data happens while running);
	afterwards the settings are returned, with adjusted analysis properties
	so that the data that has just been collected can be analyzed
	
	arguments
	
	settings		-	app settings dict, which includes a dict on the task
					properties
	
	returns
	
	settings		-	same settings dict as was passed, with updated
					analysis settings
	"""
	
	# get display
	disp = pygame.display.get_surface()
	
	# set display to fullscreen mode
	flags = disp.get_flags()
	if not flags & pygame.FULLSCREEN:
		flags = pygame.FULLSCREEN
		disp = pygame.display.set_mode(settings[u'dispsize'], flags)
	
	# inputrect
	inputrect = [	int(settings[u'dispcentre'][0]-settings[u'dispsize'][0]/4),
				int(settings[u'dispcentre'][1]-settings[u'dispsize'][1]/12),
				int(settings[u'dispsize'][0]/2),
				int(settings[u'dispsize'][0]/6)]

	# draw text input screen	
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"please provide a filename", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispsize'][1]/4-textsurf.get_height()/2)))
	disp.fill(settings[u'tfbgc'], inputrect)
	pygame.display.flip()
	
	# ask for the participant name
	settings[u'ppname'] = textfield(inputrect, settings[u'font'][u'large'][u'regular'], settings, loadtext=False)
	
	# show loading message
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"starting task, please wait", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2)))
	pygame.display.flip()
	
	# initialize new Task
	task = Task(settings)
	
	# prepare task
	task.prepare()
	
	# run task
	task.run()
	
	# show ending screen
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"thank you for participating", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispsize'][1]/3-textsurf.get_height()/2)))
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"(click to return to the main menu)", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(2*settings[u'dispsize'][1]/3-textsurf.get_height()/2)))
	pygame.display.flip()
	
	# wait for a click (allowing some time to unclick)
	pygame.time.wait(200)
	while check_mouseclicks()[0] == None:
		pass
	
	# switch back to start screen
	settings[u'currentscreen'] = u'start'
	disp.blit(settings[u'guiscreens'][settings[u'currentscreen']], (0,0))
	pygame.display.flip()
	
	# allow a bit of time to unclick
	pygame.time.wait(200)
	
	return settings


# # # # #
# CLASSES

class Task():
	
	"""The Task class if for running a task, and storing the produced data"""
	
	def __init__(self, settings):
		
		"""Initializes a Task instance, which will be based on the passed
		task properties
		
		arguments
		
		settings		-	the app settings dict, which contains a
						taskproperties dict, with the following keys:
							"taskpath"	-	full path to a task, or
											None to set up a new
											task
							"ntargets"	-	number of targets
							"ndistractors"	-	number of distractors
							"target"		-	targettype, either a
											circle or a direction
											of Landolt C ('o','u',
											'd','l','r')
							"distractor"	-	list of distractortypes
											that the (choose from
											circle and directions of
											Landolt C ('o','u','d',
											'l','r')
							"stimsize"	-	size of the stimulus,
											an integer value that
											represents both the
											width and the height
							"bgc"		-	backgroundcolour, a
											(R,G,B) tuple
							"fgc"		-	foregroundcolour, a
											(R,G,B) tuple
							"pw"			-	penwidth (integer)
							"ow"			-	opening width (integer)
							"input"		-	input type (string),
											either 'touch' or 'mouse'
						if the taskname is provided, the other settings
						will be ignored, and an error will be returned
						on running if the taskname does not exist
		"""
		
		# read taskproperties
		taskproperties = settings['taskproperties']
		
		# settings
		self.error = []
		self.dispsize = settings['dispsize']
		self.properties = {	u'target':None,
						u'visible':u'visible',
						u'distractor':[],
						u'ntargets':int(taskproperties[u'ntargets']),
						u'ndistractors':int(taskproperties[u'ndistractors']),
						u'stimsize':int(taskproperties[u'stimsize']),
						u'fgc':None,
						u'bgc':None,
						u'pw':int(taskproperties[u'pw']),
						u'ow':int(taskproperties[u'ow']),
						u'input':u'mouse'}
		self.ppname = settings[u'ppname']
		self.savebutton = {	u'fgc':settings[u'colours'][u'aluminium'][0],
						u'bgc':settings[u'colours'][u'chameleon'][2],
						u'font':settings[u'font'][u'medium'][u'bold']}

		# current time
		try:
			self.date = time.strftime(u"%Y-%m-%d")
			self.time = time.strftime(u"%T")
		except:
			ct = time.localtime()
			self.date = time.strftime(u"%4.f-%2.f-%2.f" % (ct.tm_year, ct.tm_mon, ct.tm_mday))
			self.time = time.strftime(u"%2.f:%2.f:%2.f" % (ct.tm_hour, ct.tm_min, ct.tm_sec))
			self.date = self.date.replace(u' ', '0')
			self.time = self.time.replace(u' ', '0')
		self.outdir = os.path.join(settings[u'dir'][u'rawout'], u"%s_%s_%s" % (self.ppname, self.date, self.time.replace(u':',u'-')))

		# check if a path to the task was provided
		if taskproperties[u'taskpath'] != None:
			self.existing = True
			self.path = taskproperties[u'taskpath']
			self.name = os.path.split(self.path)[1]
		# if not, use a new name (format: "yyyy_mm_dd_hh:mm:ss")
		else:
			self.existing = False
			self.name = u"%s_%s" % (self.date, self.time)
			self.name = self.name.replace(u':',u'-') # Windows proof filename
			self.path = os.path.join(settings['dir']['tasks'], self.name)
		
		# check target and distractor properties
		allowed = ('o','u','d','l','r')
		if taskproperties[u'target'] in allowed:
			# if the target is valid, add it to the properties
			self.properties[u'target'] = taskproperties[u'target']
		else:
			# if the target is invalid, add an error to the list
			self.error.append(u"target '%s' is not a valid target argument" % self.properties[u'target'])
		for d in taskproperties[u'distractor']:
			# loop through distarctors
			if d in allowed:
				# if the distarctor is valid, add it to the properties
				self.properties[u'distractor'].append(d)
			else:
				# if the distractor is invalid, add an error to the list
				self.error.append(u"distractor '%s' is not a valid target argument" % d)
		
		# check the colours
		for p in [u'fgc', u'bgc']:
			# if the colour is invalid, add an error to the error list
			if type(check_colour(taskproperties[p])) == str:
				self.error.append(check_colour(taskproperties[p]))
			# if the colour is valid, add it to the properties
			else:
				self.properties[p] = check_colour(taskproperties[p])
		
		# check the input
		# if the colour is invalid, add an error to the error list
		if taskproperties[u'input'] not in [u'mouse',u'touch']:
			self.error.append(u"invalid input type '%s'; use 'mouse' or 'touch'" % taskproperties[u'input'])
		# if the colour is valid, add it to the properties
		else:
			self.properties[u'input'] = taskproperties[u'input']
		
		# check the cancellation visibility
		# if the colour is invalid, add an error to the error list
		if taskproperties[u'visible'] not in [u'visible',u'invisible']:
			self.error.append(u"invalid cancellation visibility type '%s'; use 'visible' or 'invisible'" % taskproperties[u'visible'])
		# if the colour is valid, add it to the properties
		else:
			self.properties[u'visible'] = taskproperties[u'visible']


	def prepare(self):
		
		"""Prepares the task. If the taskname is not None, an attempt will be
		made to load the task, and an error will be produced if the task
		file does not exist. If the taskname is None, a new task will be
		created using the set properties, and an error will be produced if
		any of the properties was invalid
		
		arguments
		
		None
		
		returns
		
		None
		"""

		preperror = None
		
		# FROM FILE
		if self.existing:
			# check if the file exists
			if not os.path.isdir(self.path):
				preperror = u"task '%s' (full path '%s') not found" % (self.name,self.path)
			# load the image
			else:
				self.image = pygame.image.load(os.path.join(self.path, u'task.png'))
		
		# FROM PROPERTIES
		else:
			# create new directory
			os.mkdir(self.path)

			# open text file to save target locations
			tf = open(os.path.join(self.path, u'targets.txt'), 'w')
			# write header
			header = [u"target", u"x", u"y"]
			tf.write(u'\t'.join(header) + u"\n")
			
			# create new Surface
			self.image = pygame.Surface(self.dispsize)
			self.image.fill(self.properties[u'bgc'])
			
			# calculate the optimal grid configuration
			nstim = self.properties[u'ntargets'] + self.properties[u'ndistractors']
			grid = [nstim, 1] # columns, rows
			secondbest = [nstim, 1]
			# loop through all potential options, checking which is the
			# best grid configuration (i.e. the one that resembles the
			# display w/h ratio best)
			for cols in range(1,nstim):
				# calculate the amount of rows for the current number of
				# columns
				rows = nstim / float(cols)
				# check if the number of rows is an integer number
				if rows % 1 == 0:
					# check if the grid resembles the display resolution
					# ratio best
					if abs((cols / rows)-(self.dispsize[0]/float(self.dispsize[1]))) < abs((grid[0] / float(grid[1]))-(self.dispsize[0]/float(self.dispsize[1]))):
						grid = [cols, int(rows)]
				# keep track of the second best solution, in case the
				# numbers don't really add up to a neat grid configuration
				else:
					if abs((cols / rows)-(self.dispsize[0]/float(self.dispsize[1]))) < abs((grid[0] / float(grid[1]))-(self.dispsize[0]/float(self.dispsize[1]))):
						secondbest = [cols, int(numpy.ceil(rows))]

			# check if the grid configuration is ok
			if not grid[0] / float(nstim) <= 0.15:
				# if not, use the second best configuration
				grid = secondbest
			
			# stimuli are placed on a grid, with a jitter for each element
			# interdistances (amount of space between stimuli divided by
			# the amount of inter-stimulus spaces)
			hintdist = int((self.dispsize[0] - (grid[0] * self.properties[u'stimsize'])) / (grid[0]+1))
			vintdist = int((self.dispsize[1] - (grid[1] * self.properties[u'stimsize'])) / (grid[1]+1))
			# all the grid coordinates
			gridx = hintdist + numpy.arange(0,grid[0],1) * (hintdist+self.properties[u'stimsize'])
			gridy = vintdist + numpy.arange(0,grid[1],1) * (vintdist+self.properties[u'stimsize'])
			# create all the stimulus coordinates
			stimx = numpy.hstack(grid[1]*[gridx])
			stimx.sort()						# e.g. [1,1,1,2,2,2]
			stimy = numpy.hstack(grid[0]*[gridy])	# e.g. [1,2,3,1,2,3]
			# jitter is max half a stimulus interdistance in all directions
			stimx += (numpy.random.rand(len(stimx)) * self.properties[u'stimsize']) - self.properties[u'stimsize']/2
			stimy += (numpy.random.rand(len(stimy)) * self.properties[u'stimsize']) - self.properties[u'stimsize']/2
			
			# ommit the superfluous stimuli, in case there are any (i.e. if
			# the second best grid configuration was used)
			stimx = stimx[:nstim]
			stimy = stimy[:nstim]

			# targets per column
			tarpcol = int(numpy.floor(self.properties[u'ntargets'] / float(grid[0])))
			colnrs = range(grid[0])
			extra = []
			for i in range(self.properties[u'ntargets'] - tarpcol*grid[0]):
				extra.append(colnrs.pop(colnrs.index(random.choice(colnrs))))
			
			# empty vectors for the coordinates
			tari = []
			tarx = numpy.zeros(self.properties[u'ntargets'])
			tary = numpy.zeros(self.properties[u'ntargets'])
			
			# loop through columns
			for colnr in range(grid[0]):
				# the number of targets in this column
				nt = tarpcol + int(colnr in extra)
				# random order of indexes in this column, take the first
				# couple of indexes as target indexes
				indexes = numpy.random.permutation(grid[1])[:nt]
				# correct the index number, as all stimulus coordinates
				# are stored in one long vector
				indexes += colnr * grid[1]
				# add to the target indexes
				tari.extend(indexes)
			# assign target coordinates
			for i in range(self.properties[u'ntargets']):
				tarx[i] = stimx[tari[i]]
				tary[i] = stimy[tari[i]]

			# draw stimli
			for i in range(nstim):
				# determine stimulus type
				if i in tari:
					# set direction to target
					direction = self.properties[u'target']
					# write stimulus coordinates to file
					tf.write(u"%s\t%d\t%d\n" % (self.properties[u'target'],int(stimx[i]+self.properties[u'stimsize']/2),int(stimy[i]+self.properties[u'stimsize']/2)))
				else:
					# set direction to a random distractor
					direction = random.choice(self.properties[u'distractor'])
				# draw stimulus (size, direction, fgc, bgc, pw, ow)
				surf = draw_Landolt_C(self.properties[u'stimsize'],
								direction,
								self.properties[u'fgc'],
								self.properties[u'bgc'],
								self.properties[u'pw'],
								self.properties[u'ow'])
				# blit distractor to image
				self.image.blit(surf, (stimx[i],stimy[i]))

			# neatly close text file with stimulus coordinates
			tf.close()

			# save task image
			pygame.image.save(self.image, os.path.join(self.path, u'task.png'))


	def run(self):
		
		"""Runs the task, using the prepared task image; an output file is
		created in the raw output directory
		
		arguments
		
		None
		
		returns
		
		None
		"""
		
		# create a new raw output directory
		os.mkdir(self.outdir)
		
		# open a new output file
		outfile = open(os.path.join(self.outdir, u'raw.txt'), u'w')
		header = [u'ppname', u'taskname', u'testdate', u'testtime', u'input', u'cancellations', u'time', u'x', u'y']
		outfile.write(u'\t'.join(header) + u'\n')
		
		# get the display
		disp = pygame.display.get_surface()
		
		# blit the stimulus image
		disp.blit(self.image, (0,0))
		
		# save button properties
		saverect = [	int(self.dispsize[0]-self.dispsize[0]/20),
					int(self.dispsize[1]-self.dispsize[1]/20),
					int(self.dispsize[0]/20),
					int(self.dispsize[1]/20)]
		savetext = self.savebutton[u'font'].render(u"done", False, self.savebutton[u'fgc'])
		savetextpos = (int(saverect[0]+saverect[2]/2 - savetext.get_width()/2),
					int(saverect[1]+saverect[3]/2 - savetext.get_height()/2))

		# show save button
		disp.fill(self.savebutton[u'bgc'], saverect)
		disp.blit(savetext, savetextpos)

		# show the display
		pygame.display.flip()
		t0 = pygame.time.get_ticks()
		
		# hide the cursor if the input is by touch
		# (we do this in a sily way, due to the fact that with an invisible cursor
		# - as by pygame.mouse.set_visible(False) - the mouse position gives weird
		# values, usually with an x of 0)
		if self.properties[u'input'] == u'touch':
			# get the old cursor
			cursor = pygame.mouse.get_cursor()
			# set an invisible cursor
			pygame.mouse.set_cursor((8,8),(0,0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0))
		
		# run until Escape
		running = True
		while running:
			# check if there is a mouse click or a keypress
			for event in pygame.event.get():
#				# check if there was a keypress
#				if event.type == pygame.KEYDOWN:
#					# check if the Escape key is pressed
#					if event.key == pygame.K_ESCAPE:
#						running = False
				# check if there was a mouseclick
				if event.type == pygame.MOUSEBUTTONDOWN:
					# if the click was on the save button, stop the task
					if check_click(event.pos, saverect):
						running = False
					# if the click was not on the save button
					else:
						# get timestamp
						t1 = pygame.time.get_ticks()
						# write position to output file
						line = [self.ppname, self.name, self.date, self.time, self.properties[u'input'], self.properties[u'visible'], unicode(t1-t0), unicode(event.pos[0]), unicode(event.pos[1])]
						outfile.write(u'\t'.join(line) + u'\n')
						# draw a cross centered around the click position,
						# with starting and ending positions based on click
						spos = [	[int(event.pos[0]-self.properties[u'stimsize']/2),	# top left x
								int(event.pos[1]-self.properties[u'stimsize']/2)],	# top left y
								[int(event.pos[0]-self.properties[u'stimsize']/2),	# bottom left x
								int(event.pos[1]+self.properties[u'stimsize']/2)]]	# bottom left y
						epos = [	[int(event.pos[0]+self.properties[u'stimsize']/2),	# bottom right x
								int(event.pos[1]+self.properties[u'stimsize']/2)],	# bottom right y
								[int(event.pos[0]+self.properties[u'stimsize']/2),	# top right x
								int(event.pos[1]-self.properties[u'stimsize']/2)]]	# top right y
						# draw lines
						pygame.draw.line(disp, self.properties[u'fgc'], spos[0], epos[0], self.properties[u'pw'])
						pygame.draw.line(disp, self.properties[u'fgc'], spos[1], epos[1], self.properties[u'pw'])
						# update the display only if the cancellations are
						# supposed to be visible
						if self.properties[u'visible'] == u'visible':
							pygame.display.flip()

		# after running, close the textfile
		outfile.close()

		# save the image with all cancellation marks
		pygame.image.save(disp, os.path.join(self.outdir, u'task.png'))

		# reshow the cursor
		if self.properties[u'input'] == u'touch':
			# set the old cursor back
			pygame.mouse.set_cursor(cursor[0],cursor[1],cursor[2],cursor[3])

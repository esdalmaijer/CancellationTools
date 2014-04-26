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
from libhelper import gaussian, intersection, pearsonr
from libinput import check_mouseclicks

# native
import copy
import math
import os

# external
from matplotlib import font_manager, image, pyplot
import numpy
import pygame


# # # # #
# FUNCTIONS

def batch_analysis(settings):
	
	"""Runs an analysis for every single dataset that is in the data folder,
	saving the output while running; afterwards all the output text files are
	read and their content is combined into a single text file
	
	arguments
	
	settings		-	app settings dict, which includes a dict on the task
					properties
	
	returns
	
	settings		-	same settings dict as was passed (updated)
	"""
	
	# get display
	disp = pygame.display.get_surface()
	disp.fill(settings[u'bgc'])
	
	# loop through all data folders
	alldata = os.listdir(settings[u'dir'][u'rawout'])
	for i in range(len(alldata)):
		# set the new datafile
		settings[u'analysisproperties'][u'datapath'] = os.path.join(settings[u'dir'][u'rawout'], alldata[i])
		# show waiting message
		disp.fill(settings[u'bgc'])
		textsurf = settings[u'font'][u'large'][u'regular'].render(u"running analysis %d/%d, please wait..." % (i+1, len(alldata)), False, settings[u'fgc'])
		disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2)))
		pygame.display.flip()
		# prepare new Analysis
		analysis = Analysis(settings)
		# run analysis
		analysis.run()
	
	# show waiting message
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"combining %d data files, please wait..." % (len(alldata)), False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2)))
	pygame.display.flip()
	# create a new text file in a new batch folder
	batchtxt = open(os.path.join(settings[u'dir'][u'out'], u'batch.txt'), u'w')
	# loop through all output textfiles
	i = 0
	for dataset in alldata:
		# only use if the dataset is in fact a data set
		if os.path.isdir(os.path.join(settings[u'dir'][u'out'], dataset)):
			# read the textfile
			txtfile = open(os.path.join(settings[u'dir'][u'out'], dataset, u'summary.txt'), u'r')
			lines = txtfile.readlines()
			# write the line to the output (and the header if this is the
			# first file that is being read)
			if i == 0:
				batchtxt.write(u"ppname\tdate\ttime\t" + lines[0])
			batchtxt.write(u"%s\t%s\t%s\t" % (dataset[:-20], dataset[-19:-9], dataset[-8:].replace(u'-',u':')) + lines[1] + u'\n')
			# increase iteration number
			i += 1
	# close batch text file
	batchtxt.close()
	
	# show ending screen
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"the analysis was succesfully completed", False, settings[u'fgc'])
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


def start_analysis(settings):
	
	"""Prepares the analysis, and runs it (saving data happens while running);
	afterwards the settings are returned
	
	arguments
	
	settings		-	app settings dict, which includes a dict on the task
					properties
	
	returns
	
	settings		-	same settings dict as was passed (updated)
	"""
	
	# get display
	disp = pygame.display.get_surface()
	disp.fill(settings[u'bgc'])
	
	# show loading message
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"running analysis, please wait...", False, settings[u'fgc'])
	disp.blit(textsurf, (int(settings[u'dispcentre'][0]-textsurf.get_width()/2), int(settings[u'dispcentre'][1]-textsurf.get_height()/2)))
	pygame.display.flip()
	
	# prepare new Analysis
	analysis = Analysis(settings)
	
	# run analysis
	analysis.run()
	
	# show ending screen
	disp.fill(settings[u'bgc'])
	textsurf = settings[u'font'][u'large'][u'regular'].render(u"the analysis was succesfully completed", False, settings[u'fgc'])
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

class Analysis():
	
	"""The Analysis class if for running an analysis on stored data"""
	
	def __init__(self, settings):
		
		"""Initializes an Analysis instance, which will be based on the
		passed analysis properties
		
		arguments
		
		settings		-	the app settings dict, which contains an
						analysisproperties dict, with the following keys:
							"datapath"	-	full path to a raw data
											directory
							"disthreshold"	-	distance threshold for
											transforming click
											coordinates to target
											coordinates (every
											click ourside of this
											threshold of any target
											will be disregarded)
		"""
		
		# version
		self.version = settings[u'version']
		# read analysis properties
		self.properties = settings[u'analysisproperties']
		
		# check if the datapath exists
		if os.path.isdir(self.properties[u'datapath']):
			# store the data directory
			self.datadir = self.properties[u'datapath']
			self.ppname = os.path.basename(self.datadir)
			# create a new output directory
			self.outdir = os.path.join(settings[u'dir'][u'out'],self.ppname)
			if not os.path.isdir(self.outdir):
				os.mkdir(self.outdir)
		
		# path to the main task directory (will be used later on to grab the
		# task image from)
		self.taskdir = settings[u'dir'][u'tasks']
		
		# PLOT STUFF
		# dots per inch (float!)
		self.dpi = 100.0
		# PDF size in inches
		self.pdfsize = (8.27,11.69)
		# colour to make things look pretty
		self.colours = copy.deepcopy(settings[u'colours'])
		# transform the colours to matplotlib colours (between 0 and 1)
		for k in self.colours.keys():
			for i in range(len(self.colours[k])):
				self.colours[k][i] = (self.colours[k][i][0]/255.0, self.colours[k][i][1]/255.0, self.colours[k][i][2]/255.0)
		# set the font
		self.fontprop = font_manager.FontProperties(fname=settings[u'dir'][u'plotfont'])
		self.boldfontprop = font_manager.FontProperties(fname=settings[u'dir'][u'boldplotfont'])
		
		# prepare the analysis
		self.prepare()
	
	
	def prepare(self):
		
		"""Prepares the analysis, by reading the raw data file and creating
		some variables accordingly; among these are a dict with paths to all
		relevant files, the participant name, the task name, the task date,
		the task time, the input type, the cancellation visibility, and the
		raw x and y coordinates, along with timestamps
		"""

		# FILE DICT
		# create a files dict, to contain paths to all relevant files
		self.files = {}
		# add the raw data file and the marked task image to the files dict
		self.files[u'raw'] = os.path.join(self.datadir, u'raw.txt')
		self.files[u'marked'] = os.path.join(self.datadir, u'task.png')
		
		# READ DATAFILE
		# open the data file
		df = open(self.files[u'raw'], 'r')
		# read all lines
		raw = df.readlines()
		# clean up and split the lines
		for i in range(len(raw)):
			raw[i] = raw[i].replace(u'\n',u'').replace(u'\r',u'').replace(u'"',u'').split(u'\t')
		# extract the header
		header = raw.pop(0)
		
		# STOP FURTHER PROCESSING IF THE FILE IS EMPTY
		if len(raw) < 1:
			self.fileisempty = True
			return
		else:
			self.fileisempty = False
		
		# SETTINGS
		# set some variables
		self.ppname = raw[0][header.index(u'ppname')]
		self.taskname = raw[0][header.index(u'taskname')]
		self.testdate = raw[0][header.index(u'testdate')]
		self.testtime = raw[0][header.index(u'testtime')]
		self.inputtype = raw[0][header.index(u'input')]
		self.visibility = raw[0][header.index(u'cancellations')]
		# add the task image and task coordinates path to the files dict
		self.files[u'task'] = os.path.join(self.taskdir, self.taskname, u'task.png')
		self.files[u'taskcors'] = os.path.join(self.taskdir, self.taskname, u'targets.txt')
		
		# IMAGE SETTINGS
		# load images
		self.taskimg = image.imread(self.files[u'task'])
		# image size in pixels
		self.dispsize = (int(numpy.size(self.taskimg,axis=1)),int(numpy.size(self.taskimg,axis=0)))
		# image size in inches
		self.figsize = (self.dispsize[0]/self.dpi, self.dispsize[1]/self.dpi)
		
		# DATA EXTRACTION
		# empty lists to contain data points
		self.time = []
		self.x = []
		self.y = []
		self.cors = []
		# extract data
		for i in range(len(raw)):
			self.time.append(raw[i][header.index(u'time')])
			self.x.append(raw[i][header.index(u'x')])
			self.y.append(raw[i][header.index(u'y')])
			self.cors.append((int(self.x[i]),int(self.y[i])))
		# lists to numpy arrays of integers
		self.time = numpy.array(self.time, dtype=int)
		self.x = numpy.array(self.x, dtype=int)
		self.y = numpy.array(self.y, dtype=int)
		# task duration
		self.duration = {u'total':self.time[-1]} # ms
		h = numpy.floor(self.duration[u'total'] / 3600000.0)
		m = numpy.floor((self.duration[u'total']-h*3600000.0) / 60000.0)
		s = numpy.ceil(((self.duration[u'total']-h*3600000.0)-m*60000.0) / 1000.0)
		self.duration[u'string'] = u"%2.f:%2.f:%2.f" % (h,m,s)
		self.duration[u'string'] = self.duration[u'string'].replace(u' ',u'0')
		
		return True
		
	
	def run(self):
		
		"""Runs through all analysis, and creates output files in the output
		directory
		"""

		# # # # #
		# NO DATA
		if self.fileisempty:
			# get the data file name
			dataname = os.path.basename(self.datadir)
			# create a new text file in the output
			outfile = open(os.path.join(self.outdir, u"empty.txt"), u"w")
			# write a message to this file
			outfile.write(u"File '%s' contains no data." % dataname)
			# close the text file
			outfile.close()
		
		
		# # # # #
		# DATA ANALYSIS
		else:

			# TARGETS
			# read the target coordinates for this task
			self.read_target_cors()
			# transform clicks to targets
			self.clicks_to_targets()
			
			# NEGLECT MEASURES
			# calculate the amount of omissions
			self.calc_omissions()
			# calculate centre of cancellation (x and y)
			self.calc_centre_of_cancellation()
			
			# DISORGANIZED SEARCH MEASURES
			# calculate the amount of perseverations
			self.calc_total_perseverations()
			self.calc_immediate_perseverations()
			self.calc_delayed_perseverations()
			# calculate the mean inter-cancellation (standardized) distance
			self.calc_mean_interdist()
			self.calc_stand_interdist()
			# calculate the mean inter-cancellation time and the search speed
			self.calc_mean_intertime()
			self.calc_search_speed()
			# calculate the Q score
			self.calc_qscore()
			# calculate the mean angle between cancellations
			self.calc_mean_angle()
			# calculate the standardized angle between cancellations
			self.calc_stand_angle()
			# calculate the best R
			self.calc_best_r()
			# calculate intersection rate
			self.calc_intersect_rate()
			
			
			# # # # #
			# OUTPUT FILES
			
			# text document with all values
			self.summary_txt()
			# cancellation path
			self.plot_cancellation_path()
			# heatmaps
			self.plot_heatmap(maptype=u'cancellation')
			self.plot_heatmap(maptype=u'omission')
			self.plot_heatmap(maptype=u'intersection')
			# cancellation heatmap superimposed over the task
			self.plot_superimposed_heatmap(maptype=u'cancellation')
			self.plot_superimposed_heatmap(maptype=u'omission')
			self.plot_superimposed_heatmap(maptype=u'intersection')
			# best R plots
			self.plot_best_r()
			# summary of everything in a PDF
			self.summary_pdf()
			# close all figures (in case Matplotlib was in interactive mode)
			pyplot.close(u'all')
	
	
	# # # # #
	# CALCULATORS
	
	# TARGETS AND TRANSFORMATIONS
	def read_target_cors(self):
		
		"""Reads all the target coordinates, and adds these to self.tarcors,
		which is a dict containing two keys: u'x' and u'y', both containing
		NumPy arrays of the x and y coordinates"""

		# READ DATAFILE
		# open the data file
		df = open(self.files[u'taskcors'], 'r')
		# read all lines
		raw = df.readlines()
		# clean up and split the lines
		for i in range(len(raw)):
			raw[i] = raw[i].replace(u'\n',u'').replace(u'\r',u'').replace(u'"',u'').split(u'\t')
		# extract the header
		header = raw.pop(0)

		# DATA EXTRACTION
		# empty lists to contain data points
		self.tarcors = {u'x':[],
					u'y':[],
					u'cors':[]}
		# extract data
		for i in range(len(raw)):
			self.tarcors[u'x'].append(raw[i][header.index(u'x')])
			self.tarcors[u'y'].append(raw[i][header.index(u'y')])
			self.tarcors[u'cors'].append((int(self.tarcors[u'x'][i]),int(self.tarcors[u'y'][i])))
		# lists to numpy arrays of integers
		self.tarcors[u'x'] = numpy.array(self.tarcors[u'x'], dtype=int)
		self.tarcors[u'y'] = numpy.array(self.tarcors[u'y'], dtype=int)
	
	def clicks_to_targets(self):
		
		"""Transforms original click coordinates to target coordinates for
		all clicks within the distance treshold from a target"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()

		# empty lists for click-target transformed (ct) coordinates
		self.ctx = []
		self.cty = []
		self.ctcors = []
		
		# match click positions to star positions
		for i in range(0,len(self.x)):
			# check Cartesian distance
			dist = (self.tarcors[u'x']-self.x[i])**2 + (self.tarcors[u'y']-self.y[i])**2
			# determine lowest value (=clicked target)
			clickcor = numpy.argmin(dist)
			if dist[clickcor]**0.5 < self.properties[u'disthreshold']:
					# add transformed click to lists
					self.ctx.append(self.tarcors[u'x'][clickcor])
					self.cty.append(self.tarcors[u'y'][clickcor])
					self.ctcors.append((self.ctx[-1],self.cty[-1]))

	
	# NEGLECT MEASURES
	
	def calc_omissions(self):
		
		"""Calculates the amount of omissions"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctcors'):
			self.clicks_to_targets()

		# loop through all target coordinates
		self.omissions = {	u'cors':[],
						u'x':numpy.zeros(len(self.tarcors[u'cors'])),
						u'y':numpy.zeros(len(self.tarcors[u'cors'])),
						u'total':0}
		for i in range(len(self.tarcors[u'cors'])):
			# if the target coordinate does not appear in the list of
			# clicked targets, it was not cancelled
			c = self.tarcors[u'cors'][i]
			if self.ctcors.count(c) < 1:
				self.omissions[u'x'][i] = c[0]
				self.omissions[u'y'][i] = c[1]
				self.omissions[u'cors'].append(c)
				self.omissions[u'total'] += 1
		# correct the length of the arrays
		self.omissions[u'x'] = self.omissions[u'x'][self.omissions[u'x']>0]
		self.omissions[u'y'] = self.omissions[u'y'][self.omissions[u'y']>0]
		# number of omissions per half
		self.omissions[u'left'] = len(self.omissions[u'x'][self.omissions[u'x']<self.dispsize[0]/2])
		self.omissions[u'right'] = len(self.omissions[u'x'][self.omissions[u'x']>self.dispsize[0]/2])
	
	def calc_centre_of_cancellation(self):
		
		"""Calculates the horizontal and vertical centres of cancellation"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()

		# the centre of cancellation is the mean of the cancelled targets'
		# x or y positions, normalized between -1* and 1** (right/bottom);
		# 0 means no bias towards either side
		# * -1 corresponds with the left or upmost target position
		# ** 1 corresponds with the right or bottommost target position
		fieldsize = [numpy.max(self.tarcors[u'x'])-numpy.min(self.tarcors[u'x']), numpy.max(self.tarcors[u'y'])-numpy.min(self.tarcors[u'y'])]
		self.coc = {}
		self.coc[u'x'] = (numpy.mean(numpy.unique(self.ctx)) - fieldsize[0]/2) / float(fieldsize[0]/2)
		self.coc[u'y'] = (numpy.mean(numpy.unique(self.cty)) - fieldsize[1]/2) / float(fieldsize[1]/2)
	
	
	# DISORGANIZED SEARCH MEASURES
	
	def calc_total_perseverations(self):
		
		"""Calculates the total amount of perseverations"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctcors'):
			self.clicks_to_targets()

		# loop through all target coordinates
		self.pers = {}
		self.pers[u'tot'] = 0
		for c in self.tarcors[u'cors']:
			# the total number of perseverations is the number of times a
			# target was clicked, minus one (for the first time the targer
			# was clicked)
			if self.ctcors.count(c) > 1:
				self.pers[u'tot'] += self.ctcors.count(c) - 1
	
	def calc_immediate_perseverations(self):
		
		"""Calculates the amount of immediate perseverations"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()

		# repetitions in the coordinates will result in a diff of 0;
		# numpy.where will give the index numbers of these coordinates;
		# these are the persevarations per individual axis
		px = numpy.where(numpy.diff(self.ctx)==0)[0]
		py = numpy.where(numpy.diff(self.cty)==0)[0]
		# numpy.intersect1d gives the sorted, unique values that are in both
		# index number arrays: the immediate perseverations on both axis
		imp = numpy.intersect1d(px, py)
		
		# save value
		self.pers[u'imm'] = len(imp)
	
	def calc_delayed_perseverations(self):
		
		"""Calculates the amount of delayed perseverations"""
		
		# calculate the total amount of perseverations and the amount of
		# immediate perseverations, if this has not been done yet
		if hasattr(self, u'pers'):
			if not u'tot' in self.pers.keys():
				self.calc_total_perseverations()
			if not u'imm' in self.pers.keys():
				self.calc_immediate_perseverations()
		else:
			self.calc_total_perseverations()
			self.calc_immediate_perseverations()

		# the number of delayed perseverations, is the total number of
		# perseverations minus the number of immediate perseverations
		self.pers[u'del'] = self.pers[u'tot'] - self.pers[u'imm']

	def calc_mean_interdist(self):
		
		"""Calculates the mean distance between cancellations"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()

		# empty array to contain interdistances
		self.intdist = {u'all':numpy.zeros(len(self.ctx)-1)}
		# calculate interdistances
		for i in range(len(self.intdist[u'all'])):
			self.intdist[u'all'][i] = ((self.ctx[i]-self.ctx[i+1])**2 + (self.cty[i]-self.cty[i+1])**2)**0.5
		# calculate mean interdistance (but only for distances greater than
		# 0, as an intdist of 0 reflects a perseveration)
		self.intdist[u'mean'] = numpy.mean(self.intdist[u'all'][self.intdist[u'all']>0])
	
	def calc_stand_interdist(self):
		
		"""Calculates the standardized interdistance"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate the mean interdistance, if this has not been done yet
		if hasattr(self,u'intdist'):
			if not u'mean' in self.intdist.keys():
				self.calc_mean_interdist()
		else:
			self.calc_mean_interdist()

		# calculate mean distance between closest targets
		self.intdist[u'alltar'] = numpy.zeros(len(self.tarcors[u'x']))
		# loop through all targets
		for i in range(len(self.tarcors[u'x'])):
			# calculate the distances between the current target and all
			# the other targets (one of these will result in a distance of
			# 0: the coordinate of the current target, so we do not look at
			# distances of 0)
			intdist = ((self.tarcors[u'x'] - self.tarcors[u'x'][i])**2 + (self.tarcors[u'y'] - self.tarcors[u'y'][i])**2)**0.5
			# get the distance to the closest neighbour
			self.intdist[u'alltar'][i] = numpy.min(intdist[intdist>0])
		# calculate the mean lowest target interdistance
		self.intdist[u'meantar'] = numpy.mean(self.intdist[u'alltar'])
		
		# calculate the standardized interdistance
		self.intdist[u'standardized'] = self.intdist[u'mean'] / self.intdist[u'meantar']

	def calc_mean_intertime(self):
		
		"""Calculates the mean time between cancellations"""
		
		# empty array to contain inter-cancellation times
		self.inttime = {u'all':numpy.zeros(len(self.time)-1)}
		# calculate inter-cancellation times
		for i in range(len(self.inttime[u'all'])):
			self.inttime[u'all'][i] = self.time[i+1] - self.time[i]
		# calculate mean inter-cancellation time
		self.inttime[u'mean'] = numpy.mean(self.inttime[u'all'])
	
	def calc_search_speed(self):
		
		"""Calculates the search speed: mean(distance / time)"""
		
		# calculate the average interdistance if this has not been done yet
		if not hasattr(self, u'intdist'):
			self.calc_mean_interdistance()
		# calculate the average intertime if this has not been done yet
		if not hasattr(self, u'inttime'):
			self.calc_mean_intertime()
		
		# calculate the mean search speed
		self.searchspd = numpy.average(self.intdist[u'mean'] / self.inttime[u'mean'])
	
	def calc_qscore(self):
		
		"""Calculates the Q score (Hills & Geldmacher, 1998)"""

		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate the amount of omissions if this has not been done yet
		if not hasattr(self, u'omissions'):
			self.calc_omissions()

		# calculate the Q score
		# (correct responses/total target) * (correct responses / total time)
		corresps = float(len(self.tarcors[u'cors']) - self.omissions[u'total'])
		self.qscore = (corresps / len(self.tarcors[u'cors'])) * (corresps / (self.duration[u'total']/1000))

	def calc_mean_angle(self):
		
		"""Calculates the mean angle between cancellations, where 0 means
		all cancellations are on a horizontal line, and 90 means all
		cancellations are on a vertical line"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()
		# calculate the interdistances if this has not been done yet
		if hasattr(self, u'intdist'):
			if not u'all' in self.intdist.keys():
				self.calc_mean_interdist()
		else:
			self.calc_mean_interdist()

		# empty array for all intercancellation angles
		self.angle = {u'all':numpy.zeros(len(self.ctx)-1)}
		
		# calculate the intercancellation angles
		for i in range(len(self.angle['all'])):
			# calculate the vertical distance
			ydist = float(abs(self.cty[i]-self.cty[i+1]))
			# check if there is an interdistance (otherwise it's a
			# perseveration, and those do not have an interangle)
			if self.intdist[u'all'][i] > 0:
				self.angle['all'][i] = math.degrees(math.asin(ydist/self.intdist['all'][i]))
			# invalid angles (perseverations) will be marked -1, and are
			# not used in further calculations
			else:
				self.angle['all'][i] = -1
		# calculate the mean intercancellation angle
		self.angle[u'mean'] = numpy.mean(self.angle['all'][self.angle['all']>=0])
	
	def calc_stand_angle(self):
		
		"""Calculates the standardized angle between cancellations, where a
		value of 1 means all cancellations where on a horizontal or vertical
		line (very organised), and 0 means all cancellations were diagonal
		(disorganised)"""
		
		# calculate all intercancellation angles, if this has not been done
		if hasattr(self, u'angle'):
			if not u'all' in self.angle.keys():
				self.calc_mean_angle()
		else:
			self.calc_mean_angle()
		
		# calculate the standardized angles (invalid angles will have a
		# value below 0, we do not take those into account
		self.angle['allstd'] = abs((2 * (self.angle['all'][self.angle['all']>=0]/90.0)) -1)
		# calculate the mean standardized angle
		self.angle[u'standardized'] = numpy.mean(self.angle['allstd'])

	def calc_best_r(self):
		
		"""Calculates the 'best r' value, based on Mark et al. (2004). The
		best r is the highest of the absolute values of the Pearson
		correlations between both the x and the y values and the
		cancellation number (the cancellation rank order)"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()

		# empty dict to contain values
		self.bestr = {}
		# correlations
		rank = numpy.arange(1,len(self.ctx)+1,1)
		self.bestr[u'x'] = pearsonr(rank, self.ctx)
		self.bestr[u'y'] = pearsonr(rank, self.cty)
		self.bestr[u'best'] = max([abs(self.bestr[u'x']),abs(self.bestr[u'y'])])
	
	def calc_intersect_rate(self):
		
		"""Calculates the amount of cancellation path intersections"""
				
		# empty dict to hold all intersection coordinates
		self.intersections = {u'x':[], u'y':[], u'cors':[]}
		
		# loop through all lines
		for i in range(len(self.ctcors)-1):
			# loop through all lines after this one (not before, as we do
			# not want to count any intersections double!)
			for j in range(i+1, len(self.ctcors)-1):
				# line starting and ending coordinates
				line1 = (self.ctcors[i],self.ctcors[i+1])
				line2 = (self.ctcors[j],self.ctcors[j+1])
				# find any intersections
				intersect = intersection(line1,line2)
				# if there is an intersection, add it to the list
				if intersect:
					self.intersections[u'x'].append(intersect[0])
					self.intersections[u'y'].append(intersect[1])
					self.intersections[u'cors'].append(intersect)
		
		# lists to arrays
		self.intersections[u'x'] = numpy.array(self.intersections[u'x'])
		self.intersections[u'y'] = numpy.array(self.intersections[u'y'])
		
		# count the amount and rate of intersections
		self.intersections[u'total'] = len(self.intersections[u'cors'])
		self.intersections[u'rate'] = self.intersections['total'] / float(len(self.ctcors) - self.pers[u'imm'])

	
	# # # # #
	# PLOTTERS
	
	def plot_cancellation_path(self):
		
		"""Plots all cancellations, showing a rank number for each
		cancellation, and a line going from point to point"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()

		# create new figure
		fig, ax = pyplot.subplots(nrows=1,ncols=1)
		fig.set_dpi(self.dpi)
		fig.set_size_inches((self.figsize[0]*0.65,self.figsize[1]*0.65), forward=True)
		#fig.set_size_inches(self.figsize, forward=True)
		ax.set_axis_off()
		# draw all targets (black dots)
		ax.plot(self.tarcors[u'x'], self.tarcors[u'y'], 'o', color=self.colours[u'aluminium'][5], markersize=5, label=u"targets")
		# draw all clicks (red crosses)
		ax.plot(self.x, self.y, 'x', color=self.colours[u'scarletred'][2], markersize=15, markeredgewidth=3, label=u"clicks")
		# draw all cancellations (green crosses)
		ax.plot(self.ctx, self.cty, 'x', color=self.colours[u'chameleon'][2], markersize=15, markeredgewidth=3, label=u"cancellations")
		# draw the cancellation path (blue line)
		ax.plot(self.ctx, self.cty, '-', color=self.colours[u'skyblue'][0], linewidth=3, label=u"cancelpath")
		# annotate the cancellation rank numbers
		for i in range(1,len(self.ctcors)+1):
			ax.annotate(unicode(i), (self.ctcors[i-1]), fontsize=24, fontproperties=self.fontprop)
		# add a legend
		ax.legend(loc=u'lower right')#, fontproperties=self.fontprop)
		# fix axis
		ax.axis([0,self.dispsize[0],0,self.dispsize[1]])
		ax.invert_yaxis()
		# title
		#ax.set_title(u"participant '%s', '%s' task (%s %s)" % (self.ppname,self.taskname,self.testdate,self.testtime), fontproperties=self.fontprop)
		# save the figure
		self.files[u'cancelpath'] = os.path.join(self.outdir, u'cancellation_path.png')
		fig.savefig(self.files[u'cancelpath'])
	
	def plot_heatmap(self, maptype=u'cancellation'):
		
		"""Plots a heatmap of the cancelled targets
		
		keyword arguments
		
		maptype		--	string indicating the type of heatmap to be
						produced; the options are:
							'cancellations' for a heatmap of the
								cancelled targets
							'omissions' for a heatmap of the omissions
							'intersections' for a heatmap of the
								intersections
		"""
		
		# read target coordinates if this has not been done yet
		if not hasattr(self, u'tarcors'):
			self.read_target_cors()
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctcors'):
			self.clicks_to_targets()
		
		# DETERMINE COORDINATES
		gauscors = []
		# coordinates for the cancellations
		if maptype == u'cancellation':
			# run through all targets
			for i in range(0,len(self.tarcors[u'x'])):
				# check if the target was cancelled
				if (self.tarcors[u'x'][i],self.tarcors[u'y'][i]) in self.ctcors:
					gauscors.append(self.tarcors[u'cors'][i])
		# coordinates for the omissions
		elif maptype == u'omission':
			gauscors = copy.deepcopy(self.omissions[u'cors'])
		# coordinates for the intersections
		elif maptype == u'intersection':
			gauscors = copy.deepcopy(self.intersections[u'cors'])
		# if the maptype was incorrectly specified, print message and return
		else:
			print(u"ValueError in libanalysis.plot_heatmap: maptype '%s' not recognized" % maptype)
			return

		# HEATMAP
		# Gaussian
		gwh = int(self.dispsize[0]/2)
		gsdwh = gwh/6
		gaus = gaussian(gwh,gsdwh)
		# matrix of zeroes
		strt = gwh/2
		heatmapsize = self.dispsize[1] + 2*strt, self.dispsize[0] + 2*strt
		heatmap = numpy.zeros(heatmapsize, dtype=float)
		# run through all targets
		for x, y in gauscors:
				# correct Gaussian size if either coordinate falls outside of
				# display boundaries
				if (not 0 < x < self.dispsize[0]) or (not 0 < y < self.dispsize[1]):
					hadj=[0,gwh];vadj=[0,gwh]
					if 0 > x:
						hadj[0] = abs(x)
						x = 0
					elif self.dispsize[0] < x:
						hadj[1] = gwh - int(x-self.dispsize[0])
					if 0 > y:
						vadj[0] = abs(y)
						y = 0
					elif self.dispsize[1] < y:
						vadj[1] = gwh - int(y-self.dispsize[1])
					# add adjusted Gaussian to the current heatmap
					heatmap[y:y+vadj[1],x:x+hadj[1]] += gaus[vadj[0]:vadj[1],hadj[0]:hadj[1]]
				else:				
					# add Gaussian to the current heatmap
					heatmap[y:y+gwh,x:x+gwh] += gaus
		# resize heatmap
		heatmap = heatmap[strt:self.dispsize[1]+strt,strt:self.dispsize[0]+strt]
		
		# HEATMAP IMAGE
		# create a new figure
		fig = pyplot.figure(figsize=self.figsize, dpi=self.dpi, frameon=False)
		ax = pyplot.Axes(fig, [0,0,1,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		# draw heatmap
		ax.imshow(heatmap, cmap=u'jet', alpha=1)
		# set the axis to the display size
		ax.axis([0,self.dispsize[0],0,self.dispsize[1]])
		# remove the axis grid
		ax.axis(u'off')
		# invert the y axis, as (0,0) is top left on a display
		ax.invert_yaxis()
		# save figure
		self.files[u'%sheatmap' % maptype] = os.path.join(self.outdir, u'%s_heatmap.png' % maptype)
		fig.savefig(self.files[u'%sheatmap' % maptype])

		# TRANSPARANT HEATMAP IMAGE
		# if there are no Gaussian coordinates, make whole map transparant
		if len(gauscors) == 0:
			heatmap[heatmap==0] = numpy.NaN
		# remove low values from heatmap
		else:
			lowestval = numpy.min(heatmap)
			lowbound = numpy.mean(heatmap[heatmap>0])
			heatmap[heatmap<=lowbound] = numpy.NaN
			# hidden pixel, to re-introduce lowest value (for colour scaling)
			heatmap[0][0] = lowestval
		# create a new figure
		fig = pyplot.figure(figsize=self.figsize, dpi=self.dpi, frameon=False)
		ax = pyplot.Axes(fig, [0,0,1,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		# draw heatmap
		ax.imshow(heatmap, cmap=u'jet', alpha=1)
		# set the axis to the display size
		ax.axis([0,self.dispsize[0],0,self.dispsize[1]])
		# remove the axis grid
		ax.axis(u'off')
		# invert the y axis, as (0,0) is top left on a display
		ax.invert_yaxis()
		# draw heatmap
		ax.imshow(heatmap, cmap=u'jet', alpha=1)
		# save figure
		self.files[u'%salphaheatmap' % maptype] = os.path.join(self.outdir, u'%s_heatmap_transparant.png'  % maptype)
		fig.savefig(self.files[u'%salphaheatmap' % maptype])
	
	def plot_superimposed_heatmap(self, maptype=u'cancellation'):
		
		"""Plots a heatmap superimposed on the task image"""

		# draw heatmap if this has not been done yet
		if not u'%salphaheatmap' % maptype in self.files.keys():
			self.plot_heatmap(maptype=maptype)

		# create a new figure
		fig = pyplot.figure(figsize=(self.dispsize[0]/self.dpi, self.dispsize[1]/self.dpi), dpi=self.dpi, frameon=False)
		ax = pyplot.Axes(fig, [0,0,1,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		# load images
		taskimg = image.imread(self.files[u'task'])
		heatmap = image.imread(self.files[u'%salphaheatmap' % maptype])
		# resize task image
		taskimg = numpy.resize(taskimg, (numpy.size(heatmap,axis=0),numpy.size(heatmap,axis=1)))
		# draw task
		ax.imshow(self.taskimg, origin=u'upper', alpha=1)
		# superimpose heatmap
		ax.imshow(heatmap, alpha=0.5)
		# save figure
		self.files[u'%staskheatmap' % maptype] = os.path.join(self.outdir, u'%s_heatmap_superimposed.png' % maptype)
		fig.savefig(self.files[u'%staskheatmap' % maptype])
	
	def plot_best_r(self):
		
		"""Plots the correlations between cancellation rank number and
		cancellation x and y coordinates"""
		
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'ctx'):
			self.clicks_to_targets()
		# calculate click transformed coordinates if this has not been done
		if not hasattr(self, u'bestr'):
			self.calc_best_r()

		# create new figure
		fig, (ax1,ax2) = pyplot.subplots(nrows=2,ncols=1, sharex=True)
		fig.set_dpi(self.dpi)
		fig.set_size_inches(self.figsize, forward=True)
		# plot
		rank = numpy.arange(1,len(self.ctx)+1,1)
		ax1.plot(rank, self.ctx, '-', color=self.colours[u'chameleon'][2], label=u"R=%1.2f" % self.bestr[u'x'])
		ax2.plot(rank, self.cty, '-', color=self.colours[u'plum'][2], label=u"R=%1.2f" % self.bestr[u'y'])
		# finish plot
		ax1.legend(loc=u'best')#, fontproperties=self.fontprop)
		ax2.legend(loc=u'best')#, fontproperties=self.fontprop)
		ax1.set_ylabel(u"horizontal position (pixels)", fontproperties=self.fontprop)
		ax2.set_ylabel(u"vertical position (pixels)", fontproperties=self.fontprop)
		ax2.set_xlabel(u"cancellation rank number", fontproperties=self.fontprop)
		fig.suptitle(u"best R: %1.2f (participant '%s', task '%s')" % (self.bestr[u'best'],self.ppname,self.taskname), fontproperties=self.fontprop)
		# save figure
		self.files[u'bestr'] = os.path.join(self.outdir, u'best_r_plots.png')
		fig.savefig(self.files[u'bestr'])
	
	
	# SUMMARIES
	
	def summary_txt(self):
		
		"""Creates a simple text file, containing all the measures"""
		
		# open a new textfile
		self.files[u'txt'] = os.path.join(self.outdir, u'summary.txt')
		txtfile = open(self.files[u'txt'], 'w')
		
		# write the header to the file
		header = [u'om_tot',u'om_left',u'om_right', \
				u'pers_tot',u'pers_imm', u'pers_del', \
				u'CoC_hor',u'CoC_ver', \
				u'duration',u'mean_intertime', u'Qscore', \
				u'mean_interdist', u'stand_interdist',u'speed', \
				u'mean_angle',u'stand_angle', \
				u'bestR',u'hor_R',u'ver_R', \
				u'intersect_tot',u'intersect_rate']
		txtfile.write(u"\t".join(header))
		txtfile.write(u"\n")
		
		# write the output to the file
		output = [self.omissions[u'total'],self.omissions[u'left'],self.omissions[u'right'], \
				self.pers[u'tot'],self.pers[u'imm'],self.pers[u'del'], \
				self.coc[u'x'],self.coc[u'y'], \
				self.duration['total']/1000, self.inttime[u'mean']/1000.0, self.qscore, \
				self.intdist[u'mean'], self.intdist[u'standardized'], self.searchspd, \
				self.angle[u'standardized'], self.angle[u'standardized'], \
				self.bestr[u'best'], self.bestr[u'x'], self.bestr[u'y'], \
				self.intersections[u'total'], self.intersections[u'rate']
				]
		output = map(unicode, output)
		txtfile.write(u"\t".join(output))
		
		# close the textfile
		txtfile.close()
	
	def summary_pdf(self):
		
		"""Creates an A4-sized PDF, showing the important plots and all
		calculated measures"""
		
		# A4 dimensions (landscape):
		# 11.69x8.27 inches, 300 dpi (results in 3507x2481 px)
		# 11.69x8.27 inches, 600 dpi (results in 7014x4962 px)
		
		# CHECKS
		# check if the omissions have been calculated
		if not hasattr(self, u'omissions'):
			self.calc_omissions()
		# check if the centre of cancellation has been calculated
		if not hasattr(self, u'coc'):
			self.calc_centre_of_cancellation()
		# check if the omissions have been calculated
		if hasattr(self, u'pers'):
			if u'tot' not in self.pers.keys():
				self.calc_total_perseverations()
			if u'imm' not in self.pers.keys():
				self.calc_immediate_perseverations()
			if u'del' not in self.pers.keys():
				self.calc_delayed_perseverations()
		else:
			self.calc_total_perseverations()
			self.calc_immediate_perseverations()
			self.calc_delayed_perseverations()
		# check if the standardized interdistance has been calculated
		if hasattr(self, u'intdist'):
			if not u'standardized' in self.intdist.keys():
				self.calc_stand_interdist()
		else:
			self.calc_stand_interdist()
		# check if the intertime has been calculated
		if not hasattr(self, u'inttime'):
			self.calc_mean_intertime()
		# check if the search speed has been calculated
		if not hasattr(self, u'searchspd'):
			self.calc_search_speed()
		# check if the Q score has been calculated
		if not hasattr(self, u'qscore'):
			self.calc_qscore()
		# check if the standardized angle has been calculated
		if hasattr(self, u'angle'):
			if not u'standardized' in self.angle.keys():
				self.calc_stand_angle()
		else:
			self.calc_stand_angle()
		# check if the best R has been calculated
		if not hasattr(self, u'bestr'):
			self.calc_best_r()
		# check if the intersection rate has been calculated
		if not hasattr(self, u'intersections'):
			self.calc_intersect_rate()
		# check if the cancellation path has been plotted
		if not u'cancelpath' in self.files.keys():
			self.plot_cancellation_path()
		# check if the heatmap has been plotted
		if not u'cancellationtaskheatmap' in self.files.keys():
			self.plot_superimposed_heatmap(maptype=u'cancellation')

		# PLOTTING
		# create a new figure
		pdf = pyplot.figure(figsize=self.pdfsize, dpi=self.dpi*6, frameon=False)
		# draw the images
		imgnames = [u'cancelpath',u'cancellationtaskheatmap']
		axtitles = [u'cancellation path',u'cancellation heatmap',u'analysis output']
		bottoms = [0.35, 0.03, 0.7]
		for i in range(len(imgnames)):
			# add new axis (rect is [left,bottom,width,height])
			ax = pyplot.Axes(pdf, [0,bottoms[i],1,0.3])
			ax.set_axis_off()
			pdf.add_axes(ax)
			# load and draw the image
			img = image.imread(self.files[imgnames[i]])
			ax.imshow(img)	
			# add title
			ax.set_title(axtitles[i], fontproperties=self.fontprop)
		# add axis for text
		ax = pyplot.Axes(pdf, [0,bottoms[-1],1,0.25])
		ax.set_axis_off()
		pdf.add_axes(ax)
		ax.set_title(axtitles[-1], fontproperties=self.fontprop)
		# texts (two columns in two lists)
		texts = [[u" ",
				u"created using CancellationTools (version %s)" % self.version,
				u"<url>www.pygaze.org/cancellation",
				u"<b>participant: %s" % self.ppname,
				u"task: %s (%s, %s)" % (self.taskname,self.testdate,self.testtime),
				u"<b>neglect measures",
				u"omissions: %d (left: %d, right: %d)" % (self.omissions[u'total'],self.omissions[u'left'],self.omissions[u'right']),
				u"centre of cancellation: %1.2f (vertical: %1.2f)" % (self.coc[u'x'],self.coc[u'y']),
				u"<b>perseverations",
				u"immediate:	%d" % self.pers[u'imm'],
				u"delayed:	%d" % self.pers[u'del']],

			[	u" ",
				u"<b>timing",
				u"duration: %s" % (self.duration['string']),
				u"average inter-cancellation time: %.2f s" % (self.inttime[u'mean']/1000.0),
				u"search speed: %.2f cancellations per second" % (self.searchspd),
				u"Q score: %.2f" % (self.qscore),
				u"<b>path measures",
				u"distance; mean: %d px, standardized: %d" % (self.intdist[u'mean'],self.intdist[u'standardized']),
				u"standardized angle: %1.2f" % self.angle[u'standardized'],
				u"best R: %1.2f" % self.bestr[u'best'],
				u"intersections rate: %.2f (total: %d)" % (self.intersections[u'rate'],self.intersections[u'total'])]
				]
		# draw texts
		for c in range(len(texts)):
			for r in range(len(texts[c])):
				if u"<b>" in texts[c][r]:
					ax.text(0.1+0.5*c, 1-(0.1*r), texts[c][r].replace(u"<b>",u""), fontsize=10, fontproperties=self.boldfontprop)
				elif u"<url>" in texts[c][r]:
					ax.text(0.1+0.5*c, 1-(0.1*r), texts[c][r].replace(u"<url>",u""), color=self.colours[u'skyblue'][2], fontsize=10, fontproperties=self.fontprop)
				else:
					ax.text(0.1+0.5*c, 1-(0.1*r), texts[c][r], fontsize=10, fontproperties=self.fontprop)
		# save PDF
		self.files[u'pdf'] = os.path.join(self.outdir, u'summary.pdf')
		pdf.savefig(self.files[u'pdf'])

# -*- coding: utf-8 -*-
"""Example Google style docstrings.
"""
import numpy as np
import networkx as nx
import time

STATE_CONSTANTS ={
	0: {'stateIncreaseProb': 0.20,	'stateDecreaseProb': 0, 	'fireStartProb': 0.000,	'fireSpreadProb': 0.000},
	1: {'stateIncreaseProb': 0.10,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.0005,	'fireSpreadProb': 0.100},
	2: {'stateIncreaseProb': 0.15,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.0005,	'fireSpreadProb': 0.200},
	3: {'stateIncreaseProb': 0.10,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.0005,	'fireSpreadProb': 0.300},
	4: {'stateIncreaseProb': 0.10,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.0005,	'fireSpreadProb': 0.450},
	5: {'stateIncreaseProb': 0.00,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.0005,	'fireSpreadProb': 0.700},
	-1:{'stateIncreaseProb': 1.00,	'stateDecreaseProb': 0.00, 	'fireStartProb': 0.000,	'fireSpreadProb': 0.000}
	}

COLOR_KEY = {
	0: '\033[1;30;48;5;246m0\033[0;39m',
	1: '\033[1;30;48;5;190m1\033[0;39m',
	2: '\033[1;30;48;5;118m2\033[0;39m',
	3: '\033[1;30;48;5;46m3\033[0;39m',
	4: '\033[1;30;48;5;34m4\033[0;39m',
	5: '\033[1;30;48;5;2m5\033[0;39m',
	-1:'f'
}


class MXRegion(object):
	def __init__(self, xdim=10, ydim=10, grid_type='2d', colorize=True):
		self.xdim = xdim
		self.ydim = ydim
		self.grid_type = grid_type
		if grid_type == '2d':
			self.space = nx.grid_2d_graph(xdim, ydim)
		elif grid_type == 'hex':
			self.space = nx.hexagonal_lattice_graph(xdim, ydim)
		elif grid_type == 'tri':
			self.space = nx.triangular_lattice_graph(xdim, ydim)
		else:
			# TODO: raise exception? default to 2d?
			self.space = nx.grid_2d_graph(xdim, ydim)
		for node in self.space.nodes:
			self.space.node[node]['locale'] = Locale()
		self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
		self.time = 0
		self.colorize = colorize

	def __repr__(self, verbose=False):
		if verbose==False or self.grid_type != '2d':
			return f'NXRegion {self.xdim}x{self.ydim}'
		else: 
			out=''
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.view_locale())
				out += '\n'
			return out

	def __str__(self, verbose=False):
		if verbose==False or self.grid_type != '2d':
			return f'NXRegion {self.xdim}x{self.ydim}'
		else: 
			out = ''
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.view_locale())
				out += '\n'
			return out

	def show_map(self, do_print=True):
		if self.grid_type == '2d':
			out=''
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.view_locale(x, y))
				out += '\n'
			out += '\r'
			if do_print:
				print(out)
			else: 
				return out
		else:
			print('!!! This grid type does not have this feature implemented !!!')

	def show_fire_map(self, do_print=True):
		"""Display a visual representation of the self.space attribute with fire state layered on if do_print.

		Args:
			do_print:

		Returns:
			str:

		"""
		if self.grid_type == '2d':
			out = ''
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.view_locale(x, y, fire_state=True))
				out += '\n'
			if do_print:
				print(out)
			else: 
				return out
		else:
			print('!!! This grid type does not have this feature implemented !!!')

	def pass_time(self, count=1):
		"""Move forward one time (or count # of) step(s).

		Args:
			count:
		"""
		for _ in range(count):
			self.time+=1
			for node in self.space.nodes:
				self.space.node[node]['locale'].pass_time()
			self.spread_fire()

	def show_turns(self, count=1, pause=0.5):
		"""show_turns

		Args:
			count:
			pause:
		"""
		for _ in range(count):
			self.pass_time()
			self.show_map()
			time.sleep(pause)

	def spread_fire(self, slow_burn=False):
		"""Scan locales for fire, and if present, cause fire to spread to neighboring regions.

		Args:
			slow_burn:
		"""
		locales_on_fire = []
		locales_to_burn = {}
		fires_present = False
		for node in self.space.nodes:
			if self.space.node[node]['locale'].onFire == 1: 
				locales_on_fire.append(node)
		if locales_on_fire: fires_present = True
		for locale_ in locales_on_fire:
			neighboring_nodes = self.space.neighbors(locale_)
			for node in neighboring_nodes:
				if self.space.node[node]['locale'].onFire==0:
					if self.space.node[node]['locale'].catch_fire():
						locales_on_fire.append(node)
						if slow_burn == True:
							self.show_map()
							time.sleep(0.15)
		if fires_present:
			self.show_map()
			time.sleep(0.5)

	def view_locale(self, x, y, fire_state=False):
		if fire_state:
			return self.space.node[(x, y)]['locale'].onFire
		else:
			return self.space.node[(x, y)]['locale']


class Region():
	def __init__(self, xdim=10, ydim=10):
		self.xdim = xdim
		self.ydim = ydim
		self.space = [[Locale() for x in range(self.xdim)] for y in range(self.ydim)]
		self.conversion_rates = {0:0.2, 1:0.1, 2:0.15, 3: 0.05, 4:0.1, 5:0}
		self.time = 0

	def __repr__(self):
		out = ''
		for line in self.space:
			for item in line:
				out += str(item)
			out += '\n'
		return out

	def __str__(self):
		out = ''
		for line in self.space:
			for item in line:
				out += str(item)
			out += '\n'
		return out

	def show_fire_map(self, do_print=True):
		out = ''
		for line in self.space:
			for item in line:
				out += str(item.on_fire)
			out += '\n'
		if do_print: print(out)
		else: return out

	def pass_time(self, count = 1):
		for _ in range(count):
			self.time += 1
			for line in self.space:
				for each_locale in line:
					each_locale.pass_time()
			self.spread_fire()

	def spread_fire(self):
		locales_on_fire = []
		locales_to_burn = {}
		for x in range(self.xdim):
			for y in range(self.ydim):
				if self.space[x][y].on_fire == 1:
					locales_on_fire.append([x,y])

		for locale_ in locales_on_fire:
			if locale_[0]-1 >= 0 and self.space[locale_[0]-1][locale_[1]].on_fire == 0:
				if self.space[locale_[0]-1][locale_[1]].catch_fire():
					locales_on_fire.append([locale_[0]-1, locale_[1]])
			if locale_[0]+1 < self.xdim and self.space[locale_[0]+1][locale_[1]].on_fire == 0:
				if self.space[locale_[0]+1][locale_[1]].catch_fire():
					locales_on_fire.append([locale_[0]+1, locale_[1]])
			if locale_[1]-1 >= 0 and self.space[locale_[0]][locale_[1]-1].on_fire == 0:
				if self.space[locale_[0]][locale_[1]-1].catch_fire():
					locales_on_fire.append([locale_[0], locale_[1]-1])
			if locale_[1]+1 < self.ydim and self.space[locale_[0]][locale_[1]+1].on_fire == 0:
				if self.space[locale_[0]][locale_[1]+1].catch_fire():
					locales_on_fire.append([locale_[0]-1, locale_[1]+1])


class Locale(object):
	def __init__(self):
		self.state = 0
		self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
		self.on_fire = 0

	def __str__(self):
		if self.on_fire == 0:
			return COLOR_KEY[self.state]
		elif self.on_fire == 1:
			return '\033[1;31mf\033[0;37m'

	def __repr__(self):
		return str(self.state)

	def pass_time(self):
		if self.on_fire == 1:
			self.burn()
		self.increment_state()
		self.risk_fire()

	def increment_state(self):
		roll = np.random.uniform(0, 1)
		if roll < STATE_CONSTANTS[self.state]['stateIncreaseProb']:
			self.state += 1
			return True
		elif roll > 1 - STATE_CONSTANTS[self.state]['stateDecreaseProb']:
			self.state -= 1
			return True
		return False

	def risk_fire(self):
		roll = np.random.uniform(0, 1)
		if roll < STATE_CONSTANTS[self.state]['fireStartProb']:
			self.on_fire = 1
			return True
		return False

	def catch_fire(self):
		roll = np.random.uniform(0, 1)
		if roll < STATE_CONSTANTS[self.state]['fireSpreadProb']:
			self.on_fire = 1
			return True
		return False

	def burn(self):
		self.state = -1
		self.on_fire = 0


class Species(object):
	pass


class ABiotics(object):
	"""docstring for ClassName"""
	def __init__(self, soil=1.0, bedrock=1.0, moisture=1.0, nutrients=1.0):
		super(ABiotics, self).__init__()
		self.soil=soil
		self.bedrock=bedrock
		self.moisture=moisture
		self.nutrients=nutrients
	


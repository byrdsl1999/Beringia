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

class nxregion():
	def __init__(self, xdim=10, ydim=10, gridType='2d', colorize=True):
		self.xdim = xdim
		self.ydim = ydim
		self.gridType = gridType
		if gridType =='2d':
			self.space = nx.grid_2d_graph(xdim, ydim)
		elif gridType == 'hex':
			self.space = nx.hexagonal_lattice_graph(xdim, ydim)
		elif gridType == 'tri':
			self.space = nx.triangular_lattice_graph(xdim, ydim)
		else:
			#raise exception? default to 2d?
			self.space = nx.grid_2d_graph(xdim, ydim)
		for node in self.space.nodes:
			self.space.node[node]['locale']=locale()
		self.conversion_rates = {0:0.2, 1:0.1, 2:0.15, 3: 0.05, 4:0.1, 5:0}
		self.time = 0
		self.colorize=colorize

	def __repr__(self, verbose=False):
		if verbose==False or self.gridType != '2d':
			return('nxregion '+str(self.xdim)+'x'+str(self.ydim))
		else: 
			out=""
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.viewLocale())
				out +="\n"
			return out


	def __str__(self, verbose=False):
		if verbose==False or self.gridType != '2d':
			return('nxregion '+str(self.xdim)+'x'+str(self.ydim))
		else: 
			out=""
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.viewLocale())
				out +="\n"
			return out

	def showMap(self, doPrint=True):
		if self.gridType == '2d':
			out=""
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.viewLocale(x,y))
				out +="\n"
			out +="\r"
			if doPrint:
				print(out)
			else: 
				return(out)
		else:
			print('!!! This grid type does not have this feature implemented !!!')


	def showFireMap(self, doPrint=True):
		'''
		Display a visual representation of the self.space attribute 
		with fire state layered on if doPrint.
		'''
		if self.gridType == '2d':
			out=""
			for x in range(self.xdim):
				for y in range(self.ydim):
					out += str(self.viewLocale(x,y, fireState=True))
				out +="\n"
			if doPrint:
				print(out)
			else: 
				return(out)
		else:
			print('!!! This grid type does not have this feature implemented !!!')


	def passTime(self, count = 1):
		'''
		Move forward one time(or count # of) step(s).
		'''

		for _ in range(count):
			self.time+=1
			for node in self.space.nodes:
				self.space.node[node]['locale'].passTime()
			self.spreadFire()

	def showTurns(self, count= 1, pause=0.5):
		for _ in range(count):
			self.passTime()
			self.showMap()
			time.sleep(pause)

	def spreadFire(self, slowBurn=False):
		'''
		Scan locales for fire, and if present, cause fire to spread to 
		neighboring regions.
		'''
		localesOnFire = []
		localesToBurn = {}
		firesPresent = False
		for node in self.space.nodes:
			if self.space.node[node]['locale'].onFire == 1: 
				localesOnFire.append(node)
		if localesOnFire: firesPresent = True
		for locale_ in localesOnFire:
			neighboringNodes = self.space.neighbors(locale_)
			for node in neighboringNodes:
				if self.space.node[node]['locale'].onFire==0:
					if self.space.node[node]['locale'].catchFire():
						localesOnFire.append(node)
						if slowBurn==True: 
							self.showMap()
							time.sleep(0.15)
		if firesPresent: 
			self.showMap()
			time.sleep(0.5)

	def viewLocale(self, x, y, fireState=False):
		if fireState == False:
			return self.space.node[(x,y)]['locale']
		elif fireState == True:
			return self.space.node[(x,y)]['locale'].onFire




class region():
	
	def __init__(self, xdim=10, ydim=10):
		self.xdim = xdim
		self.ydim = ydim
		self.space = [[locale() for x in range(self.xdim)] for y in range(self.ydim)]
		self.conversion_rates = {0:0.2, 1:0.1, 2:0.15, 3: 0.05, 4:0.1, 5:0}
		self.time = 0

	def __repr__(self):
		out=""
		for line in self.space:
			for item in line:
				out += str(item)
			out +="\n"
		return out

	def __str__(self):
		out=""
		for line in self.space:
			for item in line:
				out += str(item)
			out +="\n"
		return out

	def showFireMap(self, doPrint=True):
		out=""
		for line in self.space:
			for item in line:
				out += str(item.onFire)
			out +="\n"
		if doPrint: print(out)
		else: return out

	def passTime(self, count = 1):
		for _ in range(count):
			self.time+=1
			for line in self.space:
				for eachLocale in line:
					eachLocale.passTime()
			self.spreadFire()


	def spreadFire(self):
		localesOnFire = []
		localesToBurn = {}
		for x in range(self.xdim):
			for y in range(self.ydim):
				if self.space[x][y].onFire == 1:
					localesOnFire.append([x,y])

		for locale_ in localesOnFire:
			if locale_[0]-1 >= 0 and self.space[locale_[0]-1][locale_[1]].onFire==0:
				if self.space[locale_[0]-1][locale_[1]].catchFire():
					localesOnFire.append([locale_[0]-1, locale_[1]])
			if locale_[0]+1 < self.xdim and self.space[locale_[0]+1][locale_[1]].onFire==0:
				if self.space[locale_[0]+1][locale_[1]].catchFire():
					localesOnFire.append([locale_[0]+1, locale_[1]])
			if locale_[1]-1 >= 0 and self.space[locale_[0]][locale_[1]-1].onFire==0:
				if self.space[locale_[0]][locale_[1]-1].catchFire():
					localesOnFire.append([locale_[0], locale_[1]-1])
			if locale_[1]+1 < self.ydim and self.space[locale_[0]][locale_[1]+1].onFire==0:
				if self.space[locale_[0]][locale_[1]+1].catchFire():
					localesOnFire.append([locale_[0]-1, locale_[1]+1])



class locale():
	def __init__(self):
		self.state = 0
		self.conversion_rates = {0:0.2, 1:0.1, 2:0.15, 3: 0.05, 4:0.1, 5:0}
		self.onFire=0

	def __str__(self):
		if self.onFire==0:
			#return (str(self.state))
			return (COLOR_KEY[self.state])
		elif self.onFire==1:
			return ("\033[1;31mf\033[0;37m")

	def __repr__(self):
		return(str(self.state))

	def passTime(self):
		if self.onFire == 1:
			self.burn()
		self.incrementState()
		self.riskFire()

	def incrementState(self):
		roll = np.random.uniform(0,1)
		if roll < STATE_CONSTANTS[self.state]['stateIncreaseProb']:
			self.state += 1
			return True
		elif roll > 1-STATE_CONSTANTS[self.state]['stateDecreaseProb']:
			self.state -= 1
			return True
		return False

	def riskFire(self):
		roll = np.random.uniform(0,1)
		if roll < STATE_CONSTANTS[self.state]['fireStartProb']:
			self.onFire = 1
			return True
		return False

	def catchFire(self):
		roll = np.random.uniform(0,1)
		if roll < STATE_CONSTANTS[self.state]['fireSpreadProb']:
			self.onFire = 1
			return True
		return False

	def burn(self):
		self.state = -1
		self.onFire =0


class feature(object):
	"""This is a generic class that defines features of locale."""
	def __init__(self, location=None):
		self.location=location

	def hasLocation(self):
		if self.locale == None:
			return False
		else:
			return True

	def deleteSelf(self):
		del self

class flora(feature):
	"""Flora is housed within a locale, and keeps track of which species are present and in what quantities."""
	def __init__(self):
		super(feature, self).__init__()


class species(): 
	pass


class fauna(feature):
	"""docstring for ClassName"""
	def __init__(self):
		super(feature, self).__init__()

		
class abiotics(object):
	"""docstring for ClassName"""
	def __init__(self, soil=1.0, bedrock=1.0, moisture=1.0, nutrients=1.0):
		super(ClassName, self).__init__()
		self.soil=soil
		self.bedrock=bedrock
		self.moisture=moisture
		self.nutrients=nutrients
	


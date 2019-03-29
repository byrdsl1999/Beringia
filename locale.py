import numpy as np
import networkx as nx
import time
from soil import geology

FEATURES_SWITCH={
	'geology': True
}

class locale():
	'''A locale is conceptually a small region which contains a number of biotic and abiotic
	features which simulate a local ecosystem. It has been conceived of initally as a patch 
	of land about 1 acre in size.'''
	def __init__(self):
		self.state = 0
		self.conversion_rates = {0:0.2, 1:0.1, 2:0.15, 3: 0.05, 4:0.1, 5:0}
		self.onFire=0

		if FEATURES_SWITCH['geology']: 
			self.geology = geology()

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
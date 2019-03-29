from math import e, pi, sqrt
from scipy import stats

class plant_bulk():
	def __init__(self, population=0.01, growth_rate=0.01, feeding_rate=0.5):
		self.population=population
		self.max_pop=1.0
		self.growth_rate=growth_rate  
		self.moisture_preference=0.7
		self.moisture_tolerance=0.2
		self.moisture_function=None
		self.nutrient_preference=None
		self.nutrient_tolerance=


	def grow(self, environment=None):
		'''
		This invocation of this function will cause the population to increment by 
		one step.

		maths: Ecological growth should follow a logistic growth function. The 
		slope of which is defined by the equation:
		dP/dt=rP(1-P/K)
		where P = Population, r = growth rate, and K = carrying capacity.
		'''
		self.population += self.growth_rate * self.population * (1-self.population/self.max_pop)

	def calc_max_pop(self, environment):
		if not environment: environment = 1.0

		self.max_pop = self.moisture_function.pdf(environment)

	def _calc_tolerance_functions(self):
		self.moisture_function = stats.norm(self.moisture_preference, self.moisture_tolerance)


	def _sufficient_nutrients(self, environment=None):
		if environment:
			return (False)
		else: 
			return (True)

	def _sufficient_moisture(self, environment=None):
		if environment:
			return (False)
		else:
			return (True)

class mosses(plant_bulk):
	pass

class grasses(plant_bulk):
	pass

class perennials(plant_bulk):
	pass

class shrubs(plant_bulk):
	pass

class soft_woods(plant_bulk):
	pass

class hard_woods(plant_bulk):
	pass
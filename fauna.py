#import feature

class fauna(feature):
	"""docstring for fauna"""
	def __init__(self, arg):
		super(fauna, self).__init__()
		self.arg = arg


class animal_bulk(fauna):
	"""docstring for animal_bulk"""
	def __init__(self, population=0.0, reproduction_rate=0.01, starvation_rate=0.02, feeding_rate=0.5):
		self.population=population
		self.reproduction_rate=reproduction_rate  #This is essentially the energy conversion rate.(eg 10 lb grass makes 1 lb beef)
		self.starvation_rate= starvation_rate
		self.feeding_rate=feeding_rate
		self.ambient_death_rate=0.05

	def _zero_correct_pop(self):
		if self.population <=0: 
			self.population=0.0

	def feed(self, target=None):
		# TODO Be able to feed on multiple prey, and select prey. Either at random, in order of prevalence, or order of ease of finding.
		consumption = self.population * self.feeding_rate
		if issubclass(type(target), animal_bulk):
			food = target.population
			target.population -= consumption
			target._zero_correct_pop()
		#elif: pass #TODO is type plant
		#elif: pass #TODO is type individual animal
		else: food = 1.0

		if consumption < food:
			self._breed()
			return consumption
		elif consumption >= food:
			self._starve()
			return food

	def _breed(self):
		#TODO look up population growth rate functions.
		self.population += self.population*self.reproduction_rate

	def _starve(self):
		self.population -= self.population*self.starvation_rate + self.starvation_rate
		self._zero_correct_pop()

	def _ambient_death(self):
		self.population = self.population * (1-self.ambient_death_rate)
		self._zero_correct_pop()

	def depredation(self, predation_rate):
		pass

	def migrate(self):
		pass

	def passTime(self, target=1.0):
		self.feed(target)
		self._ambient_death()



class invertebrates(animal_bulk):
	def __init__(self, population=0.0, reproduction_rate=0.01, starvation_rate=0.25, feeding_rate=0.25, fallout_rate=0.001):
		animal_bulk.__init__(self, population, reproduction_rate, starvation_rate, feeding_rate)
		self.fallout_rate=fallout_rate

	def fallout(self):
		self.population += self.fallout_rate

	def passTime(self, food=1.0):
		self.fallout()
		self.feed(food)
		self._zero_correct_pop()
		self._ambient_death()

class invert_detritivores(invertebrates):
	def __init__(self, feeding_rate=0.01):
		invertebrates.__init__(self, feeding_rate)

class invert_herbivores(invertebrates):
	def __init__(self, feeding_rate=0.01):
		invertebrates.__init__(self, feeding_rate)

class invert_predators(invertebrates):
	def __init__(self, feeding_rate=0.15, fallout_rate=0.0001):
		invertebrates.__init__(self, feeding_rate=feeding_rate, fallout_rate=fallout_rate)



class vertebrates(animal_bulk):
	def __init__(self, population=0.0, reproduction_rate=0.01):
		animal_bulk.__init__(self, population, reproduction_rate)
		self.population = population
		self.reproduction_rate = reproduction_rate
		self.starvation_rate = 0.1		

class insectivore(vertebrates):
	def __init(self, feeding_rate=0.1):
		vertebrates.__init__(self, feeding_rate=feeding_rate)


class small_herbivore(vertebrates):
	def __init(self, feeding_rate=0.1):
		self.feeding_rate = feeding_rate

class large_herbivore(vertebrates):
	def __init(self, feeding_rate=0.2):
		self.feeding_rate = feeding_rate

class small_predator(vertebrates):
	def __init(self, feeding_rate=0.2):
		self.feeding_rate = feeding_rate
		
class large_predator(vertebrates):
	def __init(self, feeding_rate=0.3):
		self.feeding_rate = feeding_rate

class medium_omnivore(vertebrates):
	def __init(self, feeding_rate=0.25):
		self.feeding_rate = feeding_rate
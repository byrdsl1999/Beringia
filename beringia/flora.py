# -*- coding: utf-8 -*-
"""flora.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""
from scipy import stats

from beringia.feature import Feature


class Flora(Feature):
    """Flora is housed within a locale, and keeps track of which species are present and in what quantities."""
    def __init__(self):
        super(Feature, self).__init__()


class PlantBulk(Flora):
    def __init__(self, population=0.01, growth_rate=0.01, feeding_rate=0.5):
        super(PlantBulk, self).__init__()
        self.population = population
        self.max_pop = 1.0
        self.growth_rate = growth_rate
        self.moisture_preference = 0.7
        self.moisture_tolerance = 0.2
        self.moisture_function = None
        self.nutrient_preference = None
        self.nutrient_tolerance = None

    def grow(self, environment=None):
        """This invocation of this function will cause the population to increment by one step.

        maths: Ecological growth should follow a logistic growth function. The slope of which is defined by the
        equation:
            dP/dt=rP(1-P/K)
        where P = Population, r = growth rate, and K = carrying capacity.

        Args:
            environment:
        """
        self.population += self.growth_rate * self.population * (1-self.population/self.max_pop)

    def calc_max_pop(self, environment):
        if not environment:
            environment = 1.0

        self.max_pop = self.moisture_function.pdf(environment)

    def _calc_tolerance_functions(self):
        self.moisture_function = stats.norm(self.moisture_preference, self.moisture_tolerance)

    @classmethod
    def _sufficient_nutrients(cls, environment=None):
        if environment:
            return False
        else:
            return True

    @classmethod
    def _sufficient_moisture(cls, environment=None):
        if environment:
            return False
        else:
            return True


class Mosses(PlantBulk):
    pass


class Grasses(PlantBulk):
    pass


class Perennials(PlantBulk):
    pass


class Shrubs(PlantBulk):
    pass


class SoftWoods(PlantBulk):
    pass


class HardWoods(PlantBulk):
    pass

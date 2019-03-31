# -*- coding: utf-8 -*-
"""flora.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
from scipy import stats

from beringia.feature import Feature


class Flora(Feature):
    def __init__(self):
        """Flora is housed within a locale, and keeps track of which species are present and in what quantities.

        """
        super(Feature, self).__init__()


class PlantBulk(Flora):
    def __init__(self, population=0.01, growth_rate=0.01, feeding_rate=0.5):
        """PlantBulk class docs

        Args:
            population (float):
            growth_rate (float):
            feeding_rate (float):

        """
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

        maths:
            Ecological growth should follow a logistic growth function. The slope of which is defined by the equation:
                dP/dt = r * P * (1 - P/K)
            where P = Population, r = growth rate, and K = carrying capacity.

        Args:
            environment (float):

        """
        self.population += self.growth_rate * self.population * (1 - self.population/self.max_pop)

    def calc_max_pop(self, environment):
        """calc_max_pop docs

        Args:
            environment (float):

        """
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
    def __init__(self):
        """Mosses class docs

        """
        super(Mosses, self).__init__()


class Grasses(PlantBulk):
    def __init__(self):
        """Grasses class docs

        """
        super(Grasses, self).__init__()


class Perennials(PlantBulk):
    def __init__(self):
        """Perennials class docs

        """
        super(Perennials, self).__init__()


class Shrubs(PlantBulk):
    def __init__(self):
        """Shrubs class docs

        """
        super(Shrubs, self).__init__()


class SoftWoods(PlantBulk):
    def __init__(self):
        """SoftWoods class docs

        """
        super(SoftWoods, self).__init__()


class HardWoods(PlantBulk):
    def __init__(self):
        """HardWoods class docs

        """
        super(HardWoods, self).__init__()

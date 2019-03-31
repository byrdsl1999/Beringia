# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from beringia.feature import Feature
from beringia.flora import PlantBulk


class Fauna(Feature):
    def __init__(self, arg):
        super(Fauna, self).__init__()
        self.arg = arg


class AnimalBulk(Fauna):
    """docstring for animal_bulk"""

    def __init__(self, population=0.0, reproduction_rate=0.01, starvation_rate=0.02, feeding_rate=0.5):
        self.population = population
        # This is essentially the energy conversion rate. (eg 10 lb grass makes 1 lb beef)
        self.reproduction_rate = reproduction_rate
        self.starvation_rate = starvation_rate
        self.feeding_rate = feeding_rate
        self.ambient_death_rate = 0.05

    def zero_correct_pop(self):
        if self.population <= 0:
            self.population = 0.0

    def feed(self, target=None):
        """How to eat.

        Todo:
            * Be able to feed on multiple prey, and select prey. Either at random, in order of prevalence, or order of
            ease of finding.
            * Eat plants.
            * Eat specific animals.

        Args:
            target:

        Returns:
            float: The thing that this returns.
        """
        consumption = self.population * self.feeding_rate

        food = target.population
        if issubclass(type(target), AnimalBulk):
            target.population -= consumption
            target.zero_correct_pop()
        elif issubclass(type(target), PlantBulk):
            pass
        else:
            food = 1.0

        if consumption < food:
            self._breed()
            return consumption
        elif consumption >= food:
            self._starve()
            return food

    def _breed(self):
        # TODO look up population growth rate functions.
        self.population += self.population * self.reproduction_rate

    def _starve(self):
        self.population -= self.population * self.starvation_rate + self.starvation_rate
        self.zero_correct_pop()

    def _ambient_death(self):
        self.population = self.population * (1 - self.ambient_death_rate)
        self.zero_correct_pop()

    def depredation(self, predation_rate):
        pass

    def migrate(self):
        pass

    def pass_time(self, target=1.0):
        self.feed(target)
        self._ambient_death()


class Invertebrates(AnimalBulk):
    def __init__(
            self, population=0.0, reproduction_rate=0.01, starvation_rate=0.25, feeding_rate=0.25,
            fallout_rate=0.001
    ):
        super(Invertebrates, self).__init__(
            population=population, reproduction_rate=reproduction_rate, starvation_rate=starvation_rate,
            feeding_rate=feeding_rate
        )
        self.fallout_rate = fallout_rate

    def fallout(self):
        self.population += self.fallout_rate

    def pass_time(self, food=1.0):
        self.fallout()
        self.feed(food)
        self.zero_correct_pop()
        self._ambient_death()


class InvertDetritivores(Invertebrates):
    def __init__(self, feeding_rate=0.01):
        super(InvertDetritivores, self).__init__(feeding_rate=feeding_rate)


class InvertHerbivores(Invertebrates):
    def __init__(self, feeding_rate=0.01):
        super(InvertHerbivores, self).__init__(feeding_rate=feeding_rate)


class InvertPredators(Invertebrates):
    def __init__(self, feeding_rate=0.15, fallout_rate=0.0001):
        super(InvertPredators, self).__init__(feeding_rate=feeding_rate, fallout_rate=fallout_rate)


class Vertebrates(AnimalBulk):
    def __init__(self, population=0.0, reproduction_rate=0.01, feeding_rate=0.1):
        super(Vertebrates, self).__init__(
            population=population, reproduction_rate=reproduction_rate, feeding_rate=feeding_rate
        )
        self.starvation_rate = 0.1


class Insectivore(Vertebrates):
    def __init__(self, feeding_rate=0.1):
        super(Insectivore, self).__init__(feeding_rate=feeding_rate)


class SmallHerbivore(Vertebrates):
    def __init__(self, feeding_rate=0.1):
        super(SmallHerbivore, self).__init__(feeding_rate=feeding_rate)


class LargeHerbivore(Vertebrates):
    def __init(self, feeding_rate=0.2):
        super(LargeHerbivore, self).__init__(feeding_rate=feeding_rate)


class SmallPredator(Vertebrates):
    def __init(self, feeding_rate=0.2):
        super(SmallPredator, self).__init__(feeding_rate=feeding_rate)


class LargePredator(Vertebrates):
    def __init(self, feeding_rate=0.3):
        super(LargePredator, self).__init__(feeding_rate=feeding_rate)


class MediumOmnivore(Vertebrates):
    def __init(self, feeding_rate=0.25):
        super(MediumOmnivore, self).__init__(feeding_rate=feeding_rate)


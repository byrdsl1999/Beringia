# -*- coding: utf-8 -*-
"""fauna.py

    TODO:
        Fauna will fall into two categories, bulk and unit fauna.
        Bulk Fauna:
            Not individuals, but instead aggregate masses of creatures.
            They will be tracked as non-discrete populations.
            Prototypical of this will be insects.
        Unit Fauna:
            These will be (potentially) roving creatures.
            These should ideally be tracked individually.
            Behaviors:
                Food detection
                Seeking food.
                following prey.
                evading predators
                mating
                keeping home ranges
                herb behavior(mobile home range?).
        Food Web:
            2 types:
                A simple food chain:
                    Plants->Herbivores->Carnivores
                A proper food web:
        Beavers:
            pond building



.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
from beringia.feature import Feature
from beringia.flora import PlantBulk


class Fauna(Feature):
    """Fauna class docs

    Args:
        arg (str):

    """
    def __init__(self, arg):
        super(Fauna, self).__init__()
        self.arg = arg


class AnimalBulk(Fauna):
    """AnimalBulk class docs

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):

    """
    def __init__(self, population=0.0, reproduction_rate=0.01, starvation_rate=0.02, feeding_rate=0.5):
        super(AnimalBulk, self).__init__()
        self.population = population
        # This is essentially the energy conversion rate. (eg 10 lb grass makes 1 lb beef)
        self.reproduction_rate = reproduction_rate
        self.starvation_rate = starvation_rate
        self.feeding_rate = feeding_rate
        self.ambient_death_rate = 0.05

    def zero_correct_pop(self):
        """zero_correct_pop docs

        """
        if self.population <= 0:
            self.population = 0.0

    def feed(self, target=None):
        """feed docs

        Todo:
            * Be able to feed on multiple prey, and select prey. Either at random, in order of prevalence, or order of
                ease of finding.
            * Eat plants.
            * Eat specific animals.
            * Cause the stuff that is being fed on are different classes, this should probably be a feeding that is
                class specific.

        Args:
            target (beringia.feature.Feature):

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
        """depredation docs

        Args:
            predation_rate:

        """
        pass

    def migrate(self):
        """migrate docs
        """
        pass

    def pass_time(self, target=1.0):
        """pass_time docs

        Todo:
            * Again this maybe has problems with typing and the feed method.

        Args:
            target (float):

        """
        self.feed(target)
        self._ambient_death()


class Invertebrates(AnimalBulk):
    """Invertebrates class docs

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):
        fallout_rate (float):

    """
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
        """fallout docs

        """
        self.population += self.fallout_rate

    def pass_time(self, food=1.0):
        """pass_time docs

        Args:
            food (float):

        """
        self.fallout()
        self.feed(food)
        self.zero_correct_pop()
        self._ambient_death()


class InvertDetritivores(Invertebrates):
    """InvertDetritivores class docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.01):
        super(InvertDetritivores, self).__init__(feeding_rate=feeding_rate)


class InvertHerbivores(Invertebrates):
    """InvertHerbivores class docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.01):
        super(InvertHerbivores, self).__init__(feeding_rate=feeding_rate)


class InvertPredators(Invertebrates):
    """InvertPredators class docs

    Args:
        feeding_rate (float):
        fallout_rate (float):

    """
    def __init__(self, feeding_rate=0.15, fallout_rate=0.0001):
        super(InvertPredators, self).__init__(feeding_rate=feeding_rate, fallout_rate=fallout_rate)


class Vertebrates(AnimalBulk):
    """Vertebrates docs

   Args:
       population (float):
       reproduction_rate (float):
       feeding_rate (float):

   """
    def __init__(self, population=0.0, reproduction_rate=0.01, feeding_rate=0.1):
        super(Vertebrates, self).__init__(
            population=population, reproduction_rate=reproduction_rate, feeding_rate=feeding_rate
        )
        self.starvation_rate = 0.1


class Insectivore(Vertebrates):
    """Insectivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.1):
        super(Insectivore, self).__init__(feeding_rate=feeding_rate)


class SmallHerbivore(Vertebrates):
    """SmallHerbivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.1):
        super(SmallHerbivore, self).__init__(feeding_rate=feeding_rate)


class LargeHerbivore(Vertebrates):
    """LargeHerbivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.2):
        super(LargeHerbivore, self).__init__(feeding_rate=feeding_rate)


class SmallPredator(Vertebrates):
    """SmallPredator docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.2):
        super(SmallPredator, self).__init__(feeding_rate=feeding_rate)


class LargePredator(Vertebrates):
    """LargePredator docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.3):
        super(LargePredator, self).__init__(feeding_rate=feeding_rate)


class MediumOmnivore(Vertebrates):
    """MediumOmnivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.25):
        super(MediumOmnivore, self).__init__(feeding_rate=feeding_rate)

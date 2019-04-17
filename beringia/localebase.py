# -*- coding: utf-8 -*-
"""localebase.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import numpy as np

from beringia.soil import Geology, BorderGeology
from beringia.constants import STATE_CONSTANTS, FEATURES_SWITCH, PLANT_COLOR_KEY
from beringia.flora import FloraSystem0, FloraSystem1, FloraSystem2



class Locale(object):
    """A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self):
        self.state = 0
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.on_fire = 0
        self.flora = FloraSystem0()

        if FEATURES_SWITCH['geology']:
            self.geology = Geology()

    def __str__(self):
        if self.on_fire == 0:
            return PLANT_COLOR_KEY[self.state]
        elif self.on_fire == 1:
            return "\033[1;31mf\033[0;37m"

    def __repr__(self):
        return str(self.state)

    def pass_time(self):
        """pass_time doc

        """
        if self.on_fire == 1:
            self.burn()
        self.increment_state()
        self.risk_fire()

    def increment_state(self):
        """increment_state docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['stateIncreaseProb']:
            self.state += 1
            return True
        elif roll > 1-STATE_CONSTANTS[self.state]['stateDecreaseProb']:
            self.state -= 1
            return True
        return False

    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['fireStartProb']:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['fireSpreadProb']:
            self.on_fire = 1
            return True
        return False

    def burn(self):
        """burn docs

        """
        self.state = -1
        self.on_fire = 0


class NewLocale(object):
    """
    IN PROGRESS. Same as old locale in function. implements flora object.
    A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self, flora_system = 1):
        self.flora = self._flora_switch(flora_system)
        if FEATURES_SWITCH['geology']:
            self.geology = Geology()
        self.state = self.flora.state
        self.on_fire = self.flora.on_fire



    def __str__(self):
        if self.on_fire == 0:
            return PLANT_COLOR_KEY[self.state]
        elif self.on_fire == 1:
            return "\033[1;31mf\033[0;37m"

    def __repr__(self):
        return str(self.state)

    def _flora_switch(self, system=1):
        switch={
            0:FloraSystem0(),
            1:FloraSystem1(),
            2:FloraSystem2()
        }
        return switch.get(system, FloraSystem1())

    def _update_values(self):
        self.state=int(self.flora.state)
        self.on_fire = self.flora.on_fire



    def pass_time(self, ticks=1):
        """pass_time doc

        """
        for i in range(ticks):
            if self.flora.on_fire == 1:
                self.flora.burn()
            self.flora.increment_state()
            self.flora.risk_fire()
            self._update_values()


class Border(Locale):
    def __init__(self):
        super(Border, self).__init__()
        self.is_border=True
        if FEATURES_SWITCH['geology']:
            self.geology = BorderGeology()


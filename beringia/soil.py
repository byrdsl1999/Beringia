# -*- coding: utf-8 -*-
"""soil.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Todo:
    * rocks
    * soil depth
        erosion
        accumulation
    * soil moisture
    * elevation
    * hydrology
        evaporation
        flow
        erosion
"""
import numpy as np


class Geology(object):
    def __init__(
            self, elevation_base=np.random.gamma(5, 0.5), soil_depth=np.random.lognormal(0.25, 0), soil_moisture=0.5
    ):
        self.elevation_base = elevation_base
        self.soil_depth = soil_depth
        self.soil_moisture = soil_moisture
        self.elevation = self._elevation()
        self.water_content = self.soil_depth * self.soil_moisture

    def recalculate_values(self):
        self.elevation = self.elevation_base+self.soil_depth
        self.water_content = self.soil_depth * self.soil_moisture

    def _elevation(self):
        return self.elevation_base+self.soil_depth

    def erode(self, magnitude=1.0, rate=0.01, slope=0.1):
        load = magnitude * rate * slope
        transport = 0.0
        if load > self.soil_depth:
            transport += self.soil_depth
            self.soil_depth = 0
            self.soil_depth += (load-self.soil_depth) * rate
            self.elevation_base -= (load-self.soil_depth) * rate
        else:
            transport += load
            self.soil_depth -= load
        self.recalculate_values()
        return transport

    def accrete(self, load):
        self.soil_depth += load
        self.recalculate_values()

    def runoff(self):
        pass

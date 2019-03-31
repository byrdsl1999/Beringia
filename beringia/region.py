# -*- coding: utf-8 -*-
"""region.py
"""
import time

import numpy as np
import networkx as nx

from beringia.localebase import Locale
from beringia.constants import *

STATE_CONSTANTS = {
    0: {'stateIncreaseProb': 0.20,    'stateDecreaseProb': 0,     'fireStartProb': 0.000,    'fireSpreadProb': 0.000},
    1: {'stateIncreaseProb': 0.10,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.0005,    'fireSpreadProb': 0.100},
    2: {'stateIncreaseProb': 0.15,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.0005,    'fireSpreadProb': 0.200},
    3: {'stateIncreaseProb': 0.10,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.0005,    'fireSpreadProb': 0.300},
    4: {'stateIncreaseProb': 0.10,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.0005,    'fireSpreadProb': 0.450},
    5: {'stateIncreaseProb': 0.00,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.0005,    'fireSpreadProb': 0.700},
    -1: {'stateIncreaseProb': 1.00,    'stateDecreaseProb': 0.00,     'fireStartProb': 0.000,    'fireSpreadProb': 0.000}
    }

PLANT_COLOR_KEY = {
    0: '\033[1;30;48;5;246m0\033[0;39m',
    1: '\033[1;30;48;5;190m1\033[0;39m',
    2: '\033[1;30;48;5;118m2\033[0;39m',
    3: '\033[1;30;48;5;46m3\033[0;39m',
    4: '\033[1;30;48;5;34m4\033[0;39m',
    5: '\033[1;30;48;5;2m5\033[0;39m',
    -1: 'f'
}


class Region():
    def __init__(self, xdim=10, ydim=10, gridType='2d', colorize=True):
        self.xdim = xdim
        self.ydim = ydim
        self.gridType = gridType
        if gridType == '2d':
            self.space = nx.grid_2d_graph(xdim, ydim)
        elif gridType == 'hex':
            self.space = nx.hexagonal_lattice_graph(xdim, ydim)
        elif gridType == 'tri':
            self.space = nx.triangular_lattice_graph(xdim, ydim)
        else:
            # TODO: raise exception? default to 2d?
            self.space = nx.grid_2d_graph(xdim, ydim)
        for node in self.space.nodes:
            self.space.node[node]['locale'] = Locale()
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.time = 0
        self.colorize=colorize
        self.constants=STATE_CONSTANTS

    def __repr__(self, verbose=False):
        if not verbose or self.gridType != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else: 
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def __str__(self, verbose=False):
        if not verbose or self.gridType != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else: 
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def show_map(self, do_print=True):
        if self.gridType == '2d':
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale(x, y))
                out += '\n'
            out += '\r''
            if do_print:
                print(out)
            else: 
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fire_map(self, do_print=True):
        """Display a visual representation of the self.space attribute with fire state layered on if doPrint.

        Args:
            do_print:

        Returns:
             str:
        """
        if self.gridType == '2d':
            out=""
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale(x, y, fire_state=True))
                out += '\n'
            if do_print:
                print(out)
            else: 
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_elevation_map(self, do_print=True):
        if self.gridType == '2d':
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_elevation(x, y))
                out += '\n'
            if do_print:
                print(out)
            else: 
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def pass_time(self, count=1):
        """Move forward one time(or count # of) step(s).

        Args:
            count:
        """
        for _ in range(count):
            self.time += 1
            for node in self.space.nodes:
                self.space.node[node]['locale'].pass_time()
            self.spread_fire()
            self.erode_all(magnitude=0.1)

    def show_turns(self, count=1, pause=0.5):
        for _ in range(count):
            self.pass_time()
            self.show_map()
            time.sleep(pause)

    def spread_fire(self, slow_burn=False):
        """Scan locales for fire, and if present, cause fire to spread to neighboring regions.

        Args:
            slow_burn:
        """
        locales_on_fire = []
        locales_to_burn = {}
        fires_present = False
        for node in self.space.nodes:
            if self.space.node[node]['locale'].onFire == 1: 
                locales_on_fire.append(node)
        if locales_on_fire:
            fires_present = True
        for locale_ in locales_on_fire:
            neighboring_nodes = self.space.neighbors(locale_)
            for node in neighboring_nodes:
                if self.space.node[node]['locale'].onFire==0:
                    if self.space.node[node]['locale'].catch_fire():
                        locales_on_fire.append(node)
                        if slow_burn:
                            self.show_map()
                            time.sleep(0.15)
        if fires_present:
            self.show_map()
            time.sleep(0.5)

    def view_locale(self, x, y, fire_state=False):
        if fire_state:
            return self.space.node[(x, y)]['locale'].onFire
        else:
            return self.space.node[(x, y)]['locale']

    def view_elevation(self, x, y):
        return int(self.space.node[(x,y)]['locale'].geology.elevation//1)

    def erode_one(self, node, magnitude=1.0, rate=0.01):
        """This will cause erosion to occur at one location.

        Args:
            node:
            magnitude:
            rate:
        """
        neighboring_nodes=self.space.neighbors(node)
        lowest_neighbor = node
        for eachNode in neighboring_nodes:
            if self.space.node[lowest_neighbor]['locale'].geology.elevation > \
                    self.space.node[eachNode]['locale'].geology.elevation:
                lowest_neighbor = eachNode

        if lowest_neighbor != node:
            slope = (self.space.node[node]['locale'].geology.elevation -
                     self.space.node[lowest_neighbor]['locale'].geology.elevation)
        else: 
            slope = 0.01
        transport = self.space.node[node]['locale'].geology.erode(magnitude, rate, slope)
        self.space.node[lowest_neighbor]['locale'].geology.accrete(transport)

    def erode_all(self, magnitude=1.0, rate=0.01):
        for node in self.space.nodes:
            self.erode_one(node, magnitude, rate)

    def randomize_elevation_base(self, mean=5, sd=1.5):
        for node in self.space.nodes():
            self.space.node[node]['locale'].geology.elevation_base = np.random.normal(mean,sd)
            self.space.node[node]['locale'].geology.recalculate_values()

    def randomize_elevation_base_cov(self, mean=5, cov = 0.4):
        adj_mat=nx.adjacency_matrix(self.space).todense()
        means=[mean for _ in range(self.xdim * self.ydim)]
        elevations=np.random.multivariate_normal(means, (adj_mat*cov))
        for node in enumerate(self.space.nodes):
            self.space.node[node[1]]['locale'].geology.elevation_base = elevations[node[0]]


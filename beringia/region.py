# -*- coding: utf-8 -*-
"""region.py

The region object should be tasked with all inter locale interactions. These might include fire spreading, and locales
eroding from ones locale to another. Locales should be able to handle all their actions on their own, but return any
relevant info that the interation requires.

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import time
#import simpy as sp

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from beringia.localebase import Locale
from beringia.localebase import Border
from beringia.constants import STATE_CONSTANTS, PLANT_COLOR_KEY, GRAYSCALE_COLOR_KEY
from math import floor



class Region(object):
    """Region class docs

    A
        xdim (int):
        ydim (int):
        grid_type (str):
        colorize (bool):

    """
    def __init__(self, xdim=10, ydim=10, grid_type='2d', flora_system=1, colorize=True, edges=True, slow_burn=False):
        self.xdim = xdim
        self.ydim = ydim
        self.grid_type = grid_type
        if grid_type == '2d':
            self.space = nx.grid_2d_graph(self.xdim, ydim)
        elif grid_type == 'hex':
            self.space = nx.hexagonal_lattice_graph(self.xdim, ydim)
        elif grid_type == 'tri':
            self.space = nx.triangular_lattice_graph(self.xdim, ydim)
        else:
            # TODO: raise exception? default to 2d?
            self.space = nx.grid_2d_graph(self.xdim, ydim)
        for node in self.space.nodes:
            self.space.node[node]['locale'] = Locale(flora_system=flora_system, location=node, region=self)
        self.nodes = set([node for node in self.space.nodes])
        if edges:
            self._add_border_nodes()
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.time = 0
        self.colorize = colorize
        self.slow_burn = slow_burn
        self.constants = STATE_CONSTANTS
        self.verbose = False


    #def _scheduler(self):
    #    self.time_env = sp.Environment()


    def __repr__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def __str__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def _add_border_nodes(self):
        """"
        Presently border nodes are going to copy the properties of their neighboring nodes.
        :return:
        """
        self.border_nodes = set()
        for i in range(self.xdim):
            self.space.add_node((i, -1))
            self.space.add_edge((i, -1), (i, 0))
            self.border_nodes.add((i, -1))
            self.space.add_node((i, self.ydim))
            self.space.add_edge((i, self.ydim), (i, self.ydim - 1))
            self.border_nodes.add((i, self.ydim))
        for j in range(self.ydim):
            self.space.add_node((-1, j))
            self.space.add_edge((-1, j), (0, j))
            self.border_nodes.add((-1, j))
            self.space.add_node((self.xdim, j))
            self.space.add_edge((self.xdim, j), (self.xdim - 1, j))
            self.border_nodes.add((self.xdim, j))
        for node in self.border_nodes:
            self.space.node[node]['locale'] = Border()
            neighbor=[i for i in nx.neighbors(self.space, node)][0]
            self.space.node[node]['locale'].geology.elevation_base = self.space.node[neighbor]['locale'].geology.elevation_base
            self.space.node[node]['locale'].geology.soil_depth = self.space.node[neighbor]['locale'].geology.soil_depth
            self.space.node[node]['locale'].geology.elevation = self.space.node[neighbor]['locale'].geology.elevation


    def show_map(self, do_print=True, show_fire=True, colorize=True):
        """show_map docs

        Args:
            do_print (bool):
            show_fire (bool):
            colorize (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            if do_print:
                out = ''
                for y in range(self.ydim):
                    for x in range(self.xdim):
                        if self.get_locale(x,y).on_fire == 1 and show_fire:
                            if colorize:
                                out += "\033[1;31mf\033[0;37m"
                            else:
                                out += "f"
                        else:
                            out += str(self.view_locale(x, y, colorize=colorize))
                    out += '\n'
                out += '\r'
                print(out)
            elif not do_print:
                out = ''
                for y in range(self.ydim):
                    for x in range(self.xdim):
                        if self.get_locale(x,y).on_fire == 1 and show_fire:
                            out += "f"
                        else:
                            out += str(self.view_locale(x, y, colorize=colorize))
                    out += '\n'
                out += '\r'
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fire_map(self, do_print=True):
        """Display a visual representation of the self.space attribute with fire state layered on if doPrint.

        Args:
            do_print (bool):

        Returns:
             str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_locale(x, y, fire_state=True))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_elevation_map(self, do_print=True):
        """show_elevation_map docs

        Args:
            do_print (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_elevation(x, y, colorize= True))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fauna_map(self, do_print=True, index=0):
        """show_elevation_map docs

        Args:
            do_print (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_fauna_pop(x, y, index, colorize=True, ceiling=10.0))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def get_map_array(self, kind="flora", index=0):
        if self.grid_type != '2d':
            print("Grid type:", self.grid_type, " not supported.")
            return None
        elif self.grid_type == '2d':
            grid = np.zeros((self.xdim, self.ydim))
            for i in range(self.xdim):
                for j in range(self.ydim):
                    if kind == "flora":
                        grid[i, j]=self.get_locale(i, j).state
                    elif kind == "fauna":
                        grid[i, j] = self.get_locale(i, j).fauna[index].population*100
                    elif kind == "elev" or kind == "elevation":
                        grid[i, j] = self.get_locale(i, j).geology.elevation
                    else:
                        grid[i, j]=self.get_locale(i, j).state
                        print("Map type error. Returning default.")  #How should I be handling this?
            return grid

    def show_heat_map(self, kind="flora"):
        array = self.get_map_array(kind)
        plt.imshow(array, cmap="YlGn")
        plt.colorbar()
        plt.show()

    def pass_time(self, count=1, show_heat_map=False):
        """Move forward one time(or count # of) step(s).

        Args:
            count (int):

        """
        if not show_heat_map or count > 50:
            if show_heat_map: print("Count too high. Display hidden")
            for _ in range(count):
                self.time += 1
                for node in self.nodes:
                    self.space.node[node]['locale'].pass_time()
                self.spread_fire(show=False)
                self.erode_all(magnitude=0.1)
        if show_heat_map:
            array = self.get_map_array("flora")
            plt.imshow(array, cmap="YlGn")
            plt.colorbar()
            for _ in range(count):
                self.time += 1
                for node in self.nodes:
                    self.space.node[node]['locale'].pass_time()
                self.spread_fire(show=False)
                self.erode_all(magnitude=0.1)

                array = self.get_map_array("flora")
                plt.imshow(array, cmap="YlGn")
                plt.draw()
                plt.pause(0.1)

    def show_turns(self, count=1, pause=0.25):
        for _ in range(count):
            self.pass_time()
            self.show_map()
            time.sleep(pause)

    def spread_fire(self, verbose=False, pause=0.15, show=True):
        """Scan locales for fire, and if present, cause fire to spread to neighboring regions.

        Todo:
            * add locales_to_burn

        Args:
            slow_burn (bool):

        """
        locales_on_fire = []
        fires_present: bool = False
        for node in self.nodes:
            if self.space.node[node]['locale'].on_fire == 1:
                locales_on_fire.append(node)
        if verbose: print("Locales initially on fire:", locales_on_fire)
        if locales_on_fire:
            fires_present = True
            if verbose: print("Fire is present.")
        for locale_ in locales_on_fire:
            neighboring_nodes = self.space.neighbors(locale_)
            if verbose: print("Fire is burning at:", node)

            for node in neighboring_nodes:
                if self.space.node[node]['locale'].flora.on_fire == 0:
                    if self.space.node[node]['locale'].catch_fire():
                        locales_on_fire.append(node)

                        if verbose: print("Fire has spread to:", node)

                        if self.slow_burn and show:
                            self.show_map()
                            time.sleep(pause)
        if fires_present and not self.slow_burn and show:
            self.show_map()
            time.sleep(pause*2)

    def insert_new_fauna(self, new_fauna=None, target=None, all_locales=True, target_locale=None, simple_food_chain=True):
        """insert_new_fauna docs

        Args:
            new_fauna (fauna):
            target (feature, or other):
            all_locales (bool):
            target_locale (Locale):
            simple_food_chain (bool)

        Returns:
            (bool): T/F success/failure

        """
        if all_locales:
            for node in self.nodes:
                if simple_food_chain:
                    self.space.node[node]['locale'].insert_fauna(new_fauna)
                    self.space.node[node]['locale'].fauna_set_simple_food_chain()
                else:
                    self.space.node[node]['locale'].insert_fauna(new_fauna, target)
            return True
        elif target_locale:
            if simple_food_chain:
                self.space.node[target_locale]['locale'].insert_fauna(new_fauna)
                self.space.node[target_locale]['locale'].fauna_set_simple_food_chain()
            else:
                self.space.node[target_locale]['locale'].insert_fauna(new_fauna, target)
            return True
        else:
            print("No target locale specified")
            return False

    def view_locale(self, x=0, y=0, fire_state=False, colorize=True):
        """view_locale docs

        Args:
            x (int):
            y (int):
            fire_state (bool):
            colorize (bool):

        Returns:
            beringia.locale.Locale:

        """
        if fire_state:
            return self.space.node[(x, y)]['locale'].on_fire
        else:
            if colorize:
                return PLANT_COLOR_KEY[int(floor(self.space.node[(x, y)]['locale'].state))]
            else:
                return int(floor(self.space.node[(x, y)]['locale'].state))

    def view_elevation(self, x=0, y=0, colorize=False):
        """view_elevation docs

        Args:
            x (int):
            y (int):
            colorize(bool)

        Returns:
            int:

        """
        if colorize:
            return GRAYSCALE_COLOR_KEY[int(self.space.node[(x, y)]['locale'].geology.elevation//1)]
        else:
            return self.space.node[(x, y)]['locale'].geology.elevation

    def view_fauna_pop(self, x=0, y=0, index=0, colorize=False, scale_factor=1.0, ceiling=100.0):
        """view_elevation docs

        Args:
            x (int): locale x dim.
            y (int): locale y dim.
            index (int): which fauna element to return. default is the first.
            colorize(bool): whether or not to return output with ascii colorization.

        Returns:
            int: May have ascii colorization.

        """
        if self.space.node[(x, y)]['locale'].fauna:
            if colorize:
                return GRAYSCALE_COLOR_KEY[min(ceiling, (int(self.space.node[(x, y)]['locale'].fauna[index].population * scale_factor //1)))]
            else:
                return int(self.space.node[(x, y)]['locale'].fauna[index].population * scale_factor //1)

    def erode_one(self, node, magnitude=1.0, rate=0.01):
        """This will cause erosion to occur at one location.

        Args:
            node (networkx.Graph.nodes):
            magnitude (float):
            rate (float):

        """
        neighboring_nodes = self.space.neighbors(node)
        lowest_neighbor = node
        for eachNode in neighboring_nodes:
            if self.space.node[lowest_neighbor]['locale'].geology.elevation > self.space.node[eachNode]['locale'].geology.elevation:
                lowest_neighbor = eachNode

        if lowest_neighbor != node:
            slope = (self.space.node[node]['locale'].geology.elevation
                     - self.space.node[lowest_neighbor]['locale'].geology.elevation)
        else:
            slope = 0.01
        transport = self.space.node[node]['locale'].geology.erode(magnitude, rate, slope)
        self.space.node[lowest_neighbor]['locale'].geology.accrete(transport)

    def erode_all(self, magnitude=1.0, rate=0.01):
        """erode_all docs

        Args:
            magnitude (float):
            rate (float):

        """
        for node in self.nodes:
            self.erode_one(node, magnitude, rate)

    def calculate_aspect(self):
        if self.grid_type == '2d':
            for y in range(self.ydim):
                for x in range(self.xdim):

                    if y == 0:
                        north = self.view_elevation(x,y, colorize=False)
                    else:
                        north = self.view_elevation(x, y-1, colorize=False)

                    if y == self.ydim:
                        south = self.view_elevation(x, y, colorize=False)
                    else:
                        south = self.view_elevation(x, y+1, colorize=False)

                    if x == 0:
                        east = self.view_elevation(x,y, colorize=False)
                    else:
                        east = self.view_elevation(x-1, y, colorize=False)

                    if x == self.xdim:
                        west = self.view_elevation(x,y, colorize=False)
                    else:
                        west = self.view_elevation(x+1, y, colorize=False)

                    print(north, south, east, west)
                    self.space.node[(x, y)]['locale'].geology._calculate_aspect(north, south, east, west)

    def randomize_elevation_base(self, mean=5, sd=1.5):
        """randomize_elevation_base docs

        Args:
            mean (int):
            sd (float):

        """
        for node in self.nodes:
            self.space.node[node]['locale'].geology.elevation_base = np.random.normal(mean, sd)
            self.space.node[node]['locale'].geology.recalculate_values()

    def randomize_elevation_base_cov(self, mean=5, cov=0.4):
        """randomize_elevation_base_cov docs

        Args:
            mean (int):
            cov (float):

        """
        adj_mat = nx.adjacency_matrix(self.space).todense()
        means = [mean for _ in range(self.xdim * self.ydim)]
        elevations = np.random.multivariate_normal(means, (adj_mat*cov))
        for node in enumerate(self.nodes):
            self.space.node[node[1]]['locale'].geology.elevation_base = elevations[node[0]]

    def find_basins(self):
        """Find all the basins in the region and update the locales with the elevation of the point of outflow for the
        basin.
        TODO: Maybe we should track all the basins, and then populate them with fish!
        """
        pass

    def get_locale(self, x=0, y=0):
        if x> self.xdim or y>self.ydim or x <0 or y <0:
            print("Value out of range.")
            return None
        else:
            return self.space.node[(x,y)]['locale']

    def get_neighbors(self, x=0, y=0, depth=1, tiered=False, ids=False, borders=False):
        if x > self.xdim or y > self.ydim or x < 0 or y < 0:
            if self.verbose:
                print("Value out of range.")
            return None
        else:
            explored = set()
            neighbors = []
            new_queue = [self.get_locale(x,y).location]
            for _ in range(depth):
                queue = new_queue
                new_queue = []
                if tiered:
                    tier = []
                for node in queue:
                    if (node[0] < 0 or node[0] > self.xdim or node[1] < 0 or node[1] > self.ydim) and borders is False:
                        pass
                    else:
                        if node not in explored:
                            neighbs = self.space.neighbors(node)
                            neighbs = [n for n in neighbs if n not in explored]     # removing duplicates.
                            if not borders:
                                neighbs = [n for n in neighbs if
                                           not (n[0] < 0 or n[0] > self.xdim or n[1] < 0 or n[1] > self.ydim)]
                            if ids:
                                if tiered:
                                    tier.extend(neighbs)
                                else:
                                    neighbors.extend(neighbs)
                            else:
                                if tiered:
                                    tier.extend([self.get_locale(*locale) for locale in neighbs])
                                else:
                                    neighbors.extend([self.get_locale(*locale) for locale in neighbs])
                            new_queue.extend(neighbs)
                    explored.add(node)
                if tiered:
                    neighbors.append(tier)

        return neighbors


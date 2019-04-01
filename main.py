import numpy as np
import networkx as nx
import time
import region as reg

class session(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.region = None
		self.main()
		self.xdim=10
		self.ydim=10

	def main(self):
		self.set_dimensions()
		self.region=reg.region(self.xdim, self.ydim)
		while True:
			inp = input("enter command('h' for help):")
			if inp in ['exit', 'e']: 
				break
			else: 
				self.parser(inp)

	def parser(self, inp):
		inp = str(inp).lower()
		if inp in ['h', 'help',]:
			self.help()
		if inp in ['param', 'parameters']:
			self.set_parameters()
		if inp in ['reset']:
			self.reset()
		if inp in ['e', 'exit']:
			self.exit()
		if inp in ['run', 'r']:
			self.run()
		if inp in ['elev', 'elevation']:
			self.show_elevation()


	def help(self):
		print("e: exit \nrun: run \nh: help\nreset: reset with a new region.\nelev: Show Elevation Map")

	def set_parameters(self):
		print("This function is not yet implemented.")

	def set_dimensions(self):
		self.xdim = int(input("x dimension(10-30 ideal)?"))
		self.ydim = int(input("y dimension?"))

	def reset(self):
		self.set_dimensions()
		self.region=reg.region(self.xdim, self.ydim)

	def run(self):
		turns = int(input("how many turns?"))
		self.region.showTurns(turns)

	def show_elevation(self):
		self.region.showElevationMap()

	def exit(self):
		pass

if __name__ == "__main__": 
	session()

#!/usr/bin/env python3

import sys as _sys


# NOTE:
#	as long as we import something from this file, these lines will always
#	get run, so we will be able to import pyna from the importing file.
#
#	Add source files to import search path
_sys.path.append("../../src") # Module imports
_sys.path.append("../src") # Suite imports



# data utilities
def print_bin(data):
	"""
		A tool for inspecting binary output, prints each byte to stdout
	"""
	try:
		for byte in data:
			print('{0:08b}'.format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		print('{0:08b}'.format(data if isinstance(data, int) else ord(data)))

def bin(data):
	"""
		A tool for inspecting binary output, returns a list containing each byte
	"""
	out = []
	try:
		for byte in data:
			out.append('{0:08b}'.format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		out.append('{0:08b}'.format(data if isinstance(data, int) else ord(data)))
	return out

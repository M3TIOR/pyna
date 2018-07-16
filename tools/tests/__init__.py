#!/usr/bin/env python3

#
# M3TIOR 2018
#	XXX don't forget you can call a library as a main executable in python XXX
#

import sys as sys
import os.path as path

# NOTE: MISC
#	as long as we import something from this file, these lines will always
#	get run, so we will be able to import pyna from the importing file.
#
#	Add source files to import search path
srcdir = path.abspath(path.join(path.dirname(repr(__file__)[1:-1]), "../../src"))
sys.path.append(srcdir)

def print_bits(data, size=8):
	"""A tool for inspecting binary output, prints each byte's bits to stdout"""
	try:
		for byte in data:
			print("".join(['{0:0',str(8),'b}']).format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		print("".join(['{0:0',str(8),'b}']).format(data if isinstance(data, int) else ord(data)))

def bits(data, size=8):
	"""A tool for inspecting binary output, returns a list containing each
	bytes' bits as a string."""
	out = []
	try:
		for byte in data:
			out.append("".join(['{0:0',str(8),'b}']).format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		out.append("".join(['{0:0',str(8),'b}']).format(data if isinstance(data, int) else ord(data)))
	return out

def int_from_bits(string):
	i = 0
	for char in string:
		if char == "1": i<<=1; i|=1;
		elif char == "0": i<<=1; i|=0;
		else:
			return 0
	return i

#!/usr/bin/env python3

#
# M3TIOR 2018
#

# globals import
# XXX:
#	these imports are really weird because of how I'm stucturing things.
#	I'm not changing the current archetecture unless it causes future problems
#	because this is how I want it to work. Four lines is tolerable.
try:
	from . import bin
except(ImportError, SystemError):
	# this allows each individual test to be run as a script independently
	from __init__ import bin

import unittest
import random
import copy
import pyna


class translations(unittest.TestCase):

	def test_string_translation():

	def test_binary_translation():


if __name__ == "__main__":
	unittest.main(verbosity=2)

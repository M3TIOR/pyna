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
	from . import bits, int_from_bits
	from .strategies import nucleotides, bioencodings
except(ImportError, SystemError):
	# this allows each individual test to be run as a script independently
	from __init__ import bits, int_from_bits
	from strategies import nucleotides, bioencodings

import unittest as unittest
import random as random
import copy as copy

from hypothesis import given

class test_types(unittest.TestCase):

	@given(nucleotides())
	def test_nucleotide(self, nucleotide):
		pass

	@given(bioencodings())
	def test_bioencoding(self, encoding):
		print(encoding, encoding.nucleotides())


if __name__ == "__main__":
	unittest.main(verbosity=2)

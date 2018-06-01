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
except(ImportError):
	# this allows each individual test to be run as a script independently
	from __init__ import bin

import unittest
import random
import copy
import pyna

class DNAEncoding(unittest.TestCase):

	def test_new_instance(self):
		new_instance = pyna.DNAEncoding()

		# type
		self.assertIsInstance( new_instance, pyna.DNAEncoding)

		# keys and values are aligned
		self.assertEqual( list(new_instance.keys()), ["G","C","A","T"])
		self.assertEqual( list(new_instance.values()) , [ 0, 0, 1, 1] )

		# correct value nucleotide count
		self.assertEqual( len(new_instance.items()), 4)

	def test_rebinding(self):
		indexes = range(1,5)	 # where we're defining each char
		keys = ["M","E","O","W"] # the new nucleotide chars
		assignment = list(zip(indexes, keys))
		assigned = pyna.DNAEncoding(off=dict(assignment[0:2]), on=dict(assignment[2:4]))

		# check assignment
		self.assertEqual( list(assigned.keys()), ["M","E","O","W"])# for readability
		self.assertEqual( list(assigned.values()), [ 0, 0, 1, 1])

	def test_wrong_keycount_rebinding(self):
		indexes = range(1,4)	 # one too few indexes means one too few nucleotides
		keys = ["M","E","O","W"] # the new nucleotide chars
		rebinding= list(zip(indexes, keys))
		self.assertRaises(
			pyna.NucleotideError,
			pyna.DNAEncoding,
			off=dict(rebinding[0:2]),
			on=dict(rebinding[2:4])
		)

	def test_redundant_index_rebinding(self):
		# there needs to be 1,2,3,4 here, we should only have
		# two values by the end of this
		indexes = [1,1,1,4]

		keys = ["M","E","O","W"] # nucleotide chars
		rebinding= list(zip(indexes, keys))
		self.assertRaises(
			pyna.NucleotideError,
			pyna.DNAEncoding,
			off=dict(rebinding[0:2]),
			on=dict(rebinding[2:4])
		)


if __name__ == "__main__":
	unittest.main(verbosity=2)

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
import pyna

class decode(unittest.TestCase):

	def setUp(self):
		self.dna_encoding = pyna.BioEncoding.DNA()
		self.rna_encoding = pyna.BioEncoding.RNA()
		self.static_dna_strand = "ATCGATATGCATAGTACATAG"
		self.static_rna_strand = "UAUGCUAAACGUAGGAUAGUGA"
		self.random_dna_strand = "" #TODO implement more variable test cases

	def test_executable_tail_static(self):
		binary = pyna.decode( self.static_dna_strand, self.dna_encoding)
		self.assertEqual( bin(binary),
			[
				"11001111",
				"00111011",
				"01110000"
			]
		)

	def test_executable_head_static(self):
		binary = pyna.decode( self.static_dna_strand, self.dna_encoding, head=True )
		self.assertEqual( bin(binary),
			[
				"00011001",
				"11100111",
				"01101110"
			]
		)

	def test_executable_flipTail_static(self):
		binary = pyna.decode( self.static_dna_strand, self.dna_encoding, flip=True )
		self.assertEqual( bin(binary),
			[	"01110110",
				"11100111",
				"10011000"
			]
		)

	def test_executable_flipHead_static(self):
		binary = pyna.decode( self.static_dna_strand, self.dna_encoding, flip=True, head=True )
		self.assertEqual( bin(binary),
			[
				"00001110",
				"11011100",
				"11110011"
			]
		)
	def test_storage_tail_static(self):
		binary = byna.decode( self.static_rna_strand, self.rna_encoding, flip=True)

if __name__ == "__main__":
	unittest.main(verbosity=2)

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

class nucleotide(unittest.TestCase):
	def setUp(self):
		self.a = pyna.Nucleotide("Adenine")
		self.t = pyna.Nucleotide("Thymine", transient=True)
		self.u = pyna.Nucleotide("Uracil", transient=True)

	def test_instance(self):
		self.assertEqual(self.a.is_transient(), False)
		self.assertEqual(self.t.is_transient(), True)
		self.assertEqual(self.u.is_transient(), True)

	def test_pair(self):
		a = self.a
		t = self.t
		u = self.u

		a.pair(t)
		self.assertEqual(a.sibling(), t)

		a.pair(u)
		self.assertEqual(a.sibling(), u)
		self.assertEqual(t.sibling(), a)

	def test_couple(self):
		c, g = pyna.Nucleotide.couple("Cytosine", "Guanine")
		z, l = pyna.Nucleotide.couple("Zelda", "Link", transient=-1)
		ga, m = pyna.Nucleotide.couple("Ganondorf", "Midna", transient=999999)

		self.assertEqual(g.sibling(), c)
		self.assertEqual(c.sibling(), g)

		self.assertEqual(z.is_transient(), True)
		self.assertEqual(l.is_transient(), False)
		self.assertEqual(m.is_transient(), True)


if __name__ == "__main__":
	unittest.main(verbosity=2)

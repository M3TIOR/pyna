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

class BioEncoding(unittest.TestCase):
	def setUp(self):
		self.default_storage = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Hed", "Ehd", transient=-1),
			*pyna.Nucleotide.siblings("Rp", "Pr"),
			standby=pyna.Nucleotide("Dhe", transient=True)
		)
		self.default_executable = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Hed", "Ehd", transient=-1),
			*pyna.Nucleotide.siblings("Rp", "Pr"),
			standby=pyna.Nucleotide("Dhe", transient=True)
			executable=True
		)
		self.no_transient_storage = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Do", "Od"),
			*pyna.Nucleotide.siblings("Nt", "Tn")
			standby=pyna.Nucleotide("Pe", transient=True)
		)
		self.no_standby_storage = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Do", "Od"),
			*pyna.Nucleotide.siblings("It", "Ti", transient=-1)
		)
		self.no_transient_executable = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Do", "Od"),
			*pyna.Nucleotide.siblings("Nt", "Tn")
			standby=pyna.Nucleotide("Pe", transient=True)
			executable=True
		)
		self.no_standby_executable = pyna.BioEncoding(
			*pyna.Nucleotide.siblings("Do", "Od"),
			*pyna.Nucleotide.siblings("It", "Ti", transient=-1)
			executable=True
		)

		# NOTE: for shortening variable names en locale scope
		#s = self.default_storage
		#e = self.default_executable
		#nts = self.no_transient_storage
		#nss = self.no_standby_storage
		#nte = self.no_transient_executable
		#nse = self.no_standby_executable


	def test_keys(self):
		s = self.default_storage
		e = self.default_executable
		nts = self.no_transient_storage
		nss = self.no_standby_storage
		nte = self.no_transient_executable
		nse = self.no_standby_executable
		self.assertEqual( s.keys(), ["H","E","R","P"] )
		self.assertEqual( e.keys(), ["D","E","R","P"] )
		self.assertEqual( nts.keys(), ["D","O","N","T"] )
		self.assertEqual( nss.keys(), ["D","O","I","T"] )
		self.assertEqual( nte.keys(), ["D","O","N","T"] )
		self.assertEqual( nse.keys(), ["D","O","I","T"] )

	def test_values(self):
		s = self.default_storage
		e = self.default_executable
		nts = self.no_transient_storage
		nss = self.no_standby_storage
		nte = self.no_transient_executable
		nse = self.no_standby_executable

		self.assertEqual( s.values() , [ 0, 1, 2, 3] )
		self.assertEqual( s.is_storage(), True)

		self.assertEqual( e.values() , [ 0, 0, 1, 1] )
		self.assertEqual( e.is_executable(), True)

		self.assertEqual( nts.values() , [ 0, 1, 2, 3] )
		self.assertEqual( nts.is_storage(), True)

		self.assertEqual( nss.values() , [ 0, 1, 2, 3] )
		self.assertEqual( nss.is_storage(), True)

		self.assertEqual( nte.values() , [ 0, 0, 1, 1] )
		self.assertEqual( nte.is_executable(), True)

		self.assertEqual( nse.values() , [ 0, 0, 1, 1] )
		self.assertEqual( nse.is_executable(), True)

	def test_dict(self):
		s = self.default_storage
		e = self.default_executable
		nts = self.no_transient_storage
		nss = self.no_standby_storage
		nte = self.no_transient_executable
		nse = self.no_standby_executable

		self.assertEqual( [s[key] for key in ["H","E","R","P"], [ 0, 1, 2, 3])
		self.assertEqual( s.is_storage(), True)

		self.assertEqual( [e[key] for key in ["D","E","R","P"], [ 0, 0, 1, 1])
		self.assertEqual( e.is_executable(), True)

		self.assertEqual( [nts[key] for key in ["D","O","N","T"], [ 0, 1, 2, 3])
		self.assertEqual( nts.is_storage(), True)

		self.assertEqual( [nss[key] for key in ["D","O","I","T"], [ 0, 1, 2, 3])
		self.assertEqual( nss.is_storage(), True)

		self.assertEqual( [nte[key] for key in ["D","O","N","T"], [ 0, 0, 1, 1])
		self.assertEqual( nte.is_executable(), True)

		self.assertEqual( [nse[key] for key in ["D","O","I","T"], [ 0, 0, 1, 1])
		self.assertEqual( nse.is_executable(), True)

	# XXX
	#	Test type change last so we don't screw up the values for
	#	the other tests, just in case.
	def test_switch(self):
		s = self.default_storage
		e = self.default_executable
		nts = self.no_transient_storage
		nss = self.no_standby_storage
		nte = self.no_transient_executable
		nse = self.no_standby_executable

		self.assertEqual(s.switch(), True)
		self.assertEqual( s.keys(), ["D","E","R","P"] )
		self.assertEqual( [s[key] for key in ["D","E","R","P"], [ 0, 0, 1, 1])

		self.assertEqual(s.switch(), True)
		self.assertEqual( e.keys(), ["H","E","R","P"] )
		self.assertEqual( [e[key] for key in ["H","E","R","P"], [ 0, 1, 2, 3])

		self.assertRaises(nts.switch(), pyna.BioEncodingError)
		self.assertRaises(nss.switch(), pyna.BioEncodingError)
		self.assertRaises(nte.switch(), pyna.BioEncodingError)
		self.assertRaises(nse.switch(), pyna.BioEncodingError)

		self.assertEqual(nts.switch(silent=True), False)
		self.assertEqual(nss.switch(silent=True), False)
		self.assertEqual(nte.switch(silent=True), False)
		self.assertEqual(nse.switch(silent=True), False)


if __name__ == "__main__":
	unittest.main(verbosity=2)

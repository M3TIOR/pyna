#!/usr/bin/env python3

#
# M3TIOR 2018
#

# globals import
# NOTE: also, add path for pyna import
from __init__ import bits, int_from_bits

# BUILTIN IMPORTS
import unittest
import random
import logging
from math import log2, floor, ceil

# THE LIBRARY WE'RE TESTING
import pyna

# HYPOTHESIS LIBRARY TESTING ASSIST
from hypothesis import given
from hypothesis.strategies import integers
from strategies import nucleotides, bioencodings

class core(unittest.TestCase):

	@given(integers(), bioencodings())
	def test_random(self, nucleotide_count, encoding):
		rand = pyna.random(nucleotide_count,
			output_flags = pyna.Flags.ALL,
			encoding = encoding
		)

		forward_string = rand["forward_string"]
		reverse_string = rand["reverse_string"]

		forward_bits = ""
		reverse_bits = ""
		for fb, rb in zip(rand["forward_binary"], rand["reverse_binary"]):
			forward_bits += "".join(bits(fb))
			reverse_bits += "".join(bits(rb))

		ns = ceil(log2(len(encoding) - 1)) # size in bits of each nucleotide

		# TEST SIZE CONSTRAINT
		self.assertEqual(len(forward_string), nucleotide_count)
		self.assertEqual(len(reverse_string), nucleotide_count)

		# TEST BINARY OUTPUTS EQUIVALENCE
		self.assertEqual(forward_bits, reverse_bits[::-1])

		# TEST STRING OUTPUTS EQUIVALENCE
		self.assertEqual(forward_string,"".join([
			encoding.get_key(
				int_from_bits(
					"".join(bits(encoding.get_value(char), size=ns))[::-1]
				) >> 8-ns
			)
			for char in reverse_string[::-1]
		]))

		# TEST FORWARD OUTPUTS EQUIVALENCE
		self.assertEqual(forward_string,"".join([
			encoding.get_key(
				int_from_bits( forward_bits[i:i+ns] )
			)
			for i in range(0, len(forward_bits) - ns**2, ns)
		]))

		# TEST REVERSE OUTPUTS EQUIVALENCE
		self.assertEqual(reverse_string,"".join([
			encoding.get_key(
				int_from_bits( reverse_bits[i:i+ns] )
			)
			for i in range(ns**2, len(reverse_bits), ns)
		]))


	@given(integers(), bioencodings())
	def test_encode(self, nucleotide_count, encoding):
		rand = pyna.random(nucleotide_count,
			output_flags = pyna.Flags.ALL,
			encoding = encoding
		)

		encoded_string = pyna.encode( rand["forward_binary"] )
		self.assertEqual( rand["forward_string"], encoded_string )

	@given(integers(), bioencodings())
	def test_decode(self, nucleotide_count, encoding):
		rand = pyna.random(nucleotide_count,
			output_flags = pyna.Flags.ALL,
			encoding = encoding
		)

		encoded_string = pyna.encode( rand["forward_binary"] )
		self.assertEqual( rand["forward_string"], encoded_string )


if __name__ == "__main__":
	unittest.main(verbosity=2)

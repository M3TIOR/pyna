#!/usr/bin/env python3

#
# M3TIOR 2018
#

from .errors import (

)

class Nucleotide(str):
	"""Nucleotide Type"""

	def __init__(self, name, sibling=None):
		# raise type errors at instanciation and optimize __str__ performance
		self.char = str(name[0]).upper()

		self.name = name # whatever we want the nucleotide represented by
		self.sibling = sibling # holder for our sibling refference

	def __str__(self):
		return self.name

	@staticmethod
	def couple(n1, n2):
		""" Creates and returns two sibling nucleotides."""
		# make two new nucleotides
		brother = Nucleotide(n1)
		sister = Nucleotide(n2)

		# make the two siblings
		brother.sibling = sister
		sister.sibling = brother

		return (brother, sister) # return them in order

	@staticmethod
	def standard():
		"""
			Group of standard nuclotides with their pairs in DNA/RNA
		"""
		adenine = Nucleotide("Adenine")
		cytosine = Nucleotide("Cytosine")
		guanine = Nucleotide("Guanine")
		uracil = Nucleotide("Uracil")
		thymine = Nucleotide("Thymine")

		# return a dictionary containing the nucleotides by name
		return {
			nucleotide.char:nucleotide for nucleotide in [
				adenine, cytosine, guanine, uracil, thymine
			]
		}

class BioEncoding():
	"""
		Base class for implementing bitwise nucleotide encodings
	"""

	def __init__(self, n1, n2, n3, n4):
		# positional args enforce strictness

		# NOTE:
		#	Make a copy of the input variables instead of using them
		#	in place just in case someone decides to create two different
		#	bioencodings with the same nucleotides.
		#
		#	This is also a read only data structure
		self._nucleotides = [n1, n2, n3, n4] # carry out strict indexing

		for n in self._nucleotides:
			# make sure our nucleotides don't have their siblings out of bounds
			# otherwise we can't ensure the validity of our executable encoding
			# and we also can't verify that translations are made properly
			# between two encodings
			if n.sibling not in self._nucleotides:
				raise BindingError(n, "sibling does not exist locally to the encoding!")

		# pre-allocate keys, storage and executable values (optimization)
		self._keys = [n1.char, n2.char, n3.char, n4.char]# designate keys
		self._bin = self._exval()# designate executable values

	def _exval(self):
		values = [] # define a list container for our output values
		pairs = [] # define a container for our pairs
		found = [] # so we don't have repeat pairs

		for n in self._nucleotides:
			if n not in found:
				# add pairs to list so we can binary search
				# NOTE: there will only ever be two
				pairs.append([str(n), str(n.sibling)])

				# add pair to the found values list
				found.append(str(n))
				found.append(str(n.sibling))

		# then we loop through our keys, because they are both:
		#	in the alignment we need our output values to be in,
		#	and they're already in the format we need to check agains
		for key in self.keys():

			# if our key belongs to the first pair, make it's value zero
			if key in pairs[0]:
				values.append(0)
			else:
				# if our key is in the second pair, make it's value one
				values.append(1)

		# the result is a one way binary encoding
		return values

	def __len__():
		return 4

	def get_key(self, index):
		""" Returns the key value of the given index """
		return self._keys[index]

	def get_quadernary(self, key):
		""" Returns the quaternary value of the input key. """
		return self._keys.index(key)

	def get_binary(self, key):
		""" Returns the binary value of a key's family. """
		return self._bin[self._keys.index(key)]

	def compliment_key(self, ikey):
		""" Returns the complimentary nucleotide key for 'ikey'"""
		return self._nucleotides[self._keys.index(ikey)].sibling.char

	def compliment_quadernary(self, key):
		""" Returns the complimentary nucleotide quadernary for 'key'"""
		return self._nucleotides.index(
			self._nucleotides[
				self._keys.index(ikey)
			].sibling
		)

	def compliment_binary(self, key):
		""" Returns the complimentary nucleotide binary for 'key'"""
		return self._bin[
			self._nucleotides.index(
				self._nucleotides[
					self._keys.index(ikey)
				].sibling
			)
		]

	def as_bytes():
		"""
			Returns the encoding object's bytecode representation.
		"""
		pass

	@staticmethod
	def DNA():
		"""
			Base class for implementing DNA translation
		"""
		# A pairs with G
		# C pairs with T
		#
		# so the resulting encoding, when compensating for
		# base pair compression looks like this.
		#
		# Well, that or it's inverse G & C == 1, A && T == 0
		#
		# Needs DNA raw dna comparison to validate.
		n = Nucleotide.standard()
		return BioEncoding(n["G"],n["C"],n["A"],n["T"])

	@staticmethod
	def RNA():
		"""
			Bitwise encoding for Ribonucleic Acid
		"""
		# There are a lot of combonations here. Which realistically should all be
		# tested against an actual rna sample from a living cell.
		#
		# However, if my hypothesis about DNA being bytecode is correct; this
		# shouldn't matter, as it would just need to be a constant medium for
		# storing the nucleotide sequence in a more compact form factor.
		n = Nucleotide.standard()
		return BioEncoding(n["G"],n["C"],n["A"],n["U"])


class Strand():
	pass

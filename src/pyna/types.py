#!/usr/bin/env python3

#
# M3TIOR 2018
#

# import function declarator contracts for testing
from dpcontracts import ( require, ensure, invariant )

# import local module necessities
from .errors import ( NucleotideError, BioEncodingError )

from copy import copy, deepcopy

@invariant("sibling should always be a nucleotide",
		lambda args: isinstance(args.self, Nucleotide))
class Nucleotide():
	""" An object representing a nucleotide inside DNA or RNA.

	Mimics the macroscopic function of a nucleotide taken from within the
	double helix mollecule, DNA; and partner mollecule, RNA.

	Args:
		name (str): The name of the new nucleotide.
		sibling (:obj:`Nucleotide`): Initial partner nucleotide for the new
			object, defaults to None.

	Attributes:
		char (str): The first character of the name attribute uppercase.
		name (str): The name of the nucleotide.
		sibling (:obj:`Nucleotide`): The partner nucleotide when paired,
			defaults to None.
	"""
	@require("`name` must be a string", lambda args: isinstance(args.name, str))
	@require("`name` string must not be empty", lambda args: len(args.name) > 0)
	@require("`sibling` must be None or Nucleotide",
			lambda args: isinstance(args, Nucleotide) or isinstance(args, None))
	def __init__(self, name):
		# raise type errors at instanciation for bad name input types
		# TODO:
		#	remove internal character storage and use dynamic key selector
		#	in the BioEncoding class upon instanciation.
		#
		#	NOTE: TO SELF...
		#		I forgot to ensure all string variants could be used within
		#		the BioEncoding class and this method means we could have
		#		overlaps in the nucleotide names and bad output when
		#		bioencodings contain nucleotides with nested names. IE:
		#			Adenine, denine, nine < would have 2 overlaps
		#		or even worse, the short key lookup would get corrupted:
		#			Adenine, Adeni, Apple, Appricot < would break the encoder!
		self.char = name[0].upper()
		self.name = name # whatever we want the nucleotide represented by

		# initalize placeholder for the sibling, XXX: this breaks dpcontracts
		# if not set...
		self.sibling = None

	def __str__(self):
		return self.name

	@require("`sibling` must be a Nucleotide",
			lambda args: isinstance(args.sibling, Nucleotide))
	def pair(self, sibling):
		""" Pairs the current nucleotide with `sibling`.

		Args:
			sibling (Nucleotide): The new partner of the current nucleotide.
		"""
		if self.sibling != None:
			# if we have a sibling, we need to disconnect it before
			# rebinding with a new sibling.
			self.sibling.sibling = None

		# pointer.to_that.to_this
		self.sibling = sibling
		self.sibling.sibling = self

	@require("n1, and n2 must be strings",
			lambda args: isinstance(args.n1, str) and isinstance(args.n2, str))
	@ensure("output must be a two value tuple",
			lambda args, result: isinstance(result, tuple) and len(result) == 2)
	@ensure("output must only contain Nucleotides",
			lambda args, result: isinstance(result[0], Nucleotide) and
								isinstance(result[1], Nucleotide))
	@ensure("both Nucleotides must be siblings",
			lambda args, result: args.n1.sibling == args.n2 and
								args.n2.sibling == args.n1)
	@staticmethod
	def couple(n1, n2):
		""" Creates and returns two paired nucleotides.

		Args:
			n1 (str): The name of the first nucleotide.
			n2 (str): The name of the second nucleotide.
		"""
		# make two new nucleotides
		brother = Nucleotide(n1)
		sister = Nucleotide(n2)

		# make the two siblings
		brother.pair(sister)

		return (brother, sister) # return them in order

	@staticmethod
	def standard():
		""" Creates and returns a dictionary of nucleotides representing
		those which formally compose both DNA and RNA molecules.

		Note:
			Nucleotides returned by this method are not bound by default
			because they are reused between molecules, and pairing them
			could cause conflicts durring later use.

		Returns:
			(:obj:`dict` of :obj:`Nucleotide`): A dictionary containing the
				virtual nucleotide equivalents of *Adenine*, *Guanine,
				*Cytosine*, *Thymine*, and *Uracil*.
		"""
		adenine = Nucleotide("Adenine")
		cytosine = Nucleotide("Cytosine")
		guanine = Nucleotide("Guanine")
		uracil = Nucleotide("Uracil")
		thymine = Nucleotide("Thymine")

		# return a dictionary containing the nucleotides by name
		return {
			nucleotide.short_name:nucleotide for nucleotide in [
				adenine, cytosine, guanine, uracil, thymine
			]
		}

@invariant("must always have one nucleotide pair per encoding",
		lambda self: len(self._nucleotides) > 1)
class BioEncoding():
	""" Mimics the storage function of DNA and RNA molecules by using
	a one-to-one integer translation per individual Nucletide of each Molecule.

	Args:
		*args (:obj:`Nucleotide`): The nucleotides used to preserve information
			contained within the encoding.
		long (:obj:`bool`, optional): The long name keyword argument, when true,
			toggles the use of long nucleotide encodings. When long Nucleotides
			are on, the resulting encoding will use the nucleotides names in
			place of their identifier characters.

			ex: ``AdenineThymineAdenineGuanineCytosine`` in place of ``ATAGC``.
	"""

	@require("must be supplied with more than one nucleotide",
			lambda args: len(args.nucleotides) > 1 )
	@require("long flag must be a boolean value",
			lambda args: isinstance(args.long, bool))
	@require("positional arguments must only be nucleotides",
		lambda args: all(isinstance(n, Nucleotide) for n in args.nucleotides))
	@ensure("all nucleotides must be bound within the encoding",
		lambda args, result:
			all(n.sibling in result._nucleotides for n in result._nucleotides))
	def __init__(self, *nucleotides, long=False):
		# positional args enforce strictness

		# This is a read only data structure, contain the nucleotides in order.
		self._nucleotides = nucleotides # carry out strict indexing

		# pre-allocate keys, paired values (optimization)
		# designate keys
		if long:
			self._keys = [n.name for n in nucleotides]
		else:
			self._keys = [n.char for n in nucleotides]
		# # designate paired values
		self._paired = self._paired_values() # it looks cleaner in a subroutine

	def __len__(self):
		return len(self._nucleotides)

	@ensure("""result must be a list of values,
			who's sum is equal to the encoding's nucleotide count""",
			lambda args, result: sum(result) == len(args.self))
	def _paired_values(self):
		""" Returns a list of values and keys, where each
			pair of keys is assigned the same value. """
		# make a container list the same size as our nucleotide count
		values = [ None for n in range(0, len(self._nucleotides)) ]
		pairs = 0 # add a counter to track the LVC value for each pair

		# per each unique nucleotide
		for n in range(0, len(self._nucleotides)):
			# we make sure we haven't already set it's value
			if not values[n]:
				# when we don't already have a value for the nucleotide
				# we assign it a new value using the LVC counter
				values[n] = pairs
				# and assign it's sibling as well. When this is passed over
				# again by the loop it will just be skipped since it already
				# has a value.
				values[ self._nucleotides.index(
						self._nucleotides[n].sibling) ] = pairs
						# target the sibling memory location by using
						# it's nucleotide index and assign it the same
						# value as it's partner.

				pairs += 1 # increment the LVC counter

		# then return our pair value populated list
		return values

	def as_bytes():
		""" Returns a bytes object representing the encoding as bytecode. """
		pass

	@require("`value` must be an int", lambda args: isinstance(args.value, int))
	def get_key(self, value):
		""" Retrive and return the nucleotide key equivalent of `value`.

		Args:
			value (str): The target encoded nucleotide's value.
		"""
		return (self._keys[value])

	@require("`key` must be a string", lambda args: isinstance(args.key, str))
	def get_value(self, key):
		""" Retrive and return the nucleotide value equivalent of `key`.

		Args:
			key (str): The character representing the target encoded nucleotide
				value. When long mode is enabled, this will be the nucleotide's
				name instead.
		"""
		# since the nucleotide values are equal to their positions
		# when passed into the new encoding instance, we just return
		# the index for the input key/identifier
		return self._keys.index(key)

	def get_paired_value(self, target):
		""" Retrieve and return the target nucleotides associated pair value.

		Args:
			target (:obj:`object`): The nucleotide we're retrieving the paired
				value of.

				When target is a string, the nucleotide's indentifier key is
				used to find it's associated pair's value.

				When target is an interger, the nucleotide's value is used to
				find it's associated pair's value.
		"""
		if isinstance(target, str):
			# grab the paired value using the key's index same as value.
			return self._paired[self._keys.index(target)]
		elif isinstance(target, int):
			# raw index list refference.
			return self._paired[target]
		else:
			raise TypeError(target, "expected str or int, got: "+typeof(target))

	def get_paired_keys(self, target):
		""" Retrieve and return the target nucleotides associated pair of keys.

		Args:
			target (:obj:`object`): The nucleotide we're retrieving the paired
				value of.

				When target is a string, the nucleotide's indentifier key is
				used to find it's associated pair of keys.

				When target is an interger, the nucleotide's value is used to
				find it's associated pair of keys.
		"""
		if isinstance(target, str):
			# grab the paired value using the key's index same as value.
			return ( target, self.compliment_key(target) )
		elif isinstance(target, int):
			# raw index list refference.
			return ( self._keys[target],
				self.compliment_key( self._keys[target] ) )
		else:
			raise TypeError(target, "expected str or int, got: "+typeof(target))

	def compliment_key(self, target):
		""" Retrieve and return the key of the target nucleotide's partner.

		Args:
			target (:obj:`object`): The nucleotide who's sibling's key we're
				retrieving.

				When target is a string, the nucleotide's indentifier key is
				used to find it's sibling's key.

				When target is an interger, the nucleotide's value is used to
				find it's sibling's key.
		"""
		if isinstance(target, str):
			# use the key indexing method to get the appropriate nucleotide
			# then index the nucleotide's sibling to get the appropriate key
			# index.
			return (self._keys[ self._nucleotides.index(
					self._nucleotides[ self._keys.index(target) ].sibling )])
		elif isinstance(value, int):
			# less complicated but basically the same as above. (direct index)
			return (self._keys[ self._nucleotides.index(
					self._nucleotides[ target ].sibling )])
		else:
			raise TypeError(target, "expected str or int, got: "+typeof(target))

	def compliment_value(self, target):
		""" Retrieve and return the key of the target nucleotide's partner.

		Args:
			target (:obj:`object`): The nucleotide who's sibling's value we're
				retrieving.

				When target is a string, the nucleotide's indentifier key is
				used to find it's sibling's value.

				When target is an interger, the nucleotide's value is used to
				find it's sibling's value.
		"""
		# same as in compliment_key method, just return the key's index instead.
		# :P "SIMPLE"
		if isinstance(target, str):
			# We don't need to protect the return here since the index function
			# already returns a value not a pointer
			return self._nucleotides.index(
				self._nucleotides[ self._keys.index(target) ].sibling )
		elif isinstance(target, int):
			return self._nucleotides.index(
				self._nucleotides[ target ].sibling )
		else:
			raise TypeError(target, "expected str or int, got: "+typeof(target))

	def nucleotides(self):
		return copy(self._keys)

	@staticmethod
	def DNA(long=False):
		""" Deoxyribonucleic Acid (DNA) encoding """
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
		n["G"].pair(n["C"])
		n["A"].pair(n["T"])
		return BioEncoding(n["G"],n["C"],n["A"],n["T"], long=long)

	@staticmethod
	def RNA(long=False):
		""" Ribonucleic Acid (RNA) encoding """
		# There are a lot of combonations here. Which realistically should all be
		# tested against an actual rna sample from a living cell.
		#
		# However, if my hypothesis about DNA being bytecode is correct; this
		# shouldn't matter, as it would just need to be a constant medium for
		# storing the nucleotide sequence in a more compact form factor.
		n = Nucleotide.standard()
		n["G"].pair(n["C"])
		n["A"].pair(n["U"])
		return BioEncoding(n["G"],n["C"],n["A"],n["U"], long=long)

#!/usr/bin/env python3

#
# M3TIOR 2018
#


class Nucleotide():
	"""Nucleotide Type"""

	def __init__(self, name, transient=False):
		# raise type errors at instanciation and optimize __str__ performance
		self.char = str(name[0])

		self.name = name # whatever we want the nucleotide represented by
		self._transient = bool(transient) # the nucleotide that should be swapped
		self._sibling = None # holder for our sibling refference

	def __str__(self):
		return str(self.char)

	def pair(self, sibling, rebind=False):
		if self._transient:
			# transient nucleotides are exempt from BindingErrors. Since
			# they can swap places with their other transients, they are
			# allowed to have the same foster siblings as other transients
			if sibling._transient:
				# but two transients cannot be siblings
				raise BindingError(sibling, "Two transient nucleotides cannot be siblings.")
			sibling.pair(self, rebind=True)
		else:
			if (sibling.sibling() != None or self._sibling != None) and not rebind:
				raise BindingError(self.pair, "Nucleotide \""+str(self)+"\" already has a sibling.")

			self._sibling = sibling
			self._sibling._sibling = self

	def sibling(self):
		return self._sibling

	def is_transient(self):
		return self._transient

	@staticmethod
	def couple(n1, n2, transient=0):
		""" Creates and returns two sibling nucleotides.

			When transient is set to below zero, the first sibling, n1 is
			set to be transient, when transient is greater than one,
			n2 is transient. Otherwise neither sibling will be transient.
		"""
		# make two new nucleotides
		brother = Nucleotide(n1,
			transient=True if transient < 0 else False
		)
		sister = Nucleotide(n2,
			transient=True if transient > 0 else False
		)
		brother.pair(sister) # make the two siblings

		return (brother, sister) # return them

	@staticmethod
	def standard():
		"""
			Group of standard nuclotides with their pairs in DNA/RNA
		"""
		adenine = Nucleotide("Adenine")
		cytosine = Nucleotide("Cytosine")
		guanine = Nucleotide("Guanine")
		uracil = Nucleotide("Uracil")
		thymine = Nucleotide("Thymine", transient=True)

		# uracil and thymine are both transient and bound to adenine
		uracil.pair(adenine)
		thymine.pair(adenine)

		# guanine only pairs with cytosine
		guanine.pair(cytosine)

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

	def __init__(self, n1, n2, n3, n4, standby=None, executable=False):
		# positional args enforce strictness

		# encodings don't need a transient
		self._hastransient = -1 # but if we have one, there must only be one.
		self._isexecutable = executable # toggle storage vs executable encoding
		self._swap= ( standby if isinstance(standby, Nucleotide) else None )

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
			if n.sibling() not in self._nucleotides:
				# we need to skip single nucleotides with a transient however,
				# since if we find their transient sibling within the nucleotide
				# both will be valid anyway.
				if not n.sibling().is_transient():
					raise BindingError(n, "sibling does not exist locally to the encoding!")

			if n.is_transient():
				# then we have to make sure we don't accidentally have more than
				# one transient member, otherwise when we do translations,
				# we won't be able to validate which nucleotides get rotated
				if self._hastransient < 1:
					self._hastransient = self._nucleotides.index(n)
				else:
					raise BindingError(n, "encodings cannot have more than one transient nucleotide")

				# Don't forget to rebind the transient's sibling so if it exists
				# within this encoding, the two will be paired.
				n.sibling().pair(n, rebind=True)

			# then bind the values of our nucleotides
			self._set_type()

	def __getitem__(self, key):
		return self._values[self.keys().index(key)] # psudo inhertiance

	def _set_type(self):
		if self._isexecutable:
			values = [] # define a list container for our output values
			pairs = [] # define a container for our pairs
			found = [] # so we don't have repeat pairs

			for n in self._nucleotides:
				if n not in found:
					# add pairs to list so we can binary search
					# NOTE: there will only ever be two
					pairs.append([str(n), str(n.sibling())])

					# add pair to the found values list
					found.append(str(n))
					found.append(str(n.sibling()))

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
			self._values = values
		else:
			# otherwise it's a storage encoding and we just do linear assignment
			self._values = [v for v in range(0,4)]

	def keys(self):
		# XXX:
		# 	don't let someone accidentally modify an internal value
		# 	because of how variable refferences work in python. :P
		return [str(n) for n in self._nucleotides]

	def values(self):
		return self._values # quote XXX note above

	def compliment(self):
		# get the nucleotide corresponding to "key" and get it's siblings key
		return {
			self._nucleotides[self._keys.index(key)]._sibling.char:
			self[self._nucleotides[self._keys.index(key)]._sibling.char]
			for key in self._keys()
		}

	def switch(self, silent=False, allow_no_swap=False):
		if self.can_change_type() or (
					True if allow_no_swap and self._swap == None else False):
			# change type signature
			self._isexecutable = not self._isexecutable

			# rotate last transient out and swap it with our standby
			next = self._swap
			self._swap = self._nucleotides[self._hastransient]
			self._nucleotides[self._hastransient] = next

			# don't forget to rebind our swapped sibling
			next.pair(self._swap.sibling())

			# change over the values
			self._set_type()

			# completed successfully
			return True
		elif silent:
			return False
		else:
			raise BioEncodingError(self, "can't switch type without a transient and swap")

	def can_change_type(self):
		return ( True if self._hastransient > -1 and self._swap else False )

	def is_executable(self):
		return copy(self._isexecutable) # quote XXX note above

	def is_storage(self):
		return not self._isexecutable

	def as_bytes():
		"""
			Returns the encoding object's bytecode equivalent.
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
		return BioEncoding(
			n["G"],n["C"],n["A"],n["T"],

			standby=n["U"],
			executable=True
		)

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
		return BioEncoding(
			n["G"],n["C"],n["A"],n["U"],

			standby=n["T"],
			executable=False
		)

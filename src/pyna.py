#!/usr/bin/env python3

#
# M3TIOR 2018
#
# This is a small internal research library. Meant to help my brain work
# through a hypothesis I've recently developed regarding the use of dna within
# micro-organisms.
#
# Basically, I'm a weird person, and by weird, I mean I'm constantly attempting
# to find ways to disprove the existence of a god or many gods. It's a component
# of my rebellion against higher powers, or puppeteers as I see them. And my
# rejection of the ideology behind their fabrication. I hate religions because
# so many have a lack of regard for logic, and they are prone to descrimination.
# A lack of logic is that oozing, bubbling, puss which errupts from the giant
# bulbous form of a corruption zit. A clear identifier of one's dissregard for
# cleansing truth and clearification in a world filled with filthy lies and
# missinformation.
#
# Getting to the point, one of the quotes I remember the most from being raised
# into a Seventh Day Adventist household was that God created us in his image.
# A thought that I'd been quick to dissregard in the past. But I'm forced to ask
# myself:
#
# What if DNA is bytecode?
#
#


from copy import copy

version = "0.0.1" # main,beta,alpha-hotfix

class Error(Exception):
	"""Base class for implementing errors in this library

	Attributes:
		message -- description of the error
		expression -- the expression where the error occurred.
	"""
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

class NucleotideError(Error):
	""" Errors that arise because of conflicts with Nucleotides """
	pass

class BindingError(NucleotideError):
	""" Raised when attempting to pair a nucleotide that already has a sibling
		or when a transient tries to pair itself with another transient"""
	pass

class BioEncodingError():
	""" Errors raised from problems with BioEncodings """
	pass

class ExecutableError(BioEncodingError):
	""" An error that is raised when attempting to encode with an executable BioEncoding"""
	# XXX:
	#	DNA cannot be encoded. The mollecule's format simply can't be
	#	interpreted as quadernary; when it's structure, via the existence of
	#	matching base pairs opposite each nucleotide, imply that
	#	that each nucleotide pair instead represents a binary signal, on or off.
	#	Since otherwise, the resulting encoding would be identical to that of its
	#	RNA counterpart. Which wouldn't make any sense. Especially considering that
	#	RNA is only used for transcription and storage with in cells
	#
	#	I could have the functions of DNA and RNA backwards, but for now, this is
	#	the hypothesis I'm running with.
	#
	#	So when DNA is being executed / read, having to read both of it's sides
	#	individually would be inefficient. This isn't to say that I think a
	#	rudimentary organism is smart enough to optimize itself, but perhaps to say
	#	that adding redundancy to the most simple form of life seems like overkill.
	#
	#	Hence the addition of the executable vs storage encoding types
	pass

class TranslationError(BioEncodingError):
	""" Exceptions raised durring BioEncoder translation.

	Attributes:
		message -- description of the error
		previous -- the previously translated nucleotide character
		nucleotide -- the character value for the targeted translation
		binding -- the target translation for said nucleotide, otherwise None
	"""
	def __init__(self, previous, next, binding, message):
		self.previous = previous
		self.next = next
		self.binding = binding
		self.message = message



class Nucleotide():
	"""Nucleotide Type"""

	def __init__(self, name, transient=False):
		# raise type errors at instanciation and optimize __str__ performance
		self.char = str(value[0])

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
			if (sibling.sibling() not None or self._sibling not None) and not rebind:
				raise BindingError(self.pair, "Nucleotide \""self+"\" already has a sibling.")

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
		self._swap= ( None if not isinstance(standby, BioEncoding) else standby)

		# NOTE:
		#	Make a copy of the input variables instead of using them
		#	in place just in case someone decides to create two different
		#	bioencodings with the same nucleotides.
		#
		#	This is also a read only data structure
		self._nucleotides = [n1, n2, n3, n4] # carry out strict indexing
		self._keys = [str(n) for n in self._nucleotides]

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
				if not self.has_transient:
					self.has_transient = self._nucleotides.index(n)
				else:
					raise BindingError(n, "encodings cannot have more than one transient nucleotide")

				# Don't forget to rebind the transient's sibling so if it exists
				# within this encoding, the two will be paired.
				n.pair(n.sibling(), rebind=True)

			# then bind the values of our nucleotides
			self._set_type()

	def __getitem__(self, key):
		return copy(self._values[self._keys.index(key))) # psudo inhertiance

	def _set_type():
		if self.isexecutable:
			values = [] # define a list container for our output values
			pairs = [] # define a container for our pairs
			found = [] # so we don't have repeat pairs

			for n in self._nucleotides:
				if n not in found:
					# add pairs to list so we can binary search
					# NOTE: there will only ever be two
					pairs.append((str(n), str(n.sibling())))

					# add pair to the found values list
					found.append(str(n))
					found.append(str(n.sibling()))

			# then we loop through our keys, because they are both:
			#	in the alignment we need our output values to be in,
			#	and they're already in the format we need to check agains
			for key in self._keys():

				# if our key belongs to the first pair, make it's value zero
				if key in pairs[0]:
					values.append(0)

				# if our key is in the second pair, make it's value one
				if key in pairs[1]:
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
		return copy(self._keys)

	def values(self):
		return copy(self._values) # quote XXX note above

	def compliment(self):
		# get the nucleotide corresponding to "key" and get it's siblings key
		return {
			self._nucleotides[self._keys.index(key)]._sibling.char:
			self[self._nucleotides[self._keys.index(key)]._sibling.char]
			for key in self._keys()
		}

	def compliment_value(self, key):

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
			next.sibling().pair(next)

			# change over the swapped key
			self._keys[self._keys.index(self._swap.char)] = next.char

			# change over the values
			self._set_type()

			# completed successfully
			return True
		elif not silent:
			return False
		else:
			raise BioEncodingError(self, "can't switch type without a transient and swap")

	def can_change_type(self):
		return ( True if self._transient > -1 and self.swap else False )

	def is_executable(self):
		return copy(self._isexecutable) # quote XXX note above

	def is_storage(self):
		return not self._isexecutable

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

			swap=n["U"],
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

			swap=n["T"],
			executable=False
		)


class BioReader():
	"""
		A class for decoding nucleotide sequences
	"""

	def __init__(self, file, encoding, flip=False, head=False):
		self.file = file
		self.encoding = encoding
		self.flip = flip
		self.head = head

	def write(self, bytes):
		pass

class BioWriter():
	"""
		A class for dispensing encoded nucleotide sequences to files
	"""

	def __init__(self, file, encoding, flip=False, head=False):
		self.file = file
		self.encoding = encoding
		self.flip = flip
		self.head = head

def encode(bytes, encoding, flip=False, head=False):
	"""
		Converts a binary blob to a string of BioEncoded data.
	"""
	if encoding.is_executable():
		raise ExecutableError(encoding, "executable encodings cannot be encoded")


	raise NotImplementedError()

def decode(sequence, encoding, flip=False, head=False):
	"""
		Converts a string of BioEncoded data to a binary blob.
	"""
	if not isinstance(encoding, BioEncoding):
		raise TypeError(encoding, "encoding must be an instance of BioEncoding")
	if isinstance(sequence, bytes):
		sequence = str(sequence, encoding="utf-8")
	elif not isinstance(sequence, str):
		sequence = str(sequence)
	code = sequence.upper() # our input dna sequence
	obin = bytearray() # our output binary
	nucleobyte = 0 # each translated byte as an integer value
	chunk_size = 1 if encoding.is_executable() else 2
	chunks = 8 // chunk_size

	try:
		# Do if and try top level so they aren't being run every iteration
		# of the loop. Which would be inefficient.

		index = 0 				# index counter for byte rollover
		length = len(dna)		# get the length of our dna, cap read distance
		offset = chunks-( length % chunks )	# the amount of bits that remain to be filled
		inset = 0				# the amount of empty bits left before beginning transcription

		# To flip the binary translation we just use the product of a positive
		# or negative integer with our index to produce the correct,
		# directionally adjusted index position for our array.
		if flip:
			direction = -1

			# compensate for negative memory justification
			length += 1
			index += 1
			inset -= chunk_size
		else:
			direction = 1

		# here, we decide what to do if we have an incomplete byte
		if head:
			# if we have "head" set, we want to put the offset at the beginning
			inset += offset

		# for nucleotide in dna:
		while (index < length):

			# get nucleotide out of dna sequence
			nucleotide = code[ direction * index ]

			nucleobyte <<= chunk_size # move stored bits left by the chunk size
			nucleobyte |= int(encoding[nucleotide]) # append next bit to the right

			if (index*chunk_size+inset) % chunks == chunks - 1:
				# if we've just mapped the last bit in a byte
				obin.append(nucleobyte) # append byte to the right of or output
				nucleobyte = 0 # reset stored byte value to zero

			index += 1 # increment pointer

		if not head:
			# othewise, we want the offset put at the end, or a partial "tail"
			# append the final byte to the right of or output with padding
			obin.append(nucleobyte<<offset) # push left with right justification

	except(KeyError):
		raise TypeError(nucleotide, "Unrecognized Nucleotide - "+nucleotide+" at #"+index)

	return obin


def compliment_string(string, encoding):
	"""
		returns the inverse complement of the input string with BioEncoding
	"""
	from = encoding.keys()
	to = encoding.compliment().keys()
	output = ""
	for char in string:
		output += to[from.index(char)]
	return output

def compliment_binary(bytes, encoding, flip=False, head=False):
	"""
		returns the inverse complement of the input binary with BioEncoding
	"""
	raise NotImplementedError()

def translate_string(string, encoding_from, encoding_to):
	"""
		translates an encoded string from one BioEncoding to another
	"""
	raise NotImplementedError()

def translate_binary(bytes, encoding_from, encoding_to, flip=False, head=False):
	"""
		translates a binary blob from one BioEncoding to another
	"""
	raise NotImplementedError()

if __name__ == "__main__":
	import argparse
	raise NotImplementedError()

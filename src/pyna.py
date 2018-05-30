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
# A thought I'd been quick to dissregard in the past. But I'm forced to ask
# myself:
#
# What if DNA is bytecode?
#
#

from enum import Enum, IntEnum

class Nucleotides(Enum):
	Adenine = 'A'
	Cytosine = 'C'
	Guanine = 'G'
	Uracil = 'U'
	Thymine = 'T'

class NucleoEncoding(IntEnum):
	"""
		Base class for implementing bitwise nucleotide encodings
	"""
	pass

class DNAEncoding(NucleoEncoding):
	"""
		Bitwise encoding for Deoxyribonucleic Acid
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
	G = 0
	C = 0
	A = 1
	T = 1

class RNAEncoding(NucleoEncoding):
	"""
		Bitwise encoding for Ribonucleic Acid
	"""
	# There are a lot of combonation here. Which realistically should all be
	# tested against an actual rna sample from a living cell.
	#
	# However, if my hypothesis about DNA being bytecode is correct; this
	# shouldn't matter, as it would just need to be a constant medium for
	# storing the nucleotide sequence in a more compact form factor.
	G = 0
	C = 1
	A = 2
	U = 3


#DNA = ['g','c','a','t']
#RNA = ['g','c','a','u']


# XXX:
#	DNA cannot be compressed. The mollecule's format simply can't be
#	interpreted as quadernary; when it's structure, via the existence of
#	matching base pairs opposite each nucleotide, imply that
#	that each nucleotide pair instead represents a binary signal, on or off.
#	Since otherwise, the resulting encoding would be identical to that of its
#	RNA counterpart. Which wouldn't make any sense. Especially considering that
#	RNA's only use, is transcription.
#
#	So when DNA is being executed / read, having to read both of it's sides
#	individually would be inefficient. This isn't to say that I think a
#	rudimentary organism is smart enough to optimize itself, but perhaps to say
#	that adding redundancy to the most simple form of life seems like overkill.
#
# NOTE: this assumes that the input encoding is text left to right
def dna2bytes(dna, encoding=DNAEncoding, flip=False, head=False):
	"""
		Converts a string of encoded dna to a binary blob.
	"""
	map = encoding.__dict__ # rebinding of enum to dictionary for easy ref
	dna = dna.upper() # our input dna sequence
	obin = bytearray() # our output binary
	nucleobyte = 0 # our translated byte as an integer value

	try:
		# Do if and try top level so they aren't being run every iteration
		# of the loop. Which would be inefficient.

		index = 0 				# index counter for byte rollover
		length = len(dna)		# get the length of our dna, cap read distance
		offset = length % 8		# the amount of bits that remain to be filled

		# To flip the binary translation we just use the product of a positive
		# or negative integer with our index to produce the correct,
		# directionally adjusted index position for our array.
		if flip:
			direction = -1
		else:
			direction = 1

		# here, we decide what to do if we have an incomplete byte
		if head:
			# if we have "head" set, we want to put the offset at the beginning
			index += 8-offset

		# for nucleotide in dna:
		while (index < length):

			# get nucleotide out of dna sequence
			nucleotide = dna[ direction * index ]

			nucleobyte <<= 1 # move stored bits left 1
			nucleobyte |= int(map[nucleotide]) # append next bit to the right

			if index % 8 == 7: # if we've just mapped the last bit in a byte
				obin.append(nucleobyte) # append byte to the right of or output
				nucleobyte = 0 # reset stored byte value to zero

			index += 1 # increment pointer

		if not head:
			# othewise, we want the offset put at the end, or a partial "tail"
			# append the final byte to the right of or output with padding
			obin.append(nucleobyte<< (8-offset)) # push left with right justification

	except(KeyError):
		raise TypeError("Broken Nucleotide Sequence: Unrecognized Nucleotide - "+char+" at #"+index)

	return obin


def crna2bytes(bytes,
					rna_encoding=RNAEncoding,
					dna_encoding=DNAEncoding):
	"""
		A more optimal implementation of rna > dna > binary encoding,
		converting directly from compressed rna to binary.
	"""
	raise NotImplementedError()

def compress_rna(string, encoding=RNAEncoding):
	raise NotImplementedError()

def decompress_rna(bytes, encoding=RNAEncoding):
	raise NotImplementedError()

def dna2rna(string):
	raise NotImplementedError()

def rna2dna(string):
	raise NotImplementedError()

if __name__ == "__main__":
	import argparse
	raise NotImplementedError()

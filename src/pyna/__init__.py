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

version = "0.0.1" # main,beta,alpha-hotfix

from .types import (
	BioEncoding,
	Strand
)

from .errors import *

def encode_raw(inbytes, encoding=BioEncoding.DNA(), flip=False, phase=0):
	""" Converts a raw binary blob to a string of BioEncoded data. """

	if not isinstance(encoding, BioEncoding):
		raise TypeError(encoding, "encoding must be an instance of BioEncoding")

	if not isinstance(inbytes, bytes) and not isinstance(inbytes, bytearray):
		raise TypeError(inbytes, "input must be of type bytes or bytearray")

	outstring = "" # our output string
	n_char = 0 # each translated byte as a nucleotide character

	n_size = 2 # since encoding must be reversable, the input must be quadernary
	n_per_byte = 4 # 8//2 constant

	# NOTE: might implement early start and finish of loop
	#skip_n = phase % 4
	#skip_bytes = (phase - skip_n) // 4
	#skip_direction = -1 if phase < 0 else 1

	index = 0 # nucleotide counter
	n_index = 0 # define a place to store our nucleotide counter inside each byte

	byte_c = len(inbytes)# byte count


	# To flip the binary translation we just use the product of a positive
	# or negative integer with our index to produce the correct,
	# directionally adjusted index position for our array.
	if flip:
		# right to left
		direction = -1

		# compensate for negative memory justification
		byte_c += 1
		index += 1

		# if we flip the output, we need the farthest right two bits per byte
		mask = 3
		def shift(num, amount):
			# shift right to get bits from right to left
			return num >> amount
		def value(num, amount):
			# bits are already aligned for extraction, no need to undo shift
			return num

	else:
		# left to right (default character pointer increments to the right)
		direction = 1

		# by default we're always looking at the left two bits of each byte
		# since the default reading order is left to right, when we append
		# each character into the output string, it will be placed left to right
		mask = 192
		def shift(num, amount):
			# shift left to get bits from left to right
			return num << amount
		def value(num, amount):
			# bits are not properly aligned for extraction, so we need to undo
			# our previous shift.
			return num >> amount


	# for byte in blob:
	while ( index < byte_c ):

		# get the nucleotide container so we can start extracting them
		n_byte = inbytes[index * direction]
		n_byte_chars = "" # define somewhere to store them (just in case)

		# NOTE: possible different method, though it may be more expensive
		#		so I'm not adding it until I build a copy and test it against
		#		this one.
		#
		#while ( n < n_per_byte ):
		#	# DIAGRAM
		#	#    - 4 3 2 1 0 1 2 3 4 +
		#	#    >ltr             rtl<
		#	# %4   0 1 2 3 0 1 2 3 4
		#	# MX   0 1 2 3 4 5 6 7 8
		#	n_index = ( n * direction + n_per_byte ) % n_per_byte
		#	mask =| bit for bit in [ 2**i for i in range(0, n_per_byte) ]
		##
		# I lack experience with generators so I can't make this work yet
		# will investigate in the future

		# loop through each nucleotide per byte (container)
		for n in range(0, n_per_byte):

			# put the target bits of our byte in range to get filtered by
			# our mask
			target = shift(n_byte, (n_size * n))

			# filter out the value with our mask, and undo the positional
			# adjustment to retrieve our actual nucleotide value
			n_value = value((mask+1) + ~(mask & ~target))

			# add each encoded nucleotide to our temporary storage location
			# before we push it out just in case things go wrong.
			n_byte_chars += encoding.get_key(n_value)

		# finally append the new nucleotides on to our main string and reset
		outstring += n_byte_chars
		index += 1 # increment pointer

	# do phase adjustment post process to (hopefully) optimize it.
	# NOTE: haven't actually researched the internals of python3's array
	#		segment syntax yet.
	if phase < 0:
		return outstring[0, len(outstring)-phase]
	elif phase > 0:
		return outstring[phase, len(outstring)]
	else:
		return outstring

def decode_raw( sequence, encoding=BioEncoding.DNA(), flip=False, align_left=True, executable=False ):
	""" Converts a string of BioEncoded data to a raw binary blob. """

	if not isinstance(encoding, BioEncoding):
		raise TypeError(encoding, "encoding must be an instance of BioEncoding")

	if isinstance(sequence, bytes):
		sequence = str(sequence, encoding="utf-8")

	elif not isinstance(sequence, str):
		sequence = str(sequence)

	sequence = sequence.upper() # our input dna sequence
	outbytes = bytearray() # our output binary
	n_value = 0 # each translated byte as an integer value

	# each nucleotide is one bit in binary otherwise two in quadernary
	n_size = 1 if executable else 2 # we're decoding a binary when executable
	n_per_byte = 8 // n_size # adjust the byte to fit all our nucleotides

	# determine how we will get the value of each character from the input sequence
	value_of = encoding.get_binary if executable else encoding.get_quadernary

	# Do if and try top level so they aren't being run every iteration
	# of the loop. Which would be inefficient.
	index = 0 				# index counter for byte rollover
	length = len(sequence)	# get the length of our dna, cap read distance

	# the amount of bits that remain to be filled
	offset = n_per_byte - ( length % n_per_byte )
	inset = 0 # the amount of empty bits left before beginning transcription

	# To flip the binary translation we just use the product of a positive
	# or negative integer with our index to produce the correct,
	# directionally adjusted index position for our array.
	if flip:
		direction = -1

		# compensate for negative memory justification
		length += 1
		index += 1
		inset -= n_size # 1 * n_size
	else:
		direction = 1

	# here, we decide what to do if we have an incomplete byte
	if align_left:
		# if we have "head" set, we want to put the offset at the beginning
		inset += offset

	try:
		# for nucleotide in dna:
		while (index < length):

			# get nucleotide out of dna sequence
			n_char = sequence[ direction * index ]

			n_value <<= n_size # move stored bits left by the chunk size
			n_value |= value_of(n_char) # append next bits to the right

			if (index*n_size + inset) % n_per_byte == ( n_per_byte - 1 ):
				# if we've just mapped the last bit in a byte
				outbytes.append(n_value) # append byte to the right of or output
				n_value = 0 # reset stored byte value to zero

			index += 1 # increment pointer

		if not head:
			# othewise, we want the offset put at the end, or a partial "tail"
			# append the final byte to the right of or output with padding
			outbytes.append(n_value<<offset) # push left with right justification

	except(KeyError):
		raise NucleotideError(n_char, "Unrecognized Nucleotide - "+str(n_char)+" at #"+str(index))

	return outbytes

def encode():
	raise NotImplementedError()

def decode():
	raise NotImplementedError()


def compliment_string(string, encoding):
	"""
		returns the inverse complement of the input string with BioEncoding
	"""
	previous = encoding.keys()			# our list of input nucleotides
	new = encoding.compliment().keys()	# list of output nucleotides
	output = ""							# and somewhere to store the output

	try:
		for char in string:
			output += new[previous.index(char)]
	except(KeyError):
		raise NucleotideError(nucleotide, "Unrecognized Nucleotide - "+nucleotide+" at #"+index)

	return output

def compliment_binary(inbytes, encoding, remainder=0):
	"""
		returns the inverse complement of the input storage binary with BioEncoding "encoding"
	"""
	if not isinstance(encoding, BioEncoding):
		raise TypeError(encoding, "encoding must be an instance of BioEncoding")
	if not isinstance(sequence, bytes):
		raise TypeError(inbytes, "input must be of type 'bytes' or 'bytearray'")
	if encoding.is_executable():
		return inbytes

	previous = encoding.values() # our old values
	new = encoding.compliment().values() # our new chunk values

	ibin = inbytes # our input binary
	outbytes = bytearray() # our output binary
	new_n_byte = 0 # each translated byte as an integer value
	chunk_size = 1 if encoding.is_executable() else 2
	chunks = 8 // chunk_size

	try:
		# Do if and try top level so they aren't being run every iteration
		# of the loop. Which would be inefficient.

		index = 0 				# index counter for byte rollover
		length = len(code)		# get the length of our dna, cap read distance
		offset = chunks-( length % chunks )	# the amount of bits that remain to be filled
		inset = 0				# the amount of empty bits left before beginning transcription

		# NOTE:
		#	Since our input binary already has it's bits aligned where we want them,
		#	we only need to know where our empty bits are. So we only need the head
		#	attribute.
		direction = 1

		# here, we decide what to do if we have an incomplete byte
		if head:
			# if we have "head" set, we want to put the offset at the beginning
			inset += offset

		# for nucleotide in dna:
		while (index < length):

			# get nucleotide out of dna sequence
			nucleotide = code[ direction * index ]

			new_n_byte <<= chunk_size # move stored bits left by the chunk size
			new_n_byte |= int(encoding[nucleotide]) # append next bit to the right

			if (index*chunk_size+inset) % chunks == chunks - 1:
				# if we've just mapped the last bit in a byte
				outbytes.append(new_n_byte) # append byte to the right of or output
				new_n_byte = 0 # reset stored byte value to zero

			index += 1 # increment pointer

		if not head:
			# othewise, we want the offset put at the end, or a partial "tail"
			# append the final byte to the right of or output with padding
			outbytes.append(new_n_byte<<offset) # push left with right justification

	except(KeyError):
		raise NucleotideError(nucleotide, "Unrecognized Nucleotide - "+nucleotide+" at #"+index)

	return outbytes

def translate_string(string, encoding_from, encoding_to):
	"""
		translates an encoded string from one BioEncoding to another
	"""
	raise NotImplementedError()

def translate_binary(bytes, encoding_from, encoding_to, flip=False, head=False):
	"""
		translates a binary chunk from one BioEncoding to another
	"""
	raise NotImplementedError()

if __name__ == "__main__":
	import argparse
	raise NotImplementedError()

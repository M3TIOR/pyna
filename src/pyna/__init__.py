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

def encode_raw(inbytes, encoding, flip=False, phase=0):
	"""
		Converts a raw binary blob to a string of BioEncoded data.
	"""
	if encoding.is_executable():
		raise ExecutableError(encoding, "executable encodings cannot be raw encoded")


	raise NotImplementedError()

def decode_raw(sequence, encoding, flip=False, phase=0, executable=False):
	"""
		Converts a string of BioEncoded data to a raw binary blob.
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
		length = len(code)		# get the length of our dna, cap read distance
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
		raise NucleotideError(nucleotide, "Unrecognized Nucleotide - "+nucleotide+" at #"+index)

	return obin

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
	obin = bytearray() # our output binary
	nucleobyte = 0 # each translated byte as an integer value
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
		raise NucleotideError(nucleotide, "Unrecognized Nucleotide - "+nucleotide+" at #"+index)

	return obin

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

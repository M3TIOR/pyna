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
# *cough cough* Trying to be poetic.
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

import ctypes
import enum

from math import log2, floor
from random import randint

from dpcontracts import ( require, ensure )

from .types import ( BioEncoding )
from .errors import *

# Since the void_p in C is always cast to be the largest size the processor
# can handle, we can use that to save the constructor for the largest c_uint.
_cpu_max_bytes = ctypes.sizeof(ctypes.c_void_p) # avoids recalculation
"""int: Stores the max amount of bytes that the Operating System supports
per CPU register. Used for determining cache size in a few methods.
"""

# But first, we have to change that to bits.
_cpu_max_bits = _cpu_max_bytes * 8 # ditto last comment
"""int: Similar to the _cpu_max_bytes but instead stores the bits size."""

# And THEN we can grab the constructor...
_c_uint = getattr(ctypes,"c_uint"+str(_cpu_max_bits))
"""ctypes.c_uint*: The python ctypes library binding for the largest CPU
register type. Used to implement the cache in the decoder, encoder, and random
methods respectively.
"""

DNA = BioEncoding.DNA()
RNA = BioEncoding.RNA()

class Flags(enum.IntEnum):
	BITS_FORWARD_BINARY = 1
	BITS_FORWARD_STRING = 2
	BITS_REVERSE_BINARY = 4
	BITS_REVERSE_STRING = 8
	STRING = 10
	BINARY = 5
	BITS_FORWARD = 3
	BITS_REVERSE = 12
	ALL = 15

def _flip_bits_x(input, size=_cpu_max_bits):
	# I'm guessing by default, python probably uses the largest pointer type
	# for the given machine when casting an interger, since that's the case
	# on my machine. #to-lazy-to-look-at-source
	inval = input
	outval = 0
	for bit in range(0, size):
		outval <<= 1
		outval |= inval % 2
		inval >>= 1
	return outval

def _bit_mask(bits, right_offset):
	# must use the same internal size as our storage variable for proper mask
	# results.
	mask = 1
	for bit in range(1, bits):
		mask |= 2**bit
	return mask << right_offset

def _can_flip_bits_x_in_range(range):
	return log2( range+2 - ( range % 2 ) ).is_integer()

#def _bits_in(input):
#	return int( log2( input ) + 1 )

#def _bits_on_off(input, onoff):
#	count = 0
#	while

def _apply_mask(input, mask, mask_offset):
	mask <<= mask_offset
	# adjust output value by unshifting it
	return ( ~mask ^ ~( mask & ~input ) ) >> mask_offset

def _no_op(*n, **kwargs):
	return n[0]

@require("input must be a bytes object",
	lambda args: isinstance(args.input, bytes))
def encode(input, encoding=DNA, flip=False, phase=0, pair_expansion=False):
	""" Converts a raw binary blob to a string of BioEncoded data.

	Args:
		input (bytes): The input data we're encoding
		encoding (:obj:`BioEncoding`, optional): The interger encoding that will
			be used to translate the binary data.

			By default, this is set to ``BioEncoding.DNA()``.
		flip (:obj:`bool`, optional): When set, this flag flips the bits of the
			input data over it's X axis.

			By default, this flag is off, and data is output from left to right.
		phase (:obj:`int`, optional): The input bits that will be stripped
			from the output. When positive, strips bits off the front of the
			input. When negative, strips bits off the end of the input.

			Defaults to zero.
		pair_compression (:obj:`bool`, optional): When set, this flag attempts
			recovery of pair compressed data. To recover pair compressed data,
			the output strand has each value assigned randomly between its two
			respective sibling nucleotides.

	Examples:
		Assuming the input encoding is ``BioEncoding.DNA()``, (the default)
		you can do instant translation of binary to DNA::
			# when using raw binary input, by default, the bits are read left
			# to right.
			# 	ex: --> 10011111 00000010 00010001 00111011
			encode_raw(b'\x9F\x02\x11\x3B')
			# results in: "ACTTGGGAGCGCGTAT"

		In use cases where you'd like to flip the encoding::
			# if the flip flag is True, then our output encoding will be
			# flipped. In other words, it will be read right to left.
			# given the example:
			encode_raw(b'\x9F\x02\x11\x3B', flip=True)
			#	ex: 10011111 00000010 00010001 00111011 <--
			# would become...
			#	ex: 11011100 10001000 01000000 11111001
			#  and would result in: "TCTGATATCGGGTTAC"

		Sometimes, you'll have useless data added to the front or back of your
		binary that don't accurately represent the output BioEncoded data.
		For instance, when using encode_raw; if more than one nucleotide is
		packed into each byte of the encoding, in order to fit the data into a
		bytes object, you have to pad the remainder that doesn't fit completely.
		The result is a few empty bits either to the left or right of the output
		bytes object. This keyword exists to compensate for that::
			# when we have the phase keyword set, we'll strip values off the
			# output's beginning or end.
			#	ex: --> 10011111 00000010 00010001 00111011
			encode_raw(b'\x9F\x02\x11\x3B', phase=2)
			# results in: "TGCGCGAGGGTTCA"
		Warning: the applied trimming is not smart, so you can accidentally snip
		off usefull data if you aren't carefull.

		And if you want to use you're own encoding that's just fine too::
			# define custom encoding
			new_encoding = BioEncoding( # MEOW (lol, I'm a cat)
				*Nucleotide.pair("Mew", "Eternal"),
				*Nucleotide.pair("Ocelot", "Witch")
			)
			#	ex: --> 10011111 00000010 00010001 00111011
			encode_raw(b'\x9F\x02\x11\x3B', encoding=new_encoding)
			# results in: "OEWWMMMOMEMEMWOW"
	"""
	# INITIALIZE STORAGE VARS
	output = "" # our output stirng
	buffer = 0 # storage location for our nucleotides
	overflow = 0 # where we store our overflow input bits

	# INITIALIZE OUTPUT MODIFIERS
	unique_values = len(encoding) // ( 2 if pair_expansion else 1 )
	bits_per_n = int(log2( unique_values )) + 1 # get bit count
	input_bytes = len(input) # set the itteration count for our loop
	mask = _bit_mask(bits_per_n, 0) # the bit mask used to retrieve our elements


	# INITIALIZE TRACKING VARS
	buffer_index = 0 # byte read counter
	residual = 0 # bits in the overflow


	if unique_values > 2**(_cpu_max_bits/2):
		# Single and Double precision float point values both need at least
		# the first half of bits to opperate properly. Without this check,
		# the _can_flip_bits_ranged_x method may produce inappropriate results.
		# Even though there probably will never be more than 7 unique
		# nucleotides in the input encoding...
		#
		# Also, this helps in managing the buffer overflow!
		#
		# TODO: raise appropriate overflow / size related error
		raise Error()

	# make directional adjustments
	if flip:
		if not _can_flip_bits_x_in_range(unique_values - 1):
			# TODO: raise appropriate bit/value overflow error
			raise Error()

		direction = -1 # changes reading order
		flip_bits = _flip_bits_x # flips bits

		# add enough bytes that the buffer can opperate properly
		buffer_index += 1 + _cpu_max_bytes

		# add space on the end of our input to compensate for negative indexing
		input_bytes += 1

		if input_bytes < _cpu_max_bytes:
			# if the input is smaller than our buffer, make it the same size,
			# so we don't have to do anything funky outside of the normal loop

			tmp = bytearray(_cpu_max_bits - input_bytes) # make a holder array
			tmp.append(input) 	# add our input bits to the end since they'll
								#	flipped when our buffer reaches the end
								#	which will bring them to the front; right
								#	where we want them.

			input = tmp	# reset the input pointer to point at the new object
			input_bytes = _cpu_max_bytes 	# change the size to accommodate
											# other environmental factors.

			del tmp # finally, delete the now unused tmp variable binding
	else:
		direction = 1							# normal/LTR reading order
		flip_bits = _no_op						# dummy, doesn't flip bits

	if pair_expansion:
		# this was too big to fit in one line... (-_-)
		def retrieve(input):
			# randomly select one of the two keys for each compressed element.
			return encoding.get_paired_keys(input)[randint(0,1)]
	else:
		# return the appropriate key for each nucleotide
		def retrieve(input): return encoding.get_key(input)

	if phase > 0:
		buffer_index += phase // _cpu_max_bytes + 1
		residual = phase % 8

		buffer = input[ ( buffer_index - 1 ) * direction ]
		buffer = flip_bits(buffer) >> _cpu_max_bits - 8

		# pre-populate the overflow so we use the rest of the bits.
		overflow = _apply_mask(buffer, _bit_mask(residual,0), 0)
		overflow <<= _cpu_max_bits - residual
	elif phase < 0:
		input_bytes -= phase // _cpu_max_bytes + 1


	while ( buffer_index < input_bytes ):
		# populate our storage variable with as many input bits as possible
		byte_index = 0
		buffer = 0
		while ( buffer_index + byte_index < input_bytes
										and byte_index < _cpu_max_bytes ):
			buffer <<= 8 # push new byte into the buffer
			buffer |= input[ buffer_index * direction + byte_index ]
			byte_index += 1 # increment the local pointer.

		# flip the storage medium when applicable
		buffer = flip_bits(buffer)

		# NOTE:
		#	now directional adjustment is done, and we just have to work
		#	left to right within our buffer and extract nucleotide values

		# keep track of unused bits
		previous_residual = residual
		residual= ( residual + ( _cpu_max_bits % bits_per_n ) ) % bits_per_n

		# extract our next overflow bits off the right
		next_overflow = _apply_mask(buffer, _bit_mask(residual,0), 0)
		next_overflow <<= _cpu_max_bits - residual

		# push in the old unused bits onto the buffer to be cycled through
		buffer = ( buffer >> previous_residual ) & overflow

		overflow = next_overflow

		# loop through our stored bytes
		for n in range(0, _cpu_max_bits // bits_per_n):
			nucleotide_value = _apply_mask( buffer, mask,
				_cpu_max_bits - bits_per_n * (n + 1)
			)
			output += retrieve(nucleotide_value)

		# when we have a full nucleotide in the overflow, make sure to empty it.
		if residual // bits_per_n >= 1:
			# collect the new nucleotide
			nucleotide_value = _apply_mask( overflow, mask,
				_cpu_max_bits - bits_per_n * (n + 1)
			)
			# retrieve it's appropriate, human-readable representation
			output += retrieve(nucleotide_value)

			# adjust overflow to compensate for bit loss
			overflow <<= bits_per_n
			residual -= bits_per_n

		buffer_index += _cpu_max_bytes # increment buffer counter

	return output # finally, return our encoded nucleotides

def decode( sequence, encoding=BioEncoding.DNA(),
		flip=False, align_left=True, pair_compression=False):
	""" Converts a string of BioEncoded data to a raw binary blob. """
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
	#	Hence the addition of the pair_compression flag. When decoding using a
	#	BioEncoding with four nucleotides, pair compression results in a
	#	language that can be represented as synonymous with binary.
	#	This is where I draw my hypothesis. I believe that the nucleotide pairs,
	#	when being read from DNA represent binary signals that are read by the
	#	cell. I know this a pretty far fetched idea. But hey, It's something
	#	probably nobody's thought of till today right? maybe?
	#
	#	Aww, who gives a shit anyway...

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
	n_size = 1 if pair_compression else 2 # we're decoding a binary when executable
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

def random(nucleotide_count, output_flags=Flags.ALL, encoding=DNA):
	"""Generates random bioencoded data.

	Arguments:
		encoding (:obj:`pyna.BioEncoding` optional):
			The encoding used to generate the output data.


	Examples:

	"""
	unique_values = len(encoding)
	bits_per_n = int(log2(unique_values-1)) + 1
	output_bytes = floor( bits_per_n * nucleotide_count / 8 )
	buffer_chunks = output_bytes - (output_bytes % _cpu_max_bytes)
	phase = -(bits_per_n * nucleotide_count) % 8

	# consolidate bitwise opperations to booleans before use within the loop
	# (it's 1 less instruction per itteration)
	forward_binary = output_flags & Flags.BITS_FORWARD_BINARY
	forward_string = output_flags & Flags.BITS_FORWARD_STRING
	reverse_binary = output_flags & Flags.BITS_REVERSE_BINARY
	reverse_string = output_flags & Flags.BITS_REVERSE_STRING

	if unique_values > 2**(_cpu_max_bits/2):
		# Single and Double precision float point values both need at least
		# the first half of bits to opperate properly. Without this check,
		# the _can_flip_bits_ranged_x method may produce inappropriate results.
		# Even though there probably will never be more than 7 unique
		# nucleotides in the input encoding...
		#
		# Also, this helps in managing the buffer overflow!
		#
		# TODO: raise appropriate overflow / size related error
		raise Error()

	if (output_flags & Flags.BITS_REVERSE) and not _can_flip_bits_x_in_range(unique_values-1):
		# TODO: raise appropriate bit/value overflow error
		# NOTE: maybe instead we could just not output that info here?
		raise Error()

	# Hold pointer locations for output buffers so we can conditionally
	# return them later
	fs_out = None; rs_out = None; fb_out = None; rb_out=None

	# no trackers needed lol
	if forward_string: fs_out= ""          # string output container
	if reverse_string: rs_out= ""          # flipped string output container

	if forward_binary or reverse_binary:
		fb_out = bytearray(output_bytes+1) # forward bytes output container
		rb_out = bytearray(output_bytes+1) # reverse bytes output container
		out_index = 0                   # bytes output tracking
		buffer = _c_uint(0)             # buffer value container
		bits = 0                        # buffer bit tracking
		overflow = _c_uint(0)           # overflow value container
		residual = 0                    # overflow bit tracking

	index = 0 # nucleotide count tracker
	while ( index < nucleotide_count ):
		# Nucleotide Generation
		nucleotide = randint(0, unique_values-1)
		reverse_nucleotide = _flip_bits_x(nucleotide , size=bits_per_n)
		index += 1 # Keep track of our nucleotides
		# --------------------------------------------

		# String Translation
		if forward_string: fs_out += encoding.get_key( nucleotide )
		if reverse_string: rs_out = encoding.get_key(reverse_nucleotide)+rs_out
		# --------------------------------------------

		# Bytes Translation               (-_-)... fuck my life

		# Shift overflow bits into the buffer.
		if overflow: # or rb_overflow: # they'll always overflow at the same time
			# NOTE: Since we already adjusted the alignment of our bits
			# in the overflow, we don't have to do it here.
			buffer.value |= overflow.value # << _cpu_max_bits - bits
			overflow.value = 0 # empty the overflow buffer's value
			# We directionally align our input bits to the left by subtracting
			# the buffer's bit tracker from the cpu's max register bits. The bit tracker
			# keeps our previously translated nucleotides from being overwritten.

			# Add the bits from our last buffer overflow into the buffer counter.
			bits += residual
			residual = 0 # reset the overflow tracker

		# Then we check to see if we've filled the buffer.
		# NOTE:
		#	Don't forget to analyze the residual bits as a part of the whole too. Just
		#	so we don't end up with an overflow that overpopulates itself over time.
		if (bits + bits_per_n) >= _cpu_max_bits:
			# If we have filled the buffer then we'll flush it.

			# First, we need to calculate the amount of bits that we need
			# to roll over into the overflow.
			residual = abs( _cpu_max_bits - (bits + bits_per_n) )
			# Push the non-overflow bits from our nucleotide into the buffer.
			# NOTE: since binary, by default, is encoded right to left, the
			#	bits we need to push into our buffer will already be aligned to the
			#	right, so all we need to do is push out the bits that we don't want.
			buffer.value |=  nucleotide >> residual # push the residual bits out

			# Trim off our unused bits to the left by levearaging the cpu.
			# NOTE:
			#	When pushing bits too far out of a byte at the processor level,
			#	the most common procedure is to discard them values. So when we bit
			#	shift back to the right, the bits we pushed out will be refilled with
			#	zeros; resulting in a kind of cut opperation.
			# XXX: Please remember it's up to the processor to decide how bits pushed
			# out of bounds are handled.
			overflow.value = nucleotide << _cpu_max_bits - residual
			# NOTE:
			#	We don't have to right align the bits for any reason. So we can
			#	optimize things a little bit by leaving this left aligned since that's
			#	how we'll be wanting it anyway.
			# overflow >>= _cpu_max_bits - residual

			# Last and most importantly, we flush the buffer:

			# loop through each byte of the nucleotide buffer
			for byte in range(0, _cpu_max_bytes):
				# In order to properly align the output buffer, the first thing
				# we need to do is reference the proper place in the output buffer.
				# We use the byte_index to track our location in the ouput byte array,
				# and use the local byte variable to track our nucleotide buffer index.
				fb_out[ out_index + byte ]=_apply_mask( buffer.value,
					# Now we need to syncronize the nucleotide buffer's bytes with the
					# output buffer. We can use the third parameter fo the _apply_mask
					# function to shift the mask forward before value retrieval.
					# The parameter expects a bit count, so we'll have to multiply
					# the byte result by 8. But first, we'll use a negative modulo,
					# to find the byte possition in decending order.
					255, ( ( -byte-1 ) % 8 ) * 8
				)

			# Increment the output buffer placeholder
			out_index += _cpu_max_bytes

			# reset our nucleotide buffer
			buffer.value = 0
			# and it's tracker too
			bits = 0

		else:
			# Left align the nucleotide before adding it to the buffer
			buffer.value |= nucleotide << _cpu_max_bits - bits_per_n - bits
			# Keep track of our nucleotide buffer's inventory.
			bits += bits_per_n

		# When we have finished adding the final nucleotide, if we have anything
		# left in the buffer, we need to flush it one last time
		if buffer.value > 0 and out_index == buffer_chunks:
			# Unlike above where we're flushing all the bytes in the
			# nucleotide buffer however, we'll need to conditionally flush each
			# byte since we want to make sure we aren't flushing any excess
			# nucleotides.
			byte = 0
			while (byte < _cpu_max_bytes) and (out_index + byte <= output_bytes):
				# If we are within bounds, flush each byte
				fb_out[ out_index + byte] = _apply_mask( buffer.value,
					255, ( (-byte-1) % 8 ) * 8
				)

				# don't forget ot increment that counter!d
				byte += 1

	if reverse_binary:
		# Loop through our forward_binary output and flip the bits!
		# This makes things slightly more expensive when generating a
		# reversed binary alone, but saves a lot of instructions when generating
		# both the forward binary and reverse binary at the same time.
		byte = 0
		while byte < len(fb_out):
			rb_out[-(byte+1)] = _flip_bits_x(fb_out[byte], size=8)
			byte += 1

	if not forward_binary:
		# if we weren't supposed to put out the fb_out, just change it's value
		# to None and let the trash collector take care of it.
		fb_out = None

	kinds=[
		"forward_string", "forward_binary", "reverse_string", "reverse_binary"
	]
	return_values=[fs_out, fb_out, rs_out, rb_out]
	# XXX: the dictionary's just here to make the output more readable.
	return {
		output[0]: output[1]
			for output in zip(kinds, return_values)
	}

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

def compliment_binary(input, encoding, remainder=0):
	"""
		returns the inverse complement of the input storage binary with BioEncoding "encoding"
	"""
	if not isinstance(encoding, BioEncoding):
		raise TypeError(encoding, "encoding must be an instance of BioEncoding")
	if not isinstance(sequence, bytes):
		raise TypeError(input, "input must be of type 'bytes' or 'bytearray'")
	if encoding.is_executable():
		return input

	previous = encoding.values() # our old values
	new = encoding.compliment().values() # our new chunk values

	ibin = input # our input binary
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

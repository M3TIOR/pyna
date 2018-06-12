#!/usr/bin/env python3

#
# M3TIOR 2018
#

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

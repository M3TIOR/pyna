#!/usr/bin/env python3

#
# M3TIOR 2018
#

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

class BioEncodingError(Error):
	""" Errors raised from problems with BioEncodings """
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

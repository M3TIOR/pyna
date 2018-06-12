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

class BindingError(NucleotideError):
	""" Raised when attempting to pair a nucleotide that already has a sibling
		or when a transient tries to pair itself with another transient"""
	pass

class BioEncodingError(Error):
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

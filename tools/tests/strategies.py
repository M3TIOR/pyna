#!/usr/bin/env python3

#
# M3TIOR 2018
#

#NOTE:
#	This library doesn't need to import anything from the testing library
#	since it's just here to store our global strategy lookups. I preffer this
#	over the "register_type_strategy" method since using it would undermine
#	modularity to a certain extent.

#XXX: grab all refferences from hypothesis.strategies and add to them.
from hypothesis.strategies import *
#import hypotheis.strategies.__all__ # used to compress caller import wildcard

# NOTE: BEGIN ADDING TYPES!
import pyna.types

__all__ = [ # add in our local strategies
	"nucleotides",
	"bioencoding"
]

@composite # MAYBE... It's a composite... today.
def nucleotides(draw, max_name_len=None):
	"""A hypothesis compliant strategy for the ``pyna.types.Nucleotide`` class.
	Use with the hypothesis.works library to generate Nucleotide test cases.

	Arguments:
		max_name_len (:obj:`int`, optional): Set's the max nucleotide name
		length. The default is synonymous with that of
		``hypothesis.strategies.text(max_size=...)``.
	"""
	return draw(builds(
		pyna.types.Nucleotide,
		# Try different variations of nucleotides with random
		# UTF-8 compliant keys.
		text( min_size=1, max_size=max_name_len )
	))

@composite
def bioencodings(draw, max_nucleotide_count=2**8, max_nucleotide_name_len=None):
	"""A hypothesis compliant strategy for the ``pyna.types.BioEncoding`` class.
	Use with the hypothesis.works library to generate BioEncoding test cases.

	Arguments:
		max_nucleotide_count (:obj:`int`, optional): The maximum amount of
		nucleotides that are embedded within each generated BioEncoding.
		max_nucleotide_name_len (:obj:`int`, optional): Synonymous with
		``strategies.nucleotides(max_name_len=...)``. Applied to all nucleotides
		within this strategy.
	"""
	nucleotide_cluster = draw(lists(
		 # create a scrambled list of nucleotide objects
		nucleotides(max_name_len=nax_nucleotide_name_len),
		min_size=2, # ensure we have at least two nucletides to work with
		max_size=max_nucleotide_count # and that we carry over the maximum

		# and post creation, make sure we have an even number of nucelotides
	).filter(lambda list: (len(list) % 2) != 1 ))

	# Ensure that all our nucleotide pairs are paired and not without their
	# siblings. Otherwise they will break the BioEncoding.
	for n in range(0, len(nucleotide_cluster)-1, 2): # pairs
		# Pair linear, we'll scramble later.
		nucleotide_cluster[n].pair(nucleotide_cluster[n+1])

	# This ensures we aren't depending on our Nucleotides
	# being in any specific order.
	scrambled = draw(permutations(nucleotide_cluster))
	long = draw(booleans())

	return draw(one_of(
		# Then finally, ensure we also complete tests with our static encodings
		# just for insurance that nothing important breaks in production.
		just(pyna.types.BioEncoding(*scrambled, long=long)),
		just(pyna.types.BioEncoding.RNA(long=long)),
		just(pyna.types.BioEncoding.DNA(long=long))
	))

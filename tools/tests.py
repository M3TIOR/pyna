#!/usr/bin/env python3

import random
import sys

sys.path.append("../src")
# import pyna
from pyna import (
	# ADD FUTURE FUNCTIONS LATER
	dna2bytes
)

def bin(data):
	# tool for looking at binary output
	try:
		for byte in data:
			print('{0:08b}'.format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		print('{0:08b}'.format(data if isinstance(data, int) else ord(data)))

if __name__ == "__main__":
	static = True

	#G = 0
	#C = 0
	#A = 1
	#T = 1

	static_strand = "ATCGATATGCATAGTACATAG"
	random_strand = "" #TODO implement more variable test cases



	strand = static_strand if static else random_strand

	print("Using Test Strand: " + strand)

	tail = dna2bytes(strand)
	# USING STATIC:
	#	11001111
	#	00111011
	#	0111 - 0000
	#
	# PASSING!
	print("Tail Test:")
	bin(tail)

	head = dna2bytes(strand, head=True)
	print("Head Test:")
	bin(head)

	fliptail = dna2bytes(strand, flip=True)
	print("Flip + Tail Test:")
	bin(fliptail)

	fliphead = dna2bytes(strand, flip=True, head=True)
	print("Flip + Head Test:")
	bin(fliphead)

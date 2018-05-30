#!/usr/bin/env python3

import unittest
import random
import sys

sys.path.append("../src")
# import pyna
from pyna import (
	#NOTE: ADD FUTURE FUNCTIONS LATER
	dna2bytes
)

def print_bin(data):
	"""
		A tool for inspecting binary output, prints each byte to stdout
	"""
	try:
		for byte in data:
			print('{0:08b}'.format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		print('{0:08b}'.format(data if isinstance(data, int) else ord(data)))

def bin(data):
	"""
		A tool for inspecting binary output, returns a list containing each byte
	"""
	out = []
	try:
		for byte in data:
			out.append('{0:08b}'.format(byte if isinstance(byte, int) else ord(byte)))
	except(TypeError):
		out.append('{0:08b}'.format(data if isinstance(data, int) else ord(data)))
	return out

def compair_targets(target, result):
	"""
		Checks if two list's contents are the same
	"""
	index = 0
	test_pass = True

	length = len(target)
	lines = list(range(0, length))

	while index < length:


	while index < length:
		if s1[index] != s2[index]:
			print(s1[index]+"\t!=\t"+s2[index])
			test_pass = False
		else:
			print(s1[index]+"\t==\t"+s2[index])
		index +=1

	if test_pass:
		print("PASSED!\n")
	else:
		print("FAILED...\n")

	return test_pass


class TestPyNA(unittest.TestSuite):
	
	class TestDNA2Bytes(unittest.TestCase):



if __name__ == "__main__":
	static = True

	#G = 0
	#C = 0
	#A = 1
	#T = 1

	static_strand = "ATCGATATGCATAGTACATAG"
	random_strand = "" #TODO implement more variable test cases



	strand = static_strand if static else random_strand

	print("Using Test Strand: " + strand+ "\n")


	tail = dna2bytes(strand)
	print("Tail Test:")
	if static:
		starget = [
			"11001111",
			"00111011",
			"01110000"
		]
		compair_streams(bin(tail), starget)
	else:
		bin(tail)
	# USING STATIC: "ATCGATATGCATAGTACATAG"
	#	11001111
	#	00111011
	#	01110 - 000 (remainder)
	#
	# PASSED!


	head = dna2bytes(strand, head=True)
	print("Head Test:")
	if static:
		starget = [
			"00001110",
			"11011100",
			"11110011"
		]
		compair_streams(bin(head), starget)
	else:
		bin(head)
	# USING STATIC: "ATCGATATGCATAGTACATAG"
	#	(remainder) 000 - 01110
	#	11011100
	#	11110011
	#
	# FAILED...


	fliptail = dna2bytes(strand, flip=True)
	# USING STATIC: "ATCGATATGCATAGTACATAG"
	#	01110110
	#	11100111
	#	10011 - 000 (remainder)
	#
	# FAILED...
	print("Flip + Tail Test:")
	bin(fliptail)


	fliphead = dna2bytes(strand, flip=True, head=True)
	print("Flip + Head Test:")
	bin(fliphead)

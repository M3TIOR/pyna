#!/usr/bin/env python3

#
# M3TIOR 2018
#	XXX don't forget you can call a library as a main executable in python XXX
#

# import unittest and test modules
import unittest
from .decode import decode
from .bioencoding import bioencoding
from .nucleotide import nucleotide


if __name__ == "__main__":
	runner = unittest.TextTestRunner(verbosity=2)

	pyna = unittest.TestSuite(tests=(
		unittest.TestSuite(tests=(
			decode('test_executable_tail_static'),
			decode('test_executable_head_static'),
			decode('test_executable_flipTail_static'),
			decode('test_executable_flipHead_static'),
			decode('test_storage_tail_static'),
			decode('test_storage_head_static'),
			decode('test_storage_flipTail_static'),
			decode('test_storage_flipHead_static')
		)),
		unittest.TestSuite(tests=(
			bioencoding('test_keys'),
			bioencoding('test_values'),
			bioencoding('test_dict'),
			bioencoding('test_switch')
		)),
		unittest.TestSuite(tests=(
			nucleotide('test_instance'),
			nucleotide('test_pair'),
			nucleotide('test_couple')
		))
	))

	# Run all test modules!
	runner.run(pyna)

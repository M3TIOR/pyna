#!/usr/bin/env python3

# import unittest and test modules
import unittest
import tests.dna2bytes as dna2bytes
import tests.dnaencoding as dnaencoding


if __name__ == "__main__":
	runner = unittest.TextTestRunner(verbosity=2)

	dna2bytes_tests = unittest.TestSuite(tests=(
		dna2bytes.DNA2Bytes('test_tail_static'),
		dna2bytes.DNA2Bytes('test_head_static'),
		dna2bytes.DNA2Bytes('test_flipTail_static'),
		dna2bytes.DNA2Bytes('test_flipHead_static')
	))

	dnaencoding_tests = unittest.TestSuite(tests=(
		dnaencoding.DNAEncoding('test_new_instance'),
		dnaencoding.DNAEncoding('test_rebinding'),
		dnaencoding.DNAEncoding('test_wrong_keycount_rebinding'),
		dnaencoding.DNAEncoding('test_redundant_index_rebinding')
	))

	pyna = unittest.TestSuite(tests=(
		dna2bytes_tests,
		dnaencoding_tests,
	))

	# Run all test modules!
	runner.run(pyna)

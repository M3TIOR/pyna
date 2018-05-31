#!/usr/bin/env python3

# import unittest and test modules
import unittest
import tests.dna2bytes as dna2bytes
import tests.dnaencoding as dnaencoding


if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	suite = unittest.TestSuite()

	#Add All Test Modules
	suite.addTest( dna2bytes.DNA2Bytes('test_tail_static') )
	suite.addTest( dna2bytes.DNA2Bytes('test_head_static') )
	suite.addTest( dna2bytes.DNA2Bytes('test_flipTail_static') )
	suite.addTest( dna2bytes.DNA2Bytes('test_flipHead_static') )

	suite.addTest( dnaencoding.DNAEncoding('test_new_instance') )
	suite.addTest( dnaencoding.DNAEncoding('test_rebinding') )
	suite.addTest( dnaencoding.DNAEncoding('test_wrong_keycount_rebinding') )
	suite.addTest( dnaencoding.DNAEncoding('test_redundant_index_rebinding') )

	# Run all test modules!
	runner.run(suite)

#!/usr/bin/env python3

#
# M3TIOR 2018
#	XXX don't forget you can call a library as a main executable in python XXX
#


# import unittest and test modules
import unittest

runner = unittest.TextTestRunner(verbosity=2)

# TODO:
#	Implement a system that dynamically finds all the "test_" preffaced
#	files in the current directory and then find all their attribute names
#	preffaced with "test_", and for each that are classes loop through them
#	and find their "test_" preffaced attributes...
#
#	(IN OTHER WORDS, MAKE A MODULAR LOADER SO ADDING TESTS IS EASIER DUMMY!)

# Run all test modules!
runner.run(pyna)

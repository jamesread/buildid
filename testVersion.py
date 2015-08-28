#!/usr/bin/python

import buildid
import unittest

class VersionIdentifierTest(unittest.TestCase):
	def test_format_gnu(self):
		v = VersionIdentifier()

		self.assertEqual(v.

#!/usr/bin/python

import sys

sys.path.append("../")

from buildid.classes import VersionIdentifier
import unittest

class VersionIdentifierTest(unittest.TestCase):
	def test_format_gnu(self):
		v1 = VersionIdentifier(1, 0, 1)
		v2 = VersionIdentifier(2, 0, 0)

		self.assertTrue(v1 < v2)
		self.assertFalse (v1 > v2)

		self.assertTrue(v2 > v1)
		self.assertFalse(v2 < v1)

#!/usr/bin/python

import sys

sys.path.append("../")
sys.path.append("./")

from buildid.classes import VersionIdentifier
import unittest

class VersionIdentifierTest(unittest.TestCase):
	def test_format_v101(self):
		v = VersionIdentifier(1, 0, 1)

		self.assertEqual(v.get_formatted_gnu(), "1.0.1")
		self.assertEqual(v.get_formatted_win(), "1.0.1.0")

	def test_comparisons(self):
		v1 = VersionIdentifier(1, 0, 1)
		self.assertEqual(v1, v1)
		self.assertIsNotNone(v1)

		v2 = VersionIdentifier(2, 0, 0)
		self.assertEqual(v2, v2)
		self.assertIsNotNone(v2)

		self.assertLess(v1, v2)
		self.assertGreater(v2, v1)

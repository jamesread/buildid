#!/usr/bin/python

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from buildid import stuff 

stuff.main()

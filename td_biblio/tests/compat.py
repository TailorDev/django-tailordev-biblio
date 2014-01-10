# -*- coding: utf-8 -*-
"""Compatibility tools for tests inspired by factory boy"""

import sys

is_python2 = (sys.version_info[0] == 2)

if sys.version_info[0:2] < (2, 7):  # pragma: no cover
    import unittest2 as unittest
else:  # pragma: no cover
    import unittest  # NOQA

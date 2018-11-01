#!/usr/bin/env python3

# stdlib
import unittest

# local
import lib.terraform


# =============================================================================
#
# test classes
#
# =============================================================================

class TestVersionMethod(unittest.TestCase):
    def test_version(self):
        lib.terraform.version()


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

# stdlib
import unittest

# local
import tests.terraform.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestInit(unittest.TestCase):
    def test_init(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

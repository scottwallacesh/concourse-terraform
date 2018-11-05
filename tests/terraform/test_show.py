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

class TestShow(unittest.TestCase):
    def test_show_plan_file(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.create_plan_file(test_working_dir)
            common.show_plan_file(test_working_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

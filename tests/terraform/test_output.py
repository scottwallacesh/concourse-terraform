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

class TestOutput(unittest.TestCase):
    def test_output(self):
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_state_dir:
                common.init_test_working_dir(test_working_dir)
                common.output_with_existing_state(test_working_dir,
                                                  test_state_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

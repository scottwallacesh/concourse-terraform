#!/usr/bin/env python3

# stdlib
import unittest
from subprocess import CalledProcessError

# local
import tests.terraform.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestPlan(unittest.TestCase):
    def test_create_plan_with_no_output(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.create_plan_with_no_output(test_working_dir)

    def test_create_plan_file(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.create_plan_file(test_working_dir)

    def test_plan_with_no_changes(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan(test_working_dir)
            with self.assertRaises(CalledProcessError):
                common.create_plan_with_no_output(test_working_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

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

class TestApply(unittest.TestCase):
    def test_apply_with_no_plan(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan(test_working_dir)

    def test_apply_with_no_plan_with_existing_state(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan_with_existing_state(test_working_dir)

    def test_apply_with_no_plan_with_existing_empty_state(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan_with_existing_empty_state(
                test_working_dir)

    def test_apply_plan_file(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.create_plan_file(test_working_dir)
            common.apply_plan_file(test_working_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

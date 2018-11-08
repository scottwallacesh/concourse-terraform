#!/usr/bin/env python3

# stdlib
import unittest

# local
import tests.terraform.common as common
from lib.terraform import TerraformNoChangesError


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
            with self.assertRaises(TerraformNoChangesError):
                common.create_plan_with_no_output(test_working_dir)

    def test_plan_with_no_changes_no_error(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan(test_working_dir)
            common.create_plan_with_no_output_allow_no_changes(
                test_working_dir)

    def test_plan_destroy_with_no_changes_no_error(self):
        with common.create_test_working_dir() as test_working_dir:
            common.init_test_working_dir(test_working_dir)
            common.apply_with_no_plan(test_working_dir)
            common.create_plan_destroy_with_no_output_allow_no_changes(
                test_working_dir)

    def test_plan_with_existing_state(self):
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_state_dir:
                common.init_test_working_dir(test_working_dir)
                with self.assertRaises(TerraformNoChangesError):
                    common.create_plan_with_existing_state(
                        test_working_dir,
                        test_state_dir)

    def test_plan_with_existing_empty_state(self):
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_state_dir:
                common.init_test_working_dir(test_working_dir)
                common.create_plan_with_existing_empty_state(
                    test_working_dir,
                    test_state_dir)

    def test_plan_destroy_with_existing_state(self):
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_state_dir:
                common.init_test_working_dir(test_working_dir)
                common.create_plan_destroy_with_existing_state(
                    test_working_dir,
                    test_state_dir)

    def test_plan_destroy_with_existing_empty_state(self):
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_state_dir:
                common.init_test_working_dir(test_working_dir)
                with self.assertRaises(TerraformNoChangesError):
                    common.create_plan_destroy_with_existing_empty_state(
                        test_working_dir,
                        test_state_dir)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

# stdlib
import unittest

# local
import lib.terraform_dir
import tests.terraform_dir.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestShowTerraformPlan(unittest.TestCase):
    def test_requires_terraform_dir(self):
        with self.assertRaises(ValueError):
            # apply with empty string as the terraform dir
            lib.terraform_dir.show_terraform_plan(
                '',
                'tfplan',
                debug=True)

    def test_show_plan(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create plan file
            terraform_plan_file = lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                debug=True)
            # show plan file
            lib.terraform_dir.show_terraform_plan(
                terraform_dir,
                terraform_plan_file,
                debug=True)

    def test_show_destroy_plan(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create plan file
            terraform_plan_file = lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                destroy=True,
                error_on_no_changes=False,
                debug=True)
            # show plan file
            lib.terraform_dir.show_terraform_plan(
                terraform_dir,
                terraform_plan_file,
                debug=True)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

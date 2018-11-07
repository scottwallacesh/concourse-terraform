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

class ApplyTerraformPlan(unittest.TestCase):
    def test_requires_terraform_dir(self):
        with self.assertRaises(ValueError):
            # apply with empty string as the terraform dir
            lib.terraform_dir.apply_terraform_plan(
                '',
                debug=True)

    def test_apply_from_default_plan_file(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create plan file
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                debug=True)
            # apply plan file
            lib.terraform_dir.apply_terraform_plan(
                terraform_dir,
                debug=True)

    def test_apply_from_explicit_plan_file(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create plan file
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                plan_file_path='test.tfplan',
                debug=True)
            # apply plan file
            lib.terraform_dir.apply_terraform_plan(
                terraform_dir,
                plan_file_path='test.tfplan',
                debug=True)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

# stdlib
import os
import unittest

# local
import lib.terraform_dir
import tests.terraform_dir.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class PlanTerraformDir(unittest.TestCase):
    def test_requires_terraform_dir(self):
        with self.assertRaises(ValueError):
            # plan with empty string as the terraform dir
            lib.terraform_dir.plan_terraform_dir(
                '',
                debug=True)

    def test_plan_with_no_output(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # plan the terraform dir
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                debug=True)

    def test_plan_creates_plan_file(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # plan the terraform dir
            terraform_plan_file = lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                debug=True)
            # check for expected file
            expected_plan_file_path = \
                os.path.join(
                    terraform_dir,
                    terraform_plan_file)
            self.assertTrue(os.path.isfile(expected_plan_file_path))


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

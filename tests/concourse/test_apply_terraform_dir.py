#!/usr/bin/env python3

# stdlib
import os
import unittest

# local
import lib.concourse
import tests.concourse.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class ApplyTerraformDir(unittest.TestCase):
    def test_apply_with_no_plan(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.concourse.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # apply the terraform dir
            lib.concourse.apply_terraform_dir(
                terraform_dir,
                debug=True)

    def test_apply_from_plan(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.concourse.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # plan the terraform dir
            terraform_plan_file = lib.concourse.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                debug=True)
            # plan the terraform dir
            lib.concourse.apply_terraform_dir(
                terraform_dir,
                plan_file_path=terraform_plan_file,
                debug=True)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

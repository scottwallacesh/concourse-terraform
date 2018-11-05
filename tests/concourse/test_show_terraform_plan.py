#!/usr/bin/env python3

# stdlib
import unittest

# local
import lib.concourse
import tests.concourse.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class ShowTerraformPlan(unittest.TestCase):
    def test_show_plan(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.concourse.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create plan file
            terraform_plan_file = lib.concourse.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                debug=True)
            # show plan file
            lib.concourse.show_terraform_plan(
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

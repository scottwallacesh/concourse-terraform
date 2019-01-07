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

class TestPlanTerraformDir(unittest.TestCase):
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

    def test_plan_with_destroy(self):
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
                error_on_no_changes=False,
                destroy=True,
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

    def test_plan_imports_state_file(self):
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
                state_file_path=common.TEST_STATE_FILE_WITHOUT_KEY,
                debug=True)
            # check for expected state file
            expected_state_file_path = \
                os.path.join(
                    terraform_dir,
                    lib.terraform_dir.TERRAFORM_STATE_FILE_NAME)
            self.assertTrue(os.path.isfile(expected_state_file_path))

    def test_plan_imports_output_var_file_with_single_value(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_VAR_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            output_var_files = {
                'algorithm': common.TEST_TERRAFORM_SINGLE_OUTPUT_VAR_FILE_PATH
            }
            expected_var_file_path = \
                os.path.join(terraform_dir, 'algorithm.tfvars.json')
            # plan the terraform dir
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                output_var_files=output_var_files,
                debug=True)
            self.assertTrue(os.path.exists(expected_var_file_path))
            with open(
                common.TEST_TERRAFORM_CONVERTED_SINGLE_OUTPUT_VAR_FILE_PATH,
                    'r') as expected_var_file:
                expected_var_file_contents = expected_var_file.read()
            with open(expected_var_file_path, 'r') as var_file:
                actual_var_file_contents = var_file.read()
            self.assertEqual(
                expected_var_file_contents,
                actual_var_file_contents)

    def test_plan_imports_output_var_file_with_multi_values(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_VAR_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            output_var_files = {
                'multi': common.TEST_TERRAFORM_MULTI_OUTPUT_VAR_FILE_PATH
            }
            expected_var_file_path = \
                os.path.join(terraform_dir, 'multi.tfvars.json')
            # plan the terraform dir
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                output_var_files=output_var_files,
                debug=True)
            self.assertTrue(os.path.exists(expected_var_file_path))
            with open(
                common.TEST_TERRAFORM_CONVERTED_MULTI_OUTPUT_VAR_FILE_PATH,
                    'r') as expected_var_file:
                expected_var_file_contents = expected_var_file.read()
            with open(expected_var_file_path, 'r') as var_file:
                actual_var_file_contents = var_file.read()
            self.assertEqual(
                expected_var_file_contents,
                actual_var_file_contents)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

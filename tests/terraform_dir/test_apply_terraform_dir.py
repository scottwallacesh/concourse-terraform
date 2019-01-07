#!/usr/bin/env python3

# stdlib
import os
import unittest
from subprocess import CalledProcessError

# local
import lib.terraform_dir
import tests.terraform_dir.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestApplyTerraformDir(unittest.TestCase):
    def test_requires_terraform_dir(self):
        with self.assertRaises(ValueError):
            # apply with empty string as the terraform dir
            lib.terraform_dir.apply_terraform_dir(
                '',
                debug=True)

    def test_apply(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # apply without plan
            lib.terraform_dir.apply_terraform_dir(
                terraform_dir,
                debug=True)

    def test_apply_imports_state_file(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # apply without plan
            lib.terraform_dir.apply_terraform_dir(
                terraform_dir,
                state_file_path=common.TEST_STATE_FILE_WITH_KEY,
                debug=True)
            # check for expected state file
            expected_state_file_path = \
                os.path.join(
                    terraform_dir,
                    lib.terraform_dir.TERRAFORM_STATE_FILE_NAME)
            self.assertTrue(os.path.isfile(expected_state_file_path))

    def test_apply_exports_state_files(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create a new temp dir as the state output dir
            with common.create_test_working_dir() as state_output_dir:
                # apply without plan
                lib.terraform_dir.apply_terraform_dir(
                    terraform_dir,
                    state_file_path=common.TEST_STATE_FILE_WITHOUT_KEY,
                    state_output_dir=state_output_dir,
                    debug=True)
                # check for exported state files
                exported_state_file_path = \
                    os.path.join(
                        state_output_dir,
                        lib.terraform_dir.TERRAFORM_STATE_FILE_NAME)
                exported_backup_state_file_path = \
                    os.path.join(
                        state_output_dir,
                        lib.terraform_dir.TERRAFORM_BACKUP_STATE_FILE_NAME)
                self.assertTrue(
                    os.path.isfile(exported_state_file_path))
                self.assertTrue(
                    os.path.isfile(exported_backup_state_file_path))

    def test_apply_exports_state_files_on_failure(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_INVALID_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create a new temp dir as the state output dir
            with common.create_test_working_dir() as state_output_dir:
                with self.assertRaises(CalledProcessError):
                    # apply without plan
                    lib.terraform_dir.apply_terraform_dir(
                        terraform_dir,
                        state_file_path=common.TEST_STATE_FILE_WITHOUT_KEY,
                        state_output_dir=state_output_dir,
                        debug=True)
                # check for exported state files
                exported_state_file_path = \
                    os.path.join(
                        state_output_dir,
                        lib.terraform_dir.TERRAFORM_STATE_FILE_NAME)
                exported_backup_state_file_path = \
                    os.path.join(
                        state_output_dir,
                        lib.terraform_dir.TERRAFORM_BACKUP_STATE_FILE_NAME)
                self.assertTrue(
                    os.path.isfile(exported_state_file_path))
                self.assertTrue(
                    os.path.isfile(exported_backup_state_file_path))

    def test_apply_imports_output_var_file_with_single_value(self):
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
            # apply the terraform dir
            lib.terraform_dir.apply_terraform_dir(
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

    def test_apply_imports_output_var_file_with_multi_values(self):
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
            # apply the terraform dir
            lib.terraform_dir.apply_terraform_dir(
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

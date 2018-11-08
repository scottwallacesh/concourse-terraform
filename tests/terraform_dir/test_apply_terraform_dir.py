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


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

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

class TestApplyTerraformPlan(unittest.TestCase):
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

    def test_apply_with_destroy_plan_file(self):
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
            # create destroy plan file
            lib.terraform_dir.plan_terraform_dir(
                terraform_dir,
                create_plan_file=True,
                destroy=True,
                debug=True)
            # apply plan file
            lib.terraform_dir.apply_terraform_plan(
                terraform_dir,
                debug=True)

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
                # create plan file
                lib.terraform_dir.plan_terraform_dir(
                    terraform_dir,
                    state_file_path=common.TEST_STATE_FILE_WITHOUT_KEY,
                    create_plan_file=True,
                    debug=True)
                # apply plan file
                lib.terraform_dir.apply_terraform_plan(
                    terraform_dir,
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
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create a new temp dir as the state output dir
            with common.create_test_working_dir() as state_output_dir:
                # run plan to import existing state
                # but don't create a plan file
                lib.terraform_dir.plan_terraform_dir(
                    terraform_dir,
                    state_file_path=common.TEST_STATE_FILE_WITHOUT_KEY,
                    debug=True)
                # manually create a backup state file since
                # apply won't succeed
                mock_backup_state_file_path = \
                    os.path.join(
                        terraform_dir,
                        lib.terraform_dir.TERRAFORM_BACKUP_STATE_FILE_NAME)
                with open(mock_backup_state_file_path, 'w') \
                        as mock_backup_state_file:
                    mock_backup_state_file.write('{}')
                # apply a missing plan file
                with self.assertRaises(CalledProcessError):
                    lib.terraform_dir.apply_terraform_plan(
                        terraform_dir,
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

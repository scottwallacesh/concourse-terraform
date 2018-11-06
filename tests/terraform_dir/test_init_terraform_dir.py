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

class TestInitTerraformDir(unittest.TestCase):
    def test_destroys_existing_terraform_dir(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # create the terraform dir
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            os.mkdir(terraform_dir)
            # create an existing file in it
            terraform_file_path = \
                os.path.join(terraform_dir, 'vars.tf')
            with open(terraform_file_path, 'w') as terraform_file:
                terraform_file.write('variable "test" {}')
            # test init
            lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # assert the file was destroyed
            self.assertFalse(os.path.exists(terraform_file_path))

    def test_creates_backend_file_for_backend_type(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the terraform dir path
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            # get the expected backend file path
            backend_file_path = \
                os.path.join(terraform_dir, lib.terraform_dir.BACKEND_FILE_NAME)
            # set the backend type in the environment
            os.environ[lib.terraform_dir.BACKEND_TYPE_VAR] = 'local'
            # test init
            lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True,
            )
            # assert the file was created
            self.assertTrue(os.path.exists(backend_file_path))
            # read the backend file
            with open(backend_file_path, 'r') as backend_file:
                backend_file_contents = backend_file.read()
            # assert the file contents contain the expected backend
            self.assertTrue(
                'backend "local"' in backend_file_contents
            )


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

# stdlib
import os
import unittest

# local
import lib.terraform_dir
import tests.terraform_dir.common as common


# =============================================================================
#
# constants
#
# =============================================================================

TEST_AUX_INPUT_NAME = 'aux_test'


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
                terraform_source_dir=common.TEST_TERRAFORM_DIR,
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
                os.path.join(terraform_dir,
                             lib.terraform_dir.BACKEND_FILE_NAME)
            # set the backend type in the environment
            with common.mocked_env_vars(
                    {lib.terraform_dir.BACKEND_TYPE_VAR: 'local'}):
                # test init
                lib.terraform_dir.init_terraform_dir(
                    terraform_source_dir=common.TEST_TERRAFORM_DIR,
                    terraform_work_dir=test_working_dir,
                    debug=True
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

    def test_creates_backend_file_for_backend_type_in_terraform_dir_path(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the terraform dir path
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            # get the terraform dir path
            terraform_dir_path = 'foo'
            # get the expected backend file path
            backend_file_path = \
                os.path.join(terraform_dir, terraform_dir_path,
                             lib.terraform_dir.BACKEND_FILE_NAME)
            # set the backend type in the environment
            with common.mocked_env_vars(
                    {lib.terraform_dir.BACKEND_TYPE_VAR: 'local'}):
                # test init
                lib.terraform_dir.init_terraform_dir(
                    terraform_source_dir=common.TEST_TERRAFORM_DIR,
                    terraform_work_dir=test_working_dir,
                    terraform_dir_path=terraform_dir_path,
                    debug=True
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

    def test_imports_aux_input_with_no_name(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the terraform dir path
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            # get the expected aux file path
            aux_file_path = \
                os.path.join(
                    terraform_dir, common.TEST_TERRAFORM_AUX_FILE_NAME)
            # set the aux path in the environment
            with common.mocked_env_vars(
                    {
                        lib.terraform_dir.AUX_INPUT_PATH_PREFIX + "0":
                            common.TEST_TERRAFORM_AUX_DIR
                    }):
                # test init
                lib.terraform_dir.init_terraform_dir(
                    terraform_source_dir=common.TEST_TERRAFORM_DIR,
                    terraform_work_dir=test_working_dir,
                    debug=True
                )
                # assert the file was copied
                self.assertTrue(os.path.exists(aux_file_path))
                # read the aux file
                with open(aux_file_path, 'r') as aux_file:
                    aux_file_contents = aux_file.read()
                # assert the file contains the expected content
                self.assertEqual(aux_file_contents, "hello world")

    def test_imports_aux_input_with_name(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the terraform dir path
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            # get the expected aux file path
            aux_file_path = \
                os.path.join(
                    terraform_dir,
                    TEST_AUX_INPUT_NAME,
                    common.TEST_TERRAFORM_AUX_FILE_NAME)
            # set the aux path and name in the environment
            with common.mocked_env_vars(
                    {
                        lib.terraform_dir.AUX_INPUT_PATH_PREFIX + "0":
                            common.TEST_TERRAFORM_AUX_DIR,
                        lib.terraform_dir.AUX_INPUT_NAME_PREFIX + "0":
                            TEST_AUX_INPUT_NAME
                    }):
                # test init
                lib.terraform_dir.init_terraform_dir(
                    terraform_source_dir=common.TEST_TERRAFORM_DIR,
                    terraform_work_dir=test_working_dir,
                    debug=True
                )
                # assert the file was copied
                self.assertTrue(os.path.exists(aux_file_path))
                # read the aux file
                with open(aux_file_path, 'r') as aux_file:
                    aux_file_contents = aux_file.read()
                # assert the file contains the expected content
                self.assertEqual(aux_file_contents, "hello world")

    def test_imports_plugin_cache(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the terraform dir path
            terraform_dir = os.path.join(
                test_working_dir, lib.terraform_dir.TERRAFORM_DIR_NAME)
            # get the expected cached aux file path
            aux_file_path = \
                os.path.join(
                    terraform_dir,
                    lib.terraform_dir.TERRAFORM_PLUGIN_CACHE_DIR_NAME,
                    common.TEST_TERRAFORM_AUX_FILE_NAME)
            # set the cache path in the environment
            with common.mocked_env_vars(
                    {
                        lib.terraform_dir.TERRAFORM_PLUGIN_CACHE_VAR_NAME:
                            common.TEST_TERRAFORM_AUX_DIR
                    }):
                # test init
                lib.terraform_dir.init_terraform_dir(
                    terraform_source_dir=common.TEST_TERRAFORM_DIR,
                    terraform_work_dir=test_working_dir,
                    debug=True
                )
                # assert the file was copied
                self.assertTrue(os.path.exists(aux_file_path))
                # read the aux file
                with open(aux_file_path, 'r') as aux_file:
                    aux_file_contents = aux_file.read()
                # assert the file contains the expected content
                self.assertEqual(aux_file_contents, "hello world")

    def test_exports_plugin_cache(self):
        # create a new temp dir as the plugin cache
        with common.create_test_working_dir() as test_plugin_cache:
            # set the cache path in the environment
            with common.mocked_env_vars(
                    {
                        lib.terraform_dir.TERRAFORM_PLUGIN_CACHE_VAR_NAME:
                            test_plugin_cache
                    }):
                # get an expected cached plugin dir path
                cached_plugin_arch_dir = \
                    os.path.join(
                        test_plugin_cache,
                        'linux_amd64')
                # assert the dir does not yet exist
                self.assertFalse(os.path.exists(cached_plugin_arch_dir))
                # create a new temp dir as the working dir
                with common.create_test_working_dir() as test_working_dir:
                    # test init
                    lib.terraform_dir.init_terraform_dir(
                        terraform_source_dir=common.TEST_TERRAFORM_DIR,
                        terraform_work_dir=test_working_dir,
                        debug=True
                    )
                    # assert the dir was created
                    self.assertTrue(os.path.exists(cached_plugin_arch_dir))


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

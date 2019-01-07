#!/usr/bin/env python3

# stdlib
import json
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

class TestOutputTerraformDir(unittest.TestCase):
    def test_requires_terraform_dir(self):
        with self.assertRaises(ValueError):
            # apply with empty string as the terraform dir
            lib.terraform_dir.output_terraform_dir(
                '',
                '/tmp/example',
                debug=True)

    def test_requires_output_file_path(self):
        with self.assertRaises(ValueError):
            # apply with empty string as the output file path
            lib.terraform_dir.output_terraform_dir(
                '/tmp/example',
                '',
                debug=True)

    def test_creates_output_file(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_output_dir:
                # init terraform dir
                terraform_dir = lib.terraform_dir.init_terraform_dir(
                    terraform_work_dir=test_working_dir,
                    debug=True)
                # output
                lib.terraform_dir.output_terraform_dir(
                    terraform_dir,
                    test_output_dir,
                    terraform_work_dir=test_working_dir,
                    state_file_path=common.TEST_STATE_FILE_WITH_OUTPUT,
                    debug=True)
                # check for expected output file
                expected_output_file_path = \
                    os.path.join(
                        test_output_dir,
                        lib.terraform_dir.TERRAFORM_OUTPUT_FILE_NAME)
                self.assertTrue(os.path.isfile(expected_output_file_path))

    def test_allows_specifying_output_targets(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            with common.create_test_working_dir() as test_output_dir:
                # init terraform dir
                terraform_dir = lib.terraform_dir.init_terraform_dir(
                    terraform_work_dir=test_working_dir,
                    debug=True)
                # create targets
                output_targets = {
                    "test": "example"
                }
                # output
                lib.terraform_dir.output_terraform_dir(
                    terraform_dir,
                    test_output_dir,
                    output_targets=output_targets,
                    terraform_work_dir=test_working_dir,
                    state_file_path=common.TEST_STATE_FILE_WITH_OUTPUT,
                    debug=True)
                # read output file
                output_file_path = \
                    os.path.join(
                        test_output_dir,
                        "test.json")
                with open(output_file_path, 'r') as output_file:
                    output_file_contents = json.load(output_file)
                self.assertTrue('value' in output_file_contents)
                self.assertEqual(output_file_contents['value'],
                                 'hello world')


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

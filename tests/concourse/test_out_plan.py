#!/usr/bin/env python3

# stdlib
import unittest
import os

# local
import lib.concourse
import tests.concourse.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestOutPlan(unittest.TestCase):
    def test_out_plan_destroys_existing_tfwork_dir(self):
        # create a new temp dir as the tfwork dir
        with common.create_test_working_dir() as test_tfwork_dir:
            # create an existing file in it
            tfwork_file_path = \
                os.path.join(test_tfwork_dir, 'file.txt')
            with open(tfwork_file_path, 'w') as tfwork_file:
                tfwork_file.write('hello world')
            # create a test payload
            test_payload = {
                'params': {
                    'action': 'plan',
                    'plan': {
                        'terraform_dir': common.TEST_TERRAFORM_DIR
                    }
                }
            }
            with common.create_test_working_dir() as test_working_dir:
                lib.concourse.do_out(
                    input_payload=test_payload,
                    working_dir_path=test_working_dir,
                    tfwork_dir_path=test_tfwork_dir)
                self.assertFalse(os.path.exists(tfwork_file_path))

    def test_out_plan_copies_terraform_dir_to_tfwork_dir(self):
        # create a new temp dir as the tfwork dir
        with common.create_test_working_dir() as test_tfwork_dir:
            # create a test payload
            test_payload = {
                'params': {
                    'action': 'plan',
                    'plan': {
                        'terraform_dir': common.TEST_TERRAFORM_DIR
                    }
                }
            }
            # format path to expected file
            tfwork_file_path = \
                os.path.join(test_tfwork_dir, 'terraform.tf')
            with common.create_test_working_dir() as test_working_dir:
                lib.concourse.do_out(
                    input_payload=test_payload,
                    working_dir_path=test_working_dir,
                    tfwork_dir_path=test_tfwork_dir)
                self.assertTrue(os.path.exists(tfwork_file_path))


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

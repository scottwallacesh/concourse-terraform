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
    def test_out_plan_with_unspecified_terraform_dir(self):
        # create a new temp dir as the tfwork dir
        with common.create_test_working_dir() as test_tfwork_dir:
            # create a test payload
            test_payload = {
                'source': {
                    'backend_type': 'local'
                },
                'params': {
                    'action': 'plan',
                    'plan': {}
                }
            }
            with common.create_test_working_dir() as test_working_dir:
                with self.assertRaises(KeyError):
                    lib.concourse.do_out(
                        input_payload=test_payload,
                        working_dir_path=test_working_dir,
                        tfwork_dir_path=test_tfwork_dir)

    def test_out_plan_destroys_existing_tfwork_terraform_dir(self):
        # create a new temp dir as the tfwork dir
        with common.create_test_working_dir() as test_tfwork_dir:
            # create the tfwork terraform dir
            os.mkdir(os.path.join(
                test_tfwork_dir, lib.concourse.TFWORK_TERRAFORM_DIR_NAME))
            # create an existing file in it
            tfwork_file_path = \
                os.path.join(
                    test_tfwork_dir,
                    lib.concourse.TFWORK_TERRAFORM_DIR_NAME,
                    'file.txt')
            with open(tfwork_file_path, 'w') as tfwork_file:
                tfwork_file.write('hello world')
            # create a test payload
            test_payload = {
                'source': {
                    'backend_type': 'local'
                },
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
                'source': {
                    'backend_type': 'local'
                },
                'params': {
                    'action': 'plan',
                    'plan': {
                        'terraform_dir': common.TEST_TERRAFORM_DIR
                    }
                }
            }
            # format file path with expected location
            tfwork_file_path = \
                os.path.join(
                    test_tfwork_dir,
                    lib.concourse.TFWORK_TERRAFORM_DIR_NAME,
                    'terraform.tf')
            with common.create_test_working_dir() as test_working_dir:
                lib.concourse.do_out(
                    input_payload=test_payload,
                    working_dir_path=test_working_dir,
                    tfwork_dir_path=test_tfwork_dir)
                self.assertTrue(os.path.exists(tfwork_file_path))

    def test_out_plan_supports_relative_paths_to_terraform_dir(self):
        # create a new temp dir as the concourse working dir
        with common.create_test_working_dir() as concourse_working_dir:
            # create the terraform dir
            dummy_tf_dir = os.path.join(concourse_working_dir, 'tfdummy')
            os.mkdir(dummy_tf_dir)
            # create a dummy file in the tfdummy dir
            dummy_tf_file_path = \
                os.path.join(
                    concourse_working_dir,
                    'tfdummy',
                    'dummy.tf')
            with open(dummy_tf_file_path, 'w') as dummy_tf_file:
                dummy_tf_file.write('variable "dummy" {}')
            # create a new temp dir as the tfwork dir
            with common.create_test_working_dir() as test_tfwork_dir:
                # create a test payload
                test_payload = {
                    'source': {
                        'backend_type': 'local'
                    },
                    'params': {
                        'action': 'plan',
                        'plan': {
                            'terraform_dir': 'tfdummy'
                        }
                    }
                }
                # format file path with expected location
                tfwork_file_path = \
                    os.path.join(
                        test_tfwork_dir,
                        lib.concourse.TFWORK_TERRAFORM_DIR_NAME,
                        'dummy.tf')
                lib.concourse.do_out(
                    input_payload=test_payload,
                    working_dir_path=concourse_working_dir,
                    tfwork_dir_path=test_tfwork_dir)
                self.assertTrue(os.path.exists(tfwork_file_path))

    def test_out_plan_with_no_plan_file(self):
        # create a new temp dir as the tfwork dir
        with common.create_test_working_dir() as test_tfwork_dir:
            # create a test payload
            test_payload = {
                'source': {
                    'backend_type': 'local'
                },
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


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

# stdlib
import os
import tempfile
import unittest
import unittest.mock


# local
import lib.ssh_keys


TEST_SSH_KEY_FILE_PATH_FOO = '/app/testdata/ssh-keys/foo'
TEST_SSH_KEY_FILE_PATH_BAR = '/app/testdata/ssh-keys/bar'


# =============================================================================
#
# test classes
#
# =============================================================================

class TestSshKeys(unittest.TestCase):
    def test_extracts_ssh_key_file_paths_from_environment(self):
        test_ssh_key_name = 'foo'
        test_ssh_key_path = TEST_SSH_KEY_FILE_PATH_FOO
        ssh_key_file_path_var = \
            lib.ssh_keys.SSH_KEY_FILE_VAR_PREFIX + test_ssh_key_name
        test_environment = {
            ssh_key_file_path_var: test_ssh_key_path
        }
        test_ssh_key_file_paths = \
            lib.ssh_keys.extract_ssh_key_paths(test_environment)
        self.assertIn(test_ssh_key_name, test_ssh_key_file_paths)
        self.assertEqual(
            test_ssh_key_file_paths[test_ssh_key_name],
            test_ssh_key_path)

    def test_copies_ssh_keys_to_ssh_keys_directory(self):
        test_ssh_key_file_paths = {
            'foo': TEST_SSH_KEY_FILE_PATH_FOO,
            'bar': TEST_SSH_KEY_FILE_PATH_BAR
        }
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.install_ssh_key_files(
                test_ssh_key_file_paths, temp_ssh_keys_dir)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_ssh_keys_dir,
                        'foo.pem')))
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_ssh_keys_dir,
                        'bar.pem')))

    def test_extracts_ssh_key_values_from_environment(self):
        test_ssh_key_name = 'foo'
        test_ssh_key_value = 'foo-value'
        ssh_key_value_var = \
            lib.ssh_keys.SSH_KEY_VAR_PREFIX + test_ssh_key_name
        test_environment = {
            ssh_key_value_var: test_ssh_key_value
        }
        test_ssh_keys = \
            lib.ssh_keys.extract_ssh_keys(test_environment)
        self.assertIn(test_ssh_key_name, test_ssh_keys)
        self.assertEqual(
            test_ssh_keys[test_ssh_key_name],
            test_ssh_key_value)

    def test_writes_ssh_keys_to_ssh_keys_directory(self):
        test_ssh_key_values = {
            'foo': 'foo-value',
            'bar': 'bar-value'
        }
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.install_ssh_keys(
                test_ssh_key_values, temp_ssh_keys_dir)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_ssh_keys_dir,
                        'foo.pem')))
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_ssh_keys_dir,
                        'bar.pem')))

    def test_writes_ssh_key_config(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.create_ssh_config(temp_ssh_keys_dir)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_ssh_keys_dir,
                        'config')))

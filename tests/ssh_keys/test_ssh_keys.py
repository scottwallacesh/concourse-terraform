#!/usr/bin/env python3

# stdlib
import os
import stat
import tempfile
import unittest
import unittest.mock


# local
import lib.ssh_keys


TEST_SSH_KEY_FILE_PATH = '/app/testdata/ssh-keys/foo'
TEST_SSH_KEY_VALUE = 'foo'


both_env_vars_set = {
    lib.ssh_keys.SSH_KEY_FILE_VAR: TEST_SSH_KEY_FILE_PATH,
    lib.ssh_keys.SSH_KEY_VALUE_VAR: TEST_SSH_KEY_VALUE
}

var_value_set = {
    lib.ssh_keys.SSH_KEY_VALUE_VAR: TEST_SSH_KEY_VALUE
}

file_path_set = {
    lib.ssh_keys.SSH_KEY_FILE_VAR: TEST_SSH_KEY_FILE_PATH
}


# =============================================================================
#
# test classes
#
# =============================================================================


class when_setting_ssh_key_from_var_value_and_file_path(unittest.TestCase):
    def test_it_throws_a_runtime_error(self):
        with self.assertRaises(RuntimeError):
            lib.ssh_keys.main(both_env_vars_set)


class when_setting_ssh_key_from_var_value(unittest.TestCase):
    def test_it_creates_the_ssh_key_file(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            self.assertTrue(os.path.exists(ssh_key_file_path))

    def test_it_sets_the_ssh_key_file_permissions(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            # check for owner read/write
            self.assertTrue(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IRUSR | stat.S_IWUSR
                ))
            )
            # check for group read/write
            self.assertFalse(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IRGRP | stat.S_IWGRP
                ))
            )
            # check for other read/write
            self.assertFalse(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IROTH | stat.S_IWOTH
                ))
            )
            # check for owner execute
            self.assertFalse(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IXUSR
                ))
            )
            # check for group execute
            self.assertFalse(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IXGRP
                ))
            )
            # check for other execute
            self.assertFalse(
                bool(os.stat(ssh_key_file_path).st_mode & (
                    stat.S_IXOTH
                ))
            )

    def test_it_writes_the_var_value_to_the_ssh_key_file(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            with open(ssh_key_file_path, 'r') as ssh_key_file:
                ssh_key_file_contents = ssh_key_file.read()
            self.assertEqual(TEST_SSH_KEY_VALUE, ssh_key_file_contents)

    def test_it_ensures_the_ssh_keys_dir_exists(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_parent_dir:
            temp_ssh_keys_dir = os.path.join(temp_ssh_keys_parent_dir, 'foo')
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            self.assertTrue(os.path.exists(temp_ssh_keys_dir))

    def test_it_creates_an_ssh_config_file(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_config_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_CONFIG_FILE_NAME)
            self.assertTrue(os.path.exists(ssh_config_file_path))

    def test_it_sets_ssh_config_identityfile(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(var_value_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            ssh_config_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_CONFIG_FILE_NAME)
            with open(ssh_config_file_path, 'r') as ssh_config_file:
                ssh_config_file_contents = ssh_config_file.read()
            self.assertIn(
                f'IdentityFile {ssh_key_file_path}',
                ssh_config_file_contents)


class when_setting_ssh_key_from_var_file(unittest.TestCase):
    def test_it_creates_the_ssh_key_file(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(file_path_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            self.assertTrue(os.path.exists(ssh_key_file_path))

    def test_it_writes_the_file_contents_to_the_ssh_key_file(self):
        with tempfile.TemporaryDirectory() as temp_ssh_keys_dir:
            lib.ssh_keys.main(file_path_set, ssh_keys_dir=temp_ssh_keys_dir)
            ssh_key_file_path = os.path.join(
                temp_ssh_keys_dir,
                lib.ssh_keys.SSH_KEY_FILE_NAME)
            with open(TEST_SSH_KEY_FILE_PATH) as ssh_key_file:
                src_ssh_key_file_contents = ssh_key_file.read()
            with open(ssh_key_file_path, 'r') as ssh_key_file:
                dst_ssh_key_file_contents = ssh_key_file.read()
            self.assertEqual(
                src_ssh_key_file_contents,
                dst_ssh_key_file_contents)

#!/usr/bin/env python3

import os
import shutil
import stat
import sys

SSH_CONFIG_FILE_NAME = 'config'
SSH_KEY_FILE_VAR = 'CT_GIT_IDENTITY_FILE'
SSH_KEY_VALUE_VAR = 'CT_GIT_IDENTITY_VALUE'
SSH_KEY_FILE_NAME = 'git.pem'
SSH_KEYS_DIR_PATH = '/root/.ssh'


def log(message: str) -> None:
    print(f"[install-ssh-keys] {message}", file=sys.stderr)


def create_ssh_config(
        ssh_key_file_path: str,
        ssh_keys_dir: str) -> None:
    ssh_config_file_path = \
        os.path.join(
            ssh_keys_dir,
            SSH_CONFIG_FILE_NAME)
    ssh_config = 'StrictHostKeyChecking no\nLogLevel quiet\n'
    if os.path.exists(ssh_key_file_path):
        ssh_config += f'Host *\n    IdentityFile {ssh_key_file_path}\n'
    with open(ssh_config_file_path, 'w') as ssh_config_file:
        ssh_config_file.write(ssh_config)
    log(f"wrote ssh config to: {ssh_config_file_path}")


def main(environment: dict, ssh_keys_dir: str = None) -> None:
    # get vars from environment
    ssh_key_file_from_var = environment.get(SSH_KEY_FILE_VAR)
    ssh_key_value_from_var = environment.get(SSH_KEY_VALUE_VAR)

    # check if both are set
    if ssh_key_file_from_var and ssh_key_value_from_var:
        raise RuntimeError('cannot specify both ssh key file path and value')

    # prep ssh keys dir
    if not ssh_keys_dir:
        ssh_keys_dir = SSH_KEYS_DIR_PATH
    if not os.path.isdir(ssh_keys_dir):
        os.makedirs(ssh_keys_dir)

    # prep ssh key file path
    ssh_key_file_path = os.path.join(ssh_keys_dir, SSH_KEY_FILE_NAME)

    if ssh_key_value_from_var:
        # write value to file
        with open(ssh_key_file_path, 'w') as ssh_key_file:
            ssh_key_file.write(ssh_key_value_from_var)
    elif ssh_key_file_from_var:
        shutil.copyfile(ssh_key_file_from_var, ssh_key_file_path)

    # chmod ssh file if present
    if os.path.exists(ssh_key_file_path):
        os.chmod(ssh_key_file_path, stat.S_IRUSR | stat.S_IWUSR)

    # create ssh config
    create_ssh_config(ssh_key_file_path, ssh_keys_dir)


if __name__ == '__main__':
    main(os.environ)

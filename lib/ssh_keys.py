#!/usr/bin/env python3

import os
import shutil
import sys

SSH_KEY_VAR_PREFIX = 'CT_SSH_KEY_VALUE_'
SSH_KEY_FILE_VAR_PREFIX = 'CT_SSH_KEY_FILE_'
SSH_KEYS_DIR_PATH = '/root/.ssh'


def log(message: str) -> None:
    print(f"[install-ssh-keys] {message}", file=sys.stderr)


def extract_ssh_key_paths(environment: dict) -> dict:
    ssh_key_paths: dict = {}
    for key, value in environment.items():
        if key.startswith(SSH_KEY_FILE_VAR_PREFIX):
            # strip prefix and use the remainder as the key name
            key_name = key[len(SSH_KEY_FILE_VAR_PREFIX):]
            log(f"found ssh key file '{key_name}' path: {value}")
            ssh_key_paths[key_name] = value
    return ssh_key_paths


def install_ssh_key_files(
        ssh_key_paths: dict,
        ssh_keys_dir: str = None) -> None:
    if not ssh_keys_dir:
        ssh_keys_dir = SSH_KEYS_DIR_PATH
    if not os.path.isdir(ssh_keys_dir):
        os.makedirs(ssh_keys_dir)
    for ssh_key_name, ssh_key_src_path in ssh_key_paths.items():
        ssh_key_dest_path = \
            os.path.join(
                ssh_keys_dir,
                ssh_key_name + '.pem')
        shutil.copyfile(ssh_key_src_path, ssh_key_dest_path)
        os.chmod(ssh_key_dest_path, 400)
        log(f"installed ssh key '{ssh_key_name}' to: {ssh_key_dest_path}")


def extract_ssh_keys(environment: dict) -> dict:
    ssh_keys: dict = {}
    for key, value in environment.items():
        if key.startswith(SSH_KEY_VAR_PREFIX):
            # strip prefix and use the remainder as the key name
            key_name = key[len(SSH_KEY_VAR_PREFIX):]
            log(f"found ssh key '{key_name}'")
            ssh_keys[key_name] = value
    return ssh_keys


def install_ssh_keys(ssh_keys: dict, ssh_keys_dir: str = None) -> None:
    if not ssh_keys_dir:
        ssh_keys_dir = SSH_KEYS_DIR_PATH
    if not os.path.isdir(ssh_keys_dir):
        os.makedirs(ssh_keys_dir)
    for ssh_key_name, ssh_key_value in ssh_keys.items():
        ssh_key_dest_path = \
            os.path.join(
                ssh_keys_dir,
                ssh_key_name + '.pem')
        with open(ssh_key_dest_path, 'w') as ssh_key_file:
            ssh_key_file.write(ssh_key_value)
        os.chmod(ssh_key_dest_path, 400)
        log(f"installed ssh key '{ssh_key_name}' to: {ssh_key_dest_path}")


def create_ssh_config(ssh_keys_dir: str = None) -> None:
    if not ssh_keys_dir:
        ssh_keys_dir = SSH_KEYS_DIR_PATH
    if not os.path.isdir(ssh_keys_dir):
        os.makedirs(ssh_keys_dir)
    ssh_config_file_path = \
        os.path.join(
            ssh_keys_dir,
            'config')
    with open(ssh_config_file_path, 'w') as ssh_config_file:
        ssh_config_file.write(
            'StrictHostKeyChecking no'
            'LogLevel quiet'
        )
    log(f"wrote ssh config to: {ssh_config_file_path}")


def main(environment: dict) -> None:
    ssh_key_paths = extract_ssh_key_paths(environment)
    if ssh_key_paths:
        install_ssh_key_files(ssh_key_paths)
    ssh_keys = extract_ssh_keys(environment)
    if ssh_keys:
        install_ssh_keys(ssh_keys)
    create_ssh_config()


if __name__ == '__main__':
    main(os.environ)

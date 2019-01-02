#!/usr/bin/env python3

import os
import json
import sys

CONSUL_CONFIG_VAR_PREFIX = 'CT_CONSUL_TF_CONFIG_'
CONSUL_CONFIG_DIR_PATH = '/consul/config'


def log(message: str) -> None:
    print(f"[consul-config] {message}", file=sys.stderr)


def extract_tf_output_paths(environment: dict) -> dict:
    tf_output_paths: dict = {}
    for key, value in environment.items():
        if key.startswith(CONSUL_CONFIG_VAR_PREFIX):
            # strip prefix and use the remainder as the key name
            key_name = key[len(CONSUL_CONFIG_VAR_PREFIX):]
            log(f"input config '{key_name}' path: {value}")
            tf_output_paths[key_name] = value
    return tf_output_paths


def process_tf_output(config_name: str, tf_output: dict) -> dict:
    consul_config: dict = {}
    # look for 'value' key, indicating this is
    # just a single output item
    if 'value' in tf_output:
        # since it's just a single item
        # use the config name as the key name
        consul_config[config_name] = tf_output['value']
    else:
        # multiple items, look for 'value' in each
        for key, value in tf_output.items():
            if value and 'value' in value:
                consul_config[key] = value['value']
    return consul_config


def process_tf_output_paths(tf_output_paths: dict) -> dict:
    for key, value in tf_output_paths.items():
        with open(value, 'r') as tf_output_file:
            tf_output = json.load(tf_output_file)
            consul_config = process_tf_output(key, tf_output)
            consul_config_file_path = os.path.join(CONSUL_CONFIG_DIR_PATH,
                                                   f"{key}.json")
        with open(consul_config_file_path, 'w') as consul_config_file:
            json.dump(consul_config, consul_config_file)
        log(f"wrote config {consul_config_file_path}")


def main(environment: dict) -> None:
    tf_output_paths = extract_tf_output_paths(environment)
    if tf_output_paths:
        process_tf_output_paths(tf_output_paths)


if __name__ == '__main__':
    main(os.environ)

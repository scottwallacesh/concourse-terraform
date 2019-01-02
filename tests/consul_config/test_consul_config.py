#!/usr/bin/env python3

# stdlib
import unittest


# local
import lib.consul_config


# =============================================================================
#
# test classes
#
# =============================================================================

class TestConsulConfig(unittest.TestCase):
    def test_extracts_tf_output_path_using_env_var_name(self):
        test_config_name = 'test_example'
        test_config_path = '/tmp/fake_example_path.json'
        config_path_var = \
            lib.consul_config.CONSUL_CONFIG_VAR_PREFIX + test_config_name
        test_environment = {
            config_path_var: test_config_path
        }
        test_tf_output_paths = \
            lib.consul_config.extract_tf_output_paths(test_environment)
        self.assertIn(test_config_name, test_tf_output_paths)
        self.assertEqual(
            test_tf_output_paths[test_config_name],
            test_config_path)

    def test_processes_tf_output_with_single_item(self):
        test_config_name = 'test_example'
        test_config_value = [
            'test_value_a',
            'test_value_b'
        ]
        test_tf_output = {
            'sensitive': False,
            'type': 'list',
            'value': test_config_value
        }
        test_consul_config = \
            lib.consul_config.process_tf_output(test_config_name,
                                                test_tf_output)
        self.assertIn(test_config_name, test_consul_config)
        self.assertEqual(test_consul_config[test_config_name],
                         test_config_value)

    def test_processes_tf_output_with_multiple_items(self):
        test_config_name = 'test_example'
        test_config_name_a = 'foo'
        test_config_value_a = [
            'test_value_a',
            'test_value_b'
        ]
        test_config_name_b = 'bar'
        test_config_value_b = 'hello world'
        test_tf_output = {
            test_config_name_a: {
                'sensitive': False,
                'type': 'list',
                'value': test_config_value_a
            },
            test_config_name_b: {
                'sensitive': False,
                'type': 'string',
                'value': test_config_value_b
            }
        }
        test_consul_config = \
            lib.consul_config.process_tf_output(test_config_name,
                                                test_tf_output)
        self.assertIn(test_config_name_a, test_consul_config)
        self.assertEqual(test_consul_config[test_config_name_a],
                         test_config_value_a)
        self.assertIn(test_config_name_b, test_consul_config)
        self.assertEqual(test_consul_config[test_config_name_b],
                         test_config_value_b)

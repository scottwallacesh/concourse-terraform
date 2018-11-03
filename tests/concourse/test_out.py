#!/usr/bin/env python3

# stdlib
import unittest

# local
import lib.concourse
import tests.concourse.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class TestOut(unittest.TestCase):
    def test_out_with_unspecified_backend(self):
        test_payload = {
            'source': {},
            'params': {}
        }
        test_working_dir_path = '.'
        with self.assertRaises(KeyError):
            lib.concourse.do_out(
                input_payload=test_payload,
                working_dir_path=test_working_dir_path)

    def test_out_with_unsupported_action(self):
        test_payload = {
            'source': {
                'backend_type': 'local'
            },
            'params': {
                'action': 'invalid'
            }
        }
        test_working_dir_path = '.'
        with self.assertRaises(ValueError):
            lib.concourse.do_out(
                input_payload=test_payload,
                working_dir_path=test_working_dir_path)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

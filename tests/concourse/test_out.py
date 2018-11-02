#!/usr/bin/env python3

# stdlib
import unittest

# local
import lib.concourse


# =============================================================================
#
# test classes
#
# =============================================================================

class TestOut(unittest.TestCase):
    def test_out_with_unsupported_backend(self):
        test_payload = {
            'params': {
                'backend_type': 'invalid'
            }
        }
        test_working_dir_path = '.'
        with self.assertRaises(ValueError):
            lib.concourse.do_out(
                input_payload=test_payload,
                working_dir_path=test_working_dir_path)

    def test_out_with_unsupported_action(self):
        test_payload = {
            'params': {
                'action': 'invalid'
            }
        }
        test_working_dir_path = '.'
        with self.assertRaises(ValueError):
            lib.concourse.do_out(
                input_payload=test_payload,
                working_dir_path=test_working_dir_path)

    def test_out_plan_create(self):
        test_payload = {
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

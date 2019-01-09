#!/usr/bin/env python3

# stdlib
import os
import tempfile
import unittest


# local
import lib.trusted_ca_certs


TEST_CA_CERT_FILE_PATH_FOO = '/app/testdata/trusted-ca-certs/foo.pem'
TEST_CA_CERT_FILE_PATH_BAR = '/app/testdata/trusted-ca-certs/bar.pem'
TEST_SYSTEM_CA_CERT_FILE_PATH = '/etc/ssl/certs/ca-certificates.crt'


# =============================================================================
#
# test classes
#
# =============================================================================

class TestTrustedCACerts(unittest.TestCase):
    def test_extracts_ca_cert_paths_from_environment(self):
        test_ca_name = 'foo_ca'
        test_ca_path = TEST_CA_CERT_FILE_PATH_FOO
        ca_cert_path_var = \
            lib.trusted_ca_certs.TRUSTED_CA_CERTS_VAR_PREFIX + test_ca_name
        test_environment = {
            ca_cert_path_var: test_ca_path
        }
        test_ca_cert_paths = \
            lib.trusted_ca_certs.extract_ca_cert_paths(test_environment)
        self.assertIn(test_ca_name, test_ca_cert_paths)
        self.assertEqual(
            test_ca_cert_paths[test_ca_name],
            test_ca_path)

    def test_copies_ca_certs_to_ca_directory(self):
        test_ca_cert_paths = {
            'foo_ca': TEST_CA_CERT_FILE_PATH_FOO,
            'bar_ca': TEST_CA_CERT_FILE_PATH_BAR
        }
        with tempfile.TemporaryDirectory() as temp_certs_dir:
            lib.trusted_ca_certs.install_ca_certs(
                test_ca_cert_paths, temp_certs_dir)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_certs_dir,
                        'foo_ca.crt')))
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        temp_certs_dir,
                        'bar_ca.crt')))

    def test_updates_ca_certificates(self):
        # this test has a side effect
        # it actually installs the certs into the system's root store
        test_ca_cert_paths = {
            'foo_ca': TEST_CA_CERT_FILE_PATH_FOO,
            'bar_ca': TEST_CA_CERT_FILE_PATH_BAR
        }
        lib.trusted_ca_certs.install_ca_certs(test_ca_cert_paths)
        lib.trusted_ca_certs.update_ca_certificates()
        with open(TEST_CA_CERT_FILE_PATH_FOO) as test_ca_cert_foo:
            test_ca_cert_foo_contents = test_ca_cert_foo.read()
        with open(TEST_CA_CERT_FILE_PATH_BAR) as test_ca_cert_bar:
            test_ca_cert_bar_contents = test_ca_cert_bar.read()
        with open(TEST_SYSTEM_CA_CERT_FILE_PATH) as test_system_ca_cert:
            test_system_ca_cert_contents = test_system_ca_cert.read()
        self.assertIn(test_ca_cert_foo_contents, test_system_ca_cert_contents)
        self.assertIn(test_ca_cert_bar_contents, test_system_ca_cert_contents)

#!/usr/bin/env python3

# stdlib
import os
import tarfile
import unittest

# local
import lib.terraform_dir
import tests.terraform_dir.common as common


# =============================================================================
#
# test classes
#
# =============================================================================

class ArchiveTerraformDir(unittest.TestCase):
    def test_creates_archive_of_terraform_dir(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create a new temp dir as the archive output dir
            with common.create_test_working_dir() as archive_output_dir:
                # archive
                archive_file_path = lib.terraform_dir.archive_terraform_dir(
                    terraform_dir,
                    archive_output_dir,
                    debug=True)
                # assert the file was created
                self.assertTrue(os.path.exists(archive_file_path))
                # assert that the terraform file exists in the archive
                expected_terraform_archive_file = \
                    os.path.join(
                        lib.terraform_dir.TERRAFORM_DIR_NAME,
                        common.TEST_TERRAFORM_FILE_NAME)
                with tarfile.open(archive_file_path, 'r:gz') as archive_file:
                    archive_file.debug = 3
                    self.assertIn(
                        expected_terraform_archive_file,
                        archive_file.getnames())


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

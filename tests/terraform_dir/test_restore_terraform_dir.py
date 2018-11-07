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

class RestoreTerraformDir(unittest.TestCase):
    def test_requires_archive_input_dir(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            with self.assertRaises(ValueError):
                # archive with empty string as the archive input dir
                lib.terraform_dir.restore_terraform_dir(
                    '',
                    terraform_work_dir=test_working_dir,
                    debug=True)

    def test_raises_when_multiple_archives_are_present(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # create a new temp dir as the archive output dir
            with common.create_test_working_dir() as archive_output_dir:
                # file paths for mock archives
                archive_file_path_a = \
                    os.path.join(archive_output_dir, 'terraform-a.tar.gz')
                archive_file_path_b = \
                    os.path.join(archive_output_dir, 'terraform-b.tar.gz')
                # write the mock archive files
                archive_file_a = tarfile.open(archive_file_path_a, 'w')
                archive_file_a.close()
                archive_file_b = tarfile.open(archive_file_path_b, 'w')
                archive_file_b.close()
                # restore the archive
                with self.assertRaises(FileExistsError):
                    lib.terraform_dir.restore_terraform_dir(
                        archive_output_dir,
                        terraform_work_dir=test_working_dir,
                        debug=True)

    def test_raises_when_no_archives_are_present(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # create a new temp dir as the archive output dir
            with common.create_test_working_dir() as archive_output_dir:
                # restore the archive
                with self.assertRaises(FileNotFoundError):
                    lib.terraform_dir.restore_terraform_dir(
                        archive_output_dir,
                        terraform_work_dir=test_working_dir,
                        debug=True)

    def test_restores_archive_of_terraform_dir(self):
        # create a new temp dir as the working dir
        with common.create_test_working_dir() as test_working_dir:
            # get the test terraform file contents
            with open(common.TEST_TERRAFORM_FILE_PATH, 'r') as terraform_file:
                terraform_file_contents = terraform_file.read()
            # init the terraform dir
            terraform_dir = lib.terraform_dir.init_terraform_dir(
                common.TEST_TERRAFORM_DIR,
                terraform_work_dir=test_working_dir,
                debug=True
            )
            # create a new temp dir as the archive output dir
            with common.create_test_working_dir() as archive_output_dir:
                # archive
                lib.terraform_dir.archive_terraform_dir(
                    terraform_dir,
                    archive_output_dir,
                    debug=True)
                # restore the archive
                restored_terraform_dir = \
                    lib.terraform_dir.restore_terraform_dir(
                        archive_output_dir,
                        terraform_work_dir=test_working_dir,
                        debug=True)
                # assert that it returned a directory path
                self.assertTrue(os.path.isdir(restored_terraform_dir))
                # get the extracted terraform file contents
                extracted_terraform_file_path = \
                    os.path.join(
                        terraform_dir,
                        common.TEST_TERRAFORM_FILE_NAME)
                with open(extracted_terraform_file_path, 'r') \
                        as terraform_file:
                    extracted_terraform_file_contents = terraform_file.read()
                # assert that the file contents match
                self.assertEqual(
                    terraform_file_contents,
                    extracted_terraform_file_contents)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    unittest.main()

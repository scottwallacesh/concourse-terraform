# stdlib
import os
import tempfile

# =============================================================================
#
# constants
#
# =============================================================================

TEST_ROOT_DIR = '/app'
RELATIVE_TEST_TERRAFORM_DIR = 'testdata/terraform'
TEST_TERRAFORM_DIR = os.path.join(TEST_ROOT_DIR, RELATIVE_TEST_TERRAFORM_DIR)
TEST_TERRAFORM_FILE_NAME = 'terraform.tf'
TEST_TERRAFORM_FILE_PATH = \
    os.path.join(TEST_TERRAFORM_DIR, TEST_TERRAFORM_FILE_NAME)


# =============================================================================
#
# test helpers
#
# =============================================================================

# =============================================================================
# create_test_working_dir
# =============================================================================
def create_test_working_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()

# stdlib
import os
import tempfile
import unittest.mock

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
TEST_STATE_DIR = '/app/testdata/terraform-state'
TEST_STATE_FILE_WITH_KEY = \
    os.path.join(TEST_STATE_DIR, 'with-key.tfstate')
TEST_STATE_FILE_WITHOUT_KEY = \
    os.path.join(TEST_STATE_DIR, 'without-key.tfstate')
TEST_STATE_FILE_WITH_OUTPUT = \
    os.path.join(TEST_STATE_DIR, 'with-output.tfstate')
TEST_INVALID_TERRAFORM_DIR = \
    os.path.join(TEST_ROOT_DIR, 'testdata/terraform-fail')
TEST_TERRAFORM_AUX_DIR = \
    os.path.join(TEST_ROOT_DIR, 'testdata/terraform-aux')
TEST_TERRAFORM_AUX_FILE_NAME = 'aux.txt'
TEST_TERRAFORM_VAR_DIR = \
    os.path.join(TEST_ROOT_DIR, 'testdata/terraform-var')
TEST_TERRAFORM_SINGLE_OUTPUT_VAR_FILE_PATH = \
    os.path.join(TEST_TERRAFORM_VAR_DIR, 'single-output.json')
TEST_TERRAFORM_MULTI_OUTPUT_VAR_FILE_PATH = \
    os.path.join(TEST_TERRAFORM_VAR_DIR, 'multi-output.json')
TEST_TERRAFORM_CONVERTED_SINGLE_OUTPUT_VAR_FILE_PATH = \
    os.path.join(TEST_TERRAFORM_VAR_DIR, 'algorithm.tfvars.json')
TEST_TERRAFORM_CONVERTED_MULTI_OUTPUT_VAR_FILE_PATH = \
    os.path.join(TEST_TERRAFORM_VAR_DIR, 'multi.tfvars.json')


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


# =============================================================================
# mocked_env_vars
# =============================================================================
def mocked_env_vars(env_vars: dict) -> dict:
    return unittest.mock.patch.dict(
        'os.environ',
        env_vars)

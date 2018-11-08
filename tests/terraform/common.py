# stdlib
import os
import shutil
import tempfile

# local
import lib.terraform

# =============================================================================
#
# constants
#
# =============================================================================

TEST_TERRAFORM_DIR = '/app/testdata/terraform'
TEST_STATE_DIR = '/app/testdata/terraform-state'
TEST_STATE_FILE_WITH_KEY = \
    os.path.join(TEST_STATE_DIR, 'with-key.tfstate')
TEST_STATE_FILE_WITHOUT_KEY = \
    os.path.join(TEST_STATE_DIR, 'without-key.tfstate')
TEST_PLAN_FILE_NAME = '.tfplan'


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
# copy_state_file
# =============================================================================
def copy_state_file(source: str, dest: str) -> str:
    return shutil.copy2(source, dest)


# =============================================================================
# init_test_working_dir
# =============================================================================
def init_test_working_dir(test_working_dir: str) -> None:
    lib.terraform.init(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# create_plan_with_no_output
# =============================================================================
def create_plan_with_no_output(test_working_dir: str) -> None:
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# create_plan_with_existing_state
# =============================================================================
def create_plan_with_existing_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITH_KEY, test_state_dir)
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        debug=True)


# =============================================================================
# create_plan_with_existing_empty_state
# =============================================================================
def create_plan_with_existing_empty_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITHOUT_KEY, test_state_dir)
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        debug=True)


# =============================================================================
# create_plan_destroy_with_existing_state
# =============================================================================
def create_plan_destroy_with_existing_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITH_KEY, test_state_dir)
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        destroy=True,
        debug=True)


# =============================================================================
# create_plan_destroy_with_existing_empty_state
# =============================================================================
def create_plan_destroy_with_existing_empty_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITHOUT_KEY, test_state_dir)
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        destroy=True,
        debug=True)


# =============================================================================
# create_plan_with_no_output_allow_no_changes
# =============================================================================
def create_plan_with_no_output_allow_no_changes(test_working_dir: str) -> None:
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        error_on_no_changes=False,
        debug=True)


# =============================================================================
# create_plan_destroy_with_no_output_allow_no_changes
# =============================================================================
def create_plan_destroy_with_no_output_allow_no_changes(
        test_working_dir: str) -> None:
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        error_on_no_changes=False,
        destroy=True,
        debug=True)


# =============================================================================
# create_plan_file
# =============================================================================
def create_plan_file(test_working_dir: str) -> None:
    lib.terraform.plan(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        create_plan_file=True,
        plan_file_path=TEST_PLAN_FILE_NAME,
        debug=True)


# =============================================================================
# show_plan_file
# =============================================================================
def show_plan_file(test_working_dir: str) -> None:
    lib.terraform.show(
        test_working_dir,
        TEST_PLAN_FILE_NAME,
        debug=True)


# =============================================================================
# apply_with_no_plan
# =============================================================================
def apply_with_no_plan(test_working_dir: str) -> None:
    lib.terraform.apply(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# apply_with_no_plan_with_existing_state
# =============================================================================
def apply_with_no_plan_with_existing_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITH_KEY, test_state_dir)
    lib.terraform.apply(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        debug=True)


# =============================================================================
# apply_with_no_plan_with_existing_empty_state
# =============================================================================
def apply_with_no_plan_with_existing_empty_state(
        test_working_dir: str,
        test_state_dir: str) -> None:
    test_state_file_path = \
        copy_state_file(TEST_STATE_FILE_WITHOUT_KEY, test_state_dir)
    lib.terraform.apply(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        state_file_path=test_state_file_path,
        debug=True)


# =============================================================================
# apply_plan_file
# =============================================================================
def apply_plan_file(test_working_dir: str) -> None:
    lib.terraform.apply(
        test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        plan_file_path=TEST_PLAN_FILE_NAME,
        debug=True)

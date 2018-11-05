# stdlib
import tempfile

# local
import lib.terraform

# =============================================================================
#
# constants
#
# =============================================================================

TEST_TERRAFORM_DIR = '/app/testdata/terraform'
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
# init_test_working_dir
# =============================================================================
def init_test_working_dir(test_working_dir: str) -> None:
    lib.terraform.init(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# create_plan_with_no_output
# =============================================================================
def create_plan_with_no_output(test_working_dir: str) -> None:
    lib.terraform.plan(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# create_plan_with_no_output_allow_no_changes
# =============================================================================
def create_plan_with_no_output_allow_no_changes(test_working_dir: str) -> None:
    lib.terraform.plan(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        error_on_no_changes=False,
        debug=True)


# =============================================================================
# create_plan_file
# =============================================================================
def create_plan_file(test_working_dir: str) -> None:
    lib.terraform.plan(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        create_plan_file=True,
        plan_file_path=TEST_PLAN_FILE_NAME,
        debug=True)


# =============================================================================
# show_plan_file
# =============================================================================
def show_plan_file(test_working_dir: str) -> None:
    lib.terraform.show(
        working_dir_path=test_working_dir,
        plan_file_path=TEST_PLAN_FILE_NAME,
        debug=True)


# =============================================================================
# apply_with_no_plan
# =============================================================================
def apply_with_no_plan(test_working_dir: str) -> None:
    lib.terraform.apply(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        debug=True)


# =============================================================================
# apply_plan_file
# =============================================================================
def apply_plan_file(test_working_dir: str) -> None:
    lib.terraform.apply(
        working_dir_path=test_working_dir,
        terraform_dir_path=TEST_TERRAFORM_DIR,
        plan_file_path=TEST_PLAN_FILE_NAME,
        debug=True)

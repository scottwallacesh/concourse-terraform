# stdlib
from typing import Optional

# local
import lib.terraform_dir

# =============================================================================
# constants
# =============================================================================

PLAN = 'plan'
APPLY = 'apply'
CREATE_PLAN = 'create-plan'
SHOW_PLAN = 'show-plan'
APPLY_PLAN = 'apply-plan'
COMMANDS = [
    PLAN,
    APPLY,
    CREATE_PLAN,
    SHOW_PLAN,
    APPLY_PLAN
]


# =============================================================================
# plan
# =============================================================================
def plan(
        terraform_source_dir: str,
        terraform_dir_path: Optional[str] = None,
        state_file_path: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        destroy: Optional[bool] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    lib.terraform_dir.plan_terraform_dir(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        state_file_path=state_file_path,
        error_on_no_changes=error_on_no_changes,
        destroy=destroy,
        debug=debug)


# =============================================================================
# apply
# =============================================================================
def apply(
        terraform_source_dir: str,
        terraform_dir_path: Optional[str] = None,
        state_file_path: Optional[str] = None,
        state_output_dir: Optional[str] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    lib.terraform_dir.apply_terraform_dir(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        state_file_path=state_file_path,
        state_output_dir=state_output_dir,
        debug=debug)


# =============================================================================
# create_plan
# =============================================================================
def create_plan(
        terraform_source_dir: str,
        archive_output_dir: str,
        plan_file_path: Optional[str] = None,
        terraform_dir_path: Optional[str] = None,
        state_file_path: Optional[str] = None,
        source_ref: Optional[str] = None,
        source_ref_file: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        destroy: Optional[bool] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    lib.terraform_dir.plan_terraform_dir(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        create_plan_file=True,
        plan_file_path=plan_file_path,
        state_file_path=state_file_path,
        error_on_no_changes=error_on_no_changes,
        destroy=destroy,
        debug=debug)
    lib.terraform_dir.archive_terraform_dir(
        terraform_dir,
        archive_output_dir,
        source_ref=source_ref,
        source_ref_file=source_ref_file,
        debug=debug)


# =============================================================================
# show_plan
# =============================================================================
def show_plan(
        archive_input_dir: str,
        plan_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.restore_terraform_dir(
        archive_input_dir,
        debug=debug)
    lib.terraform_dir.show_terraform_plan(
        terraform_dir,
        plan_file_path=plan_file_path,
        debug=debug)


# =============================================================================
# apply_plan
# =============================================================================
def apply_plan(
        archive_input_dir: str,
        state_output_dir: Optional[str] = None,
        plan_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.restore_terraform_dir(
        archive_input_dir,
        debug=debug)
    lib.terraform_dir.apply_terraform_plan(
        terraform_dir,
        state_output_dir=state_output_dir,
        plan_file_path=plan_file_path,
        debug=debug)

# stdlib
from typing import Optional

# local
import lib.terraform_dir

# =============================================================================
# constants
# =============================================================================

PLAN = 'plan'
APPLY = 'apply'
COMMANDS = [PLAN, APPLY]


# =============================================================================
# plan
# =============================================================================
def plan(
        terraform_source_dir: str,
        terraform_dir_path: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    lib.terraform_dir.plan_terraform_dir(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        error_on_no_changes=error_on_no_changes,
        debug=debug)


# =============================================================================
# apply
# =============================================================================
def apply(
        terraform_source_dir: str,
        archive_output_dir: str,
        terraform_dir_path: Optional[str] = None,
        source_ref: Optional[str] = None,
        source_ref_file: Optional[str] = None,
        debug: bool = False) -> None:
    # create artifact on error
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    # try to apply
    try:
        lib.terraform_dir.apply_terraform_dir(
            terraform_dir,
            terraform_dir_path=terraform_dir_path,
            debug=debug)
    finally:
        # ensure the archive is created
        archive_file_path = lib.terraform_dir.archive_terraform_dir(
            terraform_dir,
            archive_output_dir,
            source_ref=source_ref,
            source_ref_file=source_ref_file,
            debug=debug)
        print(f"wrote archive to: {archive_file_path}")

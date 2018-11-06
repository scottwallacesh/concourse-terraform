# stdlib
from typing import Optional

# local
import lib.terraform_dir

# =============================================================================
# constants
# =============================================================================

PLAN = 'plan'


# =============================================================================
# plan
# =============================================================================
def plan(
        terraform_source_dir: str,
        backend_type: Optional[str] = None,
        backend_config_vars: Optional[dict] = None,
        terraform_dir_path: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        debug: bool = False) -> None:
    terraform_dir = lib.terraform_dir.init_terraform_dir(
        terraform_source_dir,
        backend_type=backend_type,
        backend_config_vars=backend_config_vars,
        terraform_dir_path=terraform_dir_path,
        debug=debug)
    lib.terraform_dir.plan_terraform_dir(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        error_on_no_changes=error_on_no_changes,
        debug=debug)

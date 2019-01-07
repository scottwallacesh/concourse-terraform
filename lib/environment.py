# stdlib
from typing import Optional


# =============================================================================
#
# constants
#
# =============================================================================

TERRAFORM_OUTPUT_VAR_FILE_PREFIX = 'TF_OUTPUT_VAR_FILE_'


# =============================================================================
#
# helper functions
#
# =============================================================================

# =============================================================================
# get_tf_output_var_files
# =============================================================================
def get_tf_output_var_files(environment: dict) -> Optional[dict]:
    output_var_files: dict = {}
    for key, value in environment.items():
        if key.startswith(TERRAFORM_OUTPUT_VAR_FILE_PREFIX):
            # strip prefix and use the remainder as the key name
            output_var_files[
                key[len(TERRAFORM_OUTPUT_VAR_FILE_PREFIX):]] = value
    return output_var_files or None

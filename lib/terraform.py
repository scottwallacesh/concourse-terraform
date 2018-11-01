# stdlib
import enum
import os
import subprocess
from typing import List

# local
from lib.log import log, log_pretty


# =============================================================================
#
# constants
#
# =============================================================================

TERRAFORM_BIN_FILE_PATH = 'terraform'


# =============================================================================
#
# classes
#
# =============================================================================

class TERRAFORM_EXIT_STATUS(enum.Enum):
    SUCCESS = 0
    SUCCESS_NO_CHANGES = 1
    SUCCESS_WITH_CHANGES = 2


# =============================================================================
#
# private utility functions
#
# =============================================================================

def _read_value_from_var_file(file_path: str, working_dir=None) -> str:
    # get original working directory
    original_working_dir = os.getcwd()
    # change to specified working dir
    if working_dir:
        os.chdir(working_dir)
    # read the contents of the var file
    with open(file_path) as var_file:
        var_value = var_file.read()
    # trim any trailing newline
    var_value = var_value.rstrip('\n')
    # change back to original working dir
    if os.getcwd() != original_working_dir:
        os.chdir(original_working_dir)
    return var_value


# =============================================================================
#
# private exe functions
#
# =============================================================================

# =============================================================================
# _terraform
# =============================================================================
def _terraform(
        *args: str,
        input=None,
        working_dir=None,
        error_on_no_changes=True) -> TERRAFORM_EXIT_STATUS:
    process_args = [
        TERRAFORM_BIN_FILE_PATH,
        *args
    ]
    # force 'TF_IN_AUTOMATION'
    os.environ['TF_IN_AUTOMATION'] = '1'
    exit_status = None
    # use Popen so we can read lines as they come
    with subprocess.Popen(
            process_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # redirect stderr to stdout
            bufsize=1,
            universal_newlines=True,
            stdin=input,
            cwd=working_dir) as pipe:
        for line in pipe.stdout:
            # log the output as it arrives
            log(line, end="")
    raise_error = False
    # check if we're using detailed exit codes
    if '-detailed-exitcode' in [arg.lower() for arg in args]:
        if pipe.returncode == 0:
            if error_on_no_changes:
                raise_error = True
            exit_status = TERRAFORM_EXIT_STATUS.SUCCESS_NO_CHANGES
        elif pipe.returncode == 2:
            exit_status = TERRAFORM_EXIT_STATUS.SUCCESS_WITH_CHANGES
        else:
            raise_error = True
    else:
        if pipe.returncode != 0:
            raise_error = True
        else:
            exit_status = TERRAFORM_EXIT_STATUS.SUCCESS
    # check if we need to raise an error
    if raise_error:
        # args are masked to prevent credentials leaking
        raise subprocess.CalledProcessError(
            pipe.returncode, [TERRAFORM_BIN_FILE_PATH])
    return exit_status


# =============================================================================
#
# public terraform functions
#
# =============================================================================

# =============================================================================
# version
# =============================================================================
def version() -> None:
    # execute version command
    _terraform('--version')


# =============================================================================
# init
# =============================================================================
def init(
        working_dir_path: str,
        terraform_dir_path: str = '.') -> None:
    terraform_command_args = []
    # execute plan args
    _terraform(
        'init',
        '-input=false',
        *terraform_command_args,
        terraform_dir_path,
        working_dir=working_dir_path)


# =============================================================================
# plan
# =============================================================================
def plan(
        working_dir_path: str,
        terraform_dir_path: str = '.',
        create_plan_file: bool = False,
        plan_file_path: str = None,
        error_on_no_changes: bool = True,
        args: list = []) -> None:
    terraform_command_args = []
    terraform_command_args.extend(args)
    if create_plan_file:
        # creating a plan file
        terraform_command_args.append(f"-out={plan_file_path}")
    elif plan_file_path:
        # viewing a plan file
        terraform_dir_path = plan_file_path
    # execute plan args
    _terraform(
        'plan',
        '-input=false',
        '-detailed-exitcode',
        *terraform_command_args,
        terraform_dir_path,
        working_dir=working_dir_path,
        error_on_no_changes=error_on_no_changes)


# =============================================================================
# apply
# =============================================================================
def apply(
        working_dir_path: str,
        terraform_dir_path: str = '.',
        plan_file_path: str = None,
        args: list = []) -> None:
    terraform_command_args = []
    terraform_command_args.extend(args)
    if plan_file_path:
        # applying a plan file
        terraform_dir_path = plan_file_path
    # execute plan args
    _terraform(
        'apply',
        '-input=false',
        *terraform_command_args,
        terraform_dir_path,
        working_dir=working_dir_path)


# # =============================================================================
# # validate
# # =============================================================================
# def validate(
#         working_dir_path: str,
#         template_file_path: str,
#         var_file_paths: List[str] = None,
#         vars: dict = None,
#         vars_from_files: dict = None,
#         debug: bool = False) -> None:
#     packer_command_args = []
#     # add any specified var file paths
#     if var_file_paths:
#         for var_file_path in var_file_paths:
#             packer_command_args.append(f"-var-file={var_file_path}")
#     # add any specified vars
#     if vars:
#         for var_name, var_value in vars.items():
#             packer_command_args.append(f"-var={var_name}={var_value}")
#     # add any vars from files
#     if vars_from_files:
#         for var_name, file_path in vars_from_files.items():
#             var_value = \
#                 _read_value_from_var_file(
#                     file_path,
#                     working_dir=working_dir_path)
#             packer_command_args.append(f"-var={var_name}={var_value}")
#     # dump args on debug
#     if debug:
#         log('validate args:')
#         log_pretty(packer_command_args)
#     # execute validate command
#     _packer(
#         'validate',
#         *packer_command_args,
#         template_file_path,
#         working_dir=working_dir_path)


# # =============================================================================
# # build
# # =============================================================================
# def build(
#         working_dir_path: str,
#         template_file_path: str,
#         var_file_paths: List[str] = None,
#         vars: dict = None,
#         vars_from_files: dict = None,
#         debug: bool = False) -> dict:
#     packer_command_args = []
#     # add any specified var file paths
#     if var_file_paths:
#         for var_file_path in var_file_paths:
#             packer_command_args.append(f"-var-file={var_file_path}")
#     # add any specified vars
#     if vars:
#         for var_name, var_value in vars.items():
#             packer_command_args.append(f"-var={var_name}={var_value}")
#     # add any vars from files
#     if vars_from_files:
#         for var_name, file_path in vars_from_files.items():
#             var_value = \
#                 _read_value_from_var_file(
#                     file_path,
#                     working_dir=working_dir_path)
#             packer_command_args.append(f"-var={var_name}={var_value}")
#     # dump args on debug
#     if debug:
#         log('build args:')
#         log_pretty(packer_command_args)
#     # execute build command
#     packer_command_result = _packer(
#         'build',
#         *packer_command_args,
#         template_file_path,
#         working_dir=working_dir_path)
#     # get build manifest from output
#     packer_build_manifest = \
#         _parse_packer_parsed_output_for_build_manifest(packer_command_result)
#     # return the manifest
#     return packer_build_manifest
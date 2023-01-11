# stdlib
import os
import subprocess
import sys
from typing import Any, Optional, IO


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

# =============================================================================
# TerraformNoChangesError
# =============================================================================
class TerraformNoChangesError(subprocess.CalledProcessError):
    pass


# =============================================================================
#
# private functions
#
# =============================================================================

# =============================================================================
# _dump_plugin_cache
# =============================================================================
def _dump_plugin_cache(plugin_cache_dir: str) -> None:
    for path, _, files in os.walk(plugin_cache_dir):
        print(f'[debug] plugin cache item: {path}')
        for f in files:
            print(f'[debug] plugin cache item: {os.path.join(path, f)}')


# =============================================================================
# _terraform
# =============================================================================
def _terraform(
        *args: str,
        terraform_dir: str = ".",
        input_arg: IO[Any] = None,
        working_dir: str = None,
        plugin_cache_dir: str = None,
        error_on_no_changes: bool = True,
        output_file: str = None,
        debug: bool = False) -> None:
    process_args = [
        TERRAFORM_BIN_FILE_PATH,
        f"-chdir={terraform_dir}",
        *args
    ]
    # force 'TF_IN_AUTOMATION'
    os.environ['TF_IN_AUTOMATION'] = '1'
    if debug:
        print('[debug] executing: ' + f"{' '.join(process_args)}")
    if plugin_cache_dir:
        os.environ['TF_PLUGIN_CACHE_DIR'] = plugin_cache_dir
        if debug:
            print(f'[debug] set TF_PLUGIN_CACHE_DIR to {plugin_cache_dir}')
            _dump_plugin_cache(plugin_cache_dir)
    try:
        # use Popen so we can read lines as they come
        with subprocess.Popen(
                process_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # redirect stderr to stdout
                bufsize=1,
                universal_newlines=True,
                stdin=input_arg,
                cwd=working_dir) as pipe:
            if output_file:
                with open(output_file, 'w', encoding="utf-8") as output_file_obj:
                    for line in pipe.stdout:
                        output_file_obj.write(line)
                        if debug:
                            # log the output as it arrives
                            print(line, end="")
                if debug:
                    print(f'[debug] wrote output to {output_file}')
            else:
                for line in pipe.stdout:
                    # log the output as it arrives
                    print(line, end="")
            if pipe.stderr:
                for line in pipe.stderr:
                    print(line, end="", file=sys.stderr)
        # mask args if we're not in debug
        masked_args = pipe.args if debug else [TERRAFORM_BIN_FILE_PATH]
        # check if we're using detailed exit codes
        if '-detailed-exitcode' in [arg.lower() for arg in args]:
            # 2 == success, with changes
            if pipe.returncode != 2:
                # 0 == success, no changes
                if pipe.returncode == 0:
                    if error_on_no_changes:
                        # raise a custom exception
                        raise TerraformNoChangesError(pipe.returncode, masked_args)
                else:
                    # raise a standard exception
                    raise subprocess.CalledProcessError(
                        pipe.returncode,
                        masked_args)
        else:
            if pipe.returncode != 0:
                # raise a standard exception
                raise subprocess.CalledProcessError(
                    pipe.returncode,
                    masked_args)
    finally:
        if plugin_cache_dir and debug:
            print('[debug] dumping updated plugin cache')
            _dump_plugin_cache(plugin_cache_dir)


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
        terraform_dir_path: str = ".",
        plugin_cache_dir_path: str = "",
        backend_config_vars: Optional[dict] = None,
        debug: bool = False) -> None:
    if not terraform_dir_path:
        terraform_dir_path = '.'
    terraform_command_args = []
    # set backend config values
    if backend_config_vars:
        for k, v in backend_config_vars.items():
            terraform_command_args.append(
                f"-backend-config={k}={v}")
    # execute
    _terraform(
        'init',
        '-input=false',
        *terraform_command_args,
        terraform_dir=terraform_dir_path,
        working_dir=working_dir_path,
        plugin_cache_dir=plugin_cache_dir_path,
        debug=debug)


# =============================================================================
# plan
# =============================================================================
def plan(
        working_dir_path: str,
        terraform_dir_path: str = ".",
        plugin_cache_dir_path: str = "",
        state_file_path: Optional[str] = None,
        create_plan_file: bool = False,
        plan_file_path: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        destroy: Optional[bool] = None,
        var_file_paths: Optional[list] = None,
        debug: bool = False) -> None:
    if not terraform_dir_path:
        terraform_dir_path = '.'
    if error_on_no_changes not in [True, False]:
        error_on_no_changes = True
    if destroy not in [True, False]:
        destroy = False
    terraform_command_args = []
    if state_file_path:
        # specify state file
        terraform_command_args.append(f"-state={state_file_path}")
    if create_plan_file:
        # creating a plan file
        terraform_command_args.append(f"-out={plan_file_path}")
    if var_file_paths:
        for var_file_path in var_file_paths:
            terraform_command_args.append(f"-var-file={var_file_path}")
    if destroy:
        # creating a destroy plan
        terraform_command_args.append('-destroy')
    # execute
    _terraform(
        'plan',
        '-input=false',
        '-detailed-exitcode',
        *terraform_command_args,
        terraform_dir=terraform_dir_path,
        working_dir=working_dir_path,
        plugin_cache_dir=plugin_cache_dir_path,
        error_on_no_changes=error_on_no_changes,
        debug=debug)


# =============================================================================
# apply
# =============================================================================
def apply(
        working_dir_path: str,
        terraform_dir_path: str = ".",
        plugin_cache_dir_path: str = "",
        state_file_path: Optional[str] = None,
        output_state_file_path: Optional[str] = None,
        plan_file_path: Optional[str] = None,
        var_file_paths: Optional[list] = None,
        debug: bool = False) -> None:
    if not terraform_dir_path:
        terraform_dir_path = '.'
    terraform_command_args = []
    if plan_file_path:
        # target plan file if using a plan file
        terraform_dir_path = plan_file_path
    else:
        # auto approve if not using a plan file
        terraform_command_args.append('-auto-approve')
    if state_file_path:
        # specify state file
        terraform_command_args.append(f"-state={state_file_path}")
    if var_file_paths:
        for var_file_path in var_file_paths:
            terraform_command_args.append(f"-var-file={var_file_path}")
    # execute
    _terraform(
        'apply',
        '-input=false',
        *terraform_command_args,
        terraform_dir=terraform_dir_path,
        working_dir=working_dir_path,
        plugin_cache_dir=plugin_cache_dir_path,
        debug=debug)


# =============================================================================
# show
# =============================================================================
def show(
        working_dir_path: str,
        plan_file_path: str,
        debug: bool = False) -> None:
    # execute
    _terraform(
        'show',
        plan_file_path,
        working_dir=working_dir_path,
        debug=debug)


# =============================================================================
# output
# =============================================================================
def output(
        working_dir_path: str,
        output_file_path: str,
        state_file_path: Optional[str] = None,
        target_name: Optional[str] = None,
        debug: bool = False) -> None:
    terraform_command_args = []
    if state_file_path:
        # specify state file
        terraform_command_args.append(f"-state={state_file_path}")
    if target_name:
        # specify target
        terraform_command_args.append(target_name)
    # execute
    _terraform(
        'output',
        '-json',
        *terraform_command_args,
        working_dir=working_dir_path,
        output_file=output_file_path,
        debug=debug)

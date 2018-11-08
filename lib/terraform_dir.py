# stdlib
import distutils.dir_util
import os
import shutil
import tarfile
import tempfile
import time
from typing import Optional

# local
import lib.terraform


# =============================================================================
#
# constants
#
# =============================================================================

TERRAFORM_WORK_DIR = '/tmp/tfwork'
TERRAFORM_DIR_NAME = 'terraform'
TERRAFORM_PLAN_FILE_NAME = '.tfplan'
BACKEND_FILE_NAME = 'backend.tf'
BACKEND_TYPE_VAR = 'TF_BACKEND_TYPE'
BACKEND_CONFIG_VAR_PREFIX = 'TF_BACKEND_CONFIG_'


# =============================================================================
#
# private functions
#
# =============================================================================

# =============================================================================
# _get_working_dir_file_path
# =============================================================================
def _get_working_dir_file_path(
        working_dir_path: str, file_name: str) -> str:
    return os.path.join(working_dir_path, file_name)


# =============================================================================
# _get_terraform_dir
# =============================================================================
def _get_terraform_dir(terraform_work_dir: str) -> str:
    return os.path.join(terraform_work_dir, TERRAFORM_DIR_NAME)


# =============================================================================
# _prep_terraform_dir
# =============================================================================
def _prep_terraform_dir(terraform_dir: str) -> None:
    if os.path.isdir(terraform_dir):
        shutil.rmtree(terraform_dir)
    os.makedirs(terraform_dir)


# =============================================================================
# _copy_terraform_dir
# =============================================================================
def _copy_terraform_dir(
        source: str,
        destination: str) -> None:
    distutils.dir_util.copy_tree(source, destination)


# =============================================================================
# _generate_backend_file_contents
# =============================================================================
def _generate_backend_file_contents(backend_type: str) -> str:
    return f"""terraform {{
    backend "{backend_type}" {{}}
}}"""


# =============================================================================
# _create_backend_file
# =============================================================================
def _create_backend_file(
        backend_type: str,
        terraform_dir: str,
        debug: bool = False) -> None:
    backend_file_path = os.path.join(terraform_dir, BACKEND_FILE_NAME)
    backend_file_contents = _generate_backend_file_contents(backend_type)
    with open(backend_file_path, 'w') as backend_file:
        backend_file.write(backend_file_contents)
    if debug:
        print('[debug] created backend file:')
        with open(backend_file_path, 'r') as backend_file:
            print(backend_file.read())


# =============================================================================
# _get_value_from_file
# =============================================================================
def _get_value_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        value = file.read()
    return value


# =============================================================================
# _format_archive_version
# =============================================================================
def _format_archive_version(
    timestamp: int,
    source_ref: Optional[str] = None
) -> str:
    if source_ref:
        return f"{timestamp}.{source_ref}"
    else:
        return str(timestamp)


# =============================================================================
# _get_archive_version
# =============================================================================
def _get_archive_version(
        source_ref: Optional[str] = None,
        source_ref_file: Optional[str] = None,
        timestamp: Optional[int] = None) -> str:
    if not timestamp:
        # get current unix timestamp
        timestamp = int(time.time())
    if (not source_ref) and source_ref_file:
        # get source ref from file
        source_ref = _get_value_from_file(source_ref_file)
    return _format_archive_version(timestamp, source_ref=source_ref)


# =============================================================================
# _create_terraform_dir_archive
# =============================================================================
def _create_terraform_dir_archive(
        terraform_dir: str,
        output_dir: str,
        version: str,
        debug: bool = False) -> str:
    archive_file_name = f"terraform-{version}.tar.gz"
    archive_file_path = os.path.join(output_dir, archive_file_name)
    with tarfile.open(archive_file_path, 'x:gz') as archive_file:
        if debug:
            archive_file.debug = 3
            print('[debug] creating terraform archive: '
                f"{archive_file_path}")
        archive_file.add(terraform_dir, TERRAFORM_DIR_NAME)
    if debug:
        with tarfile.open(archive_file_path, 'r:gz') as archive_file:
            archive_file.debug = 3
            print('[debug] terraform archive contents: '
                f"{archive_file_path}")
            archive_file.list()
    return archive_file_path


# =============================================================================
# _get_archive_file_name
# =============================================================================
def _get_archive_file_name(archive_input_dir) -> str:
    archive_files = [archive_file
                     for archive_file in os.listdir(archive_input_dir)
                     if archive_file.endswith('.tar.gz')]
    if len(archive_files) == 0:
        raise FileNotFoundError('no archive file found at path: '
                                f"{archive_input_dir}")
    elif len(archive_files) > 1:
        raise FileExistsError('multiple archive files found at path: '
                              '{}\n{}'.format(archive_input_dir,
                                              '\n'.join(archive_files)))
    else:
        return archive_files[0]


# =============================================================================
# _print_directory_contents
# =============================================================================
def _print_directory_contents(directory: str) -> None:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            print(os.path.join(path, name))


# =============================================================================
# _restore_terraform_dir_archive
# =============================================================================
def _restore_terraform_dir_archive(
        terraform_dir: str,
        input_dir: str,
        debug: bool = False) -> None:
    # get the archive file name
    archive_file_name = _get_archive_file_name(input_dir)
    # get the archive file path
    archive_file_path = os.path.join(input_dir, archive_file_name)
    # get a temporary directory to extract to
    with tempfile.TemporaryDirectory() as extract_scratch_dir:
        # extract to the temporary directory
        with tarfile.open(archive_file_path, 'r:gz') as archive_file:
            if debug:
                archive_file.debug = 3
                print('[debug] extracting terraform archive: '
                      f"{archive_file_path}")
            archive_file.extractall(path=extract_scratch_dir)
        # get the extracted terraform dir path
        extracted_terraform_dir = _get_terraform_dir(extract_scratch_dir)
        # copy the extracted terraform dir to the terraform dir
        _copy_terraform_dir(extracted_terraform_dir, terraform_dir)
    if debug:
        print('[debug] extracted archive contents: ')
        _print_directory_contents(terraform_dir)


# =============================================================================
# _get_backend_type_from_environment
# =============================================================================
def _get_backend_type_from_environment() -> Optional[str]:
    return os.environ.get(BACKEND_TYPE_VAR)


# =============================================================================
# _get_backend_config_from_environment
# =============================================================================
def _get_backend_config_from_environment() -> Optional[dict]:
    backend_config: dict = {}
    for key, value in os.environ.items():
        if key.startswith(BACKEND_CONFIG_VAR_PREFIX):
            # strip prefix and use the remainder as the key name
            backend_config[key[len(BACKEND_CONFIG_VAR_PREFIX):]] = value
    return backend_config or None


# =============================================================================
#
# public functions
#
# =============================================================================

# =============================================================================
# init_terraform_dir
# =============================================================================
def init_terraform_dir(
        terraform_source_dir: str,
        terraform_dir_path: Optional[str] = None,
        terraform_work_dir: str = TERRAFORM_WORK_DIR,
        debug: bool = False) -> str:
    # check source dir
    if not terraform_source_dir:
        raise ValueError('terraform_source_dir cannot be empty')
    # get path to terraform dir
    terraform_dir = _get_terraform_dir(terraform_work_dir)
    # prep the terraform dir
    _prep_terraform_dir(terraform_dir)
    # copy the terraform source dir into terraform dir
    _copy_terraform_dir(terraform_source_dir, terraform_dir)
    # get backend type from environment
    backend_type = _get_backend_type_from_environment()
    # optionally create a backend configuration
    if backend_type:
        _create_backend_file(
            backend_type,
            terraform_dir,
            debug=debug)
    # get any backend config values from environment
    backend_config_vars = _get_backend_config_from_environment()
    # terraform init
    lib.terraform.init(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        backend_config_vars=backend_config_vars,
        debug=debug)
    return terraform_dir


# =============================================================================
# archive_terraform_dir
# =============================================================================
def archive_terraform_dir(
        terraform_dir: str,
        archive_output_dir: str,
        source_ref: Optional[str] = None,
        source_ref_file: Optional[str] = None,
        debug: bool = False) -> str:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    # check archive output dir
    if not archive_output_dir:
        raise ValueError('archive_output_dir cannot be empty')
    # create archive of terraform dir
    archive_version = _get_archive_version(
        source_ref=source_ref,
        source_ref_file=source_ref_file)
    archive_file_path = _create_terraform_dir_archive(
        terraform_dir,
        archive_output_dir,
        archive_version,
        debug=debug
    )
    return archive_file_path


# =============================================================================
# restore_terraform_dir
# =============================================================================
def restore_terraform_dir(
        archive_input_dir: str,
        terraform_work_dir: str = TERRAFORM_WORK_DIR,
        debug: bool = False) -> str:
    # check archive input dir
    if not archive_input_dir:
        raise ValueError('archive_input_dir cannot be empty')
    # get path to terraform dir
    terraform_dir = _get_terraform_dir(terraform_work_dir)
    # prep the terraform dir
    _prep_terraform_dir(terraform_dir)
    # restore the terraform dir from archive
    _restore_terraform_dir_archive(
        terraform_dir,
        archive_input_dir,
        debug=debug)
    return terraform_dir


# =============================================================================
# plan_terraform_dir
# =============================================================================
def plan_terraform_dir(
        terraform_dir: str,
        terraform_dir_path: Optional[str] = None,
        state_file_path: Optional[str] = None,
        create_plan_file: bool = False,
        plan_file_path: Optional[str] = None,
        error_on_no_changes: Optional[bool] = None,
        destroy: Optional[bool] = None,
        debug: bool = False) -> Optional[str]:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    if create_plan_file and (not plan_file_path):
            plan_file_path = TERRAFORM_PLAN_FILE_NAME
    if state_file_path:
        # ensure state file exists
        if not os.path.isfile(state_file_path):
            raise(FileNotFoundError(
                f'state_file_path not found at: {state_file_path}'))
    lib.terraform.plan(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        state_file_path=state_file_path,
        create_plan_file=create_plan_file,
        plan_file_path=plan_file_path,
        error_on_no_changes=error_on_no_changes,
        destroy=destroy,
        debug=debug)
    if create_plan_file:
        if debug:
            print(f'[debug] created plan file: {plan_file_path}')
        return plan_file_path


# =============================================================================
# apply_terraform_dir
# =============================================================================
def apply_terraform_dir(
        terraform_dir: str,
        terraform_dir_path: str = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    lib.terraform.apply(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        debug=debug)


# =============================================================================
# apply_terraform_plan
# =============================================================================
def apply_terraform_plan(
        terraform_dir: str,
        plan_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    # check plan file path
    if not plan_file_path:
        plan_file_path = TERRAFORM_PLAN_FILE_NAME
    lib.terraform.apply(
        terraform_dir,
        plan_file_path=plan_file_path,
        debug=debug)


# =============================================================================
# show_terraform_plan
# =============================================================================
def show_terraform_plan(
        terraform_dir: str,
        plan_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    # check plan file path
    if not plan_file_path:
        plan_file_path = TERRAFORM_PLAN_FILE_NAME
    lib.terraform.show(
        terraform_dir,
        plan_file_path,
        debug=debug)

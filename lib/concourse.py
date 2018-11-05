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
from lib.log import log


# =============================================================================
#
# constants
#
# =============================================================================

TERRAFORM_WORK_DIR = '/tmp/tfwork'
TERRAFORM_DIR_NAME = 'terraform'
TERRAFORM_PLAN_FILE_NAME='.tfplan'

ACTION_PLAN = 'plan'
ACTION_APPLY = 'apply'
SUPPORTED_ACTIONS = [ACTION_PLAN, ACTION_APPLY]

BACKEND_LOCAL = 'local'
BACKEND_S3 = 's3'
SUPPORTED_BACKEND_TYPES = [BACKEND_LOCAL, BACKEND_S3]
BACKEND_FILE_NAME='backend.tf'


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
    os.mkdir(terraform_dir)


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
        log('[debug] created backend file:')
        with open(backend_file_path, 'r') as backend_file:
            log(backend_file.read())


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
            log('[debug] creating terraform archive: '
                f"{archive_file_path}")
        archive_file.add(terraform_dir, TERRAFORM_DIR_NAME)
    if debug:
        with tarfile.open(archive_file_path, 'r:gz') as archive_file:
            archive_file.debug = 3
            log('[debug] terraform archive contents: '
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
            log(os.path.join(path, name))


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
                log('[debug] extracting terraform archive: '
                    f"{archive_file_path}")
            archive_file.extractall(path=extract_scratch_dir)
        # get the extracted terraform dir path
        extracted_terraform_dir = _get_terraform_dir(extract_scratch_dir)
        # copy the extracted terraform dir to the terraform dir
        _copy_terraform_dir(extracted_terraform_dir, terraform_dir)
    if debug:
        log('[debug] extracted archive contents: ')
        _print_directory_contents(terraform_dir)


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
        backend_type: Optional[str] = None,
        backend_config_vars: Optional[dict] = None,
        terraform_dir_path: str = None,
        terraform_work_dir: str = TERRAFORM_WORK_DIR,
        debug: bool = False) -> str:
    # get path to terraform dir
    terraform_dir = _get_terraform_dir(terraform_work_dir)
    # prep the terraform dir
    _prep_terraform_dir(terraform_dir)
    # copy the terraform source dir into terraform dir
    _copy_terraform_dir(terraform_source_dir, terraform_dir)
    # optionally create a backend configuration
    if backend_type:
        _create_backend_file(
            backend_type,
            terraform_dir,
            debug=debug)
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
        source_ref: str = None,
        source_ref_file: str = None,
        debug: bool = False) -> str:
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
        terraform_dir_path: str = None,
        terraform_work_dir: str = TERRAFORM_WORK_DIR,
        debug: bool = False) -> None:
    # get path to terraform dir
    terraform_dir = _get_terraform_dir(terraform_work_dir)
    # prep the terraform dir
    _prep_terraform_dir(terraform_dir)
    # restore the terraform dir from archive
    _restore_terraform_dir_archive(
        terraform_dir,
        archive_input_dir,
        debug=debug)


# =============================================================================
# plan_terraform_dir
# =============================================================================
def plan_terraform_dir(
        terraform_dir: str,
        terraform_dir_path: str = None,
        create_plan_file: bool = False,
        plan_file_path: str = None,
        debug: bool = False) -> Optional[str]:
    if create_plan_file and (not plan_file_path):
            plan_file_path = TERRAFORM_PLAN_FILE_NAME
    lib.terraform.plan(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        create_plan_file=create_plan_file,
        plan_file_path=plan_file_path,
        debug=debug)
    if create_plan_file:
        if debug:
            log(f'[debug] created plan file: {plan_file_path}')
        return plan_file_path


# =============================================================================
# apply_terraform_dir
# =============================================================================
def apply_terraform_dir(
        terraform_dir: str,
        terraform_dir_path: str = None,
        plan_file_path: str = None,
        debug: bool = False) -> None:
    lib.terraform.apply(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        plan_file_path=plan_file_path,
        debug=debug)


# =============================================================================
# show_terraform_plan
# =============================================================================
def show_terraform_plan(
        terraform_dir: str,
        plan_file_path: str = None,
        debug: bool = False) -> None:
    lib.terraform.show(
        terraform_dir,
        plan_file_path,
        debug=debug)

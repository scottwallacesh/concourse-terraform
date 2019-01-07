# stdlib
import distutils.dir_util
import json
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

AUX_INPUT_PATH_PREFIX = 'TF_AUX_INPUT_PATH_'
AUX_INPUT_NAME_PREFIX = 'TF_AUX_INPUT_NAME_'
AUX_INPUT_PATH_KEY = 'PATH'
AUX_INPUT_NAME_KEY = 'NAME'
BACKEND_FILE_NAME = 'backend.tf'
BACKEND_TYPE_VAR = 'TF_BACKEND_TYPE'
BACKEND_CONFIG_VAR_PREFIX = 'TF_BACKEND_CONFIG_'
TERRAFORM_WORK_DIR = '/tmp/tfwork'
TERRAFORM_DIR_NAME = 'terraform'
TERRAFORM_PLUGIN_CACHE_DIR_NAME = '.tfcache'
TERRAFORM_PLUGIN_CACHE_VAR_NAME = 'TF_PLUGIN_CACHE'
TERRAFORM_PLAN_FILE_NAME = '.tfplan'
TERRAFORM_STATE_FILE_NAME = 'terraform.tfstate'
TERRAFORM_OUTPUT_FILE_NAME = 'tf-output.json'
TERRAFORM_OUTPUT_FILE_SUFFIX = '.json'
TERRAFORM_BACKUP_STATE_FILE_NAME = f'{TERRAFORM_STATE_FILE_NAME}.backup'


# =============================================================================
#
# private functions
#
# =============================================================================


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
    distutils.dir_util._path_created = {}
    # preserving symlinks since terraform plan archives contain them
    distutils.dir_util.copy_tree(source, destination, preserve_symlinks=1)


# =============================================================================
# _import_state_file_to_terraform_dir
# =============================================================================
def _import_state_file_to_terraform_dir(
        state_file_path: str,
        terraform_dir: str) -> str:
    destination_file_path = os.path.join(
        terraform_dir,
        TERRAFORM_STATE_FILE_NAME)
    shutil.copyfile(state_file_path, destination_file_path)
    print(f"imported state file {state_file_path} to: {destination_file_path}")
    return TERRAFORM_STATE_FILE_NAME


# =============================================================================
# _export_state_files_from_terraform_dir
# =============================================================================
def _export_state_files_from_terraform_dir(
        terraform_dir: str,
        state_output_dir: str) -> None:
    # create output dir, if needed
    if not os.path.isdir(state_output_dir):
        os.makedirs(state_output_dir)
    # format paths to state files
    source_state_file_path = os.path.join(
        terraform_dir,
        TERRAFORM_STATE_FILE_NAME)
    source_backup_state_file_path = os.path.join(
        terraform_dir,
        TERRAFORM_BACKUP_STATE_FILE_NAME)
    destination_state_file_path = os.path.join(
        state_output_dir,
        TERRAFORM_STATE_FILE_NAME)
    destination_backup_state_file_path = os.path.join(
        state_output_dir,
        TERRAFORM_BACKUP_STATE_FILE_NAME)
    # copy state files, if found
    if os.path.isfile(source_state_file_path):
        shutil.copyfile(
            source_state_file_path,
            destination_state_file_path)
        print(f"exported state file to: {destination_state_file_path}")
    if os.path.isfile(source_backup_state_file_path):
        shutil.copyfile(
            source_backup_state_file_path,
            destination_backup_state_file_path)
        print('exported backup state file to: '
              f'{destination_backup_state_file_path}')


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
    print(f"wrote archive to: {archive_file_path}")
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
    print(f"restored archive {archive_file_path} to: {terraform_dir}")


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
# _get_aux_inputs_from_environment
# =============================================================================
def _get_aux_inputs_from_environment() -> Optional[list]:
    aux_inputs: list = []
    for key, value in os.environ.items():
        if key.startswith(AUX_INPUT_PATH_PREFIX):
            aux_input: dict = {}
            # add the path
            aux_input[AUX_INPUT_PATH_KEY] = value
            aux_input_index: str = None
            # strip prefix and use the remainder as the input index
            aux_input_index = key[len(AUX_INPUT_PATH_PREFIX):]
            # build the expected name key
            aux_input_name_key = \
                AUX_INPUT_NAME_PREFIX + aux_input_index
            # check if the name key was set
            if aux_input_name_key in os.environ:
                # add the name
                aux_input[AUX_INPUT_NAME_KEY] = os.environ[aux_input_name_key]
            # add the aux input to the output list
            aux_inputs.append(aux_input)
    return aux_inputs or None


# =============================================================================
# _copy_aux_inputs_to_terraform_dir
# =============================================================================
def _copy_aux_inputs_to_terraform_dir(
        aux_inputs: list,
        terraform_dir: str) -> None:
    for aux_input in aux_inputs:
        aux_input_source_path: str = aux_input[AUX_INPUT_PATH_KEY]
        aux_input_name: str = None
        if AUX_INPUT_NAME_KEY in aux_input:
            aux_input_name = aux_input[AUX_INPUT_NAME_KEY]
        if aux_input_name:
            aux_input_dest_path = os.path.join(terraform_dir, aux_input_name)
        else:
            aux_input_dest_path = terraform_dir
        _copy_terraform_dir(aux_input_source_path, aux_input_dest_path)


# =============================================================================
# _get_plugin_cache_dir
# =============================================================================
def _get_plugin_cache_dir(terraform_dir: str):
    return os.path.join(terraform_dir, TERRAFORM_PLUGIN_CACHE_DIR_NAME)


# =============================================================================
# _get_plugin_cache_dir_from_environment
# =============================================================================
def _get_plugin_cache_dir_from_environment() -> Optional[str]:
    return os.environ.get(TERRAFORM_PLUGIN_CACHE_VAR_NAME)


# =============================================================================
# _import_plugin_cache_dir
# =============================================================================
def _import_plugin_cache_dir(
        input_plugin_cache_dir: str,
        plugin_cache_dir: str) -> None:
    _copy_terraform_dir(input_plugin_cache_dir, plugin_cache_dir)


# =============================================================================
# _export_plugin_cache_dir
# =============================================================================
def _export_plugin_cache_dir(
        plugin_cache_dir: str,
        output_plugin_cache_dir: str) -> None:
    _copy_terraform_dir(plugin_cache_dir, output_plugin_cache_dir)


# =============================================================================
# _export_output_file
# =============================================================================
def _export_output_file(
        output_file_path: str,
        output_dir: str) -> None:
    # create output dir, if needed
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # copy path_to/file.ext to output_dir/file.ext
    dst_output_file_path = os.path.join(
        output_dir,
        os.path.basename(output_file_path))
    shutil.copyfile(
        output_file_path,
        dst_output_file_path)
    print(f"exported output to: {dst_output_file_path}")


# =============================================================================
# _convert_output_var_file_into_var_file
# =============================================================================
def _convert_output_var_file_into_var_file(
        var_name: str,
        output_var_file_contents: dict) -> Optional[dict]:
    var_file: dict = {}
    # look for 'value' key, indicating this is
    # just a single output item
    if 'value' in output_var_file_contents:
        # since it's just a single item
        # use the var name as the key name
        var_file[var_name] = output_var_file_contents['value']
    else:
        # multiple items, look for 'value' in each
        for key, value in output_var_file_contents.items():
            if value and 'value' in value:
                var_file[key] = value['value']
    return var_file or None


# =============================================================================
# _convert_and_import_output_var_files_to_terraform_dir
# =============================================================================
def _convert_and_import_output_var_files_to_terraform_dir(
        output_var_files: dict,
        terraform_dir: str) -> Optional[list]:
    var_files: list = []
    for key, value in output_var_files.items():
        with open(value, 'r') as output_var_file:
            output_var_file_contents = json.load(output_var_file)
        var_file_contents = _convert_output_var_file_into_var_file(
            key,
            output_var_file_contents)
        if var_file_contents:
            var_file_path = os.path.join(terraform_dir,
                                         f"{key}.tfvars.json")
            with open(var_file_path, 'w') as var_file:
                json.dump(var_file_contents, var_file)
            var_files.append(var_file_path)
    return var_files or None


# =============================================================================
#
# public functions
#
# =============================================================================

# =============================================================================
# init_terraform_dir
# =============================================================================
def init_terraform_dir(
        terraform_source_dir: Optional[str] = None,
        terraform_dir_path: Optional[str] = None,
        terraform_work_dir: Optional[str] = None,
        debug: bool = False) -> str:
    # default the work dir
    if not terraform_work_dir:
        terraform_work_dir = TERRAFORM_WORK_DIR
    # get path to terraform dir
    terraform_dir = _get_terraform_dir(terraform_work_dir)
    # prep the terraform dir
    _prep_terraform_dir(terraform_dir)
    # optionally copy the terraform source dir into terraform dir
    if terraform_source_dir:
        _copy_terraform_dir(terraform_source_dir, terraform_dir)
    # get aux inputs from environment
    aux_inputs = _get_aux_inputs_from_environment()
    # optionally copy aux inputs to terraform dir
    if aux_inputs:
        _copy_aux_inputs_to_terraform_dir(aux_inputs, terraform_dir)
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
    # get the plugin cache dir path
    plugin_cache_dir = _get_plugin_cache_dir(terraform_dir)
    # check for input plugin cache dir
    input_plugin_cache_dir = _get_plugin_cache_dir_from_environment()
    # optionally import the plugin cache dir into terraform plugin cache dir
    if input_plugin_cache_dir:
        _import_plugin_cache_dir(input_plugin_cache_dir,
                                 plugin_cache_dir)
    # terraform init
    lib.terraform.init(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        plugin_cache_dir_path=plugin_cache_dir,
        backend_config_vars=backend_config_vars,
        debug=debug)
    # optionally export the terraform plugin cache dir back to the input
    if input_plugin_cache_dir:
        _export_plugin_cache_dir(plugin_cache_dir,
                                 input_plugin_cache_dir)
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
        terraform_work_dir: Optional[str] = None,
        debug: bool = False) -> str:
    # check archive input dir
    if not archive_input_dir:
        raise ValueError('archive_input_dir cannot be empty')
    # default the work dir
    if not terraform_work_dir:
        terraform_work_dir = TERRAFORM_WORK_DIR
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
        output_var_files: Optional[dict] = None,
        error_on_no_changes: Optional[bool] = None,
        destroy: Optional[bool] = None,
        debug: bool = False) -> Optional[str]:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    if create_plan_file and (not plan_file_path):
            plan_file_path = TERRAFORM_PLAN_FILE_NAME
    if state_file_path:
        # import the state file and update the path
        state_file_path = \
            _import_state_file_to_terraform_dir(
                state_file_path,
                terraform_dir)
    # get the plugin cache path
    plugin_cache_dir = _get_plugin_cache_dir(terraform_dir)
    # optionally import var files
    var_file_paths = []
    if output_var_files:
        # convert and import the output var files
        imported_output_var_files = \
            _convert_and_import_output_var_files_to_terraform_dir(
                output_var_files,
                terraform_dir)
        # add their paths to the list of var files
        if imported_output_var_files:
            var_file_paths.extend(imported_output_var_files)
    lib.terraform.plan(
        terraform_dir,
        terraform_dir_path=terraform_dir_path,
        plugin_cache_dir_path=plugin_cache_dir,
        state_file_path=state_file_path,
        create_plan_file=create_plan_file,
        plan_file_path=plan_file_path,
        error_on_no_changes=error_on_no_changes,
        destroy=destroy,
        var_file_paths=var_file_paths,
        debug=debug)
    if create_plan_file:
        print(f"wrote plan file to: {plan_file_path}")
        return plan_file_path


# =============================================================================
# apply_terraform_dir
# =============================================================================
def apply_terraform_dir(
        terraform_dir: str,
        terraform_dir_path: str = None,
        state_file_path: Optional[str] = None,
        state_output_dir: Optional[str] = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    if state_file_path:
        # import the state file and update the path
        state_file_path = \
            _import_state_file_to_terraform_dir(
                state_file_path,
                terraform_dir)
    # get the plugin cache path
    plugin_cache_dir = _get_plugin_cache_dir(terraform_dir)
    try:
        lib.terraform.apply(
            terraform_dir,
            terraform_dir_path=terraform_dir_path,
            plugin_cache_dir_path=plugin_cache_dir,
            state_file_path=state_file_path,
            debug=debug)
    finally:
        if state_output_dir:
            _export_state_files_from_terraform_dir(
                terraform_dir,
                state_output_dir)


# =============================================================================
# apply_terraform_plan
# =============================================================================
def apply_terraform_plan(
        terraform_dir: str,
        state_output_dir: Optional[str] = None,
        plan_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    # check plan file path
    if not plan_file_path:
        plan_file_path = TERRAFORM_PLAN_FILE_NAME
    # get the plugin cache path
    plugin_cache_dir = _get_plugin_cache_dir(terraform_dir)
    try:
        lib.terraform.apply(
            terraform_dir,
            plugin_cache_dir_path=plugin_cache_dir,
            plan_file_path=plan_file_path,
            debug=debug)
    finally:
        if state_output_dir:
            _export_state_files_from_terraform_dir(
                terraform_dir,
                state_output_dir)


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


# =============================================================================
# output_terraform_dir
# =============================================================================
def output_terraform_dir(
        terraform_dir: str,
        output_dir: str,
        output_targets: Optional[dict] = None,
        terraform_work_dir: Optional[str] = None,
        state_file_path: Optional[str] = None,
        debug: bool = False) -> None:
    # check terraform dir
    if not terraform_dir:
        raise ValueError('terraform_dir cannot be empty')
    # check output_dir
    if not output_dir:
        raise ValueError('output_dir cannot be empty')
    if state_file_path:
        # import the state file and update the path
        state_file_path = \
            _import_state_file_to_terraform_dir(
                state_file_path,
                terraform_dir)
    if output_targets:
        # dump each output to a file named after itself
        for target_file, target_name in output_targets.items():
            output_file_path = \
                os.path.join(
                    terraform_dir,
                    target_file + TERRAFORM_OUTPUT_FILE_SUFFIX)
            lib.terraform.output(
                terraform_dir,
                output_file_path,
                state_file_path=state_file_path,
                target_name=target_name,
                debug=debug)
            _export_output_file(output_file_path, output_dir)
    else:
        # dump output(s) to default name
        output_file_path = \
            os.path.join(terraform_dir, TERRAFORM_OUTPUT_FILE_NAME)
        lib.terraform.output(
            terraform_dir,
            output_file_path,
            state_file_path=state_file_path,
            debug=debug)
        _export_output_file(output_file_path, output_dir)

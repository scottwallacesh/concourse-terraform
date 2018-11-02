# stdlib
import distutils.dir_util
import json
import os
import shutil
import sys
from typing import Any, Dict, List, Optional

# local
from lib.log import log, log_pretty


# =============================================================================
#
# constants
#
# =============================================================================

TFWORK_DIR_PATH = '/tmp/tfwork'

ACTION_PLAN = 'plan'
ACTION_APPLY = 'apply'
SUPPORTED_ACTIONS = [ACTION_PLAN, ACTION_APPLY]

BACKEND_LOCAL = 'local'
BACKEND_S3 = 's3'
SUPPORTED_BACKEND_TYPES = [BACKEND_LOCAL, BACKEND_S3]


# =============================================================================
#
# private io functions
#
# =============================================================================

# =============================================================================
# _get_working_dir_path
# =============================================================================
def _get_working_dir_path() -> str:
    return sys.argv[1]


# =============================================================================
# _get_working_dir_file_path
# =============================================================================
def _get_working_dir_file_path(
        working_dir_path: str, file_name: str) -> str:
    return os.path.join(working_dir_path, file_name)


# =============================================================================
# _read_payload
# =============================================================================
def _read_payload(stream=sys.stdin) -> Any:
    return json.load(stream)


# =============================================================================
# _write_payload
# =============================================================================
def _write_payload(payload: Any, stream=sys.stdout) -> None:
    json.dump(payload, stream)


# =============================================================================
# _prep_tfwork_dir
# =============================================================================
def _prep_tfwork_dir(tfwork_dir_path: str) -> None:
    if os.path.isdir(tfwork_dir_path):
        shutil.rmtree(tfwork_dir_path)
    os.mkdir(tfwork_dir_path)


# =============================================================================
# _copy_terraform_dir_to_tfwork_dir
# =============================================================================
def _copy_terraform_dir_to_tfwork_dir(
        terraform_dir_path: str,
        tfwork_dir_path: str) -> None:
    distutils.dir_util.copy_tree(terraform_dir_path, tfwork_dir_path)


# =============================================================================
#
# private params functions
#
# =============================================================================

# =============================================================================
# _get_action
# =============================================================================
def _get_action(params: dict) -> str:
    action: str = params.get('action', 'plan')
    if action not in SUPPORTED_ACTIONS:
        raise ValueError(
            f"action '{action}' unsupported. "
            f"supported actions are: {', '.join(SUPPORTED_ACTIONS)}")
    return action


# =============================================================================
# _get_debug_enabled
# =============================================================================
def _get_debug_enabled(params: dict) -> bool:
    return params.get('debug', False)


# =============================================================================
# _get_plan_terraform_dir
# =============================================================================
def _get_plan_terraform_dir(params: dict) -> Optional[str]:
    return params['plan']['terraform_dir']


# =============================================================================
# _get_backend_type
# =============================================================================
def _get_backend_type(params: dict) -> str:
    backend_type: str = params.get('backend_type', 'local')
    if backend_type not in SUPPORTED_BACKEND_TYPES:
        raise ValueError(
            f"backend_type '{backend_type}' unsupported. "
            f"supported values are: {', '.join(SUPPORTED_BACKEND_TYPES)}")


# # =============================================================================
# # _create_concourse_metadata_from_build_manifest_artifact
# # =============================================================================
# def _create_concourse_metadata_from_build_manifest_artifact(
#         artifact_name: str,
#         artifact_index: str,
#         artifact: dict) -> List[dict]:
#     metadata = []
#     for key, value in artifact.items():
#         metadata.append({
#             'name': f"{artifact_name}::{artifact_index}::{key}",
#             'value': value
#         })
#     return metadata


# # =============================================================================
# # _create_concourse_out_payload_from_packer_build_manifest
# # =============================================================================
# def _create_concourse_out_payload_from_packer_build_manifest(
#         build_manifest: dict) -> dict:
#     out_payload = {
#         'version': None,
#         'metadata': []
#     }
#     for artifact_name, artifacts in build_manifest['artifacts'].items():
#         for artifact_index, artifact in artifacts.items():
#             # use first artifact as version
#             if (not out_payload['version']) and (artifact_index == '0'):
#                 out_payload['version'] = {
#                     'id': artifact['id']
#                 }
#             # add artifact details as metadata
#             out_payload['metadata'].extend(
#                 _create_concourse_metadata_from_build_manifest_artifact(
#                     artifact_name, artifact_index, artifact))
#     return out_payload


# =============================================================================
#
# public lifecycle functions
#
# =============================================================================

def do_check() -> None:
    # not implemented
    _write_payload([{'id': '0'}])


def do_in() -> None:
    # not implemented
    _write_payload({
        "version": {
            'id': '0'
        }
    })


def do_out(
        input_payload: dict = None,
        working_dir_path: str = None,
        tfwork_dir_path: str = TFWORK_DIR_PATH) -> None:
    # read the concourse input payload
    if not input_payload:
        input_payload = _read_payload()
    # get the working dir path from the input
    if not working_dir_path:
        working_dir_path = _get_working_dir_path()
    # get debug setting from payload params
    debug_enabled = _get_debug_enabled(input_payload['params'])
    # get the backend type from payload params
    backend_type = _get_backend_type(input_payload['params'])
    # get the action
    action = _get_action(input_payload['params'])
    # prep the tfwork directory
    _prep_tfwork_dir(tfwork_dir_path)

    # process action
    if action == ACTION_PLAN:
        # get terraform_dir
        terraform_dir = _get_plan_terraform_dir(input_payload['params'])
        # copy terrform dir contents to tfwork directory
        _copy_terraform_dir_to_tfwork_dir(terraform_dir, tfwork_dir_path)
    elif action == ACTION_APPLY:
        raise NotImplementedError()

    # then copy the contents of the terraform directory into it
    # also be able to create an archive of the contents

    # # get the template file path from the payload
    # template_file_path: str = input_payload['params']['template']
    # # get the working dir path from the input
    # working_dir_path = _get_working_dir_path()
    # # instantiate the var file paths and vars lists
    # var_file_paths: Optional[List[str]] = None
    # vars: Optional[Dict] = None
    # vars_from_files: Optional[Dict] = None
    # # add var file paths, if provided
    # if 'var_files' in input_payload['params']:
    #     var_file_paths = input_payload['params']['var_files']
    # # add vars, if provided
    # if 'vars' in input_payload['params']:
    #     vars = input_payload['params']['vars']
    # # add vars from files, if provided
    # if 'vars_from_files' in input_payload['params']:
    #     vars_from_files = input_payload['params']['vars_from_files']
    # # dump details, if debug enabled
    # if debug_enabled:
    #     log('var_file_paths:')
    #     log_pretty(var_file_paths)
    #     log('vars:')
    #     log_pretty(vars)
    # # dump the current packer version
    # lib.packer.version()
    # # validate the template
    # lib.packer.validate(
    #     working_dir_path,
    #     template_file_path,
    #     var_file_paths=var_file_paths,
    #     vars=vars,
    #     vars_from_files=vars_from_files,
    #     debug=debug_enabled)
    # # build the template, getting the build manifest back
    # build_manifest = lib.packer.build(
    #     working_dir_path,
    #     template_file_path,
    #     var_file_paths=var_file_paths,
    #     vars=vars,
    #     vars_from_files=vars_from_files,
    #     debug=debug_enabled)
    # # dump build manifest, if debug
    # if debug_enabled:
    #     log('build manifest:')
    #     log_pretty(build_manifest)
    # # convert the manifest into a concourse output payload
    # output_payload = _create_concourse_out_payload_from_packer_build_manifest(
    #     build_manifest)
    # # dump output payload, if debug
    # if debug_enabled:
    #     log('output payload:')
    #     log_pretty(output_payload)
    # # write out the payload
    # _write_payload(output_payload)

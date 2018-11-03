# stdlib
import distutils.dir_util
import json
import os
import shutil
import sys
from typing import Any, Dict, List, Optional

# local
import lib.terraform
from lib.log import log, log_pretty


# =============================================================================
#
# constants
#
# =============================================================================

TERRAFORM_WORK_DIR = '/tmp/tfwork'
TERRAFORM_DIR_NAME = 'terraform'

ACTION_PLAN = 'plan'
ACTION_APPLY = 'apply'
SUPPORTED_ACTIONS = [ACTION_PLAN, ACTION_APPLY]

BACKEND_LOCAL = 'local'
BACKEND_S3 = 's3'
SUPPORTED_BACKEND_TYPES = [BACKEND_LOCAL, BACKEND_S3]
BACKEND_FILE_NAME='backend.tf'


# =============================================================================
#
# private io functions
#
# =============================================================================

# =============================================================================
# _get_concourse_work_dir
# =============================================================================
def _get_concourse_work_dir() -> str:
    return sys.argv[1]


# =============================================================================
# _get_working_dir_file_path
# =============================================================================
def _get_working_dir_file_path(
        working_dir_path: str, file_name: str) -> str:
    return os.path.join(working_dir_path, file_name)


# =============================================================================
# _set_working_dir_path
# =============================================================================
def _set_working_dir_path(working_dir_path: str) -> None:
    os.chdir(working_dir_path)


# =============================================================================
# _get_request
# =============================================================================
def _get_request(stream=sys.stdin) -> Any:
    return json.load(stream)


# =============================================================================
# _write_payload
# =============================================================================
def _write_payload(payload: Any, stream=sys.stdout) -> None:
    json.dump(payload, stream)


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
# _create_backend_file
# =============================================================================
def _create_backend_file(request: dict) -> Optional[str]:
    if 'source' in request:
        return request['source'].get('backend_type')
    else:
        return None


# =============================================================================
#
# private params functions
#
# =============================================================================

# =============================================================================
# _get_action
# =============================================================================
def _get_action(request: dict) -> str:
    action: str = request['params'].get('action', 'plan')
    if action not in SUPPORTED_ACTIONS:
        raise ValueError(
            f"action '{action}' unsupported. "
            f"supported actions are: {', '.join(SUPPORTED_ACTIONS)}")
    return action


# =============================================================================
# _get_debug_enabled
# =============================================================================
def _get_debug_enabled(request: dict) -> bool:
    return request['params'].get('debug', False)


# =============================================================================
# _get_plan_terraform_dir
# =============================================================================
def _get_plan_terraform_dir(request: dict) -> Optional[str]:
    return request['params']['plan']['terraform_dir']


# =============================================================================
# _get_backend_type
# =============================================================================
def _get_backend_type(backend_type: str, terraform_dir_path: str) -> None:
    backend_file_path = os.path.join(terraform_dir_path, BACKEND_FILE_NAME)
    if os.path.isfile(backend_file_path):
        raise FileExistsError('backend file already exists: '
                              f"{backend_file_path}")


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
        request: dict = None,
        concourse_work_dir: str = None,
        terraform_work_dir: str = TERRAFORM_WORK_DIR) -> None:
    # get the concourse request
    if not request:
        request = _get_request()
    # get the concourse work dir
    if not concourse_work_dir:
        concourse_work_dir = _get_concourse_work_dir()
    # change to the concourse working dir
    _set_working_dir(concourse_work_dir)
    # get debug setting from payload params
    debug_enabled = _get_debug_enabled(request)
    # get the backend type from payload params
    backend_type = _get_backend_type(request)
    # get the action
    action = _get_action(request)
    # prep the tfwork terraform dir
    tfwork_terraform_dir = _prep_terraform_dir(terraform_work_dir)

    # process action
    if action == ACTION_PLAN:
        # get terraform_dir
        terraform_dir = _get_plan_terraform_dir(request)
        # copy terrform dir contents to tfwork terraform dir
        _copy_terraform_dir(
            terraform_dir,
            terraform_work_dir)
        lib.terraform.plan(
            terraform_work_dir,
            tfwork_terraform_dir
        )
        # create backend file
        _create_backend_file(backend_type, tfwork_terraform_dir)
    elif action == ACTION_APPLY:
        raise NotImplementedError()

    # then copy the contents of the terraform dir into it
    # also be able to create an archive of the contents

    # # get the template file path from the payload
    # template_file_path: str = request['params']['template']
    # # get the working dir path from the input
    # working_dir_path = _get_working_dir_path()
    # # instantiate the var file paths and vars lists
    # var_file_paths: Optional[List[str]] = None
    # vars: Optional[Dict] = None
    # vars_from_files: Optional[Dict] = None
    # # add var file paths, if provided
    # if 'var_files' in request['params']:
    #     var_file_paths = request['params']['var_files']
    # # add vars, if provided
    # if 'vars' in request['params']:
    #     vars = request['params']['vars']
    # # add vars from files, if provided
    # if 'vars_from_files' in request['params']:
    #     vars_from_files = request['params']['vars_from_files']
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

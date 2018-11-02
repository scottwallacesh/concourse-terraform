# concourse terraform resource

a [concourse-ci](https://concourse-ci.org) resource for running [terraform](https://www.terraform.io)

## table of contents

- [overview](#overview)

	- [features](#features)

- [behavior](#behavior)

	- [check](#check-not-implemented)

	- [in](#in-not-implemented)

	- [out](#out-run-terraform-plan-or-apply)

- [development](#development)

- [building](#building)

## overview

this project provides a [concourse-ci](concourse-ci.org) custom resource designed to wrap [terraform](https://www.terraform.io)'s plan and apply phases

### features

- currently, only the **local** and **s3** backends are supported
- docker hub tags correspond to the version of terraform
- generates plan archives using an absolute working dir (`/tmp/tfwork`)
	- the `terraform_dir` will be copied into the terraform working dir

## behaviour

### `check`: not implemented

### `in`: not implemented

### `out`: run terraform plan or apply

**parameters**

- `action`: _optional_. action to perform. allowed values: `apply`, `plan`. default: `plan`

- `plan`: _optional_. parameters for the plan action.

	- `terraform_dir`: _required_. path to terraform directory.

- `backend_type`: _optional_. backend type to use. allowed values: `local`, `s3`. default: `local`

- `backend_config`: _optional_. a key-value mapping of the backend config parameters. default: `null`

	- see [backend configuration](https://www.terraform.io/docs/backends/config.html)
	- example:  
	  
	  ```yaml
	  backend_type: s3
	  backend:
	      bucket: mybucket
	      key: path/to/my/key
	      region: us-east-1
	  ```

- `debug`: _optional_. set to `true` to dump argument values on error. **may result in leaked credentials**. default: `false`

## examples

```yaml
TODO
```

## development

install python 3.7.1 and requirements from `requirements-dev.txt`

`.vscode/settings.json` will enable linters in vscode

local builds can be tested and built with the `./build` and `./test` scripts, which will automatically build and test all versions listed in the `tf-versions` file

## building

builds are handled automatically by [docker hub](https://hub.docker.com)

custom build hooks are used to automatically build every version in the `tf-versions` file

# license

see [LICENSE](LICENSE)

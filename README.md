# concourse terraform resource

a [concourse-ci](https://concourse-ci.org) resource for running [terraform](https://www.terraform.io)

## table of contents

- [overview](#overview)

	- [features](#features)

	- [issues](#issues)

- [source configuration](#source-configuration)

- [behavior](#behavior)

	- [check](#check-not-implemented)

	- [in](#in-not-implemented)

	- [out](#out-run-terraform-plan-or-apply)

- [development](#development)

- [building](#building)

## overview

this project provides a [concourse-ci](concourse-ci.org) custom resource designed to wrap [terraform](https://www.terraform.io)

**requires using a remote state backend to persist state**

### features

- docker hub tags correspond to the version of terraform
- uses remote backends to persist state
- uses the [plan and apply on different machines](https://www.terraform.io/guides/running-terraform-in-automation.html) automation strategy
	- generates plan archives using an absolute working dir `/tmp/tfwork`
	- the contents of `terraform_dir` will be copied into `/tmp/tfwork/terraform`
	- this ensures paths will be consistent when using plan files in separate pipeline steps

### issues

- TODO

## behaviour

### source configuration

- `backend_type`: _required_. backend type to use. example: `s3`.

	- this will automatically generate a `backend.tf` file to be used during `init`

- `backend_config`: _optional_. a key-value mapping of the backend config parameters. default: `null`

	- this will pass each parameter to `init` as a `-backend-config` value

example:

```yaml
source:
  backend_type: s3
  backend:
	  bucket: mybucket
	  key: path/to/my/key
	  region: us-east-1
```

creates `backend.tf`:

```hcl
terraform {
  backend "s3" {}
}
```

with init parameters:

```sh
terraform init \
	-backend-config="bucket=mybucket" \
	-backend-config="key=path/to/my/key" \
	-backend-config="region=us-east-1"
```

see terraform [backend configuration](https://www.terraform.io/docs/backends/config.html) for more information

### `check`: not implemented

### `in`: not implemented

### `out`: run terraform plan or apply

**common parameters**

- `action`: _required_. action to perform. supported values:

	- `create_plan`

	- `show_plan`

	- `apply_plan`

**create-plan parameters**

- `create_plan`: parameters for the `create_plan` action.

	- `terraform_dir`: _required_. path to terraform directory. can be relative to the concourse working directory.

	- `terraform_dir_path`: _optional_. path to terraform files relative to `terraform_dir`. default: `.`

**show-plan parameters**

- `show_plan`: parameters for the `show_plan` action.

**apply-plan parameters**

- `apply_plan`: parameters for the `apply_plan` action.

	- `plan_archive`: _required_. path to terraform plan archive. can be relative to the concourse working directory.

	- `terraform_dir_path`: _optional_. path to terraform files relative to the `terraform_dir` used during plan. default: `.`

- `debug`: _optional_. set to `true` to dump argument values on error. **may result in leaked credentials**. default: `false`

## examples

```yaml
TODO
```

## development

install python 3.7.1 and requirements from `requirements-dev.txt`

`.vscode/settings.json` will enable linters in vscode

`.vscode/launch.json` contains the vscode launch configuration for `ptvsd`

local builds can be tested and built with the `./build` and `./test` scripts, which will automatically build and test all versions listed in the `tf-versions` file

**build script**

`./build` supports two run modes:

- `./build`

	- builds an image for each version in `tf-versions`

- `./build [VERSION]`

	- builds an image for the specified version

note: to install `ptvsd` in the test image, set the environment variable `PTVSD_INSTALL=1` when running `./build`, e.g.: `PTVSD_INSTALL=1 ./build [VERSION]`

**test script**

`./test` supports two run modes:

- `./test`

	- runs `unittest discover` against all versions in `tf-versions`

- `./test [VERSION] [ARGS]`

	- runs `unittest discover ARGS` against `VERSION`
	- supports `ptvsd` (if installed) by setting environment variables:

		- `PTVSD_ENABLE=1` runs `-m ptvsd -host 0.0.0.0 --port 5678` as the entry point
		- `PTVSD_WAIT=1` enables `--wait` causing the process to wait for the debugger to attach

## building

builds are handled automatically by [docker hub](https://hub.docker.com)

custom build hooks are used to automatically build and test every version in the `tf-versions` file

# license

see [LICENSE](LICENSE)

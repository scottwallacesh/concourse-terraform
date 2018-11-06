# concourse terraform

[concourse-ci](https://concourse-ci.org) tasks for running [terraform](https://www.terraform.io)

## table of contents

- [overview](#overview)

	- [features](#features)

	- [issues](#issues)

	- [usage](#usage)

		- [specifying the version](#specifying-the-version)

		- [providing input variable values](#providing-input-variable-values)

		- [configuring the backend](#configuring-the-backend)

		- [providing terraform source files](#providing-terraform-source-files)

- [tasks](#tasks)

	- [plan](#plan)

	- [apply](#apply)

	- [create-plan](#create-plan)

	- [show-plan](#show-plan)

	- [apply-plan](#apply-plan)

- [development](#development)

- [automated builds](#automated-builds)

# overview

this project provides a series of concourse-ci [tasks](https://concourse-ci.org/tasks.html) which are powered by a small python library that wraps and orchestrates terraform

## features

- stays simple by avoiding management of remote and local state

	- remote state can be managed entirely by terraform using [backends](https://www.terraform.io/docs/backends/)

	- local state can be produced as an output and saved with concourse resources

- pre-built images for the terraform versions in `tf-versions` are available on docker hub, or you can build any version with the provided `Dockerfile`

- orchestrates the [plan and apply on different machines](https://www.terraform.io/guides/running-terraform-in-automation.html) automation strategy

	- generates plan archives using an absolute working dir `/tmp/tfwork/terraform`  
	(this ensures paths will be consistent when using plan files in separate pipeline steps).

	- plan archives can be persisted to remote storage using concourse resources (such as the [s3 resource](https://github.com/concourse/s3-resource))

## issues

- no current interface to `-var-file`, so var files must be provided via `.tfvars` files in the `terraform_dir_path`

	- variables can easily be provided with [task params](#providing-input-variable-values)

- [workspaces](https://www.terraform.io/docs/state/workspaces.html) are not supported

- most terraform commands other than those needed to provide a `plan -> approve -> apply` lifecycle are not yet supported

## usage

### specifying the version

the tasks require a pipeline to provide them with their docker image resource

this ensures you provide a specific version of the terraform image when executing

```yaml
resources:
# the terraform tasks
- name: concourse-terraform
  type: git
  source:
  	uri: https://github.com/Snapkitchen/concourse-terraform

# the terraform image
- name: concourse-terraform-image
  type: docker-image
  source:
    repository: snapkitchen/concourse-terraform
    tag: <VERSION>

jobs:
# a job using a terraform task with the terraform image
- name: terraform-task
  plan:
  - get: concourse-terraform
  - get: concourse-terraform-image
  - task: do-terraform-task
    image: concourse-terraform-image
    file: concourse-terraform/tasks/<TASK>.yml
```

you can also build the docker image yourself using the [docker-image-resource](https://github.com/concourse/docker-image-resource) and the `Dockerfile` from the source

### providing input variable values

tfvars can be provided by including `terraform.tfvars` or `*.auto.tfvars` files in the terraform source dir, or by passing them as parameters into the task

```
jobs:
# a terraform task with variables
- name: terraform-task
  plan:
  - get: concourse-terraform
  - get: concourse-terraform-image
  - task: do-terraform-task
    image: concourse-terraform-image
    file: concourse-terraform/tasks/<TASK>.yml
    params:
      TF_VAR_my_var: 'my_value'
```

### configuring the backend

the backend can be configured two ways:

- by including a `.tf` file containing the backend configuration in the terraform source dir

- by specifying the `TF_BACKEND_TYPE` parameter to automatically create a `backend.tf` file for you

the backend configuration can be dynamically provided with additional params in the form of `TF_BACKEND_CONFIG_<var_name>: <var_value>`

automatically create and configure an s3 backend:

```
jobs:
# a terraform task with variables
- name: terraform-task
  plan:
  - get: concourse-terraform
  - get: concourse-terraform-image
  - task: do-terraform-task
    image: concourse-terraform-image
    file: concourse-terraform/tasks/<TASK>.yml
    params:
      TF_BACKEND_TYPE: s3
      TF_BACKEND_CONFIG_bucket: my-bucket
      TF_BACKEND_CONFIG_region: us-east-1
      TF_BACKEND_CONFIG_key: terraform
```

### providing terraform source files

terraform source files are provided through the `terraform_source_dir` parameter

typically this should point to the directory where your `.tf` files are

by default, this directory is used as both the working directory and the target for terraform, meaning terraform expects that all `.tf` files are contained in this directory

however, some terraform projects may reference other files relative to the working directory and the contents of the source tree

e.g. given a source tree such as:

```
src/
src/templates/example.tpl
src/terraform/terraform.tf
```

with a terraform template that references a source tree path:

```
data "template_file" "example" {
  template = "${file("templates/example.tpl")}"
}
```

this path would become invalid if the `terraform_source_dir` was set to `src/terraform`, as only the contents of the `terraform_source_dir` are copied to the absolute path `/tmp/tfwork/terraform` and then used as the working directory

thus, the working directory tree would contain

```
terraform.tf
```

where `../templates/example.tpl` does not exist

thus, in that case, one should provide the base directory as the `terraform_source_dir`, and then specify the `terraform_dir_path` which will instruct terraform to target the specified dir inside the `terraform_source_dir`

e.g. a task for the above example would be configured as:

```yaml
- task: terraform-plan
  image: concourse-terraform-image
  file: concourse-terraform/tasks/plan.yaml
  params:
    terraform_source_dir: src
    terraform_dir_path terraform
```

which would result in the working directory tree:

```
templates/example.tpl
terraform/terraform.tf
```

with `terraform` being the target terraform directory

**see [examples](#examples) for more usage descriptions**

# tasks

## `plan.yaml`: plan with no output

### inputs

- `terraform_source_dir`: _required_. path to the terraform source directory.

### outputs

### params

- `error_on_no_changes`: _optional_. raises an error if applying the plan would result in no changes. default: `true`

## `apply.yaml`: apply with no plan

### inputs

### outputs

### params

## `create-plan.yaml`: create a plan

### inputs

### outputs

### params

## `show-plan.yaml`: show a plan

### inputs

### outputs

### params

## `apply-plan.yaml`: apply a plan

### inputs

### outputs

### params

# legacy

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

# examples

```yaml
TODO
```

# development

install python 3.7.1 and requirements from `requirements-dev.txt`

`.vscode/settings.json` will enable linters in vscode

`.vscode/launch.json` contains the vscode launch configuration for `ptvsd`

local builds can be tested and built with the `./build` and `./test` scripts, which will automatically build and test all versions listed in the `tf-versions` file

## build

builds base and test images

`./build` supports two run modes:

- `./build`

	- builds an image for each version in `tf-versions`

- `./build [VERSION]`

	- builds an image for the specified version

note: to install `ptvsd` in the test image, set the environment variable `PTVSD_INSTALL=1` when running `./build`, e.g.: `PTVSD_INSTALL=1 ./build [VERSION]`

## test

runs `unittest discover` against a test image

`./test` supports two run modes:

- `./test`

	- runs `unittest discover` against all versions in `tf-versions`

- `./test [VERSION] [ARGS]`

	- runs `unittest discover ARGS` against `VERSION`
	- supports `ptvsd` (if installed) by setting environment variables:

		- `PTVSD_ENABLE=1` runs `-m ptvsd -host 0.0.0.0 --port 5678` as the entry point
		- `PTVSD_WAIT=1` enables `--wait` causing the process to wait for the debugger to attach

## run

runs arbitrary args against a test image

`./run` supports one mode:

- `./run [VERSION] [ARGS]`

	- runs `ARGS` against `VERSION`

# automated builds

automated builds are handled by [docker hub](https://hub.docker.com)

custom build hooks are used to build and test every version in the `tf-versions` file

# license

see [LICENSE](LICENSE)

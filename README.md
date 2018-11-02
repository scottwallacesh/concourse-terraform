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

- docker hub tags correspond to the version of terraform
- generates plan archives using an absolute working dir `/tmp/tfwork`
- the contents of `terraform_dir` will be copied into `/tmp/tfwork/terraform`

## behaviour

### `check`: not implemented

### `in`: not implemented

### `out`: run terraform plan or apply

**parameters**

- `backend_type`: _required_. backend type to use. example: `local`, `s3`.

	- this will automatically generate a config file to be used during `init`:  

	  ```
	  terraform {
	      backend "$backend_type" {}
	  }
	  ```

- `backend_config`: _optional_. a key-value mapping of the backend config parameters. default: `null`

	- this will pass each parameter to `init` as a `-backend-config` value:  

	  ```
	  backend_type: s3
	  backend:
	      bucket: mybucket
	      key: path/to/my/key
	      region: us-east-1
	  ```
	  
	  results in:  
	  
	  ```
	  terraform init <ARGS> \
	  		-backend-config="bucket=mybucket" \
	  		-backend-config="key=path/to/my/key" \
	  		-backend-config="region=us-east-1"
	  ```
	  

- `action`: _optional_. action to perform. allowed values: `apply`, `plan`. default: `plan`

- `plan`: _optional_. parameters for the plan action.

	- `terraform_dir`: _required_. path to terraform directory.

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

for the `./test` script, you can use `ptvsd` to remote debug into the container (if installed):

`./test` supports two run modes:

- `./test`

	- runs `unittest discover` against all versions in `tf-versions`

- `./test [VERSION] [ARGS]`

	- runs `unittest discover ARGS` against `VERSION`
	- supports `ptvsd` by setting environment variables:

		- `PTVSD_ENABLE=1` runs `-m ptvsd -host 0.0.0.0 --port 5678` as the entry point
		- `PTVSD_WAIT=1` enables `--wait` causing the process to wait for the debugger to attach

## building

builds are handled automatically by [docker hub](https://hub.docker.com)

custom build hooks are used to automatically build every version in the `tf-versions` file

# license

see [LICENSE](LICENSE)

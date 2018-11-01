# concourse terraform resource

a [concourse-ci](https://concourse-ci.org) resource for running [terraform](https://www.terraform.io)

## table of contents

- [overview](#overview)

	- [requirements](#requirements)

	- [features](#features)

- [behavior](#behavior)

	- [check](#check-not-implemented)

	- [in](#in-not-implemented)

	- [out](#out-run-terraform-plan-or-apply)

- [development](#development)

- [building](#building)

## overview

this project provides a [concourse-ci](concourse-ci.org) custom resource designed to wrap [terraform](https://www.terraform.io)'s plan and apply phases

### requirements

- an s3 bucket
- s3 iam credentials with permissions needed for the [s3 backend](https://www.terraform.io/docs/backends/types/s3.html)

### features

- currently, only the **s3 backend** is supported and is required
- docker hub tags correspond to the version of terraform

## behaviour

### `check`: not implemented

### `in`: not implemented

### `out`: run terraform plan or apply

**parameters**

TODO

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

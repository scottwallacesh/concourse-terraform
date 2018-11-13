# concourse terraform examples

## table of contents

- [s3-plan-approve-apply.yaml](#s3-plan-approve-applyyaml)

## `s3-plan-approve-apply.yaml`

- uses an s3 backend to persist state and an s3 bucket to persist the plan archives

- triggered `auto-plan` runs a no-output plan for every commit

- manually triggered `plan` generates a plan archive for the latest commit

- requires `review` and `approve` jobs before the plan archive can be applied

- uses serial groups to prevent concurrent state modifications

- also creates destroy plans

- uses yaml anchors and aliases to DRY up the template
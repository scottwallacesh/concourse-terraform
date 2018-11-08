# concourse terraform examples

## table of contents

- [s3-plan-approve-apply.yaml](#s3-plan-approve-applyyaml)

## `s3-plan-approve-apply.yaml`

- uses an s3 backend to persist state and an s3 bucket to persist the plan archives

- generates a plan archive for each commit

- requires reviewing and approving the plan archive before it can be applied

- uses serial groups to prevent concurrent state modifications

- supports creating and destroying using plans


FROM python:3.9-slim-bullseye AS base

FROM base AS build-env

ARG TERRAFORM_VERSION=0.0.0

COPY hashicorp.asc .

RUN apt update && apt install -y curl gnupg unzip && \
  curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig > terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig && \
  curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_SHA256SUMS > terraform_${TERRAFORM_VERSION}_SHA256SUMS && \
  gpg --import hashicorp.asc && \
  gpg --verify terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig terraform_${TERRAFORM_VERSION}_SHA256SUMS && \
  curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
  cat terraform_${TERRAFORM_VERSION}_SHA256SUMS | grep terraform_${TERRAFORM_VERSION}_linux_amd64.zip | sha256sum -c && \
  unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /bin && \
  rm -f terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig \
  terraform_${TERRAFORM_VERSION}_SHA256SUMS \
  terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
  hashicorp.asc

FROM base

ENV PYTHONUNBUFFERED=1

COPY --from=build-env /bin/terraform /bin/terraform

RUN CHECKPOINT_DISABLE=1 terraform --version
RUN apt update && apt install -y git

CMD ["/bin/sh"]

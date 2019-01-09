FROM alpine:3.8 as build

ARG TERRAFORM_VERSION=0.0.0

COPY hashicorp.asc .

RUN apk add --no-cache --update \
      curl \
      gnupg \
      openssh \
      && \
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

FROM python:3.7.2-alpine3.8

ENV PYTHONUNBUFFERED=1

COPY --from=build /bin/terraform /bin/terraform

RUN CHECKPOINT_DISABLE=1 terraform --version && \
    apk add --no-cache --update \
      git

CMD ["/bin/sh"]

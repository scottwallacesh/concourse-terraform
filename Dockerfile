FROM python:3.7.0-alpine3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

RUN pip3 --no-cache-dir install --upgrade pip

ARG TERRAFORM_VERSION=0.0.0

COPY hashicorp.asc .

RUN apk add --update curl openssh gnupg && \
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

# COPY requirements.txt /app/requirements.txt

# RUN pip3 --no-cache-dir install -r /app/requirements.txt

# copy scripts
COPY \
  bin/check \
  bin/in \
  bin/out \
  /opt/resource/

# copy library files
COPY \
  lib/__init__.py \
  lib/concourse.py \
  lib/log.py \
  lib/terraform.py \
  /opt/resource/lib/
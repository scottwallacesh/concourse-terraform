ARG PARENT_IMAGE=public.ecr.aws/g9q9d1i9/concourse-terraform:latest
FROM $PARENT_IMAGE

ENV PYTHONPATH=$PYTHONPATH:/app
WORKDIR /app

RUN pip3 --no-cache-dir install --upgrade pip

# optionally install ptvsd
ARG PTVSD_INSTALL
RUN if [ -n "${PTVSD_INSTALL}" ]; then pip3 --no-cache-dir install ptvsd==4.1.4; fi
EXPOSE 5678/tcp

# APP FILES

# COPY requirements.txt /app/requirements.txt

# RUN pip3 --no-cache-dir install -r /app/requirements.txt

# copy library files
COPY \
  lib/__init__.py \
  lib/commands.py \
  lib/consul_config.py \
  lib/environment.py \
  lib/ssh_keys.py \
  lib/terraform_dir.py \
  lib/terraform.py \
  lib/trusted_ca_certs.py \
  /app/lib/

# copy binary files
COPY \
  bin/concourse-terraform \
  bin/consul-config \
  bin/consul-entrypoint \
  bin/consul-wrapper \
  bin/install-ssh-keys \
  bin/install-trusted-ca-certs \
  /app/bin/

# TESTS

# copy test data
COPY testdata /app/testdata

# copy tests
COPY tests /app/tests

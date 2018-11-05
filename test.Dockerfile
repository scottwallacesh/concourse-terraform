ARG APP_IMAGE=snapkitchen/concourse-terraform-resource:latest
FROM $APP_IMAGE

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
  lib/concourse.py \
  lib/log.py \
  lib/terraform.py \
  /app/lib/

# TESTS

# copy test data
COPY testdata /app/testdata

# copy tests
COPY tests /app/tests

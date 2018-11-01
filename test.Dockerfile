ARG APP_IMAGE=snapkitchen/concourse-terraform-resource:latest
FROM $APP_IMAGE

ENV PYTHONPATH=$PYTHONPATH:/opt/resource

# TESTS

# copy test data
COPY testdata /opt/resource/testdata

# copy tests
COPY tests /opt/resource/tests

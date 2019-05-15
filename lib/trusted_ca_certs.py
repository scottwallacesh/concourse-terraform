#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

TRUSTED_CA_CERTS_VAR_PREFIX = 'CT_TRUSTED_CA_CERT_'
TRUSTED_CA_CERTS_DIR_PATH = '/usr/local/share/ca-certificates'


def log(message: str) -> None:
    print(f"[install-trusted-ca-certs] {message}", file=sys.stderr)


def extract_ca_cert_paths(environment: dict) -> dict:
    ca_cert_paths: dict = {}
    for key, value in environment.items():
        if key.startswith(TRUSTED_CA_CERTS_VAR_PREFIX):
            # strip prefix and use the remainder as the key name
            key_name = key[len(TRUSTED_CA_CERTS_VAR_PREFIX):]
            log(f"found ca cert '{key_name}' path: {value}")
            ca_cert_paths[key_name] = value
    return ca_cert_paths


def install_ca_certs(ca_cert_paths: dict, ca_certs_dir: str = None) -> None:
    if not ca_certs_dir:
        ca_certs_dir = TRUSTED_CA_CERTS_DIR_PATH
    for ca_cert_name, ca_cert_src_path in ca_cert_paths.items():
        ca_cert_dest_path = \
            os.path.join(
                ca_certs_dir,
                ca_cert_name + '.crt')
        shutil.copyfile(ca_cert_src_path, ca_cert_dest_path)
        log(f"installed ca cert '{ca_cert_name}' to: {ca_cert_dest_path}")


def update_ca_certificates() -> None:
    subprocess.run(['update-ca-certificates'], check=True)


def main(environment: dict) -> None:
    ca_cert_paths = extract_ca_cert_paths(environment)
    if ca_cert_paths:
        install_ca_certs(ca_cert_paths)
        update_ca_certificates()


if __name__ == '__main__':
    main(os.environ)

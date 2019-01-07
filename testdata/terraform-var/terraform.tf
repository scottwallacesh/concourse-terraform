variable "algorithm" {}

resource "tls_private_key" "test_keypair" {
  algorithm = "${var.algorithm}"
  rsa_bits  = 2048
}

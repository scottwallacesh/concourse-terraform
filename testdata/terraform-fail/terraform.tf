resource "tls_private_key" "test_keypair" {
  algorithm = "INVALID"
  rsa_bits  = 2048
}

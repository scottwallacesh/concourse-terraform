resource "tls_private_key" "test_keypair" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

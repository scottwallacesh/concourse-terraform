resource "tls_private_key" "test_keypair" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

output "test_keypair_private_key" {
  sensitive = true
  value     = "${tls_private_key.test_keypair.private_key_pem}"
}

output "example" {
  value     = "hello world"
}

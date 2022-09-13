# Signature Management

Sigma provides a gui and api mechanism to manage various text based intrusion signatures

examples of signature types are
- snort
- suricata
- yara
- ip
- domain
- url
- hash
- fuzzyhash
- any other text based signature

roles
- admin - django admin that can CRUD signatures and sig types and manage user accounts
- sigma_manager - can CRUD assets and organisations
- user - can read only all data

see deployment instructions for
- INSTALL_ubuntu_20.md
- INSTALL_ubuntu_18.md
- INSTALL_centos_8.md

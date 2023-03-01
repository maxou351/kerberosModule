Role Name
=========

Ce rôle installe, configure et vérifie le bon fonctionnement d'une authentification Kerberos

Requirements
------------



Role Variables
--------------

domain_ad: 
realm_name:

# Installation Kerberos
packages_list:
  - krb5-workstation
  - libkadmin5
  - krb5-libs
services_list:
  - krb5kdc
  - kadmin

# Configuration Kerberos
kerberos:
  realm_name: "{{ realm_name }}.{{ domain_ad }}"
  domain_controller:
  user:
  conf_file_path:

# Keypass data
keytab:
  file_path: 
  init_file_path:

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

Author Information
------------------

Max MORELLI <m.morelli.ext@intradef.gouv.fr>

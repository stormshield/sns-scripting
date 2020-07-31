Ansible Role: sns-firmware-update
=========

This role update the firmware of Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------

    download_path: /firmware

Folder where the downloaded firmware files ares stored (default to ~/Downloads).

    version: 3.8.0

Firmware version to install.

    arch: amd64

Architecture to update (default to inventory `arch` variable).

    model: XL-VM

Model of the appliance to update (default to inventory `model` variable).

    system_clone: True|False

Backup the system partition before update (default to `False`).

Dependencies
------------

None.

Example Playbook
----------------

This playbook upgrade the firmware of a SNS VM.

    ---
    - hosts: all
      roles:
        - role: sns-firmware-update
          version: 4.1.0
          system_clone: False

With the inventory referencing the `arch` and `model` parameters:

    sns_appliances:
      hosts:
        appliance1:
          ansible_connection: local
          appliance:
            host: 10.0.0.254
            user: admin
            password: password123
            sslverifyhost: False
          arch: amd64
          model: XL-VM
          force_modify: True


License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

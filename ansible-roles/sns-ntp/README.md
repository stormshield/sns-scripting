Ansible Role: sns-ntp
=========

This role configures the NTP service and timezone on Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------

     timezone: "Europe/Paris"

Set the timezone.

     ntp_state: 1

Set the NTP service state (default to 1).

    ntp_servers:
      - { host: "fr.pool.ntp.org"}
      - { host: "be.pool.ntp.org", key: "12345678"}

Specify the NTP servers to use.

    reboot_if_needed: true

If true, reboot the appliance to apply the timezone update if needed (default to false).

Dependencies
------------

This role uses dig lookup and needs the `dnspython` library.

Example Playbook
----------------

This playbook will configure the system timezone, NTP servers and reboot the appliance if necessary.

    - hosts: sns_appliances
      roles:
        - role: sns-ntp
          timezone: "Europe/Paris"
          ntp_servers:
            - { host: "fr.pool.ntp.org"}
            - { host: "be.pool.ntp.org", key: "12345678"}
          reboot_if_needed: true

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

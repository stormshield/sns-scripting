Ansible Role: sns-alarm
=========

This role configure IPS alarms of Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------

    alarms:
      protocol_name: 
        - { index:<profile index>, id:<int>, context:(protocol|<ASQ context name>), options... }

Alarm definition options are: 

    [action=(pass|block)] [level=(minor|major|ignore)] [dump=(0|1)] [email=off | email=on emailduration=<seconds> emailcount=<int>] [blacklist=off | blacklist=on blduration=<minutes>] [comment=<string>] [qid=<Queue name>]

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: sns_appliances
      roles:
        - role: sns-alarm
          alarms:
            http: 
              - { index: 1, context: "http:client:header", id: 67, level: ignore }
          

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

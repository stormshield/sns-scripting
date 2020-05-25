Ansible Role: sns-url
=========

This role configures URL/CN filtering on Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------

    base: cloud|embedded

Choose between downloadable embedded url database or extended web control cloud service.

    urlgroups:
      - name: <urlgroup name>
        comment: <comment>
        urls: [ { url: <url>, comment: <comment> }, ... ]

Define url groups.

    cngroups:
      - name: <urlgroup name>
        comment: <comment>
        cns: [ { cn: <url>, comment: <comment> }, ... ]

Define CN groups.

    urlcategorygroups:
      - name: <category group>
        comment: <comment>
        members: [ <urlgroup>, ... ]
        mode: <add|del|reset>

Define url category groups.

    cncategorygroups:
      - name: <category group>
        comment: <comment>
        members: [ <cngroup>, ... ]
        mode: <add|del|reset>

Define CN category groups.

`mode: add` adds members to an existing group, `mode: reset` empties the group before adding members, `mode: del` remove members from the group. Default to `reset`.

    state: absent

If set to `absent`, deletes the objects.

    urlfiltering:
      - index: <slot number>
        name: <slot name>
        comment: <slot comment>
        rules:
         - [ruleid: <digit>]
           state: on|off
           action: pass|block|blockpage0|blockpage1|blockpage2|blockpage3
           urlgroup: <urlgroup object|urlcategory group object>
           [comment: <string>]

Define the URL filtering slots and rules.

    sslfiltering:
      - index: <slot number>
        name: <slot name>
        comment: <slot comment>
        rules:
         - [ruleid: <digit>]
           state: on|off
           action: pass|block|blockpage0|blockpage1|blockpage2|blockpage3
           cngroup: <cngroup object|cncategory group object>
           [comment: <string>]

Define the URL filtering slots and rules.

    blockpages:
      - index: 0 
        file: <filepath>
        name: <page name>
      - index: 1
        file: <filepath>
        name: <page name>
      
Upload the HTML files for block pages (index 0 to 4).

Dependencies
------------

None.

Example Playbook
----------------

This example configure 2 URL filtering rule in the slot number 3:

    - hosts: sns_appliances
      roles:
      - role: sns-url
        base: embedded
        slots:
          - index: 3
            name: myurlslot
            comment: "slot comment"
            rules:
              - { state: "On", action: block, urlgroup: ads, comment: "Block ads" }
              - { state: "On", action: pass, urlgroup: any }

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

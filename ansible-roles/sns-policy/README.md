Ansible role: sns-policy
=========

this role configures filter and NAT policies of Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------
    slotname: ""

Slot name.

    comment: ""

Slot description.

    filter: []

Filter rules.

    nat: []

NAT Rules.

NAT and filter rules tokens are:

( position=<digit> | name=<string> )
[state=(on|off)]
[action=(pass|block|deleg|reset|log|decrypt|nat)]
[loglevel=(none|log|minor|major)]
[noconnlog=(|all|[disk],[syslog],[ipfix])]
[count=(on|off)]
[rate=(|<tcp>,<udp>,<icmp>,<request>)]
[synproxy=(on|off)]
[settos=(|<1-254>)]
[qosid=(|<qid name>)]
[ackqosid=(|<qid name>)]
[qosfairness=(|state|user|host)]
[route=(|<objrouter>|<hostname>|<ipaddr>)]
[inspection=(firewall|ids|ips)]
[antivirus=(on|off)]
[sandboxing=(on|off)]
[antispam=(on|off)]
[proxycache=(on|off)]
[ftpfiltering=(on|off)]
[urlfiltering=(|<0-9>)] (URL policy index)
[mailfiltering=(|<0-9>)] (Mail policy index)
[sslfiltering=(|<0-9>)] (SSL policy index)
[fwservice=(|httpproxy|webportal)]
[webportalexcept=(|urlgroup[,urlgroup[,urlgroup[,...]]])]
[inbound=(|sip_udp)]
[schedule=(anytime|<time object>)]
[securityinspection=(|<0-9>)] (ASQ config index)
[tos=(|<1-254>)]
[ipstate=(on|off)]
[ipproto=(any|<IP protocol name>)] (for instance, TCP, UDP, ICMP, etc)
[icmptype=(|<0-255>)][icmpcode=(|<0-255>)][proto=(auto|none|<app protocol name>)] (for instance, HTTP, FTP, etc)
[srcuser=(|any|unknown|[!]<user>|[!]<usergroup>)]
[srcusertype=(|user|group)]
[srcuserdomain=(|<domain name>)]
[srcusermethod=(|plain|spnego|ssl|radius|kerberos|agent-ad|openvpn|ipsec|guest|agent-guard)]
[srctarget=(any|[!]<objectname>[,<objectname>[,<objectname>[,...]]])]
[srcportop=(eq|ne|gt|lt)]
[srcport=(any|<objectservice>[,<objectservice>[,<objectservice>[,...]]])]
[srcif=(any|<interface name>)]
[srcgeo=(<objectgeo[|<objectgeo>[|...]]])]
[srciprep=(<objectiprep[|<objectiprep>[|...]]])]
[srchostrep=(<0-65535>)]
[srchostrepop=(lt|gt)]
[via=(any|sslvpn|httpproxy|ipsec|sslproxy|none)]
[dsttarget=(any|[!]<objectname>[,<objectname>[,<objectname>[,...]]])]
[dstportop=(eq|ne|gt|lt)]
[dstport=(any|<objectservice>[,<objectservice>[,<objectservice>[,...]]])]
[dstif=(any|<interface name>)]
[dstgeo=(<objectgeo[|objectgeo[|...]]])]
[dstiprep=(<objectiprep[|objectiprep[|...]]])]
[dsthostrep=(<0-65535>)]
[dsthostrepop=(lt|gt)]
[natsrctarget=(|original|<object name>)] (empty value to disable nat on source)
[natsrclb=(none|roundrobin|srchash|connhash|random)]
[natsrcarp=(on|off)]
[natsrcportop=(eq|ne|gt|lt)]
[natsrcport=(original|<objectservice>|<port range>)]
[natsrcportlb=(none|random)]
[natdsttarget=(|original|<object name>)] (empty value to disable nat on destination)
[natdstlb=(none|roundrobin|srchash|connhash|random)]
[natdstarp=(on|off)]
[natdstportop=(eq|ne|gt|lt)]
[natdstport=(original|<objectservice>|<port range>)]
[natdstportlb=(none|roundrobin|srchash|connhash|random)]
[beforevpn=(on|off)]
[enforceipsecforward=(on|off)]
[enforceipsecreverse=(on|off)]
[comment=<string>]
[rulename=<string>]


    scope: local|global

Use global or local slot, (default to local).

    slot: 0-10

Slot number (default to 5).

    activate: yes|no

Activate the slot (default to yes).

    mode: add|reset|del

With `reset`, flush the rules before adding, `add` inserts rules in existing slot, `del` deletes specified rules  (default to `reset`).

Note: ackqosid parameter appears in 4.3.0

Dependencies
------------

None.

Example Playbook
----------------

This playbook will configure filter and nat policies.

    - hosts: sns_appliances
      roles:
          - role: sns-policy
            activate: yes
            slot: 5
            filter:
              - { action: pass, srctarget: any, dsttarget: Firewall_out, dstport: ssh, comment: "Allow SSH"}
              - { action: block, srctarget: any, srcif: out, dsttarget: any }
              - { action: pass, srctarget: any, dsttarget: any, inspection: firewall }
            nat:
              - { action: nat, srctarget: network_in, dsttarget: Internet, dstif: out, natsrctarget: firewall_out, natsrcport: ephemeral_fw }


License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

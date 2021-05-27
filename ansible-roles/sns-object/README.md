Ansible Role: sns-object
=========

This role updates the object base of Stormshield Network Security appliances.

Requirements
------------

The Ansible-SNS module and python-SNS-API package are required.

- https://github.com/stormshield/ansible-SNS
- https://github.com/stormshield/python-SNS-API

Role Variables
--------------

    csvfileimport: [<file.csv>]
    hosts:
      - { name: <hostname>, ip: <ipaddress>, ipv6: <ipv6address>, type: router|server|host, resolve: static|dynamic|manual, mac: xx:xx:xx:xx:xx:xx, color: xxxxxx, comment: <comment> }
    ranges:
      - { name:<rangename>, begin:<range first ip>, end:<range last ip>, beginv6:<range first ipv6>, endv6:<range last ipv6>, color:xxxxxx, comment:<comment>}
    networks:
      - { name:<netname>, ip=<network IPV4 address>, mask:<netmask>, ipv6:<network IPv6 address>, prefixlenv6:<prefixlen>, color:xxxxxx, comment:<comment>  }
    netgroups:
      - { name:<groupname>, comment:<group comment>, members: [], mode: <add|reset> }
    services:
      - { name:<servicename>, port:<port number>, proto:<tcp|udp|any>, toport:<porthigh>, color:xxxxxx, comment:<comment> }
    servicegroups:
      - { name:<servicegroupname>, comment=<servicegroup comment>, members: [], mode: <add|reset> }
    protocols:
      - { name:<protocolname>, protonumber:<IP protocol number>, color:xxxxxx, comment=<comment> }
    timeobjects:
      - { name:<timeobject name>, time:(|hh:mm-hh:mm[;hh:mm-hh:mm]...), weekday:(|dow[-dow][;dow[-dow]]...), yearday:(|mm:dd[-mm:dd][;mm:dd[-mm:dd]]...), date:(|yyyy:mm:dd[:hh:mm][-yyyy:mm:dd[:hh:mm]]), color:xxxxxx, comment:<comment> }
    fqdnobjects:
      - { name:<fqdn>, ip:<ipaddress>, ipv6:<ipv6address>, color:xxxxxx, comment:comment> }
    geogroups:
      - { name:<geogroupname>, comment:<geogroup comment>, members: [], mode: <add|reset> }
    iprepgroups:
      - { name:<iprepgroupname>, comment:<iprepgroup comment>, members: [], mode: <add|reset> }
    routers:
      - { name:<router name>, monitor:(ICMP|TCP_PROBE), comment:<comment>, tries:<int>, wait:<seconds>, frequency:<seconds> gatewaythreshold:<int>, activateallbackup:(on|off), loadbalancing:<none|connhash|srchash>, onfailpolicy:(pass|block), gateways:[ {type:<principalgateway|backupgateway>, host:<host>, check:<host|group>, weight:<int>, monitor: <none|icmp|all>} ], mode: <add|reset> }
    internet:
      object: <host|network|range|group>
      operator: <ne|eq>
    qos:
      bandwidth: <bw kbps>
      drop: <0 (TailDrop) |1 (Blue)>
      defaultqueue: <qid|bypass>
      qids:
        - { name:<qid>, comment:<comment> (type:CBQ, min:<min>, min_rev:<minrev>, max:<max>, max_rev:<maxrev>) | (type:<PRIQ>, pri:<pri>), color:<color>, length:<queue_length>, prioritizeack:<on|off>,prioritizelowdelay:<on|off> }

List of objects to create or update.

For groups, `mode: add` adds members to an existing group, `mode: reset` empties the group before adding members, `mode: del` remove members from the group. Default to `reset`.

    state: absent

If set to `absent`, delete the objects. The Internet object can't be deleted and is common to local and global base.

    scope: local|global

Choose object base (default to local). QIDs are only local.


Dependencies
------------

None.

Example Playbook
----------------

This playbook creates objects on SNS appliance:

    ---
    - hosts: sns_appliances
      roles:
        - role: sns-object
          hosts :
            - { name: myhost, ip: 1.2.3.4, comment: "My comment"}
          networks:
            - { name: mynetwork, ip: 10.0.0.0, mask: 255.0.0.0 }
          netgroups:
            - { name: mygroup, members: myhost, mynetwork] }
          routers:
            - { name: myrouter, gatewaythreshold: 1, gateways: [ { type: principalgateway, host: myhost1 }, { type: backupgateway, host: myhost2 } ] }
          geogroups:
            - { name: mygeogroup, members: ["eu:fr", "eu:de"] }
          timeobjects:
            - { name: mytime1, time: "08:00-12:00", weekday: "1;2;3;4;5" }
          internet:
            object: Network_internals
            operator: ne


This playbook deletes an object:

    ---
    - hosts: sns_appliances
      roles:
        - role: sns-object
          state: absent
          networks :
            - { name: mynetwork }

This playbook import a CSV file describing the objects:

    ---
    - hosts: sns_appliances
      roles:
        - role: sns-object
          csvfileimport:
            - /path/myobjects.csv

License
-------

Apache version 2.0

Author Information
------------------

Stormshield 2020

https://www.stormshield.com

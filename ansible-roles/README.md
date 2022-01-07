# Ansible roles

## Roles

- **sns-backup**: configuration backup and restore
- **sns-firmware-upgrade**: upgrade firmware for single appliance and high availability cluster
- **sns-object**: configure the object database
- **sns-ntp**: configure time and NTP service
- **sns-dns**: configure the DNS servers
- **sns-policy** configure the filter and NAT policies
- **sns-url**: configure the URL groups and slots
- **sns-alarm**: configure the alarms

See the README in each role folder to get the detailed documentation of each role.

Note: installation instructions are given for Ubuntu 20.04 as example.

### Install Ansible and python-SNS-API

```
sudo apt install git python3-pip
pip3 install ansible
pip3 install stormshield.sns.sslclient
```

Note: when using a packaged version of Ansible, be sure to install the python-SNS-API using the same python environment than Ansible. `ansible --version` indicates which python env is used.

See https://github.com/stormshield/python-SNS-API for more information.

### Install SNS Ansible module

```
cd /tmp
git clone https://github.com/stormshield/ansible-SNS
sudo mkdir -p /usr/share/ansible/plugins/modules
cp /tmp/ansible-SNS/library/* /usr/share/ansible/plugins/modules

```

Note: SNS Ansible module is installed system wide, it can be installed for one user only in `~/.ansible/plugins/modules`.

See https://github.com/stormshield/ansible-SNS for more information.

### Install SNS roles

```
sudo apt install git python3-dnspython
cd /tmp
git clone https://github.com/stormshield/sns-scripting
sudo mkdir -p /etc/ansible/roles
sudo cp -r sns-scripting/ansible-roles/sns-* /etc/ansible/roles
```

Note: roles are installed system wide, they can be installed locally in a `roles/` folder at the playbook level.

### Create an inventory file

Edit `/etc/ansible/hosts` and add your SNS appliances.

```
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 10.0.0.254
        user: admin
        password: secret
        sslverifyhost: false
```

If you want to verify the CN of the appliance certificate, set the `host` parameter to the appliance serial number and the `ip` parameter to the product IP address.

```
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: VMSNSX08K000111
        ip: 10.0.0.254
        user: admin
        password: secret
        sslverifyhost: true
```

Note: a local inventory file can be used by adding -i inventory.yml to the `ansible-playbook` command.

### Improve ansible-playbook output (optional)

 Edit `~/.ansible.cfg`:
 ```
[defaults]
bin_ansible_callbacks=True
stdout_callback = yaml
localhost_warning = false
display_skipped_hosts = false
```

### Execute a playbook

Create a playbook named `sysprop.yml`.

```
- hosts: sns_appliances
  tasks:
  - name: Get appliance information
    sns_command:
      appliance: "{{ hostvars[inventory_hostname].appliance }}"
      command: SYSTEM PROPERTY
    register: sysprop
  
  - name: Extract version
    sns_getconf:
      result: "{{ sysprop.result }}"
      section: Result
      token: Version
    register: version
  
  - name: Extract model
    sns_getconf:
      result: "{{ sysprop.result }}"
      section: Result
      token: Model
    register: model

  - name: Get appliance name
    sns_command:
      appliance: "{{ hostvars[inventory_hostname].appliance }}"
      command: SYSTEM IDENT
    register: ident

  - name: Extract system name
    sns_getconf:
      result: "{{ ident.result }}"
      section: Result
      token: SystemName
    register: sysname

  - debug:
      msg: "Appliance: {{ sysname.value }}, model: {{ model.value }}, firmware version: {{ version.value }}"
```

Run the playbook:

```
$ ansible-playbook sysprop.yml

PLAY [sns_appliances] *******************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [appliance1]

TASK [Get appliance information] ********************************************************************************************************************************************
changed: [appliance1]

TASK [Extract version] ******************************************************************************************************************************************************
changed: [appliance1]

TASK [Extract model] ********************************************************************************************************************************************************
changed: [appliance1]

TASK [Get appliance name] ***************************************************************************************************************************************************
changed: [appliance1]

TASK [Extract system name] **************************************************************************************************************************************************
changed: [appliance1]

TASK [debug] ****************************************************************************************************************************************************************
ok: [appliance1] =>
  msg: 'Appliance: UTM1, model: EVA1, firmware version: 4.0.3'

PLAY RECAP ******************************************************************************************************************************************************************
appliance1                 : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Using roles

### Configuration backup

This playbook will backup all the configuration of SNS appliances in the inventory to a local folder using the `sns-backup` role.

Create a playbook named `backup.yml`:
```
- hosts: sns_appliances
  roles:
    - role: sns-backup
      backup_path: "./backup"
      backup: "mybackup.na"
      timestamp_prefix: true
```

Run the playbook:

```
$ mkdir ./backup

$ ansible-playbook backup.yml

PLAY [sns_appliances] *******************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [appliance1]

TASK [sns-backup : Set backup file (with timestamp)] ************************************************************************************************************************
ok: [appliance1]

TASK [sns-backup : Backup configuration] ************************************************************************************************************************************
changed: [appliance1]

PLAY RECAP ******************************************************************************************************************************************************************
appliance1                 : ok=3    changed=1    unreachable=0    failed=0    skipped=7    rescued=0    ignored=0

$ ls ./backup
20200520T175355_mybackup.na
```

### Configure a policy

This playbook will allow a user network to access the https intranet server.

Create a playbook named `policy.yml`:
```
- hosts: sns_appliances
  roles:
    - role: sns-object
      hosts :
      - { name: intranet, ip: 192.168.2.1, comment: "Intranet server"}
      networks:
      - { name: usernetwork, ip: 192.168.1.0, mask: 255.255.255.0 }
    - role: sns-policy
      activate: yes
      slot: 5
      filter:
      - { action: pass, srctarget: usernetwork, dsttarget: intranet, dstport: https, comment: "Intranet"}
      - { action: pass, srctarget: any, dsttarget: any, comment: "Warning, pass all example"}
```

Run the playbook:
```
PLAY [sns_appliances] *******************************************************************************************************************************************************

[...]

TASK [sns-policy : Save rules] **********************************************************************************************************************************************
ok: [appliance1]

TASK [sns-policy : Activate slot] *******************************************************************************************************************************************
ok: [appliance1]

TASK [sns-policy : Execute script] ******************************************************************************************************************************************
changed: [appliance1]

PLAY RECAP ******************************************************************************************************************************************************************
appliance1                 : ok=26   changed=2    unreachable=0    failed=0    skipped=40   rescued=0    ignored=0
```


## Encrypt SNS passwords with Ansible Vault

SNS passwords can be read in the inventory:

```yaml
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 192.168.152.129
        user: admin
        password: secret
        sslverifyhost: false
```

To add a layer of security, we can create a ciphered file protected by a master password which will contains all the SNS passwords.

### Create a encrypted variable file for the inventory group

    mkdir -p groups_vars/sns_appliances
    ansible-vault create groups_vars/sns_appliances/vault.yml

The encrypted file can be later edited:

    ansible-vault edit groups_vars/sns_appliances/vault.yml

### Add entries for the inventory

```yaml
---
utm1_password: "secret"
```

### Edit the inventory and replace the password by the variable referencing the encrypted password:

```yaml
sns_appliances:
  hosts:
    utm1:
      ansible_connection: local
      appliance:
        host: 10.0.0.254
        user: admin
        password: "{{utm1_password}}"
        sslverifyhost: false
```

### Run the playbook and provide the master password:

    ansible-playbook -i inventory.yml --ask-vault-pass sysprop.yml

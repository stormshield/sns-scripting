# SNS Ansible Docker image

This docker image embeds Ansible, the SNS module and roles in one container.

Files are shared via a bind mount, copy the playbooks and get result files (backups for example) in the home folder.

## Build

    docker build --tag sns-ansible:latest .


## Usage

### Edit the inventory file

    ./sns-ansible.sh vi /etc/ansible/hosts

or

    vi config/hosts

### Run a playbook

Get firmware version:

    ./sns-ansible.sh ansible-playbook sysprop.yml

Backup the configuration:

    ./sns-ansible.sh ansible-playbook backup.yml

The backup files are available in `home/backup`.

### Open a shell session

    ./sns-ansible.sh bash

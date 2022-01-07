FROM ubuntu:latest

# upgrade OS and install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3-pip python3-dnspython joe vim

# install python modules
RUN pip3 install ansible stormshield.sns.sslclient

# install ansible module from github
RUN cd /tmp && \
    git clone https://github.com/stormshield/ansible-SNS && \
    mkdir -p /usr/share/ansible/plugins/modules && \
    cp /tmp/ansible-SNS/library/* /usr/share/ansible/plugins/modules && \
    rm -rf /tmp/ansible-SNS

# install roles from github
RUN cd /tmp && \
    git clone https://github.com/stormshield/sns-scripting && \
    mkdir -p /etc/ansible/roles && \
    cp -r sns-scripting/ansible-roles/sns-* /etc/ansible/roles && \
    rm -rf /tmp/sns-scripting

WORKDIR /sns-ansible

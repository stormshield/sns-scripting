#!/bin/sh

docker run --rm -it \
    --mount type=bind,source="$(pwd)"/home,target=/sns-ansible \
    --mount type=bind,source="$(pwd)"/config/hosts,target=/etc/ansible/hosts \
    sns-ansible:latest $@


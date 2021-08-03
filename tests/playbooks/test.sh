#!/bin/bash
set -x
set -e

_pwd=$(dirname "$0")
tempDir=$(mktemp -d)

cd $_pwd

# ANSIBLE_DEBUG=true -vvvv

# --skip-starting-state

ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes ' \
ansible-playbook \
    -i ./inventory.ini \
    -i vagrant-groups.ini \
    ./playbooks.yml

# vagrant snapshot save [vm-name] NAME
# vagrant snapshot restore
# vagrant snapshot list


# https://raymii.org/s/tutorials/Ansible_-_Playbook_Testing.html
# ansible-playbook --syntax-check --list-tasks -i tests/ansible_hosts
# ./example-playbook.yml


# Stories
# Stop one slave then add another
# vagrant destroy slave 1
# vagrant destroy amsh-3
# store file in config volume
# store file in config volume

[ -n "$tempDir" ] && rm -rf "$tempDir"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, [Jean Claveau (https://github.com/jclaveau)]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import sys
import subprocess
import os
import argparse
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


parser = argparse.ArgumentParser(description='This script runs the testcases playbooks')

parser.add_argument('--testcases', metavar='T', type=str, nargs='+', help='the testcases to run', default=None)

# --skip-starting-state

args = parser.parse_args()
requested_testcases = args.testcases
requested_testcases = list(dict.fromkeys(requested_testcases)) # remove duplicates

# print(requested_testcases)


scan = os.scandir('.')
testcase_dirs = []
for entry in scan:
    if entry.is_dir() and re.fullmatch(r'^\d+_\w+$', entry.name):
        if requested_testcases is None:
            testcase_dirs.append(entry.name)
        elif entry.name in requested_testcases:
            testcase_dirs.append(entry.name)
            requested_testcases.remove(entry.name)

scan.close()
if len(requested_testcases):
    # TODO implement argparse action  to handle the error?
    print('Error: Testcases not found')
    print(requested_testcases)
    quit()

testcase_dirs.sort()

my_env = os.environ.copy()
my_env['ANSIBLE_HOST_KEY_CHECKING'] = 'False'
my_env['ANSIBLE_SSH_ARGS'] = '-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes '
# ANSIBLE_DEBUG=true -vvvv

subprocess.call([
    "ansible-playbook",
    "-i ./inventory.ini",
#     -i vagrant-groups.ini \
    "./playbooks.yml",
    "--extra-vars",
    "testcase=" + testcase_dirs[0],
], env=my_env)

# https://raymii.org/s/tutorials/Ansible_-_Playbook_Testing.html
# ansible-playbook --syntax-check --list-tasks -i tests/ansible_hosts
# ./example-playbook.yml

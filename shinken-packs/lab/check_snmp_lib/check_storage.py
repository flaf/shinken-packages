#!/usr/bin/python
# -*- coding: utf-8 -*-

import check_snmp_lib.common as common
import subprocess

help_message = """
Usage:
  check_snmp storage (-h | --help)
  check_snmp storage -w <warning> -c <critical> %s

Options:
%s
  -w <warning>, --warning=<warning>
        With -w 80, the ckeck raises a warning if one local
        files system at least is full at more than 80%%.
  -c <critical>, --critical=<critical>
        With -c 90, the ckeck raises a critical if one local
        files system at least is full at more than 90%%.
""" % (common.common_syntax, common.common_help,)

OID = 'NET-SNMP-EXTEND-MIB::nsExtendOutputFull."get_storage"'

# d is the dictionary of options.
def run(d):
    cmd_tokens = ['snmpget', '-OvQ'] +  common.snmpcmd_common_options(d) + [OID]
    try:
        output = subprocess.check_output(cmd_tokens, shell=False, stderr=subprocess.STDOUT)
        lines = output.strip().split('\n')
        for l in lines:
            l = l.split(':')
            directory = l[1]
            size = l[2]
            used = l[3]
            human_readable_size = l[4]
            human_readable_used = l[5]

        print('--' + output + '--')
    except subprocess.CalledProcessError as e:
        print('return value != 0')
        print('--' + str(e.returncode) + '--')
        print('--' + e.output + '--')



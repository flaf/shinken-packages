#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

common_syntax = """-H <host-address> -t <timeout>
      (--v2c -C <community> -l <login> -x <passwd> -X <privpass> -L <protocols>)"""

common_help = """  -h, --help
        Show this help message and exit.
  -H <host-address>, --host=<host-address>
        Set the address of the host.
  -t <timeout>, --timeout=<timeout>
        Set the timeout, in seconds, of the SNMP request.
  --v2c
        Use SNMP V2c instead of SNMP V3.
  -C <community>, --community=<community>
        Set the community password for SNMP V2c.
  -l <login>, --login=<login>
        Set the login for SNMP V3.
  -x <passwd>, --passwd=<passwd>
        Set the auth password for SNMP V3.
  -X <privpass>, --privpass=<privpass>
        Set the priv password for SNMP V3.
  -L <protocols>, --protocols=<protocols>
        Set the auth and priv protocols for SNMP V3. The authorised
        values are: "md5,des" "md5,aes" "sha,des" and "sha,aes"."""

protocols_list = [ 'md5,des', 'md5,aes', 'sha,des', 'sha,aes' ]

# d is the dictionary of options.
def auth_snmpcmd_options(d):
    if d['--v2c'] == True:
        return ['-v', '2c', '-c', d['--community'], ]
    else:
        protocols = d['--protocols'].lower()
        if protocols not in protocols_list:
            print("Sorry, '%s' isn't a correct value for the --protocols option.") % (protocols,)
            sys.exit(1)
        authproto = protocols.split(',')[0]
        privproto = protocols.split(',')[1]
        return ['-v', '3', '-u', d['--login'], '-l', 'authPriv',
                '-A', d['--passwd'], '-a', authproto,
                '-X', d['--privpass'], '-x', privproto,
               ]

# d is the dictionary of options.
def snmpcmd_common_options(d):
    auth = auth_snmpcmd_options(d)
    return auth + ['-r', '0', '-t', d['--timeout'], d['--host']]



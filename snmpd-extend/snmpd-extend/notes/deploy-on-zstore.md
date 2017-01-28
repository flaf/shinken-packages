# How to deploy this package in zstore-1,2


```sh
# Copy binaries.
cp ./sharebin/get_lockd_threads /usr/local/bin/ && chown root:root /usr/local/bin/get_lockd_threads && chmod 755 /usr/local/bin/get_lockd_threads
cp ./sharebin/get_zpool_status  /usr/local/bin/ && chown root:root /usr/local/bin/get_zpool_status  && chmod 755 /usr/local/bin/get_zpool_status

# Update snmpd configuration.
echo "
extend get_zpool_status  /usr/local/bin/get_zpool_status
extend get_lockd_threads /usr/local/bin/get_lockd_threads
" > /etc/net-snmp/snmp/snmpd.local.conf

# Restarting of snmpd.
svcadm disable net-snmp && sleep 1 && svcadm enable net-snmp && echo OK
```



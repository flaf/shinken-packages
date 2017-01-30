# How to retrieve `check_dns`

In fact, this nagios plugin just comes from the package
`nagios-plugins-contrib` on Debian **Wheezy** :

But the problem of the package `nagios-plugins-contrib` is
there are lot of useless dependencies (for instance with
samba packages) which I don't want to install in production.

```sh
apt-get update && apt-get install nagios-plugins-standard
scp /usr/lib/nagios/plugins/check_dns $my_host:~ # etc.
```



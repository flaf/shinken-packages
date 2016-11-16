# How to build `check_http_cookie` to have cookie support on redirection

Made on Debian **Wheezy** :


```sh
apt-get update
apt-get install devscripts quilt dpatch autotools-dev libldap2-dev libpq-dev libmysqlclient-dev libradiusclient-ng-dev libnet-snmp-perl hardening-wrapper
apt-get source nagios-plugins-basic
cd nagios-plugins-1.4.16/

export QUILT_PATCHES=debian/patches
export QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"

# The patch is applied.
patch -p1 < /path/to/.../check-http-cookie/check-http-cookie.diff

time debuild -b -us -uc && echo 'Building is OK!'

# After the build, the file check_http is present here.
ls -l plugins/check_http
```



#!/usr/bin/python
# -*- coding: utf-8 -*-

import pycurl
import cStringIO
from urllib import urlencode

post_data = { 'phone': '0676553219', 'msg': "Éléphant ça va ?" }
postfields = urlencode(post_data)

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://172.30.240.23/cgi-bin/sendsms.pl')
c.setopt(c.WRITEFUNCTION, buf.write)
c.setopt(c.POSTFIELDS, postfields)
c.perform()

output = buf.getvalue()
buf.close()

print output,


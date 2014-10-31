#!/usr/bin/python
# -*- coding: utf-8 -*-

from spnotify import *
from nose.tools import *



def test_Rule():

    contact_pattern = u'^(john|bob)$'
    ts = TimeSlots()
    ts.add(u'[12h00;13h35][23h00;23h59]')
    name = u'john'
    service_desc_regex = u'^disk space$'
    service_desc = u'disk space'
    hostname = u'srv-2'
    now = datetime.time(23, 2)

    def test():
        rule = Rule(
            contact_names = Regexp(contact_pattern),
            hostnames = Regexp(u'^srv-'), timeslots = ts,
            service_desc = Regexp(service_desc_regex))
        contact = Contact(
            name = name, sms_threshold = 4, rarefaction_threshold = 15,
            email = u'john@domain.tld', phone_number=u'0666666666')
        notif = Notification(
            contact = contact, hostname = hostname, address = u'172.31.0.1',
            ntype = u'Problem', state = u'CRITICAL', business_impact = 4,
            additional_info = u'CRITICAL, there is a big problem',
            number = 7, service_desc = service_desc, time = now)
        return rule.is_matching_with(notif)

    assert_equal(test(), True)

    now = datetime.time(0, 0) # time doesn't match
    assert_equal(test(), False)

    now = datetime.time(23, 0)
    hostname = u'wsrv-2' # hostname doesn't match
    assert_equal(test(), False)

    contact_pattern = u'!^(john|bob)$'
    hostname = u'srv-2'
    name = u'bobby' # name doesn't match but the pattern begins with '!'
    assert_equal(test(), True)

    name = u'bob' # name matches but the pattern begins with '!'
    assert_equal(test(), False)

    name = u'pit' # it's matched (it's host notification)
    service_desc_regex = u''
    service_desc = None
    assert_equal(test(), True)

    name = u'john'
    service_desc_regex = u'cpu'
    service_desc = None
    assert_equal(test(), False)


def test_Regexp():

    r1 = Regexp(u'^(aaa|bbb)')
    r2 = Regexp(u'!^(aaa|bbb)') # '!' must reverse the regex.
    r3 = Regexp(u'') # an empty regex must catch nothing.
    assert_false(r1.is_empty())
    assert_true(r3.is_empty())
    assert_true(r1.catch(u'aaaxxxx'))
    assert_false(r1.catch(u'xaaaxxxx'))
    assert_true(r2.catch(u'xaaaxxxx'))
    assert_false(r2.catch(u'aaaxxxx'))
    assert_false(r3.catch(u''))
    assert_false(r3.catch(u'any'))


def test_Notification():

    c = Contact(
       name=u'john', sms_threshold=4, rarefaction_threshold=10,
       email=u'john@domain.tld', phone_number=u'0666666666')
    notif = Notification(
        contact=c, hostname=u'google', address=u'www.google.fr',
        ntype=u'PROBLEM', state=u'CRITICAL', business_impact=4,
        additional_info=u'http is out!', number=34, service_desc=u'http')


def test_Contact():

    c = Contact(name=u'john', sms_threshold=4, rarefaction_threshold=10,
                email=u'john@domain.tld', phone_number=u'0666666666')



#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: 2013 Francois Lafont <francois.lafont@ac-versailles.fr>
#
# License: GPL-3.0+
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import datetime
import subprocess
import re
import string
import pycurl
import cStringIO
import ast
from urllib import urlencode



class Rule:
    """Represents a rule in a black list file."""

    def __init__(self, contact_names, hostnames, timeslots, weekdays,
                 service_desc=None):
        assert isinstance(contact_names, Regexp)
        assert isinstance(hostnames, Regexp)
        assert isinstance(timeslots, TimeSlots)
        assert isinstance(service_desc, Regexp) or (service_desc is None)
        assert isinstance(weekdays, Weekdays)
        self.contact_names = contact_names
        self.hostnames = hostnames
        self.service_desc = service_desc
        if self.service_desc.is_empty():
            self.service_desc = None
        self.timeslots = timeslots
        self.weekdays = weekdays

    def is_matching_with(self, notif):
        assert isinstance(notif, Notification)
        if self.service_desc == None and notif.service_desc == None:
            # This is a host rule and a host notification.
            if self.contact_names.catch(notif.contact.name):
                if self.hostnames.catch(notif.hostname):
                    if notif.time in self.timeslots:
                        if datetime.datetime.now().isoweekday() in self.weekdays:
                            # The rule is matching.
                            return True
        elif self.service_desc != None and notif.service_desc != None:
            # This is a service rule and a service notification.
            if self.contact_names.catch(notif.contact.name):
                if self.hostnames.catch(notif.hostname):
                    if self.service_desc.catch(notif.service_desc):
                        if notif.time in self.timeslots:
                            if datetime.datetime.now().isoweekday() in self.weekdays:
                                # The rule is matching.
                                return True
        # If no matching.
        return False

    def __repr__(self):
        return repr(self.timeslots)


class Weekdays:
    """Represents a set of weekdays."""

    def __init__(self, s):
        assert isinstance(s, unicode)

        try:
            if s == u'*':
                # * is special, it means all days.
                self.days = [1, 2, 3, 4, 5, 6, 7]
            else:
                self.days = ast.literal_eval(s)
        except:
            # There is a problem with the string s which
            # is not a list, so the instance contains nothing.
            logger = Logger()
            logger.write(u"Problem in the blacklist file, the string `%s' is not a valid weekdays list." % s)
            del(logger)
            self.days = []

        for day in self.days:
            if day not in [1, 2, 3, 4, 5, 6, 7]:
                # There is a day not valid in the string,
                # so the instance contains nothing.
                logger = Logger()
                logger.write(u"Problem, the string %s is a list with invalid numbers." % s)
                del(logger)
                self.days = []
                break

    def __contains__(self, day):
        assert day in [1, 2, 3, 4, 5, 6, 7]
        return (day in self.days)


class Regexp:
    """Represents a regexp."""

    def __init__(self, s):
        assert isinstance(s, unicode)
        if s == '':
            self.reverse = False
            self.pattern = ''
        elif s[0] == '!':
            self.reverse = True
            self.pattern = s[1:]
        else:
            self.reverse = False
            self.pattern = s

    def is_empty(self):
        if self.pattern == '':
            return True
        else:
            return False

    def catch(self, s_test):
        assert isinstance(s_test, unicode)
        if self.pattern == '':
            # An empty pattern catches nothing
            return False
        else:
            try:
                if self.reverse:
                    return not bool(re.search(self.pattern, s_test))
                else:
                    return bool(re.search(self.pattern, s_test))
            except:
                logger = Logger()
                logger.write(u"Problem the regex %s is not a valid" % s)
                del(logger)
                # If there is a problem, the Regexp doesn't catch.
                return False


class Notification:
    """Represents a notification to a contact."""

    date_now = datetime.datetime.now().replace(microsecond=0)
    time_now = date_now.time()
    sender = os.uname()[1]
    subject_pattern = u''
    message_pattern = u''

    def __init__(
            self, contact,
            hostname, address, ntype, state, business_impact,
            additional_info, number, service_desc=None, time=None, file_name=None):
        assert isinstance(contact, Contact)
        assert isinstance(hostname, unicode)
        assert isinstance(address, unicode)
        assert isinstance(ntype, unicode)
        assert isinstance(state, unicode)
        assert isinstance(business_impact, int)
        assert isinstance(additional_info, unicode)
        assert isinstance(number, int)
        assert isinstance(service_desc, unicode) or (service_desc is None)
        assert isinstance(time, datetime.time) or (time is None)
        assert isinstance(file_name, unicode) or (file_name is None)
        self.contact = contact
        self.hostname = hostname
        self.address = address
        self.ntype = ntype
        self.state = state
        self.business_impact = business_impact
        self.additional_info = additional_info
        self.number = number
        self.service_desc = service_desc
        self.time = time
        self.date = Notification.date_now
        self.file_name = file_name
        if self.time == None:
            self.time = Notification.time_now
        self.sender = Notification.sender
        self.logger = Logger()

    def get_subject(self):
        return string.Template(self.subject_pattern).substitute(self.__dict__)

    def get_message(self):
        return string.Template(self.message_pattern).substitute(self.__dict__)

    def get_short_message(self):
        return string.Template(self.short_message_pattern).substitute(self.__dict__)

    def get_mini_message(self):
        return string.Template(self.mini_message_pattern).substitute(self.__dict__)

    def __repr__(self):
        t = (self.contact.name, self.number, self.contact.rarefaction_threshold,
             self.hostname, self.service_desc, self.ntype, self.state,
             self.additional_info)
        return str(t)

    def send_email(self):
        if self.contact.email is None:
            msg = u"No e-mail sending to %s which is not a valid " \
                  "address: " % (self.contact.email,) + str(self)
            self.logger.write(msg)
            return None

        try:
            p = subprocess.Popen(
                ['mail', '-s', self.get_subject(), self.contact.email],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            p.communicate(input=self.get_message().encode('utf-8'))
            self.logger.write(u"Notification sent by e-mail to %s: " \
                              % (self.contact.email,) + str(self))
        except:
            msg = u"Problem with the e-mail sending to %s and the 'mail' " \
                  u"command: " % (self.contact.email,) + str(self)
            self.logger.write(msg)

    def write_in_file(self):
        try:
            f = open(self.file_name, 'a')
            f.write(self.get_short_message().encode('utf-8'))
            f.close()
            self.logger.write(u"Notification sent by file %s: " \
                              % (self.file_name) + str(self))
        except:
            self.logger.write(u'Problem with the writing in the "%s" file: ' \
                              % (self.file_name,) + str(self))

    def send_sms(self):
        phone = self.contact.phone_number
        if phone is not None:
            phone = phone.encode('utf-8')
        sms_threshold = self.contact.sms_threshold
        sms_url = self.contact.sms_url.encode('utf-8')
        msg = self.get_mini_message().encode('utf-8')
        business_impact = self.business_impact
        if phone is not None and business_impact >= sms_threshold:
            try:
                post_data = { 'phone': phone, 'msg': msg }
                postfields = urlencode(post_data)
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, sms_url)
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.setopt(c.POSTFIELDS, postfields)
                c.setopt(c.TIMEOUT, 5)
                c.perform()
                output = buf.getvalue()
                buf.close()
                if output.upper().startswith(u'OK'):
                    self.logger.write("SMS sent to %s" % phone + ' ' + str(self))
                else:
                    self.logger.write("Failed to send SMS to %s" \
                                      % phone + ' ' + str(self))
            except Exception as e:
                if 'buf' in globals(): buf.close()
                self.logger.write("Failed to send SMS to %s. Exception raised %s" \
                                  % (phone + ' ' + str(self), e))


    def send(self):
        if self.file_name:
            self.write_in_file()
        else:
            self.send_email()
        self.send_sms()

    def in_rarefaction_range(self):
        R = self.contact.rarefaction_threshold
        N = self.number
        if R > 0 and N >= R and (N %10 != 0):
            return True
        else:
            return False


class HostNotification(Notification):

    subject_pattern = u'$hostname $ntype: state is $state'
    message_pattern = u'''This is a shinken notification from $sender server.

Host: $hostname (address $address)
State: $state (business impact $business_impact/5)
Date: $date

Additional info
$additional_info
'''
    # The last \n is crucial. If absent, the last line isn't sent.

    short_message_pattern = '''
$hostname ($address) $ntype: state is $state.
Additional info: $additional_info
'''

    mini_message_pattern = \
'''$hostname ($address) $ntype: state is $state.
Date: $date'''


class ServiceNotification(Notification):

    subject_pattern = u'$hostname $ntype: "$service_desc" in $state state'
    message_pattern = u'''This is a shinken notification from $sender server.

Service: $service_desc
Host: $hostname (address $address)
State: $state (business impact $business_impact/5)
Date: $date

Additional info
$additional_info
'''
    # The last \n is crucial. If absent, the last line isn't sent.

    short_message_pattern = '''
$hostname ($address) $ntype: \"$service_desc\" in $state state.
Additional info: $additional_info
'''

    mini_message_pattern = \
'''$hostname ($address) $ntype: \"$service_desc\" in $state state.
Date: $date'''


class Contact:
    """Represents a contact."""

    def __init__(self, name, sms_threshold, sms_url, rarefaction_threshold,
                 email=None, phone_number=None):
        assert isinstance(name, unicode)
        assert isinstance(sms_threshold, int)
        assert isinstance(sms_url, unicode)
        assert isinstance(rarefaction_threshold, int)
        assert isinstance(email, unicode) or (email is None)
        assert isinstance(phone_number, unicode) or (phone_number is None)
        self.name = name
        self.sms_threshold = sms_threshold
        self.sms_url = sms_url
        self.rarefaction_threshold = rarefaction_threshold
        if email is not None and u'@' in email:
            self.email = email
        else:
            self.email = None
        if phone_number is not None and re.search(ur'^[0-9]+$', phone_number):
            self.phone_number = phone_number
        else:
            self.phone_number = None


class TimeSlot:
    """Represents a time slot.
    Takes 2 datetime.time arguments and represents the time
    slot between this 2 datetimes. In this example below,
    ts is represents [14h30; 17h47] time slot."""

    def __init__(self, t1, t2):
        assert isinstance(t1, datetime.time) and isinstance(t1, datetime.time)
        assert t1 <= t2
        self.t1 = t1
        self.t2 = t2

    def __contains__(self, time):
        assert isinstance(time, datetime.time)
        # Round the time to the minute.
        rounded_time = datetime.time(time.hour, time.minute)
        return self.t1 <= rounded_time <= self.t2

    def __repr__(self):
        # Secondes are removed.
        return '[%s-->%s]' % (str(self.t1)[0:5], str(self.t2)[0:5])


class TimeSlots:
    """Represents an union of TimeSlot objects.
    Takes one argument which must be a list of TimeSlot objects.
    If the argument is omitted, the list is an empty list.
    The .add method takes one argument which can be a TimeSlot
    objet or an unicode string which represents an of timeslots."""

    timeslots_pattern = r'^(\[\d+h\d+;\+?\d+h\d+\])+$'
    timeslots_regex = re.compile(timeslots_pattern)
    numbers_regex = re.compile(r'\+?\d+')

    def __init__(self, timeslots=None):
        if timeslots is None:
            timeslots = []
        assert isinstance(timeslots, list)
        for ts in timeslots:
            assert isinstance(ts, TimeSlot)
        self.timeslots = timeslots

    def add(self, ts):
        assert isinstance(ts, TimeSlot) or isinstance(ts, unicode)
        if isinstance(ts, TimeSlot):
            self.timeslots.append(ts)
        elif isinstance(ts, unicode):
            self._add_via_unicode(ts)

    def _add_via_unicode(self, s):
        assert isinstance(s, unicode)
        s = s.replace('\t', '').replace(' ', '').lower()
        assert TimeSlots.timeslots_regex.match(s)
        numbers = TimeSlots.numbers_regex.findall(s)
        timeslots = []
        for i in xrange(0, len(numbers), 4):
            if u'+' in numbers[i+2]:
                # datetime.time doesn't support __add__() so
                # we have to use datetime.datetime and
                # datetime.timedelta.
                t1 = datetime.datetime(1978, 6, 12, int(numbers[i]), int(numbers[i+1]))
                td = datetime.timedelta(hours=int(numbers[i+2]), minutes=int(numbers[i+3]))
                t2 = t1 + td
                t1 = t1.time()
                t2 = t2.time()
                if t1 < t2:
                    timeslots.append(TimeSlot(t1,t2))
                else:
                    timeslots.append(TimeSlot(t1,datetime.time(23, 59)))
                    timeslots.append(TimeSlot(datetime.time(0, 0), t2))
            else:
                t1 = datetime.time(int(numbers[i]), int(numbers[i+1]))
                t2 = datetime.time(int(numbers[i+2]), int(numbers[i+3]))
                timeslots.append(TimeSlot(t1,t2))
        for timeslot in timeslots:
            self.add(timeslot)

    def __contains__(self, time):
        for timeslot in self.timeslots:
            if time in timeslot:
                return True
        return False

    def __repr__(self):
        return str(self.timeslots)


class Logger:

    def __init__(self):
      self.tag = u'shinken/' + os.path.basename(sys.argv[0])

    def write(self, message):
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        subprocess.call(['logger', '-t', self.tag, message])


class Line:
    """Represents a line in the black list file."""

    comments_regex = re.compile('#.*$')

    def __init__(self, s):
        assert isinstance(s, unicode)
        # The line is cleaned: comments and useless blanks are removed.
        self.line = Line.comments_regex.sub('', s).strip()

    def get_rule(self):

        if len(self.line) == 0:
            return None

        if self.line.count(':') != 4:
            # The rule is not well written.
            logger = Logger()
            logger.write(u"The line `%s' is not valid in the blacklist file." % (self.line))
            del(logger)
            return None

        l = self.line.split(':')
        ts = TimeSlots()
        ts.add(l[3])
        weekdays = Weekdays(l[4])
        rule = Rule(
            contact_names = Regexp(l[0]),
            hostnames = Regexp(l[1]), timeslots=ts,
            weekdays=weekdays,
            service_desc=Regexp(l[2]),
        )
        return rule



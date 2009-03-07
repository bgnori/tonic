#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#
import os.path
import sys
import time
from datetime import datetime as dt
from datetime import timedelta as delta
import pickle
import smtplib

import urllib

from BeautifulSoup import BeautifulSoup as Parser
import tonic.mailingbot

'''
http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi?action=memo&yy=2009&mm=3&dd=8&id=1408
'''


'''<a href="javaScript:void(0)" onClick=newWin=window.open("/EventSchedule/calendar/calendar.cgi?action=memo&yy=2009&mm=3&dd=28&id=2863","newWin","width=560,height=300,scrollbars=yes,resizable=yes") class="typed">'''

'''<a href="javaScript:void(0)" onClick=newWin=window.open("/EventSchedule/calendar/calendar.cgi?action=memo&yy=2009&mm=3&dd=3&id=1357","newWin","width=560,height=300,scrollbars=yes,resizable=yes") class="typed">'''
'''"/EventSchedule/calendar/calendar.cgi?action=memo&yy=2009&mm=3&dd=3&id=1357"'''

import re
parseOnClick = re.compile((
  r'"/EventSchedule/calendar/calendar.cgi\?action=memo&'
  r'yy=(?P<year>\d{4})&'
  r'mm=(?P<month>\d{1,2})&'
  r'dd=(?P<day>\d{1,2})&'
  r'id=(?P<id>\d+)"'
  ))


class Bot(tonic.mailingbot.Bot):
  def run(self):
    pages = self.get(self.feed_url)

    self.write('connecting to mail server.\n')
    con = smtplib.SMTP(self.server)
    c = 0
    try:
      con.ehlo()
      con.starttls()
      con.ehlo()
      con.login(self.sender_addr, self.password)
      self.write('sending with %s to %s\n'
                  %(self.sender_addr, self.grp_addr))
      for uhtml in pages:
        msg = self.make_message(uhtml)
        con.sendmail(self.sender_addr, self.grp_addr, msg.as_string())
        c += 1
        self.write('.')
    finally:
      con.close()
    if c > 0:
      self.write('sent.\n')
    else:
      self.write('no item to work with.\n')
    self.write('done.\n')
    return 

  def mailsubject(self, uhtml):
    p = Parser()
    p.feed(uhtml)
    p.goahead(0)
    div = p.find('div', attrs={'class':'moji'})
    return str(div.contents[0]).decode('utf8')

  def mailbody(self, uhtml):
    p = Parser()
    p.feed(uhtml)
    p.goahead(0)
    td = p.find('td', attrs={'class':'moji'})
    return repr(td).decode('utf8')#ugh!
    #return td#.p.contents
    #return ''.join([str(c) for c in td.p.contents])

  def get(self, url):
    #ym=2009.3
    #vmode=itiran
    now = dt.now()
    tomorrow = now + delta(1)

    option = urllib.urlencode(dict(
          ym='%i.%i'%(now.year, now.month),
          vmode='itiran'
          ))
    #print option
    url += '?' + option
    self.write('getting feed from "%s".\n'%(url))

    p = Parser()
    f = urllib.urlopen(url)
    try:
      #f.read()
      p.feed(f.read().decode('Shift-JIS'))
      p.goahead(0)
    finally:
      f.close()

    pages = []
    for a in p.findAll('a', attrs=dict(href="javaScript:void(0)")):
      #print a['onclick']
      m = parseOnClick.search(a['onclick'])
      if m:
        d = m.groupdict()
        #print d['year'], d['month'], d['day'], d['id']
        memo = '''http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi'''
        if int(d['day']) == tomorrow.day:
          option = urllib.urlencode(dict(
              action='memo',
              yy=d['year'],
              mm=d['month'],
              dd=d['day'],
              id=d['id'],
              ))
          f = urllib.urlopen(memo + '?' + option)
          try:
            uhtml = f.read().decode('Shift-JIS')
          finally:
            f.close()
          pages.append(uhtml)
    return pages



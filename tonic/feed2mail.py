#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import sys
import time
from datetime import datetime as dt
import urllib
import feedparser
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate


class Bot(object):
  def __init__(self, feed_url, bot_addr, 
                     sender_addr, password, grp_addr,
                     out=None):
    if out is None:
      out = sys.stdout
    self.feed_url = feed_url
    self.bot_addr = bot_addr
    self.sender_addr = sender_addr
    self.password = password
    self.grp_addr = grp_addr
    self.out = out

  def run(self):
    self.get()
    tobepost = self.check()
    if not tobepost:
      print 'no new post found'
      return
    print len(tobepost), ' new posts found'
    tosend = self.make_messages(tobepost)
    print 'connecting to mail server.'
    self.mail(tosend)
    print 'sent'
    print 'done.'

  def get(self):
    print 'getting feed'
    f = urllib.urlopen(self.feed_url)
    try:
      self.feed  = feedparser.parse(f.read())
    finally:
      f.close()

  def check(self):
    tobepost = []
    now = dt.utcnow()
    for entry in x.entries:
      generated = dt(*entry.updated_parsed[:5])
      delta = generated - now
      if delta.days == 0 and delta.seconds < 3600:
        tobepost.append(entry)
    return tobepost

  def make_messages(self, tobepost):
    tosend = []
    for entry in tobepost:
      msg = MIMEText(entry.summary.encode('utf-8'), 'plain', 'utf-8')
      msg['Subject'] = entry.title.encode('utf-8')
      msg['From'] = self.bot_addr 
      msg['To'] = self.grp_addr 
      msg['Date'] = formatdate()
      tosend.append(msg)
    return tosend

  def mail(self, tosend):
    con = smtplib.SMTP('smtp.gmail.com')#, 587)
    try:
      con.ehlo()
      con.starttls()
      con.ehlo()
      con.login(self.sender_addr, self.password)
      print 'sending',
      for msg in tosend:
        print '.',
        con.sendmail(self.sender_addr, self.grp_addr, msg.as_string())
    finally:
      con.close()


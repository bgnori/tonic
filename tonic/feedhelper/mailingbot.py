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

import urllib
import feedparser
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header 
from email.Utils import formatdate


class Item(object):
  def mailbody(self):
    pass

  def mailsubject(self):
    pass

  def sendP(self):
    return True

  def get_timestamp(self):
    return dt.now()
    
  def mark_as_sent(self, t):
    assert isinstance(t, dt)

  def make_message(self, bot):
    msg = MIMEText(self.mailbody().encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = Header(self.mailsubject().encode('utf-8'), 'utf-8')
    msg['From'] = bot.bot_addr
    msg['To'] = bot.grp_addr
    msg['Date'] = formatdate()
    return msg


class Bot(object):
  def __init__(self, out=None, **kw):
  #feed_url, bot_addr, sender_addr, password, server, grp_addr,
    if out is None:
      out = sys.stdout
    self.out = out
    self.depot = kw

  def __getattr__(self, name):
    assert name in ("subject_prefix",
                    "feed_url", "bot_addr", 
                    "sender_addr", "password", 
                    "grp_addr", "server",
                    "last",), '%s is not in list'%name
    return self.__dict__['depot'][name]

  def write(self, s):
    self.out.write(s)
    
  def mail(self, container):
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
      for item in container:
        if item.sendP():
          msg = item.make_message(self)
          con.sendmail(self.sender_addr, self.grp_addr, msg.as_string())
          item.mark_as_sent(self.get_timestamp())
          c += 1
          self.write('.')
    finally:
      con.close()
    if c > 0:
      self.write('\nsent!\n')
    else:
      self.write('no item to work with.\n')

  def run(self, now=None):
    container = self.get(self.feed_url, now)
    self.mail(container)
    self.write('done.\n')
    return 


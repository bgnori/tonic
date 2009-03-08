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
import pickle

import urllib
import feedparser
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate


class Item(object):
  def mailbody(self):
    pass
  def mailsubject(self):
    pass
  def sendP(self):
    return True
  def mark_as_sent(self):
    self.bot_addr 
    pass

  def make_message(self, bot):
    msg = MIMEText(self.mailbody().encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = self.mailsubject().encode('utf-8')
    msg['From'] = bot.bot_addr
    msg['To'] = bot.grp_addr
    msg['Date'] = formatdate()
    return msg

class ContainerIF(object):
  def __iter__(self):
    raise StopIteration


class Bot(object):
  def __init__(self, out=None, **kw):
  #feed_url, bot_addr, sender_addr, password, server, grp_addr,
    if out is None:
      out = sys.stdout
    self.out = out
    self.depot = kw

  def __getattr__(self, name):
    assert name in ("feed_url", "bot_addr", 
                    "sender_addr", "password", 
                    "grp_addr", "server",
                    "last",), '%s is not in list'%name
    return self.__dict__['depot'][name]

  def write(self, s):
    self.out.write(s)

    
  def mail(self, container):
    assert isinstance(container, ContainerIF)

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
          item.mark_as_sent()
          c += 1
          self.write('.')
    finally:
      con.close()
    if c > 0:
      self.write('\nsent!\n')
    else:
      self.write('no item to work with.\n')

  def run(self):
    container = self.get(self.feed_url)
    self.mail(container)
    self.write('done.\n')
    return 


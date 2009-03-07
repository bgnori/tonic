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
                    "mailbody", "mailsubject",
                    "last",), '%s is not in list'%name
    return self.__dict__['depot'][name]

  def write(self, s):
    self.out.write(s)

  def run(self):
    feed = self.get(self.feed_url)

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
      for entry in reversed(feed.entries):
        generated = dt(*entry.updated_parsed[:5])
        if generated > self.lastupdate():
          msg = self.make_message(entry)
          con.sendmail(self.sender_addr, self.grp_addr, msg.as_string())
          self.update(generated)
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

  def get(self, url):
    self.write('getting feed from "%s".\n'%(url))
    f = urllib.urlopen(url)
    try:
      return feedparser.parse(f.read())
    finally:
      f.close()

  def lastupdate(self):
    path = os.path.abspath(self.last)
    if not os.path.exists(path):
      return dt(1900, 1, 1)
    else:
      f = file(path)
      try:
        t = pickle.load(f)
      finally:
        f.close()
      assert isinstance(t, dt)
      return t

  def update(self, t):
    assert isinstance(t, dt)
    path = os.path.abspath(self.last)
    f = file(path, 'w')
    try:
      pickle.dump(t, f)
    finally:
      f.close()
    
  def make_message(self, entry):
    msg = MIMEText(self.mailbody(entry).encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = self.mailsubject(entry).encode('utf-8')
    msg['From'] = self.bot_addr 
    msg['To'] = self.grp_addr 
    msg['Date'] = formatdate()
    return msg



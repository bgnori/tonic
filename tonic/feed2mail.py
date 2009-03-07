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
                     sender_addr, password, server, grp_addr,
                     out=None):
    if out is None:
      out = sys.stdout
    self.feed_url = feed_url
    self.bot_addr = bot_addr
    self.sender_addr = sender_addr
    self.password = password
    self.grp_addr = grp_addr
    self.server = server
    self.out = out

  def write(self, s):
    self.out.write(s)

  def run(self):
    feed = self.get(self.feed_url)
    tobepost = self.check(feed)
    if not tobepost:
      self.write('no new post found.\n')
      return
    self.write('%i new posts found.\n'%(len(tobepost)))

    messages = self.make_messages(tobepost)

    self.write('connecting to mail server.\n')
    self.mail(messages)
    self.write('sent.\n')
    self.write('done.\n')
    return 

  def get(self, url):
    self.write('getting feed from "%s".\n'%(url))
    f = urllib.urlopen(url)
    try:
      return feedparser.parse(f.read())
    finally:
      f.close()

  def check(self, feed):
    tobepost = []
    now = dt.utcnow()
    for entry in feed.entries:
      generated = dt(*entry.updated_parsed[:5])
      delta = generated - now
      #if delta.days == 0 and delta.seconds < 3600:
      tobepost.append(entry)
    return tobepost

  def make_messages(self, tobepost):
    messages = []
    for entry in tobepost:
      msg = MIMEText(entry.summary.encode('utf-8'), 'plain', 'utf-8')
      msg['Subject'] = entry.title.encode('utf-8')
      msg['From'] = self.bot_addr 
      msg['To'] = self.grp_addr 
      msg['Date'] = formatdate()
      messages.append(msg)
    return messages

  def mail(self, messages):
    con = smtplib.SMTP(self.server)
    try:
      con.ehlo()
      con.starttls()
      con.ehlo()
      con.login(self.sender_addr, self.password)
      self.write('sending with %s to %s\n'
                  %(self.sender_addr, self.grp_addr))
      for msg in messages:
        con.sendmail(self.sender_addr, self.grp_addr, msg.as_string())
        self.write('.')
    finally:
      con.close()


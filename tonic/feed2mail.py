#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#
from datetime import datetime as dt

import urllib
import feedparser
import smtplib

import tonic.mailingbot

class Bot(tonic.mailingbot.Bot):
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


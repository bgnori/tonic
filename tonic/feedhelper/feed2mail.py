#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import os.path
from datetime import datetime as dt
import urllib
import pickle
import feedparser
import smtplib

import tonic.feedhelper.mailingbot

class Item(tonic.feedhelper.mailingbot.Item):
  def __init__(self, bot, entry):
    self._imp = entry
    self._bot = bot

  def mailbody(self):
    return self._imp.summary

  def mailsubject(self):
    return u'jbl hokkaido news:' + self._imp.title

  def sendP(self):
    return dt(*self._imp.updated_parsed[:5]) > self.lastupdate()

  def mark_as_sent(self):
    t = dt(*self._imp.updated_parsed[:5])
    path = os.path.abspath(self._bot.last)
    f = file(path, 'w')
    try:
      pickle.dump(t, f)
    finally:
      f.close()

  def lastupdate(self):
    path = os.path.abspath(self._bot.last)
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
  

class Bot(tonic.feedhelper.mailingbot.Bot):
  def get(self, url, now=None):
    self.write('getting feed from "%s".\n'%(url))
    f = urllib.urlopen(url)
    try:
      feed = feedparser.parse(f.read())
      def xxx():
        for entry in reversed(feed.entries):
          yield Item(self, entry)
      return xxx()
    finally:
      f.close()


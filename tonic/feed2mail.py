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

class Item(tonic.mailingbot.Item):
  last='/home/nori/Desktop/work/tonic/bygit/jblhokkaido_last'
  def __init__(self, entry):
    self._imp = entry

  def mailbody(self):
    return self._imp.content[0].value

  def mailsubject(self):
    return u'jbl hokkaido news:' + self._imp.title

  def sendP(self):
    return dt(*entry.updated_parsed[:5]) > self.lastupdate()

  def mark_as_sent(self, bot):
    t = dt(*entry.updated_parsed[:5])
    path = os.path.abspath(bot.last)
    f = file(path, 'w')
    try:
      pickle.dump(t, f)
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
  

class FeedContainer(tonic.mailingbot.ContainerIF):
  def __init__(self, feed):
    self._feed = feed
  def __iter__(self):
    for entry in reversed(self._feed.entries):
      yield Item(entry)


class Bot(tonic.mailingbot.Bot):
  def get(self, url):
    self.write('getting feed from "%s".\n'%(url))
    f = urllib.urlopen(url)
    try:
      return FeedContainer(feedparser.parse(f.read()))
    finally:
      f.close()



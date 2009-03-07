#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import StringIO
import unittest
import os
from tonic.feed2mail import Bot

class BotTest(unittest.TestCase):
  def setUp(self):
    self.bot = Bot(
          feed_url='feed_url',
          bot_addr='bot_addr',
          sender_addr='sender_addr', 
          password='password', 
          grp_addr='grp_addr',
          server='server',
          storage=StringIO.StringIO(),
          mailbody = lambda x: x.content[0].value,
          mailsubject = lambda x: x.title,
          last='feed2mail_lastfile',
          )

  def tearDown(self):
    try:
      os.remove('feed2mail_lastfile')
    except:
      pass

  def test_get(self):
    print self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')

  def test_check(self):
    feed = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    new = self.bot.check(feed)
    print new
    self.assert_(len(new))

  def test_make_message(self):
    feed = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    news = self.bot.check(feed)
    msgs = self.bot.make_messages(news)
    for m in msgs:
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')

  def test_mail(self):
    pass
      


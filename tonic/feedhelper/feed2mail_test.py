#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

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
          last='feed2mail_lastfile',
          server='server',
          )

  def tearDown(self):
    try:
      os.remove('feed2mail_lastfile')
    except:
      pass

  def test_get(self):
    feed = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    print feed

  def test_make_message(self):
    container = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    for item in container:
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      


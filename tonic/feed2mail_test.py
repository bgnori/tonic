#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
from tonic.feed2mail import Bot

class BotTest(unittest.TestCase):
  def setUp(self):
    self.bot = Bot(
          'feed_url',
          'bot_addr',
          'sender_addr', 
          'password', 
          'grp_addr',
          'server',
          )

  def tearDown(self):
    pass

  def test_get(self):
    self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')

  def test_check(self):
    feed = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    new = self.bot.check(feed)
    self.assert_(len(new))

  def test_make_message(self):
    feed = self.bot.get('http://nori-on-baking.blogspot.com/feeds/posts/default')
    new = self.bot.check(feed)
    msgs = self.bot.make_messages(new)




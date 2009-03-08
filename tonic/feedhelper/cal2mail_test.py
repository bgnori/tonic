#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import StringIO
import unittest
import os
from tonic.cal2post import Bot

class BotTest(unittest.TestCase):
  def setUp(self):
    self.bot = Bot(
          feed_url='feed_url',
          bot_addr='bot_addr',
          sender_addr='sender_addr', 
          password='password', 
          grp_addr='grp_addr',
          last='cal2post_lastfile',
          server='server',
          )

  def tearDown(self):
    try:
      os.remove('cal2post_lastfile')
    except:
      pass

  def test_get(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi')
    print container

  def test_make_message(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi')

    for item in container:
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      


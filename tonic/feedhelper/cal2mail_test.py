#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import StringIO
import unittest
import os
from datetime import datetime as dt
from tonic.feedhelper.cal2mail import *

class BotTest(unittest.TestCase):
  def setUp(self):
    self.bot = Bot(
          subject_prefix='subject_prefix',
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
  def assertNoTag(self, got):
    self.assert_('<td' not in got)
    self.assert_('</td>' not in got)
    self.assert_('<p' not in got)
    self.assert_('</p>' not in got)
    self.assert_('<br' not in got)
    self.assert_('<a' not in got)
    self.assert_('</a>' not in got)
    self.assert_('</h' not in got)
    self.assert_('<h' not in got)
    self.assert_('<img' not in got)
    self.assert_('<span' not in got)
    self.assert_('</span>' not in got)
    self.assert_('&rsaquo;' not in got)
    self.assert_('&lsaquo;' not in got)
    self.assert_('& amp;' not in got)

  def tagStrip_1_test(self):
    dat = u'''<td valign="top" class="moji" bgcolor="#FFFFFF"><p>日本のトッププレイヤーが数多く参加するバックギャモンの例会です。しかし、あまり恐れずにどうぞお気軽にお越し下さい。初心者の方も大歓迎です。なお、チャレンジカップ(月に1度程度)開催時はお休みですのでご注意下さい。<br /><br />(アドミラルトーナメント開催中)<br />15時から希望者でアドミラルトーナメントを開催しています。(参加費別途1500円・但し15時までの最多勝ち越し者はフリーエントリー)<br />7pマッチ、優勝すると賞金+ポイントがもらえます。ポイントレース(半年間)の優勝者にはアドミラル産業から豪華賞品が贈られます。現在の状況は<a href="http://www.backgammon.gr.jp/forum/viewtopic.php?t=437" target="_blank">http://www.backgammon.gr.jp/forum/viewtopic.php?t=437</a> でご確認下さい。</p><p><h4 style="margin-bottom:0;">場所：</h4>赤坂囲碁ラウンジ<br />><a href="http:/maps.google.com/maps?f=q&hl;=ja&q;=%E6%9D%B1%E4%BA%AC%E9%83%BD%E6%B8%AF%E5%8C%BA%E8%B5%A4%E5%9D%823-10-5%28%E8%B5%A4%E5%9D%82%E5%9B%B2%E7%A2%81%E3%83%A9%E3%82%A6%E3%83%B3%E3%82%B8)" target="_blank">東京都港区赤坂3-10-5 クイーンビル4F</p><p><h4 style="margin-bottom:0;">時間：</h4>12:00<span>&rsaquo;& amp;rsaquo;&rsaquo;</span>19:00</p><p><h4 style="margin-bottom:0;">参加費：</h4>1日2,000円<br />学生、17時から1,000円<br />初めての方無料<br />アドミラルトーナメント(参加者のみ)1500円</p><p><h4 style="margin-bottom:0;">方式：</h4>5pマッチのレーティング戦.、アドミラルトーナメント(7p マッチ)</p><p><h4 style="margin-bottom:0;">連絡先：</h4>望月 正行<br />>070-5577-5016<br><a href="mailto:mo...@backgammon.gr.jp">mo...@backgammon.gr.jp</a></p>
   </td> '''
    got = tagStrip.sub(replproc, dat)
    self.assertNoTag(got)

  def tagStrip_2_test(self):
    dat = ''
    got = tagStrip.sub(replproc, dat)
    self.assertNoTag(got)


  def test_get(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi')
    print container

  def test_make_message_2009_3_6(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi', now=dt(2009, 3, 6))

    for item in container:
      print item.mailbody().encode('utf8')
      self.assertNoTag(item.mailbody())
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      self.assert_(str(m['Subject']).startswith('=?utf-8'))

  def test_make_message_2009_3_17(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi', now=dt(2009, 3, 17))

    for item in container:
      print item.mailbody().encode('utf8')
      self.assertNoTag(item.mailbody())
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      self.assert_(str(m['Subject']).startswith('=?utf-8'))

  def test_make_message_2009_3_25(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi', now=dt(2009, 3, 25))

    for item in container:
      print item.mailbody().encode('utf8')
      self.assertNoTag(item.mailbody())
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      self.assert_(str(m['Subject']).startswith('=?utf-8'))

  def test_make_message_2009_3_27(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi', now=dt(2009, 3, 27))

    for item in container:
      print item.mailbody().encode('utf8')
      self.assertNoTag(item.mailbody())
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      self.assert_(str(m['Subject']).startswith('=?utf-8'))

  def test_make_message_2009_3_20(self):
    container = self.bot.get('http://www.backgammon.gr.jp/EventSchedule/calendar/calendar.cgi', now=dt(2009, 3, 20))

    for item in container:
      print item.mailbody().encode('utf8')
      self.assertNoTag(item.mailbody())
      m = item.make_message(self.bot)
      print '='*60
      print m
      print '='*60
      self.assertEqual(m['From'], 'bot_addr')
      self.assertEqual(m['To'], 'grp_addr')
      self.assertEqual(m['Content-Type'], 'text/plain; charset="utf-8"')
      self.assert_(str(m['Subject']).startswith('=?utf-8'))
      


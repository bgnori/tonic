#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest

from tonic.funny import LooseQuacker as ChangeMock
from tonic.funny import LooseQuacker as UserMock
from turbogears.view import load_engines

from tonic.tg.widgets import HistoryListWithDiffSelection
class WidgetTest(unittest.TestCase):
  def setUp(self):
    load_engines()

  def tearDown(self):
    pass

  def test_ok(self):
    editor = UserMock(
                 display_name='nori',
                 )
    history=[
              ChangeMock(id=1,
                         last_modified='1001 10 10',
                         editor=editor,
                         after='after',
                         before='before',
                         wikiname='FrontPage',
                         ),
              ChangeMock(id=2,
                         last_modified='1111 11 11',
                         editor=editor,
                         after='after2',
                         before='before2',
                         wikiname='FrontPage',
                        ),
              ]
    hw = HistoryListWithDiffSelection(history=history)
    ret = hw.render()

    self.assert_('Left' in ret)
    self.assert_('Right' in ret)
    self.assert_('''<form class="HistoryListWithDiffSelection" method="post">''' in ret)
    self.assert_(
        '''<input type="submit" value="show diff">'''
        in ret)

  def test_empty_history(self):
    editor = UserMock(
                 display_name='nori',
                 )
    history=[]
    hw = HistoryListWithDiffSelection(history=history)
    ret = hw.render()
    self.assert_('Left' in ret)
    self.assert_('Right' in ret)
    self.assert_('''<form class="HistoryListWithDiffSelection" method="post">''' in ret)
    self.assert_(
        '''<input type="submit" value="show diff">'''
        in ret)


#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import unittest
import re
import sys

import elementtree.ElementTree as ET

from tonic.cache import hub
from tonic.cache.imp import Dict 
from tonic.visitbus import Requests
from tonic.visitbus import merge
from tonic.visitbus import compile

hub.connect(Dict())

class XPathTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_absroot(self):
    query = '''/root'''
    m = compile(query)
    self.assert_(m)
    self.assertEqual(m.pattern, r'^/root')
    self.assert_(m.match('/root'))


  def test_descendant(self):
    query = '''//node'''
    m = compile(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root'''))
    self.assert_(m.match('''/root/node'''))
    self.assert_(m.match('''/root/parent/node'''))
    self.assert_(m.match('''/root/grandparent/parent/node'''))

  def test_descendant_with_parent(self):
    query = '''//parent/node'''
    m = compile(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node'''))
    self.assert_(m.match('''/root/parent/node'''))
    self.assert_(m.match('''/root/grandparent/parent/node'''))

  def test_descendant_with_ancester(self):
    query = '''//ancester//node'''
    m = compile(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node'''))
    self.assert_(m.match('''/root/ancester/node'''))
    self.assert_(m.match('''/root/ancester/parent/node'''))


class RequestTest(unittest.TestCase):
  def setUp(self):
    self.r = Requests()
    self.tokyo = re.compile('.*tokyo$')
    self.osaka = re.compile('^osaka')
  def tearDown(self):
    pass

  def test_re(self):
    self.assert_(self.tokyo.match('tokyo'))
    self.assert_(self.osaka.match('osaka'))
    self.assert_(self.osaka.match('osakatokyo'))
    self.assert_(self.tokyo.match('osakatokyo'))

  def test_append(self):
    self.r.append(self.tokyo, 'mochy')
    self.assert_(self.tokyo in self.r)
    self.assert_(self.osaka not in self.r)
    self.r.append(self.tokyo, 'kenji')
    self.assert_(self.tokyo in self.r)
    self.r.append(self.osaka, 'michy')
    self.assert_(self.osaka in self.r)
    self.assert_('mochy' in self.r[self.tokyo])
    self.assert_('mochy' not in self.r[self.osaka])
    self.assert_('michy' in self.r[self.osaka])
    self.assert_('michy' not in self.r[self.tokyo])
    self.r.pop(self.tokyo)
    self.assert_(self.tokyo not in self.r)


  def test_match(self):
    self.r.append(self.tokyo, 'mochy')
    self.r.append(self.tokyo, 'kenji')
    self.r.append(self.osaka, 'michy')
    self.assertEqual(list(self.r.match('tokyo')), 
                        [self.tokyo])
    self.assertEqual(list(self.r.match('osaka')),
                        [self.osaka])
    self.assert_(self.tokyo in self.r.match('osakatokyo'))
    self.assert_(self.osaka in self.r.match('osakatokyo'))

  def test_merge(self):
    r = Requests()
    s = Requests()
    tokyo = re.compile('tokyo')
    r.append(self.tokyo, 'kenji')
    s.append(self.tokyo, 'mochy')

    t = merge(s, r)
    self.assert_('mochy' in t[self.tokyo])
    self.assert_('kenji' in t[self.tokyo])


class VisitBusTest(unittest.TestCase):
  def setUp(self):

    ET.Element('japan')
    self.r = Requests()
    self.tokyo = re.compile('.*tokyo$')
    self.osaka = re.compile('^osaka')
  def tearDown(self):
    pass



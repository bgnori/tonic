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
from tonic.visitbus import VisitPassenger
from tonic.visitbus import VisitBus

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


class VisitPassengerTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
  def testNull(self):
    class NullPassenger(VisitPassenger):
      def itinerary(self):
        raise StopIteration
    p = NullPassenger()
    try:
      p.next()
      self.assert_(False)
    except StopIteration:
      pass

  def testOnce(self):
    class OncePassenger(VisitPassenger):
      def itinerary(self):
        yield '/node'
        raise StopIteration

    p = OncePassenger()
    try:
      path = p.next()
    except StopIteration:
      self.assert_(False)
    self.assertEqual(path.pattern, '^/node')

    try:
      path = p.next()
      self.assert_(False)
    except StopIteration:
      pass


class VisitBusTest(unittest.TestCase):
  def setUp(self):
    world = ET.Element('world')
    japan = ET.SubElement(world, 'japan')
    tokyo = ET.SubElement(world, 'tokyo')
    osaka = ET.SubElement(world, 'osaka')
    self.tree = ET.ElementTree(world)
  def tearDown(self):
    pass

  def test_tokyo(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False

      def itinerary(self):
        yield '//tokyo'
        self.tokyo = True
        raise StopIteration
    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)

  def test_visitTwo(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False
        self.osaka = False

      def itinerary(self):
        yield '//tokyo'
        self.tokyo = True
        yield '//osaka'
        self.osaka = True
        raise StopIteration

    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    self.assert_(not p.osaka)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)
    self.assert_(p.osaka)



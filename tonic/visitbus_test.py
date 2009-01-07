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
from tonic.visitbus import vpath2regexp
from tonic.visitbus import VisitPassenger
from tonic.visitbus import VisitBus

hub.connect(Dict())

class VPathTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_absroot(self):
    query = '''/root'''
    m = vpath2regexp(query)
    self.assert_(m)
    self.assert_(m.match('/root>'))

  def test_absrootdown(self):
    query = '''/root>'''
    m = vpath2regexp(query)
    self.assert_(m)
    self.assert_(m.match('/root>'))

  def test_absrootup(self):
    query = '''/root<'''
    m = vpath2regexp(query)
    self.assert_(m)
    self.assert_(m.match('/root<'))

  def test_descendant(self):
    query = '''//node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root>'''))
    self.assert_(m.match('''/root/node>'''))
    self.assert_(not m.match('''/root/node<'''))
    self.assert_(m.match('''/root/parent/node>'''))
    self.assert_(not m.match('''/root/parent/node<'''))
    self.assert_(m.match('''/root/grandparent/parent/node>'''))

  def test_descendant_with_parent(self):
    query = '''//parent/node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/root/parent/node>'''))
    self.assert_(not m.match('''/root/parent/node<'''))
    self.assert_(m.match('''/root/grandparent/parent/node>'''))
    self.assert_(not m.match('''/root/grandparent/parent/node<'''))

  def test_descendant_with_ancester(self):
    query = '''//ancester//node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/root/ancester/node>'''))
    self.assert_(not m.match('''/root/ancester/node<'''))
    self.assert_(m.match('''/root/ancester/parent/node>'''))
    self.assert_(not m.match('''/root/ancester/parent/node<'''))

  def test_Or(self):
    query = '''//A|B'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/root/A>'''))
    self.assert_(m.match('''/root/B>'''))

  def test_Or3(self):
    query = '''//A|B|C'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/root/A>'''))
    self.assert_(m.match('''/root/B>'''))
    self.assert_(m.match('''/root/C>'''))

  def test_OrParent(self):
    query = '''//A|B/node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/root/A/node>'''))
    self.assert_(m.match('''/root/B/node>'''))

  def test_OrAncester(self):
    query = '''//A|B//node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/root/node>'''))
    self.assert_(m.match('''/A/node>'''))
    self.assert_(m.match('''/root/A/node>'''))
    self.assert_(m.match('''/root/B/node>'''))
    self.assert_(not m.match('''/root/C/node>'''))
    self.assert_(m.match('''/A/hoge/node>'''))
    self.assert_(m.match('''/root/A/hoge/node>'''))
    self.assert_(m.match('''/root/B/hoge/node>'''))
    self.assert_(m.match('''/root/B/hoge/bar/node>'''))
    self.assert_(not m.match('''/root/C/hoge/node>'''))

  def test_Any(self):
    query = '''/*'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(m.match('''/A>'''))
    self.assert_(m.match('''/B>'''))
    self.assert_(m.match('''/C>'''))

  def test_AnyInParent(self):
    query = '''/*/node'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(m.match('''/A/node>'''))
    self.assert_(m.match('''/B/node>'''))
    self.assert_(m.match('''/C/node>'''))

  def test_TwoAnys(self):
    query = '''/*/*'''
    m = vpath2regexp(query)
    self.assert_(m)
    print m, m.pattern
    self.assert_(not m.match('''/A'''))
    self.assert_(m.match('''/A/a>'''))
    self.assert_(m.match('''/B/b>'''))
    self.assert_(m.match('''/C/c>'''))
    self.assert_(not m.match('''/C/c/D>'''))


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
    self.r._append(self.tokyo, 'mochy')
    self.assert_(self.tokyo in self.r)
    self.assert_(self.osaka not in self.r)
    self.r._append(self.tokyo, 'kenji')
    self.assert_(self.tokyo in self.r)
    self.r._append(self.osaka, 'michy')
    self.assert_(self.osaka in self.r)
    self.assert_('mochy' in self.r[self.tokyo])
    self.assert_('mochy' not in self.r[self.osaka])
    self.assert_('michy' in self.r[self.osaka])
    self.assert_('michy' not in self.r[self.tokyo])
    self.r.pop(self.tokyo)
    self.assert_(self.tokyo not in self.r)


  def test_match(self):
    self.r._append(self.tokyo, 'mochy')
    self.r._append(self.tokyo, 'kenji')
    self.r._append(self.osaka, 'michy')
    print zip(self.r.match('tokyo'))[0]
    self.assert_(self.tokyo
                    in zip(self.r.match('tokyo'))[0][0])
    self.assert_(self.osaka
                    in zip(self.r.match('osaka'))[0][0])
    self.assert_(self.tokyo 
                    in zip(self.r.match('osakatokyo'))[0][0])
    self.assert_(self.osaka 
                    in zip(self.r.match('osakatokyo'))[1][0])

  def test_merge(self):
    r = Requests()
    s = Requests()
    tokyo = re.compile('tokyo')
    r._append(self.tokyo, 'kenji')
    s._append(self.tokyo, 'mochy')

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
        yield vpath2regexp('/node')
        raise StopIteration

    p = OncePassenger()
    try:
      path = p.next()
    except StopIteration:
      self.assert_(False)
    self.assertEqual(path.pattern, '^/(node)>$')

    try:
      path = p.next()
      self.assert_(False)
    except StopIteration:
      pass


class VisitBusTest(unittest.TestCase):
  def setUp(self):
    world = ET.Element('world')
    japan = ET.SubElement(world, 'japan')
    tokyo = ET.SubElement(japan, 'tokyo')
    osaka = ET.SubElement(japan, 'osaka')
    self.tree = ET.ElementTree(world)
  def tearDown(self):
    pass

  def test_tokyo(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False

      def itinerary(self):
        yield vpath2regexp('//tokyo')
        self.tokyo = True
        raise StopIteration
    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)
    self.assertEqual(p.visitbus, bus)

  def test_tokyoup(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False

      def itinerary(self):
        yield vpath2regexp('//tokyo<')
        self.tokyo = True
        raise StopIteration
    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)

  def test_tokyodu(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.down = False
        self.up= False

      def itinerary(self):
        yield vpath2regexp('//tokyo>')
        self.down = True
        yield vpath2regexp('//tokyo<')
        self.up= True
        raise StopIteration
    p = TokyoPassenger()
    self.assert_(not p.down)
    self.assert_(not p.up)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.down)
    self.assert_(p.up)

  def test_japandu(self):
    class JapanPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.down = False
        self.up= False
        self.tokyo = False
        self.osaka = False

      def itinerary(self):
        yield vpath2regexp('//japan>')
        self.down = True
        yield vpath2regexp('//tokyo')
        self.tokyo = True
        yield vpath2regexp('//osaka')
        self.osaka = True
        yield vpath2regexp('//japan<')
        self.up = True
        raise StopIteration
    p = JapanPassenger()
    self.assert_(not p.down)
    self.assert_(not p.up)
    self.assert_(not p.tokyo)
    self.assert_(not p.osaka)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.down)
    self.assert_(p.tokyo)
    self.assert_(p.osaka)
    self.assert_(p.up)

  def test_visitTwoCity(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False
        self.osaka = False

      def itinerary(self):
        yield vpath2regexp('//tokyo')
        self.tokyo = True
        yield vpath2regexp('//osaka')
        self.osaka = True
        raise StopIteration

    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    self.assert_(not p.osaka)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)
    self.assert_(p.osaka)

  def test_ManyPassengers(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False
      def itinerary(self):
        yield vpath2regexp('//tokyo')
        self.tokyo = True
        raise StopIteration
    class OsakaPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.osaka = False
      def itinerary(self):
        yield vpath2regexp('//osaka')
        self.osaka = True
        raise StopIteration
    tokyo1 = TokyoPassenger()
    tokyo2 = TokyoPassenger()
    osaka = OsakaPassenger()

    self.assert_(not tokyo1.tokyo)
    self.assert_(not tokyo2.tokyo)
    self.assert_(not osaka.osaka)
    bus = VisitBus((tokyo1, tokyo2, osaka))
    bus.visit(self.tree.getroot())
    self.assert_(tokyo1.tokyo)
    self.assert_(tokyo2.tokyo)
    self.assert_(osaka.osaka)

  def test_visitRegexp(self):
    class TokyoPassenger(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False
        self.osaka = False

      def itinerary(self):
        yield re.compile('^.*tokyo')
        self.tokyo = True
        yield re.compile('^.*osaka')
        self.osaka = True
        raise StopIteration

    p = TokyoPassenger()
    self.assert_(not p.tokyo)
    self.assert_(not p.osaka)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)
    self.assert_(p.osaka)

  def test_spawn(self):
    class Child(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.osaka= False

      def itinerary(self):
        yield vpath2regexp('//osaka')
        self.osaka= True
        raise StopIteration

    c = Child()
    class Parent(VisitPassenger):
      def __init__(self):
        VisitPassenger.__init__(self)
        self.tokyo = False
      def spawn(self):
        return [c]
      def itinerary(self):
        yield re.compile('^.*tokyo')
        self.tokyo = True
        raise StopIteration

    p = Parent()
    self.assert_(not p.tokyo)
    self.assert_(not c.osaka)
    bus = VisitBus((p,))
    bus.visit(self.tree.getroot())
    self.assert_(p.tokyo)
    self.assert_(c.osaka)




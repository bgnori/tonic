#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
from tonic.networksim import *
from tonic.networksim.primitive import PortNumber


class UtilTest(unittest.TestCase):
  def test_itom_0(self):
    self.assertEqual(itom(0), '\x00\x00\x00\x00')
  def test_itom_1(self):
    self.assertEqual(itom(1), '\x80\x00\x00\x00')
  def test_itom_16(self):
    self.assertEqual(itom(16), '\xff\xff\x00\x00')
  def test_itom_32(self):
    self.assertEqual(itom(32), '\xff\xff\xff\xff')

  def test_mtoi_0(self):
    self.assertEqual(mtoi('\x00\x00\x00\x00'), 0)
  def test_mtoi_x80x00x00x00(self):
    self.assertEqual(mtoi('\x80\x00\x00\x00'), 1)
  def test_mtoi_xffxffx00x00(self):
    self.assertEqual(mtoi('\xff\xff\x00\x00'), 16)
  def test_mtoi_xffxffxffxff(self):
    self.assertEqual(mtoi('\xff\xff\xff\xff'), 32)


class PrimitiveTest(unittest.TestCase):
  def test_IPv4Addr_immutalbeness(self):
    hash(IPv4Addr('192.168.0.1'))
    
  def test_ip_singular(self):
    one = IPv4Addr('192.168.0.1')
    two = IPv4Addr('192.168.0.1')
    self.assertEqual(id(one), id(two))
    
  def test_IPvMask_str_immutalbeness(self):
    hash(IPv4Mask('255.255.0.0'))
  def test_IPvMask_int_immutalbeness(self):
    hash(IPv4Mask(16))

  def test_PortNumber_validrange(self):
    try:
      PortNumber('0')
      self.assert_(False)
    except TypeError:
      pass
    try:
      PortNumber(-1)
      self.assert_(False)
    except ValueError:
      pass
    for i in range(0, 65535+1):
      PortNumber(i)
    try:
      PortNumber(65536)
      self.assert_(False)
    except ValueError:
      pass

  def test_PortNumber_immutableness(self):
    hash(PortNumber(0))

  def test_UDPPort_immutableness(self):
    hash(UDPPort(0))

  def test_TCPPort_immutableness(self):
    hash(TCPPort(0))

  def test_request(self):
    r = Request(IPv4Addr('192.168.0.2'), IPv4Addr('192.168.0.1'))

  def test_nwif(self):
    m = Machine()
    nwif = m.make_interface(IPv4Addr('192.168.0.1'), IPv4Mask(24))

  def test_nwif_receive_accept(self):
    m = Machine()
    nwif = m.make_interface(IPv4Addr('192.168.0.1'), IPv4Mask(24))
    r = Request(IPv4Addr('192.168.0.2'), IPv4Addr('192.168.0.1'))
    self.assert_(nwif.receive(r))

  def test_nwif_receive_ignore(self):
    m = Machine()
    nwif = m.make_interface(IPv4Addr('192.168.0.1'), IPv4Mask(24))
    r = Request(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.2'))
    self.assert_(not nwif.receive(r))

  def test_router(self):
    r = Router()
    

class SimpleSegmentTest(unittest.TestCase):
  def setUp(self):
    m1 = Machine()
    m2 = Machine()
    self.nw = Segment()
    self.nw.connect(m1.make_interface(IPv4Addr('192.168.0.1'), IPv4Mask(24)))
    self.nw.connect(m2.make_interface(IPv4Addr('192.168.0.2'), IPv4Mask(24)))

  def test_send(self):
    r = Request(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.2'))
    self.nw.receive(r)

  def test_send_no_receiver(self):
    r = Request(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.3'))
    try:
      self.nw.receive(r)
      self.assert_(False)
    except DestinationNotFound:
      pass


class TwoSegmentTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network(
                seg0=Segment(),
                seg1=Segment(),
                )
    m0 = Machine()
    m1 = Machine()
    r = Router()
    self.nw.seg0.connect(
      r.make_interface(IPv4Addr('192.168.0.1'), IPv4Mask(24)))
    self.nw.seg0.connect(
      m0.make_interface(IPv4Addr('192.168.0.2'), IPv4Mask(24)))
    self.nw.seg1.connect(
      r.make_interface(IPv4Addr('192.168.1.1'), IPv4Mask(24)))
    self.nw.seg1.connect(
      m1.make_interface(IPv4Addr('192.168.1.2'), IPv4Mask(24)))

  def test_send(self):
    r = Request(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.1.2'))
    self.nw.seg0.receive(r)

  def test_send_no_receiver(self):
    r = Request(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.2.3'))
    try:
      self.nw.seg0.receive(r)
      self.assert_(False)
    except DestinationNotFound:
      pass


class SegmentWithUplinkTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network(
                seg=Segment(),
                up=Uplink(),
                )
    m = Machine()
    r = Router()
    s = inetServer()
    self.nw.seg.connect(r.make_interface(IPv4Addr('192.168.0.1')))
    self.nw.seg.connect(m.make_interface(IPv4Addr('192.168.0.2')))
    self.nw.up.connect(r.make_interface(IPv4Addr('0.0.1.1')))
    self.nw.up.connect(m1.make_interface(IPv4Addr('0.0.1.2')))



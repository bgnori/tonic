#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
from tonic.networksim import *
from tonic.networksim.primitive import PortNumber, QuadByte

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
  def test_quadbyte_str(self):
    qb = QuadByte('\x00\x00\x00\x00')
    self.assertEqual(str(qb), '0.0.0.0')

  def test_quadbyte_repr(self):
    qb = QuadByte('\x00\x00\x00\x00')
    self.assertEqual(repr(qb), '<QuadByte "\x00\x00\x00\x00">')

  def test_quadbyte_immutableness(self):
    hash(QuadByte('\x00\x00\x00\x00'))

  def test_quadbyte_eq(self):
    a = QuadByte('\x00\x00\x00\x00')
    b = QuadByte('\x00\x00\x00\x00')
    self.assert_(a == b)

  def test_quadbyte_not_eq(self):
    a = QuadByte('\x00\x00\x00\x00')
    b = QuadByte('\xf0\x00\x00\x00')
    self.assert_(a != b)

  def test_quadbyte_and(self):
    a = QuadByte('\xff\x00\x00\x00')
    b = QuadByte('\xf0\xf0\x00\x00')
    self.assertEqual(a & b, QuadByte('\xf0\x00\x00\x00'))

  def test_quadbyte_or(self):
    a = QuadByte('\xff\x00\x00\x00')
    b = QuadByte('\xf0\xf0\x00\x00')
    self.assertEqual(a | b, QuadByte('\xff\xf0\x00\x00'))

  def test_quadbyte_or(self):
    a = QuadByte('\xff\x00\x00\x00')
    b = QuadByte('\xf0\xf0\x00\x00')
    self.assertEqual(a ^ b, QuadByte('\x0f\xf0\x00\x00'))

  def test_IPv4Addr_immutableness(self):
    hash(IPv4Addr('192.168.0.1'))
    
  def test_ip_singular(self):
    one = IPv4Addr('192.168.0.1')
    two = IPv4Addr('192.168.0.1')
    self.assertEqual(id(one), id(two))
    
  def test_IPvMask_str_immutableness(self):
    hash(IPv4Mask('255.255.0.0'))
  def test_IPvMask_int_immutableness(self):
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

  def test_packet(self):
    p = Packet(IPv4Addr('192.168.0.2'), IPv4Addr('192.168.0.1'))


class NetworkManagedObjectTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network()
    self.seg = self.nw.make_segment(IPv4Addr('192.168.0.0'), IPv4Mask(24))

  def test_nwif(self):
    m = Machine()
    nwif = self.nw.make_interface(
        self.seg, m,
        IPv4Addr('192.168.0.1'), IPv4Mask(24))

  def test_nwif_receive_accept(self):
    m = Machine()
    nwif = self.nw.make_interface(
        self.seg, m,
        IPv4Addr('192.168.0.1'), IPv4Mask(24))
    p = Packet(IPv4Addr('192.168.0.2'), IPv4Addr('192.168.0.1'))
    nwif.receive(p)
    self.nw.tick()

  def test_nwif_receive_ignore(self):
    m = Machine()
    nwif = self.nw.make_interface(
        self.seg, m,
        IPv4Addr('192.168.0.1'), IPv4Mask(24))
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.2'))
    nwif.receive(p)
    self.nw.tick()

  def test_router(self):
    r = Router()
    

class SimpleSegmentTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network()
    self.m1 = Machine()
    self.m2 = Machine()
    self.seg = self.nw.make_segment(IPv4Addr('192.168.0.0'), IPv4Mask(24))
    self.nw.make_interface(self.seg, self.m1,
              IPv4Addr('192.168.0.1'), IPv4Mask(24))
    self.nw.make_interface(self.seg, self.m2,
              IPv4Addr('192.168.0.2'), IPv4Mask(24))

  def test_in(self):
    self.assert_(IPv4Addr('192.168.0.1') in self.seg)

  def test_not_in(self):
    self.assert_(IPv4Addr('192.192.0.1') not in self.seg)

  def test_send(self):
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.2'))
    self.m1.nis[0].send(p)
    self.assert_(self.seg.packets)
    self.nw.tick()
    self.assert_(not self.seg.packets)
    self.assert_(self.m2.nis[0].packets)

  def test_send_no_receiver(self):
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.3'))
    self.seg.receive(p)
    self.assert_(self.seg.packets)
    self.nw.tick()
    self.assert_(not self.seg.packets)
    self.assert_(not self.m2.nis[0].packets)
    self.assert_(not self.m1.nis[0].packets)


class TwoSegmentTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network()
    self.seg0 = self.nw.make_segment(IPv4Addr('192.168.0.0'), IPv4Mask(24))
    self.seg1 = self.nw.make_segment(IPv4Addr('192.168.1.0'), IPv4Mask(24))

    self.m0 = Machine()
    self.m1 = Machine()
    self.r = Router()
    self.nw.make_interface(
        self.seg0, self.r,
        IPv4Addr('192.168.0.1'), IPv4Mask(24))
    self.nw.make_interface(
        self.seg0, self.m0,
        IPv4Addr('192.168.0.2'), IPv4Mask(24))

    self.nw.make_interface(
        self.seg1, self.r,
        IPv4Addr('192.168.1.1'), IPv4Mask(24))
    self.nw.make_interface(
        self.seg1, self.m1,
        IPv4Addr('192.168.1.1'), IPv4Mask(24))

  def test_send_within_segment(self):
    p = Packet(IPv4Addr('192.168.0.2'), IPv4Addr('192.168.0.1'))
    self.m0.nis[0].send(p)

  def test_send_send_to_router(self):
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.0.2'))
    self.m0.nis[0].send(p)

  def test_send_over_router(self):
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.1.2'))
    self.m0.nis[0].send(p)

  def test_send_no_receiver(self):
    p = Packet(IPv4Addr('192.168.0.1'), IPv4Addr('192.168.2.3'))
    self.m0.nis[0].send(p)
    #self.nw.seg0.send(p)
    #self.assert_(False)


class SegmentWithUplinkTest(unittest.TestCase):
  def setUp(self):
    self.nw = Network(
                seg=Segment(IPv4Addr('192.168.0.0'), IPv4Mask(24)),
                up=Uplink(),
                )
    m = Machine()
    r = Router()
    s = inetServer()
    self.nw.seg.connect(r.make_interface(IPv4Addr('192.168.0.1')))
    self.nw.seg.connect(m.make_interface(IPv4Addr('192.168.0.2')))
    self.nw.up.connect(r.make_interface(IPv4Addr('0.0.1.1')))
    self.nw.up.connect(m1.make_interface(IPv4Addr('0.0.1.2')))



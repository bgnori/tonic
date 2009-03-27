#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

__all__ = ['itom', 'mtoi',
           'IPv4Addr', 'IPv4Mask', 
           'TCPPort', 'UDPPort',
           'Packet', 'NetworkInterface', 'Machine', 'Router',
           'DestinationUnreachable',
           'DestinationNotFound',
           'Segment', 'Network']


import socket
import struct


ALL32BIT =  (1 << 32) -1
def itom(i):
  assert isinstance(i, int)
  assert i >= 0
  assert i < 33
  return struct.pack('<I', socket.htonl(ALL32BIT & ALL32BIT << (32 - i)))

def mtoi(m):
  i = 0
  bits = socket.ntohl(struct.unpack('<I', m)[0])
  while bits & ALL32BIT:
    bits = bits << 1
    i += 1
  return i


class QuadByte(str):
  def __new__(cls, v):
    assert isinstance(v, str)
    assert len(v) == 4
    self = str.__new__(QuadByte, v)
    return self

  def __str__(self):
    return socket.inet_ntop(socket.AF_INET, self)

  def __repr__(self):
    return '<QuadByte "%s">'%super(QuadByte, self).__str__()

  def _bitop(self, other, op):
    s = socket.ntohl(struct.unpack('<I', self)[0])
    o = socket.ntohl(struct.unpack('<I', other)[0])
    return QuadByte(struct.pack('<I', socket.htonl(op(s, o))))

  def __and__(self, other):
    return self._bitop(other, int.__and__)
  def __or__(self, other):
    return self._bitop(other, int.__or__)
  def __xor__(self, other):
    return self._bitop(other, int.__xor__)


class IPv4Addr(QuadByte):
  'immutable'
  _bag = {}
  def __new__(cls, presentation):
    if presentation not in cls._bag:
      self = QuadByte.__new__(cls, socket.inet_pton(socket.AF_INET, presentation))
      cls._bag.update({presentation:self})
    return cls._bag[presentation]


class IPv4Mask(QuadByte):
  'immutable'
  def __new__(cls, mask):
    if isinstance(mask, int):
      self = QuadByte.__new__(cls, itom(mask))
    elif isinstance(mask, str):
      self = QuadByte.__new__(cls, socket.inet_pton(socket.AF_INET, mask))
    else:
      raise TypeError
    return self


class PortNumber(int):
  'immutable'
  def __new__(cls, number):
    if not isinstance(number, int):
      raise TypeError
    if number < 0 or number > 65535:
      raise ValueError
    self = int.__new__(PortNumber, number)
    return self

class UDPPort(PortNumber):pass
class TCPPort(PortNumber):pass


class Packet(object):
  def __init__(self, src, dest, port=None):
    self.src = src
    self.dest = dest
    self.port = port
    self._hops = []


class DestinationUnreachable(Exception):pass
class DestinationNotFound(Exception):pass


class Network(object):
  def __init__(self):
    self.pots = []
  def add(self, pot):
    self.pots.append(pot)
  def tick(self):
    for pot in self.pots:
      pot.on_tick()
  def verify(self):
    pass
  def make_segment(self, addr, mask):
    seg = Segment(addr, mask)
    self.add(seg)
    return seg

  def make_interface(self, seg, machine, addr, mask, *args, **kw):
    ni = NetworkInterface(seg, machine, addr, mask, *args, **kw)
    self.add(ni)
    seg.add(ni)
    machine.add(ni)
    return ni
    

class Pot(object):
  def __init__(self):
    self.packets = []

  def on_tick(self):
    if not self.packets:
      return
    p = self.packets.pop()
    self.handle(p)

  def receive(self, packet):
    self.packets.append(packet)

  def handle(self, p):
    pass


class Segment(Pot):
  def __init__(self, addr, mask):
    super(Segment, self).__init__()
    self.addr = addr
    self.mask = mask
    self.nis = []

  def add(self, ni):
    self.nis.append(ni)

  def handle(self, packet):
    '''dumb hub model'''
    for ni in self.nis: 
      ni.receive(packet)

  def __contains__(self, addr):
    return (self.addr & self.mask) == (addr & self.mask)


class Uplink(Pot):
  def __init__(self):
    super(Uplink, self).__init__()
    self.nis = []


class NetworkInterface(Pot):
  def __init__(self, seg, owner, addr, mask, *args, **kws):
    super(NetworkInterface, self).__init__()
    self.segment = seg
    self.owner = owner
    self.addr = addr
    self.mask = mask

  def __repr__(self):
    return '<NetworkInterface addr=%s/mask=%s>'%(self.addr, self.mask)

  def handle(self, packet):
    if packet.dest == self.addr:
      if self.owner:
        self.owner.receive(self, packet)

  def send(self, packet):
    self.segment.receive(packet)


class Consumer(object):
  def consume(self, packet):
    pass

class Machine(Consumer):
  def __init__(self):
    super(Machine, self).__init__()
    self.nis = []

  def add(self, ni):
    self.nis.append(ni)

  def receive(self, ni, packet):
    assert packet.dest == ni.addr
    self.consume(packet)


class Router(Machine):
  def __init__(self):
    super(Router, self).__init__()
    self.routes = {}

  def receive(self, ni, packet):
    '''\
    very dumb routing. 
    Able to handle single hop only.
    '''
    for i in self.nis:
      if packet.dest in i.segment.addr:
        i.segment.receive(packet)
        return
    self.consume(packet)


class VirtualMachine(Machine):
  pass

class Service(Machine):pass



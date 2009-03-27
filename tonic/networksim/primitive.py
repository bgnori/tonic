#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

__all__ = ['itom', 'mtoi',
           'IPv4Addr', 'IPv4Mask', 'TCPPort', 'UDPPort',
           'Request', 'NetworkInterface', 'Machine', 'Router',
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


class QuadByte(object):
  __slots__ = ('_value',)
  def __new__(cls, v):
    assert isinstance(v, str)
    assert len(v) == 4
    self = object.__new__(QuadByte)
    self._value = v
    return self

  def __and__(self, other):
    s = socket.ntohl(struct.unpack('<I', self._value)[0])
    o = socket.ntohl(struct.unpack('<I', other._value)[0])
    return QuadByte(struct.pack('<I', socket.htonl(s&o)))

  def __eq__(self, other):
    return self._value == other._value


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
  __slots__ = ('_number')
  def __new__(cls, number):
    if not isinstance(number, int):
      raise TypeError
    if number < 0 or number > 65535:
      raise ValueError
    #self = object.__new__(cls) is not safe, since int is embeded type.
    self = int.__new__(PortNumber)
    self._number = number
    return self

class UDPPort(PortNumber):pass
class TCPPort(PortNumber):pass


class Request(object):
  def __init__(self, src, dest, port=None):
    self.src = src
    self.dest = dest
    self.port = port
    self._hops = []
  def hop(self, ni):
    self._hops.append(ni)


class DestinationUnreachable(Exception):pass
class DestinationNotFound(Exception):pass


class Segment(object):
  def __init__(self, addr, mask):
    self.addr = addr
    self.mask = mask
    self.nis = []

  def connect(self, ni):
    self.nis.append(ni)
    ni.set_segment(self)

  def receive(self, request):
    found = False
    for ni in self.nis:
      found |= ni.receive(request) #FIXME stack may be too deep
    if not found:
      raise DestinationNotFound

  def __contains__(self, addr):
    return (self.addr & self.mask) == (addr & self.mask)


class Uplink(Segment):
  def __init__(self):
    self.nis = []


class NetworkInterface(object):
  def __init__(self, owner, addr, mask, *args, **kws):
    self.owner = owner
    self.addr = addr
    self.segment = None

  def set_segment(self, segment):
    self.segment = segment

  def receive(self, request):
    if request.dest == self.addr:
      if self.owner:
        return self.owner.receive(self, request)
      return True
    return False


class Network(object):
  def __init__(self, **kws):
    self.__dict__.update(kws)

  #def __getattr__(self, name):

  def verify(self):
    pass


class Machine(object):
  def __init__(self):
    self.nis = []

  def make_interface(self, addr, mask, *args, **kw):
    ni = NetworkInterface(self, addr, mask, *args, **kw)
    self.nis.append(ni)
    return ni

  def receive(self, ni, request):
    return request.dest == ni.addr

class Router(Machine):
  def __init__(self):
    super(Router, self).__init__()
    self.routes = {}

  def receive(self, ni, request):
    if super(self).receive(ni, request):
      return True
    for i in self.nis:
      if request.addr in i.segment.addr:
        return i.segment.receive(request)
    return True

class VirtualMachine(Machine):
  pass

class Service(Machine):pass



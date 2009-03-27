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

class IPv4Addr(object):
  'singleton and immutable'
  __slots__ = ('_numeric',)
  _bag = {}
  def __new__(cls, presentation):
    if presentation not in cls._bag:
      self = object.__new__(cls)
      self._numeric = socket.inet_pton(socket.AF_INET, presentation)
      cls._bag.update({presentation:self})
    return cls._bag[presentation]

class IPv4Mask(object):
  'immutable'
  __slots__ = ('_numeric', '_mask')
  def __new__(cls, mask):
    self = object.__new__(cls)
    if isinstance(mask, int):
      self._mask = itom(mask)
    elif isinstance(mask, str):
      self._mask = socket.inet_pton(socket.AF_INET, mask)
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
  def __init__(self, *args):
    self.nis = list(args)
  def connect(self, ni):
    self.nis.append(ni)
  def receive(self, request):
    found = False
    for ni in self.nis:
      found |= ni.receive(request) #FIXME stack may be too deep
    if not found:
      raise DestinationNotFound


class NetworkInterface(object):
  def __init__(self, owner, addr, mask, *args, **kws):
    self.owner = owner
    self.addr = addr

  def receive(self, request):
    if request.dest == self.addr:
      if self.owner:
        return self.owner.receive(self, request)
      return True
    return False

class Uplink(Segment):
  pass

class Network(object):
  def __init__(self, **kws):
    self.__dict__.update(kws)

  #def __getattr__(self, name):

  def verify(self):
    pass




class Machine(object):
  def make_interface(self, addr, mask, *args, **kw):
    ni = NetworkInterface(self, addr, mask, *args, **kw)
    self.register(ni)
    return ni

  def register(self, ni):
    pass
  def receive(self, ni, request):
    return True

class Router(Machine):
  def __init__(self):
    self.nis = []
    self.routes = {}

  def register(self, ni):
    self.nis.append(ni)
    #self.routes = 

  def receive(self, ni, request):
    return True

class VirtualMachine(Machine):
  pass

class Service(Machine):pass




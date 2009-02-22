#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#
import struct

bits_in_byte = 8 # 1 byte == 8 bits

def byte_length(length_in_bit):
  if length_in_bit % bits_in_byte:
    roundup = 1
  else:
    roundup = 0
  return length_in_bit / bits_in_byte + roundup


class BitsArray(object):
  struct_format = '!B'
  def __init__(self, size, binary=None, endian=None):
    self.size = size
    if binary: 
      if len(binary) > byte_length(size):
        raise ValueError('spilling data, %i byte is too long for array size %i bits !'
                         %(len(binary), size))
      self.binary = binary
    else:
      self.binary = '\x00'*byte_length(self.size)
    if endian:
      self.endian = endian
    else:
      self.endian = '<' # little endian

  def __len__(self):
    return self.size

  def int(self):
    ret = 0
    mask = 1
    for bit in self:
      if bit:
        ret |= mask
      mask = mask << 1
    return ret

  def _getbyte(self, pos_of_byte):
    return struct.unpack(self.struct_format, self.binary[pos_of_byte])[0]
  
  def _setbyte(self, pos_of_byte, value):
    self.binary = (self.binary[:pos_of_byte]
                   + struct.pack(self.struct_format, value) 
                   + self.binary[pos_of_byte+1:]
                   )[:self.size]

  def _pos_in_byte(self, nth):
    assert(isinstance(nth, int))
    assert(nth < bits_in_byte)
    assert(0 <= nth)
    if self.endian == '<':
      return nth%bits_in_byte
    elif self.endian == '>':
      return 7 - nth%bits_in_byte
    
  def _getpos(self, nth):
    assert(isinstance(nth, int))
    if 0 >  nth or nth >= self.size:
      raise IndexError('out of range')
    return (nth/bits_in_byte, self._pos_in_byte(nth%bits_in_byte))

  def getnth(self, nth):
    pos_of_byte, pos_in_byte = self._getpos(nth)

    byte = self._getbyte(pos_of_byte)
    if byte & 1 << pos_in_byte:
      return 1
    else:
      return 0

  def __getitem__(self, nth_or_slice):
    if isinstance(nth_or_slice, int):
      return self.getnth(nth_or_slice)
    elif isinstance(nth_or_slice, slice):
      assert(nth_or_slice.step is None)# or nth_or_slice.step == 1)
      assert isinstance(nth_or_slice.start, int)
      assert isinstance(nth_or_slice.stop, int)
      slice_length = nth_or_slice.stop - nth_or_slice.start
      ret = BitsArray(size=slice_length, 
                     endian=self.endian
                      )
      for i in range(ret.size):
        ret[i] = self.getnth(nth_or_slice.start + i)
      return ret
    else:
      raise TypeError('index must be int or slice, but got %s'%str(type(nth_or_slice)))

  def __setitem__(self, nth, value):
    assert(isinstance(nth, int))
    if not value in (0, 1):
      raise ValueError('value for asignment must be 0 or 1')
    pos_of_byte, pos_in_byte = self._getpos(nth)
    data = self._getbyte(pos_of_byte)

    if value:
      data |= 1 << pos_in_byte
    else:
      data &= ~(1 << pos_in_byte)

    self._setbyte(pos_of_byte, data)

  def __iter__(self):
    for i in range(self.size):
      yield self[i]

  def __repr__(self):
    return "<BitsArray Instance '%s'>"%(':'.join(map(str, list(self))))

  '''unsupported'''
  def __contains__(self, item):raise NotImplemented
  def __delitem__(self, key):raise NotImplemented
  def __add__(self, x):raise NotImplemented
  def __radd__(self, x):raise NotImplemented
  def __iadd__(self, x):raise NotImplemented
  def __mul__(self, x): raise NotImplemented
  def __rmul__(self, x): raise NotImplemented
  def __imul__(self, x): raise NotImplemented


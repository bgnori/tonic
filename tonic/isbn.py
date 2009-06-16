#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import sys
import re

class ISBN(object):
  @classmethod
  def isvalid(cls, s):
    d = cls.parse(s)
    if d is None:
      return False
    return d['check'] == cls.parity(d['value'])

  @classmethod
  def parse(cls, s):
    mo = cls.pattern.match(s)
    if mo is None:
      return None
    return mo.groupdict()

  def __new__(cls, s):
    self = object.__new__(cls)
    d = cls.parse(s)
    if d is None:
      raise ValueError
    if d['check'] != cls.parity(d['value']):
      raise ValueError

    self.value = d['value']
    self.check= d['check']
    return self

  def __hash__(self):
    return hash(self.value)


class ISBN10(ISBN):
  pattern = re.compile('(?P<value>\d{9})(?P<check>(\d|X))')

  @classmethod
  def parity(cls, s):
    parity = 0
    for i, d in enumerate(s[:9]):
      parity += int(d) * (10 - i)
    return '0123456789X0'[11 - ( parity % 11 )]


def convert(isbn10):
  assert isinstance(isbn10, ISBN10)
  c = "978" + isbn10.value + ISBN13.parity("978" + isbn10.value)
  return ISBN13(c)


class ISBN13(ISBN):
  pattern = re.compile('(?P<value>\d{12})(?P<check>\d)')
  @classmethod
  def parity(cls, s):
    parity = 0
    for i, d in enumerate(s):
      parity += int(d) * (1+2*(i%2))
    return '01234567890'[10 - ( parity % 10 )]





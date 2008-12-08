#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import re

EMPTY = r'($^)' #never match with anything.

class RegExpCompositionMeta(type):
  def __init__(cls,  name, bases, dictionary):
    assert 'regexp_str' not in cls.__dict__
    assert 'regexp' not in cls.__dict__
    base = cls.__base__
    first = cls._first 
    last = cls._last
    if base == object:
      cls.regexp_str = first + r'|' + last
    else:
      cls.regexp_str = first + r'|' + base.regexp_str + r'|' + last
    cls.regexp = re.compile(cls.regexp_str)


class LineParser(object):
  __metaclass__ = RegExpCompositionMeta
  name = '???'
  _first = EMPTY
  _last = EMPTY
  #_compiled = None
  def __init__(self, parent, debug=None):
    self.debug = debug
    self.parent = parent
    self.oninit()

  def oninit(self):pass
  def done(self):pass

  def parse(self, line):
    for matchobj in self.regexp.finditer(line):
      for name, match in matchobj.groupdict().items():
        if match:
          handler_name = 'handle_' + name
          handler = getattr(self, handler_name, None)
          if handler:
            if self.debug:
              print '  where:', line
              print ' envoke:', handler_name
              print '     by:', self
            handler(match, matchobj)


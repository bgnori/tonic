#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
__all__ = ['VisitBus', 'VisitPassenger']
import re
from tonic.cache import hub, memoize


@memoize(hub, lambda x: x)
def compile(xpath):
  assert isinstance(xpath, str)
  assert xpath.startswith('/')
  if xpath.endswith('<'):
    direction = '<'
    xpath = xpath[:-1]
  elif xpath.endswith('>'):
    direction = '>'
    xpath = xpath[:-1]
  else:
    '''defulat'''
    direction = '>'

  p = []
  for i, n in enumerate(xpath.split('/')):
    if i == 0:
      assert n == ''
      p.append('^')
    elif not n:
      p.append('((/[a-zA-Z][a-zA-Z0-9]*)*)')
    elif n == '*':
      p.append('(/[a-zA-Z][a-zA-Z0-9]*)')
    else:
      assert re.compile(n)
      p.append('/('+n+')')

  p = ''.join(p) + direction + '$'
  return re.compile(p)


def path2xpath(stack, direction):
  if direction == 'down':
    return '/' + '/'.join([node.tag for node in stack]) + '>'
  elif direction == 'up':
    return '/' + '/'.join([node.tag for node in stack]) + '<'
  else:
    assert False

class Requests(object):
  def __init__(self, *args):
    self._imp = dict(*args)

  def append(self, dest, p):
    rs = self._imp.get(dest, [])
    assert isinstance(rs, list)
    rs.append(p)
    self._imp.update({dest: rs})

  def remove(self, dest):
    del self._imp[dest]

  def match(self, xpath):
    '''
      remark: SRE object is hashable.
    '''
    for dest in self._imp:
      match = getattr(dest, 'match', None)
      if match and match(xpath):
        yield dest
      else:
        pass

  def __getitem__(self, dest):
    return self._imp[dest]

  def __contains__(self, dest):
    return dest in self._imp
    
  def get(self, dest, default=None):
    if default is not None and dest not in self._imp:
      src = default
    else:
      src = self._imp[dest]
    for r in src:
      yield r

  def pop(self, dest):
    self._imp.pop(dest)

  def keys(self):
    return self._imp.keys()

def merge(a, b):
  return Requests([
      (dest, list(a.get(dest, [])) + list(b.get(dest, [])))
        for dest in set(a.keys() + b.keys())
      ])



class VisitBus(object):
  def __init__(self, passengers):
    self.stack = []
    self.requests = self.dropin(passengers)
    # Every body get in, it is starting point

  def dropin(self, passengers):
    r = Requests()
    for p in passengers:
      assert isinstance(p, VisitPassenger)
      p.setresult(self.stack[:])
      try:
        dest = p.next()
      except StopIteration:
        continue
      r.append(dest, p)
    return r

  def dispatch(self, direction):
    r = Requests()
    for dest in list(self.requests.match(path2xpath(self.stack, direction))):
      passengers = self.requests[dest]
      r = merge(r, self.dropin(passengers))
      self.requests.remove(dest)
    self.requests = merge(self.requests, r)

  def visit(self, node):
    self.stack.append(node)
    self.dispatch('down')
    for n in node:
      self.visit(n)
    self.dispatch('up')
    self.stack.pop()


class VisitPassenger(object):
  def __init__(self):
    self.result = None
    try:
      self._itinerary = self.itinerary()
    except StopIteration:
      self._itinerary = None

  def next(self):
    if self._itinerary is None:
      raise StopIteration
    try:
      return compile(self._itinerary.next())
    except StopIteration:
      self._itinerary = None
      raise

  def setresult(self, stack):
    self.result = stack

  def getresult(self):
    return self.result

  def __iter__(self):
    return self

  def itinerary(self):
    raise StopIteration


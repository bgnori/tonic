#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import sys
import base


assert len(sys.argv) == 2
print '='*80
print '  parse  '
print '='*80
parser = base.Parser(debug=True)
source = file(sys.argv[1])
root = parser.parse(source)
source.close()

print '='*80
print '  visit  '
print '='*80

def visit(n, space):
  def usefulinfo(n):
    return n.get('name', None) or n.get('value', None) or n.text or 'nothing'
  print space, n.tag, usefulinfo(n)[:20]
  for c in n:
    visit(c, space+'  ')
visit(root, '')


#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#
import sha

def register(g):
  path = g["__file__"]
  if path.endswith("pyc") or path.endswith("pyo"):
    path = path[:-1]
  h = sha.new()
  for n in [path] + g.get("__moduleid_deps__", []):
    f = open(n, 'r+b') 
    try:
      for read in f.read():
        h.update(read)
    finally:
      f.close()
  g.update({'__moduleid__': h.hexdigest()})


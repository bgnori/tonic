#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

__all__ = ['getid', 'mergedid', 'onMANIFEST']

import git
import sha

repo = git.Repo()
master_head = repo.commits(max_count=1)[0]

def getid(path):
  b = git.Blob.blame(repo, master_head, path)[0][0]
  return b.id

def mergedid(*xs):
  h = sha.new()
  for path in xs:
    s = getid(path)
    b = s.decode('hex')
    h.update(b)
  return h.hexdigest()

def onMANIFEST(m=None):
  if m is None:
    m = 'MANIFEST'
  f = open(m)
  xs = [line[:-1] for line in f.readlines()]
  #xs = f.readlines()
  f.close()
  return mergedid(*xs)


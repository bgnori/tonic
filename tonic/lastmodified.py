#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

__all__ = ['getid']

import git

repo = git.Repo()
master_head = repo.commits(max_count=1)[0]

def getid(path):
  b = git.Blob.blame(repo, master_head, path)[0][0]
  return b.id


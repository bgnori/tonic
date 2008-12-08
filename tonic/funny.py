#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#


'''
WARN: 
This is almost no feature for testing.
If you want more features for testing, use Mock for testing.

Mock is available at
http://www.voidspace.org.uk/python/mock.html
'''

class LooseQuacker(object):
  '''Super loose duck typing QUACKS!'''
  def __init__(self, **kw):
    self.__dict__.update(kw)
  def __setattr__(self, name, value):
    self.__dict__.update({name:value})

if __name__ == '__main__':
  """
    Monty Python's Meaning Of Life(1983)
  """
  fish = LooseQuacker(greetings='Good morning!')
  tank = dict(TerryJones=fish,
              TerenceGilliam=fish,
              GrahamChapman=fish,
              JohnCleese=fish,
              EricIdle=fish,
              MichaelPalin=fish
              )

  for name, fish in tank.items():
    print name,':',  fish.greetings


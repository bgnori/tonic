#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

"""
  Monty Python's Meaning Of Life(1983)
"""
import unittest
from tonic.funny import *
class FishTest(unittest.TestCase):
  def test(self):
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


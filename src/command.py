# -*- coding: utf-8 -*-
class command(object):
  def __init__(self, main, mask, channel, message):
    self.main = main
    self.mask = mask
    self.channel = channel
    self.message = message

    self.do()

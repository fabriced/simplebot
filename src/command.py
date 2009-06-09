# -*- coding: utf-8 -*-
from settings import *

class command(object):
  chan = CHANNELS
  admin = ADMINS
  def __init__(self, main, mask, channel, message):
    self.main = main
    self.mask = mask
    self.channel = channel
    self.message = message

    self.do()
    
  def getChannels(self):
  	return self.chan
  	
  def getAdmins(self):
  	return self.admin
  	
  def setChannels(self, chans):
  	self.chan = chans
  	
  def setAdmins(self, admins):
  	self.admin = admins

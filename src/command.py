# -*- coding: utf-8 -*-
from settings import *

class command(object):
  chan = CHANNELS
  admin = ADMINS
  def __init__(self, main, mask, channel, message):
    self.main = main
    self.mask = mask
    self.channel = channel
    try:
      self.command, self.message = message.split(' ', 1)
    except ValueError:
      self.message = None
      self.command = message

    self.do()
    
  def getChannels(self):
  	return self.chan
  	
  def getAdmins(self):
  	return self.admin
  	
  def setChannels(self, chans):
  	self.chan = chans
  	
  def setAdmins(self, admins):
  	self.admin = admins


class multiCommand(command):

  def do(self):
    try:
      method_name = self.message.split()[0]
      method = self.__getattribute__(method_name)
      method()
    except:
      print "oops"


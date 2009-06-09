# -*- coding:utf-8 -*-

from command import command

class forum(command):
  def do(self): 
  	self.main.say('http://www.lanvegas.fr/punbb/', self.channel)

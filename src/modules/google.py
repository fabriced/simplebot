# -*- coding:utf-8 -*-

from command import command

class google(command):
  def do(self):
    if len(self.message.split(None, 1))>1:
      self.main.say('http://www.google.com/search?q=%s' % self.message.split(None, 1)[1], self.channel)
    else:
      self.main.say('http://www.google.com', self.channel)

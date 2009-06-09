# -*- coding:utf-8 -*-

from command import command

class google(command):
  def do(self):
    if self.message:
      self.main.say('http://www.google.com/search?q=%s' % self.message.replace(' ', '+'), self.channel)
    else:
      self.main.say('http://www.google.com', self.channel)

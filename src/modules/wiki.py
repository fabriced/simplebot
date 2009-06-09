# -*- coding:utf-8 -*-

from command import command

class wiki(command):
  def do(self):
    if len(self.message.split(None, 1))>1:
      self.main.say('http://fr.wikipedia.org/wiki/%s' % self.message.split(None, 1)[1], self.channel)
    else:
      self.main.say('http://fr.wikipedia.org', self.channel)

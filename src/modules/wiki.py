# -*- coding:utf-8 -*-

#TODO check the url for 404

from command import command

class wiki(command):
  def do(self):
    if self.message:
      self.main.say('http://fr.wikipedia.org/wiki/%s' % self.message.split()[0], self.channel)
    else:
      self.main.say('http://fr.wikipedia.org', self.channel)

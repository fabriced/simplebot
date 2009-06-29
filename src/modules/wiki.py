# -*- coding:utf-8 -*-

#TODO improve displayed url

from command import command

class wiki(command):
  def do(self):
    if self.message:
      self.main.say('http://fr.wikipedia.org/wiki/Special:Recherche?search=%s' % self.message.replace(' ', '+'), self.channel)
    else:
      self.main.say('http://fr.wikipedia.org', self.channel)
  def help(self):
    self.main.say('help!', self.channel)

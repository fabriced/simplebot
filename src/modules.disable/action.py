# -*- coding:utf-8 -*-

from lib.decorator import admin_required

from command import command

class action(command):

  @admin_required
  def do(self):
    place, phrase = self.message.split(' ', 1)
    self.main.send('PRIVMSG %s :\x01ACTION %s\n' % (place, phrase))

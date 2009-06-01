# -*- coding:utf-8 -*-

from lib.decorator import admin_required

from command import command

class action(command):

    @admin_required
    def do(self):
      place = self.message.split()[1]
      phrase = " ".join(self.message.split()[2:])
      self.main.send('PRIVMSG %s :\x01ACTION %s\n' % (place, phrase))


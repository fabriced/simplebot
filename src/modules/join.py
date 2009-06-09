#coding -*- utf-8 -*-

from command import command

from lib.decorator import admin_required

class join(command):

  @admin_required
  def do(self):
    if self.message:
      for chan in self.message.split():
        self.main.s.send("JOIN %s\n" % chan)
        self.setChannels(self.getChannels().append(chan))

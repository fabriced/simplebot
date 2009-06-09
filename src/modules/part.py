# -*- coding : utf-8 -*- 

from command import command

from lib.decorator import admin_required

class part(command):

  @admin_required
  def do(self):
    for chan in self.message.split():
      self.main.s.send("PART %s\n" % chan)
      self.setChannels(self.getChannels().remove(chan))

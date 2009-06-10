# -*- coding : utf-8 -*- 

from command import command
from lib.decorator import admin_required

class part(command):

  @admin_required
  def do(self):
    print self.channel
    if len(self.message.split(None, 1))>1:
      chan = self.message.split()[1]
    else:
      chan = self.channel
    self.main.s.send("PART %s\n" % chan)
    self.setChannels(self.getChannels().remove(chan))
      

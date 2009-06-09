#coding -*- utf-8 -*-

from command import command

from lib.decorator import admin_required

class join(command):

  @admin_required
  def do(self):
    if self.message.split()[1:]:
      self.main.s.send("JOIN %s\n" % self.message.split()[1])
      self.setChannels(self.getChannels().append(self.message.split()[1]))

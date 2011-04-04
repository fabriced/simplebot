# -*- coding : utf-8 -*- 

from command import command
from lib.decorator import admin_required

class part(command):

    @admin_required
    def __call__(self):
        for chan in self.message.split():
            self.server.send_msg("PART %s\n" % chan)
            # self.setChannels(self.getChannels().remove(chan))

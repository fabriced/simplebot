#coding -*- utf-8 -*-

from command import command

from lib.decorator import admin_required

class join(command):

    @admin_required
    def __call__(self):
        if self.message:
            for chan in self.message.split():
                self.server.send_msg("JOIN %s\n" % chan)

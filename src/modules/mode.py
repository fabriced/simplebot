# -*- coding:utf-8 -*-

from command import command
from lib.decorator import admin_required

class mode(command):

    @admin_required
    def __call__(self):
        self.server.send_msg('MODE %s\n' % self.message) 

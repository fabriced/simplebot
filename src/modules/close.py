# -*- coding: utf-8 -*-
import sys
from command import command
from lib.decorator import admin_required
import main
import time

class close(command):

    @admin_required
    def __call__(self):
        self.server.send_msg('QUIT :%s\n' % self.server.leaveMsg)

        # sleep pour éviter les Read error: EOF from client
        time.sleep(5.0)
        
        self.server.set_status(False)



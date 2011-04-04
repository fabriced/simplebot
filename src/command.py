# -*- coding: utf-8 -*-
from settings import *
from lib.utils import get_nick

class command(object):
    def __init__(self, server, event):
        self.server = server
        self.event = event
        
        self.mask = event.mask
        # self.user = get_nick(self.mask)[1:]
        self.user = get_nick(self.mask)
        if event.target == server.nick:
            self.channel = self.user
        else:
            self.channel = event.target
        self.message = " ".join(event.message.split()[1:])
        self.cmd = event.cmd
        self.responses = []

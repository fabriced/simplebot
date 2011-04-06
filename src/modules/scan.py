# -*- Coding: UTF-8 -*-

import time

from settings import *
from command import command
from lib.pyquake import *
from lib.utils import get_nick

NICK_PATTERN = re.compile( '\^.')

def format_nick(nick):
    """ format Quake 3 players nicknames to remove color infos """
    return NICK_PATTERN.sub('',nick)

def is_valid_ip(ip):
    pattern = re.compile(r'0*(?:25[0-5]|2[0-4]\d|1?\d{1,2})'
                                    r'(?:\.0*(?:25[0-5]|2[0-4]\d|1?\d{1,2})){3}$')
    return pattern.match(ip) is not None

def is_valid_port(p):
    port = int(p)
    return 0 < port and port < 2 ** 16


class scan(command):
    def __call__(self):
        user = get_nick(self.mask)
        self.channel = user

        mod_list = ['duel', '2v2', 'tdm', 'ffa', 'ctf']    

        param = self.message.split(' ')
        if param[0] in ['1v1', 'endif', 'end']:
            param[0] = 'duel'

        if param[0] in mod_list:
            # !scan modname [game]

            # parse le fichier servers.cfg
            f = open('./config/servers.cfg', 'r')
            servers = list()
            for line in f:
                servers.append(line.strip())
            f.close
            
            if len(param) > 1:
                game = param[1]
            else:
                game = None

            for server in servers:
                try:
                    if len(server) > 2:
                        s = server.split('|')
                        if game == None or game == s[0]:
                            if len(s) > 2:
                                self.give_stat(s[1], is_not_ip = False, game = s[0])
                except:
                    # oops, it failed
                    pass
        elif len(param[0]) > 1:
            # todo
            # !scan ip:port
            #try:
            #    self.give_stat(self.message, is_not_ip = False)
            #except:
            #    self.server.say('echec pour %s' % self.message, self.channel)
            #    pass
            print 'TODO: !scan ip:port'
            print 'DEBUG: len(param)| '+str(len(param))
        else:
            # !scan
            
            # parse le fichier servers.cfg
            f = open('./config/servers.cfg', 'r')
            servers = list()
            print 'DEBUG: servers'
            for line in f:
                servers.append(line.strip())
            f.close

            for server in servers:
                try:
                    if len(server) > 2:
                        s = server.split('|')
                        self.give_stat(s[1], is_not_ip = False, game = s[0])
                except:
                    # oops, it failed
                    pass


    def is_valid_address(self, ad):
        ip, port = ad.split(':')
        try:
            assert is_valid_ip(ip) == True
            assert is_valid_port(port) == True
        except:
            self.main.say('adresse invalide : %s' % ad, self.channel)
            return False
        return True


    def usage(self, server):
        self.main.say('usage :', self.channel)
        self.main.say(' ', self.channel)
        self.main.say(' !scan <serv>', self.channel)
        self.main.say(' ', self.channel)
        self.main.say(' serv list : %s' % ", ".join(server_dict.keys()), self.channel)


    def give_stat(self, server, is_not_ip = True, game = 'qw'):
        COLOUR_STYLE = ('\x034','\x03','\x039','\x03','\x0312','\x03')

        if game == 'qw':
                g = PyQuakeWorld(server, rcon_password='')
        if game == 'q3':
                g = PyQuake3(server, rcon_password='')
        if game == 'pk':
                g = PyPainkiller(server, rcon_password='')
        g.update()
        self.server.say('-> %s' % (g.__repr__() % COLOUR_STYLE), self.channel)

        if game == 'qw':
            if g.players:
                self.server.say('\x035     %s\x03' % ' '.join([p.name for p in g.players]), self.channel)
        if game == 'q3':
            if g.players:
                self.server.say('\x035     %s\x03' % ' '.join([format_nick(p.name) for p in g.players]), self.channel)
        time.sleep(1)
        

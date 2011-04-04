"""
Python Quake 3 Library
http://misc.slowchop.com/misc/wiki/pyquake3
Copyright (C) 2006-2007 Gerald Kaszuba

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA    02110-1301, USA.
"""

import socket
import re

class Player:
    def __init__(self, name, frags, ping, address=None, bot=-1):
        self.name = name
        self.frags = frags
        self.ping = ping
        self.address = address
        self.bot = bot
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

class QueryGame:
    def __init__(self, server, rcon_password=''):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_server(server)
        self.set_rcon_password(rcon_password)
    def set_server(self, server):
        try:
            self.address, self.port = server.split(':')
        except:
            raise Exception('Server address must be in the format of \
                            "address:port"')
        self.port = int(self.port)
        self.s.connect((self.address, self.port))
    def get_address(self):
        return '%s:%s' % (self.address, self.port)
    def set_rcon_password(self, rcon_password):
        self.rcon_password = rcon_password
    def send_packet(self, data):
        self.s.send('%s\n' % data)
    def recv(self, timeout=1):
        self.s.settimeout(timeout)
        try:
            return self.s.recv(4096)
        except socket.error, e:
            raise Exception('Error receiving the packet: %s' % e[1])
    def command(self, cmd, timeout=1, retries=3):
        while retries:
            self.send_packet(cmd)
            try:
                data = self.recv(timeout)
            except:
                data = None
            if data:
                return self.parse_packet(data)
            retries -= 1
        raise Exception('Server response timed out')


class PyPainkiller(QueryGame):
    def __init__(self, server, rcon_password=''):
        QueryGame.__init__(self, server,rcon_password)
        self.packet = '\xfe\xfd\x00    \xff\x00\x00'
    def parse_packet(self, data):
        return data.split('\x00')
    def update(self):
        data = self.command(self.packet)
        self.infos = data
    def __repr__(self):
        couleur = '%s'
        return '%s     %s    %s%s%s    map %s%s%s    with %s%s%s player(s).' % (self.get_address(),
                                                            self.infos[2],
                                                            couleur, self.infos[8],couleur,
                                                            couleur, self.infos[6],couleur,
                                                            couleur, self.infos[10], couleur)

class PyQuakeWorld(QueryGame):
    # source : http://www.quakebrasil.com.br/specs/qwspec11.html#MsgSpecial
    packet = '\xff\xff\xff\xff' + 'status'
    player_reo = re.compile(r'^(\d+) (\d+) (\d+) (\d+) "(.*)" "(.*)" (\d+) (\d+)')
    def __init__(self, server, rcon_password=''):
        QueryGame.__init__(self, server,rcon_password)
    def parse_packet(self, data):
        return data.split('\0')
    def update(self):
        data = self.command(self.packet)
        rawdata = data[0].split('\n')
        game_infos = rawdata[0].split('\\')[1:]
        self.player_rawdata = rawdata[1:-1]
        self.infos = dict([(game_infos[i], game_infos[i+1]) for i in range(0, len(game_infos), 2)])
        self.parse_players()
    def parse_players(self):
        # format \d \d \d \d \w \w \d \d
        # eg : 8 15 2 26 "gaz" "gaz" 4 4
        # ? frag ? ping "nick" "skin" color1 color2
        self.players = []

        for player in self.player_rawdata:
            if not player:
                continue
            match = self.player_reo.match(player)
            if not match:
                print 'WARNING: couldnt match', player
                continue
            foo, frags, id, ping, name, mystere, bar, baz = match.groups()
            self.players.append(Player(name, frags, ping))
    def __repr__(self):
        couleur = '%s'
        # print 'DEBUG serv_infos: %s' % self.infos
        return '%s  %s%s%s  map %s%s%s    with %s%s%s player(s).' % (self.get_address(), couleur, self.infos['hostname'], couleur,
                                                                     couleur, self.infos['map'], couleur,
                                                                     couleur, len(self.players), couleur)

class PyQuake3(QueryGame):
    packet_prefix = '\xff' * 4
    player_reo = re.compile(r'^(\d+) (\d+) "(.*)"')
    def __init__(self, server, rcon_password=''):
        QueryGame.__init__(self, server,rcon_password)
    def update(self):
        cmd, data = self.command(self.packet_prefix + 'getstatus')
        self.vars = self.parse_status(data)
    def rcon(self, cmd):
        r = self.command('rcon "%s" %s' % (self.rcon_password, cmd))
        if r[1] == 'No rconpassword set on the server.\n' or r[1] == \
                'Bad rconpassword.\n':
            raise Exception(r[1][:-1])
        return r
    def parse_packet(self, data):
        if data.find(self.packet_prefix) != 0:
            raise Exception('Malformed packet')
        first_line_length = data.find('\n')
        if first_line_length == -1:
            raise Exception('Malformed packet')
        response_type = data[len(self.packet_prefix):first_line_length]
        response_data = data[first_line_length+1:]
        return response_type, response_data
    def parse_status(self, data):
        split = data[1:].split('\\')
        values = dict(zip(split[::2], split[1::2]))
        # if there are \n's in one of the values, it's the list of players
        for var, val in values.items():
            pos = val.find('\n')
            if pos == -1:
                continue
            split = val.split('\n', 1)
            values[var] = split[0]
            self.parse_players(split[1])
        return values
    def parse_players(self, data):
        self.players = []
        for player in data.split('\n'):
            if not player:
                continue
            match = self.player_reo.match(player)
            if not match:
                print 'WARNING: couldnt match', player
                continue
            frags, ping, name = match.groups()
            self.players.append(Player(name, frags, ping))
    def rcon_update(self):
        cmd, data = self.rcon('status')
        lines = data.split('\n')
        players = lines[3:]
        self.players = []
        for p in players:
            while p.find('    ') != -1:
                p = p.replace('    ', ' ')
            while p.find(' ') == 0:
                p = p[1:]
            if p == '':
                continue
            p = p.split(' ')
            self.players.append(Player(p[3][:-2], p[0], p[1], p[5], p[6]))
    def __repr__(self):
        couleur = '%s'
        return '%s     %s%s%s    map %s%s%s    with %s%s%s player(s).' % (
                            self.get_address(),
                            couleur, self.vars['sv_hostname'], couleur,
                            couleur, self.vars['mapname'], couleur,
                            couleur, len(self.players), couleur)

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


# if __name__ == '__main__':
#    q = PyQuake3('88.191.79.170:27960', rcon_password='')
#    q.update()
#    print 'The name of %s is %s, running map %s with %s player(s).' % (q.get_address(), q.vars['sv_hostname'], q.vars['mapname'], len(q.players))
#    for player in q.players:
#        print '%s with %s frags and a %sms ping' % (player.name, player.frags, player.ping)
#    print q.__repr__()

    #g = PyQuakeWorld('qw-dev.net:27500', rcon_password='')
    # pk = PyQuakeWorld('qw-dev.net:28001', rcon_password='')
    # pk = PyQuakeWorld('77.74.194.189:27504', rcon_password='')
    #g.update()
    # print g.__repr__()
    #if g.players:
    #    for p in g.players:
    #        # print bytes.decode(p.name)
            # print to_unicode_or_bust(p.name)
    #        p.name.decode('cp1140')
    # andi
    # name = b'\x9c \xe1 \xee\xe4\xf9\x9c'
    # print name
    # print '\x9c'.decode('cp1252')

    # print name.decode('cp1140')
    # print name.decode('utf_8')
    # print '\x035     %s\x03' % ' '.join([chr(p.name) for p in g.players])
    # pk = PyQuakeWorld('188.165.243.56:28001', rcon_password='')
    # pk = PyQuakeWorld('188.165.243.56:27500', rcon_password='')
    # pk.update()
    # print pk.__repr__()

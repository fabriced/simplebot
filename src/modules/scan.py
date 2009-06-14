# -*- Coding: UTF-8 -*-

import time

from settings import *
from command import command
from lib.pyquake3 import *
from lib.utils import  get_nick

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
  def do(self):
    user = get_nick(self.mask)
    self.channel = user

    request_list = self.message and self.message.split() or None
    if not request_list:
      request_list = server_dict.keys()

    failed = []
    success = True
    for r in request_list:
      if r in server_dict.keys():
        try:
          self.give_stat(r)
        except:
          # oops, it failed
          pass
      elif self.is_valid_address(r):
        try:
          self.give_stat(r, is_not_ip = False)
        except:
          # oops, it failed
          pass
      else:
        failed.append(r)
        success = False
    if not success:
      self.main.say('echec pour %s' % ','.join(failed), self.channel)


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


  def give_stat(self, server, is_not_ip = True):
    COLOUR_STYLE = ('\x034','\x03','\x039','\x03','\x0312','\x03')
    if is_not_ip:
      game, ip = server_dict[server]
    else:
      game = 'q3'
      ip = server

    if game == 'q3':
        g = PyQuake3(ip, rcon_password='')
    if game == 'pk':
        g = PyPainkiller(ip, rcon_password='')
    g.update()
    self.main.say('%s -> %s' % (server,
                                g.__repr__() % COLOUR_STYLE),
                  self.channel)

    if game == 'q3':
        if g.players:
            self.main.say('\x035   %s\x03' % ' '.join([format_nick(p.name) for p in g.players]), self.channel)
    time.sleep(1)

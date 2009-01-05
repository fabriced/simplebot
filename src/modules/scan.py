#*-* Coding: UTF-8 *-*

import time

from settings import *
from lib.pyquake3 import *
from lib.utils import  get_nick


def format_nick(nick):
  """ format Quake 3 players nicknames to remove color infos """
  p = re.compile( '\^.')
  return p.sub('',nick)

class scan(object):
  def __init__(self, main, mask, channel, message):
    self.main = main
    self.user = get_nick(mask)
    self.channel = self.user
    request_list = message.split()[1:]
    if not request_list:
      request_list = server_dict.keys()


    failed = []
    success = True
    for r in request_list:
      if r in server_dict.keys():
        self.give_stat(r)
      else:
        failed.append(r)
        success = False
    if not success:
      self.main.say('echec pour %s' % ','.join(failed), self.channel)




  def usage(self, server):
    self.main.say('usage :', self.user)
    self.main.say(' ', self.user)
    self.main.say(' !scan <serv>', self.user)
    self.main.say(' ', self.user)
    self.main.say(' serv liste : %s' % ", ".join(server_dict.keys()), self.user)




  def give_stat(self, q3server):
    ip = server_dict[q3server]

    q = PyQuake3(ip, rcon_password='')
    q.update()
    self.main.say('%s -> %s   %s    map %s    with %s player(s).' %
                         (q3server,
                          q.get_address(),
                          q.vars['sv_hostname'],
                          q.vars['mapname'],
                          len(q.players)),
                          self.channel
                      )
    self.main.say('%s' % ' '.join([format_nick(p.name) for p in q.players]), self.channel)
    time.sleep(1)

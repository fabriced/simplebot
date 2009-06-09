# -*- coding:utf-8 -*-

import re
import random

from command import multiCommand
from lib.decorator import admin_required

set_pattern = re.compile('(?P<map>[-_\d\w]+) (?P<coeff>[\d]+)')

class NotMapAdminError(Exception):
  pass

maps = {'bardok-cpm' : 5, 'pornstar-redemption' : 5, 'pornstar-luckr': 0 }
map_list = ['blabla']


class pick_map(multiCommand):
#
#  def plouf(self):
#    print "yahoo"

  def get(self):
    phrase = map_list[ random.randint(0, len(map_list) -1)  ]
    self.main.send('PRIVMSG %s :%s\n' % (self.channel, phrase))

  @admin_required
  def set(self):
    match = set_pattern.search(self.message)
    if match:
      map, coeff = match.group('map', 'coeff')
      if int(coeff) == 0 and maps.has_key(map):
        del maps[map]
        return_msg = u'Map %s supprimée de la liste' % map
      else:
        print "else"
        maps[map] = coeff
        return_msg = u'Map %s ajoutée à la liste avec un coefficient de %s' % (map, coeff)
    else:
      # ca a pas matché
      return_msg = u'Erreur de syntaxe dans la ligne'

    self.main.send('PRIVMSG %s :%s\n' % (self.channel,return_msg))

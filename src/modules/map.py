# -*- coding= UTF-8 -*-

import urllib
import re

from command import command

pat = re.compile('download.php/(?P<map>[-\w]+).pk3')

class map(command):
  """ cherche jusque 5 maps sur q3a.ath.cx et retourne les liens correspondant """

  def do(self):
    for map in self.message.split()[1:]:
      data = urllib.urlencode({"map" : map, "fo" : "" })
      f = urllib.urlopen("http://q3a.ath.cx/index.php", data)
      result= f.read()
      f.close()

      if pat.search(result):
        map_url = "http://q3a.ath.cx/download.php/%s.pk3" % pat.search(result).group('map')
        ret_msg = "%s  -> %s" % (map,map_url)
      else:
        ret_msg = "Map not found : %s."% map

      self.main.say(ret_msg , self.channel)

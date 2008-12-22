# -*- coding= UTF-8 -*-

import urllib

class map(object):

  def __init__(self, main, mask, channel, message):
    self.main = main
    user = None
    for map in message.split()[1:]:
      data = urllib.urlencode({"map":map.replace('_','\_'),"fo": ""})
      f = urllib.urlopen("http://q3a.ath.cx/index.php", data)
      result= f.read()
      f.close()
      nb_result = result.count('download.php')
      if nb_result == 1:
        start = result.find('download.php')
        end = result.find('.pk3')
        map_url = "http://q3a.ath.cx/%s" % result[start:end + 4]
        self.main.say("%s  -> %s" % (map,map_url),  channel, user)
      elif nb_result < 1:
        self.main.say("Map not found : %s."% map, channel, user)
      elif nb_result > 1:
        self.main.say("%s : Trop de résultats pour cette map.i -> http://q3a.ath.cx/"% map, channel, user)


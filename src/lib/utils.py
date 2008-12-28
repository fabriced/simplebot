#*-* Coding: UTF-8 *-*



def get_nick(host):
  return host.split("!")[0]

def format_nick(nick):
  """ format Quake 3 players nicknames to remove color infos """
  p = re.compile( '\^.')
  return p.sub('',nick)

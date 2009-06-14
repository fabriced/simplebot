
HOST = "irc.quakenet.org"   # irc host server
PORT = 6667                 # irc port server
NICK = "nick"               # nick bot
IDENT = "ident"             # identiant bot
REALNAME = "realname"       # realname bot
LEAVE_MSG = ""              # leaving message bot
ADMINS = ""                 # list of admins eg: ["nick1.users.quakenet.org","nick2.users.quakenet.org"]
CHANNELS = ""               # list of channel to autojoin eg: ['#lanvegas','#doom3']
MODPATH = ""                # absolute or relative path to src/modules/

server_dict = None

# example
# server_dict = {
#               '1v1' :  ('q3', '88.191.79.170:27961'),
#               'ctf' :  ('q3', '88.191.79.170:27962'),
#               'pk' :   ('pk', '88.191.79.170:28666'),
#               }

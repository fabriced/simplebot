#*-* Coding: UTF-8 *-*

def get_nick(host):
    return host.split("!")[0][1:]
    
def is_onchan(nick, channel = None):
	return True

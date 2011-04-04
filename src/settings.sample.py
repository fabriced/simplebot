# Obtenir un compte Q sur Quakenet
# !say Q HELLO address@mail.com address@mail.com
# !say Q@CServe.quakenet.org AUTH username password 

servers = {'quakenet': 
            {'host': 'irc.quakenet.org', 
            'port': 6667, 
            'nick': 'botnick', 
            'identifiant': 'botid', 
            'realname': 'botrealname', 
            'autojoin': ["#botchannel"], 
            'username': None, 
            'password': None,
            'leaveMsg': 'low battery'
            },
#           'freenode': {'host': 'irc.freenode.net', 'port': 6667, 'nick': 'stupidbot'}
           }

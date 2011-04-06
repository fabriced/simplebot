# -*- coding:utf-8 -*-

from command import command
from lib.pyquake import *
from threading import Event, Thread, Timer
import threading
from lib.decorator import admin_required

class ech(command):
    def __call__(self):
          
        # si la commande n'est pas !ech add, mais juste !add
        if not self.cmd == 'ech':
            self.message = '%s %s' % (self.cmd, self.message)

        self.message = self.message.split()
        
        if len(self.message) < 1:
            return False

        # can't ask in pm
        if self.channel == self.user and self.message[0] != 'clear' :
            self.server.say('Ug ?', self.user)
            return False

        # définition du jeu utilisé par défaut sur le channel courant 
        self.games_list = []
        self.default_game = None
        f = open('./config/games.cfg', 'r')
        for line in f:
            if len(line) > 2:
                game = line.strip().split('|')
                self.games_list.append(game[0])
                if len(game) > 1:
                    if self.channel in game[1:]:
                        self.default_game = game[0]
        f.close
        
        if self.default_game == None:
            print 'WARNING: default_game not found in ./config/games.cfg for %s' % (self.channel)
            print 'WARNING: set instead "QW"'
            self.default_game = 'qw'


        if self.message[0] == 'add':
            # print 'DEBUG: !ech add [game] tdm'
            self.add()
        if self.message[0] == 'rm':
            # print 'DEBUG: !ech rm'
            self.rm()
        if self.message[0] == 'list':
            # print 'DEBUG: !ech list'
            self.list()
        if self.message[0] == 'ready':
            # print 'DEBUG: !ech ready'
            self.ready()
        if self.message[0] == 'clear':
            # print 'DEBUG: !ech clear'
            self.clear()
            
  
    def add(self):
        # !ech add [game] <mode>
        # ajoute le joueur X dans le mode souhaité
        
        # complete si [game] est manquant
        if len(self.message) == 3 and self.message[1] not in self.games_list:
            self.message[1] = self.default_game
        elif len(self.message) == 2:
            self.message.append(self.message[1])
            self.message[1] = self.default_game


        if not len(self.message) == 3:
            self.server.say('Usage: !add [game] <mode>', self.user)
            self.server.say('eg: !add tdm', self.user)
        else:
            # set irc serveur
            if self.server.host not in self.ech_dict:
                self.ech_dict[self.server.host] = {}

            # set irc channel
            if self.channel not in self.ech_dict.get(self.server.host):
                self.ech_dict[self.server.host][self.channel] = {}
                
            # set game
            if self.message[1] not in self.ech_dict.get(self.server.host).get(self.channel):
                self.ech_dict[self.server.host][self.channel][self.message[1]] = {}
                
            # set mode
            if self.message[2] == '1v1':
                self.message[2] = 'duel'
            if self.message[2] not in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]):
                self.ech_dict[self.server.host][self.channel][self.message[1]][self.message[2]] = []
            
            # set user
            if self.user not in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]):
                self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]).append(self.user)
                
                cnt = len(self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]))
                if cnt == 2 and self.message[2] in ['duel', 'end', 'endif']:
                    self.ready(self.message[1], self.message[2], auto = True)
                elif cnt == 4 and self.message[2] in ['2v2']:
                    self.ready(self.message[1], self.message[2], auto = True)
                elif cnt == 8 and self.message[2] in ['tdm', 'ctf']:
                    self.ready(self.message[1], self.message[2], auto = True)
                else:
                    self.list(self.message[1], self.message[2])
            else:
                self.server.say('Already in %s (%s)' % (self.message[2], self.message[1]), self.user)


    def rm(self, user = '', auto = False):
        # !ech rm [game] <mode>
        # retire le joueur X dans le mode souhaité
        if user == '':
            user = self.user
            
        try:
            _del = {}
            # !ech rm
            if len(self.message) == 1 or auto == True:
                # parcours chaque branche "jeu"
                for game, games in self.ech_dict.get(self.server.host).get(self.channel).iteritems():
                    # parcours chaque branche "mode"
                    for mode, users in games.iteritems():
                        if user in users:
                            # supprime l'utilisateur de la branche "mode"
                            users.remove(user)
                            if game not in _del:
                                # mémorise la branche "jeu"
                                _del[game] = []
                            if len(self.ech_dict.get(self.server.host).get(self.channel).get(game).get(mode)) == 0:
                                # mémorise les branches vides à néttoyer
                                _del.get(game).append(mode)
            else:
                # !ech rm [qw] tdm
                
                # complete si [game] est manquant
                if len(self.message) == 3 and self.message[1] not in self.games_list:
                    self.message[1] = self.default_game
                elif len(self.message) == 2:
                    self.message.append(self.message[1])
                    self.message[1] = self.default_game
                    
                # print 'DEBUG check game'
                if self.message[1] in self.ech_dict.get(self.server.host).get(self.channel):
                    # print 'DEBUG check mode'
                    if self.message[2] in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]):
                        # print 'DEBUG check user'
                        if user in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]):
                            # supprime l'utilisateur
                            # print 'DEBUG rm %s' % (user)
                            self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]).remove(user)
                            _del[self.message[1]] = []
                            if len(self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2])) == 0:
                                # mémorise les branches vides à nettoyer
                                _del.get(self.message[1]).append(self.message[2])


            # nettoyage des branches
            
            # print 'DEBUG # rm empty mode'
            for game, modes in _del.iteritems():
                for mode in modes:
                    self.ech_dict.get(self.server.host).get(self.channel).get(game).pop(mode)
                    
            # print 'DEBUG # rm empty game'
            for game in _del:
                if len(self.ech_dict.get(self.server.host).get(self.channel).get(game)) == 0:
                    self.ech_dict.get(self.server.host).get(self.channel).pop(game)
                    
            # print 'DEBUG # rm empty chan'
            if len(self.ech_dict.get(self.server.host).get(self.channel)) == 0:
                del self.ech_dict.get(self.server.host)[self.channel]
                
                # print 'DEBUG # rm empty serv'
                if len(self.ech_dict.get(self.server.host)) == 0:
                    del self.ech_dict[self.server.host]
        except:
            print 'WARNING: rm probleme ? pas de !add'
            
    def list(self, game = None, mode = None):
        # !ech list
        # liste tous les modes en cours

        if game == None or mode == None:
            # appel utilisateur
            message = ''
            try:
                # parcours chaque branche "jeu"
                for game in self.ech_dict.get(self.server.host).get(self.channel).keys():
                    # parcours chaque branche "mode"
                    for mode in self.ech_dict.get(self.server.host).get(self.channel).get(game).keys():
                        message += "%s (%s) [%i joueur(s)], " % (mode, game, len(self.ech_dict.get(self.server.host).get(self.channel).get(game).get(mode)))
                self.server.say('Liste: %s' % (message[:-2]), self.channel)
            except:
                self.server.say('Liste: aucun évènement', self.channel)
        else:
            # appel interne
            self.server.say('Joueur(s) inscrit(s) en %s (%s) : %s' % (mode, game, str(self.ech_dict.get(self.server.host).get(self.channel).get(game).get(mode))), self.user)
            
    def ready(self, game = None, mode = None, auto = False):
        # !ech ready [game] <mode>
        # lance l'event si le joueur[0] X le demande
        
        if auto == False:
            # !ech ready <qw> tdm
            try:
                # complete si [game] est manquant
                if len(self.message) == 3 and self.message[1] not in self.games_list:
                    self.message[1] = self.default_game
                elif len(self.message) == 2:
                    self.message.append(self.message[1])
                    self.message[1] = self.default_game
                if self.message[2] == '1v1':
                    self.message[2] = 'duel'
                
                if len(self.message) == 3:
                    # check game
                    if self.message[1] in self.ech_dict.get(self.server.host).get(self.channel):
                        # check mode
                        if self.message[2] in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]):
                            # définit l'owner (1er utilisateur dans la liste)
                            owner = self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2])[0]

                            if self.user == owner:
                                infos = self.get_infos()
                                self.server.say('Joueur(s) inscrit(s) en %s (%s) : %s' % (self.message[2], self.message[1], str(self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]))), self.channel)
                                if not infos == None:
                                    self.server.say('%s' % (infos), self.channel)
                                # supprime tous les utilisateurs présents dans d'autres évènements
                                for user in self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]):
                                    self.rm(user, auto = True)
                            else:
                                self.server.say('Seul %s peut taper la commande !ready %s' % (owner, self.message[1]), self.user)
            except:
                print 'WARNING: ready probleme ? pas de !add'
        else:
            # appel interne/automatique
            infos = self.get_infos()
            self.server.say('Joueur(s) inscrit(s) en %s (%s) : %s' % (self.message[2], self.message[1], str(self.ech_dict.get(self.server.host).get(self.channel).get(self.message[1]).get(self.message[2]))), self.channel)
            if not infos == None:
                self.server.say('%s' % (infos), self.channel)
            # supprime tous les utilisateurs présents dans d'autres évènements
            # fait un clone indépendant de la liste 
            users = self.ech_dict.get(self.server.host).get(self.channel).get(game).get(mode)[:]
            for user in users:
                self.rm(user, auto = True)
                
    @admin_required
    def clear(self):
        # reset les files d'attente d'un channel
        channel = self.message

        if len(channel) == 1:
            # channel[1] = self.channel
            channel.append(self.channel)
        elif len(channel) != 2:
            self.server.say('manque un paramètre', self.user)
            return False
        if channel[1] in self.ech_dict.get(self.server.host):
            del self.ech_dict.get(self.server.host)[channel[1]]
            if len(self.ech_dict.get(self.server.host)) == 0:
                del self.ech_dict[self.server.host]
        else:
            self.server.say('quel chan ?', self.user)

                
    def get_infos(self):
        # retourne un pool de maps et une ip d'un serveur libre
        ip = self.pick_server(game = self.message[1], mode = self.message[2])
        maps = self.pick_maps(game = self.message[1], mode = self.message[2])

        if not (ip == None and maps == None):
            infos = ''
            if ip != None:
                infos = 'Serveur: %s ' % (ip)
            if len(maps) > 0:
                infos += 'Maps suggérées: %s' % str(maps)
            return infos
        return None
                
    def pick_maps(self, game, mode, numof = 3):
        # retourne un pool de [numof] maps au hasard (ou une liste vide)
        if mode in ['1v1']:
            mode = 'duel'
        
        maps = []
        
        # à enlever pour que ça marche
        return maps

        f = open('./config/maps.cfg', 'r')
        for line in f:
            line = line.strip().split('|', 3)
            if line[0] == game and line[1] == mode:
                for map in line[2:]:
                    maps.append(map)
        f.close
        
        maps_list = []
        for i in range(numof):
            maps_list.append(maps[i])

        return maps_list

    def pick_server(self, game, mode):
        # retourne un serveur libre (ou None)
        if game == None:
            game = self.default_game
        if mode in ['endif', 'end', '1v1']:
            mode = 'duel'
        
        mod_list = ['duel', '2v2', 'tdm', 'ffa', 'ctf']
        game_list = ['qw', 'q3', 'pk']

        if game in game_list and mode in mod_list:
            
            # parse le fichier servers.cfg
            f = open('./config/servers.cfg', 'r')
            servers = list()
            for line in f:
                servers.append(line.strip())
            f.close

            # parcours tous les serveurs
            for server in servers:
                try:
                    if len(server) > 2:
                        s = server.split('|')
                        if game == s[0]:
                            if len(s) > 2:
                                for mode in s[2:]:
                                    if game == 'qw':
                                            g = PyQuakeWorld(s[1], rcon_password='')
                                    if game == 'q3':
                                            g = PyQuake3(s[1], rcon_password='')
                                    if game == 'pk':
                                            g = PyPainkiller(s[1], rcon_password='')
                                    g.update()
                                    # si il n'y a pas de joueurs, on retourne ce serveur
                                    if len(g.players) == 0:
                                        return s[1]
                                    time.sleep(1)
                except:
                    # oops, it failed
                    print "WARNING: oops, it failed"
                    pass
        return None

# static ech_dict
ech.ech_dict = {}

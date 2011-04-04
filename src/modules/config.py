# -*- coding:utf-8 -*-
from command import command
from lib.decorator import admin_required
import glob, os
# !config <type> add <value>
# !config <type> rm <value>
# !config <type>
# !config

class config(command):
    @admin_required
    def __call__(self):
       
        # commande disponible uniquement en mp
        if self.channel != self.user:
            return False
        
        message = self.message.split(' ', 3)
        print message
        if len(message) == 1:
            if message[0] == '':
                # !config
                self.listcfg()
            else:
                # !config <type>
                self.showcfg(message[0])
        elif len(message) == 3:
            # !config <type> add <value>
            # !config <type> rm <value>
            self.updatecfg(message[0], message[1], message[2])
            
    def listcfg(self):
        for dirname, dirnames, filenames in os.walk('./config'):
            for filename in filenames:
                self.server.say(filename[:-4], self.user)
    
    def showcfg(self, name):
        for dirname, dirnames, filenames in os.walk('./config'):
            if name+".cfg" in filenames:
                # liste les lignes dans .cfg
                f = open('./config/'+name+'.cfg', 'r')
                for line in f:
                    self.server.say(line, self.user)
                f.close

    def updatecfg(self, name, action, value):
        value = value.strip()
        if action == 'add':
            for dirname, dirnames, filenames in os.walk('./config'):
                if name+".cfg" in filenames:
                    # ajoute la ligne dans .cfg
                    f = open('./config/'+name+'.cfg', 'a+')
                    for line in f:
                        if value == line.strip():
                            self.server.say('impossible d\'ajouter une valeur déjà existante', self.user)
                            return False
                    f.write("%s\n" % value)
                    f.close
                    self.server.say('valeur ajoutée', self.user)
        elif action == 'rm':
            for dirname, dirnames, filenames in os.walk('./config'):
                if name+".cfg" in filenames:
                    # recherche la ligne à supprimer dans .cfg
                    f = open('./config/'+name+'.cfg', 'r')
                    newcfg = ''
                    for line in f:
                        if value == line.strip():
                            found = True
                        else:
                            newcfg += line
                    f.close
                    
                    # réécrit le fichier .cfg au besoin
                    if found == True:
                        f = open('./config/'+name+'.cfg', 'r+')
                        f.write(newcfg)
                        f.close
                        self.server.say('valeur supprimée', self.user)
                    else:
                        self.server.say('attention: valeur non supprimée', self.user)
        else:
            self.server.say('les actions possibles sont add et rm', self.user)



# -*- coding:utf-8 -*-

import time
import sqlite3
from datetime import date
from command import command
from settings import *

# return True if date string (DD/MM/YY or DD/MM/YYYY) is a valid date
def is_date(date):
  splitdate = date.split('/')
  if len(splitdate) == 3:
    if len(splitdate[2].strip()) == 2:
      splitdate[2] = '19'+splitdate[2].strip()
    try:
      date1 = (int(splitdate[2]), int(splitdate[1]), int(splitdate[0]), 0,0,0,0,0,0)
      date2 = time.localtime(date_to_timestamp(date))
      if date1[:2] != date2[:2]:
        return False
      else:
        return True
    except OverflowError:
      return False
  else:
    return False

# convert a date string (DD/MM/YY or DD/MM/YYYY) to unix timestamp
def date_to_timestamp(date):
  date = date.split('/')
  if len(date) == 3:
    if len(date[2].strip()) == 2:
      date[2] = '19'+date[2].strip()
    return time.mktime((int(date[2]), int(date[1]), int(date[0]), 0,0,0,0,0,-1))
  else:
    return False


class birth(command):
  def do(self):
    if not DBPATH or DBPATH == '':
      user = self.main.get_user_nick(self.mask)
      self.channel = user
      self.main.say('%s est mal configuré, veuillez contacter son administrateur' % NICK, self.channel)
        
    if self.main.is_onquakenet():
      if self.message and self.message.strip() == 'me':
        auth = self.main.is_auth_onquakenet(self.channel)
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        c.execute('SELECT SB.birthday FROM simplebot_users SU, simplebot_birthday SB WHERE SU.idUser = SB.idUser AND SU.auth LIKE \''+auth+'\'')
        idUser = c.fetchone()
        if idUser == None:
          self.main.say('Vous n\'avez pas donné votre anniversaire au bot %s' % NICK, self.channel)
        else:
          dt = date.fromtimestamp(idUser[0])
          birthday = str(dt.strftime("%A %d %B"))
          self.main.say('Votre anniversaire est le %s' % birthday, self.channel)
      elif self.message:
        user = self.main.get_user_nick(self.mask)
        self.channel = user
        auth = self.main.is_auth_onquakenet(self.channel)
        print auth
        if auth:
          if is_date(self.message):
            conn = sqlite3.connect(DBPATH)
            c = conn.cursor()
            c.execute('SELECT idUser FROM simplebot_users WHERE auth LIKE \''+auth+'\'')
            idUser = c.fetchone()
            
            if idUser == None:
                c.execute('INSERT INTO simplebot_users(auth,last_nick) VALUES(\''+auth+'\',\''+user+'\')')
                conn.commit()
                c.execute('SELECT idUser FROM simplebot_users WHERE auth LIKE \''+auth+'\'')
                idUser = str(c.fetchone()[0])
                
                c.execute('INSERT INTO simplebot_birthday VALUES('+date_to_timestamp(self.message)+','+idUser+')')
                conn.commit()
            else:
                idUser = str(idUser[0])
                c.execute('SELECT idUser FROM simplebot_birthday WHERE idUser = %s' % idUser)
                if c.fetchone() == None:
                    c.execute('INSERT INTO simplebot_birthday VALUES('+str(date_to_timestamp(self.message)+(24*60*60))+','+idUser+')')
                    conn.commit()
                else:
                    c.execute('UPDATE simplebot_birthday SET birthday = %s WHERE idUser = %s' % (str(date_to_timestamp(self.message)+(24*60*60)), idUser))
                    conn.commit()
            c.close()
            self.main.say('J\'ai bien enregistré ton anniversaire : le %s' % self.message, self.channel)
          else:
            self.main.say('Le format de la date doit être DD/MM/AAAA.', self.channel)
            self.main.say('Exemple : !birth 20/01/1990', self.channel)
        else:
          self.main.say('Vous devez être authentifié sur Quakenet pour pouvoir ajouter votre anniversaire', self.channel)
      else:
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        c.execute('SELECT SU.last_nick, strftime("%Y", SB.birthday, "unixepoch") FROM simplebot_birthday SB, simplebot_users SU WHERE SU.idUser=SB.idUser AND strftime(\'%d-%m\', SB.birthday, \'unixepoch\') = strftime(\'%d-%m\', datetime("now","localtime"))')
        birth = c.fetchall()
        if len(birth) > 0:
          annee = int(time.strftime('%Y', time.localtime()))
          chaine = ', à'.join(['%s (%s ans)' % (b[0], annee - int(b[1])) for b in birth ])
#          if len(birth) > 1:
#            nick = str(birth[0][0])
#            annee = int(birth[0][1])
#            i = 1
#            while i < len(birth):
#              if i+1 == len(birth):
#                nick = ' et à ' + str(birth[i][0])
#              else:
#                nick = nick + ', à ' + str(birth[i][0])
#              i = i + 1
#          else:
#            nick = str(birth[0][0])
          ret = chaine.encode('iso-8859-1', 'replace')
          self.main.say('Joyeux anniversaire à %s' % ret, self.channel) 
          c.close()
          return True
        
        c.execute('SELECT U.last_nick, strftime(\'%d/%m\',B.birthday,\'unixepoch\'), strftime(\'%Y\',current_date) FROM simplebot_birthday B, simplebot_users U WHERE U.idUser=B.idUser AND ((strftime(\'%m\', B.birthday, \'unixepoch\') = strftime(\'%m\', current_date) AND strftime(\'%d\', B.birthday, \'unixepoch\') >= strftime(\'%d\', current_date)) OR (strftime(\'%m\', B.birthday, \'unixepoch\') > strftime(\'%m\', current_date))) ORDER BY strftime(\'%m%d\',B.birthday,\'unixepoch\'), U.last_nick LIMIT 0,3')
        birth = c.fetchall()
        if len(birth) > 0:
          if len(birth) > 1:          
            nick = str(birth[0][0]) + ' (' + str(birth[0][1]) + '/'+str(birth[0][2])+')'
            i = 1
            while i < len(birth):
              str_birth = str(birth[i][0]) + ' (' + str(birth[i][1]) + '/'+str(birth[i][2])+')'
              if i+1 == len(birth):
                nick = nick + ' et de ' + str_birth
              else:
                nick = nick + ', de ' + str_birth
              i = i + 1
            self.main.say('Nous allons bientôt fêter les anniversaires de %s' % nick, self.channel) 
          else:
            str_birth = str(birth[0][1]) + '/'+str(birth[0][2])
            self.main.say('Nous fêterons bientôt l\'anniversaire de %s le %s' % (str(birth[0][0]), str_birth), self.channel) 
          c.close()
          return True
        self.main.say('Pas d\'anniv à venir', self.channel) 
        c.close()
    else:
      self.main.say('Command only available on quakenet servers', self.channel)


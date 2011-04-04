# -*- coding: utf-8 -*-

# from settings import ADMINS
from lib.exception import *

def admin_required(func):
    def check_admin(self):
        admins = []
        f = open('./config/admins.cfg', 'r')
        for line in f:
            if len(line) > 2:
                admins.append(line.strip())
        f.close
        
        if self.mask.split('@')[-1] in admins:
            func(self)
        else:
            # raise NotAdminError
            return False
    return check_admin

# autre decorateur pour faire la meme chose, mais avec un autre nom
devel = admin_required

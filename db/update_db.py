from genericpath import isdir
import urllib.parse
import os
import stat
import sys
from install_db import rmdir

'''
    DB_URI
'''

if __name__ == "__main__":

    rmdir('db')
    os.system(f'git clone https://github.com/reclada/db.git')
    os.chdir(os.path.join('db','update'))
    
    os.chdir('..')
    os.chdir('..')
    rmdir('db')
        
    

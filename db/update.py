from genericpath import isdir
import urllib.parse
import os
import stat
import sys
from install import rmdir,DB_URI


'''
    DB_URI
'''

if __name__ == "__main__":

    rmdir('db')
    os.system(f'git clone https://github.com/reclada/db.git')
    os.chdir(os.path.join('db','update'))
    #{ for debug
    #os.system(f'git checkout deployments')
    #} for debug
    os.rename('update_config_template.json', 'update_config.json')

    os.system(f'python update_db.py {DB_URI}')

    os.chdir('..')
    os.chdir('..')
    rmdir('db')
        
    

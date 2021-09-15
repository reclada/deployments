import urllib.parse
import os
import stat

def rmdir(top:str):
    if os.path.exists(top) and os.path.isdir(top):
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(top)

def create_db(DB_URI):
    constr = DB_URI

    res = os.popen(f'psql -c "select 1 as a;" {constr}').read()
    if res != '':
        raise Exception('Database already exist')

    def execute(cmd:str):
        os.system(f'psql -c "{cmd}" {constr}')
    
    db_name = DB_URI.split('/')[-1]
    constr = constr.replace(db_name,'postgres')
    
    execute(f'''CREATE DATABASE {db_name};''')


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    DB_URI = os.environ.get('DB_URI')
    parsed = urllib.parse.urlparse(DB_URI)
    DB_URI = DB_URI.replace(parsed.password, urllib.parse.quote(parsed.password))
    create_db(DB_URI)
    rmdir('artifactory')
    os.system(f'git clone https://github.com/reclada/artifactory.git')
    os.chdir('artifactory/db')

    os.system(f'psql -f install_db.sql {DB_URI} ')
    rmdir('artifactory')

    l_name = os.environ.get('LAMBDA_NAME')

    cmd = '''SELECT reclada_object.create('{"class": "Lambda","attributes": {"name": "#@#name#@#"}}'::jsonb);'''
    cmd = cmd.replace('#@#name#@#', l_name)

    os.system(f'psql -c "{cmd}" {DB_URI}')

    

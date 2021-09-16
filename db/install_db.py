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
    def exec_scalar(q:str):
        return os.popen(f'psql -P pager=off -c "{q}" {DB_URI}').readlines()[2].strip()

    res = exec_scalar("select version()")
    if not res.startswith("PostgreSQL"):
        raise Exception(f'Database {res} not supported')
    else:
        v = res.split()[1]
        v = list(map(int,v.split('.')))
        if (v[0] < 13) or (v[0] == 13 and v[1]<3):
            raise Exception(f'PostgreSQL must be 13.3 or upper version, current version: {res}')

    res = exec_scalar("select count(*) from pg_catalog.pg_namespace where nspname = 'reclada'")
    if res != '0':
        res = exec_scalar("SELECT max(ver) FROM dev.ver")
        raise Exception(f'Schema reclada already exist, version:{res}')
         

'''
    DB_URI
    LAMBDA_NAME
    CUSTOM_REPO_PATH
'''

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
    if l_name is not None:
        cmd = '''SELECT reclada_object.create('{\"class\": \"Lambda\",\"attributes\": {\"name\": \"#@#name#@#\"}}'::jsonb);'''
        cmd = cmd.replace('#@#name#@#', l_name)
        with open('tmp.sql','w') as f:
            f.write(cmd)
        cmd = f"psql -f tmp.sql {DB_URI}"
        os.system(cmd)
        os.remove('tmp.sql')
    
    print('instaling from CUSTOM_REPO_PATH/db')
    crp = os.environ.get('CUSTOM_REPO_PATH')+'\\db\\'
    os.chdir(crp)
    if crp is not None:
        os.system("chmod u+x install.sh")
        os.system("./install.sh")
        
        
    

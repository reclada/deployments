from genericpath import isdir
import urllib.parse
import os
import stat
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_URI = os.environ.get('DB_URI')
parsed = urllib.parse.urlparse(DB_URI)
DB_URI = DB_URI.replace(parsed.password, urllib.parse.quote(parsed.password))

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



def prepare_db(DB_URI, rms):
    def exec_scalar(q:str):
        return os.popen(f'psql -t -P pager=off -c "{q}" {DB_URI}').read().strip()

    DB_name = DB_URI.split('/')[-1]
    DB_URI_postgres = DB_URI.replace(DB_name,'')+'postgres'

    res = exec_scalar("select version()")
    if not res.startswith("PostgreSQL"):
        raise Exception(f'Database {res} not supported')
    else:
        v = res.split()[1]
        v = list(map(int,v.split('.')))
        if (v[0] < 13) or (v[0] == 13 and v[1]<3):
            raise Exception(f'PostgreSQL must be 13.3 or upper version, current version: {res}')

    for db_list_name in os.popen(f'psql -lqt {DB_URI_postgres}'):
        if db_list_name.split('|')[0].strip() == DB_name:
            if rms:
                cmd = f"psql -f drop_schema.sql {DB_URI}"
                os.system(cmd)
            else:
                res = exec_scalar("select count(*) from pg_catalog.pg_namespace where nspname = 'reclada'")
                if res != '0':
                    res = exec_scalar("SELECT max(ver) FROM dev.ver")
                    raise Exception(f'Schema reclada already exist, version:{res}')
            break
    else:
        print (f'Can\'t found {DB_name}')
        os.system(f'psql -c "CREATE DATABASE {DB_name}" {DB_URI_postgres}')
        print(f'Database {DB_name} created')
        

'''
    DB_URI
    LAMBDA_NAME
    CUSTOM_REPO_PATH
    ENVIRONMENT_NAME
'''

if __name__ == "__main__":

    rms = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'rm_schema':
            rms = True

    prepare_db(DB_URI, rms)
  
    rmdir('db')
    os.system(f'git clone https://github.com/reclada/db.git')
        
    os.chdir(os.path.join('db','update'))
    #{ for debug
    #os.system(f'git checkout deployments')
    #} for debug

    os.system(f'psql -f install_db.sql {DB_URI} ')
    os.rename('update_config_template.json', 'update_config.json')
    from db.update.update_db import json_schema_install,install_objects
    json_schema_install(DB_URI)

    e_name = os.environ.get('ENVIRONMENT_NAME')
    l_name = os.environ.get('LAMBDA_NAME')

    if l_name is not None and e_name is not None:
       install_objects(l_name,e_name,DB_URI)
    else:
        print('LAMBDA_NAME or ENVIRONMENT_NAME not found can not install objects (Context, Jobs)')

    os.chdir('..')
    os.chdir('..')

    rmdir('db')

    # check if we can run aws_lambda.invoke
    if os.popen(f'psql -t -P pager=off -c "SELECT COUNT(*) FROM pg_proc p JOIN pg_namespace n on p.pronamespace=n.oid WHERE n.nspname =\'aws_lambda\' and p.proname = \'invoke\' and not has_function_privilege(p.oid,\'execute\')" {DB_URI}').read().strip() != '0':
        raise Exception(f'User {parsed.username} should have GRANT to EXECUTE aws_lambda.invoke functions')
        exit()
    else:
        print (f'OK: User {parsed.username} has GRANT to EXECUTE aws_lambda.invoke functions')
    
    print('instaling from CUSTOM_REPO_PATH/db')
    crp = os.path.join(os.environ.get('CUSTOM_REPO_PATH'),'db')
    os.chdir(crp)
    if crp is not None:
        os.system("chmod u+x install.sh")
        os.system("./install.sh")
        
        
    

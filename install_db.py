import urllib.parse
import os

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

if __name__ == "__main__":
    DB_URI = os.environ.get('DB_URI')
    #'postgresql://reclada:fesge%46sfdf@dev-reclada-k8s.c9lpgtggzz0d.eu-west-1.rds.amazonaws.com:5432/dev3_reclada_k8s'
    parsed = urllib.parse.urlparse(DB_URI)
    DB_URI = DB_URI.replace(parsed.password, urllib.parse.quote(parsed.password))
    rmdir('artifactory')
    os.system(f'git clone https://github.com/reclada/artifactory.git')
    os.chdir('artifactory/db')

    os.system(f'psql {DB_URI} -f install_db.sql')


    
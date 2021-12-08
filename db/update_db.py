import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    DB_URI = os.environ.get('DB_URI')
    os.chdir('..')
    os.chdir('..')
    os.chdir('db')
    os.chdir('update')
    with open('update_config_template.json') as s, open('update_config.json','w') as d:
        for line in s:
            ll = ''
            if line.find('"db_URI"') > 0:
                line = f'"db_URI" : "{DB_URI}",'
            d.write(line)

    os.system('python update_db.py')
    
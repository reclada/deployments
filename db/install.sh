#!/bin/bash
python3 install_db.py
echo 'instaling from CUSTOM_REPO_PATH/db'
DB_URI_QUOTED=`python3 -c "import urllib.parse; parsed = urllib.parse.urlparse('$DB_URI'); print('$DB_URI'.replace(parsed.password, urllib.parse.quote(parsed.password)))"`
if [[ ! -z $CUSTOM_REPO_PATH ]]; then
  pushd $CUSTOM_REPO_PATH/db
  ./install.sh
  popd
end if
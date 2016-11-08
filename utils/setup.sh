#!/bin/bash

PROJECT_DIR=endojo
REPO_URL=https://github.com/hamasho/endojo

export LC_ALL=C

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip nginx libmysqlclient-dev \
    supervisor nodejs npm
sudo pip3 install -U pip3
sudo pip3 install virtualenv
cd ~
if [[ -d $PROJECT_DIR ]]; then
    cd ~/$PROJECT_DIR
    git pull origin master
else
    git clone $REPO_URL
    cd ~/$PROJECT_DIR
fi
[[ -f /usr/bin/node ]] || sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo npm install -g bower
bower install
virtualenv -p python3 venv
source venv/bin/activate
venv/bin/pip3 install -r requirements.txt

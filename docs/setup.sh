#!/bin/bash

PROJECT_DIR=endojo
REPO_URL=https://github.com/hamasho/endojo

apt-get update
apt-get upgrade -y
apt-get install -y python3 python3-pip nginx
pip3 install virtualenv
cd ~
if [[ -d $PROJECT_DIR ]]; then
    cd ~/$PROJECT_DIR
    git pull origin master
else
    git clone $REPO_URL
    cd ~/$PROJECT_DIR
fi
virtualenv -p python3 venv
source venv/bin/activate
venv/bin/activate/pip3 -r requirements.txt

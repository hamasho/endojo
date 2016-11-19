# TODOs
```sh
export DJANGO_SETTINGS_MODULE=endojo.settings.staging
venv/bin/python3 manage.py collectstatics
venv/bin/python3 manage.py makemigrations
venv/bin/python3 manage.py migrate
# if modified (in local)
# scp secrets.py
# bower install
# venv/bin/pip3 install -r requirements.txt
# sudo supervisorctl restart webserver-dev
# gulp init
```

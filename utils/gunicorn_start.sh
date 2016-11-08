#!/bin/bash

NAME="endojo-app"
DJANGO_DIR=/home/ubuntu/endojo
SOCK_FILE=$DJANGO_DIR/run/gunicorn.sock
N_WORKERS=3
DJANGO_WSGI_MODULE=endojo.wsgi

cd $DJANGO_DIR
source venv/bin/activate
export PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

RUNDIR=$(dirname $SOCK_FILE)
[[ -d $RUNDIR ]] || mkdir $RUNDIR

venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $N_WORKERS \
    --bind unix:$SOCK_FILE \
    --log-level debug \
    --log-file -

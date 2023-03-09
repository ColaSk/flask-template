# !/bin/bash
echo "SERVICE RUN STATUS: ONLINE !!!"

echo '################################ run migrations ################################'

cd app

export GLOBAL_CONF_PATH=configs/global-docker.conf
export FLASK_APP=app

flask db upgrade
gunicorn app:app -c configs/gunicornconf.py

#!/bin/sh

. ${OPTION_VENVDIR}/bin/activate
gunicorn hdlproxy.app:app \
    --bind=[::]:${OPTION_GUNICORN_PORT} \
    --workers=${OPTION_GUNICORN_WORKERS} \
    --worker-tmp-dir=/dev/shm \
    --log-file=- \
    --access-logfile=-
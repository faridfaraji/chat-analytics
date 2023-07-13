#!/bin/bash
echo 'starting gnicorn now'
gunicorn -w 2 -k gevent -b 0.0.0.0:$PORT --timeout 120 --forwarded-allow-ips="*" --log-level=info --error-logfile - --access-logfile - 'chat_analytics.app:create_app()'

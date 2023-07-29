#!/bin/bash
. activate chat-analytics
celery -A chat_analytics.celery.tasks beat --loglevel=info

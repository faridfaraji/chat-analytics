

from celery import Celery
from celery.schedules import schedule

from chat_analytics.config import config
from chat_analytics.adapter.database import DatabaseApiClient as db

from redis import Redis
import time
import logging
from chat_analytics.core.analyzer import analyze_conversations
from chat_analytics.core.filter.filter import get_artifact_size_confirmation, get_artifacts

# configure celery app with Redis as the message broker
app = Celery("analysis_tasks",
             broker=f"{config.celery_broker.url}/0",
             result_backend=f"{config.celery_broker.url}/0")
app.conf.task_default_queue = "analysis_tasks_queue"

redis_conn = Redis()

CONV_ANAL_TASK_QUEUE = "conversation_analysis_task_queue"
PERIOD_TIME = 90
BATCH_SIZE = 20


def get_queued_conversations(offset=0, limit=10):
    conversation_ids = redis_conn.zrange(CONV_ANAL_TASK_QUEUE, offset, limit)
    return [c.decode("utf-8") for c in conversation_ids]


def add_to_queue(conversation_id):
    get_artifact_size_confirmation(conversation_id, db.get_conversation_messages)
    if not redis_conn.zscore(CONV_ANAL_TASK_QUEUE, conversation_id):
        score = time.time()
        redis_conn.zadd(CONV_ANAL_TASK_QUEUE, {conversation_id: score})


@app.task
def save_conversation_analysis_task(conversation_id):
    return add_to_queue(conversation_id)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        PERIOD_TIME,
        process_bulk_tasks.s(),
    )


@app.task
def process_bulk_tasks():
    # process tasks here
    try:
        conversation_ids = get_queued_conversations(limit=BATCH_SIZE)
        conversation_ids = get_artifacts(conversation_ids, db.get_conversation_messages)
        print(conversation_ids)
        if conversation_ids:
            redis_conn.zrem(CONV_ANAL_TASK_QUEUE, *conversation_ids)
            print(conversation_ids)
            # conversation_ids = [c.decode("utf-8") for c in conversation_ids]
            analyze_conversations(conversation_ids)
    except Exception as e:
        logging.exception("could not process bulk tasks")
        for c in conversation_ids:
            add_to_queue(c)

from celery import Celery

from core.config import RABBITMQ_URL

worker = Celery(
    "tasks",
    broker=RABBITMQ_URL,
    backend="rpc://",
    include=["tasks.tasks"],
)

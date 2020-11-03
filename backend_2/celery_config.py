from celery import Celery
from kombu import Exchange, Queue


default_queue_name = 'default'
default_exchange_name = 'default'
default_routing_key = 'default'


add_queue_name ="add"
add_routing_key ="add"


celery_app = Celery('worker', broker='pyamqp://guest@localhost//')

default_exchange = Exchange(default_exchange_name, type='direct')

default_queue = Queue(
    default_queue_name,
    default_exchange,
    routing_key=default_routing_key)

add_queue = Queue(
    add_queue_name,
    default_exchange,
    routing_key = add_routing_key
)

celery_app.conf.task_queues = (default_queue, add_queue)

celery_app.conf.task_default_queue = default_queue
celery_app.conf.task_default_exchange = default_exchange_name
celery_app.conf.task_default_routing_key = default_routing_key

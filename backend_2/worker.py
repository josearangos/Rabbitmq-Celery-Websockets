
from celery.utils.log import get_task_logger
import time
from celery_config import celery_app

logger = get_task_logger(__name__)
#acks_late=True
try:
    import pika

except Exception as e:
    print("Sone Modules are missings {}".format_map(e))

class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):
        # Singelton Design Pattern  
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitmqConfigure(metaclass = MetaClass):
    def __init__(self, queue='hello',host='localhost', routingKey = 'hello',exchange='default'):
        self.queue=queue
        self.host=host
        self.routingKey = routingKey
        self.exchange = exchange

class RabbitMq():

    __slots__ = ["server","_channel","_connection"]

    def __init__(self,server):
        """
        :param server: Object of class RabbitmqConfigure
        """
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        print("__exit__")
        self._connection.close()



    def publish(self,payload = {}):
        """
        :param payload: JSON payload 
        :return: None

        """
        self._channel.basic_publish(exchange=self.server.exchange, routing_key=self.server.routingKey,body=str(payload))
        print("Published Message: {}".format(payload))



@celery_app.task(acks_late=True)
def add(x, y):
    res = x + y
    time.sleep(15)
    logger.info("Adding %s + %s, res: %s" % (x, y, res))

    #Finish work
    # Send results to consumer
    server = RabbitmqConfigure(queue='results',host='localhost', routingKey = 'results',exchange='default')
    with RabbitMq(server) as rabbitmq:
        rabbitmq.publish(payload={"Result":res})
        
    return res


